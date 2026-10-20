"""Archive/source checks and numerical replay, not full search or external replication."""
import argparse
import hashlib
import json
import zipfile
import numpy as np
from mb_common import HERE, BASE, ROOT, contract, config, encode, digest, write_json
from mb_model import ARMS, prepare
from mb_fields import evaluate
from mb_analyze import load_rows, analyze
from cg_inference import prepare as original_prepare
from cg_relations import check
from run_calibration import coordinates_only
from feasibility import design, TARGET
from variance_weights import certify


def compare(a,b):
    if isinstance(a,dict):
        assert a.keys()==b.keys()
        for key in a: compare(a[key],b[key])
    elif isinstance(a,list):
        assert len(a)==len(b)
        for x,y in zip(a,b): compare(x,y)
    elif isinstance(a,float):
        np.testing.assert_allclose(a,b,atol=1e-9,rtol=1e-7)
    else:
        assert a==b,(a,b)


def main(strict=False):
    manifest_path=HERE/'manifest.json'
    if manifest_path.exists():
        for path,expected in json.loads(manifest_path.read_text()).items():
            assert hashlib.sha256((HERE/path).read_bytes()).hexdigest()==expected,path
    with zipfile.ZipFile(HERE/'test_clouds.zip') as archive:
        for name in archive.namelist():
            p=HERE/name
            if not p.exists():
                p.parent.mkdir(parents=True,exist_ok=True)
                p.write_bytes(archive.read(name))
            else:
                assert p.read_bytes()==archive.read(name),name
    frozen=json.loads((HERE/'frozen_model.json').read_text())
    for path,sha in frozen['archive_sha256'].items():
        assert hashlib.sha256((BASE/path).read_bytes()).hexdigest()==sha,path
    for path,sha in frozen['source_sha256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,path
    with zipfile.ZipFile(HERE/'residual_calibration.zip') as archive:
        records=json.loads(archive.read('records.json'))
    # Replay calibration inference and field evaluation from its original archive.
    _,oc,_,_=config()
    by_seed={r['seed']:r for r in records}
    residuals=[]
    with zipfile.ZipFile(BASE/contract()['residual_calibration_archive']) as archive:
        for name in sorted(archive.namelist()):
            if '/seed-' not in name or not name.endswith('.json'): continue
            r=json.loads(archive.read(name)); saved=by_seed[r['seed']]
            p=prepare(r['intrinsic'],frozen['models'])
            compare(p,saved['prepared'])
            z=coordinates_only(r['rho'],r['seed'],oc)
            ev=evaluate(p,r['selection']['selected'],z,r['seed'])
            compare(ev,saved['evaluation'])
            if ev['status']=='COMPLETE':
                residuals.extend([np.array(v['clean'])-v['truth'] for v in ev['fields']])
    residuals=np.array(residuals); mu=residuals.mean(axis=0)
    np.testing.assert_allclose(mu,frozen['residual_mean'],atol=1e-9,rtol=1e-7)
    np.testing.assert_allclose(np.cov(residuals,rowvar=False,ddof=0),frozen['residual_covariance'],atol=1e-9,rtol=1e-7)
    np.testing.assert_allclose(residuals.T@residuals/len(residuals),frozen['residual_second_moment'],atol=1e-9,rtol=1e-7)
    executions,rows=load_rows()
    hashes=intervals=moments=qps=0
    max_field=max_weight=0.
    for e in executions:
        assert e['source_sha256']==frozen['source_sha256']
    for r in rows:
        assert hashlib.sha256(encode(r['metadata_inference']).encode()).hexdigest()==r['inference_seal']
        z=coordinates_only(r['rho'],r['seed'],oc)
        matched=digest(z)==r['coordinates_sha256']; hashes+=int(matched)
        if strict: assert matched,'Strict coordinate-byte mismatch'
        w=r['selection']['selected']; order=np.array(r['observed_order'],bool)
        if w is not None:
            ids=[w['root']]+w['support']; assert check(z[ids],order)['passed']
            for (aa,bb),count in zip(w['certificate']['interval_pairs'],w['certificate']['interval_counts']):
                if z[aa,0]>z[bb,0]: aa,bb=bb,aa
                da,db=z-z[aa],z[bb]-z
                inside=(da[:,0]>0)&(db[:,0]>0)&(da[:,0]**2>np.sum(da[:,1:]**2,axis=1))&(db[:,0]**2>np.sum(db[:,1:]**2,axis=1))
                inside[[0,r['inner_physical_count']+1]]=False
                assert int(inside.sum())==count
                intervals+=1
        fresh=original_prepare(w,order,r['joint_pass'])
        assert fresh['status']==r['intrinsic']['status']
        p=prepare(fresh,frozen['models'])
        saved=r['metadata_inference']
        assert p['status']==saved['status']
        if p['status']!='COMPLETE': continue
        np.testing.assert_allclose(p['weights'],saved['weights'],atol=1e-7,rtol=1e-6)
        max_weight=max(max_weight,float(np.max(np.abs(np.array(p['weights'])-saved['weights']))))
        assert check(np.vstack(([0,0,0],r['intrinsic']['projection']['features'])),order)['passed']
        # Independent direct matrix products on all SIX actual weight vectors.
        for arm in [0,1]:
            x=r['intrinsic']['original_features'] if arm==0 else r['intrinsic']['projection']['features']
            d=design(x); qp=r['intrinsic']['certificates'][arm]
            assert certify(d,qp['weights'],None,qp['dual'])['passed']; qps+=1
            for j in ([0,1,4] if arm==0 else [2,3,5]):
                np.testing.assert_allclose(d@np.array(saved['weights'][j]),TARGET,atol=2e-6,rtol=0)
                moments+=1
        a=np.array(saved['weights']); s=saved['scale']
        independent=contract()['field_noise_sigma']**2*np.array([
            [float(x@y+x.sum()*y.sum())/s**4 for y in a] for x in a])
        np.testing.assert_allclose(independent,saved['conditional_field_covariance'],atol=1e-10,rtol=1e-10)
        np.testing.assert_allclose(np.array(saved['full_coefficients']).sum(axis=1),0,atol=1e-8)
        ev=evaluate(saved,w,z,r['seed'],transfer=True)
        compare(ev,r['evaluation'])
        for new,old in zip(ev['fields'],r['evaluation']['fields']):
            max_field=max(max_field,float(np.max(np.abs(np.array(new['clean'])-old['clean']))),
                          float(np.max(np.abs(np.array(new['observed'])-old['observed']))))
    summary=analyze(save=False)
    compare(summary,json.loads((HERE/'summary.json').read_text()))
    result=dict(status='PASS_STRICT_REPLAY' if strict else 'PASS_NUMERICAL_REPLAY',clouds=len(rows),
                complete=summary['complete'],coordinate_hash_matches=hashes,
                coordinate_hash_mismatches=len(rows)-hashes,independent_intervals=intervals,
                qp_certificates=qps,moment_certificates=moments,
                maximum_field_difference=max_field,maximum_recomputed_weight_difference=max_weight,
                scope='Residual calibration, order projection, moments, covariance, field and analysis replay. No full frame-search replay, no external replication, no componentwise archived-coordinate comparison. Portable tolerances predeclared in this source before test generation.')
    write_json(HERE/('verification_strict.json' if strict else 'verification.json'),result)
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--strict',action='store_true')
    main(p.parse_args().strict)
