"""SPDX-License-Identifier: Apache-2.0"""
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
from gc_common import HERE,ROOT,cfg,ec,source_check,model,run_cloud,encode,sha,write
from gc_model import predict,evaluate

def main():
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['calibration','test'])
    parser.add_argument('worker',type=int,choices=range(4));args=parser.parse_args()
    c=cfg();freeze=source_check();dest=HERE/f'results/{args.phase}/worker-{args.worker}'
    assert not dest.exists(),'Refuse to replace execution.'
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    if args.phase=='calibration':assert head==freeze['commit']
    else:
        path=HERE/'frozen_calibration.json';raw=path.read_bytes()
        assert subprocess.check_output(['git','show',head+':'+str(path.relative_to(ROOT))],cwd=ROOT)==raw
        assert json.loads(raw)['status']=='FROZEN'
    tasks=json.loads((HERE/'seed_schedule.json').read_text())[args.phase][args.worker::c['workers']]
    jf,oc,guards,estimator_cfg=ec.config();frozen=model();dest.mkdir(parents=True)
    start=time.monotonic();execution=dict(status='RUNNING',phase=args.phase,worker=args.worker,
        source_commit=freeze['commit'],execution_commit=head,
        started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),records=[],
        versions=dict(python=os.sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__),
        assigned_indices=[s['index'] for s in tasks])
    def save():
        execution['seconds']=time.monotonic()-start
        execution['peak_mib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
        write(dest/'execution.json',execution)
    def timeout(*args):raise TimeoutError('fixed wall budget')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(c['wall_seconds_per_worker']);save()
    try:
        for spec in tasks:
            row=run_cloud(c['rho'],spec['geometry_seed'],jf,oc,guards,estimator_cfg)
            prediction=predict(row['intrinsic'],row['observed_order'],frozen)
            seal=sha(encode(prediction).encode());points=None
            if prediction['status']=='COMPLETE':
                z=ec.coordinates_only(c['rho'],spec['geometry_seed'],oc)
                assert ec.digest(z)==row['coordinates_sha256']
                selected=row['selection']['selected'];ids=[selected['root']]+selected['support']
                points=(z[ids]-z[selected['root']]).tolist();del z
            evaluation=evaluate(row['intrinsic'],row['observed_order'],prediction,points)
            assert sha(encode(prediction).encode())==seal
            record=dict(index=spec['index'],phase=args.phase,seed=spec['geometry_seed'],cloud=row,
                prediction=prediction,prediction_seal=seal,true_support_points=points,evaluation=evaluation)
            name=f"cloud-{spec['index']:02d}.json.gz"
            raw=gzip.compress(encode(record).encode(),compresslevel=9,mtime=0)
            with (dest/name).open('xb') as f:f.write(raw)
            execution['records'].append(dict(file=name,sha256=sha(raw)));save()
            print(json.dumps(dict(phase=args.phase,worker=args.worker,index=spec['index'],
                status=evaluation['status'],seconds=round(execution['seconds'],2))),flush=True)
            if execution['peak_mib']>c['memory_mib_per_worker']:raise MemoryError('fixed RSS budget')
            del row,prediction,evaluation,record;gc.collect()
        execution['status']='COMPLETE'
    except Exception as exc:
        execution.update(status='HOLD',reason=repr(exc));raise
    finally:
        signal.alarm(0);save()

if __name__=='__main__':main()
