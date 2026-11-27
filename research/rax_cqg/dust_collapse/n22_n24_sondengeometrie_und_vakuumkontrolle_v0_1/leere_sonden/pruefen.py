"""Exact PR413 geometric ray controls and source-free future-collar obstruction."""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "pr413"))
from geometrie import balls, causal, extended_order, inside_clock, mul, probes, square
from stationaritaet import check as original_equations

FUTURE = (7, 8, 9, 10)
LAYERS = (1, -9, 16, -8, 0)
LEFT = F(15, 32)


def read_input(name, digest):
    data = (ROOT / "input" / name).read_bytes()
    assert sha256(data).hexdigest() == digest, name
    return json.loads(data)


def field(side, name):
    return [tuple(F(x) for x in pair) for pair in side[name]]


def diff(a, b):
    return a[0]-b[1], a[1]-b[0]


def total(terms):
    terms = list(terms)
    return sum(t[0] for t in terms), sum(t[1] for t in terms)


def coeff(rel, i, j, n):
    if (i, j) not in rel:
        return 0
    size = sum((i, h) in rel and (h, j) in rel for h in range(n))
    return LAYERS[min(4, size)]


def collar_residual(pattern, clocks, weights, x):
    # For each possible collar realization the raw clock is affine in x.
    z = total([mul(clocks[3], (1-x, 1-x)), mul(clocks[7], (x, x))])
    return total(mul((k,k), mul(weights[j], diff(clocks[j], z)))
                 for j,k in zip(FUTURE, pattern))


def last_before_seven(clocks, weights):
    # h_7 = 0. Cap each nondecreasing h_j at four without changing any kernel.
    offsets = [(0, *v) for v in combinations_with_replacement(range(5), 3)]
    patterns = sorted({tuple(LAYERS[min(4,i+n)] for i,n in enumerate(h)) for h in offsets})
    assert len(offsets) == 35 and len(patterns) == 8
    report = []
    for pattern in patterns:
        left = collar_residual(pattern, clocks, weights, LEFT)
        right = collar_residual(pattern, clocks, weights, F(1))
        if pattern == (1,0,0,0):
            # y_v<y_7 is a strict causal inequality. No lower bound on the gap.
            assert weights[7][0] > 0 and left[0] > 0
            sign = "positiv_bis_zum_offenen_Endpunkt"
        elif min(left[0], right[0]) > 0:
            sign = "positiv"
        else:
            assert max(left[1], right[1]) < 0
            sign = "negativ"
        report.append({"k":pattern, "G_15_32":left, "G_1":right, "Vorzeichen":sign})
    return report


def joint_sets(rows, close, relation, y, w):
    result = []
    for n in (2,3):
        for selected in combinations(range(3), n):
            ids = range(22,22+n)
            edges = relation.copy()
            separation = []
            for a,b in combinations(selected,2):
                d2 = total(square(diff(u,v)) for u,v in zip(rows[a]["point_box"], rows[b]["point_box"]))
                assert d2[0] > 0
                separation.append(d2[0])
            for i, idx in zip(ids, selected):
                one = close[idx]
                edges.update((j,i) for j in one["past"])
                edges.update((i,j) for j in one["future"])
            assert all((i,k) in edges for i,j in edges for b,k in edges if j==b)
            assert not any((i,j) in edges for i in ids for j in ids)
            for i,idx in zip(ids, selected):
                one = close[idx]
                # Restrict to the original 22 plus this readout. No other new
                # event enters any parent-density row used in the PR413 proof.
                sub = {(a,b) for a,b in edges if a not in set(ids)-{i} and b not in set(ids)-{i}}
                for j in (4,5,6,11,i):
                    for a in range(22+n):
                        assert coeff(sub,a,j,22+n)==coeff(edges,a,j,22+n)
                for j in range(22+n):
                    assert coeff(sub,i,j,22+n)==coeff(edges,i,j,22+n)
                assert not any(q in {4,5,6,11,i} for _,q in ((15,16),(16,18),(17,18),(18,7)))
                assert one["future"]==list(FUTURE)
                test = original_equations(relation,one,y,w)
                assert test["D22_window"][1] < F(-131,100)
                assert test["empty_G22_on_0_to_1"][1] < 0
            result.append({"N":22+n, "Bahnen":[rows[j]["von"] for j in selected],
                           "Relationen":len(edges), "minimaler_Quadratabstand_unten":min(separation),
                           "ausgeschlossene_Besetzungsmuster":2**n})
    return result


def main():
    pair=read_input("Vergleichspaar.json","c75c0c97c1b536d0140d77b4f01d8bfa0a2aab487a1b05a2b58f2ebf23159c2f")
    pos=read_input("Ortskoordinaten.json","a8bdf817687174d3c47d6ebf105974b41008a9037555e66da62a581c9f9601f4")
    source=read_input("Sonden_auf_N23.json","0e43915b9f8a83491630b3aae99c3b92a03bbf5e6527f256b747d5a5b05a45ae")
    rel=set(map(tuple,pair["relation"])); pos=[tuple(map(F,p)) for p in pos]
    assert len(pos)==22 and len(rel)==152 and all((a,b) in rel for a,b in combinations(FUTURE,2))
    out={}
    for side in ("heavy","light"):
        y=field(pair[side],"clock_box"); w=field(pair[side],"weight_box")
        clock=field(pair[side],"normalized_clocks")
        causal(pos,clock,rel);balls(pos,clock,inside_clock(clock,w))
        rays=probes(pos,clock,rel,extend=True)
        rows=[r for r in rays if [b["tag"] for b in r["balls"]]==["innen","aussen"]]
        assert len(rays)==46 and [(r["von"],r["durch"]) for r in rows]==[(3,11),(4,11),(5,11)]
        orders=[extended_order(pos,clock,rel,r) for r in rows]
        assert all(a==b["order"] for a,b in zip(orders,source[side],strict=True))
        joint=joint_sets(rows,orders,rel,y,w)
        assert len(joint)==4 and sum(r["ausgeschlossene_Besetzungsmuster"] for r in joint)==20
        out[side]={"Simultane_Anbindungen":joint,
                   "Letztes_neues_Ereignis_vor_7":last_before_seven(y,w)}
    return json.dumps(out, default=str, indent=2, sort_keys=True)+"\n"


if __name__=="__main__":
    if not __debug__: raise RuntimeError("Bitte ohne -O starten")
    parser=argparse.ArgumentParser()
    parser.add_argument("--ausgabe",action="store_true")
    args=parser.parse_args()
    actual=main().encode(); path=ROOT/"Ergebnisse.json"
    if args.ausgabe:path.write_bytes(actual)
    else:assert actual==path.read_bytes()
    print("Beide Präparationen, drei Bahnen, 40 simultane Besetzungsfälle und 16 Kragen-Vorzeichenprüfungen bestätigt.")
