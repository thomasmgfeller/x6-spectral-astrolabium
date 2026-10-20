"""Independent certificate/field/order replay; not a full search replication."""
import hashlib
import json
import zipfile
import numpy as np
from cg_common import HERE, BASE, ROOT, config, contract, digest
from cg_analyze import load_rows, analyze
from cg_relations import check
from cg_inference import prepare
from cg_run import evaluate
from run_calibration import coordinates_only
from feasibility import design
from variance_weights import certify


def main(portable=False):
    for prefix in ['test', 'development']:
        manifest = json.loads((HERE/f'{prefix}_manifest.json').read_text())
        archive_name = 'test_clouds.zip' if prefix == 'test' else 'development_records.zip'
        with zipfile.ZipFile(HERE/archive_name) as archive:
            for path, expected_hash in manifest.items():
                data = (HERE/path).read_bytes() if path == archive_name else archive.read(path)
                assert hashlib.sha256(data).hexdigest() == expected_hash, path
    with zipfile.ZipFile(HERE/'development_records.zip') as archive:
        development = json.loads(archive.read('development_records.json'))
    with zipfile.ZipFile(BASE/'feynman_combiner/independent_clouds.zip') as archive:
        assert len(development) == 64
        for row in development:
            assert hashlib.sha256(archive.read(row['source_file'])).hexdigest() == row['source_sha256']
    complete_development = [r for r in development if r['evaluation']['status'] == 'COMPLETE']
    cal = json.loads((HERE/'frozen_calibration.json').read_text())
    clean = np.array([r['evaluation']['clean'] for r in complete_development])+.75
    np.testing.assert_allclose(cal['bias'], clean.mean(axis=0),atol=1e-12,rtol=1e-12)
    np.testing.assert_allclose(cal['geometry_covariance'],np.cov(clean,rowvar=False),atol=1e-12,rtol=1e-12)
    np.testing.assert_allclose(cal['bias_mean_covariance'],np.cov(clean,rowvar=False)/len(clean),atol=1e-12,rtol=1e-12)
    np.testing.assert_allclose(cal['mean_noise_covariance'],np.mean([r['intrinsic']['conditional_field_covariance'] for r in complete_development],axis=0),atol=1e-12,rtol=1e-12)
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
    coordinate_matches = 0
    max_field_error = 0.
    max_weight_error = 0.
    for row in rows:
        z = coordinates_only(row['rho'],row['seed'],oc)
        assert z.shape == (row['physical_count']+2,3) and np.isfinite(z).all()
        matched = digest(z) == row['coordinates_sha256']
        coordinate_matches += int(matched)
        if not portable:
            assert matched, 'strict coordinate-byte replay failed; use separately labelled portable replay for diagnostics'
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
        max_weight_error = max(max_weight_error,float(np.max(np.abs(np.array(intrinsic['weights'])-original['weights']))))
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
            max_field_error = max(max_field_error,float(np.max(np.abs(np.array(ev[key])-row['evaluation'][key]))))
    prior = (HERE/'summary.json').read_bytes() if (HERE/'summary.json').exists() else None
    summary = analyze()
    if prior is not None:
        def compare(a,b):
            if isinstance(a,dict):
                assert a.keys()==b.keys()
                for key in a: compare(a[key],b[key])
            elif isinstance(a,list):
                assert len(a)==len(b)
                for x,y in zip(a,b): compare(x,y)
            elif isinstance(a,float):
                np.testing.assert_allclose(a,b,atol=1e-10,rtol=1e-9)
            else: assert a==b
        compare(json.loads(prior),summary)
        (HERE/'summary.json').write_bytes(prior)
    result = dict(status='PASS_PORTABLE_ORDER_CERTIFICATES_FIELD_REPLAY' if portable else 'PASS_ORDER_CERTIFICATES_FIELD_AND_ANALYSIS_REPLAY',clouds=len(rows),
                  complete=summary['complete'],coordinate_hashes=coordinate_matches,
                  coordinate_hash_mismatches=len(rows)-coordinate_matches,
                  maximum_absolute_field_difference=max_field_error,
                  maximum_absolute_recomputed_weight_difference=max_weight_error,
                  independently_counted_intervals=total_intervals,qp_certificates=total_qp,
                  scope='Not full frame-search replay or external replication; projection repeated, numerical witnesses checked independently. Summary discrete outputs exact; floats atol=1e-10, rtol=1e-9. Portable mode records but does not require coordinate bytehash equality; no componentwise comparison against archived coordinates is claimed.')
    name = 'portable_verification.json' if portable else 'verification.json'
    (HERE/name).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
