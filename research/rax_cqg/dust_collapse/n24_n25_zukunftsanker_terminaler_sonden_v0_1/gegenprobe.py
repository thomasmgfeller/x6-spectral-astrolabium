"""Separate order census and direct rational checks of the physical rows."""
import csv
from fractions import Fraction as F
from hashlib import sha256
import json
from itertools import combinations
from pathlib import Path

from model import DEVICE, EMPTY, ROOT, WINDOW, inputs, minimal_anchor_orders
from schranken import ACTIVE, constraints, initial_boxes, moment_rows, with_terminal_clock


def old_ideals(relation):
    antichains = [frozenset()]
    for v in range(22):
        antichains += [a|{v} for a in antichains
                       if all((i,v) not in relation and (v,i) not in relation for i in a)]
    return {a|{i for i,j in relation if j in a} for a in antichains}


def direct_layers(edges, n):
    past = [{h for h in range(n) if (h,j) in edges} for j in range(n)]
    future = [{h for h in range(n) if (j,h) in edges} for j in range(n)]
    values = [1,-9,16,-8]
    result = {}
    for i,j in edges:
        assert i!=j and (j,i) not in edges and future[j]<=future[i]
        size = len(future[i]&past[j])
        result[i,j] = F(values[size] if size<4 else 0)-F((i,j) in DEVICE,10**11)
    return result


def orders(pair, rel):
    seen = old_ideals(rel)
    assert len(seen)==337
    reg = list(csv.DictReader((ROOT/"N24_Register.tsv").open(),delimiter="\t"))
    decode = lambda t: frozenset() if t=="∅" else frozenset(map(int,t.split(",")))
    assert {decode(row["Alte_Vergangenheit_22"]) for row in reg}==seen
    for row in reg:
        p=decode(row["Alte_Vergangenheit_22"])
        r23=rel|{(i,22) for i in p}
        # Any old past of 23 is recovered by first adjoining it as a maximal event
        # above an antichain in N23. Require 22 to occur in that downward closure.
        # With 22 terminal, a generating antichain must then contain 22.
        generators=[{22}]
        for i in range(22):
            generators += [s|{i} for s in generators
                           if all((i,j) not in r23 and (j,i) not in r23 for j in s)]
        pasts = {frozenset(s|{a for a,b in r23 if b in s}) for s in generators}
        assert len(pasts)==int(row["N24_Ordnungen"])
        hits={18:0,19:0}
        union=0
        for s in pasts:
            assert 22 in s and p<=s
            found=set()
            for q in (18,19):
                if q in s and (q,22) not in r23 and any((i,q) in rel and i not in EMPTY for i in p):
                    found.add(q)
                    hits[q]+=1
            union+=bool(found)
        assert (hits[18],hits[19],union)==tuple(int(row[s]) for s in
                         ("Partner18","Partner19","Mindestens_ein_Partner"))
        for side,col in (("heavy","N23_Zeitstatus_schwer"),("light","N23_Zeitstatus_leicht")):
            times=pair[side]["normalized_clocks"]
            known=max([WINDOW[0],*[F(times[j][1]) for j in p]])<WINDOW[1]
            assert known==(row[col]=="ZEUGE")
    # Brute force only on subsets of the principal ideal, then check the ideal
    # and old comparability requirements directly, without topological enumeration.
    all_pilot=set()
    next_counts={}
    for q in (18,19):
        minimal={q}|{i for i,j in rel if j==q}
        for b in seen:
            if not minimal<=b or len(b)>len(minimal)+1:
                continue
            subsets=[frozenset(g) for n in range(len(b)+1) for g in combinations(b,n)
                     if all(i in g for i,j in rel if j in g)]
            triples={(q,p,a) for a in subsets for p in subsets if p and q not in p and p<=a}
            if b==minimal:
                all_pilot.update(triples)
            else:
                next_counts[q,tuple(b-minimal)[0]]=len(triples)
    assert all_pilot=={(q,p,a) for q,p,a,ext in minimal_anchor_orders(rel)}
    assert next_counts=={(18,3):349,(18,19):233,(19,3):46,(19,17):60,(19,20):60}
    return next_counts


