"""Exact replay for each partner/order pair. Uses only the standard library."""
import argparse
import csv
import gzip
import hashlib
import json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as F
from io import StringIO

from model import COLLAR, ROOT, boundary_hull, cases, inputs
from schranken import Form, constraints, initial_order_boxes, margin, moment_rows

BASE = "9d476610314a68f0a8b413ddc843aa5e24b90071"
INPUT_SHA256 = "c75c0c97c1b536d0140d77b4f01d8bfa0a2aab487a1b05a2b58f2ebf23159c2f"
COUNTS = {1:748, 2:3366}


def label(seq):
    return ",".join(map(str, sorted(seq)))


def tsv(rows):
    out = StringIO()
    csv.writer(out, dialect="excel-tab", lineterminator="\n").writerows(rows)
    return out.getvalue()


def replay_node(pair, side, q, rel, boxes, node):
    for batch in node["tighten"]:
        rows = moment_rows(pair, side, q, rel, boxes)
        next_boxes = boxes.copy()
        axes = set()
        for event, sign, value, weights in batch:
            assert event in boxes and sign in (-1,1) and (event,sign) not in axes
            axes.add((event,sign))
            value = F(value)
            assert "opposite" not in weights
            opposite = sign*Form({f"y{event}":1})-value
            assert margin(rows | {"opposite":opposite}, weights | {"opposite":"1"}, boxes)>0
            lo,hi = next_boxes[event]
            next_boxes[event] = (max(lo,value),hi) if sign==1 else (lo,min(hi,-value))
        boxes = next_boxes
        if any(lo>hi for lo,hi in boxes.values()):
            assert "empty" in node and boxes[node["empty"]][0]>boxes[node["empty"]][1]
            return
    if "split" in node:
        i=node["split"]; at=F(node["at"]); lo,hi=boxes[i]
        assert lo<at<hi and len(node["children"])==2
        for interval,subnode in zip(((lo,at),(at,hi)),node["children"]):
            replay_node(pair,side,q,rel,boxes|{i:interval},subnode)
    else:
        assert set(node)=={"tighten","no"}
        assert margin(moment_rows(pair,side,q,rel,boxes),node["no"],boxes)>0


def classify(pair, side, q, rel, cert):
    rows=constraints(pair,side,q,rel)
    if "linear" in cert:
        assert margin(rows,cert["linear"])>0
        return "Uhrgleichungen"
    if cert.get("projected") is True:
        boxes=initial_order_boxes(pair,side,None,None,rel,False)
        replay_node(pair,side,q,rel,boxes,cert["moment"])
        return "Eliminierte_Nachfolgeruhren"
    if "bound" in cert:
        event,upper=cert["cap"]
        assert event in (23,24) and upper>0
        rows[f"y{event}ge{upper}"]=upper-Form({f"y{event}":1})
        assert margin(rows,cert["bound"])>0
        boxes=initial_order_boxes(pair,side,upper,event,rel,cert.get("terminal21",False))
        replay_node(pair,side,q,rel,boxes,cert["moment"])
        return "Dichte_und_Uhrgleichungen"
    if cert=={"open":True}:
        return "OFFEN"
    raise ValueError("Unbekannter Nachweistyp")


def execute(item):
    idx,(q,extra,p,a,b,rel),cert,pair=item
    if "separate" in cert:
        assert set(cert["separate"])=={"heavy","light"}
        methods=[classify(pair,side,q,rel,cert["separate"][side]) for side in ("heavy","light")]
        domain="Einzelpraeparation"
    else:
        method=classify(pair,"both",q,rel,cert)
        methods=[method,method]
        domain="Gemeinsame_Kragenuhrhuelle"
    return idx,q,label(extra),label(p),label(a),label(b),domain,methods


def check_or_write(path,text,write):
    encoded=text.encode("utf-8")
    if write:
        path.write_bytes(encoded)
    else:
        assert path.read_bytes()==encoded,path.name


def run(jobs,write,levels):
    assert hashlib.sha256((ROOT/"input/Vergleichspaar.json").read_bytes()).hexdigest()==INPUT_SHA256
    pair,base=inputs()
    pair["both"]=boundary_hull(pair)
    for side in ("heavy","light"):
        for i in COLLAR:
            a,b=pair["both"]["clock_box"][i]
            l,h=map(F,pair[side]["clock_box"][i])
            assert a<=l<=h<=b
    reports={}
    for level in levels:
        orders=list(cases(base,level))
        with gzip.open(ROOT/f"Zertifikate_Stufe{level}.json.gz","rt",encoding="utf-8") as f:
            proofs=json.load(f)
        assert len(orders)==len(proofs)==COUNTS[level]
        assert all(len(set(row[1]))==level for row in orders)
        header=["Fall","Partner","Zusaetzliche_alte_Vorgaenger","Alt_vor_22","Alt_vor_23","Alt_vor_24",
                "Beweisbereich","Praeparation","Kontakt","Begruendung"]
        rows=[header]; counts=Counter(); group=Counter()
        items=[(i,order,cert,pair) for i,(order,cert) in enumerate(zip(orders,proofs))]
        with ProcessPoolExecutor(max_workers=jobs) as pool:
            for idx,q,extra,p,a,b,domain,methods in pool.map(execute,items,chunksize=8):
                for side,method in zip(("heavy","light"),methods):
                    status="OFFEN" if method=="OFFEN" else "AUSGESCHLOSSEN"
                    counts[side+"/"+method]+=1
                    group[f"{q}/{extra}/{side}/{status}"]+=1
                    rows.append([idx,q,extra,p,a,b,domain,side,status,method])
        reports[str(level)]={"orders":len(orders),"methods":dict(sorted(counts.items())),
                             "groups":dict(sorted(group.items()))}
        check_or_write(ROOT/f"Fallregister_Stufe{level}.tsv",tsv(rows),write)
    if set(levels)=={1,2}:
        output={"base_commit":BASE,"window":["15/32","17/32"],"levels":reports,
                "physical_radii":[None]*8,"physical_P3":{"status":"NOT_RUN","count":60}}
        check_or_write(ROOT/"Ergebnisse.json",json.dumps(output,indent=2,ensure_ascii=False)+"\n",write)
    for level,o in reports.items():
        print("Stufe",level,o["orders"],o["methods"])


if __name__=="__main__":
    if not __debug__:raise RuntimeError("Ohne -O ausführen")
    parser=argparse.ArgumentParser()
    parser.add_argument("--jobs",type=int,default=1)
    parser.add_argument("--ausgabe",action="store_true")
    parser.add_argument("--stufe",type=int,choices=(1,2))
    args=parser.parse_args()
    run(args.jobs,args.ausgabe,[args.stufe] if args.stufe else [1,2])
