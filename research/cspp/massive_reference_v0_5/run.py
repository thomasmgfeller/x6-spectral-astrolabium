"""Frozen deterministic production and independent higher-precision replay."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import platform
import signal
import time
from pathlib import Path
import flint
import numpy as np
import reference as r
import audit
import detector

HERE=r.HERE
SOURCES=['reference.py','detector.py','audit.py','run.py','verify_publication.py','PROTOCOL.json','requirements.txt']
DEPENDENCIES=['../certified_budget_v0_3/source.py','../certified_budget_v0_3/balls.py',
 '../certified_budget_v0_3/PROTOCOL.json','../certified_budget_v0_3/results/SOURCE.json',
 '../certified_budget_v0_3/audit.py','../certified_budget_v0_3/budget.py',
 '../scale_calibration_v0_2/results/source.npz','../e4_v0_1/contract.json']


def inventory():
    return {p:hashlib.sha256((HERE/p).read_bytes()).hexdigest() for p in SOURCES+DEPENDENCIES}


def frozen():
    lock=json.loads((HERE/'FREEZE.json').read_text())
    if inventory()!=lock['files']:raise RuntimeError('frozen input/source mismatch')


def compare_detector(low,high):
    audit.check(low['spatial_cells']==high['spatial_cells']==648,'detector cell inventory')
    audit.check(low['status']==high['status'],'stable spatial goal decision')
    for a,b in zip(low['rows'],high['rows']):
        audit.check(a['entry']==b['entry'],'detector entry identity')
        audit.check(r.balls.decode(a['value']).overlaps(r.balls.decode(b['value'])),'detector replay overlap')
    return {'spatial_cells':648,'matrix_entries':3,'precision_bits':[128,192],
            'overlap_is_regression_not_proof':True}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['freeze','all'])
    parser.add_argument('--out',type=Path,default=HERE/'results')
    args=parser.parse_args()
    if args.phase=='freeze':
        if (HERE/'FREEZE.json').exists():raise RuntimeError('refusing to overwrite freeze')
        r.balls.write(HERE/'FREEZE.json',{'UTC':datetime.now(timezone.utc).isoformat(),
          'phase':'deterministic production after explicit exploratory preflight; not E4 confirmation',
          'files':inventory()});return
    frozen();p=json.loads((HERE/'PROTOCOL.json').read_text());signal.alarm(p['wall_seconds_max'])
    if (flint.__version__,flint.__FLINT_VERSION__,np.__version__)!=('0.8.0','3.3.1','2.3.5'):
        raise RuntimeError('pinned numerical environment required')
    args.out.mkdir(parents=True,exist_ok=True);t=time.monotonic()
    r.balls.configure(128)
    controls={'source':audit.controls(),'detector':audit.detector_controls()}
    records={}
    for bits in (128,192):
        r.balls.configure(bits)
        suffix='' if bits==128 else '_192bit'
        records[bits]={'source':r.compute()}
        r.balls.write(args.out/('SOURCE'+suffix+'.json'),records[bits]['source'])
        records[bits]['detector']=detector.compute()
        r.balls.write(args.out/('DETECTOR'+suffix+'.json'),records[bits]['detector'])
    controls['source_replay']=audit.compare(records[128]['source'],records[192]['source'])
    controls['detector_replay']=compare_detector(records[128]['detector'],records[192]['detector'])
    controls['status']='PASS';r.balls.write(args.out/'AUDIT.json',controls)
    r.balls.write(args.out/'COMPUTE.json',{'elapsed_seconds':time.monotonic()-t,
      'python':platform.python_version(),'python_flint':flint.__version__,'FLINT':flint.__FLINT_VERSION__,
      'numpy':np.__version__,'precision_bits':[128,192],'new_random_realizations':0,
      'confirmation_seed_used':False,'scientific_status':p['scientific_status']})

if __name__=='__main__':main()
