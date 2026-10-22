"""Frozen paired fresh-A experiment. No replacement or B-driven reselection.
SPDX-License-Identifier: Apache-2.0
"""
import argparse
import hashlib
import json
import platform
import resource
import signal
import time
import numpy as np
import scipy
from eb_common import HERE, encode, save, frozen
from inference import measurement
from simulation_pair import selection_pair, counting_cloud

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('worker',type=int,choices=[0,1]); args=ap.parse_args()
    frozen(); c=json.loads((HERE/'contract.json').read_text()); start=time.monotonic()
    execution=HERE/f'results/worker-{args.worker}.json'; assert not execution.exists(), 'no replacements'
    execution.parent.mkdir(exist_ok=True)
    status=dict(status='RUNNING',worker=args.worker,started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),records=[],
                versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__))
    def checkpoint():
        status.update(seconds=time.monotonic()-start,peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
        execution.write_bytes(encode(status))
    def alarm(*_): raise TimeoutError('fixed worker budget')
    signal.signal(signal.SIGALRM,alarm); signal.alarm(c['worker_seconds']); checkpoint()
    try:
        for index in range(args.worker,c['clouds'],c['workers']):
            begun=time.monotonic(); seed=c['selection_seed_base']+index
            selection,private=selection_pair(seed,c); seal=hashlib.sha256(encode(selection)).hexdigest()
            row=dict(index=index,seed=seed,selection=selection,selection_seal=seal,replicates=[])
            if private:
                for rep in range(c['count_replicates']):
                    rr=dict(replicate=rep,arms={})
                    for arm,pp in private.items():
                        packet=selection['arms'][arm]['packet']; observed=counting_cloud(pp,packet,seed,rep,c)
                        measured=measurement(packet,observed['counts'],observed['overlaps'],c['count_density'],c['minimum_measurement_count'])
                        # Preserve the full propagated covariance and negative control.
                        rr['arms'][arm]=dict(observed=observed,measurement=measured)
                    if len(rr['arms'])==2:
                        assert rr['arms']['legacy']['observed']['coordinates_sha256']==rr['arms']['candidate']['observed']['coordinates_sha256']
                    row['replicates'].append(rr)
            assert hashlib.sha256(encode(selection)).hexdigest()==seal
            row['seconds']=time.monotonic()-begun
            h=save(HERE/f'results/cloud-{index:02d}.json.gz',row)
            if private: save(HERE/f'results/truth/cloud-{index:02d}.json',dict(index=index,arms=private,inference_sha256=h))
            rec=dict(index=index,seconds=row['seconds'],selection={a:s['status'] for a,s in selection['arms'].items()},sha256=h)
            if row['replicates']: rec['primary']={a:dict(status=r['measurement']['four']['status'],qualified=r['measurement']['four'].get('qualified',False)) for a,r in row['replicates'][0]['arms'].items()}
            status['records'].append(rec); checkpoint(); print(json.dumps(rec),flush=True)
            if status['peak_mib']>c['worker_memory_mib']: raise MemoryError('fixed memory budget')
        status['status']='COMPLETE'
    except Exception as exc:
        status.update(status='BUDGET_OR_EXECUTION_HOLD',reason=repr(exc)); raise
    finally:
        signal.alarm(0); checkpoint()

if __name__=='__main__': main()
