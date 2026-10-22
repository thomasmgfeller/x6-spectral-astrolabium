"""Run all fixed ablations and new conditional count experiments.
SPDX-License-Identifier: Apache-2.0
"""
import argparse,gzip,hashlib,json,platform,signal,time
from pathlib import Path
import numpy as np
import scipy
from models import PRIOR,estimate
from fit import estimate as old_estimate
from inference import measurement
from run import encode,save

HERE=Path(__file__).resolve().parent
def verify_freeze():
    f=json.loads((HERE/'freeze.json').read_text())
    for name,digest in f['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name

def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['development','conditional']);args=ap.parse_args()
    verify_freeze();c=json.loads((HERE/'contract.json').read_text());oldc=json.loads((PRIOR/'contract.json').read_text());oldc['count_seed_tag']=c['conditional_count_seed_tag']
    from simulation import counting_cloud
    begin=time.monotonic();records=[]
    def alarm(*_):raise TimeoutError('fixed 1200-second runner budget')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(1200)
    for index in c['selected_indices']:
        raw=(PRIOR/f'results/cloud-{index:02d}.json.gz').read_bytes();old=json.loads(gzip.decompress(raw));source_hash=hashlib.sha256(raw).hexdigest()
        p=old['selection']['fourth']['packet'];truth=json.loads((PRIOR/f'results/truth/cloud-{index:02d}.json').read_text());assert truth['inference_sha256']==source_hash
        private=dict(points=np.array(truth['points']),ids=truth['ids']);row=dict(index=index,source_sha256=source_hash,replicates=[]);start=time.monotonic()
        for rep in range(c['replicates']):
            if args.mode=='development':
                previous=old['replicates'][rep];obs=previous['observed']
                arms=dict(four=previous['baseline']['four'],old_poisson=previous['fit'])
                for arm in c['development_arms']:arms[arm]=estimate(p,obs['counts'],obs['overlaps'],c['count_density'],c['fit'],arm)
            else:
                obs=counting_cloud(private,p,old['seed'],rep,oldc)
                oldfour=measurement(p,obs['counts'],obs['overlaps'],c['count_density'])['four']
                for key in ['weight_jacobian','weight_covariance','independent_counts_negative_control']:oldfour.pop(key,None)
                arms=dict(four=oldfour,old_poisson=old_estimate(p,obs['counts'],c['count_density'],c['fit']),full_gls=estimate(p,obs['counts'],obs['overlaps'],c['count_density'],c['fit'],'full_gls'))
            rr=dict(replicate=rep,arms=arms)
            if args.mode=='conditional':rr['observed']=obs
            row['replicates'].append(rr)
        row['seconds']=time.monotonic()-start
        digest=save(HERE/f'{args.mode}/cloud-{index:02d}.json.gz',row)
        # Write the new record before its separate evaluation-truth binding.
        save(HERE/f'{args.mode}/truth/cloud-{index:02d}.json',dict(index=index,points=truth['points'],ids=truth['ids'],inference_sha256=digest,source_inference_sha256=source_hash))
        rec=dict(index=index,seconds=row['seconds'],primary={k:v['status'] for k,v in row['replicates'][0]['arms'].items()},full_gls_qualified=sum(r['arms']['full_gls'].get('qualified',False) for r in row['replicates']))
        records.append(rec);print(json.dumps(rec),flush=True)
    signal.alarm(0);save(HERE/f'{args.mode}/execution.json',dict(status='COMPLETE',seconds=time.monotonic()-begin,records=records,versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__)))

if __name__=='__main__':main()
