"""Frozen, reference-band-only SED selection experiment. Source payloads remain in RAM."""
import argparse
import hashlib
import itertools
import json
import math
import re
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from pathlib import Path

import numpy as np
from obspy import UTCDateTime
from scipy.stats import binomtest

from agent import sed_three_station as sed
from agent.run_agent import ROOT, require

STUDY = ROOT/"research/sed_filter_prediction/v1"
CONTRACT = hashlib.sha256((STUDY/"CONTRACT.md").read_bytes()).hexdigest()
HALVES = [f"{year}-H{half}" for year in range(2018,2026) for half in (1,2)]
PAIRS = list(itertools.combinations(sed.STATIONS,2))
REFERENCE = (2,8)
CONTROLS = ((1,5),(4,12))


def encoded(data):
    return (json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)+"\n").encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def output(path, data):
    # Hard-linking a finished temporary file is atomic and never overwrites a frozen stage.
    import os
    import tempfile
    if path.name=="cohort.json":
        check_selection(data)
    elif path.name=="predictions.json":
        check_predictions(data)
    elif path.name=="results.json":
        require(set(data)=={"prediction_sha256","cohort_sha256","outcomes","result"},"Unexpected evaluation fields")
        frozen_raw=(path.parent/"predictions.json").read_bytes()
        frozen=json.loads(frozen_raw)
        check_predictions(frozen)
        require(data["prediction_sha256"]==digest(frozen_raw) and data["cohort_sha256"]==frozen["cohort_sha256"]
                and data["result"]==trial_result(frozen["events"],data["outcomes"]),"Invalid evaluation output")
    else:
        raise ValueError("Unknown evidence type")
    raw = encoded(data)
    path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=path.parent) as temp:
        candidate=Path(temp)/"complete.json"
        candidate.write_bytes(raw)
        try:
            os.link(candidate,path)
        except FileExistsError:
            require(path.read_bytes()==raw, f"Existing file differs at {path}; use a fresh output directory")


def years_half(t):
    return f"{t.year}-H{1 if t.month<=6 else 2}"


def candidates():
    result=sed.fetch("event", starttime="2018-01-01", endtime="2025-12-31T23:59:59.999999",
                     minlatitude=46.35,maxlatitude=47.55,minlongitude=7.8,maxlongitude=9.8,
                     minmagnitude=2,format="text")
    raw=result.getvalue()
    lines=raw.decode().splitlines()
    columns=lines[0].lstrip("#").split("|")
    by_half={key:[] for key in HALVES}
    seen=set()
    for line in lines[1:]:
        row=dict(zip(columns,line.split("|"),strict=True))
        if row["EventType"].lower() != "earthquake":
            continue
        t=UTCDateTime(row["Time"])
        event_id=row["EventID"]
        require(event_id not in seen and re.fullmatch(r"smi:ch\.ethz\.sed/[\w./-]+",event_id), "Unexpected catalogue ID")
        seen.add(event_id)
        by_half[years_half(t)].append((-Decimal(row["Magnitude"]),t.ns,event_id))
    return by_half, digest(raw)


def cohort():
    by_half, table_hash=candidates()
    last=None
    blocks=[]
    for half in HALVES:
        possible=[c for c in sorted(by_half[half]) if last is None or c[1]-last >= 30*86400*10**9]
        reviewed=[]
        selected=None
        for _,ns,event in possible[:4]:
            try:
                origin, marks=sed.event_references(event)
            except sed.PgUnavailable:
                reviewed.append({"id":event,"status":"PG_UNAVAILABLE"})
                continue
            if any(not 0 <= p-origin <= 30 for p in marks.values()):
                reviewed.append({"id":event,"status":"PG_OUTSIDE"})
                continue
            selected=event
            last=ns
            reviewed.append({"id":event,"status":"SELECTED"})
            break
        blocks.append({"half":half,"eligible_catalogue_count":len(possible),"reviewed":reviewed,"selected":selected})
        print(half,selected or "NO_ELIGIBLE_EVENT",flush=True)
    return {"contract_sha256":CONTRACT,"catalogue_sha256":table_hash,"blocks":blocks}


