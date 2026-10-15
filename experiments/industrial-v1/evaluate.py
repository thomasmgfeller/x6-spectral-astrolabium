"""Offline V1-D result evaluator. No supplied confidence interval or PASS is trusted.

Input records are independent bearing units, not overlapping windows. The
confidence procedure is exact binomial with a conservative paired-difference
bound. Read README.md for scope, assumptions and unsupported routes.
"""
import argparse
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker
from scipy.stats import beta

ROOT = Path(__file__).resolve().parent
MAX_JSON = 16*1024*1024


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def strict_json(raw):
    if len(raw) > MAX_JSON:
        raise ValueError("JSON_SIZE_LIMIT")
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result:
                raise ValueError("DUPLICATE_JSON_KEY")
            result[k] = v
        return result
    def invalid(value):
        raise ValueError("NON_FINITE_JSON")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=invalid)
    def walk(x):
        if isinstance(x, float) and not math.isfinite(x):
            raise ValueError("NON_FINITE_NUMBER")
        if type(x) is int and abs(x) > 2**53-1:
            raise ValueError("NON_INTEROPERABLE_INTEGER")
        if isinstance(x, dict):
            for v in x.values():
                walk(v)
        if isinstance(x, list):
            for v in x:
                walk(v)
    walk(value)
    return value


def read(path):
    path = Path(path)
    if path.stat().st_size > MAX_JSON:
        raise ValueError("JSON_SIZE_LIMIT")
    raw = path.read_bytes()
    return strict_json(raw), digest(raw)


def validate(value, kind):
    schema = json.loads((ROOT/"schema"/(kind+".schema.json")).read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(value)


def local_file(root, ref):
    root = Path(root).resolve()
    part = Path(ref["path"])
    if part.is_absolute() or ".." in part.parts:
        raise ValueError("UNSAFE_REFERENCE_PATH")
    p = root/part
    if any(parent.is_symlink() for parent in [p, *p.parents] if parent != root.parent):
        raise ValueError("SYMLINK_REFERENCE")
    if not p.resolve().is_relative_to(root) or not p.is_file():
        raise ValueError("MISSING_REFERENCE: "+ref["path"])
    if p.stat().st_size > 256*1024*1024:
        raise ValueError("REFERENCE_SIZE_LIMIT")
    h = hashlib.sha256()
    with p.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b""):
            h.update(chunk)
    if h.hexdigest() != ref["sha256"]:
        raise ValueError("REFERENCE_HASH_MISMATCH: "+ref["path"])
    return p


def samples(path, count):
    import array
    if path.stat().st_size != count*4:
        raise ValueError("SAMPLE_SHAPE_OR_DTYPE_MISMATCH")
    values = array.array("f")
    with path.open("rb") as stream:
        values.fromfile(stream, count)
    if sys.byteorder != "little":
        values.byteswap()
    if any(not math.isfinite(v) for v in values):
        raise ValueError("NON_FINITE_SAMPLE")
    return values


def peak(values, window):
    start, end = window
    if not 0 <= start < end <= len(values):
        raise ValueError("INVALID_PEAK_WINDOW")
    amplitude = max(values[start:end])
    indices = [i for i in range(start, end) if values[i] == amplitude]
    if len(indices) != 1:
        raise ValueError("AMBIGUOUS_PEAK_LOCATION")
    return amplitude, indices[0]


def readiness(profile, root):
    validate(profile, "profile")
    missing = []
    if profile["status"] != "FROZEN" or profile["frozen_utc"] is None:
        missing.append("PROFILE_NOT_FROZEN")
    for k, v in profile["processing"].items():
        if v is None:
            missing.append("processing."+k)
    for k in ("min_positive_units", "min_negative_units"):
        if profile["statistics"][k] is None:
            missing.append("statistics."+k)
    if profile["statistics"]["sensitivity_gain_min"] <= 0:
        missing.append("POSITIVE_GAIN_MARGIN_REQUIRED")
    if profile["statistics"]["sensitivity_min"] <= 0:
        missing.append("POSITIVE_SENSITIVITY_FLOOR_REQUIRED")
    ids = [c["id"] for c in profile["preservation_cases"]]
    if len(set(ids)) != len(ids):
        raise ValueError("DUPLICATE_PRESERVATION_CASE")
    for role, ref in profile["references"].items():
        if ref is None:
            missing.append("references."+role)
        else:
            local_file(root, ref)
    for case in profile["preservation_cases"]:
        path = local_file(root, case["reference"])
        if case["reference_kind"] == "DESIGN_ONLY":
            missing.append("preservation_reference_not_materialized:"+case["id"])
        else:
            amplitude, index = peak(samples(path, case["sample_count"]), case["peak_window"])
            if not math.isclose(amplitude, case["reference_amplitude"], rel_tol=1e-7) or index != case["reference_sample"]:
                raise ValueError("PRESERVATION_REFERENCE_METADATA_MISMATCH")
    return missing


