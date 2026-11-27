"""Independent finite-order census and exact symbolic checks of field identities."""
import argparse
import csv
import gzip
import json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as F
from itertools import combinations

from model import COLLAR, DEVICE, EMPTY, ROOT, boundary_hull, inputs
from schranken import constraints, initial_order_boxes, moment_rows


def ideals_from_antichains(rel):
    antichains=[frozenset()]
    for j in range(22):
        antichains += [s|{j} for s in antichains
                       if all((j,i) not in rel and (i,j) not in rel for i in s)]
    return {s|{i for i,j in rel if j in s} for s in antichains}


def census(rel,level):
    ideals=ideals_from_antichains(rel)
    result=set()
    for q in (18,19):
        minimum={q}|{i for i,j in rel if j==q}
        for b in ideals:
            if not minimum<=b or len(b-minimum)!=level:continue
            subsets=[frozenset(g) for n in range(len(b)+1) for g in combinations(b,n)
                     if all(i in g for i,j in rel if j in g)]
            for a in subsets:
                for p in subsets:
                    if not p<=a or q in p:continue
                    if any(i not in EMPTY and (i,q) in rel for i in p):
                        result.add((q,tuple(sorted(b-minimum)),p,a,b))
    return result


def direct_kernel(edges):
    past=[{i for i,j in edges if j==v} for v in range(25)]
    future=[{j for i,j in edges if i==v} for v in range(25)]
    assert all(i not in a for i,a in enumerate(past))
    assert all(future[j]<=future[i] for i,j in edges)
    return {(i,j):F((1,-9,16,-8,0)[min(4,len(future[i]&past[j]))])
            -F((i,j) in DEVICE,10**11) for i,j in edges}


# Polynomials have rational coefficients and monomials stored as sorted index tuples.
def plus(*terms):
    value=Counter()
    for term in terms:value.update(term)
    return {k:v for k,v in value.items() if v}


def scale(p,c):
    return {k:c*v for k,v in p.items() if c*v}


def times(a,b):
    value=Counter()
    for u,x in a.items():
        for v,y in b.items():value[tuple(sorted(u+v))]+=x*y
    return {k:v for k,v in value.items() if v}


def unpack(row):
    def key(s):
        if not s:return ()
        if s.startswith("y"):return (int(s[1:]),)
        return tuple(map(int,s[1:].split("_")))
    return {key(s):v for s,v in row.items() if v}


def field_checks(item):
    q,extra,p,a,b,proof,pair,rel=item
    ext=rel|{(22,23),(23,24),(22,24)}
    for j,s in ((22,p),(23,a),(24,b)):
        ext.update((n,j) for n in s)
    k=direct_kernel(ext)
    assert (k[22,23],k[22,24],k[23,24])==(1,-9,1)
    y=[{(i,):F(1)} for i in range(25)]
    def gap(i,j):return plus(y[j],scale(y[i],-1))
    def h(j):
        return plus(*(scale(gap(i,j),v) for (i,end),v in k.items() if end==j))
    def density(j):
        return plus({():F(19)},*(scale(times(gap(i,j),gap(i,j)),v)
                    for (i,end),v in k.items() if end==j))
    t=gap(22,23);v=gap(23,24)
    rows=constraints(pair,"both",q,ext)
    for key,want in (("H23_lower",scale(h(23),-1)),("H23_upper_t",plus(scale(h(23),9),scale(t,-1))),
                     ("H23_upper_v",plus(scale(h(23),9),scale(v,-1))),("H24+",h(24))):
        assert unpack(rows[key])==want
    if 21 in b:
        assert "H21+" not in rows and "H21-" not in rows
        if 21 in p:
            assert k[21,23]==-9 and k[21,24]==16 and unpack(rows["H21_new_negative"])==h(21)
        elif 21 not in a:
            assert k[21,24]==1 and unpack(rows["H21_new_positive"])==scale(h(21),-1)
        else:
            assert (k[21,23],k[21,24])==(1,-9)
    else:
        assert unpack(rows["H21+"] )==h(21)
    if "linear" in proof:return
    projected=proof.get("projected",False)
    event,upper=proof.get("cap",(None,None))
    boxes=initial_order_boxes(pair,"both",upper,event,ext,proof.get("terminal21",False))
    moments=moment_rows(pair,"both",q,ext,boxes)
    for j in boxes:
        if f"D{j}+" in moments:
            assert unpack(moments[f"D{j}+"])==density(j)
        if "H21+" in rows and 21 in boxes:
            assert unpack(moments[f"H21_y{j}+"] )==times(h(21),y[j])
    if "H21_new_middle" in moments:
        assert unpack(moments["H21_new_middle"])==scale(times(h(21),gap(21,22)),-1)
    if not projected:
        if 24 not in boxes:
            assert sum(c for (i,j),c in k.items() if j==24)==0
            assert unpack(moments["D24+"])==plus(density(24),scale(times(y[24],h(24)),-2))
        else:
            balance=plus(scale(times(h(23),gap(22,24)),9),scale(times(t,v),-1))
            assert unpack(moments["paired_impulses+"] )==balance
        for j in boxes:
            assert unpack(moments[f"H24_y{j}+"] )==times(h(24),y[j])
        return
    # Substitute the unique Y24 imposed by H24=0 before comparing polynomials.
    v=plus(*(scale(y[i],c) for (i,j),c in k.items() if j==24 and i!=23))
    y[24]=plus(y[23],v)
    assert h(24)=={} and (23,) not in h(23)
    balance=plus(scale(times(h(23),plus(t,v)),9),scale(times(t,v),-1))
    A=plus(density(23),scale(times(t,h(23)),-2))
    B=plus(density(24),scale(times(v,t),2))
    assert unpack(moments["proj_D23"])==A
    assert unpack(moments["proj_D24"])==scale(B,-1)
    assert unpack(moments["proj_balance+"])==plus(density(24),scale(density(23),9),scale(balance,-2))


