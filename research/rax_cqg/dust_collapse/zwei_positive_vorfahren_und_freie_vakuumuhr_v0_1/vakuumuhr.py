"""Exploratory mixed N17 control on an explicitly specified family of orders."""
from collections import Counter
from fractions import Fraction as F
import json

from kegel import SOURCE
from quelle.intervall import Box, SCALE, box
from uhr import E, SLAB

U, Z = 15, 16
OLD_REL = set(map(tuple, SOURCE['order']))
PAST = SOURCE['past']
FUTURE = SOURCE['future']
INNER = SOURCE['inner']
B = (1, -9, 16, -8)


def encode(a):
    return [str(F(k, SCALE)) for k in (a.lo, a.hi)]


def relation(first, second):
    rel = OLD_REL | {(i, j) for i in [0, 1, 2] for j in (U, Z)} | {(U, Z)}
    rel.update((U, j) for j in FUTURE[first:])
    rel.update((Z, j) for j in FUTURE[second:])
    assert not any((i, i) in rel for i in range(17))
    assert all((i, k) in rel for i, j in rel for h, k in rel if j == h)
    return rel


def weights(rel):
    result = {}
    for i, j in sorted(rel):
        n = sum((i, k) in rel and (k, j) in rel for k in range(17))
        if n < 4:
            result[i, j] = B[n]
    return result


def old_stationary():
    """Construct an existing real ordered branch by quadratic roots and backsolve.

    The archived enclosures choose a sign; they are never used to narrow any
    result. Positive discriminants and strict inequalities certify existence.
    """
    h = weights(OLD_REL)
    y = {j: box(j - 5) for j in PAST + FUTURE}
    y[3] = box(F(1, 6)) - 2
    origin = y[3]
    order = sorted(INNER, key=lambda j: sum(v == j for _, v in OLD_REL))
    for j in order:
        incoming = [(i, b) for (i, v), b in h.items() if v == j]
        degree = sum(b for i, b in incoming)
        moment = sum((b * (y[i] - origin) for i, b in incoming), box(0))
        c = 19 + sum((b * (y[i] - origin).square() for i, b in incoming), box(0))
        if degree:
            disc = moment.square() - degree * c
            assert disc.lo > 0
            radical = disc.sqrt_nonnegative_part()
            roots = [origin + (moment + sign * radical) / degree for sign in (-1, 1)]
        else:
            assert not moment.lo <= 0 <= moment.hi
            roots = [origin + c / (2 * moment)]
        saved = Box.hull(*map(F, SOURCE['clock_midpoint'][str(j)]))
        chosen = [root for root in roots if root.intersection(saved) is not None]
        assert len(chosen) == 1
        y[j] = chosen[0]
    assert all(y[i].hi < y[j].lo for i, j in OLD_REL)
    w = {**{i: box(F(1, 8)) for i in PAST}, **{j: box(F(1, 64)) for j in FUTURE}}
    for j in reversed(order):
        moment = sum((b * (y[j] - y[i]) for (i, v), b in h.items() if v == j), box(0))
        out = sum((b * w[k] * (y[k] - y[j]) for (i, k), b in h.items() if i == j), box(0))
        w[j] = out / moment
        assert 0 < w[j].lo <= w[j].hi < SCALE
        assert w[j].intersection(Box.hull(*map(F, SOURCE['positive_fields_midpoint'][str(j)])))
    return y, w


def current(h, y, w, j):
    incoming = sum((b * (y[j] - y[i]) for (i, k), b in h.items() if k == j), box(0))
    outgoing = sum((b * w[k] * (y[k] - y[j]) for (i, k), b in h.items() if i == j), box(0))
    return outgoing - w[j] * incoming


def action(h, y, w):
    gravity = 38 * (len(w) - sum(h.values()))
    return gravity - 19 * sum(w.values(), box(0)) - sum(
        (b * w[j] * (y[j] - y[i]).square() for (i, j), b in h.items()), box(0))


