"""Exact symbolic cross-checks, dependence trap and all-cloud reproduction."""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[key] = '1'
import argparse
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import numpy as np
import sympy as sp
from exact import (coefficients, kernels, monomial, certificate, probability,
                   q_bounds, epsilon, invert, confidence, relative_radius)
from support import (HERE, contract, sources, digest, read, dump, seed,
                     geometry, quadrature, relation_hash)
from analysis import mathematics, planning, analyze_cell


def selftest():
    # Independently derive the ball-overlap integral symbolically.
    a, b, d, s, t, u = sp.symbols('a b d s t u', real=True)
    overlap = (a+b-s)**2*(s*s+2*s*(a+b)-3*(a-b)**2)/(12*s)
    integral = sp.Rational(16, 9)*b**3*(a-b)**3+sp.integrate(4*s*s*overlap, (s, a-b, d))
    independent = sp.expand(integral.subs({a:sp.Rational(1, 2)+t,
        b:sp.Rational(1, 2)-u, d:u-t}))
    stored = sum(sp.Rational(v.numerator, v.denominator)*t**i*u**j
                 for (i, j), v in kernels()[2].items())
    assert sp.expand(independent-stored) == 0
    assert sp.expand(integral-integral.xreplace({a:b, b:a})) == 0
    # Exact monomial integration via SymPy, including high-degree edge cases.
    regions = [(t, 0, -sp.Rational(1, 2), 0),
               (t, sp.Rational(1, 2), 0, sp.Rational(1, 2)),
               (0, t+sp.Rational(1, 2), -sp.Rational(1, 2), 0),
               (t+sp.Rational(1, 2), sp.Rational(1, 2), -sp.Rational(1, 2), 0)]
    for region, (lo, hi, left, right) in enumerate(regions):
        for i, j in ((0, 0), (1, 2), (4, 3), (0, 38), (19, 19), (37, 1)):
            value = sp.integrate(sp.integrate(t**i*u**j, (u, lo, hi)), (t, left, right))
            assert Q(int(value.p), int(value.q)) == monomial(i, j, region)
    assert list(coefficients()[0][:4]) == [Q(1, 10), Q(14, 75), Q(79, 315), Q(218, 735)]
    cert = certificate()
    assert cert['monotone_numerator_lower'] > Q(1, 20)
    assert cert['probability_enclosure_width_upper'] < Q(1, 10**12)
    h = Q(1, 3)
    lo, hi = probability(h)
    assert abs(float((lo+hi)/2)-quadrature.pair_probability(float(h), 32)) < 2e-14
    band = invert(lo-Q(1, 10000), hi+Q(1, 10000))
    assert band[0] < h < band[1]
    assert invert(Q(-2), Q(-1)) is None and invert(Q(2), Q(3)) is None
    # Exact counterexample to treating all pairs as independent:
    # Xi iid Bernoulli(1/2), binary pair kernel Xi Xj, E U=1/4.
    n = 128
    correct, naive = epsilon(n, 1), epsilon(2*comb(n, 2), 1)
    covered, bad_covered = Q(0), Q(0)
    for k in range(n+1):
        prob = Q(comb(n, k), 2**n)
        err = abs(Q(k*(k-1), n*(n-1))-Q(1, 4))
        covered += prob*(err <= correct)
        bad_covered += prob*(err <= naive)
    assert covered >= Q(19, 20) and bad_covered < Q(19, 20)
    for args in ((-1, 8, 1), (29, 8, 1), (0, 1, 1), (0, 8, 0), (1.5, 8, 1)):
        try:
            confidence(*args)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid input accepted')
    for value in (Q(-1), Q(3, 4), .2):
        try:
            probability(value)
        except ValueError:
            pass
        else:
            raise AssertionError('unsupported domain/type accepted')
    result = dict(status='PASS_EXACT_CONTROLS', symbolic_geometry_identity=True,
        exact_monomial_checks=24, correct_dependent_kernel_coverage=float(covered),
        invalid_independent_pairs_coverage=float(bad_covered))
    print(result, flush=True)
    return result


def compare(a, b):
    if isinstance(a, dict):
        assert a.keys() == b.keys()
        for k in a:
            compare(a[k], b[k])
    elif isinstance(a, list):
        assert len(a) == len(b)
        for x, y in zip(a, b):
            compare(x, y)
    elif isinstance(a, float):
        np.testing.assert_allclose(a, b, rtol=1e-11, atol=2e-14)
    else:
        assert a == b


def verify(out, replay=True):
    tests = selftest()
    execution = read(out/'execution.json')
    assert sources(execution['source_ref']) == execution['source_sha256']
    hashes = read(out/'hashes.json')
    assert sorted(p.name for p in out.iterdir()) == sorted([*hashes, 'hashes.json'])
    for name, expected in hashes.items():
        assert digest(out/name) == expected, name
    math = mathematics()
    compare(math, read(out/'mathematics.json'))
    assert max(r['quadrature_absolute_discrepancy'] for r in math['probability_grid']) < 2e-14
    design = planning()
    compare(design, read(out/'planning.json'))
    clouds, cells = 0, []
    for j, value in enumerate(contract()['fresh_h']):
        raw = np.load(out/f'raw-{j}.npz', allow_pickle=False)
        counts = raw['c2']
        assert counts.shape == (contract()['fresh_clouds_per_h'],)
        assert np.issubdtype(counts.dtype, np.integer)
        if replay:
            for r, count in enumerate(counts):
                rng = np.random.Generator(np.random.PCG64(seed(f'holdout/h{j}/r{r}')))
                x, _ = geometry.sample(rng, 128, {'h': float(Q(value))})
                c = geometry.flat_density_twin_relation(x, float(Q(value)))
                assert relation_hash(c).encode() == raw['relation_sha256'][r]
                assert np.count_nonzero(c) == count
                clouds += 1
            print(f'replayed h={value}: {len(counts)} clouds', flush=True)
        result = analyze_cell(counts, Q(value))
        compare(result, read(out/f'groups-{j}.json.gz'))
        # Independent acceptance check: h interval contains truth whenever the
        # complete certified p enclosure is inside the exact observed band.
        pl, pu = probability(Q(value))
        for group in result['groups']:
            m = group['group_size']
            observed = Q(group['total_c2'], m*comb(128, 2))
            e = epsilon(128, m)
            if observed-e <= pl and pu <= observed+e:
                assert group['contains_true_h']
        cells.extend(result['rows'])
    return dict(status='PASS_FULL_C2_CONFIDENCE_REPLAY' if replay else 'PASS_ARCHIVE_AND_ANALYSIS',
        source_ref=execution['source_ref'], fresh_clouds_replayed=clouds,
        exact_controls=tests, cells=cells, external_replication=False,
        coverage_scope='Finite-sample theorem for known uniform model and each fixed budget; not sequential')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--selftest', action='store_true')
    p.add_argument('--input', type=Path, default=HERE/'results')
    p.add_argument('--archive-only', action='store_true')
    p.add_argument('--report', type=Path)
    args = p.parse_args()
    if args.selftest:
        selftest()
    else:
        result = verify(args.input, replay=not args.archive_only)
        if args.report:
            dump(args.report, result)
        print(result['status'], flush=True)
