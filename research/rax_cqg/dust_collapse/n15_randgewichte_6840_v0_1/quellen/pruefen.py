"""Recompute the M=4 pointer-angle certificates from PR 351 using only the standard library."""
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from math import factorial, isqrt
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'basis'))
import coherence
import support
import tube
from affin import phase_box

MASS, ETA, COUPLING = Q(4), Q(1, 100), Q(1, 2)
LIMIT, GRID = Q(1, 50), 10**6


def angle_bound(span):
    """Return an outward upper bound on the relative systematic error, or None."""
    width = span + COUPLING * MASS * ETA
    assert width >= 0
    if width >= 3:  # Every arc used in a positive certificate is shorter than pi.
        return None
    cos_floor = sum((-1)**i * width**(2*i) / factorial(2*i) for i in range(6))
    if cos_floor >= 0:
        return ETA
    if cos_floor <= -1:
        return None
    squared = ETA**2 / (1 - cos_floor**2)
    numerator = squared.numerator * GRID**2
    root = isqrt(numerator // squared.denominator)
    if root**2 * squared.denominator < numerator:
        root += 1
    return Q(root, GRID)


def accepted(error):
    return error is not None and error <= LIMIT and COUPLING * MASS * (1 + error) < 3


def controls():
    # Sharp derivative witness using rational unit phasors and positive weights 3:2.
    cos_theta, sin_theta = Q(-12, 13), Q(5, 13)
    assert cos_theta**2 + sin_theta**2 == 1
    assert Q(9 - 4) / (9 + 4 + 12 * cos_theta) == 1 / sin_theta == Q(13, 5)
    # Finite two-history readout: following removal of lambda*M and normalization,
    # its real and imaginary parts are 13 cos(h) + 12 cos(theta) and 5 sin(h).
    h = COUPLING * MASS * ETA
    target = COUPLING * MASS * LIMIT
    re_lo, re_hi = 13 * (1 - h*h/2) + 12*cos_theta, 13 + 12*cos_theta
    im_lo, im_hi = 5 * (h - h**3/6), 5 * h
    assert re_lo > 0 and im_lo/re_hi > target/(1 - target**2/2)
    assert COUPLING*MASS + im_hi/re_lo < 3
    assert angle_bound(Q(0)) == ETA
    # For constant X the two complex amplitudes share the same factor.
    # This rational phasor pair checks a nontrivial amplitude including an imaginary part.
    a, b = Q(5, 13), Q(12, 13)
    assert a*a + b*b == 1
    real, imag = Q(2, 7), Q(-3, 11)
    times_plus = (a*real-b*imag, b*real+a*imag)
    times_minus = (a*real+b*imag, -b*real+a*imag)
    re = sum(x*y for x, y in zip(times_plus, times_minus))
    im = times_plus[1]*times_minus[0] - times_plus[0]*times_minus[1]
    assert (re, im) == ((a*a-b*b)*(real*real+imag*imag), 2*a*b*(real*real+imag*imag))
    return dict(two_history_weights=[3, 2], cosine=str(cos_theta), sine=str(sin_theta),
                finite_phase_error_above_rad=str(target), finite_error_exceeds_2_percent=True)


def coefficients(order):
    edges = []
    for a, b in sorted(order):
        k = sum((a,j) in order and (j,b) in order for j in range(15))
        if k < 4:
            edges.append((a, b, (1,-9,16,-8)[k]))
    return edges


def direct_checks(code, tile_index, tile, rho, setup, edges, enclosure):
    paths, centers, radius, eta, _, _ = setup
    for case in range(3):
        sign = (-1)**case
        def flip(j):
            return 1 if ((code + tile_index*13 + case*19) >> (j % 7)) & 1 else -1
        # The two endpoints of the proven Delta enclosure also test a larger domain.
        delta = support.DELTA[case % 2]
        offset = (tile[0], sum(tile)/2, tile[1])[case]
        e = offset / delta
        u = {j: c + (0 if case == 1 else radius * flip(i)) for i, (j,c) in enumerate(centers.items())}
        shares = support.fractions_on_paths(paths, u)
        assert sum(shares) == 1 and min(shares) > 0
        y = {j: Q(j-5) for j in support.PAST + support.FUTURE}
        y[3] += e
        w = dict.fromkeys(support.PAST, rho + sign*Q(1,32))
        w.update(dict.fromkeys(support.FUTURE, Q(1,8)))
        for i,(j, share) in enumerate(zip(support.I, shares)):
            y[j] = y[3] + (4-e)*u[j]
            w[j] = MASS * (4*delta-offset) * share * (1 + eta*flip(6-i))
        action = -sum(w.values())/2 - sum(k*w[b]*(y[b]-y[a])**2 for a,b,k in edges)/38
        assert enclosure[0] <= action <= enclosure[1], (code, tile, rho, case)


def record(args):
    code, baseline = args
    _, order = support.geometry(code)
    setup = tube.template(code)
    _, centers, radius, eta, low, high = setup
    assert eta == ETA and (1+ETA)*MASS*(4*support.DELTA[1]+Q(3,32))*max(high) < 1
    assert all(sum((a,b) in order for a in support.I) < 4 for b in support.I)
    edges = coefficients(order)
    profile = {'clock_center':{str(k):str(v) for k,v in centers.items()},
               'clock_halfwidth':str(radius),
               'dwell_affine_ranges_per_vertex':{str(j):[str(a),str(b)] for j,a,b in zip(support.I,low,high)}}
    result = {}
    for rho in (Q(1,8), Q(1,4)):
        old_tiles, joint_tiles = [], []
        for lobe,(a,b) in enumerate(support.WINDOWS):
            for i in range(8):
                step = (b-a)/8
                tile = (a + i*step, a + (i+1)*step)
                old = coherence.phase_box(order, tile, rho, MASS, profile)
                new = phase_box(setup, edges, tile, rho)
                joint = max(old[0], new[0]), min(old[1], new[1])
                assert joint[0] <= joint[1]
                direct_checks(code, lobe*8+i, tile, rho, setup, edges, joint)
                old_tiles.append(old)
                joint_tiles.append(joint)
        def span(boxes):
            return max(r for _,r in boxes) - min(l for l,_ in boxes)
        legacy, joint = span(old_tiles), span(joint_tiles)
        assert 0 <= joint <= legacy
        floor = max(Q(0), 1-legacy**2/8)
        archived = baseline['4;'+str(rho)]
        assert floor == Q(archived['phase_floor'])
        perturb = COUPLING*MASS*ETA/2
        old_error = ETA/(floor-perturb) if floor > perturb else None
        assert accepted(old_error) == (archived['status'] == 'PASS')
        old_angle, new_angle = angle_bound(legacy), angle_bound(joint)
        result[str(rho)] = dict(old=accepted(old_error), angle_old=accepted(old_angle),
                                angle_joint=accepted(new_angle), old_span=str(legacy), joint_span=str(joint),
                                angle_old_relative=str(old_angle) if old_angle is not None else None,
                                angle_joint_relative=str(new_angle) if new_angle is not None else None)
    return str(code), result


def run(jobs):
    data = json.loads((ROOT/'basis/katalog.json').read_text())
    rows = data['evaluation_rows']
    assert len(rows) == 61
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        by_type = dict(pool.map(record, sorted(((int(c),v) for c,v in rows.items()))))
    summary = {}
    for field in ('old','angle_old','angle_joint'):
        passing = [int(c) for c,r in by_type.items() if all(v[field] for v in r.values())]
        summary[field] = dict(both=len(passing), cases=sum(v[field] for r in by_type.values() for v in r.values()),
                              types=passing)
    for c,r in by_type.items():
        assert all(not row['old'] or row['angle_old'] for row in r.values())
        assert all(not row['angle_old'] or row['angle_joint'] for row in r.values())
    assert summary['old']['types'] == sorted(data['full_pass_types'])
    assert summary['old']['both'] == 19
    return dict(mass=str(MASS), per_type=by_type, summary=summary, controls=controls(),
                direct_action_checks=len(rows)*2*16*3, physical_P3='60 x NOT_RUN')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Use Python without -O.')
    parser = argparse.ArgumentParser()
    parser.add_argument('--jobs', type=int, default=2)
    parser.add_argument('--emit', action='store_true', help='emit the full recomputed JSON')
    args = parser.parse_args()
    for manifest in ('pruefplan.sha256','quellen.sha256'):
        for line in (ROOT/manifest).read_text().splitlines():
            expected, path = line.split(maxsplit=1)
            assert sha256((ROOT/path).read_bytes()).hexdigest() == expected, path
    result = run(args.jobs)
    if args.emit:
        print(json.dumps(result,sort_keys=True,indent=2))
    else:
        assert result == json.loads((ROOT/'ergebnis.json').read_text())
        print('PASS', {k:(v['both'],v['cases']) for k,v in result['summary'].items()},
              result['direct_action_checks'], 'direct action checks;', result['physical_P3'])
