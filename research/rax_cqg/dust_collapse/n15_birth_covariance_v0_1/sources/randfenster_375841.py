"""Rational proof of separate and common charge support in the two offset windows.

Usage: python3 -B randfenster_375841.py <PR-336 study directory>
Only Python's standard library and the pinned files below are needed.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from pathlib import Path
import sys


SOURCE_HASHES = {
    "support.py": "19a1ef8caef8f371f53984604b00d32e1af8f95b4d9c9756713cfbab2b36bc61",
    "tube.py": "b062243d601780511e87504ac980961d9c8016348aafe82ea90764550f564701",
    "coherence.py": "66c7e632c09559b87a4791ada16f601826ef431404e5237a5375c67012e46c8d",
}


def product_bound(a, b):
    corners = [x*y for x, y in product(a, b)]
    return min(corners), max(corners)


def tiles(interval, count):
    left, right = interval
    step = (right-left)/count
    for j in range(count):
        yield left+j*step, left+(j+1)*step


def edge_coefficients(past, inner, relation):
    # The derivative of the dust action for v is sum_i b_iv(Y_i-Y_v).
    # Y_i=i-5 except for an additional e=delta/Delta at i=3.
    # It has the form c + b3 e - s Y_v.
    rows = {}
    for v in inner:
        coefficients = {}
        for i in past:
            assert (i, v) in relation
            n = sum((i, k) in relation and (k, v) in relation for k in range(15))
            coefficients[i] = (1, -9, 16, -8)[n] if n < 4 else 0
        c = sum(b*(i-5) for i, b in coefficients.items())
        rows[v] = c, coefficients[3], sum(coefficients.values())
    return rows


def right_tile_bound(e_range, inner, center, radius, epsilon, dwell_bounds, rows):
    # u and e enter each current factor bilinearly. The four corner values
    # enclose that factor exactly on this rectangular projection. Subsequent
    # independent bounds on dwell fractions/density widths are conservative.
    lower = upper = Q(0)
    for v in inner:
        c, b3, s = rows[v]
        us = (center[v]-radius, center[v]+radius)
        factors = [c + b3*e - s*(-2+4*u+(1-u)*e) for u, e in product(us, e_range)]
        relative_density = product_bound(dwell_bounds[v], (1-epsilon, 1+epsilon))
        lo, hi = product_bound((min(factors), max(factors)), relative_density)
        lower += lo
        upper += hi
    return product_bound((lower/19, upper/19), (4-e_range[1], 4-e_range[0]))


def audit(study):
    src = study.resolve()/"inputs"/"sync"
    for name, expected in SOURCE_HASHES.items():
        if sha256((src/name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Source hash mismatch: {name}")
    sys.path.insert(0, str(src))
    import support
    from tube import template
    from coherence import phase_box

    mass, rho = Q(1, 4), Q(1, 8)
    inner, relation = support.geometry(375841)
    paths, center, radius, epsilon, fmin, fmax = template(375841)
    assert inner == (4, 5, 6, 11, 12, 13, 14)
    assert radius == Q(1, 64) and epsilon == Q(1, 100)
    assert support.WINDOWS == ((Q(-3, 32), Q(-1, 32)), (Q(1, 32), Q(3, 32)))
    dlo, dhi = support.DELTA
    assert dlo**4 <= Q(3, 722) <= dhi**4
    left, right = support.WINDOWS
    assert (4*dlo-right[1])*min(fmin)*mass*(1-epsilon) > 0
    assert (4*dhi-left[0])*max(fmax)*mass*(1+epsilon) < 1
    dwell_bounds = dict(zip(inner, zip(fmin, fmax)))
    rows = edge_coefficients(support.PAST, inner, relation)
    inv_delta = (1/dhi, 1/dlo)

    # Both interior profiles retain their respective signs for every left-hand
    # offset; all inner densities take the centre values M (4 Delta-delta) f_v(u).
    profiles = (
        ("positive", (0, 1, 0, 1, -1, -1, 0), (Q(5335319,6553600), Q(52555241,26214400))),
        ("negative", (0, -1, 0, -1, 1, 1, 1), (Q(615207,3276800), Q(29270873,13107200))),
    )
    e_range = product_bound(left, inv_delta)
    for label, shifts, expected in profiles:
        u = {v: center[v]+Q(7,8)*radius*t for v, t in zip(inner, shifts)}
        assert all(0 < center[v]-radius < u[v] < center[v]+radius < 1 for v in inner)
        assert all(u[i] < u[j] for i,j in relation if i in u and j in u)
        dwell = dict(zip(inner, support.fractions_on_paths(paths, u)))
        assert min(dwell.values()) > 0 and sum(dwell.values()) == 1
        a = sum(dwell[v]*(c-s*(-2+4*u[v])) for v,(c,b3,s) in rows.items())
        b = sum(dwell[v]*(b3-s*(1-u[v])) for v,(c,b3,s) in rows.items())
        assert (a,b) == expected
        affine = sorted(a+b*e for e in e_range)
        bounds = product_bound(affine, ((4-e_range[1])/19,(4-e_range[0])/19))
        if label == "positive":
            assert bounds[0] > Q(1,100)
        else:
            assert bounds[1] < -Q(1,100)
        print(f"Left window, fixed {label} profile: p/M "
              + ("> 1/100" if label=="positive" else "< -1/100")
              + f", affine coefficients ({a}, {b}).")

    bounds = [right_tile_bound(product_bound(tile, inv_delta), inner, center,
                               radius, epsilon, dwell_bounds, rows)
              for tile in tiles(right, 8)]
    lower, upper = min(a for a,b in bounds), max(b for a,b in bounds)
    assert lower > Q(5175,10**6) and upper < Q(393,1000)
    print("Entire right window and full internal box: 5175/1000000 < p/M < 393/1000.")

    # Coherent integration: common phase cone for both offsets, both signs,
    # and the whole outer past density band [rho-1/32,rho+1/32].
    profile = {"clock_center": {str(k): str(v) for k,v in center.items()},
               "clock_halfwidth": str(radius),
               "dwell_affine_ranges_per_vertex": {
                   str(k): list(map(str, pair)) for k,pair in dwell_bounds.items()}}
    boxes = [phase_box(relation, tile, rho, mass, profile)
             for window in support.WINDOWS for tile in tiles(window, 8)]
    width = max(y for x,y in boxes)-min(x for x,y in boxes)
    assert width < Q(409,1000)
    assert 1-width**2/2 > Q(916,1000)
    print("Common dust-phase width < 409/1000; pairwise cosine > 916/1000.")


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Use Python without -O so the assertions are active")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("study", type=Path)
    audit(parser.parse_args().study)
