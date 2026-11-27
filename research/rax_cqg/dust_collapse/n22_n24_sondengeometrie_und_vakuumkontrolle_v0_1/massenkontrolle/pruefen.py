"""N22 source-free dust null controls and weight-scaling identities, exact arithmetic."""
import argparse
import csv
import hashlib
import json
from fractions import Fraction as F
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "input/Vergleichspaar.json"
INPUT_HASH = "c75c0c97c1b536d0140d77b4f01d8bfa0a2aab487a1b05a2b58f2ebf23159c2f"
EARLY = (0, 1, 2, 3)
LATE = (7, 8, 9, 10)
NODES = tuple(range(22))
INNER = tuple(i for i in NODES if i not in EARLY + LATE)
DEVICE = {(15, 16), (16, 18), (17, 18), (18, 7)}
GUARDS = DEVICE | {(15, 18)}
CLOCKS = (-12300, -12300, -12300, -2674, -1782, -1856, 13449,
          -20012, -11155, -288, 12, -288, -288, 20312)


def kernel(rel):
    descendants = {i: {j for a, j in rel if a == i} for i in NODES}
    ancestors = {j: {i for i, b in rel if b == j} for j in NODES}
    assert all(i not in descendants[i] for i in NODES)
    assert all(descendants[j] <= descendants[i] for i, j in rel)
    layers = {edge: len(descendants[edge[0]] & ancestors[edge[1]]) for edge in sorted(rel)}
    coefficients = {edge: F((1, -9, 16, -8, 0)[min(4, n)]) - F(edge in DEVICE, 10**11)
                    for edge, n in layers.items()}
    return layers, coefficients


def minus(a, b):
    return a[0] - b[1], a[1] - b[0]


def ratio(a, b):
    assert b[0] > 0
    values = [x/y for x in a for y in b]
    return min(values), max(values)


def clocks(pair):
    boxes = {i: (F(n, 10000), F(n, 10000)) for i, n in zip(INNER, CLOCKS)}
    for i in EARLY + LATE:
        intervals = [tuple(map(F, pair[side]["clock_box"][i])) for side in ("heavy", "light")]
        boxes[i] = min(l for l, h in intervals), max(h for l, h in intervals)
    return boxes


def dust_gradients(rel, y, w, k):
    g = dict.fromkeys(NODES, F(0))
    current = {}
    for i, j in sorted(rel):
        f = k[i, j] * w[j] * (y[j] - y[i])
        current[i, j] = f
        g[i] += f
        g[j] -= f
    return g, current


def projected_density_rows(rel, k, gap):
    bounds = {}
    for j in NODES:
        pieces = []
        for i, h in sorted(rel):
            if h == j:
                lo, hi = gap[i, j]
                assert lo > 0
                ends = [k[i, j] * lo**2, k[i, j] * hi**2]
                pieces.append((min(ends), max(ends)))
        bounds[j] = (19 + sum(v[0] for v in pieces),
                     19 + sum(v[1] for v in pieces))
    return bounds


def identities(rel, k):
    # Each term is proportional to w_receiver and independent of other weights.
    # All terms in a free row scale under a uniform rescaling outside the early ideal.
    assert all(i in EARLY for i, j in rel if j in EARLY)
    for j in INNER:
        assert all(receiver not in EARLY for i, receiver in rel if i == j and k[i, receiver])
        assert j not in EARLY
    # The sum of incoming-collar gradients cancels every term internal to the early ideal.
    for i,j in rel:
        assert int(i in EARLY)-int(j in EARLY) == int(i in EARLY and j not in EARLY)
    # The following finite test detects sign/receiver regressions in the exact flux code.
    y = {j:F(3*j-7,4) for j in NODES}
    w = {j:F(2*j+3,64) for j in NODES}
    g, flow = dust_gradients(rel, y, w, k)
    q = -sum(g[i] for i in EARLY)
    assert q == -sum(f for (i, j),f in flow.items() if i in EARLY and j not in EARLY)
    for scale in (F(0), F(1,16), F(1,2), F(1)):
        ws = {i:w[i] if i in EARLY else scale*w[i] for i in NODES}
        gs, _ = dust_gradients(rel, y, ws, k)
        assert all(gs[i] == scale*g[i] for i in INNER)
        assert -sum(gs[i] for i in EARLY) == scale*q


