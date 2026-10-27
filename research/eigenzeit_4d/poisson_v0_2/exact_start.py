#!/usr/bin/env python3
"""Exact 3+1 Minkowski landmark preflight, standard library only.

This is an algebraic diagnostic with exact interval input, not a reconstruction
from a finite Poisson observation. Run: python3 verify_4d.py > results.json
Original X6 research support code, 2026-10-27. SPDX-License-Identifier: Apache-2.0
"""
from fractions import Fraction as F
from itertools import permutations
import json
import platform
import sys


def point(*xs):
    return tuple(F(x) for x in xs)


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def interval(a, b):
    d = sub(a, b)
    return -d[0]**2 + sum(v*v for v in d[1:])


def matvec(a, v):
    return [sum(x*y for x, y in zip(row, v)) for row in a]


def quadratic(a, v):
    return sum(x*y for x, y in zip(v, matvec(a, v)))


def determinant(a):
    a = [list(row) for row in a]
    ans = F(1)
    for k in range(len(a)):
        j = next((j for j in range(k, len(a)) if a[j][k]), None)
        if j is None:
            return F(0)
        if j != k:
            a[k], a[j] = a[j], a[k]
            ans = -ans
        pivot = a[k][k]
        ans *= pivot
        for j in range(k+1, len(a)):
            factor = a[j][k]/pivot
            a[j] = [x-factor*y for x, y in zip(a[j], a[k])]
    return ans


def solve(a, b):
    a = [list(row)+[rhs] for row, rhs in zip(a, b)]
    n = len(a)
    for k in range(n):
        j = next((j for j in range(k, n) if a[j][k]), None)
        if j is None:
            raise ValueError('singular landmark Gram matrix')
        a[k], a[j] = a[j], a[k]
        pivot = a[k][k]
        a[k] = [v/pivot for v in a[k]]
        for j in range(n):
            if j != k:
                factor = a[j][k]
                a[j] = [x-factor*y for x, y in zip(a[j], a[k])]
    return [row[-1] for row in a]


def gram(s):
    """Only a signed interval matrix enters the reconstruction."""
    n = len(s)
    return [[(s[0][i]+s[0][j]-s[i][j])/2
             for j in range(1, n)] for i in range(1, n)]


def chart(s, target_intervals):
    g = gram(s)
    b = [(s[0][i]+target_intervals[0]-target_intervals[i])/2
         for i in range(1, len(s))]
    c = solve(g, b)
    residual = target_intervals[0]-quadratic(g, c)
    return c, residual


def matrix(points):
    return [[interval(a, b) for b in points] for a in points]


def order(points):
    return [[a[0] < b[0] and interval(a, b) < 0 for b in points]
            for a in points]


def transform(p):
    """Proper orthochronous rational boost in x, then translation."""
    t, x, y, z = p
    return (F(5, 3)*t-F(4, 3)*x+2,
            -F(4, 3)*t+F(5, 3)*x-3, y+F(2, 7), z+5)


