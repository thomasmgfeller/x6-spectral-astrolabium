"""Independent identities and full fresh-cloud replay; software verification."""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[key] = '1'
import argparse
import itertools
import json
from pathlib import Path
import tempfile
import numpy as np
from core import (HERE, ROOT, B, P, METHODS, contract, sources, plan, dump, digest,
    seed, geometry, chains, count_check, relation_hash, features, gls, budget, summarize)


def selftest():
    for n in (5, 7, 11):
        x = geometry.flat_points(np.random.default_rng(771+n), n)
        x = x[np.argsort(x[:, 0])]
        c = geometry.relation(x)
        brute = np.array([sum(all(c[a, b] for a, b in zip(v, v[1:]))
                             for v in itertools.combinations(range(n), k)) for k in (2, 3, 4)])
        np.testing.assert_array_equal(brute, count_check(c))
        np.testing.assert_array_equal(brute, chains.chain_sums(c))
        np.testing.assert_array_equal(c, geometry.flat_density_twin_relation(x, 0))
    cov = np.array([[2., .4, .2], [.4, 3., .1], [.2, .1, 4.]])
    for size in (1, 2, 3):
        w = gls(cov, size)
        np.testing.assert_allclose(w@B, 1, atol=1e-14)
        # Independent KKT constrained minimization, including Lagrange multiplier.
        block = np.block([[cov[:size, :size], B[:size, None]],
                          [B[None, :size], np.zeros((1, 1))]])
        kkt = np.linalg.lstsq(block, np.r_[np.zeros(size), 1.], rcond=None)[0]
        np.testing.assert_allclose(w[:size], kkt[:size], rtol=1e-11)
    for bad in (np.zeros((3, 3)), np.eye(2), np.full((3, 3), np.nan)):
        try:
            gls(bad, 3)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid covariance accepted')
    for radius in (0, -1, float('nan')):
        try:
            budget(1., radius)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid precision radius accepted')
    np.testing.assert_allclose([float(chains.de_sitter_slope(k)) for k in (2, 3, 4)], B)
    np.testing.assert_allclose([chains.flat_probability(4, k) for k in (2, 3, 4)], P)
    print('PASS_OFF_GRID_IDENTITIES_AND_REJECTIONS', flush=True)


def close(a, b):
    if isinstance(a, dict):
        assert a.keys() == b.keys()
        for k in a:
            close(a[k], b[k])
    elif isinstance(a, list):
        assert len(a) == len(b)
        for x, y in zip(a, b):
            close(x, y)
    elif isinstance(a, float):
        np.testing.assert_allclose(a, b, rtol=2e-10, atol=2e-10)
    else:
        assert a == b


def verify(out, replay=True):
    execution = json.loads((out/'execution.json').read_text())
    assert sources(execution['source_ref']) == execution['source_sha256']
    hashes = json.loads((out/'hashes.json').read_text())
    assert sorted(p.name for p in out.iterdir()) == sorted([*hashes, 'hashes.json'])
    for name, expected in hashes.items():
        assert digest(out/name) == expected, name
    p = plan()
    close(p, json.loads((out/'planning.json').read_text()))
    # Independent constrained solves on published pilot for every weight.
    pilot = np.load(ROOT/'research/lorentz_rss_fixed_n/results/raw.npz')['direct_counts']
    for n, index in ((64, 0), (128, 4)):
        cov = np.cov(features(pilot[index], n), rowvar=False, ddof=1)
        for size, name in enumerate(METHODS, 1):
            block = np.block([[cov[:size, :size], B[:size, None]],
                              [B[None, :size], np.zeros((1, 1))]])
            alt = np.linalg.lstsq(block, np.r_[np.zeros(size), 1.], rcond=None)[0][:size]
            np.testing.assert_allclose(alt, p['weights'][str(n)][name][:size], rtol=1e-9)
    clouds = 0
    if p['fresh_run_budget_gate']:
        all_counts = []
        for j, h in enumerate(contract()['h_grid']):
            raw = np.load(out/f'cell-{j}.npz', allow_pickle=False)
            counts = raw['counts']
            assert counts.shape == (contract()['fresh_clouds_per_cell'], 3)
            assert np.issubdtype(counts.dtype, np.integer) and np.all(counts >= 0)
            if replay:
                for r, stored in enumerate(counts):
                    rng = np.random.Generator(np.random.PCG64(seed(f'holdout/n128/h{j}/r{r}')))
                    x, _ = geometry.sample(rng, 128, {'h': h})
                    c = geometry.flat_density_twin_relation(x, h)
                    assert relation_hash(c).encode() == raw['relation_sha256'][r]
                    np.testing.assert_array_equal(count_check(c), stored)
                    clouds += 1
                print(f'replayed h={h}: {len(counts)} clouds', flush=True)
            all_counts.append(counts)
        summary = summarize(all_counts, p)
        close(summary, json.loads((out/'summary.json').read_text()))
        # Recompute mean and sample variance with scalar sums, not covariance projection.
        for row in summary['rows']:
            j = contract()['h_grid'].index(row['h'])
            w = p['weights']['128'][row['method']]
            vals = [sum(float(a)*b for a, b in zip(y, w)) for y in features(all_counts[j], 128)]
            mean = sum(vals)/len(vals)
            var = sum((v-mean)**2 for v in vals)/(len(vals)-1)
            np.testing.assert_allclose([mean-row['q'], var**.5], [row['bias'], row['sd']], atol=2e-10)
    else:
        assert json.loads((out/'summary.json').read_text())['status'] == 'BUDGET_GATE_FAILED_NO_FRESH_RUN'
    result = dict(status='PASS_FULL_INFORMATION_REPLAY' if replay else 'PASS_ARCHIVE_AND_ANALYSIS',
                  fresh_clouds_replayed=clouds, source_ref=execution['source_ref'],
                  independent_checks=['KKT weights', 'middle-vertex/edge chain counts',
                                      'square-root causal predicate', 'scalar moments'],
                  external_replication=False)
    print(json.dumps(result), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--selftest', action='store_true')
    parser.add_argument('--input', type=Path)
    parser.add_argument('--archive-only', action='store_true')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    selftest()
    if not args.selftest:
        result = verify(args.input or HERE/'results', replay=not args.archive_only)
        if args.report:
            dump(args.report, result)
