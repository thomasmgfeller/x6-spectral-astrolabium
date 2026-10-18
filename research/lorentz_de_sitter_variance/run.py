"""Prospective variance-certificate comparison; fresh campaign conditional on gain."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import argparse,platform,resource,signal,time
from datetime import datetime,timezone
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from moments import certificate
from support import contract,dump,sources,seed,geometry,relation_hash,digest
from analysis import planning,analyze

def run(out,ref):
    tic=time.monotonic();start=datetime.now(timezone.utc).isoformat();source_hashes=sources(ref)
    out.mkdir(parents=True,exist_ok=False)
    dump(out/'mathematics.json',certificate())
    plan=planning();dump(out/'planning.json',plan);print(plan['status'],flush=True)
    rows=[]
    if plan['fresh_gate']:
        for j,cell in enumerate(contract()['fresh_cells']):
            all_counts=[]
            for begin in range(0,cell['clouds'],contract()['storage_block']):
                end=min(cell['clouds'],begin+contract()['storage_block']);counts=[];hashes=[]
                for r in range(begin,end):
                    rng=np.random.Generator(np.random.PCG64(seed(f'holdout/h{j}/r{r}')))
                    x,_=geometry.sample(rng,128,{'h':float(Q(cell['h']))});c=geometry.relation(x)
                    counts.append(int(c.sum()));hashes.append(relation_hash(c))
                np.savez_compressed(out/f'raw-{j}-{begin}.npz',c2=np.array(counts,dtype=np.int64),relation_sha256=np.array(hashes,dtype='S64'))
                all_counts.extend(counts);print(f'h={cell["h"]}: {end}/{cell["clouds"]}',flush=True)
            result=analyze(np.array(all_counts,dtype=np.int64),cell);dump(out/f'groups-{j}.json.gz',result);rows.extend(result['rows'])
    dump(out/'summary.json',dict(status=plan['status'],fresh_clouds=sum(c['clouds'] for c in contract()['fresh_cells']) if plan['fresh_gate'] else 0,rows=rows))
    dump(out/'execution.json',dict(started_utc=start,finished_utc=datetime.now(timezone.utc).isoformat(),source_ref=ref,
         source_sha256=source_hashes,python=platform.python_version(),numpy=np.__version__,seconds=time.monotonic()-tic,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    dump(out/'hashes.json',{p.name:digest(p) for p in sorted(out.iterdir())})
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-ref',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3));signal.alarm(600);run(a.output,a.source_ref)
