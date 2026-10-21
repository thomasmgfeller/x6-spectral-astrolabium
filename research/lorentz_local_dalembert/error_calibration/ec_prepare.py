"""SPDX-License-Identifier: Apache-2.0
Fit scales on explicitly reused development clouds; never run a target cloud.
"""
import json
import math
import secrets
import zipfile
import numpy as np
from ec_common import HERE,BASE,ROOT,cfg,config,models,prepare,pins,sha,write,coordinates_only,digest
from ec_measure import field_values


def archive_rows(path):
    with zipfile.ZipFile(path) as archive:
        return sorted([json.loads(archive.read(n)) for n in archive.namelist()
                       if '/seed-' in n and n.endswith('.json')],key=lambda r:r['seed'])


def fit_development():
    rows=archive_rows(BASE/'metadata_bias/test_clouds.zip')
    _,oc,_,_=config(); frozen=models(); records=[]; errors=[]
    for row in rows:
        p=prepare(row['intrinsic'],frozen)
        if p['status']!='COMPLETE':
            records.append(dict(seed=row['seed'],status=p['status']));continue
        np.testing.assert_allclose(p['full_coefficients'],row['metadata_inference']['full_coefficients'],atol=1e-8,rtol=1e-7)
        z=coordinates_only(row['rho'],row['seed'],oc)
        selected=row['selection']['selected']
        delta=z[selected['support']]-z[selected['root']]
        b=np.asarray(p['full_coefficients'])[:4]
        error=[]
        for spec in cfg()['fields']:
            values,truth=field_values(delta,spec)
            error.append((b[:,1:]@values-truth).tolist())
        errors.append(error)
        records.append(dict(seed=row['seed'],status='COMPLETE',errors=error,
                            coordinate_hash_matches=digest(z)==row['coordinates_sha256']))
    e=np.asarray(errors);n=len(e);assert n>=24
    mu=e.mean(axis=0); centered=e-mu
    g=np.einsum('cfa,cfb->fab',centered,centered)/n
    second=np.einsum('cfa,cfb->fab',e,e)/n
    np.testing.assert_allclose(second,g+np.einsum('fa,fb->fab',mu,mu),atol=1e-12)
    mean_variance=g/(n-1)
    scales=np.sqrt(np.maximum(1e-12,np.diagonal(second+mean_variance,axis1=1,axis2=2)))
    return dict(status='DEVELOPMENT_FIT',clouds=len(rows),complete=n,fields=cfg()['fields'],
                mean_bias=mu.tolist(),geometry_covariance=g.tolist(),
                uncentered_second_moment=second.tolist(),estimated_mean_fit_covariance=mean_variance.tolist(),
                fixed_scales=scales.tolist(),records=records,
                interpretation='Old test clouds explicitly reused for development. Per-field means/covariances across clouds; no conditional or embedding covariance, no independent evidence.')


def main():
    assert not (HERE/'seed_schedule.json').exists(),'No replacement of drawn target seeds.'
    development=fit_development();write(HERE/'development_fit.json',development)
    prior={0,1,4294967295}
    for name in ['feynman_combiner/independent_clouds.zip','conditional_geometry/test_clouds.zip','metadata_bias/test_clouds.zip']:
        prior.update(r['seed'] for r in archive_rows(BASE/name))
    skipped=[];schedule={}
    for phase,count in [('calibration',cfg()['geometry_calibration_clouds']),('test',cfg()['test_clouds'])]:
        specs=[]
        while len(specs)<count:
            seed=secrets.randbits(32)
            if seed in prior:skipped.append(seed);continue
            specs.append(dict(index=len(specs),geometry_seed=seed,noise_key=secrets.randbits(128)))
        schedule[phase]=specs
    write(HERE/'seed_schedule.json',dict(excluded_prior_seeds=sorted(prior),skipped=skipped,
            eligible_population=2**32-len(prior),**schedule))
    files=pins()
    for n in ['development_fit.json','seed_schedule.json']:
        path=HERE/n;files[str(path.relative_to(ROOT))]=sha(path.read_bytes())
    write(HERE/'source_pins.json',dict(files=files))
    print(json.dumps(dict(development_complete=development['complete'],new_clouds=64,
        excluded=len(prior),source_files=len(files),fixed_scales=development['fixed_scales'])))


if __name__=='__main__':main()
