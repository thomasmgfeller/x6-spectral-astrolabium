"""Direct interval residual at z, without solving its clock polynomial.

Use successor/past intersections to regrade the incident edges. Use the
pairwise-difference discriminant for every free ancestor.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import json

from kegel import IDEALS, SOURCE, U, V, Z, members, successive
from quelle.intervall import Box, SCALE, box
from uhr import E, SLAB


@lru_cache(maxsize=32768)
def ancestor_roots(inputs):
    # The origin is a point, chosen from the first clock bound.
    # The discriminant is translation invariant, and comes from pair differences.
    origin = Box(inputs[0][1], inputs[0][1]) if inputs else box(0)
    terms = [(weight, Box(lo, hi)) for weight, lo, hi in inputs]
    degree = sum(b for b, _ in terms)
    moment = sum((b * (y - origin) for b, y in terms), box(0))
    if degree == 0:
        constant = 19 + sum((b * (y - origin).square() for b, y in terms), box(0))
        if moment.lo <= 0 <= moment.hi:
            undecided = moment.lo != moment.hi or constant.lo <= 0 <= constant.hi
            return (), undecided
        roots = [origin + constant / (2 * moment)]
    else:
        disc = box(-19 * degree)
        for index, (b, y) in enumerate(terms):
            for c, w in terms[:index]:
                disc -= b * c * (y - w).square()
        if disc.hi < 0:
            return (), False
        root = disc.sqrt_nonnegative_part()
        roots = [origin + (moment - root) / degree, origin + (moment + root) / degree]
    return [(y.lo, y.hi) for y in roots], False


def rows(ideal, key):
    kind, p, f, q, g = key
    nodes = set(members(ideal)) | {U, V, Z}
    edges = {(i, j) for i, j in SOURCE['order'] if j in nodes and i in nodes}
    for new, down, up in [(U, p, f), (V, q, g)]:
        edges.update((i, new) for i in members(down))
        edges.update((new, i) for i in members(up))
    if kind:
        edges.add((U, V))
    edges.update((i, Z) for i in nodes if i != Z)
    past = {j: set() for j in nodes}
    future = {i: set() for i in nodes}
    for i, j in edges:
        past[j].add(i)
        future[i].add(j)
    weights = {j: [] for j in nodes}
    for i, j in sorted(edges):
        size = len(future[i] & past[j])
        if size < 4:
            weights[j].append((i, (1, -9, 16, -8)[size]))
    return past, weights


def audit_cone(ideal, key, target):
    pred, weights = rows(ideal, key)
    fixed = set(SOURCE['past'] + SOURCE['future'])
    states = [{}]
    for j in sorted(pred, key=lambda i: (len(pred[i]), i)):
        following = []
        for state in states:
            # All ancestors of z strictly precede the candidate clock in the band.
            if j == Z:
                residual = 19 + sum((b * (target - Box(*state[i])).square()
                                     for i, b in weights[Z]), box(0))
                if residual.lo <= 0 <= residual.hi:
                    return 'residual_contains_zero'
                continue
            if j in fixed:
                y = E - 2 if j == 3 else box(j - 5)
                candidates = [(y.lo, y.hi)]
            else:
                inputs = tuple((b, *state[i]) for i, b in weights[j])
                candidates, singular = ancestor_roots(inputs)
                if singular:
                    return 'singular'
            for lo, hi in candidates:
                if lo < target.hi and all(hi > state[i][0] for i in pred[j]):
                    following.append({**state, j: (lo, hi)})
        if j == Z:
            return 'residual_excludes_zero'
        states = following
        if not states:
            return 'ancestor_exclusion'
    raise AssertionError('Missing target')


def audit():
    # Y_z = e-2+(4-e)*x. Dependency overestimation is conservative.
    target = E - 2 + (4 - E) * Box.hull(*SLAB)
    count = {kind: Counter() for kind in ('chain', 'incomparable')}
    pending = []
    for ideal in IDEALS:
        future_collar = any(ideal & (1 << j) for j in SOURCE['future'])
        for key in sorted(successive(ideal)):
            name = ('incomparable', 'chain')[key[0]]
            status = 'future_collar' if future_collar else audit_cone(ideal, key, target)
            count[name][status] += 1
            if status in ('singular', 'residual_contains_zero'):
                pending.append([ideal, *key, status])
    return {'counts': {k: dict(v) for k, v in count.items()}, 'undecided': pending,
            'absolute_target': [str(F(x, SCALE)) for x in (target.lo, target.hi)]}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
