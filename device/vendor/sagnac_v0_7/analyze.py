#!/usr/bin/env python3
"""Raw-count validation and explicitly model-conditional CHSH diagnostics.

Standard library only. No efficiency compensation or background subtraction.
All outputs remain NOT_ASSESSED for physical quantum evidence.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

FORMAT = "sagnac.fixed_bins.v0.6"
U64_MAX = (1 << 64) - 1
COEFF = (1, 1, 1, -1)
ANGLES = ((0.0, 22.5), (0.0, -22.5), (45.0, 22.5), (45.0, -22.5))
FLAG_NAMES = ("counter_overflow", "time_order", "source_loss", "calibration_mismatch",
              "configuration", "event_kind_or_range", "control", "reserved")

class InvalidRecord(ValueError):
    pass

def uint(value, bits=64):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise InvalidRecord("integer or decimal string required")
    if isinstance(value, str) and (not value or not value.isascii() or not value.isdigit()):
        raise InvalidRecord("nonnegative decimal string required")
    number = int(value)
    if not 0 <= number < 1 << bits:
        raise InvalidRecord("integer outside declared range")
    return number

def local_symbol(mask, side):
    bits = (mask >> (2 * side)) & 3
    return ("0", "+", "-", "both")[bits]

def assigned_product(mask):
    # Predeclared deterministic rule: no click and both ports -> +1.
    return (-1 if local_symbol(mask, 0) == "-" else 1) * (-1 if local_symbol(mask, 1) == "-" else 1)

def validate(record):
    if not isinstance(record, dict) or record.get("format") != FORMAT:
        raise InvalidRecord("unknown snapshot format")
    if record.get("complete") is not True:
        raise InvalidRecord("incomplete snapshot")
    flags = uint(record.get("flags"), 8)
    if flags:
        raise InvalidRecord("RTL integrity flags: " + ",".join(n for i,n in enumerate(FLAG_NAMES) if flags & (1<<i)))
    if record.get("origin") not in ("synthetic", "hardware"):
        raise InvalidRecord("origin must be explicit")
    setting = uint(record.get("setting_index"), 2)
    cal = uint(record.get("calibration_id"), 32)
    cfg = record.get("configuration", {})
    if not isinstance(cfg, dict):
        raise InvalidRecord("configuration object required")
    start, stop, width = (uint(cfg.get(k)) for k in ("start_ps", "stop_ps", "window_ps"))
    if width == 0 or stop <= start or (stop-start) % width:
        raise InvalidRecord("invalid fixed-bin configuration")
    raw = record.get("counters")
    if not isinstance(raw, list) or len(raw) != 24:
        raise InvalidRecord("exactly 24 counters required")
    c = [uint(x) for x in raw]
    n = (stop-start)//width
    if c[16] != n or sum(c[:16]) != n:
        raise InvalidRecord("trial accounting identity failed")
    presence = [sum(c[m] for m in range(16) if m & (1<<ch)) for ch in range(4)]
    if any(c[18+ch] < presence[ch] for ch in range(4)):
        raise InvalidRecord("raw clicks smaller than occupied bins")
    extras = sum(c[18:22]) - sum(presence)
    if c[22] != extras or c[17] > min(n, extras) or ((c[17] == 0) != (extras == 0)):
        raise InvalidRecord("repeat accounting identity failed")
    if c[23] != sum(c[m] for m in range(16) if m & 3 == 3 or (m>>2) & 3 == 3):
        raise InvalidRecord("multiport accounting identity failed")
    return setting, cal, width, c

def correlation(positive, negative):
    n = positive + negative
    if n == 0:
        return {"n": 0, "E": None, "sigma_normal_approx": None}
    e = (positive-negative)/n
    # Do not publish a spurious zero uncertainty at empirical boundaries.
    sigma = math.sqrt(max(0.0, 1-e*e)/n) if min(positive, negative) >= 5 else None
    return {"n": n, "positive": positive, "negative": negative, "E": e,
            "sigma_normal_approx": sigma}

def summarize(record):
    setting,cal,width,c = validate(record)
    nine = {a+b: 0 for a in ("0","+","-") for b in ("0","+","-")}
    for m in range(16):
        a,b = local_symbol(m,0),local_symbol(m,1)
        if a != "both" and b != "both": nine[a+b] += c[m]
    pos,neg = c[5]+c[10],c[9]+c[6]
    assigned_pos = sum(c[m] for m in range(16) if assigned_product(m)==1)
    return {"setting_index":setting,"calibration_id":cal,"window_ps":width,
            "origin":record["origin"],"trials":c[16],"nine_categories":nine,
            "multiport_trials":c[23],"repeat_trials":c[17],"extra_same_channel_clicks":c[22],
            "repeat_fraction_observed":c[17]/c[16],
            "conditional_coincidences":correlation(pos,neg),
            "all_trials_fixed_assignment":correlation(assigned_pos,c[16]-assigned_pos)}

def combine(correlations, alpha):
    if any(x["E"] is None for x in correlations):
        return {"status":"INSUFFICIENT_DATA","S":None,"singlet_T_lower_hoeffding":None,
                "model_conditional_gate":False}
    s = sum(k*x["E"] for k,x in zip(COEFF,correlations))
    # Singlet sign chosen before acquisition; no data-dependent abs(S) choice.
    t = -s
    margin = sum(math.sqrt(2*math.log(4/alpha)/x["n"]) for x in correlations)
    lower = t-margin
    sigmas = [x["sigma_normal_approx"] for x in correlations]
    sigma = math.sqrt(sum(x*x for x in sigmas)) if all(x is not None for x in sigmas) else None
    return {"status":"MODEL_CONDITIONAL_DIAGNOSTIC","S":s,"singlet_T":t,
            "sigma_normal_approx":sigma,"singlet_T_lower_hoeffding":lower,
            "hoeffding_alpha":alpha,"model_conditional_gate":lower>2,
            "normal_3sigma_gate":None if sigma is None else t-3*sigma>2}

def analyze(records, alpha=0.0027):
    if not isinstance(alpha,(int,float)) or isinstance(alpha,bool) or not math.isfinite(alpha) or not 0<alpha<1:
        raise InvalidRecord("alpha must be strictly between zero and one")
    if not isinstance(records,list) or len(records)!=4:
        raise InvalidRecord("exactly four independent setting records required")
    summaries = sorted((summarize(r) for r in records),key=lambda x:x["setting_index"])
    if [x["setting_index"] for x in summaries] != [0,1,2,3]:
        raise InvalidRecord("settings must occur exactly once")
    if len({(x["calibration_id"],x["window_ps"],x["origin"]) for x in summaries})!=1:
        raise InvalidRecord("incompatible calibration, time-bin width or provenance")
    return {"format":"sagnac.analysis.v0.6","integrity":"VALIDATED_COUNTER_IDENTITIES",
            "physical_quantum_claim":"NOT_ASSESSED","origin":summaries[0]["origin"],
            "protocol":"CHSH_PSI_MINUS_V1","analyzer_angles_degrees":ANGLES,
            "sign_convention":"S=E00+E01+E10-E11; T=-S (predeclared singlet)",
            "settings":summaries,
            "conditional_coincidences":combine([x["conditional_coincidences"] for x in summaries],alpha),
            "all_trials_fixed_assignment":combine([x["all_trials_fixed_assignment"] for x in summaries],alpha),
            "assumptions_not_tested":["correct detector and analyzer calibration",
               "independent identically distributed trials within each setting for stated bounds",
               "independence of settings from source; stationarity across separate blocks",
               "representative coincident subset (fair sampling) for conditional result",
               "physical locality and freedom-of-choice conditions are not established"],
            "processing":{"background_subtraction":False,"efficiency_compensation":False,
                          "automatic_five_percent_rejection":False,"data_selected_window":False}}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input",type=Path,help="JSON containing four snapshots under records")
    parser.add_argument("--output",required=True,type=Path)
    parser.add_argument("--alpha",type=float,default=0.0027)
    args=parser.parse_args()
    try:
        data=args.input.read_bytes(); obj=json.loads(data)
        result=analyze(obj["records"],args.alpha)
        result["input_sha256"]=hashlib.sha256(data).hexdigest()
        status=0
    except (InvalidRecord,KeyError,TypeError,ValueError,OSError) as exc:
        result={"integrity":"INVALID_OR_UNREADABLE","reason":str(exc),
                "physical_quantum_claim":"NOT_ASSESSED"}; status=2
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    return status

if __name__=="__main__":
    raise SystemExit(main())
