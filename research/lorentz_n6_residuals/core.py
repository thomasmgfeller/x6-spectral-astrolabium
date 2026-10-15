"""Exact finite causal-order observables; Python standard library only.

Independent polynomial method: Faddeev-LeVerrier integer recurrence.
The older atlas verifier uses Bareiss determinants and interpolation instead.
"""
from collections import defaultdict
from itertools import permutations
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def transpose(a):
    return [list(row) for row in zip(*a)]


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def add(a, b, sign=1):
    return [[x+sign*y for x, y in zip(r, s)] for r, s in zip(a, b)]


def polynomial(a):
    n = len(a)
    b = [[int(i == j) for j in range(n)] for i in range(n)]
    coefficients = [1]
    for k in range(1, n+1):
        b = multiply(a, b)
        trace = sum(b[i][i] for i in range(n))
        require(trace % k == 0, 'Nonintegral characteristic coefficient')
        coefficient = -trace // k
        coefficients.append(coefficient)
        for i in range(n):
            b[i][i] += coefficient
    require(all(x == 0 for row in b for x in row), 'Cayley-Hamilton residual')
    return coefficients


def validate_order(c):
    n = len(c)
    require(n > 0 and all(len(row) == n for row in c), 'Square nonempty matrix required')
    require(all(type(x) is int and x in (0, 1) for row in c for x in row), 'Binary integer matrix required')
    require(all(c[i][i] == 0 for i in range(n)), 'Strict relation required')
    require(all(not (c[i][j] and c[j][k]) or c[i][k]
                for i in range(n) for j in range(n) for k in range(n)),
            'Full transitive relation required, not Hasse links')


def degree_pairs(c):
    return [[sum(col), sum(row)] for row, col in zip(c, zip(*c))]


def connected(c):
    seen, todo = {0}, [0]
    while todo:
        i = todo.pop()
        for j in range(len(c)):
            if (c[i][j] or c[j][i]) and j not in seen:
                seen.add(j); todo.append(j)
    return len(seen) == len(c)


def features(c):
    validate_order(c)
    n, ct = len(c), transpose(c)
    s, a = add(c, ct), add(c, ct, -1)
    k = add(multiply(s, a), multiply(a, s), -1)
    d = sorted(degree_pairs(c))
    return {
        'n': n, 'polynomials_S_A_K': [polynomial(x) for x in (s, a, k)],
        'degree_pairs': d,
        'minimal_maximal_isolated': [sum(x == 0 for x, y in d),
                                     sum(y == 0 for x, y in d),
                                     sum(x == y == 0 for x, y in d)],
        'W_future': sum(y*(y-1)//2 for x, y in d),
        'W_past': sum(x*(x-1)//2 for x, y in d),
        'edges': sum(map(sum, c)),
        'height_at_most_two': not any(x for row in multiply(c, c) for x in row),
        'connected': connected(c),
    }


def isomorphic(a, b):
    """Exhaustive bijections, pruned only by the necessary paired degrees."""
    if len(a) != len(b):
        return False
    da, db = degree_pairs(a), degree_pairs(b)
    if sorted(da) != sorted(db):
        return False
    for p in permutations(range(len(a))):
        if all(da[i] == db[p[i]] for i in range(len(a))) and all(
                a[i][j] == b[p[i]][p[j]] for i in range(len(a)) for j in range(len(a))):
            return True
    return False


def f0(f):
    return [f['n'], f['polynomials_S_A_K'], f['minimal_maximal_isolated'][:2]]


def key(value):
    return json.dumps(value, separators=(',', ':'))


def pair_result(ids, matrices, records):
    left, right = ids
    a, b = records[left], records[right]
    return {'ids': ids, 'same_F0': f0(a) == f0(b),
            'same_D': a['degree_pairs'] == b['degree_pairs'],
            'same_W_future': a['W_future'] == b['W_future'],
            'same_W_past': a['W_past'] == b['W_past'],
            'isomorphic': isomorphic(matrices[left], matrices[right]),
            'dual_isomorphic': isomorphic(transpose(matrices[left]), matrices[right])}


def selected(inputs):
    matrices = {r['id']: r['causal_matrix'] for r in inputs['records']}
    require(len(matrices) == len(inputs['records']), 'Duplicate record ID')
    records = {name: features(c) for name, c in matrices.items()}
    pairs = [pair_result(ids, matrices, records) for ids in
             inputs['primary_pairs'] + inputs['scope_pairs']]
    return {'records': records, 'pairs': pairs}


def grouping(records, mode):
    groups = defaultdict(list)
    for name, f in records.items():
        value = f0(f)
        if mode == 'D_only':
            value = f['degree_pairs']
        elif mode == 'F0_D':
            value += [f['degree_pairs']]
        elif mode == 'F0_W_future':
            value += [f['W_future']]
        elif mode == 'F0_W_both':
            value += [f['W_future'], f['W_past']]
        elif mode != 'F0':
            raise ValueError('Unknown grouping')
        groups[key(value)].append(name)
    return {'classes': len(groups),
            'collision_pairs': sum(len(g)*(len(g)-1)//2 for g in groups.values()),
            'collision_groups': sorted(sorted(g) for g in groups.values() if len(g) > 1)}


def block_order(b, isolates=0):
    p, q = len(b), len(b[0])
    n = p+q+isolates
    return [[0]*p + list(row) + [0]*isolates for row in b] + [[0]*n for _ in range(q+isolates)]


def canonical_bipartite(b):
    # Keep (p,q,z) OUTSIDE this canonical word to retain time orientation.
    if len(b[0]) > len(b):
        b = transpose(b)
    return min(tuple(sorted(tuple(row[j] for j in perm) for row in b))
               for perm in permutations(range(len(b[0]))))


def height_two_seven():
    """Complete height <= 2 enumeration on seven vertices, including isolates."""
    records = {'n7-antichain': features([[0]*7 for _ in range(7)])}
    matrices, strata = {}, []
    for p in range(1, 7):
        for q in range(1, 8-p):
            z, representatives, valid = 7-p-q, {}, 0
            for word in range(1 << (p*q)):
                b = [[(word >> (p*q-1-i*q-j)) & 1 for j in range(q)] for i in range(p)]
                if not all(map(any, b)) or not all(map(any, zip(*b))):
                    continue
                valid += 1
                representatives.setdefault(canonical_bipartite(b), b)
            strata.append([p, q, z, valid, len(representatives)])
            for i, canon in enumerate(sorted(representatives)):
                name = f'n7-h2-{p}-{q}-{z}-{i:03}'
                c = block_order(representatives[canon], z)
                matrices[name] = c
                records[name] = features(c)
    groups = {mode: grouping(records, mode) for mode in ('F0', 'F0_W_future', 'F0_W_both', 'F0_D')}
    collisions = {name: matrices[name] for g in groups['F0_W_future']['collision_groups'] for name in g}
    return {'orders': len(records), 'strata_p_q_isolates_valid_classes': strata,
            'groups': groups, 'future_collision_matrices': collisions}
