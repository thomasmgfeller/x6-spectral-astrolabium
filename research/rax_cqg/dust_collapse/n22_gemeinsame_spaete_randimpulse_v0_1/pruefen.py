"""Recompute the N22 boundary impulse certificates and all registers offline."""
import argparse
import csv
from fractions import Fraction as F
from hashlib import sha256
from io import StringIO
from itertools import combinations
import json
from versuch import ROOT, LATE, inputs, targets


def register(header, rows):
    stream=StringIO()
    writer=csv.writer(stream,delimiter="\t",lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return stream.getvalue()


def rounded(value,up=False):
    scale=10**15
    return F(-(-value*scale//1) if up else value*scale//1,scale)


def run():
    assert sha256((ROOT/"Pruefplan.md").read_bytes()).hexdigest()==(ROOT/"Pruefplan.sha256").read_text().split()[0]
    with inputs() as (previous,(seed,collar,coeff,free,relations,goals,_)):
        from paarvergleich import certify
        from sekantenimpuls import prove
        from sekanten import ALL,UNIT,domain
        from zukunftsbasis import name
        from randversuch import SOURCES
        from kontrolle import audit
        assert set(free)==set(range(22))-(set(range(4))|set(LATE))
        assert len(set(free))==14
        edges=[(i,j,F(v)) for (i,j),v in sorted(coeff.items())]
        assert all(21 not in (i,j) for i,j,k in edges if k and (i in LATE or j in LATE))
        target=targets(previous,edges,goals)
        assert sum(target.values())==-sum(goals[1:])
        old={a:tuple(map(int,previous["domain"][name(a)])) for a in ALL}
        rows=[]
        shifts=[]
        for pair in combinations(LATE,2):
            group=[certify(seed,collar,s,coeff,free,relations,goals,pair,target) for s in SOURCES]
            for s,r in zip(SOURCES,group):
                assert r["decisions"]==[int(s*10**6)]
                for j in pair:
                    lo,hi=map(F,r["impulses"][str(j)])
                    assert lo<=target[j]<=hi
                outside=[]
                for k,i in ALL:
                    lo,hi=map(F,r[k][i])
                    a,b=old[k,i]
                    if not (a<=lo*UNIT<=hi*UNIT<=b):
                        outside.append(name((k,i)))
                r["outside_old_box"]=outside
            first,second=sorted(set(LATE)-set(pair))
            for a,b in zip(group,group[1:]):
                def gap(node):
                    l,h=map(F,a["impulses"][str(node)])
                    L,H=map(F,b["impulses"][str(node)])
                    return L-h,H-l
                l,h=gap(first)
                u,v=gap(second)
                # Exact impulse balance makes the two increments opposites.
                lo,hi=max(l,-v),min(h,-u)
                assert lo<=hi and (hi<0 or lo>0)
                shifts.append(dict(pair=list(pair),moving=[first,second],sources=[a["source"],b["source"]],
                                   first_change=list(map(str,[rounded(lo),rounded(hi,True)]))))
            rows.extend(group)
        combined=domain(rows+previous["witnesses"],free)
        for axis,(l,h) in old.items():
            assert combined[axis][0]<=l<=h<=combined[axis][1]
        for row in rows:
            for k,i in ALL:
                lo,hi=map(F,row[k][i])
                l,h=combined[k,i]
                assert l<=lo*UNIT<=hi*UNIT<=h
        proofs={}
        bounds={}
        for label,box in (("PR410",old),("extended",combined)):
            certs=[prove(box,edges,free,triple) for triple in combinations(LATE,3)]
            proofs[label]=certs
            if all(p["status"]=="EXCLUDED" for p in certs):
                bounds[label]=str(max(F(p["minimum_adjacent_gap"]) for p in certs))
        checks=audit(rows,edges,free)
        return dict(source_archive="PR 410",early_targets=list(map(str,goals)),
                    impulse_targets={str(i):str(v) for i,v in target.items()},total_impulse=str(sum(target.values())),
                    cases=rows,transfers=shifts,triples=proofs,adjacent_lower=bounds,
                    extended_domain_grid=str(UNIT),extended_domain={name(a):list(map(str,v)) for a,v in combined.items()},
                    independent_audit=checks,P3_NOT_RUN=previous["P3_NOT_RUN"])


def output(data):
    files={"Ergebnisse.json":json.dumps(data,indent=2,sort_keys=True)+"\n"}
    files["Fallregister.tsv"]=register(["Fest_1","Fest_2","Quelle","Code_min","Code_max","Leserklasse",
                                        "Ganz_in_PR410","Kontraktion_oben","Bildnorm_oben"],[
        [*r["pair"],r["source"],*r["codes"],*r["decisions"],"NEIN" if r["outside_old_box"] else "JA",
         r["upper_contraction"],r["upper_image"]] for r in data["cases"]])
    files["Impulsaustausch.tsv"]=register(["Fest_1","Fest_2","Freier_Impuls_A","Freier_Impuls_B",
        "Quelle_vorher","Quelle_nachher","Delta_G_A_unten","Delta_G_A_oben"],[
        [*t["pair"],*t["moving"],*t["sources"],*t["first_change"]] for t in data["transfers"]])
    files["Dreierregister.tsv"]=register(["Gebiet","Fest_1","Fest_2","Fest_3","Status","Norm_oben","Mindestabstand"],[
        [label,*r["triple"],r["status"],r.get("norm_upper"),r.get("minimum_adjacent_gap")]
        for label,certs in data["triples"].items() for r in certs])
    return files


if __name__=="__main__":
    if not __debug__:
        raise RuntimeError("Python ohne -O erforderlich")
    parser=argparse.ArgumentParser()
    parser.add_argument("--ausgabe",action="store_true",help="Register und Ergebnisdatei erzeugen")
    args=parser.parse_args()
    result=run()
    for filename,content in output(result).items():
        path=ROOT/filename
        if args.ausgabe:
            path.write_text(content,encoding="utf-8")
        else:
            assert path.read_text(encoding="utf-8")==content,filename
    print("Stationäre Fälle:",len(result["cases"]))
    print("Ausschlüsse je Gebiet:",{k:sum(s["status"]=="EXCLUDED" for s in rows) for k,rows in result["triples"].items()})
    print("Unabhängige Kontrollen:",result["independent_audit"])
