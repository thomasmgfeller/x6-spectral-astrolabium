"""Independent high-precision checks and full fresh-cloud replay."""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[key] = '1'
import argparse
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import mpmath as mp
import numpy as np
from core import (reference, log_bounds, kl_bounds, geometric_probability,
                  confidence, design_interval, THRESHOLD)
from support import contract, sources, digest, read, dump, seed, geometry, relation_hash, HERE
from analysis import planning, analyze


def selftest():
    mp.mp.dps = 90
    real = lambda q: mp.mpf(q.numerator)/q.denominator
    for x in (Q(1, 2**30), Q(1, 7), Q(1, 3), Q(1023, 1024), Q(1), Q(2), Q(31, 3), Q(2**20)):
        lo, hi = log_bounds(x)
        actual = mp.log(real(x))
        assert real(lo) <= actual <= real(hi)
        assert hi-lo < Q(1, 10**20)
    for u in (Q(0), Q(1, 13), Q(1, 3), Q(4, 7), Q(1)):
        for p in (Q(1, 7), Q(2, 7), Q(1, 2)):
            lo, hi = kl_bounds(u, p)
            actual = sum(real(w)*mp.log(real(w/v)) for w, v in ((u,p),(1-u,1-p)) if w)
            assert real(lo) <= actual <= real(hi)
            assert hi >= 2*(u-p)**2
    # Exact finite Bernoulli-kernel control: Xi Xj, p=1/4, N=64.
    # Classification uses rational lower/upper KL bounds; probability sums exact.
    n = 64
    coverages = []
    for effective in (n//2, comb(n, 2)):
        covered = Q(0)
        for k in range(n+1):
            u = Q(k*(k-1), n*(n-1))
            lo, hi = kl_bounds(u, Q(1, 4))
            assert hi <= THRESHOLD/effective or lo > THRESHOLD/effective
            if hi <= THRESHOLD/effective:
                covered += Q(comb(n, k), 2**n)
        coverages.append(covered)
    assert coverages[0] >= Q(19, 20) and coverages[1] < Q(19, 20)
    # Multiple independent clouds, exact count convolution, N=8 and M=3.
    frequencies = {0:1}
    for _ in range(3):
        nxt = {}
        for total, frequency in frequencies.items():
            for k in range(9):
                count = total+comb(k, 2)
                nxt[count] = nxt.get(count, 0)+frequency*comb(8, k)
        frequencies = nxt
    multi_coverage = Q(0)
    for count, frequency in frequencies.items():
        lo, hi = kl_bounds(Q(count, 3*comb(8, 2)), Q(1, 4))
        assert hi <= THRESHOLD/12 or lo > THRESHOLD/12
        if hi <= THRESHOLD/12:
            multi_coverage += Q(frequency, 2**24)
    assert multi_coverage >= Q(19, 20)
    h, n, m = Q(1, 3), 96, 54321
    pl, pu = geometric_probability(h)
    total = int((pl+pu)/2*m*comb(n, 2))
    new, old = confidence(total, n, m), reference.confidence(total, n, m)
    assert old[0] <= new[0] <= h <= new[1] <= old[1]
    assert confidence(0, 8, 100000) is None
    assert confidence(2800000, 8, 100000) is None
    for args in ((-1,8,1),(29,8,1),(0,1,1),(0,8,0),(1.5,8,1)):
        try:
            confidence(*args)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid input accepted')
    for value in (Q(0), Q(-1), .1):
        try:
            log_bounds(value)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid logarithm accepted')
    result = dict(status='PASS_KL_CONTROLS', independent_log_checks=8, independent_kl_checks=15,
        correct_dependent_kernel_coverage=float(coverages[0]), invalid_pair_independence_coverage=float(coverages[1]),
        exact_three_cloud_coverage=float(multi_coverage), interval_nesting=True)
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
        np.testing.assert_allclose(a, b, rtol=1e-12, atol=1e-14)
    else:
        assert a == b


def verify(out, replay=True):
    controls = selftest()
    execution = read(out/'execution.json')
    assert sources(execution['source_ref']) == execution['source_sha256']
    hashes = read(out/'hashes.json')
    assert sorted(p.name for p in out.iterdir()) == sorted([*hashes, 'hashes.json'])
    for name, expected in hashes.items():
        assert digest(out/name) == expected, name
    design = planning()
    compare(design, read(out/'planning.json'))
    rows, clouds = [], 0
    if design['fresh_run_gate']:
        for j, cell in enumerate(contract()['fresh_cells']):
            all_counts = []
            for begin in range(0, cell['clouds'], contract()['storage_block']):
                raw = np.load(out/f'raw-{j}-{begin}.npz', allow_pickle=False)
                counts = raw['c2']
                assert counts.shape == (min(contract()['storage_block'], cell['clouds']-begin),)
                assert np.issubdtype(counts.dtype, np.integer)
                if replay:
                    for index, count in enumerate(counts):
                        rng = np.random.Generator(np.random.PCG64(seed(f'holdout/h{j}/r{begin+index}')))
                        x, _ = geometry.sample(rng, 128, {'h': float(Q(cell['h']))})
                        c = geometry.flat_density_twin_relation(x, float(Q(cell['h'])))
                        assert relation_hash(c).encode() == raw['relation_sha256'][index]
                        assert np.count_nonzero(c) == count
                        clouds += 1
                all_counts.extend(counts)
            result = analyze(np.array(all_counts, dtype=np.int64), cell)
            compare(result, read(out/f'groups-{j}.json.gz'))
            rows.extend(result['rows'])
            print(f'verified h={cell["h"]}: {cell["clouds"]} clouds', flush=True)
    summary = read(out/'summary.json')
    compare(rows, summary['rows'])
    assert summary['primary_status'] == design['primary_status']
    assert summary['fresh_clouds'] == (sum(c['clouds'] for c in contract()['fresh_cells']) if design['fresh_run_gate'] else 0)
    return dict(status='PASS_FULL_KL_REPLAY' if replay else 'PASS_ARCHIVE_AND_ANALYSIS',
        source_ref=execution['source_ref'], fresh_clouds_replayed=clouds, exact_controls=controls,
        primary_status=design['primary_status'], external_replication=False,
        claim='Analytical fixed-budget model-conditional coverage; simulation is an implementation check')


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
        result = verify(args.input, not args.archive_only)
        if args.report:
            dump(args.report, result)
        print(result['status'], flush=True)