def reference_station(velocity,t0,guide,rate):
    times=t0+np.arange(len(velocity))/rate
    filtered,_,baseline=sed.filtered_band(velocity,times,REFERENCE,rate)
    pick,status=sed.checked_variance_pick(filtered,times,guide,baseline,rate)
    if pick is None:
        return {"status":status},None
    pulse=filtered[(times>=pick)&(times<pick+0.5)]
    noise=filtered[(times>=-45)&(times<-15)]
    snr=float(np.sqrt(np.mean(pulse**2)/np.mean(noise**2)))
    require(math.isfinite(snr),"Invalid reference SNR")
    variants=[sed.variance_onset(filtered,times,guide+dt,baseline,rate)[0] for dt in (-0.15,0.15)]
    variants.append(pick)
    width=None if None in variants else max(variants)-min(variants)
    return {"status":"OK","snr":snr,"width_s":width},pick


def select(event, features):
    ranks=[]
    for a,b in PAIRS:
        sa,sb=features[a],features[b]
        if sa["status"]!="OK" or sb["status"]!="OK":
            continue
        name=a+"-"+b
        width=None if sa["width_s"] is None or sb["width_s"] is None else round(1e6*(sa["width_s"]+sb["width_s"]))
        ranks.append({"pair":name,"risk_us":width,"snr":min(sa["snr"],sb["snr"])})
    return choose(event,ranks)


def choose(event,ranks):
    def tie(row):
        return digest((event+"|"+row["pair"]).encode())
    if not ranks:
        return {"pairs":[],"x6":None,"snr":None}
    x6=min(ranks,key=lambda r:(math.inf if r["risk_us"] is None else r["risk_us"],tie(r)))
    snr=min(ranks,key=lambda r:(-r["snr"],tie(r)))
    return {"pairs":ranks,"x6":x6["pair"],"snr":snr["pair"]}


# Expected station-level unavailability is recorded. Transport and unexpected errors stop the stage.
STATION_HOLDS = {
    "station: no data for selected window":"NO_METADATA",
    "dataselect: no data for selected window":"NO_WAVEFORM",
    "Missing explicit open status at network, station or channel":"ACCESS_HOLD",
    "Metadata epoch does not cover the window":"EPOCH_HOLD",
    "Ambiguous station/channel epoch":"EPOCH_HOLD",
    "Missing or incompatible vertical velocity response":"RESPONSE_HOLD",
    "Gap or overlap inside the analysis interval":"GAP_HOLD",
    "Incomplete waveform interval":"GAP_HOLD",
    "Cannot form one continuous trace":"GAP_HOLD",
    "Unusable noise baseline":"NOISE_HOLD",
}


def prepare_event(event):
    origin,marks=sed.event_references(event)
    signals,features,identities={}, {}, {}
    for station in sed.STATIONS:
        guide=marks[station]-origin
        try:
            velocity,t0,counts_hash,rate=sed.station_velocity(station,origin,(120,200))
            features[station],pick=reference_station(velocity,t0,guide,rate)
        except ValueError as exc:
            if str(exc) not in STATION_HOLDS:
                raise
            features[station]={"status":STATION_HOLDS[str(exc)]}
            continue
        identities[station]=digest(encoded([counts_hash,rate,origin.ns,marks[station].ns,t0,
                                           digest(np.asarray(velocity,dtype="<f8").tobytes())]))
        if pick is not None:
            signals[station]=(velocity,t0,guide,rate,pick)
    prediction={"id":event,"input_hashes":identities,
                "station_status":{s:f["status"] for s,f in features.items()},**select(event,features)}
    return prediction,signals


def label(delays_s):
    if None in delays_s:
        return {"label":"INDETERMINATE","spread_us":None}
    values=[round(1_000_000*d) for d in delays_s]
    spread=max(values)-min(values)
    return {"label":"WITHIN" if spread<=100_000 else "EXCEEDED","spread_us":spread}


def controls(signals, prediction):
    picks={}
    for station,(velocity,t0,guide,rate,pick) in signals.items():
        times=t0+np.arange(len(velocity))/rate
        picks[station]=[pick]
        for band in CONTROLS:
            filtered,_,baseline=sed.filtered_band(velocity,times,band,rate)
            picks[station].append(sed.checked_variance_pick(filtered,times,guide,baseline,rate)[0])
    outcomes={}
    for row in prediction["pairs"]:
        pair=row["pair"]
        a,b=pair.split("-")
        outcomes[pair]=label([None if x is None or y is None else y-x
                              for x,y in zip(picks[a],picks[b],strict=True)])
    return outcomes


