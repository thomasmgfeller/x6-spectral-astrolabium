"""Independent certificate/field/order replay; not a full search replication."""
import hashlib
import json
import numpy as np
from cg_common import HERE, ROOT, config, contract, digest
from cg_analyze import load_rows, analyze
from cg_relations import check
from cg_inference import prepare
from cg_run import evaluate
from run_calibration import coordinates_only
from feasibility import design
from variance_weights import certify


def main():
    executions, rows = load_rows()
    c = contract()
    expected = list(range(c['test_seeds'][0], c['test_seeds'][1]+1))
    assert [r['seed'] for r in rows] == expected
    for e in executions:
        assert e['status'] == 'COMPLETE'
        for path, sha in e['source_sha256'].items():
            assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == sha, path
    _, oc, _, _ = config()
    total_intervals = 0
    total_qp = 0
    for row in rows:
        z = coordinates_only(row['rho'],row['seed'],oc)
        assert digest(z) == row['coordinates_sha256']
        w = row['selection']['selected']
        r = np.array(row['observed_order'],bool)
        if w is not None:
            ids = [w['root']]+w['support']
            assert check(z[ids],r)['passed']
            # Independent full-coordinate interval counts; remove artificial probes.
            for (a,b), count in zip(w['certificate']['interval_pairs'],w['certificate']['interval_counts']):
                if z[a,0] > z[b,0]: a,b = b,a
                da, db = z-z[a], z[b]-z
                inside = (da[:,0]>0)&(db[:,0]>0)&(da[:,0]**2>np.sum(da[:,1:]**2,axis=1))&(db[:,0]**2>np.sum(db[:,1:]**2,axis=1))
                inside[[0,row['inner_physical_count']+1]] = False
                assert int(inside.sum()) == count
                total_intervals += 1
        intrinsic = prepare(w,r,row['joint_pass'])
        assert intrinsic['status'] == row['intrinsic']['status']
        if intrinsic['status'] != 'COMPLETE': continue
        original = row['intrinsic']
        for key in ['weights','conditional_field_covariance']:
            np.testing.assert_allclose(intrinsic[key],original[key],atol=1e-8,rtol=1e-7)
        points = np.vstack(([0,0,0],original['projection']['features']))
        assert check(points,r)['passed']
        for x, qp in zip([original['original_features'],original['projection']['features']],original['certificates']):
            assert certify(design(x),qp['weights'],None,qp['dual'])['passed']
            total_qp += 1
        weights = np.array(original['weights'])
        assert hashlib.sha256(weights.tobytes()).hexdigest() == original['weights_seal']
        full = np.column_stack((-weights.sum(axis=1),weights))/original['scale']**2
        # Independent row-pair scalar sum for covariance.
        want = [[c['field_noise_sigma']**2*sum(float(a*b) for a,b in zip(x,y)) for y in full] for x in full]
        np.testing.assert_allclose(want,original['conditional_field_covariance'],atol=1e-10,rtol=1e-10)
        ev = evaluate(original,w,z,row['seed'])
        for key in ['clean','observed']:
            np.testing.assert_allclose(ev[key],row['evaluation'][key],atol=1e-10,rtol=1e-10)
    prior = (HERE/'summary.json').read_bytes() if (HERE/'summary.json').exists() else None
    summary = analyze()
    if prior is not None:
        assert prior == (HERE/'summary.json').read_bytes()
    result = dict(status='PASS_ORDER_CERTIFICATES_FIELD_AND_ANALYSIS_REPLAY',clouds=len(rows),
                  complete=summary['complete'],coordinate_hashes=len(rows),
                  independently_counted_intervals=total_intervals,qp_certificates=total_qp,
                  scope='Not full frame-search replay or external replication; projection repeated, numerical witnesses checked independently.')
    (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
