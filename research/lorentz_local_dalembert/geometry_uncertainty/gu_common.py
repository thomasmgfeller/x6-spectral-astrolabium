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
from cg_cloud import run_cloud
from feasibility import design

def cfg():return json.loads((HERE/'contract.json').read_text())
def sha(data):return hashlib.sha256(data).hexdigest()
def encode(value):return ec.encode(value)
def write(path,value):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
def close(a,b):np.testing.assert_allclose(a,b,atol=cfg()['numerical_atol'],rtol=cfg()['numerical_rtol'])
def model():return json.loads((HERE/'development_model.json').read_text())
def source_check():
    frozen=json.loads((HERE/'source_freeze.json').read_text())
    for name,h in frozen['files'].items():assert sha((ROOT/name).read_bytes())==h,name
    return frozen
def load_phase(phase):
    executions=[];rows=[]
    for worker in range(cfg()['workers']):
        folder=HERE/f'results/{phase}/worker-{worker}'
        execution=json.loads((folder/'execution.json').read_text());executions.append(execution)
        for rec in execution['records']:
            raw=(folder/rec['file']).read_bytes();assert sha(raw)==rec['sha256']
            rows.append(json.loads(gzip.decompress(raw)))
    return executions,sorted(rows,key=lambda r:r['index'])
def pins():
    files=dict(json.loads((BASE/'error_calibration/source_freeze.json').read_text())['files'])
    paths=list(HERE.glob('gu_*.py'))+[HERE/'contract.json',HERE/'PROTOCOL.md',
        HERE/'development_model.json',HERE/'seed_schedule.json',
        BASE/'error_calibration/source_freeze.json']
    for phase in ['calibration','test']:
        paths.extend(p for p in (BASE/f'error_calibration/results/{phase}').rglob('*') if p.is_file())
    for p in paths:files[str(p.relative_to(ROOT))]=sha(p.read_bytes())
    return dict(sorted(files.items()))
def compare(a,b,path='root'):
    if isinstance(b,dict):
        assert a.keys()==b.keys(),path
        for k in b:compare(a[k],b[k],path+'.'+k)
    elif isinstance(b,list):
        assert len(a)==len(b),path
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,f'{path}[{i}]')
    elif isinstance(b,float):
        np.testing.assert_allclose(a,b,atol=cfg()['numerical_atol'],rtol=cfg()['numerical_rtol'],err_msg=path)
    else:assert a==b,(path,a,b)
