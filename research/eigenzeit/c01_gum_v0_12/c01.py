"""One C01 anchor check and a streaming diagnostic for separately closed event records."""
import argparse
from fractions import Fraction as F
from itertools import zip_longest
import hashlib
import json
from pathlib import Path

DESIGN = "X6/Eigenzeit/v0.12/C01-quarter"
NODE = "C01@1/4"
CLAIMS = ("target", "gain", "comparator", "transfer")
PPM = 1_000_000
PER_NODE_RISK = F(2, PPM)
FULL_PAIRS = 3_300_000


def unique(items):
    data = {}
    for k,v in items:
        if k in data:
            raise ValueError("duplicate key: "+k)
        data[k]=v
    return data


def loads(line):
    return json.loads(line,object_pairs_hook=unique)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def number(raw):
    require(isinstance(raw,str) and len(raw)<=60,"expected rational string")
    return F(raw)


def integer(value):
    return type(value) is int


def exact_keys(data,keys):
    return isinstance(data,dict) and set(data)==set(keys)


def signature(path):
    with path.open("rb") as fp:
        return hashlib.file_digest(fp,"sha256").hexdigest()


def interval(data):
    require(isinstance(data,list) and len(data)==2,"expected interval")
    lo,hi=map(number,data)
    require(lo<=hi,"empty interval")
    return lo,hi


def anchored(record,root):
    fields=("design","mode","scope_id","node","bounds","evidence")
    require(exact_keys(record,fields) and record["design"]==DESIGN and record["node"]==NODE, "wrong anchor contract")
    mode,scope=record["mode"],record["scope_id"]
    require(mode in ("field","synthetic") and isinstance(scope,str) and bool(scope.strip()),"mode or scope")
    bounds,docs=record["bounds"],record["evidence"]
    require(exact_keys(bounds,CLAIMS) and exact_keys(docs,CLAIMS),"missing claims")
    base={"node":NODE,"mode":mode,"scope_id":scope,"geometry_release":False}
    missing=[k for k in CLAIMS if bounds[k] is None or docs[k] is None]
    if missing:
        return dict(base,status="HOLD_EVIDENCE",missing=missing)
    total_risk=F(0)
    root=root.resolve()
    for key in CLAIMS:
        ref=docs[key]
        require(exact_keys(ref,("file","sha256")) and isinstance(ref["file"],str),"evidence reference")
        relative=Path(ref["file"]); path=(root/relative).resolve()
        require(not relative.is_absolute() and path.is_relative_to(root) and path.is_file()
                and signature(path)==ref["sha256"],"evidence file "+key)
        data=loads(path.read_text())
        require(isinstance(data,dict) and data.get("mode")==mode and data.get("scope_id")==scope and data.get("node")==NODE, "scope mismatch")
        claim=data.get("claims",{}).get(key)
        require(exact_keys(claim,("bound","alpha")) and claim["bound"]==bounds[key],"unbound claim "+key)
        risk=number(claim["alpha"])
        require(0<=risk<=1,"invalid risk")
        total_risk+=risk
    pl,ph=interval(bounds["target"]); al,ah=interval(bounds["gain"]); yl,yh=interval(bounds["comparator"])
    b=number(bounds["transfer"])
    require(0<=pl<=ph<=1 and 0<=yl<=yh<=1 and F(99,100)<=al<=ah<=F(101,100) and b>=0,"physical bounds")
    width=max(abs(yl-ah*ph),abs(yh-al*pl))+b
    if total_risk>PER_NODE_RISK:
        status="HOLD_RISK"
    elif width>F(2,PPM):
        status="HOLD_2PPM"
    else:
        status="SYNTHETIC_BOUND_OK" if mode=="synthetic" else "FIELD_BOUND_REQUIRES_REVIEW"
    return dict(base,status=status,worst_ppm=str(width*PPM),false_certificate_budget=str(total_risk))


