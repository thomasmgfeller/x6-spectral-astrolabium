"""Main entrance: GUM evaluation first, supplementary tolerance and risk control second."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
from c01 import anchored,loads,interval,number
from gum import assess_file

def evaluate(gum_path,anchor_path):
    g=assess_file(gum_path)
    record=loads(anchor_path.read_text())
    base={"geometry_release":False,"gum":g}
    if g.get('status')!="GUM_BUDGET_95_APPROX":
        return {**base,"status":g['status']}
    if any(record.get(k)!=g.get(k) for k in ('mode','scope_id','node')):
        return {**base,'status':'HOLD_SCOPE'}
    a=anchored(record,anchor_path.parent)
    base["interval_control"]=a
    if a["status"] not in ("SYNTHETIC_BOUND_OK","FIELD_BOUND_REQUIRES_REVIEW"):
        return {**base,"status":a["status"]}
    y,p,gain,c=map(F,g["estimates"])
    for name,value in (("target",p),("gain",gain),("comparator",y)):
        lo,hi=interval(record["bounds"][name])
        if not lo<=value<=hi:
            return {**base,"status":"HOLD_INCONSISTENT_EVIDENCE"}
    if abs(c)>number(record["bounds"]["transfer"]):
        return {**base,"status":"HOLD_INCONSISTENT_EVIDENCE"}
    return {**base,"status":"SYNTHETIC_MODEL_ONLY" if g["mode"]=="synthetic" else "FIELD_METROLOGICAL_REVIEW_REQUIRED"}

if __name__=="__main__":
    cli=argparse.ArgumentParser(description=__doc__);cli.add_argument("gum",type=Path);cli.add_argument("intervals",type=Path)
    args=cli.parse_args()
    try:out=evaluate(args.gum,args.intervals)
    except (OSError,ValueError,ArithmeticError,AttributeError,TypeError,KeyError) as exc:
        out={"status":"HOLD_INPUT","reason":str(exc),"geometry_release":False}
    print(json.dumps(out,indent=2,sort_keys=True,allow_nan=False))
