"""SPDX-License-Identifier: Apache-2.0"""
import argparse
import gzip
import json
import os
import resource
import signal
import subprocess
import time
import numpy as np
import scipy
from ca_common import HERE,ROOT,cfg,history,model,source_check,sha,encode,write
from ca_model import predict,evaluate

def main():
    parser=argparse.ArgumentParser();parser.add_argument('worker',type=int,choices=range(4));args=parser.parse_args()
    c=cfg();f=source_check();head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head==f['commit']
    dest=HERE/f'results/worker-{args.worker}';assert not dest.exists(),'Refuse replacement execution.'
    rows=history();frozen=model();dest.mkdir(parents=True);start=time.monotonic()
    assigned=list(range(args.worker,len(rows),c['workers']))
    execution=dict(status='RUNNING',worker=args.worker,source_commit=head,assigned_indices=assigned,records=[],
        versions=dict(python=os.sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__),
        started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
    def save():
        execution['seconds']=time.monotonic()-start;execution['peak_mib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
        write(dest/'execution.json',execution)
    def timeout(*args):raise TimeoutError('fixed wall budget')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(c['wall_seconds_per_worker']);save()
    try:
        for index in assigned:
            row=rows[index];p=predict(row['cloud']['intrinsic'],row['cloud']['observed_order'],frozen)
            seal=sha(encode(p).encode());evaluation=evaluate(row,p,frozen);assert sha(encode(p).encode())==seal
            record=dict(index=index,historical_phase=row['phase'],historical_index=row['index'],seed=row['seed'],prediction=p,prediction_seal=seal,evaluation=evaluation)
            name=f'cloud-{index:03d}.json.gz';raw=gzip.compress(encode(record).encode(),compresslevel=9,mtime=0)
            with (dest/name).open('xb') as out:out.write(raw)
            execution['records'].append(dict(file=name,sha256=sha(raw)));save()
            print(json.dumps(dict(worker=args.worker,index=index,status=evaluation['status'],seconds=round(execution['seconds'],2))),flush=True)
            if execution['peak_mib']>c['memory_mib_per_worker']:raise MemoryError('fixed RSS budget')
        execution['status']='COMPLETE'
    except Exception as exc:execution.update(status='HOLD',reason=repr(exc));raise
    finally:signal.alarm(0);save()
if __name__=='__main__':main()
