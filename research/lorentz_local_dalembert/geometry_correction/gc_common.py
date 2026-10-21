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
sys.path.insert(0,str(BASE/'geometry_groups'))
import gg_common as inherited
from gg_model import matrices,covariance,intervals
from cg_relations import check as order_check, constraints
ec=inherited.ec
run_cloud=inherited.run_cloud
encode=inherited.encode
write=inherited.write
sha=inherited.sha

def cfg():return json.loads((HERE/'contract.json').read_text())
def model():return inherited.model()
def close(a,b):np.testing.assert_allclose(a,b,atol=cfg()['numerical_atol'],rtol=cfg()['numerical_rtol'])
def source_check():
    frozen=json.loads((HERE/'source_freeze.json').read_text())
    for name,h in frozen['files'].items():assert sha((ROOT/name).read_bytes())==h,name
    return frozen
def pins():
    files=dict(json.loads((BASE/'geometry_groups/source_freeze.json').read_text())['files'])
    paths=list(HERE.glob('gc_*.py'))+[HERE/'contract.json',HERE/'PROTOCOL.md',HERE/'seed_schedule.json',
        BASE/'geometry_groups/source_freeze.json',BASE/'geometry_groups/seed_schedule.json']
    for p in paths:files[str(p.relative_to(ROOT))]=sha(p.read_bytes())
    return dict(sorted(files.items()))
def load_phase(phase):
    executions=[];rows=[]
    for worker in range(cfg()['workers']):
        folder=HERE/f'results/{phase}/worker-{worker}'
        e=json.loads((folder/'execution.json').read_text());executions.append(e)
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
    elif isinstance(b,float):
        np.testing.assert_allclose(a,b,atol=cfg()['numerical_atol'],rtol=cfg()['numerical_rtol'],err_msg=path)
    else:assert a==b,(path,a,b)
