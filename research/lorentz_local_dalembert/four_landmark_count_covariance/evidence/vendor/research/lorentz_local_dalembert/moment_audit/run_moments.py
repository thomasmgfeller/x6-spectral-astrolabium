"""Bounded paired moment diagnosis with no target-informed decisions."""
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
from moment_common import HERE,ROOT,core,estimator,experiment,oracle_cap,encode,config,sources
from moments import diagnose
from moment_controls import check


def run_cloud(rho,seed,cfg):
    start=time.monotonic()
    z,relation,marks,bottom,top=experiment.sprinkle(rho,seed)
    g=core.Poset(relation,marks)
    original=estimator.neighborhood(g,rho,bottom,top,cfg)
    stencils={'balanced64':original,'oracle_cap':oracle_cap(z,marks,original,cfg)}
    arms={}
    for name,s in stencils.items():
        row=dict(status=s['status'],root=s['root'],n=s['n'],m=s['m'],tau_n=s['tau_n'],tau_m=s['tau_m'])
        if 'sides' in s:
            row.update(temporal=s['temporal'],references=[q['reference'] for q in s['sides']],selected=[q['selected'] for q in s['sides']])
        if s['status']=='ok':
            root=z[s['root']]
            d=diagnose(z[s['temporal']]-root,[z[q['selected']]-root for q in s['sides']],
                       z[row['references']]-root,s['tau_n'],s['tau_m'],cfg['coefficient_C'])
            raw=core.metric_outer(s,z-root)
            np.testing.assert_allclose(d['variants']['raw']['metric'],raw,atol=1e-10,rtol=1e-10)
            row.update(diagnosis=d,raw_identity_pass=True)
        arms[name]=row
    return dict(rho=rho,seed=seed,poisson_count=len(z)-2,
                coordinates_sha256=hashlib.sha256(z.tobytes()).hexdigest(),
                relation_sha256=hashlib.sha256(relation.tobytes()).hexdigest(),
                marks_sha256=hashlib.sha256(marks.tobytes()).hexdigest(),
                arms=arms,seconds=time.monotonic()-start)


def main():
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['development','test'],required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();contract,cfg=config()
    if a.output.exists(): raise SystemExit('Refusing to overwrite existing output')
    sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();hashes=sources()
    if a.mode=='test':
        for path,digest in hashes.items():
            data=subprocess.check_output(['git','show',sha+':'+path],cwd=ROOT)
            assert hashlib.sha256(data).hexdigest()==digest,'unfrozen source '+path
    controls=check();a.output.mkdir(parents=True)
    execution=dict(mode=a.mode,source_commit=sha,source_sha256=hashes,numpy=np.__version__,scipy=scipy.__version__,
                   controls=controls,records=[],status='RUNNING')
    save=lambda:(a.output/'execution.json').write_text(json.dumps(execution,indent=2)+'\n')
    save();start=time.monotonic()
    def timeout(signum,frame): raise TimeoutError('fixed wall budget exhausted')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(contract['wall_budget_seconds'])
    try:
        for i,rho in enumerate(contract['densities']):
            seeds=contract['development_seeds'] if a.mode=='development' else [contract['test_seed_base']+100*i+j for j in range(contract['test_replicates_per_density'])]
            for seed in seeds:
                row=run_cloud(rho,seed,cfg);name=f'rho-{rho}-seed-{seed}.json';data=encode(row)
                (a.output/name).write_text(data)
                execution['records'].append(dict(file=name,sha256=hashlib.sha256(data.encode()).hexdigest()));save()
                print(json.dumps(dict(rho=rho,seed=seed,status={k:v['status'] for k,v in row['arms'].items()},seconds=round(row['seconds'],2))),flush=True)
                if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024>contract['memory_budget_mib']: raise MemoryError('fixed memory budget exhausted')
        execution['status']='COMPLETE'
    except (TimeoutError,MemoryError) as error: execution.update(status='BUDGET_HOLD',reason=str(error))
    except Exception as error:
        execution.update(status='ERROR',reason=repr(error));raise
    finally:
        signal.alarm(0);execution.update(seconds=time.monotonic()-start,peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024);save()
    if execution['status']!='COMPLETE': raise SystemExit(2)

if __name__=='__main__': main()