def cp_bounds(k, n, alpha):
    """Each endpoint is a one-sided 1-alpha Clopper-Pearson bound."""
    if type(k) is not int or type(n) is not int or not 0 <= k <= n or n <= 0 or not 0 < alpha < 1:
        raise ValueError("INVALID_BINOMIAL_COUNTS")
    return (0.0 if k == 0 else float(beta.ppf(alpha, k, n-k+1)),
            1.0 if k == n else float(beta.ppf(1-alpha, k+1, n-k)))


def paired_bounds(wins, losses, n, alpha):
    if wins+losses > n:
        raise ValueError("INVALID_PAIRED_COUNTS")
    wlo, whi = cp_bounds(wins, n, alpha/2)
    llo, lhi = cp_bounds(losses, n, alpha/2)
    return max(-1.0, wlo-lhi), min(1.0, whi-llo)


def bound_gate(interval, threshold, direction, strict=False):
    lo, hi = interval
    if direction == "lower":
        passed = lo > threshold if strict else lo >= threshold
        failed = hi <= threshold if strict else hi < threshold
    else:
        passed, failed = hi <= threshold, lo > threshold
    return "PASS" if passed else "FAIL" if failed else "INCONCLUSIVE"


def diagnostic_gates(stats, positive, negative, true_positive, false_positive, wins, losses):
    alpha = stats["family_alpha"]/stats["registered_claim_count"]
    sensitivity = cp_bounds(true_positive, positive, alpha)
    false_alarm = cp_bounds(false_positive, negative, alpha)
    gain = paired_bounds(wins, losses, positive, alpha)
    gates = {"sensitivity": bound_gate(sensitivity, stats["sensitivity_min"], "lower"),
             "false_positive_rate": bound_gate(false_alarm, stats["false_positive_rate_max"], "upper"),
             "paired_sensitivity_gain": bound_gate(gain, stats["sensitivity_gain_min"], "lower", True)}
    return alpha, sensitivity, false_alarm, gain, gates


