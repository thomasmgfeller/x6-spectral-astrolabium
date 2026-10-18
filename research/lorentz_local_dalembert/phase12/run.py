"""Fixed-seed development / held-out execution, with an explicit budget."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import signal
import subprocess
import time
import numpy as np
import scipy
import core
import experiment


def plain(value):
    if isinstance(value,np.ndarray): return value.tolist()
    if isinstance(value,np.generic): return value.item()
    raise TypeError(type(value).__name__)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mode',choices=['development','test'],required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--density',type=int,help='Development only')
    args=parser.parse_args()
    cfg=json.loads((core.HERE/'contract.json').read_text())
    if args.mode=='test' and args.density: raise SystemExit('No selective held-out runs')
    if args.output.exists(): raise SystemExit('Output exists; use a new directory')
    args.output.mkdir(parents=True)
    source={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in core.HERE.iterdir() if p.suffix in ['.py','.cpp','.json','.md'] and p.is_file()}
    if args.mode=='test':
        for name in source:
            path=core.HERE/name
            tracked=subprocess.check_output(['git','show','HEAD:'+str(path.relative_to(core.HERE.parents[2]))],cwd=core.HERE)
            if tracked!=path.read_bytes(): raise SystemExit('Held-out source differs from HEAD: '+name)
    execution=dict(mode=args.mode,source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=core.HERE,text=True).strip(),
                   source_sha256=source,numpy=np.__version__,scipy=scipy.__version__,records=[],status='RUNNING')
    (args.output/'execution.json').write_text(json.dumps(execution,indent=2)+'\n')
    start=time.monotonic()
    def timeout(signum,frame): raise TimeoutError('fixed wall budget exhausted')
    signal.signal(signal.SIGALRM,timeout)
    signal.alarm(cfg['wall_budget_seconds'])
    try:
        for i,rho in enumerate(cfg['densities']):
            if args.density and rho!=args.density: continue
            seeds=cfg['development_seeds'] if args.mode=='development' else [cfg['test_seed_base']+100*i+j for j in range(cfg['test_replicates_per_density'])]
            for j,seed in enumerate(seeds):
                record=experiment.run_cloud(rho,seed,cfg,relabel=(j==0))
                name=f'rho-{rho}-seed-{seed}.json'
                data=json.dumps(record,default=plain,allow_nan=False,separators=(',',':'))+'\n'
                (args.output/name).write_text(data)
                execution['records'].append(dict(file=name,sha256=hashlib.sha256(data.encode()).hexdigest()))
                print(json.dumps(dict(rho=rho,seed=seed,n=record['poisson_count'],seconds=round(record['seconds'],3),
                      status=record['evaluation']['status'],population=record['evaluation'].get('populations'))),flush=True)
                if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024>cfg['memory_budget_mib']:
                    raise MemoryError('fixed memory budget exhausted')
        execution['status']='COMPLETE'
    except (TimeoutError,MemoryError) as error:
        execution['status']='BUDGET_HOLD'; execution['reason']=str(error)
    finally:
        signal.alarm(0)
        execution['seconds']=time.monotonic()-start
        execution['peak_mib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
        (args.output/'execution.json').write_text(json.dumps(execution,indent=2)+'\n')
    if execution['status']!='COMPLETE': raise SystemExit(2)

if __name__=='__main__': main()
