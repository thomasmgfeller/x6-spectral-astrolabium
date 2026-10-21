"""SPDX-License-Identifier: Apache-2.0
Separate successor: immutable PR69 estimators, new calibration observations.
"""
import gzip
import hashlib
import json
import sys
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(BASE/'metadata_bias'))
from mb_common import config, sources as inherited_sources, encode, digest
from mb_model import prepare
from run_calibration import coordinates_only

ARMS=['original','metadata','projected','projected_metadata']


def cfg():
    return json.loads((HERE/'contract.json').read_text())


def sha(x):
    return hashlib.sha256(x).hexdigest()


def write(path,value):
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')


def pins():
    names=['ec_common.py','ec_measure.py','ec_prepare.py','ec_collect.py','ec_calibrate.py',
           'ec_analyze.py','ec_verify.py','ec_controls.py','contract.json','PROTOCOL.md']
    files={**inherited_sources()}
    for p in [*[HERE/n for n in names],BASE/'metadata_bias/frozen_model.json',
              BASE/'metadata_bias/test_clouds.zip']:
        files[str(p.relative_to(ROOT))]=sha(p.read_bytes())
    return files


def models():
    return json.loads((BASE/'metadata_bias/frozen_model.json').read_text())['models']


def load_phase(phase):
    executions=[]; rows=[]
    for worker in range(cfg()['workers']):
        path=HERE/f'results/{phase}/worker-{worker}'
        execution=json.loads((path/'execution.json').read_text())
        executions.append(execution)
        for record in execution['records']:
            raw=(path/record['file']).read_bytes()
            assert sha(raw)==record['sha256']
            rows.append(json.loads(gzip.decompress(raw)))
    rows.sort(key=lambda r:r['index'])
    return executions,rows


def source_check():
    frozen=json.loads((HERE/'source_freeze.json').read_text())
    for name,h in frozen['files'].items():
        assert sha((ROOT/name).read_bytes())==h,name
    return frozen