def exact_control():
    y, w = old_stationary()
    rel = relation(0, 0)
    h = weights(rel)
    old_h = weights(OLD_REL)
    assert {k: b for k, b in h.items() if set(k) & set(INNER)} == {
        k: b for k, b in old_h.items() if set(k) & set(INNER)}
    y[U], y[Z] = -box(6).sqrt_nonnegative_part(), box(0)
    w[U], w[Z] = box(0), (3 - y[U]) / 192
    assert 0 < w[Z].lo and w[Z].hi < SCALE
    assert all(y[i].hi < y[j].lo for i, j in rel)
    step = F(1, 256)
    for j in INNER + [U, Z]:
        grad = current(h, y, w, j)
        assert grad.lo <= 0 <= grad.hi
        # Full action difference in chart at fixed density; equals the clock gradient.
        assert all(y[v].lo - y[i].hi > step * SCALE for i, v in rel if j in (i, v))
        diff = (action(h, {**y, j: y[j] + step}, w) -
                action(h, {**y, j: y[j] - step}, w)) / (4 * step)
        assert diff.lo <= 0 <= diff.hi
        if j != U:
            density = 19 + sum((b * (y[j] - y[i]).square() for (i, k), b in h.items() if k == j), box(0))
            assert density.lo <= 0 <= density.hi
    x = (F(0) - (F(1, 6) - 2)) / (4 - F(1, 6))
    assert x == F(11, 23) < SLAB[0]
    return {'e': '1/6', 'Y_z': '0', 'Y_u': '-sqrt(6)', 'w_z': '(3+sqrt(6))/192',
            'w_u': '0', 'x_z': str(x), 'distance_to_slab': str(SLAB[0] - x),
            'old_free_positive': len(INNER), 'free_clocks_checked': len(INNER) + 2}


def scan():
    control = exact_control()
    t = E - 2 + (4 - E) * Box.hull(*SLAB)
    d = (t.square() + 6 * t + 6).sqrt_nonnegative_part()
    u = t - d
    assert -3 * SCALE < u.lo < u.hi < t.lo < t.hi < 2 * SCALE
    y = {**{i: box(i - 5) for i in PAST + FUTURE}, U: u, Z: t}
    moment = d - t - 3
    counts = Counter()
    rows = []
    for first in range(5):
        for second in range(first, 5):
            h = weights(relation(first, second))
            assert {i: b for (i, j), b in h.items() if j == Z} == {0: -8, 1: 16, 2: -9, U: 1}
            out = sum((b * (y[j] - t) / 64 for (i, j), b in h.items() if i == Z), box(0))
            w_z = out / moment
            row = {'u_future': FUTURE[first:], 'z_future': FUTURE[second:], 'w_z': encode(w_z)}
            if w_z.hi <= 0 or w_z.lo >= SCALE:
                status = 'outside_open_density_domain'
            elif first == second == 0:
                assert 0 < w_z.lo and w_z.hi < SCALE
                assert [h.get((U, j), 0) for j in FUTURE] == [-9, 16, -8, 0]
                assert [h.get((Z, j), 0) for j in FUTURE] == [1, -9, 16, -8]
                # Exact simplification using d^2=t^2+6t+6.
                g = t * (d + t + 9) / 192
                naive = current(h, y, {**{j: box(F(1, 64)) for j in FUTURE}, U: box(0), Z: w_z}, U)
                assert g.lo > 0 and naive.intersection(g)
                row['G_u'] = encode(g)
                status = 'nonzero_vacuum_clock_gradient'
            else:
                status = 'unresolved'
            counts[status] += 1
            rows.append({**row, 'status': status})
    return {'family': 'old past {0,1,2} for u and z; u<z; only old future collars as successors',
            'post_hoc': True, 'target_density_witness': {'Y_z': '1/12', 'Y_u': '(1-sqrt(937))/12',
            'e': '1/6', 'x_z': '1/2'}, 'counts': dict(counts), 'future_attachments': rows,
            'stationary_off_band_control': control}


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O')
    print(json.dumps(scan(), indent=2, sort_keys=True))
