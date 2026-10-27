"""Explicit numeric replay of v0.1; original archives/audit remain unchanged.

The original audit's general seed-to-coordinate byte assumption is not portable
across NumPy CPU dispatch paths. This separate post-failure audit keeps exact
archive/RNG/count checks and the original numerical tolerances.
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
LEGACY=HERE.parent/'scalar_pilot_v0_1'
sys.path.insert(0,str(LEGACY))
import scalar
from fields import fields
from reference import evaluate
from run import frozen, summarize
from prepare_reference import prepare
spec=importlib.util.spec_from_file_location('original_scalar_pilot_audit',LEGACY/'audit.py')
legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
SCREEN=2.0**-48  # L0; numerical screen, not an exact-geometry theorem.


def check(ok,label):
    if not bool(ok):raise RuntimeError('PORTABILITY HOLD: '+label)


class RecordedGenerator:
    def __init__(self,g):self.g=g;self.sha=hashlib.sha256()
    def __getattr__(self,name):
        def call(*args,**kwargs):
            result=getattr(self.g,name)(*args,**kwargs)
            v=np.asarray(result)
            self.sha.update(name.encode()+v.dtype.str.encode()+str(v.shape).encode()
                            +np.ascontiguousarray(v).tobytes())
            return result
        return call


def regenerate(d,i,inner=None):
    # Instrument only RNG call results; the frozen sampler executes unchanged.
    original=scalar.rng;generators=[]
    def recorded(*args,**kwargs):
        g=RecordedGenerator(original(*args,**kwargs));generators.append(g);return g
    scalar.rng=recorded
    try:
        x=scalar.sprinkle(d,i) if inner is None else scalar.extend(inner,d,i)
    finally:
        scalar.rng=original
    check(len(generators)==1,'one unchanged sampler stream')
    return x,generators[0].sha.hexdigest()


def runtime():
    return {'numpy':np.__version__,'disabled_features':os.getenv('NPY_DISABLE_CPU_FEATURES'),
            'enabled_features':[k for k,v in np._core._multiarray_umath.__cpu_features__.items() if v]}


def capture():
    frozen();records=json.loads((LEGACY/'results/RUNS.json').read_text())
    clouds=np.load(LEGACY/'results/clouds.npz');rows=[]
    for r in records:
        d,i,key=r['density_index'],r['realization_index'],r['key']
        x,stream=regenerate(d,i)
        check(np.array_equal(x,clouds[key]) and scalar.digest(x)==r['coordinates_sha256'],
              'capture must reproduce all original inner bytes')
        row={'key':key,'rng_draw_output_sha256':stream,
             'historical_coordinates_sha256':r['coordinates_sha256']}
        if 'outer_metric_index' in r:
            y,outer_stream=regenerate(d,i,x)
            check(np.array_equal(y,clouds[key+'_outer']) and scalar.digest(y)==r['outer_sha256'],
                  'capture must reproduce all original outer bytes')
            row['outer_rng_draw_output_sha256']=outer_stream
            row['historical_outer_sha256']=r['outer_sha256']
        rows.append(row)
    return {'scope':'post-CI diagnostic capture on a path reproducing all original bytes; not a prior raw-draw archive',
            'runtime':runtime(),'coordinate_absolute_screen_L0':SCREEN,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'rows':rows}


def coordinate_check(x,canonical,digest,label):
    check(scalar.digest(canonical)==digest,'canonical archive '+label)
    check(x.shape==canonical.shape and np.isfinite(x).all(),'shape/finiteness '+label)
    delta=float(np.max(np.abs(x-canonical),initial=0))
    check(delta<=SCREEN,'coordinate screen '+label)
    return {'bytes_identical':bool(np.array_equal(x,canonical)),
            'maximum_coordinate_absolute_difference':delta,
            'changed_coordinate_components':int(np.count_nonzero(x!=canonical))}


def replay():
    prepare();frozen();controls=legacy.self_test();out=LEGACY/'results'
    z=np.load(out/'metrics.npz');clouds=np.load(out/'clouds.npz');ref=np.load(out/'reference.npz')
    records=json.loads((out/'RUNS.json').read_text());p=scalar.probes();fp,bp=fields(p)
    source=json.loads((HERE/'STREAMS.json').read_text())
    check(source['script_sha256']==hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'source lock')
    streams={r['key']:r for r in source['rows']}
    check(len(streams)==64 and set(streams)=={r['key'] for r in records},'all 64 stream identities')
    unchanged=json.loads((LEGACY/'amendment_01/UNCHANGED_PRIMARY_HASHES.json').read_text())
    for key,value in unchanged.items():check(scalar.digest(z[key])==value,'unchanged primary array '+key)
    rows=[];maxop=0.;maxprop=0.;maxres=0.;negative=0
    for r in records:
        d,i,key=r['density_index'],r['realization_index'],r['key']
        check(r['status']=='COMPUTED_DIAGNOSTIC','resolved historical run status')
        x,stream=regenerate(d,i);s=streams[key]
        check(stream==s['rng_draw_output_sha256'],'exact RNG draw outputs '+key)
        check(s['historical_coordinates_sha256']==r['coordinates_sha256'],'fixed inner identity')
        row={'key':key,**coordinate_check(x,clouds[key],r['coordinates_sha256'],key)}
        cc,pc=scalar.counts(x,p)
        check(scalar.digest(cc)==r['interval_counts_sha256'] and
              scalar.digest(pc)==r['probe_counts_sha256'],'all interval/probe counts exact '+key)
        for mask in [lambda a:a[:,0]<=-1,lambda a:a[:,0]<1]:
            check(np.array_equal(mask(x),mask(clouds[key])),'history and active memberships exact')
        f,b=fields(x);h=np.column_stack([f[:,6:],ref[key+'_fine'],np.ones(len(x))])
        J=np.column_stack([b[:,6:]-f[:,6:],np.zeros((len(x),4))])
        Jp=np.column_stack([bp[:28,6:]-fp[:28,6:],np.zeros((28,4))])
        rho=r['nu']/scalar.volume(4)
        for ei,e in enumerate([1,.25,.0625]):
            op=scalar.apply(pc,rho,e,f,fp)
            v,res=scalar.propagate(cc,pc[:28],x,p[:28],rho,e,h,J,Jp,[1,1,1,1,0,1,2,1])
            check(np.allclose(op,z['operator'][d,i,ei],atol=1e-10,rtol=1e-11),'original operator tolerance')
            check(np.allclose(v,z['propagation'][d,i,ei],atol=1e-10,rtol=1e-11) and res<1e-12,
                  'original propagation/residual tolerances')
            maxop=max(maxop,float(np.max(np.abs(op-z['operator'][d,i,ei]))))
            maxprop=max(maxprop,float(np.max(np.abs(v-z['propagation'][d,i,ei]))));maxres=max(maxres,res)
        if 'outer_metric_index' in r:
            y,outer_stream=regenerate(d,i,x)
            check(outer_stream==s['outer_rng_draw_output_sha256'],'exact shell RNG draw outputs')
            check(s['historical_outer_sha256']==r['outer_sha256'],'fixed outer identity')
            row['outer']=coordinate_check(y,clouds[key+'_outer'],r['outer_sha256'],key+'_outer')
            _,oc=scalar.counts(y,p,full=False)
            check(scalar.digest(oc)==r['outer_probe_counts_sha256'],'all outer probe counts exact')
            fy,_=fields(y)
            for ei,e in enumerate([1,.25,.0625]):
                value=scalar.apply(oc,rho,e,fy,fp);target=z['outer_operator'][r['outer_metric_index'],ei]
                check(np.allclose(value,target,atol=1e-10,rtol=1e-11),'original outer operator tolerance')
                maxop=max(maxop,float(np.max(np.abs(value-target))))
        if not rows:
            bad=clouds[key].copy();bad[0,1]=np.nextafter(bad[0,1],np.inf)
            check(scalar.digest(bad)!=r['coordinates_sha256'],'negative: archive corruption');negative+=1
            bad=x.copy();bad[0,1]+=1e-9
            check(np.max(np.abs(bad-clouds[key]))>SCREEN,'negative: coordinate shift');negative+=1
            bad=cc.copy();bad[0,0]+=1
            check(scalar.digest(bad)!=r['interval_counts_sha256'],'negative: full interval count');negative+=1
            check(regenerate(d,i+1)[1]!=stream,'negative: wrong seed');negative+=1
            mask=x[:,0]<=-1;bad=mask.copy();bad[0]=not bad[0]
            check(not np.array_equal(bad,mask),'negative: history membership');negative+=1
            bad=oc.copy();bad[0,0]+=1
            check(scalar.digest(bad)!=r['outer_probe_counts_sha256'],'negative: outer count');negative+=1
        row['rng_counts_and_history_memberships_exact']=True
        rows.append(row)
    for label,n,dt in [('coarse',64,.125),('fine',128,.0625)]:
        value,_=evaluate(p[:28],n,dt)
        check(np.allclose(value,ref['probes_'+label],atol=1e-12,rtol=1e-11),'original Fourier probe replay')
    with tempfile.TemporaryDirectory() as tmp:
        temp=Path(tmp)
        for name in ['metrics.npz','reference.npz','RUNS.json']:
            (temp/name).symlink_to((out/name).resolve())
        summarize(temp)
        check(json.loads((temp/'RESULTS.json').read_text())==json.loads((out/'RESULTS.json').read_text()),
              'exact historical summary replay')
    return {'status':'PASS_NUMERIC_REPLAY_NOT_GENERAL_BITWISE_REPRODUCIBILITY',
            'runtime':runtime(),'legacy_controls':controls,'runs':rows,'negative_controls':negative,
            'maximum_operator_absolute_difference':maxop,'maximum_propagation_absolute_difference':maxprop,
            'maximum_backward_residual':maxres,'inner_runs':len(rows),'outer_runs':sum('outer' in r for r in rows),
            'all_coordinate_bytes_identical':all(r['bytes_identical'] and r.get('outer',{}).get('bytes_identical',True) for r in rows),
            'claim_boundary':'computed interval/probe counts and history memberships exact; original numerical tolerances retained; no general bitwise portability',
            'G1':'HOLD','confirmation_seed_used':False}


def main():
    p=argparse.ArgumentParser();p.add_argument('--capture',action='store_true');p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();check(np.__version__=='2.3.5','pinned NumPy')
    if args.capture:check(not args.output.exists(),'do not overwrite captured stream identity')
    result=capture() if args.capture else replay()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['rows','runs','legacy_controls','runtime']}))


if __name__=='__main__':main()
