"""SPDX-License-Identifier: Apache-2.0"""
import gzip
import hashlib
import json
import sys
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(BASE/'error_calibration'))
import ec_common as ec
from ec_measure import field_values
from feasibility import design,TARGET
from variance_weights import minimum_variance


def cfg():return json.loads((HERE/'contract.json').read_text())
def sha(data):return hashlib.sha256(data).hexdigest()
def write(path,value):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
def close(a,b):np.testing.assert_allclose(a,b,atol=cfg()['numerical_atol'],rtol=cfg()['numerical_rtol'])


def pins():
    files=dict(json.loads((BASE/'error_calibration/source_freeze.json').read_text())['files'])
    names=['contract.json','PROTOCOL.md','ra_common.py','ra_core.py','ra_analyze.py','ra_run.py','ra_controls.py','ra_verify.py']
    paths=[*[HERE/n for n in names],BASE/'error_calibration/source_freeze.json',
           BASE/'error_calibration/seed_schedule.json',BASE/'error_calibration/results/summary.json']
    for phase in cfg()['phases']:
        paths.extend(p for p in (BASE/f'error_calibration/results/{phase}').rglob('*') if p.is_file())
    for p in paths:files[str(p.relative_to(ROOT))]=sha(p.read_bytes())
    return dict(sorted(files.items()))


def source_check():
    frozen=json.loads((HERE/'source_freeze.json').read_text())
    for name,h in frozen['files'].items():assert sha((ROOT/name).read_bytes())==h,name
    return frozen


def inputs():
    out=[]
    schedule=json.loads((BASE/'error_calibration/seed_schedule.json').read_text())
    for phase in cfg()['phases']:
        executions,rows=ec.load_phase(phase)
        assert len(rows)==cfg()['expected_clouds_per_phase']
        assert all(v['status']=='COMPLETE' for v in executions)
        assert [(r['index'],r['seed']) for r in rows]==[(r['index'],r['geometry_seed']) for r in schedule[phase]]
        out.extend(rows)
    return out
