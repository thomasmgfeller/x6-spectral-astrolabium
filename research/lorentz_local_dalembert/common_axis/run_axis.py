"""Frozen common-axis trial; embedding access confined to oracle/evaluation."""
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
from axis_common import HERE,ROOT,core,estimator,experiment,encode,config,sources,weighting,evaluate
from axis_controls import check,cloud_controls
from assembly import rebuild
import selection

def reference_quality(s,z,chosen=None):
    if 'sides' not in s:return None
    a,b=s['temporal'];r=s['root'];u=z[b]-z[a];u=u/experiment.proper(u)
    values=[]
    for side in s['sides']:
        x=side['reference'];v=z[x]-z[r];q=float(experiment.proper(v))
        dt=float(v[0]*u[0]-v[1:]@u[1:]);h=(dt/q)**2-1
        values.append(dict(point=x,actual_h=h,rapidity=float(np.arcsinh(np.sqrt(max(0.,h)))),population=len(side['selected'])))
    out=dict(references=values,mean_rapidity=float(np.mean([v['rapidity'] for v in values])),
             mean_population=float(np.mean([v['population'] for v in values])))
    if chosen and chosen['status']=='ok':
        eligible=[v for side in chosen['sides'] for v in side['candidates'] if v['status']=='ok']
        picked=[next(v for v in side['candidates'] if v['point']==side['reference']) for side in chosen['sides']]
        out.update(eligible_candidates=len(eligible),negative_h_fraction=sum(v['h']<0 for v in eligible)/len(eligible),
                   chosen_negative_fraction=sum(v['h']<0 for v in picked)/2,
                   mean_h_bias=float(np.mean([v['h']-actual['actual_h'] for v,actual in zip(picked,values)])))
    return out


def run_cloud(rho,seed,cfg,controls=False):
    tick=time.monotonic();z,relation,marks,bottom,top=experiment.sprinkle(rho,seed)
    g=core.Poset(relation,marks);base=estimator.neighborhood(g,rho,bottom,top,cfg);c=cfg['coefficient_C']
    chosen=selection.select(g,base,rho)
    oracle=selection.choose_with_times(g,base,lambda a,b,n:float(experiment.proper(z[b]-z[a])))
    axis=rebuild(g,base,chosen,rho,cfg);exact=rebuild(g,base,oracle,rho,cfg)
    stencils={'raw':base,'volume_shell':weighting.reweight(g,base,rho,c),
              'axis_shell':weighting.reweight(g,axis,rho,c),'oracle_axis_shell':weighting.reweight(g,exact,rho,c)}
    arms={}
    for name,s in stencils.items():
        row=dict(status=s['status'],evaluation=evaluate(s,z))
        row['selection']={k:s[k] for k in ['root','n','m','tau_n','tau_m','temporal'] if k in s}
        if 'sides' in s:row['selection']['sides']=[dict(reference=side['reference'],selected=side['selected']) for side in s['sides']]
        if s['status']=='ok':row.update(support=s['support'],weights=s['weights'])
        if 'interval_times' in s:row['interval_times']=s['interval_times']
        if name in ['raw','volume_shell'] or (chosen if name=='axis_shell' else oracle)['status']=='ok':
            row['reference_quality']=reference_quality(s,z,chosen if name=='axis_shell' else oracle if name=='oracle_axis_shell' else None)
        arms[name]=row
    control=cloud_controls(g,base,rho,cfg,seed) if controls else None
    return dict(rho=rho,seed=seed,poisson_count=len(z)-2,base_status=base['status'],chain=base['chain'],
                reference_selection=dict(axis_shell=chosen,oracle_axis_shell=oracle),arms=arms,
                coordinates_sha256=hashlib.sha256(z.tobytes()).hexdigest(),relation_sha256=hashlib.sha256(relation.tobytes()).hexdigest(),
                marks_sha256=hashlib.sha256(marks.tobytes()).hexdigest(),cloud_controls=control,seconds=time.monotonic()-tick)


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
                row=run_cloud(rho,seed,cfg,controls=j==0);name=f'rho-{rho}-seed-{seed}.json';data=encode(row)
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
