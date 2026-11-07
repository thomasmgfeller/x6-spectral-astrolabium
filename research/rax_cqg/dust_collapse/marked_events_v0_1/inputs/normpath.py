"""Auxiliary norms and an unmarked coherent quotient; no physical selection."""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / 'inputs'))
import memory as m


def relation_count(order):
    return sum(s.bit_count() for s in order)


def link_count(order):
    return sum(k == 0 for _, _, k in m.intervals(order))


def mu(order, p):
    n = len(order)
    return p ** link_count(order) * (1-p) ** (n*(n-1)//2-relation_count(order))


def metric(order, p):
    return m.extensions(order)**2 * mu(order, p)


def transition(order, ideal, p):
    maxima = sum(not any(ideal >> j & 1 and order[j] >> i & 1
                        for j in range(len(order))) for i in m.bits(ideal))
    return p**maxima * (1-p)**(len(order)-ideal.bit_count())


def edge_distribution(n, probabilities):
    """Independent route: every natural DAG, then Warshall transitive closure."""
    pairs = [(i,j) for j in range(n) for i in range(j)]
    distributions = [defaultdict(F) for _ in probabilities]
    weights = [[p**k*(1-p)**(len(pairs)-k) for k in range(len(pairs)+1)]
               for p in probabilities]
    for mask in range(1 << len(pairs)):
        matrix = [[False]*n for _ in range(n)]
        for bit, (i,j) in enumerate(pairs):
            matrix[i][j] = bool(mask >> bit & 1)
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    matrix[i][j] = matrix[i][j] or (matrix[i][k] and matrix[k][j])
        order = tuple(sum(1 << i for i in range(n) if matrix[i][j]) for j in range(n))
        for dist, weight in zip(distributions, weights):
            dist[order] += weight[mask.bit_count()]
    return distributions


@lru_cache(None)
def canonical(order):
    return min(m.relabel(order, perm) for perm in permutations(range(len(order))))


@lru_cache(None)
def groups(n):
    result = defaultdict(list)
    for order in m.natural_orders(n):
        result[canonical(order)].append(order)
    return dict(sorted(result.items()))


def aut_count(order):
    return sum(m.relabel(order, perm) == order for perm in permutations(range(len(order))))


def column(order):
    result = defaultdict(F)
    for ideal in m.ideals(order):
        child = order + (ideal,)
        result[canonical(child)] += F(m.extensions(order), m.extensions(child))
    return dict(result)


def quotient_matrix(n):
    parents, children = list(groups(n)), list(groups(n+1))
    columns = [column(groups(n)[parent][0]) for parent in parents]
    return [[col.get(child, F(0)) for col in columns] for child in children]


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def multiply(a, b):
    bt = transpose(b)
    return [[sum((x*y for x,y in zip(row,col) if x and y), F(0)) for col in bt] for row in a]


def left_inverse(n):
    """Select the child obtained by adding a unique greatest element."""
    parents, children = list(groups(n)), list(groups(n+1))
    rows = []
    for parent in parents:
        rep = groups(n)[parent][0]
        cone = canonical(rep + ((1 << n)-1,))
        rows.append([F(child == cone) for child in children])
    return rows


def extend_metric(n, old, complement_weight=F(1)):
    b, ell = quotient_matrix(n), left_inverse(n)
    b_ell = multiply(b, ell)
    residual = [[F(i == j)-x for j,x in enumerate(row)] for i,row in enumerate(b_ell)]
    inherited = multiply(multiply(transpose(ell), old), ell)
    extra = multiply(transpose(residual), residual)
    return [[x+complement_weight*y for x,y in zip(rx,ry)] for rx,ry in zip(inherited,extra)]


def ldl_pivots(a):
    """Exact positive-definiteness certificate for a rational symmetric matrix."""
    n = len(a)
    lower = identity(n)
    diag = []
    for j in range(n):
        pivot = a[j][j]-sum((lower[j][k]**2*diag[k] for k in range(j)), F(0))
        if pivot <= 0:
            raise RuntimeError('Nonpositive LDL pivot')
        diag.append(pivot)
        for i in range(j+1,n):
            lower[i][j] = (a[i][j]-sum((lower[i][k]*lower[j][k]*diag[k]
                                       for k in range(j)), F(0)))/pivot
    reconstructed = multiply(multiply(lower, [[diag[i] if i == j else F(0)
                                              for j in range(n)] for i in range(n)]), transpose(lower))
    if reconstructed != a:
        raise RuntimeError('LDL reconstruction')
    return diag
