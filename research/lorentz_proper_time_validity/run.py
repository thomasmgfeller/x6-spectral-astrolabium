"""Execute the publicly frozen deterministic grid into a new directory."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import time
import numpy as np
import scipy
from core import evaluate

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FROZEN=['contract.json','DERIVATION.md','core.py','run.py','verify.py','requirements.txt']


def dump(path,obj):
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')


def run(output,source_ref):
    c=json.loads((HERE/'contract.json').read_text())
    hashes={}
    for f in FROZEN:
        raw=(HERE/f).read_bytes()
        pinned=subprocess.check_output(['git','show',f'{source_ref}:research/lorentz_proper_time_validity/{f}'],cwd=ROOT)
        if raw!=pinned:
            raise RuntimeError('frozen source mismatch: '+f)
        hashes[f]=hashlib.sha256(raw).hexdigest()
    for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
        if os.environ.get(key)!='1':
            raise RuntimeError(key+' must be 1 before Python starts')
    resource.setrlimit(resource.RLIMIT_AS,(c['resources']['address_space_bytes'],c['resources']['address_space_bytes']))
    resource.setrlimit(resource.RLIMIT_CPU,(c['resources']['wall_seconds'],c['resources']['wall_seconds']))
    output.mkdir(parents=True,exist_ok=False)
    started=datetime.now(timezone.utc).isoformat()
    tic=time.monotonic()
    rows=evaluate(c)
    elapsed=time.monotonic()-tic
    if elapsed>c['resources']['wall_seconds']:
        raise RuntimeError('runtime budget exceeded; do not qualify output')
    groups={}
    for r in rows:
        key=(r['model'],r['d'],r['planning_theta'],r['parameter'],r['interval'])
        groups.setdefault(key,[]).append(r)
    planning=[]
    for key,group in groups.items():
        passing=[r['m'] for r in group if r['status']=='MEETS_DECLARED_GRID_CRITERIA']
        planning.append(dict(model=key[0],d=key[1],planning_theta=key[2],parameter=key[3],interval=key[4],
                             first_passing_grid_m=min(passing) if passing else None,
                             passing_grid_counts=passing,in_assumed_class=group[0]['in_assumed_class'],
                             asymptotic_interval_relative_radius=group[0]['asymptotic_interval_relative_radius']))
    dump(output/'grid.json',rows)
    dump(output/'planning.json',planning)
    dump(output/'execution.json',dict(source_commit=source_ref,started_utc=started,
         elapsed_seconds=elapsed,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,
         rows=len(rows),frozen_sha256=hashes,evidence='DETERMINISTIC_MODEL_CALCULATION_NOT_NEW_MEASUREMENTS'))
    dump(output/'hashes.json',{f:hashlib.sha256((output/f).read_bytes()).hexdigest() for f in ['grid.json','planning.json','execution.json']})
    print(json.dumps(dict(status='GRID_CALCULATED_NOT_YET_INDEPENDENTLY_CHECKED',rows=len(rows),elapsed_seconds=elapsed)))


if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--output',type=Path,required=True)
    a.add_argument('--source-ref',required=True)
    ns=a.parse_args()
    run(ns.output,ns.source_ref)
