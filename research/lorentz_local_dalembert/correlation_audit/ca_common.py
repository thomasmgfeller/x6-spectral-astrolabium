"""SPDX-License-Identifier: Apache-2.0"""
import gzip
import json
import sys
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(BASE/'geometry_correction'))
import gc_common as old
from gc_model import canonical,correct,intervals
from gg_model import matrices,covariance,basis
model=old.model
sha=old.sha
encode=old.encode
write=old.write
order_check=old.order_check

def cfg():return json.loads((HERE/'contract.json').read_text())
def close(a,b):np.testing.assert_allclose(a,b,atol=cfg()['numeric_atol'],rtol=cfg()['numeric_rtol'])
def history():
    rows=[]
    for phase in ['calibration','test']:
        _,batch=old.load_phase(phase)
        for row in batch:
            assert sha(encode(row['prediction']).encode())==row['prediction_seal']
        rows+=batch
    assert len(rows)==cfg()['historical_attempts']
    return rows
def source_check():
    f=json.loads((HERE/'source_freeze.json').read_text())
    for name,h in f['files'].items():assert sha((ROOT/name).read_bytes())==h,name
    return f
def pins():
    files=dict(json.loads((BASE/'geometry_correction/source_freeze.json').read_text())['files'])
    paths=list(HERE.glob('ca_*.py'))+[HERE/'contract.json',HERE/'PROTOCOL.md',BASE/'geometry_correction/source_freeze.json']
    for phase in ['calibration','test']:
        paths.extend(p for p in (BASE/f'geometry_correction/results/{phase}').rglob('*') if p.is_file())
    for p in paths:files[str(p.relative_to(ROOT))]=sha(p.read_bytes())
    return dict(sorted(files.items()))
def load_results():
    executions=[];rows=[]
    for worker in range(cfg()['workers']):
        folder=HERE/f'results/worker-{worker}';e=json.loads((folder/'execution.json').read_text());executions.append(e)
        for r in e['records']:
            raw=(folder/r['file']).read_bytes();assert sha(raw)==r['sha256']
            rows.append(json.loads(gzip.decompress(raw)))
    return executions,sorted(rows,key=lambda r:r['index'])
def compare(a,b,path='root'):
    if isinstance(b,dict):
        assert a.keys()==b.keys(),path
        for k in b:compare(a[k],b[k],path+'.'+k)
    elif isinstance(b,list):
        assert len(a)==len(b),path
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,f'{path}[{i}]')
    elif isinstance(b,float):np.testing.assert_allclose(a,b,atol=cfg()['numeric_atol'],rtol=cfg()['numeric_rtol'],err_msg=path)
    else:assert a==b,(path,a,b)