def evaluate(form,assign):
    return sum(c*(1 if not n else assign[n]) for n,c in form.items())


def physical_rows(pair, rel):
    for idx,(q,p,a,ext) in enumerate(minimal_anchor_orders(rel)):
        k=direct_layers(ext,25)
        assert (k[22,23],k[22,24],k[23,24])==(1,-9,1)
        for trial in (1,2):
            # Distinct rational arguments for polynomial identities. These points
            # do not purport to solve the coupled field equations.
            y=[F((i+trial)**2 + trial*i,13+trial) for i in range(25)]
            h={j:sum(c*(y[j]-y[i]) for (i,v),c in k.items() if v==j) for j in (21,23,24)}
            d={j:19+sum(c*(y[j]-y[i])**2 for (i,v),c in k.items() if v==j)
               for j in (16,18,19,21,23,24)}
            assign={f"y{i}":v for i,v in enumerate(y)}
            assign.update({f"m{i}_{j}":y[i]*y[j] for i in range(25) for j in range(i,25)})
            t=y[23]-y[22]
            v=y[24]-y[23]
            rows=constraints(pair,"heavy",q,ext)
            assert evaluate(rows["H23_upper_t"],assign)==9*h[23]-t
            assert evaluate(rows["H23_upper_v"],assign)==9*h[23]-v
            assert evaluate(rows["H23_lower"],assign)==-h[23]
            assert evaluate(rows["H24+"],assign)==h[24]
            boxes=with_terminal_clock(initial_boxes(pair,"heavy"),ext)
            rows=moment_rows(pair,"heavy",q,ext,boxes)
            assert all(evaluate(rows[f"D{j}+"],assign)==val for j,val in d.items())
            assert evaluate(rows["paired_impulses+"],assign)==9*h[23]*(t+v)-t*v
            for j in boxes:
                for end in (21,24):
                    assert evaluate(rows[f"H{end}_y{j}+"],assign)==h[end]*y[j]
            if sum(c for (i,j),c in k.items() if j==24)==0:
                del boxes[24]
                reduced=moment_rows(pair,"heavy",q,ext,boxes)
                assert evaluate(reduced["D24+"],assign)==d[24]-2*y[24]*h[24]
        # At positive test gaps the ratio solves the probe equation. Equal
        # weights fail and a perturbed ratio changes its sign as expected.
        for t,v in ((F(1),F(1)),(F(2,7),F(4,5))):
            r=t/(9*(t+v))
            assert 0<r<F(1,9) and t-9*r*(t+v)==0
            assert t-9*2*r*(t+v)<0<t-9*r/2*(t+v)
            assert t-9*(t+v)<0
    return idx+1


def main():
    digests={"Terminalregister.tsv":"ef1334a6f6a87eafc6ae896461e507850687be8b190e792cbd527382c8dba200",
             "Vergleichspaar.json":"c75c0c97c1b536d0140d77b4f01d8bfa0a2aab487a1b05a2b58f2ebf23159c2f"}
    for fn,d in digests.items():
        assert sha256((ROOT/"input"/fn).read_bytes()).hexdigest()==d
    pair,rel=inputs()
    for side in ("heavy","light"):
        assert pair[side]["positive_in_window"]==[18,19]
        assert [q for q,((lo,hi),(a,b)) in enumerate(zip(pair[side]["normalized_clocks"],pair[side]["weight_box"]))
                if F(a)>0 and WINDOW[0]<=F(lo)<=F(hi)<=WINDOW[1]]==[18,19]
    next_counts=orders(pair,rel)
    assert physical_rows(pair,rel)==175
    totals=json.loads((ROOT/"Ergebnisse.json").read_text())
    assert totals["n24"]==23356 and totals["n24_topology_q18_or_q19"]==13338
    print("Eingabedaten, 23 356 N24-Ordnungen, 175 N25-Ordnungen und Feldidentitäten bestätigt.")
    print("Genau ein zusätzlicher alter Vorfahr von 24:", sum(next_counts.values()),
          "Partner/Ordnungs-Fälle je Präparation, nur kombinatorisch gezählt.")


if __name__=="__main__":
    if not __debug__:raise RuntimeError("Bitte ohne -O ausführen")
    main()