def main(jobs):
    pair,rel=inputs();pair["both"]=boundary_hull(pair)
    result={}
    for level in (1,2):
        expected=census(rel,level)
        rows=list(csv.DictReader((ROOT/f"Fallregister_Stufe{level}.tsv").open(),delimiter="\t"))
        with gzip.open(ROOT/f"Zertifikate_Stufe{level}.json.gz","rt") as f:proofs=json.load(f)
        tested={};sides={};old21=Counter()
        for row in rows:
            groups=[frozenset(map(int,row[k].split(","))) for k in ("Alt_vor_22","Alt_vor_23","Alt_vor_24")]
            p,a,b=groups;q=int(row["Partner"])
            extra=tuple(map(int,row["Zusaetzliche_alte_Vorgaenger"].split(",")))
            key=(q,extra,p,a,b);i=int(row["Fall"])
            assert key not in tested or tested[key]==i
            tested[key]=i
            assert row["Kontakt"]=="AUSGESCHLOSSEN" and row["Praeparation"] not in sides.get(key,set())
            sides.setdefault(key,set()).add(row["Praeparation"])
        assert set(tested)==expected and all(s=={"heavy","light"} for s in sides.values())
        assert len(rows)==2*len(proofs) and set(tested.values())==set(range(len(proofs)))
        items=[]
        for (q,extra,p,a,b),idx in tested.items():
            if 21 in b:old21["P" if 21 in p else "A_only" if 21 in a else "B_only"]+=1
            items.append((q,extra,p,a,b,proofs[idx],pair,rel))
        with ProcessPoolExecutor(max_workers=jobs) as pool:
            for _ in pool.map(field_checks,items,chunksize=12):pass
        result[str(level)]={"cases":len(tested),"verdicts":len(rows),"old21_inside":dict(sorted(old21.items()))}
    ref=census(rel,0);next_cases=census(rel,3)
    assert len(ref)==175 and len(next_cases)==10272
    result["next_by_partner"]=dict(sorted(Counter(str(x[0]) for x in next_cases).items()))
    result["previous_minimal_family"]=len(ref)
    return result


if __name__=="__main__":
    if not __debug__:raise RuntimeError("Ohne -O ausführen")
    parser=argparse.ArgumentParser();parser.add_argument("--jobs",type=int,default=1)
    parser.add_argument("--ausgabe",action="store_true");args=parser.parse_args()
    result=main(args.jobs)
    answer=json.dumps(result,sort_keys=True,indent=2)+"\n"
    path=ROOT/"Gegenprobe.json"
    if args.ausgabe:path.write_text(answer)
    else:assert path.read_bytes()==answer.encode()
    print(answer)