def evaluate():
    assert hashlib.sha256(INPUT.read_bytes()).hexdigest() == INPUT_HASH
    pair = json.loads(INPUT.read_text())
    rel = set(map(tuple, pair["relation"]))
    assert len(rel) == 152 and len(CLOCKS) == len(INNER) == 14
    layers, k = kernel(rel)
    boxes = clocks(pair)
    gaps = {(i, j):minus(boxes[j], boxes[i]) for i, j in rel}
    lowest = min(lo for lo, _ in gaps.values())
    assert lowest == F(3,100)
    assert max(max(abs(v) for v in gaps[e]) for e in GUARDS) < 8
    w = dict.fromkeys(NODES, F(0))
    # Given w_j=0, each monomial defining an edge current vanishes throughout every clock box.
    assert all(k[i,j]*w[j] == 0 for i,j in rel)
    midpoints = {i:(lo+hi)/2 for i,(lo,hi) in boxes.items()}
    g, flux = dust_gradients(rel, midpoints, w, k)
    assert all(x == 0 for x in (*g.values(), *flux.values()))
    density = projected_density_rows(rel, k, gaps)
    assert min(density[i][0] for i in INNER) > F(19,100)
    worst = min(INNER, key=lambda i:density[i][0])
    assert worst == 21 and density[2][1] < -15
    window = tuple(map(F, pair["normalized_window"]))
    normalized = {i:ratio(minus(boxes[i],boxes[3]),minus(boxes[7],boxes[3])) for i in NODES}
    inside = [i for i in NODES if window[0] <= normalized[i][0] <= normalized[i][1] <= window[1]]
    assert inside == [17,18,19,20]
    assert all(i in inside or normalized[i][1]<window[0] or normalized[i][0]>window[1] for i in NODES)
    # Necessary G6 and G15 at entirely empty interior, before imposing any new clock values.
    for i in (6,15):
        assert [(layers[i,j],k[i,j]) for j in LATE] == [(3,-8),(4,0),(5,0),(6,0)]
        assert not any(a == i and j in EARLY for a,j in rel)
        revived, _ = dust_gradients(rel, midpoints, w|{7:F(1,16)}, k)
        assert revived[i] == -F(1,2)*(midpoints[7]-midpoints[i]) < 0
        for side in ("heavy","light"):
            assert F(pair[side]["weight_box"][7][0]) > 0
    identities(rel,k)
    assert pair["external_mass_standard"] is None
    # If labels 4 and 1/4 are imposed as targets, an order-only identical estimate
    # has the minimax relative error where its under- and overestimation coincide.
    a,b=F(pair["nominal_light"]),F(pair["nominal_heavy"])
    best=2*a*b/(a+b); error=(b-a)/(a+b)
    assert (a,b,best,error)==(F(1,4),F(4),F(8,17),F(15,17))
    assert best/a-1 == 1-best/b == error
    data={
        "input_sha256":INPUT_HASH, "order_id":pair["order_id"],"relations":len(rel),
        "same_late_weights_empty_interior":"EXCLUDED_BY_G6_AND_G15",
        "same_late_weights_proof":{"late_receivers":LATE,"open_interval_counts":[3,4,5,6],
                                   "formula":"G6 = -8*w7*(Y7-Y6) < 0"},
        "zero_weight_collar_control":"EXISTS_SEPARATE_DUST_NULL_SECTOR",
        "strict_gap_lower":str(lowest), "free_clock_count":len(INNER),
        "interior_density_gradient_lower":str(density[worst][0]),
        "interior_density_gradient_argmin":worst, "one_sided_interior_lower_exceeds":"19/100",
        "collar_density_gradient_D2_upper":str(density[2][1]),
        "one_sided_all_weights_with_given_collar_times":"EXCLUDED_BY_D2",
        "clock_window_events":inside, "occupied_window_events":[],
        "edge_currents_all_zero":True,"clock_gradients_all_zero":True,
        "signed_flux_Q":"0","residence_proxy_B":"0",
        "scale_support":"outside fixed early ideal 0..3, including late Dirichlet weights",
        "model_ratio_target_only":{"light":str(a),"heavy":str(b),"best_common":str(best),
                                   "minimax_relative_error_lower":str(error)},
        "independent_positive_mass_standard":None,"physical_vacuum_certification":"OPEN",
        "physical_pilot_radii":[None]*8,"physical_P3":{"status":"NOT_RUN","count":60},
    }
    table=StringIO()
    writer=csv.writer(table,delimiter="\t",lineterminator="\n")
    writer.writerow(("Ereignis","Uhrrolle","Y_unten","Y_oben","w","D_unten","D_oben","x_unten","x_oben"))
    for i in NODES:
        writer.writerow((i,"Innen" if i in INNER else "Dirichlet",*boxes[i],0,*density[i],*normalized[i]))
    return {"Ergebnisse.json":json.dumps(data,indent=2,sort_keys=True)+"\n","Nullkontrolle.tsv":table.getvalue()}


if __name__=="__main__":
    if not __debug__:
        raise RuntimeError("Prüfung ohne -O ausführen")
    parser=argparse.ArgumentParser()
    parser.add_argument("--ausgabe",action="store_true");args=parser.parse_args()
    for name,content in evaluate().items():
        if args.ausgabe:(ROOT/name).write_bytes(content.encode())
        else:assert (ROOT/name).read_bytes()==content.encode(),name
    print("152 Uhrordnungen, 14 positive Innen-D-Ableitungen, 152 verschwindende Ströme und zwei Ausschlussformen bestätigt.")
