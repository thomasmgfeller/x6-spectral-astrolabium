"""SPDX-License-Identifier: Apache-2.0
One frozen decision from archived per-cloud observations.
"""
import gzip
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
import scipy
from bounds import bounded_mean, cp, equivalence, minimum, interval_table, marginal_specs

HERE = Path(__file__).resolve().parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def analyze(raw_dir=None):
    raw_dir = Path(raw_dir or HERE/'results/raw')
    protocol = json.loads((HERE/'protocol.json').read_text())
    schedule = json.loads((HERE/'seeds.json').read_text())
    manifest = json.loads((raw_dir/'manifest.json').read_text())
    assert not manifest['fixture']
    assert manifest['protocol_sha256'] == sha((HERE/'protocol.json').read_bytes())
    assert protocol['core_sha256'] == sha((HERE.parent/'core.js').read_bytes())
    for file, pin in protocol['frozen_files'].items():
        assert sha((HERE/file).read_bytes()) == pin, file
    assert sha((raw_dir/'native-intervals.json.gz').read_bytes()) == manifest['intervals_sha256']
    native = json.loads(gzip.decompress((raw_dir/'native-intervals.json.gz').read_bytes()))
    m, eps, alpha = protocol['m'], protocol['engineering_allocation']['scale_equivalent_mean_bias'], protocol['alpha_per_gate']
    tables = {d: interval_table(m,d,eps) for d in protocol['dimensions']}
    interval_error = 0.0
    for ds, values in native.items():
        d = int(ds)
        for ks, v in values.items():
            k = int(ks)
            for native_key, py_key in [('lower','low'),('upper','high'),('center','center'),('relativeRadius','radius')]:
                interval_error = max(interval_error,abs(v[native_key]-float(tables[d][py_key][k])))
            for key, py_key in [('lower','native_low'),('upper','native_high')]:
                interval_error = max(interval_error,abs(v['native'][key]-float(tables[d][py_key][k])))
    assert interval_error <= protocol['technical_tolerances']['native_interval_absolute']
    gates, diagnostics, controls, engineering = [], [], {}, []
    assert len(manifest['groups']) == len(schedule['groups']) == 5
    for group, spec in zip(manifest['groups'],schedule['groups']):
        assert group['id'] == spec['id']
        data = (raw_dir/group['file']).read_bytes()
        assert sha(data) == group['sha256']
        raw = gzip.decompress(data)
        assert sha(raw) == group['raw_sha256']
        records = [json.loads(line) for line in raw.splitlines()]
        assert [r['seed'] for r in records] == spec['seeds']
        assert len(records) == group['clouds']
        d, arm, n = group['d'], group['arm'], len(records)
        assert n == (protocol['repetitions'] if arm == 'native' else 512)
        for i, r in enumerate(records):
            assert r['index'] == i and r['d'] == d and r['arm'] == arm
            assert r['max_support'] < .5
            assert 0 <= r['max_radial_error'] <= 1e-12 and 0 <= r['max_time_error'] <= 1e-12
            assert len(r['coordinates_sha256']) == 64
            assert all(0 <= k <= m for k in r['counts']+list(r['marginals'].values()))
            assert r['counts'] == sorted(r['counts'])
        engineering.append(dict(group=group['id'],clouds=n,
            max_transform_error=max(max(r['max_radial_error'],r['max_time_error']) for r in records),
            max_support=max(r['max_support'] for r in records),
            rejected={k:sum(r['rejected'][k] for r in records) for k in records[0]['rejected']},
            zero_radius=sum(r['zero_radius'] for r in records)))
        local_gates = []
        counts = np.array([r['counts'] for r in records])
        for j, theta in enumerate(protocol['theta_grid']):
            k = counts[:,j]
            p = theta**d
            mean = bounded_mean(k/m,p,m,alpha)
            allowed = [p*(1-eps)**d,p*(1+eps)**d]
            # Decisions use the actual native wrapper, independently checked above.
            low=np.array([native[str(d)][str(int(v))]['lower'] for v in k])
            high=np.array([native[str(d)][str(int(v))]['upper'] for v in k])
            radius=np.array([native[str(d)][str(int(v))]['relativeRadius'] for v in k])
            covered=(low <= theta) & (theta <= high)
            precise=radius <= .1
            successes=int(covered.sum())
            joint=int((covered & precise).sum())
            cov_ci, joint_ci = cp(successes,n,alpha), cp(joint,n,alpha)
            detail=dict(group=group['id'],d=d,theta=theta,clouds=n,mean_count_fraction=mean,
                scale_equivalent_mean_bias_interval=[(v/p)**(1/d)-1 for v in mean['interval']],
                coverage_successes=successes,coverage=successes/n,coverage_interval=cov_ci,
                precision=float(precise.mean()),joint_successes=joint,joint=joint/n,joint_interval=joint_ci,
                raw_estimator_relative_bias=float(np.mean((k/m)**(1/d)/theta-1)),
                raw_estimator_relative_rmse=float(np.sqrt(np.mean(((k/m)**(1/d)/theta-1)**2))),
                primary=theta in protocol['primary_theta'])
            diagnostics.append(detail)
            if detail['primary']:
                for metric, interval, target, status in [
                    ('mean-bias',mean['interval'],allowed,equivalence(mean['interval'],allowed)),
                    ('coverage',cov_ci,.95,minimum(cov_ci,.95)),
                    ('covered-and-precise',joint_ci,.90,minimum(joint_ci,.90))]:
                    local_gates.append(dict(id=f'd{d}-theta{theta}-{metric}',kind=metric,
                        interval=interval,target=target,status=status))
        for name, ideal in marginal_specs(d):
            values=np.array([r['marginals'][name] for r in records])/m
            bound=bounded_mean(values,ideal,m,alpha)
            allowed=[ideal-.005,ideal+.005]
            local_gates.append(dict(id=f'd{d}-{name}',kind='marginal',
                interval=bound['interval'],target=allowed,status=equivalence(bound['interval'],allowed),details=bound))
        if arm == 'native':
            gates.extend(local_gates)
        else:
            controls[arm]=local_gates
    assert len(gates) == protocol['gates'] == 52
    positive_checks=dict(
        wrong_radius_detected=any(g['status']=='FAIL' for g in controls['wrong-radius'] if '-radial_' in g['id']),
        repeated_point_detected=all(g['status']=='FAIL' for g in controls['repeated-point'] if g['kind']=='coverage'))
    assert all(positive_checks.values()), 'Positive control failed to expose a known defect.'
    status='FAIL' if any(g['status']=='FAIL' for g in gates) else (
        'PASS' if all(g['status']=='PASS' for g in gates) else 'UNENTSCHIEDEN')
    return dict(schema='x6.v1b-scoped-decision/2',decision=status,scope=protocol['scope'],
        historical_v1b='NOT_PASSED',phase3='HOLD_PHASE3',primary_points=protocol['primary_points'],
        family_confidence=.95,alpha_per_gate=alpha,
        gate_counts={s:sum(g['status']==s for g in gates) for s in ['PASS','FAIL','UNENTSCHIEDEN']},
        gates=gates,diagnostics=diagnostics,positive_controls=positive_checks,control_gates=controls,
        engineering=engineering,native_interval_max_absolute_error=interval_error,
        python_runtime=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__))


if __name__ == '__main__':
    result=analyze()
    target=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'results/decision.json'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:result[k] for k in ['decision','gate_counts','positive_controls','native_interval_max_absolute_error']}))
