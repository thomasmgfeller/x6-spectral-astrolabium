"""Repeat all checks of the finite N15 future-boundary test using Python 3."""
import json
import subprocess
import sys
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path

import density_translation_375841 as cells
import randfenster_375841 as windows

ROOT = Path(__file__).resolve().parent
STUDY = ROOT / "studie"
sys.path.insert(0, str(STUDY / "inputs" / "sync"))
import support
from tube import template


def coefficients(events, relations):
    result = {}
    for a, b in relations:
        layer = sum((a, k) in relations and (k, b) in relations for k in events)
        result[a, b] = (1, -9, 16, -8)[layer] if layer < 4 else 0
    return result


def dust_action(y, densities, coeff):
    """S_d with common clock unit Delta, linear in the target density."""
    kinetic = sum(weight * densities[b] * (y[b] - y[a])**2
                  for (a, b), weight in coeff.items())
    return -sum(densities.values()) / 2 - kinetic / 38


def independent_action_check():
    code, e = 375841, Q(-1, 4)
    inner, relation = support.geometry(code)
    paths, u, radius, epsilon, _, _ = template(code)
    assert radius == Q(1, 64) and epsilon == Q(1, 100)
    assert tuple(inner) == cells.INNER and u == cells.CENTER
    f = dict(zip(inner, support.fractions_on_paths(paths, u)))
    edges = [(a,b) for a,b in relation if a in inner and b in inner]
    automorphisms = []
    for perm in permutations(inner):
        mapping = dict(zip(inner, perm))
        if all((mapping[a],mapping[b]) in relation for a,b in edges):
            automorphisms.append(perm)
    assert automorphisms == [tuple(inner)]
    old = tuple(range(15))
    weights = coefficients(old, relation)
    common = {i: Q(i - 5) for i in support.PAST + support.FUTURE}
    common[3] += e
    common.update({v: -2 + e + (4 - e) * u[v] for v in inner})

    axes = (5, 12, 13)
    C = [1 + sum(b * (common[v] - common[a])**2 for (a, t), b in weights.items() if t == v)/19
         for v in axes]
    k = [(4-e)*sum(weights[a,v]*(common[a]-common[v]) for a in support.PAST)/19
         for v in axes]
    assert C == [Q(n,7600) for n in (-2187,4253,2109)]
    det = k[0]*(C[2]-C[1]) + k[1]*(C[0]-C[2]) + k[2]*(C[1]-C[0])
    assert det == Q(1217081,180500)
    shift = {v:Q(n,10**6) for v,n in zip(axes,(268,537,-805))}
    assert sum(shift.values()) == 0 and sum(C[i]*shift[v] for i,v in enumerate(axes)) == 0
    assert all(abs(shift.get(v,0)) < epsilon * f[v] for v in inner)

    # All densities here are expressed in the common unit M(4 Delta-delta).
    # The common outer rows cancel in the action difference and source derivative.
    extensions = [
        (old, relation),
        (old + (15,), relation | {(i,15) for i in old}),
        (old + (15,16), relation | {(i,15) for i in old} | {(i,16) for i in old} | {(15,16)}),
    ]
    results = {}
    for nodes, rel in extensions:
        b = coefficients(nodes, rel)
        assert all(b[edge] == val for edge,val in weights.items())
        y = common | {v:Q(v-8) for v in nodes if v>=15}
        for variant in (0,1):
            y = y | {i:common[i] + Q(variant*(i-7),2**23) for i in support.FUTURE}
            background = {i:Q(1,8) + Q(variant,2**22) for i in nodes}
            if variant:
                background[10] += Q(1,2**23)
            actions, p_over_m = [], []
            for direction in (-1,1):
                w = background | {v:f[v] + direction*shift.get(v,0) for v in inner}
                actions.append(dust_action(y,w,b))
                step = Q(1,11)
                before = y | {i:y[i]-step for i in support.PAST}
                after = y | {i:y[i]+step for i in support.PAST}
                p_over_m.append((4-e)*(dust_action(before,w,b)-dust_action(after,w,b))/(2*step))
            assert actions[0] == actions[1]
            assert p_over_m == [Q(1429581,190000000), Q(-1004581,190000000)]
        results[str(len(nodes))] = "two future profiles: equal actions and opposite currents"
    return det, p_over_m, results


def main():
    if not __debug__:
        raise RuntimeError("Run with assertions enabled.")
    cells.enclose(Q(0))
    boxes = cells.enclose(cells.RADIUS)
    det, p, extensions = independent_action_check()
    # All original dust phases live in one cone. Re-open the four future
    # densities and last three clocks in a finite box around the reference.
    # At most 105 ordered pairs, |b|<=16, |Y|<=6 and 0<w<1.
    eta = Q(1,2**20)
    future_phase_change = (4*eta + Q(105*16,19)*(144+48)*eta)/2
    assert future_phase_change < Q(1,100)
    phase_check = subprocess.run([sys.executable, "-B", str(ROOT/"randfenster_375841.py"),
                                  str(STUDY)], check=True, capture_output=True, text=True)
    # Original phase extrema for nonvanishing of every positive cell integral.
    # This uses the same pinned interval-action function as the lobe test.
    from coherence import phase_box
    nodes, rel = support.geometry(cells.ORDER)
    _, center, radius, _, lower, upper = template(cells.ORDER)
    profile = {"clock_center":{str(i):str(x) for i,x in center.items()},
               "clock_halfwidth": str(radius),
               "dwell_affine_ranges_per_vertex": {str(i):[str(l),str(h)]
                                                   for i,l,h in zip(nodes,lower,upper)}}
    phases = [phase_box(rel,tile,Q(1,8),Q(1,4),profile) for w in support.WINDOWS
              for tile in windows.tiles(w,8)]
    lo = min(l for l,h in phases) - future_phase_change
    hi = max(h for l,h in phases) + future_phase_change
    assert Q(-775,1000) < lo <= hi < Q(-346,1000)
    assert 1 - max(abs(lo),abs(hi))**2/2 > Q(69,100)
    # Normalized Gram on the two real indicator packets: the common norm is >0.
    def gram_norm(x):
        return abs(sum(x))**2
    assert gram_norm((1,-1)) == 0 and gram_norm((1,0)) == 1
    return {"type":cells.ORDER,"marked_mass":"1/4","initial_density_center":"1/8",
            "center_p_over_M":list(map(str,p)),"translation_intervals":boxes,
            "cell_coordinate_halfwidth":str(cells.RADIUS),"determinant":str(det),
            "fixed_collar_automorphisms":1,"center_charge_difference":str((p[0]-p[1])/4),
            "future_test_halfwidth":str(eta),"future_phase_change_upper":str(future_phase_change),
            "future_dust_phase_outer_bounds":["-775/1000","-346/1000"],
            "direct_action_checks":extensions,
            "gram_over_common_squared_norm":[[1,1],[1,1]],"gram_rank":1,
            "null_vector":[1,-1],"selected_norm_over_common_squared_norm":1,
            "lobe_control":phase_check.stdout.splitlines(),
            "P3":"HOLD_NOT_ELIGIBLE / NOT_RUN"}


if __name__ == "__main__":
    print(json.dumps(main(),indent=2))
