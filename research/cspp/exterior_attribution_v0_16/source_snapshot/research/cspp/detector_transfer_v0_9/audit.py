"""Independent analytic controls for signed integration and stochastic transfer."""
from fractions import Fraction
from itertools import product

import numpy as np
from flint import arb, acb, ctx
from support import check, geometry, propagation, pack, load, HERE
from detector import IntegerGeometry, CoefficientRanges, integrate, sample_moments
runner = load('v09_transfer_run', HERE / 'run.py')
adjoint = runner.adjoint


def fraction(z):
    return arb(z.numerator) / z.denominator


def compute():
    ctx.prec = 192
    checks = []
    # A single event at the detector centre: the future-cone volume inside
    # radius1/2, averaged on [0,1/4], is exactly 1/32 of the detector volume.
    x = np.array([[0., 0., 0., 1.5]])
    geo = IntegerGeometry(x, np.array([[-1]], dtype=np.int32))
    for sign in [1, -3]:
        q, meta = integrate(geo, [arb(sign), arb(0)], ['0', '1/4'], 256)
        check(q[0].contains(arb(sign) / 32), 'analytic future-cone volume with signed coefficient')
    checks.append('signed analytic cone-volume integral')
    # All points in the detector lie in this event's future: the exact-volume
    # control variate must integrate a constant without sphere-cell bias.
    x = np.array([[-1., 0., 0., 1.5]])
    geo = IntegerGeometry(x, np.array([[-1]], dtype=np.int32))
    q, meta = integrate(geo, [arb(3) / 7, arb(0)], ['3/4', '1'], 256)
    check(q[0].contains(arb(3) / 7) and q[0].rad() < arb('1e-40'), 'exact constant over curved detector boundary')
    checks.append('constant field exact-volume control variate')
    # Exact null and one-ULP timelike/spacelike points.
    x = np.array([[0., 0., 0., 0.]])
    geo = IntegerGeometry(x, np.array([[-1]], dtype=np.int32))
    points = [[1., 1., 0., 0.], [1., np.nextafter(1., 0.), 0., 0.],
              [1., np.nextafter(1., 2.), 0., 0.], [-1., 0., 0., 0.]]
    for point, expected in zip(points, [False, True, False, False]):
        check(bool(geo.point_past(point)) == expected, 'integer near-null predicate')
        check(geometry.relation(x[0], point)[0] == expected, 'predecessor near-null predicate')
    checks.append('exact near-null and endpoint predicates')
    for e in ['1', '1/16']:
        table = propagation.coefficient_table(24, 512, e, 1)
        ranges = CoefficientRanges(table)
        for lo in range(25):
            for hi in range(lo, 25):
                envelope = ranges.get(lo, hi)
                check(all(envelope.contains(v) for v in table[lo:hi + 1]), 'all signed weight extrema included')
    checks.append('nonmonotone signed weight range inventory')
    means, cov = sample_moments([[acb(-1), acb(1)], [acb(1), acb(-1)]])
    check(all(z.contains(0) for z in means), 'exact sample means')
    check(cov[0][0].contains(2) and cov[0][1].contains(-2), 'negative cross-covariance retained')
    checks.append('negative paired covariance and unbiased divisor')
    # Nilpotent exact resolvent, four equiprobable realizations, no RNG.
    sigma = Fraction(1, 4)
    outcomes = []
    for u, v in product([-1, 1], repeat=2):
        a, b = Fraction(1, 2) + sigma * u, Fraction(1, 2) + sigma * v
        result = a * b
        edges = [[], [(0, fraction(a))], [(1, fraction(b))]]
        t = adjoint([arb(0), arb(0), arb(1)], edges, 1)
        check(t[0].contains(fraction(result)), 'adjoint equals rational exact resolvent')
        outcomes.append(result)
    mean = sum(outcomes) / 4
    variance = sum((a - mean) ** 2 for a in outcomes) / 4
    first_order = 2 * Fraction(1, 4) * sigma ** 2
    check(mean == Fraction(1, 4) and variance == Fraction(9, 256), 'analytic exact stochastic transfer')
    check(variance - first_order == sigma ** 4, 'first-order covariance remainder detected')
    correlated_mean = sum((Fraction(1, 2) + sigma * u) ** 2 for u in [-1, 1]) / 2
    check(correlated_mean - Fraction(1, 4) == sigma ** 2, 'average inverse differs from inverse mean')
    checks.append('exact stochastic resolvent, covariance remainder and mean shift')
    toy = np.array([[-2., 0., 0., 0.], [-.5, 0., 0., .25], [.5, 0., 0., .5]])
    counts, _, _, _, _ = geometry.inventory(toy, np.empty((0, 4)))
    values, history, edges, table, scales, errors = runner.forward(toy, counts, arb(1))
    check(len(values) == 3 and len(values[0]) == 14 and len(errors) == 5, 'complete synthetic adapter inventory')
    q, _ = integrate(IntegerGeometry(toy, counts), table, ['3/4', '1'], 32)
    z, weights = runner.evaluate(q, values, history, edges)
    check(len(z) == 9 and len(weights) == 1 and all(v.is_finite() for v in z), 'synthetic end-to-end detector')
    checks.append('synthetic full adapter/solve/integral/adjoint pipeline')
    return {'status': 'PASS', 'checks': checks,
            'finite_ensemble_control': {'exact_population_mean': str(mean),
                'exact_population_variance': str(variance), 'first_order_variance': str(first_order),
                'covariance_remainder': str(sigma ** 4), 'correlated_mean_shift': str(sigma ** 2)},
            'scope': 'analytic method controls, not causal-set population confirmation or quantum-gravity evidence'}


if __name__ == '__main__':
    import json
    print(json.dumps(compute(), indent=2))
