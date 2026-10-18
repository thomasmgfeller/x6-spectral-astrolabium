"""Numerical cross-platform replay; the frozen bitwise verifier stays unchanged.

File/source hashes, all integer counts, selections and decisions remain exact.
Only derived floating-point fields use abs(error) <= 1e-10 + 1e-12*abs(reference).
Coordinate byte-hash matches are reported separately, not called bitwise replay.
"""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from core import contract, counts, curvature, seed, sprinkle
from analyze import gate, group_result
from run import frozen
from verify import independent_counts, selftest

ATOL = 1e-10
RTOL = 1e-12


def compare(got, expected, path='root'):
    """Exact structure/discrete values; finite numerical tolerance for floats."""
    if isinstance(expected, dict):
        assert isinstance(got, dict) and got.keys() == expected.keys(), path
        for key in expected:
            compare(got[key], expected[key], path + '.' + key)
    elif isinstance(expected, list):
        assert isinstance(got, list) and len(got) == len(expected), path
        for i, (a, b) in enumerate(zip(got, expected)):
            compare(a, b, f'{path}[{i}]')
    elif isinstance(expected, float):
        assert math.isfinite(got) and math.isfinite(expected), path
        assert abs(got-expected) <= ATOL + RTOL*abs(expected), (path, got, expected)
    else:
        assert type(got) is type(expected) and got == expected, (path, got, expected)


def negative_controls():
    for got, expected in [(1.000001, 1.0), (2, 1), (True, False),
                          ({'status': 'GO'}, {'status': 'NO_GO'}),
                          (float('nan'), 1.0)]:
        try:
            compare(got, expected)
        except AssertionError:
            continue
        raise AssertionError('mutation escaped the portability guard')
    compare(1.0 + 2.84e-14, 1.0)


def replay(folder):
    for name, digest in json.loads((folder/'hashes.json').read_text()).items():
        assert hashlib.sha256((folder/name).read_bytes()).hexdigest() == digest, name
    execution = json.loads((folder/'execution.json').read_text())
    assert frozen(execution['source_ref']) == execution['source_hashes']
    assert execution['status'] == 'COMPLETE'
    c = contract()
    selection = json.loads((folder/'selection.json').read_text())
    recomputed = {}
    checked = independent = coordinate_hash_matches = 0
    max_bd_error = 0.0
    for file in sorted(folder.glob('*.npz')):
        with np.load(file, allow_pickle=False) as a:
            split, ls, hs = file.stem.split('-')
            lam, h = int(ls), float(hs)
            rho = lam/(np.pi/24)
            values = []
            for i in range(len(a['n'])):
                ns = a['interval_counts'][a['offsets'][i]:a['offsets'][i+1]]
                assert len(ns) == a['n'][i] and int(ns.sum()) == a['c2'][i]
                assert hashlib.sha256(ns.tobytes()).hexdigest() == a['interval_hash'][i]
                bd = [curvature(ns, rho, e) for e in c['epsilon_candidates']]
                compare(bd, a['bd'][i].tolist(), file.name + f'/BD/{i}')
                max_bd_error = max(max_bd_error, float(np.max(np.abs(bd-a['bd'][i]))))
                values.append(bd)
                rng = np.random.default_rng(seed(f'{split}/{lam}/{h:.8f}/{i}'))
                x, proposed = sprinkle(rng, rho, h)
                assert len(x) == a['n'][i] and proposed == a['proposed'][i]
                np.testing.assert_array_equal(counts(x), ns)
                coordinate_hash_matches += int(hashlib.sha256(x.tobytes()).hexdigest() == a['coordinate_hash'][i])
                if i % 64 == 0:
                    np.testing.assert_array_equal(independent_counts(x), ns)
                    independent += 1
                checked += 1
            values = np.asarray(values)
            if split == 'development':
                mse = np.mean(values.reshape(-1, c['group_size'], 4).mean(axis=1)**2, axis=0)
                record = next(r for r in selection['development'] if r['file'] == file.name)
                compare(mse.tolist(), record['group_mse'], file.name + '/development')
                assert int(np.argmin(mse)) == selection['selected'][str(lam)]
            else:
                j = selection['selected'][str(lam)]
                recomputed[file.name] = group_result(a['n'], a['c2'], values[:, j], h)
    summary = json.loads((folder/'summary.json').read_text())
    rows = copy.deepcopy(summary['rows'])
    assert len(recomputed) == len(rows) == 12
    for row in rows:
        metrics = recomputed[row['file']]
        compare(metrics, row['metrics'], row['file'] + '/metrics')
        row['metrics'] = metrics
    controls = all(r['poisson_control'] and r['continuum_control'] for r in rows)
    # Reevaluate the decision using recomputed, not archived, floating metrics.
    decision = gate(rows, controls)
    assert decision == summary['decision']
    assert checked == 6528 and independent == 102
    return dict(status='PASS_PORTABLE_NUMERICAL_REPLAY', clouds=checked,
                independent_predicate_clouds=independent,
                coordinate_byte_hash_matches=coordinate_hash_matches,
                coordinate_byte_hash_mismatches=checked-coordinate_hash_matches,
                all_interval_counts_exact=True, all_discrete_metrics_exact=True,
                max_bd_absolute_difference=max_bd_error,
                floating_tolerance={'absolute': ATOL, 'relative': RTOL},
                negative_controls='PASS', decision=decision)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, default=Path(__file__).parent/'results')
    args = parser.parse_args()
    negative_controls()
    result = {'selftest': selftest(), 'archive': replay(args.archive)}
    print(json.dumps(result, indent=2, allow_nan=False))
