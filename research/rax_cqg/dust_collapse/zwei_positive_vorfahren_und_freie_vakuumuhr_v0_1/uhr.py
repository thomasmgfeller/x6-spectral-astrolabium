"""Outward clock enclosures for necessary density stationarity in a causal past."""
from fractions import Fraction as F
from functools import lru_cache

from kegel import SOURCE, Z, members
from quelle.intervall import Box, SCALE, box

COEFF = (1, -9, 16, -8)
FIXED = set(SOURCE['past'] + SOURCE['future'])
E = Box.hull(F(1, 6) - F(1, 2**22), F(1, 6) + F(1, 2**22))
SLAB = (F(999, 2000), F(1001, 2000))


def endpoints(interval):
    return interval.lo, interval.hi


@lru_cache(maxsize=32768)
def local_roots(inputs, mode, e_bounds):
    e = Box(*e_bounds)
    origin = box(0) if mode == 'absolute' else e - 2
    values = [(weight, Box(lo, hi)) for weight, lo, hi in inputs]
    degree = sum(b for b, _ in values)
    linear = sum((b * (y - origin) for b, y in values), box(0))
    constant = 19 + sum((b * (y - origin).square() for b, y in values), box(0))
    if degree:
        disc = linear.square() - degree * constant
        if disc.hi < 0:
            return (), False
        radical = disc.sqrt_nonnegative_part()
        roots = [origin + (linear + sign * radical) / degree for sign in (-1, 1)]
    elif linear.lo > 0 or linear.hi < 0:
        roots = [origin + constant / (2 * linear)]
    else:
        impossible = linear.lo == linear.hi == 0 and not constant.lo <= 0 <= constant.hi
        return (), not impossible
    return tuple(endpoints(y) for y in roots), False


def solve(pred, mode, e=E):
    clocks = [{}]
    singular = False
    for j in sorted(pred, key=lambda i: (pred[i].bit_count(), i)):
        past = list(members(pred[j]))
        if j not in FIXED:
            terms = []
            for i in past:
                interior = sum(bool(pred[k] & (1 << i)) for k in past)
                if interior < len(COEFF):
                    terms.append((i, COEFF[interior]))
        following = []
        for state in clocks:
            if j in FIXED:
                roots = (endpoints(e - 2 if j == 3 else box(j - 5)),)
            else:
                inputs = tuple((b, *state[i]) for i, b in terms)
                roots, undecided = local_roots(inputs, mode, endpoints(e))
                singular |= undecided
            for y in roots:
                if all(y[1] > state[i][0] for i in past):
                    following.append({**state, j: y})
        clocks = following
        if not clocks:
            break
    intervals = [endpoints((Box(*s[Z]) - (e - 2)) / (4 - e)) for s in clocks]
    return sorted(set(intervals)), singular


def intersect(left, right):
    return sorted({(max(a, c), min(b, d)) for a, b in left for c, d in right
                   if max(a, c) <= min(b, d)})


def enclose(pred, modes=('absolute', 'shifted'), e=E):
    result = None
    unresolved = []
    for mode in modes:
        intervals, singular = solve(pred, mode, e)
        if singular:
            unresolved.append(mode)
            continue
        result = intervals if result is None else intersect(result, intervals)
    return result, unresolved
