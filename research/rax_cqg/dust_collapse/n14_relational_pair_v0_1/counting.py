"""Exact marked-path counting tests using every fully admissible N14 end type."""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, permutations
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
PAIRS = tuple(combinations(range(6), 2))
LABELS = tuple(permutations(range(6)))
MARKS = tuple((0, 1, 2, *p) for p in permutations((3, 4, 5)))
PAIR_MASK = sum(1 << (6*i+j) for i in range(5) for j in range(5) if i != j)
SWAP = (0, 1, 2, 4, 3, 5)


def encode(edges, perm):
    return sum(1 << (6*perm[i]+perm[j]) for i, j in edges)


def edges_of(code):
    return [(i, j) for i in range(6) for j in range(6) if code & (1 << (6*i+j))]


def study(root):
    target = {int(p): Q(v) for p, v in root['target_pair_marginal'].items()}
    ordered = {}
    for p in target:
        q = encode(edges_of(p), SWAP)
        ordered[p] = ordered[q] = p
    counts = {p: Counter() for p in target}
    aut = {}
    selected = {}
    orbit_ids = set()
    for end in root['fully_admissible_end_types']:
        edges = [ij for k, ij in enumerate(PAIRS) if end & (1 << k)]
        labelled = {encode(edges, perm) for perm in LABELS}
        aut[end] = len(LABELS) // len(labelled)
        for code in labelled:
            if code & PAIR_MASK not in ordered:
                continue
            orbit = {encode(edges_of(code), perm) for perm in MARKS}
            if all((c & PAIR_MASK) in ordered for c in orbit):
                orbit_ids.add(min(orbit))
                counts[ordered[code & PAIR_MASK]][end] += 1
                if end in (1790, 5374):
                    selected.setdefault(end, []).append(code)
    assert len(orbit_ids) == root['fully_admissible_orbits']
    assert sum(row.total() for row in counts.values()) == root['paths_valid_in_all_six_orders']
    assert set.union(*(set(row) for row in counts.values())) == set(aut)
    tests = {}
    for name, coeff in [('uniform', {k: Q(1) for k in aut}),
                        ('inverse_automorphisms', {k: 1/Q(n) for k, n in aut.items()})]:
        raw = {p: sum(n*coeff[e] for e, n in row.items()) for p, row in counts.items()}
        norm = sum(raw.values())
        actual = {p: v/norm for p, v in raw.items()}
        distance = sum(abs(target[p]-actual[p]) for p in target)/2
        witness = max(target, key=lambda p: abs(target[p]-actual[p]))
        tests[name] = {'total_variation': str(distance), 'largest_gap_prefix_class': witness,
                       'expected': str(target[witness]), 'obtained': str(actual[witness])}
    assert tests['uniform']['total_variation'] == root['uniform_path_law_pair_marginal_TV']
    # A left-null vector excludes even complex per-end coefficients under the
    # *given linear coefficient marginal*. Positivity is not used in this test.
    import sympy as sp
    rows, ends = sorted(target), sorted(aut)
    matrix = sp.Matrix([[counts[p][j] for j in ends] for p in rows])
    b = sp.Matrix([sp.Rational(target[p]) for p in rows])
    impossible = []
    for v in matrix.T.nullspace():
        defect = (v.T*b)[0]
        if defect:
            assert v.T*matrix == sp.zeros(1, len(ends))
            impossible.append({'multiplier_by_prefix': {str(p): str(a) for p, a in zip(rows,v) if a},
                               'target_product': str(defect)})
    result = {'marked_paths': sum(row.total() for row in counts.values()),
              'endtypes':len(ends), 'prefix_classes':len(rows), 'tests':tests,
              'rank_terminal_map':matrix.rank(), 'left_null_witness':min(impossible, key=lambda v:len(v['multiplier_by_prefix']), default=None)}
    from marginal_distance import minimum
    result["best_terminal_law"] = minimum(matrix,b,rows,ends)
    return result, selected


def run():
    archived = json.loads((BASE/'inputs/exchange.json').read_text())
    weights = json.loads((BASE/'inputs/weights.json').read_text())
    out = {}
    for name, root in archived.items():
        out[name], selected = study(root)
        if name == 'one':
            columns = []
            for branch in ('A','B'):
                entry = weights[branch]
                codes = selected[entry['end']]
                assert sorted(codes) == entry['codes']
                for perm in MARKS:
                    col = Counter(encode(edges_of(c),perm) & PAIR_MASK for c in codes)
                    columns.append({p:Q(v,len(codes)) for p,v in col.items()})
            assert all(x == columns[0] for x in columns)
            assert columns[0] == {int(p):Q(v) for p,v in weights['common_unit_column_in_each_of_six_marked_cuts'].items()}
            out['one']['selected_column'] = {str(p): str(v) for p,v in sorted(columns[0].items())}
    return out


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
