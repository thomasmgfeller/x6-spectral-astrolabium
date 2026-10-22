"""Frozen bounded campaign; all inference sealed before exporting truth.
SPDX-License-Identifier: Apache-2.0
"""
import argparse, gzip, hashlib, json, platform, resource, signal, time
from pathlib import Path
import numpy as np
import scipy
from fit import estimate, SOURCE
from inference import measurement

HERE=Path(__file__).resolve().parent
def encode(data):
    def native(x):
        if isinstance(x,np.ndarray):return x.tolist()
        if isinstance(x,np.generic):return x.item()
        raise TypeError(type(x).__name__)
    return json.dumps(data,default=native,allow_nan=False,separators=(',',':')).encode()

def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True);raw=encode(data)
    if path.suffix=='.gz':raw=gzip.compress(raw,mtime=0)
    with path.open('xb') as f:f.write(raw)
    return hashlib.sha256(raw).hexdigest()

def frozen():
    freeze=json.loads((HERE/'freeze.json').read_text())
    for name,h in freeze['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name

def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['archive','fresh']);ap.add_argument('--worker',type=int,choices=[0,1],default=0);a=ap.parse_args()
    frozen();c=json.loads((HERE/'contract.json').read_text());root=HERE/('archive' if a.mode=='archive' else 'results')
    root.mkdir(exist_ok=True);execution=root/f'worker-{a.worker}.json';assert not execution.exists(),'no replacement'
    status=dict(status='RUNNING',mode=a.mode,worker=a.worker,started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),records=[])
    start=time.monotonic()
    def checkpoint():
        status.update(seconds=time.monotonic()-start,peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
        execution.write_bytes(encode(status))
    def timeout(*_):raise TimeoutError('fixed worker budget')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(c['worker_seconds']);checkpoint()
    if a.mode=='fresh':
        from simulation import selection_cloud,counting_cloud
    try:
        indices=range(c['clouds']) if a.mode=='archive' else range(a.worker,c['clouds'],c['workers'])
        for index in indices:
            begun=time.monotonic();private=None
            if a.mode=='archive':
                raw=(SOURCE/f'results/cloud-{index:02d}.json.gz').read_bytes();old=json.loads(gzip.decompress(raw))
                selection=old['selection'];seed=old['seed']
            else:
                seed=c['selection_seed_base']+index
                selection,private=selection_cloud(seed,c)
            seal=hashlib.sha256(encode(selection)).hexdigest()
            row=dict(index=index,seed=seed,selection=selection,selection_seal=seal,replicates=[])
            if selection['status']=='SELECTED':
                packet=selection['fourth']['packet']
                for rep in range(1 if a.mode=='archive' else c['count_replicates']):
                    observed=old['replicates'][rep]['observed'] if a.mode=='archive' else counting_cloud(private,packet,seed,rep,c)
                    baseline=measurement(packet,observed['counts'],observed['overlaps'],c['count_density'],c['minimum_measurement_count'])
                    # Large analytic matrices remain in source; not needed by this comparison.
                    for key in ['weight_jacobian','weight_covariance','independent_counts_negative_control']:
                        baseline['four'].pop(key,None)
                    fitted=estimate(packet,observed['counts'],c['count_density'],c['fit'])
                    row['replicates'].append(dict(replicate=rep,observed=observed,baseline=baseline,fit=fitted))
                assert hashlib.sha256(encode(selection)).hexdigest()==seal
            row['seconds']=time.monotonic()-begun
            h=save(root/f'cloud-{index:02d}.json.gz',row)
            if row['replicates']:
                if a.mode=='archive':
                    truth=json.loads((SOURCE/f'results/truth/cloud-{index:02d}.json').read_text())
                    assert truth['inference_sha256']==hashlib.sha256(raw).hexdigest()
                    private=dict(points=truth['points'],ids=truth['ids'])
                save(root/f'truth/cloud-{index:02d}.json',dict(index=index,points=private['points'],ids=private['ids'],inference_sha256=h))
            rec=dict(index=index,selection=selection['status'],seconds=row['seconds'],sha256=h)
            if row['replicates']:
                rec.update(fit=row['replicates'][0]['fit']['status'],fit_qualified=row['replicates'][0]['fit']['qualified'],four_qualified=row['replicates'][0]['baseline']['four'].get('qualified',False),fit_repeats=sum(r['fit']['qualified'] for r in row['replicates']))
            status['records'].append(rec);print(json.dumps(rec),flush=True);checkpoint()
            if status['peak_mib']>c['worker_memory_mib']:raise MemoryError('worker memory budget')
        status['status']='COMPLETE'
    except Exception as exc:
        status.update(status='BUDGET_OR_EXECUTION_HOLD',reason=repr(exc));raise
    finally:
        signal.alarm(0);checkpoint()

if __name__=='__main__':main()
