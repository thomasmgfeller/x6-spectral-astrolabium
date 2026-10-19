"""Bounded coordinate-assisted feasibility audit, no fitted-field validation."""
import argparse
import copy
import hashlib
import json
import resource
import signal
import subprocess
import time
from pathlib import Path
import numpy as np
import scipy
from feas_common import HERE,ROOT,core,estimator,experiment,encode,config,sources,weighting,evaluate
from feas_controls import check,cloud_controls
from feasibility import design,solve,validate_record

def broaden(base,marks,cfg):
    s=copy.deepcopy(base)
    if 'sides' not in s:return s
    for side in s['sides']:side['selected']=side['shell']
    s.pop('support',None);s.pop('weights',None)
    if min(len(side['selected']) for side in s['sides'])<cfg['minimum_neighborhood_population']:
        s['status']='insufficient_neighborhood';return s
    s['status']='ok';times={x:s['tau_m'] for side in s['sides'] for x in side['selected']}
    return weighting.assemble(s,marks,cfg['coefficient_C'],times)


def analyze_support(stencil,z,contract):
    out=dict(status=stencil['status'])
    if stencil['status']!='ok':return out
    support=stencil['support'];tm=stencil['tau_m'];x=z-z[stencil['root']]
    d=design(x[support]/tm);a0=np.array(stencil['weights'])*tm**2
    temporal=[b in stencil['temporal'] for b in support]
    out.update(support=support,temporal_mask=temporal,design=d,baseline_coefficients=a0,
               baseline_mass=float(np.abs(a0).sum()),baseline_evaluation=evaluate(stencil,z),
               support_count=len(support),maximum_scaled_distance=float(np.linalg.norm(x[support]/tm,axis=1).max()),
               sides=[dict(reference=s['reference'],selected=s['selected']) for s in stencil['sides']],policies={})
    for policy in contract['policies']:
        row=solve(d,a0,temporal,policy,contract)
        if row['status']=='FEASIBLE':
            fitted={**stencil,'weights':(np.array(row['weights'])/tm**2).tolist()}
            matrix=core.metric_outer(fitted,x);product=core.metric(fitted,x)
            bound=contract['certificate_tolerance']*(1+np.abs(fitted['weights'])@(x[support]**2).sum(axis=1))
            assert float(np.max(np.abs(matrix-product)))<=bound
            assert float(core.apply(fitted,np.ones(len(z))))==0
            row['reconstructed']=dict(fitted_metric=matrix,fitted_linear_response=core.apply(fitted,x),
                product_identity_error=float(np.max(np.abs(matrix-product))),algebra_pass=True,
                root_coefficient=-float(np.sum(row['weights'])))
        out['policies'][policy]=row
    return out


def run_cloud(rho,seed,cfg,contract,controls=False):
    tick=time.monotonic();z,relation,marks,bottom,top=experiment.sprinkle(rho,seed)
    g=core.Poset(relation,marks);base=estimator.neighborhood(g,rho,bottom,top,cfg)
    stencils={'caps':base,'full_shells':broaden(base,marks,cfg)}
    supports={name:analyze_support(weighting.reweight(g,s,rho,cfg['coefficient_C']),z,contract) for name,s in stencils.items()}
    checks=cloud_controls(supports,contract,seed) if controls else None
    row=dict(rho=rho,seed=seed,poisson_count=len(z)-2,root=base['root'],chain=base['chain'],
             tau_m=base['tau_m'],tau_n=base['tau_n'],supports=supports,cloud_controls=checks,
             coordinates_sha256=hashlib.sha256(z.tobytes()).hexdigest(),relation_sha256=hashlib.sha256(relation.tobytes()).hexdigest(),
             marks_sha256=hashlib.sha256(marks.tobytes()).hexdigest(),seconds=time.monotonic()-tick)
    assert validate_record(row,contract)
    return row


def main():
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['development','test'],required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();contract,cfg=config()
    if a.output.exists():raise SystemExit('Refusing to overwrite output')
    sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();hashes=sources()
    if a.mode=='test':
        for path,digest in hashes.items():
            data=subprocess.check_output(['git','show',sha+':'+path],cwd=ROOT)
            assert hashlib.sha256(data).hexdigest()==digest,'unfrozen source '+path
    controls=check();a.output.mkdir(parents=True)
    e=dict(mode=a.mode,source_commit=sha,source_sha256=hashes,numpy=np.__version__,scipy=scipy.__version__,controls=controls,records=[],status='RUNNING')
    save=lambda:(a.output/'execution.json').write_text(json.dumps(e,indent=2)+'\n')
    save();start=time.monotonic()
    def timeout(signum,frame):raise TimeoutError('fixed wall budget exhausted')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(contract['wall_budget_seconds'])
    try:
        for i,rho in enumerate(contract['densities']):
            seeds=contract['development_seeds'] if a.mode=='development' else [contract['test_seed_base']+100*i+j for j in range(contract['test_replicates_per_density'])]
            for j,seed in enumerate(seeds):
                row=run_cloud(rho,seed,cfg,contract,controls=j==0);name=f'rho-{rho}-seed-{seed}.json';data=encode(row)
                (a.output/name).write_text(data);e['records'].append(dict(file=name,sha256=hashlib.sha256(data.encode()).hexdigest()));save()
                print(json.dumps(dict(rho=rho,seed=seed,seconds=round(row['seconds'],2),status={k:v['status'] for k,v in row['supports'].items()})),flush=True)
                if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024>contract['memory_budget_mib']:raise MemoryError('fixed memory budget exhausted')
        e['status']='COMPLETE'
    except (TimeoutError,MemoryError) as error:e.update(status='BUDGET_HOLD',reason=str(error))
    except Exception as error:
        e.update(status='ERROR',reason=repr(error));raise
    finally:
        signal.alarm(0);e.update(seconds=time.monotonic()-start,peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024);save()
    if e['status']!='COMPLETE':raise SystemExit(2)

if __name__=='__main__':main()
