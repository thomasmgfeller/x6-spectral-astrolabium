import argparse
import gzip
import hashlib
import json
import platform
import resource
import signal
import time
from pathlib import Path
import numpy as np
import scipy
from simulation import selection_cloud,counting_cloud
from inference import measurement

HERE=Path(__file__).resolve().parent

def encode(data):
    def native(v):
        if isinstance(v,np.ndarray):return v.tolist()
        if isinstance(v,np.generic):return v.item()
        raise TypeError(type(v).__name__)
    return json.dumps(data,default=native,separators=(',',':'),allow_nan=False).encode()

def save_new(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    raw=encode(data)
    if path.suffix=='.gz':raw=gzip.compress(raw,mtime=0)
    with path.open('xb') as f:f.write(raw)
    return hashlib.sha256(raw).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('worker',type=int,choices=[0,1]);args=ap.parse_args()
    contract=json.loads((HERE/'contract.json').read_text())
    freeze=json.loads((HERE/'freeze.json').read_text())
    for name,expected in freeze['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==expected,name
    root=HERE/'results';root.mkdir(exist_ok=True)
    execution=root/f'worker-{args.worker}.json'
    assert not execution.exists(),'no execution replacement'
    status=dict(worker=args.worker,status='RUNNING',started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
                versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),records=[])
    start=time.monotonic()
    def checkpoint():
        status.update(seconds=time.monotonic()-start,peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
        execution.write_bytes(encode(status))
    def timeout(*args):raise TimeoutError('fixed worker time budget')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(contract['worker_seconds']);checkpoint()
    try:
        for index in range(args.worker,contract['clouds'],contract['workers']):
            seed=contract['selection_seed_base']+index;begun=time.monotonic()
            try:
                selection,private=selection_cloud(seed,contract)
                seal=hashlib.sha256(encode(selection)).hexdigest()
                row=dict(index=index,seed=seed,selection=selection,selection_seal=seal,replicates=[])
                if private is not None:
                    packet=selection['fourth']['packet']
                    for rep in range(contract['count_replicates']):
                        observed=counting_cloud(private,packet,seed,rep,contract)
                        inferred=measurement(packet,observed['counts'],observed['overlaps'],contract['count_density'],contract['minimum_measurement_count'])
                        f=inferred['four']
                        if rep!=0:
                            for key in ['weight_jacobian','weight_covariance','independent_counts_negative_control']:
                                f.pop(key,None)
                        row['replicates'].append(dict(replicate=rep,observed=observed,inference=inferred))
                    assert hashlib.sha256(encode(selection)).hexdigest()==seal
                row['seconds']=time.monotonic()-begun
                record_hash=save_new(root/f'cloud-{index:02d}.json.gz',row)
                # Record weights and seal before exporting evaluation truth.
                if private is not None:
                    save_new(root/f'truth/cloud-{index:02d}.json',dict(index=index,points=private['points'],ids=private['ids'],inference_sha256=record_hash))
                status['records'].append(dict(index=index,status=selection['status'],file=f'cloud-{index:02d}.json.gz',sha256=record_hash))
                print(json.dumps(dict(index=index,status=selection['status'],seconds=round(row['seconds'],2),
                      primary=row['replicates'][0]['inference']['four']['status'] if row['replicates'] else None,
                      qualified=row['replicates'][0]['inference']['four'].get('qualified') if row['replicates'] else None)),flush=True)
            except (TimeoutError,MemoryError):raise
            except Exception as exc:
                error=dict(index=index,seed=seed,status='ERROR',reason=repr(exc))
                save_new(root/f'cloud-{index:02d}-error.json',error);status['records'].append(error)
                print(json.dumps(error),flush=True)
            checkpoint()
            if status['peak_mib']>contract['worker_memory_mib']:raise MemoryError('fixed worker memory budget')
        status['status']='COMPLETE'
    except Exception as exc:
        status.update(status='BUDGET_OR_EXECUTION_HOLD',reason=repr(exc));raise
    finally:
        signal.alarm(0);checkpoint()

if __name__=='__main__':main()
