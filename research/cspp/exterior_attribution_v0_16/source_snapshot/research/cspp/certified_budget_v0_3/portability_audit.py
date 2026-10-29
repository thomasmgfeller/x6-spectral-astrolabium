"""Explicit v0.2 portability qualification; frozen data and legacy audit stay intact.

The original seed-to-coordinate byte claim is hardware-specific. This companion
keeps canonical-byte checks, pins RNG draw outputs, and separately qualifies
numeric replay by exact probe counts/masks and the original operator tolerance.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import numpy as np

HERE=Path(__file__).resolve().parent
LEGACY=HERE.parent/'scale_calibration_v0_2'
sys.path.insert(0,str(LEGACY))
from common import old,plan,digest,cloud,gaussian_fields,load
from mean_operator import integral
from green_reference import evaluate as green
from fourier_nodes import evaluate as fourier
from run import frozen,summary
legacy=load('cspp_v02_original_audit',LEGACY/'audit.py')

COORDINATE_ABSOLUTE_SCREEN=2.0**-48  # L0; engineering screen, not a geometry theorem

def check(ok,label):
    if not bool(ok):raise RuntimeError('PORTABILITY HOLD: '+label)

class RecordedGenerator:
    def __init__(self,g):self.g=g;self.sha=hashlib.sha256()
    def __getattr__(self,name):
        def call(*args,**kwargs):
            result=getattr(self.g,name)(*args,**kwargs)
            v=np.asarray(result)
            self.sha.update(name.encode()+v.dtype.str.encode()+str(v.shape).encode()+np.ascontiguousarray(v).tobytes())
            return result
        return call

def regenerate(d,i):
    g=RecordedGenerator(np.random.Generator(np.random.PCG64DXSM(
        np.random.SeedSequence([1,3,d,i,1,plan()['master_seed']]))))
    n=int(g.poisson(plan()['nu_equivalent_Omega4'][d]))
    check(n<=plan()['point_cap'],'original point cap')
    x=old.points(g,n,4.);x[:,0]-=4.
    return np.ascontiguousarray(x),g.sha.hexdigest()

def runtime():
    return {'numpy':np.__version__,'disabled_features':os.environ.get('NPY_DISABLE_CPU_FEATURES'),
            'enabled_features':[k for k,v in np._core._multiarray_umath.__cpu_features__.items() if v]}

def capture():
    frozen();records=json.loads((LEGACY/'results/RUNS.json').read_text());rows=[]
    for r in records:
        d,i=r['density_index'],r['realization_index'];x,stream=regenerate(d,i)
        check(digest(x)==r['cloud_sha256'] and np.array_equal(x,cloud(d,i)),'capture must match historical coordinate bytes')
        rows.append({'key':r['key'],'rng_draw_output_sha256':stream,'historical_cloud_sha256':r['cloud_sha256']})
    return {'scope':'post-CI diagnostic capture on a CPU path reproducing all historical bytes; not a pre-existing raw-draw archive',
            'runtime':runtime(),'coordinate_absolute_screen_L0':COORDINATE_ABSOLUTE_SCREEN,
            'historical_package_unchanged':True,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'rows':rows}

def replay():
    frozen();controls=legacy.tests();out=LEGACY/'results'
    expected=np.load(out/'sprinklings.npz')['values'];records=json.loads((out/'RUNS.json').read_text())
    reference=json.loads((HERE/'PORTABILITY_STREAMS.json').read_text())
    check(reference['script_sha256']==hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'portability source lock')
    streams={r['key']:r for r in reference['rows']}
    check(len(streams)==48 and set(streams)=={r['key'] for r in records},'all fixed stream identities')
    rows=[];max_operator=0.;negative=0
    for r in records:
        d,i=r['density_index'],r['realization_index'];x,stream=regenerate(d,i)
        check(stream==streams[r['key']]['rng_draw_output_sha256'],'RNG draw outputs')
        canonical=np.load(out/f'clouds_d{d}_b{i//8}.npz')[r['key']]
        check(digest(canonical)==r['cloud_sha256']==streams[r['key']]['historical_cloud_sha256'],'canonical archive bytes')
        check(x.shape==canonical.shape and np.isfinite(x).all(),'coordinate shape/finiteness')
        difference=float(np.max(np.abs(x-canonical)))
        check(difference<=COORDINATE_ABSOLUTE_SCREEN,'coordinate numeric screen')
        _,pc=old.counts(x,np.zeros((1,4)),full=False)
        check(digest(pc[0])==r['counts_sha256'],'all regenerated probe interval counts exact')
        f=gaussian_fields(x,2);rho=r['nu_equivalent_Omega4']/old.volume(4)
        for hi,H in enumerate([4,6,8]):
            use=-x[:,0]+np.linalg.norm(x[:,1:],axis=1)<H
            canonical_use=-canonical[:,0]+np.linalg.norm(canonical[:,1:],axis=1)<H
            check(np.array_equal(use,canonical_use),'all nested-region memberships exact')
            for ei,ell in enumerate([1.,1.5,2.]):
                v=old.apply(pc[:,use],rho,ell**-4/rho,f[use],np.ones((1,4)))[0]
                max_operator=max(max_operator,float(np.max(np.abs(v-expected[d,i,hi,ei]))))
                check(np.allclose(v,expected[d,i,hi,ei],atol=1e-10,rtol=1e-11),'original operator tolerance')
        if not rows:
            # Negative controls keep archival corruption distinct from permitted
            # arithmetic portability. These exercise each separate guard.
            damaged=canonical.copy();damaged[0,1]=np.nextafter(damaged[0,1],np.inf)
            check(digest(damaged)!=r['cloud_sha256'],'archive one-ULP corruption rejected');negative+=1
            shifted=x.copy();shifted[0,1]+=1e-9
            check(np.max(np.abs(shifted-canonical))>COORDINATE_ABSOLUTE_SCREEN,'large coordinate shift rejected');negative+=1
            changed=pc[0].copy();changed[0]+=1
            check(digest(changed)!=r['counts_sha256'],'one interval-count change rejected');negative+=1
            check(regenerate(d,i+1)[1]!=stream,'wrong seed stream rejected');negative+=1
            badmask=use.copy();badmask[0]=not badmask[0]
            check(not np.array_equal(badmask,canonical_use),'changed region membership rejected');negative+=1
        rows.append({'key':r['key'],'coordinate_bytes_identical':bool(np.array_equal(x,canonical)),
                     'maximum_coordinate_absolute_difference':difference,
                     'changed_coordinate_components':int(np.count_nonzero(x!=canonical)),
                     'rng_draws_probe_counts_and_region_masks_exact':True})
    # Retain all deterministic v0.2 replay checks, including Fourier resolutions.
    m=np.load(out/'mean.npz')['values'];mrows=json.loads((out/'MEAN.json').read_text())['rows']
    for i,r in enumerate(mrows):
        check(np.allclose(integral(r['ell_k'],r['H'],r['L'],384),m[i,-1],atol=1e-9,rtol=1e-10),'full mean replay')
    src=np.load(out/'source.npz')
    check(np.allclose(green(src['query'],256),src['green'][-1],atol=1e-11,rtol=1e-10),'full Green replay')
    for j,n in enumerate([64,128,256]):
        value,_=fourier(src['query'][:28],n)
        check(np.allclose(value,src['fourier'][j],atol=1e-10,rtol=1e-9),'all Fourier resolutions')
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)
        for name in ['mean.npz','MEAN.json','sprinklings.npz','RUNS.json','source.npz']:(p/name).symlink_to((out/name).resolve())
        summary(p);check(json.loads((p/'RESULTS.json').read_text())==json.loads((out/'RESULTS.json').read_text()),'exact summary replay')
    return {'status':'PASS_NUMERIC_REPLAY_NOT_GENERAL_BITWISE_REPRODUCIBILITY',
            'runtime':runtime(),'legacy_controls':controls,'negative_controls':negative,
            'runs':rows,'maximum_operator_absolute_difference':max_operator,
            'coordinate_bytes_identical_for_all_runs':all(r['coordinate_bytes_identical'] for r in rows),
            'claim_boundary':'probe interval counts and masks exact; operator tolerances unchanged; not all pairwise causal relations certified',
            'G1':'HOLD','confirmation_seed_used':False}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--capture-streams',action='store_true')
    ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    if a.capture_streams and a.output.exists():raise RuntimeError('do not replace stream capture')
    check(np.__version__=='2.3.5','pinned numpy version')
    result=capture() if a.capture_streams else replay()
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['rows','runs','legacy_controls']},indent=2))

if __name__=='__main__':main()
