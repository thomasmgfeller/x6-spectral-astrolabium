"""Exact finite incidence matching; no numerical hashes used as equality tests."""
from collections import Counter, defaultdict
from itertools import combinations
import hashlib
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def token(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


class Stream:
    """Portable counter-based pseudorandom stream, not a physical RNG."""
    def __init__(self, *key):
        self.key = token(['x6-matching-geometry-v1', *key])
        self.counter = 0

    def word(self):
        raw = hashlib.sha256((self.key + ':' + str(self.counter)).encode()).digest()
        self.counter += 1
        return int.from_bytes(raw[:8], 'big')

    def below(self, n):
        limit = (1 << 64) - ((1 << 64) % n)
        while True:
            x = self.word()
            if x < limit:
                return x % n

    def unit(self):
        return ((self.word() >> 12) + 0.5) / (1 << 52)

    def shuffle(self, seq):
        seq = list(seq)
        for i in range(len(seq)-1, 0, -1):
            j = self.below(i+1)
            seq[i], seq[j] = seq[j], seq[i]
        return seq


def binary(b):
    require(len(b) > 0 and len(b[0]) > 0, 'nonempty matrix dimensions')
    require(all(len(row) == len(b[0]) and all(type(x) is int and x in (0, 1)
                for x in row) for row in b), 'binary rectangular matrix')


def encode(b):
    binary(b)
    m, u = len(b), len(b[0])
    cap = max(sum(b[i][j] for i in range(m)) for j in range(u))
    masks = [sum(x << j for j, x in enumerate(row)) for row in b]
    counts = []
    for k in range(cap+1):
        for group in combinations(range(m), k):
            common = (1 << u)-1
            for i in group:
                common &= masks[i]
            counts.append([sum(1 << i for i in group), common.bit_count()])
    return dict(rows=m, columns=u, degree_cap=cap, counts=sorted(counts))


def decode(e):
    m, u, cap = (e[k] for k in ['rows', 'columns', 'degree_cap'])
    require(all(type(x) is int for x in [m, u, cap]) and m > 0 and u > 0
            and 0 <= cap <= m, 'indexed metadata')
    domain = sorted(sum(1 << i for i in s) for k in range(cap+1)
                    for s in combinations(range(m), k))
    require(all(type(s) is int and type(g) is int and 0 <= g <= u
                for s, g in e['counts']), 'indexed count types and bounds')
    require([s for s, g in e['counts']] == domain, 'complete unique subset domain')
    remaining = dict(e['counts'])
    require(remaining[0] == u, 'empty subset count')
    columns = []
    for mask in sorted(domain, key=lambda s: (-s.bit_count(), s)):
        a = remaining[mask]
        require(a >= 0, 'negative multiplicity')
        columns.extend([mask]*a)
        if mask:
            sub = (mask-1) & mask
            while True:
                remaining[sub] -= a
                if not sub:
                    break
                sub = (sub-1) & mask
    require(len(columns) == u, 'column total')
    columns.sort()
    return [[(mask >> i) & 1 for mask in columns] for i in range(m)]


def verify_incidence(a, b, witness):
    p, q = witness['rows'], witness['columns']
    require(sorted(p) == list(range(len(a))) and len(b) == len(a), 'row bijection')
    require(sorted(q) == list(range(len(a[0]))) and len(b[0]) == len(a[0]), 'column bijection')
    require(all(a[i][j] == b[p[i]][q[j]] for i in range(len(a))
                for j in range(len(a[0]))), 'full incidence witness')


def match(a, b, budget=2000000):
    """Complete backtracking with necessary projected-column tests.

    Witnesses map source indices to target indices. There is no canonical form
    or unique-witness claim. Exhausted search is distinct from exhausted budget.
    """
    binary(a)
    binary(b)
    nodes = 0
    if (len(a), len(a[0])) != (len(b), len(b[0])):
        return dict(status='NONISOMORPHIC', nodes=0, witness=None)
    m, u = len(a), len(a[0])
    def gram(x):
        return [[sum(v*w for v, w in zip(r, s)) for s in x] for r in x]
    ga, gb = gram(a), gram(b)
    signatures_a = [(ga[i][i], tuple(sorted(ga[i]))) for i in range(m)]
    signatures_b = [(gb[i][i], tuple(sorted(gb[i]))) for i in range(m)]
    if Counter(signatures_a) != Counter(signatures_b):
        return dict(status='NONISOMORPHIC', nodes=0, witness=None)
    candidates = [[j for j in range(m) if signatures_a[i] == signatures_b[j]] for i in range(m)]
    mapping, used = {}, set()

    class Exhausted(Exception):
        pass

    def visit():
        nonlocal nodes
        nodes += 1
        if nodes > budget:
            raise Exhausted
        if len(mapping) == m:
            return True
        options = []
        for i in range(m):
            if i in mapping:
                continue
            possible = [j for j in candidates[i] if j not in used and
                        all(ga[i][v] == gb[j][w] for v, w in mapping.items())]
            if not possible:
                return False
            options.append((len(possible), i, possible))
        _, i, possible = min(options)
        for j in possible:
            mapping[i] = j
            used.add(j)
            roots = sorted(mapping)
            left = Counter(tuple(a[v][k] for v in roots) for k in range(u))
            right = Counter(tuple(b[mapping[v]][k] for v in roots) for k in range(u))
            if left == right and visit():
                return True
            used.remove(j)
            del mapping[i]
        return False

    try:
        same = visit()
    except Exhausted:
        return dict(status='INCONCLUSIVE', nodes=nodes, witness=None)
    if not same:
        return dict(status='NONISOMORPHIC', nodes=nodes, witness=None)
    p = [mapping[i] for i in range(m)]
    buckets = defaultdict(list)
    for j in range(u):
        buckets[tuple(b[p[i]][j] for i in range(m))].append(j)
    q = [buckets[tuple(a[i][j] for i in range(m))].pop(0) for j in range(u)]
    witness = dict(rows=p, columns=q)
    verify_incidence(a, b, witness)
    return dict(status='ISOMORPHIC', nodes=nodes, witness=witness)


def match_indexed(a, b, budget=2000000):
    return match(decode(a), decode(b), budget)


def closure(c):
    out = [r[:] for r in c]
    for k in range(len(out)):
        for i in range(len(out)):
            if out[i][k]:
                out[i] = [int(x or y) for x, y in zip(out[i], out[k])]
    require(not any(out[i][i] for i in range(len(out))), 'acyclic relation')
    return out


def validate_order(c):
    binary(c)
    require(len(c) == len(c[0]) and closure(c) == c, 'strict transitive order')


def layers(c):
    validate_order(c)
    n = len(c)
    low = [i for i in range(n) if not any(c[j][i] for j in range(n)) and any(c[i])]
    high = [i for i in range(n) if not any(c[i]) and any(c[j][i] for j in range(n))]
    require(len(low)+len(high) == n and all(not c[i][j] or (i in low and j in high)
                for i in range(n) for j in range(n)), 'positive height-two order required')
    return low, high, [[c[i][j] for j in high] for i in low]


def sorted_columns(b):
    return sorted(range(len(b[0])), key=lambda j: sum(b[i][j] << i for i in range(len(b))))


def lift_witness(c, d, witness):
    low, high, a = layers(c)
    ll, hh, b = layers(d)
    ac, bc = sorted_columns(a), sorted_columns(b)
    p = [None]*len(c)
    for i, j in enumerate(witness['rows']):
        p[low[i]] = ll[j]
    for i, j in enumerate(witness['columns']):
        p[high[ac[i]]] = hh[bc[j]]
    verify_relation(c, d, p)
    return p


def verify_relation(c, d, p):
    require(len(c) == len(d) and sorted(p) == list(range(len(c))), 'node bijection')
    require(all(c[i][j] == d[p[i]][p[j]] for i in range(len(c)) for j in range(len(c))),
            'full directed relation witness')


def three_order(b, c):
    binary(b)
    binary(c)
    l, m, u = len(b), len(c), len(c[0])
    require(len(b[0]) == m, 'shared middle size')
    out = [[0]*(l+m+u) for _ in range(l+m+u)]
    for i in range(l):
        for j in range(m):
            out[i][l+j] = b[i][j]
    for j in range(m):
        for k in range(u):
            out[l+j][l+m+k] = c[j][k]
    return closure(out)


def joint_matrix(b, c):
    return [row[:] for row in b] + [[c[j][k] for j in range(len(c))] for k in range(len(c[0]))]


def from_joint(joint, lower):
    b = joint[:lower]
    c = [list(row) for row in zip(*joint[lower:])]
    return three_order(b, c)
