"""Freeze and execute a finite, deterministic interval-budget calculation."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import platform
import signal
import time
from pathlib import Path
import flint
from balls import HERE, plan, configure, write
import budget
import source

SOURCES = ['PROTOCOL.json','balls.py','budget.py','source.py','run.py','audit.py']
DEPENDENCIES = ['../scale_calibration_v0_2/results/source.npz',
                '../scale_calibration_v0_2/results/mean.npz',
                '../scale_calibration_v0_2/results/MEAN.json',
                '../scalar_pilot_v0_1/scalar.py','../e4_v0_1/contract.json']

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def inventory():
    return {p:sha(HERE/p) for p in SOURCES+DEPENDENCIES}

def frozen():
    lock = json.loads((HERE/'FREEZE.json').read_text())
    if inventory() != lock['files']:
        raise RuntimeError('HOLD: frozen input/source mismatch')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('phase',choices=['freeze','all'])
    ap.add_argument('--out',type=Path,default=HERE/'results')
    a = ap.parse_args()
    if a.phase=='freeze':
        if (HERE/'FREEZE.json').exists():
            raise RuntimeError('refusing to replace source lock')
        write(HERE/'FREEZE.json',{'UTC':datetime.now(timezone.utc).isoformat(),
            'scope':'implementation freeze before fixed production matrix; exploratory preflight, not E4 confirmation',
            'files':inventory()})
        return
    frozen(); configure(); signal.alarm(plan()['wall_seconds_max'])
    if flint.__version__ != plan()['python_flint'] or flint.__FLINT_VERSION__ != '3.3.1':
        raise RuntimeError('pinned python-flint 0.8.0 / FLINT 3.3.1 required')
    a.out.mkdir(parents=True,exist_ok=True); t=time.monotonic()
    write(a.out/'BUDGET.json',budget.compute())
    write(a.out/'SOURCE.json',source.compute())
    write(a.out/'COMPUTE.json',{'elapsed_seconds':time.monotonic()-t,'python':platform.python_version(),
        'python_flint':flint.__version__,'FLINT':flint.__FLINT_VERSION__,
        'precision_bits':plan()['precision_bits'],'new_random_realizations':0,
        'scientific_status':'G1 HOLD; full source reference HOLD; G2/G3 NOT_RUN'})

if __name__=='__main__':
    main()