def trial_result(predictions, outcomes):
    counts={k:{c:0 for c in ("WITHIN","EXCEEDED","INDETERMINATE")} for k in ("x6","snr")}
    wins=losses=equal_pairs=n=0
    require(set(outcomes)=={r["id"] for r in predictions},"Outcome cohort differs from freeze")
    for rec in predictions:
        labels=outcomes[rec["id"]]
        for value in labels.values():
            require(set(value)=={"label","spread_us"},"Unexpected control fields")
            spread=value["spread_us"]
            require(spread is None or (type(spread) is int and 0<=spread<=95_000_000),"Invalid control spread")
            state="INDETERMINATE" if spread is None else ("WITHIN" if spread<=100_000 else "EXCEEDED")
            require(value["label"]==state,"Control label disagrees with spread")
        require(set(labels)=={r["pair"] for r in rec["pairs"]},"Outcome pair set differs from freeze")
        if not rec["pairs"]:
            require(rec["x6"] is None and rec["snr"] is None,"Asymmetric abstention")
            continue
        n+=1
        xs,ss=(labels[rec[rule]]["label"] for rule in ("x6","snr"))
        counts["x6"][xs]+=1
        counts["snr"][ss]+=1
        equal_pairs+=rec["x6"]==rec["snr"]
        wins+=xs=="WITHIN" and ss!="WITHIN"
        losses+=ss=="WITHIN" and xs!="WITHIN"
    p=float(binomtest(wins,wins+losses,.5,alternative="greater").pvalue) if wins+losses else 1.
    return {"released_each":n,"same_pair":equal_pairs,"counts":counts,"x6_only_success":wins,
            "snr_only_success":losses,"p_one_sided":p,
            "decision":"ADVANTAGE_SUPPORTED" if n>=12 and wins>losses and p<=0.05 else "ADVANTAGE_NOT_DEMONSTRATED"}


def valid_hash(value):
    return isinstance(value,str) and re.fullmatch("[0-9a-f]{64}",value) is not None


def valid_id(value):
    return isinstance(value,str) and re.fullmatch(r"smi:ch\.ethz\.sed/[\w./-]{1,110}",value) is not None


def check_selection(data):
    require(set(data)=={"contract_sha256","catalogue_sha256","blocks"} and
            data["contract_sha256"]==CONTRACT and valid_hash(data["catalogue_sha256"]),"Invalid selection header")
    require([b["half"] for b in data["blocks"]]==HALVES,"Unexpected time blocks")
    for b in data["blocks"]:
        require(set(b)=={"half","eligible_catalogue_count","reviewed","selected"} and
                type(b["eligible_catalogue_count"]) is int and len(b["reviewed"])<=min(4,b["eligible_catalogue_count"]),
                "Unexpected catalogue fields")
        for r in b["reviewed"]:
            require(set(r)=={"id","status"} and valid_id(r["id"]) and
                    r["status"] in {"SELECTED","PG_UNAVAILABLE","PG_OUTSIDE"},"Unexpected catalogue result")
        selected=[v["id"] for v in b["reviewed"] if v["status"]=="SELECTED"]
        require(selected==([] if b["selected"] is None else [b["selected"]]),"Selection mismatch")


