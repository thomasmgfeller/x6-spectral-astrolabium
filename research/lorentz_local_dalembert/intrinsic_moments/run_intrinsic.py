"""Frozen experiment: inference completes before independent field evaluation."""
import argparse
import hashlib
import json
import resource
import signal
import subprocess
import time
from pathlib import Path
import numpy as np
import scipy
from im_common import HERE,ROOT,core,estimator,experiment,encode,config,sources,weighting,evaluate
from im_controls import check,transport
from intrinsic import infer,calibrate

def field_evaluation(s,z,c):
    out=evaluate(s,z)
    if s['status']!='ok':return out
    x=z-z[s['root']];fields={}
    for ki,k in enumerate(c['wavevectors']):
        k=np.array(k,float)
        for frequency in c['frequencies']:
            phase=frequency*(x@k);normalizer=frequency**2*float(k@k)
            for kind,values,target in [('cos',np.cos(phase),frequency**2*(k[0]**2-k[1]**2-k[2]**2)),('sin',np.sin(phase),0.)]:
                response=float(core.apply(s,values));name=f'{kind}-k{ki}-f{frequency}'
                fields[name]=dict(value=response,target=float(target),normalized_error=(response-target)/normalizer)
    out['independent_fields']=fields
    out['independent_field_rms']=float(np.sqrt(np.mean([f['normalized_error']**2 for f in fields.values()])))
    weights=np.array(s['weights']);a=weights*s['tau_m']**2
    out.update(absolute_mass=float(np.abs(a).sum()),root_coefficient=-float(a.sum()),
               iid_noise_variance_factor=float(a@a+a.sum()**2),
               dimensional_iid_noise_variance_factor=float(weights@weights+weights.sum()**2))
    return out

def run_cloud(rho,seed,cfg,c,controls=False):
    tick=time.monotonic();z,relation,marks,bottom,top=experiment.sprinkle(rho,seed)
    colours=np.random.default_rng(seed^c['colour_seed_xor']).integers(0,2,size=len(z),dtype=np.uint8)
    g=core.Poset(relation,marks);base=estimator.neighborhood(g,rho,bottom,top,cfg)
    s=weighting.reweight(g,base,rho,cfg['coefficient_C'])
    inferred=infer(g,s,rho,[bottom,top],colours,c)
    checks=transport(g,s,rho,[bottom,top],colours,c,inferred,seed) if controls else None
    arms={};oracle=None
    if s['status']=='ok':
        a0=np.array(s['weights'])*s['tau_m']**2;mask=[b in s['temporal'] for b in s['support']]
        # First access of validation coordinates for calibration: diagnostic oracle only.
        oracle=calibrate((z[s['support']]-z[s['root']])/s['tau_m'],a0,mask,c)
        oracle_used=oracle['status']=='VERIFIED'
        stencils={'volume_shell':(s,False,[]),
            **{name:({**s,'weights':inferred[name]['weights']},inferred[name]['adopted'],inferred[name]['fallback_reasons'])
               for name in ['intrinsic_raw','intrinsic_guarded']},
            'coordinate_oracle':({**s,'weights':np.array(oracle['weights'])/s['tau_m']**2 if oracle_used else s['weights']},oracle_used,[] if oracle_used else ['unresolved_calibration'])}
        for name,(stencil,adopted,reasons) in stencils.items():
            arms[name]=dict(status='ok',adopted=adopted,fallback_reasons=reasons,weights=stencil['weights'],
                            evaluation=field_evaluation(stencil,z,c))
    else:
        arms={name:dict(status=s['status'],adopted=False,fallback_reasons=['unavailable_stencil'],evaluation={'status':s['status']}) for name in c['methods']}
    keys=['status','root','chain','n','m','tau_n','tau_m','temporal','support','weights']
    selection={k:s[k] for k in keys if k in s}
    if 'sides' in s:selection['sides']=[dict(reference=v['reference'],selected=v['selected']) for v in s['sides']]
    return dict(rho=rho,seed=seed,poisson_count=len(z)-2,selection=selection,inference=inferred,
                coordinate_oracle=oracle,arms=arms,cloud_controls=checks,
                coordinates_sha256=hashlib.sha256(z.tobytes()).hexdigest(),relation_sha256=hashlib.sha256(relation.tobytes()).hexdigest(),
                marks_sha256=hashlib.sha256(marks.tobytes()).hexdigest(),colours_sha256=hashlib.sha256(colours.tobytes()).hexdigest(),
                seconds=time.monotonic()-tick)

def main():
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['development','test'],required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();c,cfg=config()
    if a.output.exists():raise SystemExit('Refusing to overwrite output')
    sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();hashes=sources()
    if a.mode=='test':
        for path,digest in hashes.items():
            assert hashlib.sha256(subprocess.check_output(['git','show',sha+':'+path],cwd=ROOT)).hexdigest()==digest,'unfrozen source '+path
    controls=check();a.output.mkdir(parents=True)
    e=dict(mode=a.mode,source_commit=sha,source_sha256=hashes,numpy=np.__version__,scipy=scipy.__version__,controls=controls,records=[],status='RUNNING')
    save=lambda:(a.output/'execution.json').write_text(json.dumps(e,indent=2)+'\n')
    save();start=time.monotonic()
    def timeout(signum,frame):raise TimeoutError('fixed wall budget exhausted')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(c['wall_budget_seconds'])
    try:
        for i,rho in enumerate(c['densities']):
            seeds=c['development_seeds'] if a.mode=='development' else [c['test_seed_base']+100*i+j for j in range(c['test_replicates_per_density'])]
            for j,seed in enumerate(seeds):
                row=run_cloud(rho,seed,cfg,c,controls=j==0);name=f'rho-{rho}-seed-{seed}.json';data=encode(row)
                (a.output/name).write_text(data);e['records'].append(dict(file=name,sha256=hashlib.sha256(data.encode()).hexdigest()));save()
                print(json.dumps(dict(rho=rho,seed=seed,seconds=round(row['seconds'],2),frame=row['inference']['frame']['status'],
                    adopted={k:v['adopted'] for k,v in row['arms'].items()})),flush=True)
                if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024>c['memory_budget_mib']:raise MemoryError('fixed memory budget exhausted')
        e['status']='COMPLETE'
    except (TimeoutError,MemoryError) as error:e.update(status='BUDGET_HOLD',reason=str(error))
    except Exception as error:
        e.update(status='ERROR',reason=repr(error));raise
    finally:
        signal.alarm(0);e.update(seconds=time.monotonic()-start,peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024);save()
    if e['status']!='COMPLETE':raise SystemExit(2)

if __name__=='__main__':main()
