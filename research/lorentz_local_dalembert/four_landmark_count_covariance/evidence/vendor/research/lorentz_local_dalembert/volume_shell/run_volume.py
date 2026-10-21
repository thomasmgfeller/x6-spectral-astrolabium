"""Frozen bounded experiment; coordinates used only in oracle arms/evaluation."""
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
from volume_common import HERE,ROOT,core,estimator,experiment,diagnose,encode,config,sources
import weighting
from volume_controls import check,relabel_check


def evaluate(s,z):
    if s['status']!='ok':return dict(status=s['status'])
    x=z-z[s['root']];metric=core.metric_outer(s,x);linear=core.apply(s,x)
    np.testing.assert_allclose(metric,core.metric(s,x),atol=1e-10,rtol=1e-10)
    transform=np.array([[1.2,.1,0.],[.2,.9,.1],[0.,.15,1.1]])
    transformed=x@transform.T+np.array([.3,-.2,.7])
    np.testing.assert_allclose(core.metric(s,transformed),transform@metric@transform.T,atol=1e-9,rtol=1e-10)
    fields={'constant':np.ones(len(x)),'t':x[:,0],'x':x[:,1],'y':x[:,2],
            'tt':x[:,0]**2,'xx':x[:,1]**2,'yy':x[:,2]**2,
            'tx':x[:,0]*x[:,1],'ty':x[:,0]*x[:,2],'xy':x[:,1]*x[:,2],
            'exp':np.exp(x.sum(axis=1))}
    targets={'constant':0.,'t':0.,'x':0.,'y':0.,'tt':-2.,'xx':2.,'yy':2.,'tx':0.,'ty':0.,'xy':0.,'exp':1.}
    response={k:dict(value=float(core.apply(s,v)),target=targets[k]) for k,v in fields.items()}
    assert response['constant']['value']==0
    return dict(status='ok',metric=metric,metric_error=experiment.relative_error(metric,experiment.ETA),
                lorentz_signature=bool(experiment.signature(metric)),linear_response=linear,
                affine_drift=float(s['tau_m']*np.linalg.norm(linear)/np.sqrt(3)),
                dimensional_affine_norm=float(np.linalg.norm(linear)),fields=response,algebra_pass=True)


def run_cloud(rho,seed,cfg,relabel=False):
    tick=time.monotonic();z,relation,marks,bottom,top=experiment.sprinkle(rho,seed)
    g=core.Poset(relation,marks);base=estimator.neighborhood(g,rho,bottom,top,cfg);c=cfg['coefficient_C']
    stencils={'raw':base,'volume_shell':weighting.reweight(g,base,rho,c),
              'volume_both':weighting.reweight(g,base,rho,c,True)}
    if base['status']=='ok':
        root=z[base['root']];points=set(base['temporal'])|{b for s in base['sides'] for b in s['selected']}
        times={b:float(experiment.proper(z[b]-root)) for b in points}
        for both,name in [(False,'oracle_shell'),(True,'oracle_both')]:
            stencils[name]=weighting.assemble(base,marks,c,times,both)
        diagnostics=diagnose(z[base['temporal']]-root,[z[s['selected']]-root for s in base['sides']],
                             z[[s['reference'] for s in base['sides']]]-root,base['tau_n'],base['tau_m'],c)
        for name,variant in [('raw','raw'),('oracle_shell','S'),('oracle_both','TS')]:
            np.testing.assert_allclose(core.metric_outer(stencils[name],z-root),diagnostics['variants'][variant]['metric'],atol=1e-10,rtol=1e-10)
    else:
        stencils.update(oracle_shell=base,oracle_both=base);times={}
    arms={}
    for name,s in stencils.items():
        row=dict(status=s['status'],evaluation=evaluate(s,z))
        if s['status']=='ok':row.update(support=s['support'],weights=s['weights'])
        if 'interval_times' in s:
            row['interval_times']=s['interval_times']
            if s['status']=='ok':
                shell={b for side in s['sides'] for b in side['selected']}
                ratios=[q['time']/times[q['point']] for q in s['interval_times'] if q['point'] in shell]
                counts=[q['interior_count'] for q in s['interval_times'] if q['point'] in shell]
                row['shell_time_quality']=dict(mean_ratio=float(np.mean(ratios)),relative_mse=float(np.mean((np.array(ratios)-1)**2)),minimum_count=min(counts),mean_count=float(np.mean(counts)))
        arms[name]=row
    passed=relabel_check(g,base,rho,c,seed) if relabel else None
    selection={k:base[k] for k in ['status','root','chain','n','m','tau_n','tau_m','temporal'] if k in base}
    if 'sides' in base:selection['sides']=[dict(reference=s['reference'],selected=s['selected']) for s in base['sides']]
    return dict(rho=rho,seed=seed,poisson_count=len(z)-2,selection=selection,arms=arms,
                coordinates_sha256=hashlib.sha256(z.tobytes()).hexdigest(),relation_sha256=hashlib.sha256(relation.tobytes()).hexdigest(),
                marks_sha256=hashlib.sha256(marks.tobytes()).hexdigest(),relabel_pass=passed,
                oracle_moment_identity_pass=base['status']=='ok',seconds=time.monotonic()-tick)


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
                row=run_cloud(rho,seed,cfg,relabel=j==0);name=f'rho-{rho}-seed-{seed}.json';data=encode(row)
                (a.output/name).write_text(data);e['records'].append(dict(file=name,sha256=hashlib.sha256(data.encode()).hexdigest()));save()
                print(json.dumps(dict(rho=rho,seed=seed,seconds=round(row['seconds'],2),status={k:v['status'] for k,v in row['arms'].items()})),flush=True)
                if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024>contract['memory_budget_mib']:raise MemoryError('fixed memory budget exhausted')
        e['status']='COMPLETE'
    except (TimeoutError,MemoryError) as error:e.update(status='BUDGET_HOLD',reason=str(error))
    except Exception as error:
        e.update(status='ERROR',reason=repr(error));raise
    finally:
        signal.alarm(0);e.update(seconds=time.monotonic()-start,peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024);save()
    if e['status']!='COMPLETE':raise SystemExit(2)

if __name__=='__main__':main()