def check_predictions(data):
    require(set(data)=={"contract_sha256","cohort_sha256","events"} and
            data["contract_sha256"]==CONTRACT and valid_hash(data["cohort_sha256"]),"Invalid prediction header")
    for rec in data["events"]:
        require(set(rec)=={"id","input_hashes","station_status","pairs","x6","snr"} and valid_id(rec["id"]),
                "Unexpected prediction fields")
        statuses=rec["station_status"]
        allowed={"OK","BOUNDARY_OR_FLAT","LOW_CONTRAST","QUIET_TRIGGER"}|set(STATION_HOLDS.values())
        require(set(statuses)==set(sed.STATIONS) and all(s in allowed for s in statuses.values()),"Invalid station status")
        require(set(rec["input_hashes"])=={s for s,v in statuses.items() if v not in STATION_HOLDS.values()} and
                all(valid_hash(v) for v in rec["input_hashes"].values()),"Invalid input identities")
        pairs=rec["pairs"]
        require([p["pair"] for p in pairs]==[a+"-"+b for a,b in PAIRS if statuses[a]==statuses[b]=="OK"],
                "Wrong common eligibility pool")
        for p in pairs:
            cost=p["risk_us"]
            require(set(p)=={"pair","risk_us","snr"} and (cost is None or (type(cost) is int and 0<=cost<10_000_000))
                    and type(p["snr"]) in (float,int) and math.isfinite(p["snr"]) and p["snr"]>=0,"Invalid pair scores")
        ranking=choose(rec["id"],pairs)
        require(all(rec[k]==ranking[k] for k in ("x6","snr")),"Freigabe disagrees with frozen scores")


def load_cohort(path):
    data=json.loads(path.read_bytes())
    check_selection(data)
    ids=[b["selected"] for b in data["blocks"] if b["selected"] is not None]
    require(len(ids)==len(set(ids)), "Duplicate selected event")
    return ids


def predict(cohort_path):
    ids=load_cohort(cohort_path)
    def one(event):
        prediction,_=prepare_event(event)
        print("PREDICT",event,prediction["x6"],prediction["snr"],flush=True)
        return prediction
    with ThreadPoolExecutor(3) as pool:
        rows=list(pool.map(one,ids))
    return {"contract_sha256":CONTRACT,"cohort_sha256":digest(cohort_path.read_bytes()),"events":rows}


def evaluate(cohort_path, frozen_path, expected_sha):
    raw=frozen_path.read_bytes()
    require(digest(raw)==expected_sha,"Frozen predictions changed")
    frozen=json.loads(raw)
    check_predictions(frozen)
    ids=load_cohort(cohort_path)
    require(frozen["contract_sha256"]==CONTRACT and frozen["cohort_sha256"]==digest(cohort_path.read_bytes()) and
            [r["id"] for r in frozen["events"]]==ids,"Wrong contract, cohort or event order")
    def one(rec):
        reference,signals=prepare_event(rec["id"])
        require(reference==rec,"Input or prior decision changed for "+rec["id"])
        outcomes=controls(signals,reference)
        print("SCORED",rec["id"],flush=True)
        return rec["id"],outcomes
    with ThreadPoolExecutor(3) as pool:
        outcomes=dict(pool.map(one,frozen["events"]))
    return {"prediction_sha256":expected_sha,"cohort_sha256":frozen["cohort_sha256"],
            "outcomes":outcomes,"result":trial_result(frozen["events"],outcomes)}


if __name__=="__main__":
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("stage",choices=("cohort","predict","evaluate","verify"))
    cli.add_argument("--directory",type=Path,default=STUDY)
    cli.add_argument("--prediction-sha256",help="Digest of the externally frozen reference decisions")
    args=cli.parse_args()
    folder=args.directory
    cs,rs,results=(folder/k for k in ("cohort.json","predictions.json","results.json"))
    if args.stage=="cohort":
        output(cs,cohort())
    elif args.stage=="predict":
        output(rs,predict(cs))
        print("PREDICTION SHA-256",digest(rs.read_bytes()))
    else:
        require(args.prediction_sha256 and re.fullmatch("[a-f0-9]{64}",args.prediction_sha256),
                "Supply the reviewed reference freeze SHA-256")
        if args.stage=="evaluate":
            output(results,evaluate(cs,rs,args.prediction_sha256))
        else:
            ids=load_cohort(cs)
            f=json.loads(rs.read_bytes());r=json.loads(results.read_bytes())
            check_predictions(f)
            require(digest(rs.read_bytes())==r["prediction_sha256"]==args.prediction_sha256 and
                    digest(cs.read_bytes())==f["cohort_sha256"]==r["cohort_sha256"] and
                    f["contract_sha256"]==CONTRACT and [e["id"] for e in f["events"]]==ids,
                    "Evidence chain mismatch")
            require(trial_result(f["events"],r["outcomes"])==r["result"],"Decision does not replay")
            print(json.dumps(r["result"],indent=2))