def bit(row,tag_t,delay,uncertainty):
    edges=row["edge_ps"]
    require(isinstance(edges,list) and all(integer(e) and e>=0 for e in edges)
            and edges==sorted(edges),"invalid timestamps")
    center=tag_t+delay
    require(all(center-3000<=e<center+3000 for e in edges),"edge outside acquisition interval or wrong ID")
    left=center-1000
    right=left+2000
    hit=False
    for e in edges:
        low,high=e-uncertainty,e+uncertainty
        if high<left or low>=right:
            continue
        require(low>=left and high<right,"ambiguous timing boundary")
        hit=True
    return int(hit)


def events(plan,streams):
    keys=("design","mode","scope_id","run_id","node","first_id","scheduled","delay_ps","timestamp_bound_ps")
    require(exact_keys(plan,keys) and plan["design"]==DESIGN and plan["node"]==NODE,"wrong raw contract")
    mode,scope,run=plan["mode"],plan["scope_id"],plan["run_id"]
    require(mode in ("synthetic","field") and all(isinstance(v,str) and v.strip() for v in (scope,run)),"mode or scope")
    first,n=plan["first_id"],plan["scheduled"]
    require(integer(first) and first>=0 and integer(n) and 0<n<=FULL_PAIRS,"expected fixed ID range")
    delays,unc=plan["delay_ps"],plan["timestamp_bound_ps"]
    for values in (delays,unc):
        require(exact_keys(values,("X","Y")) and all(integer(v) for v in values.values()),"channel parameters")
    require(all(0<=v<1000 for v in unc.values()),"uncertainty must be below half window")
    for role,stream in zip(("TAG","X","Y"),streams,strict=True):
        expected={"role":role,"design":DESIGN,"scope_id":scope,"mode":mode,"run_id":run,"node":NODE}
        require(loads(next(stream,"null"))==expected,"stream header "+role)
    counts=dict.fromkeys(("00","01","10","11"),0)
    last_t=None; seen=0; stop_id=None
    for i,lines in enumerate(zip_longest(*streams)):
        require(i<n and all(v is not None for v in lines),"extra or missing row")
        tag,x,y=map(loads,lines)
        require(exact_keys(tag,("id","t_ps","complete")) and all(exact_keys(r,("id","edge_ps","complete")) for r in (x,y)),"raw fields")
        require(all(integer(r["id"]) and r["id"]==first+i and r["complete"] is True for r in (tag,x,y)),"unclosed or inconsistent ID")
        t=tag["t_ps"]
        require(integer(t) and t>=0,"tag time")
        if last_t is not None:
            require(t-last_t>6000+2*max(unc.values()),"windows overlap or tag not increasing")
        a=bit(x,t,delays["X"],unc["X"]); b=bit(y,t,delays["Y"],unc["Y"])
        counts[f"{a}{b}"]+=1; seen+=1;last_t=t
        if stop_id is None and counts["01"]+counts["10"]==26:
            stop_id=first+i
    require(seen==n,"truncated declared input")
    status="STOP_DISCORDANCE" if stop_id is not None else "PREFIX_VALID_NO_RELEASE"
    return dict(mode=mode,scope_id=scope,run_id=run,node=NODE,seen=seen,counts=counts,
                first_stop_id=stop_id,status=status,geometry_release=False)


def main():
    from contextlib import ExitStack
    cli=argparse.ArgumentParser(description=__doc__)
    sub=cli.add_subparsers(dest="kind",required=True)
    sub.add_parser("anchor").add_argument("record",type=Path)
    sub.add_parser("events").add_argument("files",nargs=4,type=Path,metavar="FILE")
    args=cli.parse_args()
    try:
        if args.kind=="anchor":
            result=anchored(loads(args.record.read_text()),args.record.parent)
        else:
            plan,*paths=args.files
            with ExitStack() as stack:
                streams=[stack.enter_context(p.open()) for p in paths]
                result=events(loads(plan.read_text()),streams)
    except (OSError,ValueError,ZeroDivisionError,AttributeError,TypeError,KeyError) as exc:
        result={"status":"HOLD_INPUT","reason":str(exc),"geometry_release":False}
    print(json.dumps(result,indent=2,sort_keys=True))
    return int(result["status"]=="HOLD_INPUT")

if __name__=="__main__":
    raise SystemExit(main())
