"""Exact binary-mark reference for the finite quotient; no physical selection.

Coordinates are INTEGRATED marked-orbit amplitudes. The binary field measure
replaces the continuous one and is not a certified quadrature approximation.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations, product
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / 'inputs'))
import memory as m
import normpath as q

PROB = (F(1, 2), F(1, 2))
TIMES = (F(-1), F(1))
WEIGHTS = (F(0), F(1, 2))
I, T, matmul = q.identity, q.transpose, q.multiply


def permute(state, perm):
    order, colors = state
    return m.relabel(order, perm), tuple(colors[i] for i in perm)


@lru_cache(None)
def canonical(state):
    return min(permute(state, p) for p in permutations(range(len(state[0]))))


@lru_cache(None)
def aut(state):
    return sum(permute(state, p) == state
               for p in permutations(range(len(state[0]))))


@lru_cache(None)
def groups(n):
    out = defaultdict(list)
    for order in m.natural_orders(n):
        for colors in product(range(2), repeat=n):
            state = order, colors
            out[canonical(state)].append(state)
    return dict(sorted(out.items()))


def column(state):
    order, colors = state
    out = defaultdict(F)
    for ideal in m.ideals(order):
        child = order + (ideal,)
        for color in range(2):
            out[canonical((child, colors+(color,)))] += (
                PROB[color] * F(m.extensions(order), m.extensions(child)))
    return dict(out)


def delete_max(state, z):
    order, colors = state
    keep = tuple(i for i in range(len(order)) if i != z)
    m.require(not any(s >> z & 1 for s in order), 'Deletion requires a maximal element')
    return m.relabel(order, keep), tuple(colors[i] for i in keep)


def deletion_row(state):
    """Independent abstract-child route; stabilizers include the marks."""
    order, colors = state
    out = defaultdict(F)
    for z in range(len(order)):
        if not any(s >> z & 1 for s in order):
            parent = delete_max(state, z)
            out[canonical(parent)] += PROB[colors[z]] * F(
                m.extensions(parent[0])*aut(parent),
                m.extensions(order)*aut(state))
    return dict(out)


@lru_cache(None)
def matrix(n):
    parents, children = list(groups(n)), list(groups(n+1))
    columns = [column(groups(n)[p][0]) for p in parents]
    return [[c.get(child, F(0)) for c in columns] for child in children]


def left_inverse(n):
    children = list(groups(n+1))
    out = []
    for reps in groups(n).values():
        p, c = reps[0]
        cone = canonical((p+((1 << n)-1,), c+(0,)))
        out.append([F(s == cone)/PROB[0] for s in children])
    return out


def add(a, b):
    return [[x+y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def scale(a, s):
    return [[s*x for x in row] for row in a]


def complement(b, ell):
    return add(I(len(b)), scale(matmul(b, ell), -1))


def extend(n, old, k=F(1)):
    b, ell = matrix(n), left_inverse(n)
    r = complement(b, ell)
    return add(matmul(matmul(T(ell), old), ell),
               scale(matmul(T(r), r), k))


def mv(a, x):
    return [sum((v*w for v, w in zip(row, x)), F(0)) for row in a]


def inner(x, a, y):
    return sum((u*v for u, v in zip(x, mv(a, y))), F(0))


def solve(a, b):
    rows = [list(row)+[v] for row, v in zip(a, b)]
    n = len(rows)
    for j in range(n):
        pivot = next(i for i in range(j, n) if rows[i][j])
        rows[j], rows[pivot] = rows[pivot], rows[j]
        rows[j] = [x/rows[j][j] for x in rows[j]]
        for i in range(n):
            if i != j and rows[i][j]:
                f = rows[i][j]
                rows[i] = [x-f*y for x, y in zip(rows[i], rows[j])]
    out = [row[-1] for row in rows]
    m.require(mv(a, out) == b, 'Exact linear solve residual')
    return out


def action(state, close=False):
    order, colors = state
    pred = m.with_anchor(order, close)
    times = (F(-2),)+tuple(TIMES[c] for c in colors)+((F(2),) if close else ())
    weights = (F(0),)+tuple(WEIGHTS[c] for c in colors)+((F(0),) if close else ())
    return m.gravity(pred), m.matter(pred, times, weights)


def projector(flags):
    return [[F(i == j and f) for j in range(len(flags))]
            for i, f in enumerate(flags)]


def zero(n):
    return [[F(0)]*n for _ in range(n)]
