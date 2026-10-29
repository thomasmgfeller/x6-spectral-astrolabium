"""Freeze and reproduce the full deterministic joint-budget decision."""
import argparse
from datetime import datetime,timezone
import gzip
import hashlib
import json
import platform
import signal
import time
from pathlib import Path
import flint
import numpy as np
import model as m
import optimize,resources,audit

HERE=m.HERE
SOURCES=['PROTOCOL.json','model.py','optimize.py','resources.py','audit.py','run.py','verify_publication.py','requirements.txt']
DEPENDENCIES=['../certified_budget_v0_3/balls.py','../certified_budget_v0_3/budget.py',
 '../certified_budget_v0_3/PROTOCOL.json','../certified_budget_v0_3/results/BUDGET.json',
 '../variance_budget_v0_4/variance.py','../variance_budget_v0_4/results/BUDGET.json',
 '../scale_calibration_v0_2/PROTOCOL.json','../scalar_pilot_v0_1/PROTOCOL.json',
 '../scalar_pilot_v0_1/counts.cpp','../scalar_pilot_v0_1/scalar.py','../scalar_pilot_v0_1/fields.py',
 '../e4_v0_1/contract.json','../massive_reference_v0_5/results/AUDIT.json']


def inventory():return {name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in SOURCES+DEPENDENCIES}

def frozen():
    if inventory()!=json.loads((HERE/'FREEZE.json').read_text())['files']:raise RuntimeError('frozen source/input mismatch')

def gzwrite(path,obj):
    data=(json.dumps(obj,ensure_ascii=False,allow_nan=False,separators=(',',':'))+'\n').encode()
    Path(path).write_bytes(gzip.compress(data,compresslevel=9,mtime=0))

def gzread(path):return json.loads(gzip.decompress(Path(path).read_bytes()))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['freeze','all']);ap.add_argument('--out',type=Path,default=HERE/'results');args=ap.parse_args()
    if args.phase=='freeze':
        if (HERE/'FREEZE.json').exists():raise RuntimeError('refusing to overwrite freeze')
        m.balls.write(HERE/'FREEZE.json',{'UTC':datetime.now(timezone.utc).isoformat(),
          'scope':'deterministic development freeze after exploratory preflight, before saved production; not confirmation',
          'files':inventory()});return
    frozen();p=optimize.plan();signal.alarm(p['production_wall_seconds_max'])
    if (flint.__version__,flint.__FLINT_VERSION__,np.__version__)!=('0.8.0','3.3.1','2.3.5'):raise RuntimeError('pinned numerical environment required')
    args.out.mkdir(parents=True,exist_ok=True);start=time.monotonic();m.ctx.prec=128
    checks=audit.controls();records={}
    for bits in [128,192]:
        m.ctx.prec=bits;record=optimize.compute();audit.validate(record);records[bits]=record
        gzwrite(args.out/('SCAN.json.gz' if bits==128 else 'SCAN_192bit.json.gz'),record)
    checks['replay']=audit.compare(records[128],records[192]);checks['status']='PASS'
    m.balls.write(args.out/'AUDIT.json',checks)
    resource=resources.compute(records[192]);m.balls.write(args.out/'RESOURCES.json',resource)
    low=records[128]
    summary={key:low[key] for key in ['schema','decision','expected_point_budget','systematic_allocation_candidates','summaries','relaxed_total_only','budget_sensitivity','fixed_mode_followups','scope','new_poisson_clouds','confirmation_seed_used','gate_status']}
    summary['scan_pairs']=len(low['rows']);summary['rejection_counts']=audit.validate(low)
    summary['physical_parameters_fixed']=True;summary['next_sprinkling']='NOT_STARTED_NO_BUDGETED_CANDIDATE'
    m.balls.write(args.out/'DECISION.json',summary)
    m.balls.write(args.out/'COMPUTE.json',{'elapsed_seconds':time.monotonic()-start,'python':platform.python_version(),
      'python_flint':flint.__version__,'FLINT':flint.__FLINT_VERSION__,'numpy':np.__version__,'precision_bits':[128,192],
      'new_poisson_clouds':0,'confirmation_seed_used':False,'gate_status':p['scientific_status']})

if __name__=='__main__':main()
