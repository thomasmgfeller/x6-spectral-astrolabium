"""SPDX-License-Identifier: Apache-2.0
Four bounded independent workers. Save every outcome; never replace failures.
"""
import argparse
import gc
import gzip
import json
import os
import resource
import signal
import subprocess
import time
import numpy as np
import scipy
from ec_common import HERE,ROOT,cfg,config,source_check,models,prepare,coordinates_only,digest,encode,sha,write
from ec_measure import evaluate
from cg_cloud import run_cloud


def main():
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['calibration','test'])
    parser.add_argument('worker',type=int,choices=range(4));args=parser.parse_args()
    c=cfg();freeze=source_check()
    dest=HERE/f'results/{args.phase}/worker-{args.worker}'
    assert not dest.exists(),'Refuse to replace an execution.'
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    if args.phase=='test':
        calibration=(HERE/'frozen_calibration.json').read_bytes()
        assert subprocess.check_output(['git','show',head+':'+str((HERE/'frozen_calibration.json').relative_to(ROOT))],cwd=ROOT)==calibration
        assert json.loads(calibration)['status']=='FROZEN'
    schedule=json.loads((HERE/'seed_schedule.json').read_text())[args.phase]
    tasks=schedule[args.worker::c['workers']]
    jf,oc,guards,estimator_cfg=config(); frozen=models()
    dest.mkdir(parents=True)
    start=time.monotonic()
    execution=dict(status='RUNNING',phase=args.phase,worker=args.worker,source_commit=freeze['commit'],
        execution_commit=head,started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
        versions=dict(python=os.sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__),
        records=[],assigned_indices=[s['index'] for s in tasks])
    def save():
        execution['seconds']=time.monotonic()-start
        execution['peak_mib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
        write(dest/'execution.json',execution)
    def timeout(*args):raise TimeoutError('fixed wall budget')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(c['wall_seconds_per_worker']);save()
    try:
        for spec in tasks:
            row=run_cloud(c['rho'],spec['geometry_seed'],jf,oc,guards,estimator_cfg)
            p=prepare(row['intrinsic'],frozen)
            seal=sha(encode(p).encode())
            z=coordinates_only(c['rho'],spec['geometry_seed'],oc)
            assert digest(z)==row['coordinates_sha256']
            observed=evaluate(row,z,p,spec['noise_key'])
            assert sha(encode(p).encode())==seal
            record=dict(index=spec['index'],phase=args.phase,seed=spec['geometry_seed'],noise_key=spec['noise_key'],
                cloud=row,prepared=p,inference_seal=seal,evaluation=observed)
            name=f"cloud-{spec['index']:02d}.json.gz"
            raw=gzip.compress(encode(record).encode(),compresslevel=9,mtime=0)
            with (dest/name).open('xb') as f:f.write(raw)
            execution['records'].append(dict(file=name,sha256=sha(raw)))
            save()
            print(json.dumps(dict(phase=args.phase,worker=args.worker,index=spec['index'],
                 status=observed['status'],seconds=round(execution['seconds'],2))),flush=True)
            if execution['peak_mib']>c['memory_mib_per_worker']:raise MemoryError('fixed RSS budget')
            del row,z,p,observed,record;gc.collect()
        execution['status']='COMPLETE'
    except Exception as exc:
        execution.update(status='HOLD',reason=repr(exc));raise
    finally:
        signal.alarm(0);save()


if __name__=='__main__':main()