def main():
    checks = []

    def check(name, ok):
        if not ok:
            raise AssertionError(name)
        checks.append(name)

    a = [point(-8, 0, 0, 0), point(-6, 1, 0, 0),
         point(-4, 0, 1, 0), point(-2, 0, 0, 0)]
    p = point(1, F(1, 4), F(1, 4), F(1, 4))
    qp = point(2, -F(1, 4), F(1, 4), F(1, 4))
    qm = point(2, -F(1, 4), F(1, 4), -F(1, 4))
    a5 = a+[point(0, 0, 0, 1)]
    check('four_anchor_target_intervals_identical',
          [interval(v, qp) for v in a] == [interval(v, qm) for v in a])
    check('labelled_six_event_orders_identical', order(a+[p, qp]) == order(a+[p, qm]))
    check('plus_support_interval', interval(p, qp) == -F(3, 4))
    check('minus_support_interval', interval(p, qm) == -F(1, 2))
    check('fifth_anchor_distinguishes', interval(a5[-1], qp) != interval(a5[-1], qm))
    check('all_five_anchors_and_targets_timelike',
          all(interval(v, w) < 0 for pts in (a5+[p, qp], a5+[p, qm])
              for i, v in enumerate(pts) for w in pts[i+1:]))
    s = matrix(a5)
    g = gram(s)
    e = [[v[j]-a5[0][j] for v in a5[1:]] for j in range(4)]
    check('affine_frame_invertible', determinant(e) != 0)
    check('gram_determinant_congruence', determinant(g) == -determinant(e)**2)
    # G=E^T eta E and invertible E give inertia (1 negative, 3 positive).
    eta_e = [[-v if i == 0 else v for v in row] for i, row in enumerate(e)]
    congruence = [[sum(e[k][i]*eta_e[k][j] for k in range(4))
                   for j in range(4)] for i in range(4)]
    check('gram_exact_congruence', g == congruence)
    for perm in permutations(range(5)):
        anchors = [a5[i] for i in perm]
        sm = matrix(anchors)
        gm = gram(sm)
        cp, rp = chart(sm, [interval(v, p) for v in anchors])
        check(f'permutation_{perm}_p_residual', rp == 0)
        for tag, q in [('plus', qp), ('minus', qm)]:
            cq, rq = chart(sm, [interval(v, q) for v in anchors])
            check(f'permutation_{perm}_{tag}_residual', rq == 0)
            check(f'permutation_{perm}_{tag}_interval',
                  quadratic(gm, sub(cp, cq)) == interval(p, q))
    for tag, pts in [('plus', a5+[p, qp]), ('minus', a5+[p, qm])]:
        transformed = [transform(v) for v in pts]
        check(f'boost_translation_intervals_{tag}', matrix(pts) == matrix(transformed))
        check(f'boost_translation_order_{tag}', order(pts) == order(transformed))
    flat = a+[point(0, 0, 0, 0)]
    try:
        chart(matrix(flat), [interval(v, p) for v in flat])
    except ValueError:
        check('rank_deficient_negative_control_rejected', True)
    else:
        check('rank_deficient_negative_control_rejected', False)
    collapse = []
    for eps in [F(1), F(1, 2), F(1, 4), F(1, 8), F(0)]:
        moving = a+[point(0, 0, 0, eps)]
        d = determinant(gram(matrix(moving)))
        check(f'collapse_{eps}', d == -36*eps**2)
        collapse.append({'epsilon': str(eps), 'det_G': str(d)})
    result = {
        'schema_version': '1.0', 'status': 'PASS_EXACT_ALGEBRA_ONLY',
        'date': '2026-10-27', 'dimension': '3+1', 'units': 'c=1',
        'arithmetic': 'fractions.Fraction; exact rational',
        'python': platform.python_version(), 'checks_passed': len(checks),
        'landmark_permutations': 120,
        'four_anchors': [[str(x) for x in v] for v in a],
        'fifth_anchor': [str(x) for x in a5[-1]],
        'p': [str(x) for x in p], 'q_plus': [str(x) for x in qp],
        'q_minus': [str(x) for x in qm],
        'tau_squared_plus': '3/4', 'tau_squared_minus': '1/2',
        'four_anchor_q_intervals': [str(interval(v, qp)) for v in a],
        'fifth_anchor_q_plus': str(interval(a5[-1], qp)),
        'fifth_anchor_q_minus': str(interval(a5[-1], qm)),
        'gram': [[str(x) for x in row] for row in g],
        'det_E': str(determinant(e)), 'det_G': str(determinant(g)),
        'gram_inertia': {'negative': 1, 'positive': 3, 'zero': 0},
        'collapse_diagnostic': collapse,
        'limits': ['Exact interval input; no Poisson reconstruction run.',
                   'No equality of joint count laws asserted.',
                   'No operator accuracy, curvature or global stability claim.',
                   'No external independent replication.'],
        'checks': checks,
    }
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == '__main__':
    main()
