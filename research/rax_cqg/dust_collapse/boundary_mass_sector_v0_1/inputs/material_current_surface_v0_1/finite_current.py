"""Signed action flux and two kinematic positive mass preparations on published finite orders."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
INPUT = HERE / "inputs"
sys.path.insert(0,str(INPUT / "variation_v0_1"))
sys.path.insert(0,str(INPUT / "current_calibration_v0_1"))
from variation import edges as action_edges, current_and_gradient
from gluing import encode
from current import Current

PAST = (0,1,2,3)
INNER = (4,5,6,11,12,13,14)
FUTURE = (7,8,9,10)
MASSES = (F(1,4),F(4))

def geometry(mask):
    relations = set(combinations(PAST,2)) | set(combinations(FUTURE,2))
    relations.update(product(PAST,INNER+FUTURE))
    relations.update(product(INNER,FUTURE))
    relations.update(e for bit,e in enumerate(combinations(INNER,2)) if mask & (1<<bit))
    return relations

def action_probe(relations):
    n = 15
    code = encode(relations,n)
    coeff = {(u,v):b for u,v,b in action_edges(code,n)}
    assert all(coeff[u,v]==0 for u in PAST for v in FUTURE)
    minima = [v for v in INNER if not any((u,v) in relations for u in INNER)]
    assert minima
    for v in minima:
        assert [coeff[u,v] for u in PAST]==[-8,16,-9,1]
    # Sum on Q(P) in units of beta/2. Variables: T0..2=(-5,-4,-3)*d, T3=t.
    # The density row of every minimal inner event is -3*d - t (independent of its clock).
    # d^2=2/(19*beta), beta=4/sqrt(6)<2. Thus d^2>1/19>(3/32)^2.
    assert F(1,19)>F(3,32)**2
    inners_with_both = sum(any(coeff[u,v]>0 for u in range(n) if (u,v) in coeff)
                           and any(coeff[u,v]<0 for u in range(n) if (u,v) in coeff) for v in INNER)
    # Cross-check the symbolic row with the archived current routine on two rational
    # coefficient probes. These d,t values exercise the algebra, not the physical scale.
    for d,t in [(F(2,7),F(-4,7)+F(1,16)),(F(3,10),F(-3,5)-F(1,16))]:
        T = [F(0)]*n
        for i in PAST+FUTURE:
            T[i] = (i-5)*d
        T[3] = t
        for k,v in enumerate(INNER):
            T[v] = F(k-3,15)
        for mass_center,active in [(F(1,8),False),(F(1,4),False),(F(1,8),True),(F(1,4),True)]:
            w = [F(0)]*n
            for i in PAST: w[i] = mass_center
            for i in FUTURE: w[i] = F(1,8)
            if active: w[minima[0]] = F(1,2)
            edges,grad = current_and_gradient(code,n,T,w)
            flux = sum(q for u,v,q in edges if u in PAST and v not in PAST)
            assert flux==sum(grad[u] for u in PAST)
            assert flux==(F(-1,4)*(3*d+t) if active else 0)
    return len(minima), inners_with_both

def transport(relations):
    start, stop = PAST[-1], FUTURE[0]
    sequence = (start,)+INNER+(stop,)
    edges = [(u,v) for u,v in relations if u in sequence and v in sequence
             and not any((u,k) in relations and (k,v) in relations for k in sequence)]
    # Internal canonical codes use ascending positions in INNER as a linear extension.
    pos = {u:i for i,u in enumerate(sequence)}
    assert all(pos[u]<pos[v] for u,v in edges)
    forward,back = {start:1},{stop:1}
    for v in sequence[1:]:
        forward[v] = sum(forward[u] for u,w in edges if w==v)
    for u in reversed(sequence[:-1]):
        back[u] = sum(back[v] for w,v in edges if w==u)
    total = forward[stop]
    assert total==back[start] and total>0
    fractions = {(u,v):F(forward[u]*back[v],total) for u,v in edges}
    mandatory = sum(forward[v]*back[v]==total for v in INNER)
    # PAST plus any inner order ideal: includes both bounding cuts.
    cuts = []
    for bits in range(128):
        selected = {u for k,u in enumerate(INNER) if bits & (1<<k)}
        if all(u in selected for u,v in relations if v in selected and u in INNER):
            cuts.append(set(PAST)|selected)
    for mass in MASSES:
        stream = Current(range(15),relations,{e:mass*f for e,f in fractions.items()},
                         {start:mass,stop:-mass})
        for cut in cuts:
            assert stream.cut_mass(cut)==mass
            assert stream.outward(cut)==mass
    return total,mandatory,len(cuts)

def run():
    catalog = json.loads((INPUT/"prefix_1564_two_event_v0_1/inputs/catalog.json").read_text())
    orders = sorted(int(k) for k,(a,_,b) in catalog["ranks_pure_free_mixed"].items() if a==b==0)
    assert len(orders)==catalog["counts"]["good"]==1048
    counts = Counter()
    path_hist, mandatory_hist, mix_hist = Counter(),Counter(),Counter()
    examples = {}
    for mask in orders:
        relations = geometry(mask)
        roots, mixed = action_probe(relations)
        paths, mandatory, cuts = transport(relations)
        path_hist[paths] += 1
        mandatory_hist[mandatory] += 1
        mix_hist[mixed] += 1
        counts["inner_rows_with_both_coefficient_signs"] += mixed
        counts["minimal_inner_rows_with_exact_hidden_density_response"] += roots
        counts["ideal_cuts_per_mass"] += cuts
        if paths>1 and "branching_order" not in examples:
            examples["branching_order"] = {"type":mask,"maximal_paths":paths,"mandatory_inner_events":mandatory}
    return {"orders":len(orders),"tested_masses":list(map(str,MASSES)),
            "balance_tests_both_masses":2*counts["ideal_cuts_per_mass"],**counts,
            "orders_with_nonunique_positive_routing":len(orders)-path_hist[1],
            "maximal_path_histogram":dict(sorted(path_hist.items())),
            "mandatory_inner_vertices_histogram":dict(sorted(mandatory_hist.items())),
            "mixed_incoming_coefficient_counts":dict(sorted(mix_hist.items())),"examples":examples,
            "inherited_raw_flux":{"empty_inner_densities":"0","only_one_minimal_density_positive":"-beta*w*(3*Delta+T3)/2",
                "fixed_positive_mass_on_inherited_boundary_preparation":False},
            "marked_positive_flux":{"initial_and_all_ideal_cut_masses":["1/4","4"],
                "status":"CONDITIONAL_EXACT","comoving_area_from_marks":None}}
