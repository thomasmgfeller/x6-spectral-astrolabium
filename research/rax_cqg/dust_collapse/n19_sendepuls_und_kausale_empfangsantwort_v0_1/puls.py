"""Exact source responses and consistency certificates for the two specified models."""
from fractions import Fraction as F
import json
from math import gcd, lcm
from ordnung import load_background, operators, select


def block(matrix, rows, cols):
    return [[matrix[r][c] for c in cols] for r in rows]


def reduce_system(matrix, rhs):
    """Reduce a rational linear system, retaining the row-combination certificate."""
    nr, nc = len(matrix), len(matrix[0])
    width = len(rhs[0])
    work = [[*map(F, row), *map(F, target), *(F(i == j) for j in range(nr))]
            for i, (row, target) in enumerate(zip(matrix, rhs, strict=True))]
    pivots = []
    for col in range(nc):
        pos = len(pivots)
        pivot = next((k for k in range(pos, nr) if work[k][col]), None)
        if pivot is None:
            continue
        work[pos], work[pivot] = work[pivot], work[pos]
        divisor = work[pos][col]
        work[pos] = [v / divisor for v in work[pos]]
        for k, row in enumerate(work):
            if k != pos and row[col]:
                factor = row[col]
                work[k] = [v - factor * u for v, u in zip(row, work[pos])]
        pivots.append(col)
    reduced = [row[nc:nc + width] for row in work]
    transforms = [row[nc + width:] for row in work]
    return pivots, reduced, transforms


def vector_unit(i, nodes):
    return [int(k == i) for k in nodes]


def inverse(matrix):
    n = len(matrix)
    pivots, values, _ = reduce_system(matrix, [vector_unit(i, range(n)) for i in range(n)])
    if len(pivots) != n:
        raise ArithmeticError('singular free block')
    return values


def dot(a, b):
    return sum(x * y for x, y in zip(a, b, strict=True))


def primitive(vector):
    denominator = lcm(*(v.denominator for v in vector))
    scaled = [int(v * denominator) for v in vector]
    return [x // gcd(*scaled) for x in scaled]


def on_off(bg, matrix):
    inner = bg.inner
    sender, receiver = select(bg)
    local = block(matrix, inner, inner)
    green = inverse(local)
    fields = {}
    for name, src, amp in [('off', sender, 0), ('on', sender, 1),
                           ('negative', sender, -1), ('reverse', receiver, 1)]:
        source = [amp * v for v in vector_unit(src, inner)]
        response = [dot(row, source) for row in green]
        assert [dot(row, response) for row in local] == source
        fields[name] = {i: F(0) for i in bg.nodes}
        fields[name].update(zip(inner, response))
    on = fields['on']
    assert all(fields['off'][i] == 0 and fields['negative'][i] == -on[i] for i in bg.nodes)
    outside = [i for i in bg.nodes if i != sender and (sender, i) not in bg.relation and on[i]]
    catalogue = {}
    for k, src in enumerate(inner):
        column = [row[k] for row in green]
        assert [dot(row, column) for row in local] == vector_unit(src, inner)
        catalogue[src] = {'response': dict(zip(inner, map(str, column))),
                          'outside_future': [i for i, v in zip(inner, column)
                                             if v and i != src and (src, i) not in bg.relation]}
    values = {name: str(f[receiver]) for name, f in fields.items() if name != 'reverse'}
    return {'receiver': values, 'reverse_at_sender': str(fields['reverse'][sender]),
            'on_outside_future': outside,
            'on_in_strict_past': [i for i in outside if (i, sender) in bg.relation],
            'on_incomparable': [i for i in outside if (i, sender) not in bg.relation],
            'all_arms': {name: {i: str(v) for i, v in f.items()} for name, f in fields.items()},
            'all_inner_sources': catalogue,
            'retarded_inner_sources': [i for i, row in catalogue.items() if not row['outside_future']],
            'gates': {'nonzero': bool(on[receiver]), 'reverse_zero': not fields['reverse'][sender],
                      'causal_support': not outside, 'odd': True, 'off_zero': True}}


def retarded_feasibility(bg, hessian, release_future):
    sender, _ = select(bg)
    rows = bg.inner
    allowed = set(rows) | (bg.future if release_future else set())
    cols = sorted(j for j in allowed if j == sender or (sender, j) in bg.relation)
    a = block(hessian, rows, cols)
    rhs = vector_unit(sender, rows)
    pivots, reduced, transforms = reduce_system(a, [[v] for v in rhs])
    rank = len(pivots)
    witness = next((i for i in range(rank, len(rows)) if reduced[i][0]), None)
    report = {'variables': cols, 'inner_rows': rows, 'rank': rank,
              'augmented_rank': rank + int(witness is not None), 'solvable': witness is None}
    if witness is not None:
        left = primitive(transforms[witness])
        assert all(dot(left, col) == 0 for col in zip(*a))
        assert dot(left, rhs) != 0
        report.update(left_null_witness=dict(zip(rows, left)), witness_source=dot(left, rhs))
    else:
        x = [F(0)] * len(cols)
        for i, col in enumerate(pivots):
            x[col] = reduced[i][0]
        assert [dot(row, x) for row in a] == rhs
        report['one_solution'] = dict(zip(cols, map(str, x)))
    return report


def run():
    bg = load_background()
    z, r = select(bg)
    b, h = operators(bg)
    return {'source': z, 'receiver': r, 'inner': bg.inner, 'ordered_pairs': len(bg.relation),
            'direct_link': not any((z, k) in bg.relation and (k, r) in bg.relation for k in bg.nodes),
            'action': on_off(bg, h), 'bd_probe': on_off(bg, b),
            'retarded_action_fixed': retarded_feasibility(bg, h, False),
            'retarded_action_free_future': retarded_feasibility(bg, h, True),
            'matter_record_delta_on_fixed_branch': {'clock': 0, 'dust_weight': 0},
            'physical_checkpoints': {'NOT_RUN': 60}}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