def evaluate(profile, inputs, result, root, profile_hash, inputs_hash):
    missing = readiness(profile, root)
    validate(inputs, "inputs")
    validate(result, "result")
    if inputs["profile_sha256"] != profile_hash or result["profile_sha256"] != profile_hash or result["input_manifest_sha256"] != inputs_hash:
        raise ValueError("CONTRACT_HASH_BINDING_MISMATCH")
    if not profile["evidence_class"] == inputs["evidence_class"] == result["evidence_class"]:
        raise ValueError("EVIDENCE_CLASS_MISMATCH")
    if missing:
        return {"status": "NOT_READY", "blocking_items": missing, "claim_supported": False}
    if datetime.fromisoformat(result["started_utc"]) <= datetime.fromisoformat(profile["frozen_utc"]):
        raise ValueError("RUN_NOT_AFTER_PROTOCOL_FREEZE")
    for role in ("candidate", "baseline"):
        if result[role+"_source_sha256"] != profile["references"][role+"_source"]["sha256"]:
            raise ValueError("ALGORITHM_SOURCE_MISMATCH")
    local_file(root, result["environment"]["measurement_report"])
    units, bearings, hashes = {}, set(), set()
    for unit in inputs["units"]:
        if unit["record_id"] in units or unit["bearing_id"] in bearings:
            raise ValueError("REPEATED_BEARING_OR_RECORD_ACROSS_SPLITS")
        if unit["samples"]["sha256"] in hashes:
            raise ValueError("DUPLICATE_SAMPLE_CONTENT_ACROSS_UNITS")
        units[unit["record_id"]] = unit
        bearings.add(unit["bearing_id"])
        hashes.add(unit["samples"]["sha256"])
        path = local_file(root, unit["samples"])
        samples(path, profile["sampling"]["record_samples_per_channel"]*4)
    holdout = {k: u for k, u in units.items() if u["split"] == "holdout"}
    decisions = result["decisions"]
    if len(decisions) != len(holdout) or {r["record_id"] for r in decisions} != set(holdout):
        raise ValueError("MISSING_DUPLICATE_OR_EXTRA_HOLDOUT_DECISION")
    positive, negative, true_positive, false_positive, wins, losses = (0,)*6
    for row in decisions:
        candidate = row["candidate_score"] >= profile["processing"]["candidate_threshold"]
        baseline = row["baseline_score"] >= profile["processing"]["baseline_threshold"]
        if holdout[row["record_id"]]["label"] == "damaged":
            positive += 1
            true_positive += candidate
            wins += candidate and not baseline
            losses += baseline and not candidate
        else:
            negative += 1
            false_positive += candidate
    stats = profile["statistics"]
    if positive < stats["min_positive_units"] or negative < stats["min_negative_units"] or not positive or not negative:
        return {"status": "NOT_READY", "blocking_items": ["INSUFFICIENT_INDEPENDENT_UNITS"], "claim_supported": False}
    alpha, sensitivity, false_alarm, gain, gates = diagnostic_gates(
        stats, positive, negative, true_positive, false_positive, wins, losses)
    limits, resources = profile["limits"], result["resources"]
    count = limits["resource_blocks"]
    if len(resources["service_ms"]) != count or len(resources["latency_ms"]) != count:
        raise ValueError("MISSING_RESOURCE_BLOCK_OBSERVATIONS")
    service = sorted(resources["service_ms"])
    mean_service = math.fsum(service)/count
    p99 = service[math.ceil(0.99*count)-1]  # Registered nearest-rank definition.
    conditions = {"mean_service": mean_service < limits["mean_service_exclusive_ms"],
                  "p99_service": p99 <= limits["p99_service_max_ms"],
                  "latency": max(resources["latency_ms"]) <= limits["latency_max_ms"],
                  "state_memory": resources["additional_state_peak_bytes"] <= limits["additional_state_max_bytes"],
                  "no_drops": resources["dropped_blocks"] == 0,
                  "bounded_backlog": resources["peak_backlog_blocks"] <= limits["max_backlog_blocks"] and resources["final_backlog_blocks"] == 0}
    expected = {c["id"]: c for c in profile["preservation_cases"]}
    observed = result["preservation"]
    if len(observed) != len(expected) or {c["id"] for c in observed} != set(expected):
        raise ValueError("MISSING_DUPLICATE_OR_EXTRA_PRESERVATION_OBSERVATION")
    for row in observed:
        reference = expected[row["id"]]
        values = samples(local_file(root, row["output"]), reference["sample_count"])
        amplitude, index = peak(values, reference["peak_window"])
        conditions["amplitude:"+row["id"]] = abs(amplitude-reference["reference_amplitude"])/reference["reference_amplitude"] <= limits["amplitude_relative_error_max"]
        conditions["timing:"+row["id"]] = abs(index-reference["reference_sample"]) <= limits["timing_error_max_samples"]
    gates.update({k: "PASS" if v else "FAIL" for k, v in conditions.items()})
    status = "FAIL" if "FAIL" in gates.values() else "INCONCLUSIVE" if "INCONCLUSIVE" in gates.values() else "PASS"
    real = result["evidence_class"] == "REAL_MEASURED"
    return {"schema": "x6.industrial.v1.assessment/1", "status": status,
            "evidence_class": result["evidence_class"],
            "claim_supported": real and status == "PASS",
            "claim_scope": "REGISTERED_V1_DATASET_ONLY" if real else "SOFTWARE_CONTROL_ONLY",
            "alpha_per_claim": alpha, "gates": gates,
            "counts": {"positive_bearings": positive, "negative_bearings": negative,
                       "true_positive": true_positive, "false_positive": false_positive,
                       "paired_wins": wins, "paired_losses": losses},
            "one_sided_bounds": {"sensitivity": list(sensitivity), "false_positive_rate": list(false_alarm),
                                 "paired_sensitivity_gain": list(gain)},
            "resources": {"mean_service_ms": mean_service, "p99_service_ms": p99,
                          "max_observed_latency_ms": max(resources["latency_ms"])},
            "unavailable_metrics": {"reconstruction_MSE": "NO_CLEAN_WAVEFORM_REFERENCE_IN_V1_D",
                                    "energy_savings": "NOT_MEASURED_BY_THIS_CONTRACT"}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", type=Path)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--inputs", type=Path)
    parser.add_argument("--result", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        profile, ph = read(args.profile)
        if args.inputs is None and args.result is None:
            missing = readiness(profile, args.root)
            out = {"status": "NOT_READY" if missing else "READY_FOR_RESULT_REVIEW",
                   "blocking_items": missing, "claim_supported": False}
        elif args.inputs is None or args.result is None:
            raise ValueError("INPUTS_AND_RESULT_REQUIRED_TOGETHER")
        else:
            inputs, ih = read(args.inputs)
            result, rh = read(args.result)
            out = evaluate(profile, inputs, result, args.root, ph, ih)
            out.update({"profile_sha256": ph, "inputs_sha256": ih, "result_sha256": rh})
    except Exception as exc:
        # Invalid data is never downgraded to scientific FAIL or PASS.
        out = {"status": "INVALID", "reason": (str(exc) or type(exc).__name__)[:1000], "claim_supported": False}
    out["schema"] = "x6.industrial.v1.assessment/1"
    out["evaluator_sha256"] = digest(Path(__file__).read_bytes())
    validate(out, "assessment")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2, allow_nan=False)+"\n")
    print(json.dumps(out, allow_nan=False))
    return {"PASS": 0, "READY_FOR_RESULT_REVIEW": 0, "FAIL": 1, "INVALID": 2,
            "NOT_READY": 3, "INCONCLUSIVE": 4}[out["status"]]


if __name__ == "__main__":
    sys.exit(main())
