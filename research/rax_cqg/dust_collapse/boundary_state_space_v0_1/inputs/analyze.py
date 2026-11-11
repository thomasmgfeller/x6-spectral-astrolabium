"""Exact directed-carrier audit. No physical matter kernel is supplied."""
from pathlib import Path
from itertools import product, permutations
from collections import Counter
from fractions import Fraction
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'inputs'))
import gluing as g

L, M, R = (0, 1), (2,), (3, 4)
OPTIONAL = tuple((i, j) for i in L for j in M + R) + ((2, 3), (2, 4))

def fixed_edges(x, y):
    return ({(0, 1)} if x == 'K' else set()) | ({(3, 4)} if y == 'K' else set())

def admissible(code, x, y, covered=False):
    rel = set(g.pairs(code, 5))
    if not g.valid(code, 5):
        return False
    if rel - set(OPTIONAL) != fixed_edges(x, y):
        return False
    if not any((i, 2) in rel for i in L) or not any((2, j) in rel for j in R):
        return False
    if covered:
        return all(any((i, j) in rel for j in R) for i in L) and all(
            any((i, j) in rel for i in L) for j in R)
    return True

def carrier(x, y, covered=False):
    codes = []
    for flags in product((False, True), repeat=len(OPTIONAL)):
        edges = fixed_edges(x, y) | {e for e, use in zip(OPTIONAL, flags) if use}
        code = g.encode(edges, 5)
        if admissible(code, x, y, covered):
            codes.append(code)
    return sorted(codes)

def boundary_group(x, y):
    left = tuple(permutations(L)) if x == 'A' else (L,)
    right = tuple(permutations(R)) if y == 'A' else (R,)
    return tuple(l + M + r for l in left for r in right)

def summarize(x, y, covered):
    codes = carrier(x, y, covered)
    group = boundary_group(x, y)
    orbits = {}
    for code in codes:
        orbit = sorted({g.relabel(code, 5, p) for p in group})
        representative = min(orbit)
        if representative not in orbits:
            stabilizer = sum(g.relabel(code, 5, p) == code for p in group)
            orbits[representative] = {
                'representative': representative, 'members': orbit,
                'stabilizer': stabilizer, 'weight': str(Fraction(1, stabilizer))}
    poly = Counter(int(g.action(c, 5)) for c in codes)
    phase_values = {z: [str(a) for a in g.poly_readout(poly, z)] for z in ('1', '-1', 'i')}
    return {
        'count': len(codes), 'codes': codes, 'group_order': len(group),
        'orbits': list(orbits.values()),
        'orbit_weight_sum': str(sum((Fraction(o['weight']) for o in orbits.values()), Fraction())),
        'F4_polynomial_raw': {str(e): v for e, v in sorted(poly.items())},
        'raw_phase_readouts': phase_values,
    }

def run(out):
    out.mkdir(parents=True, exist_ok=True)
    result = {
        'status': 'EXACT_COMBINATORICS_ONLY',
        'boundary_order': 'input X then output Y; NOT a matrix row convention',
        'L': L, 'I': M, 'R': R,
        'weak': {}, 'covered': {},
        'action_scope': 'F4 counts only; no dust, scalar, outer boundary action, or physical amplitude',
    }
    for x, y in product('AK', repeat=2):
        for name, covered in [('weak', False), ('covered', True)]:
            result[name][x+y] = summarize(x, y, covered)
    (out / 'carriers.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=ROOT/'results')
    run(parser.parse_args().out)
