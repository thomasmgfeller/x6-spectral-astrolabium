#!/usr/bin/env python3
"""Integrity and independent isolated replay. No repository files are changed."""
from pathlib import Path
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
PROGRAMS=[
 'checks/full_weight/check.py',
 'checks/scalar_response/check.py',
 'checks/physical_readout/check.py',
 'checks/composition/check.py',
 'checks/geometry_response/check.py',
 'checks/independent_audit/check.py',
 'checks/independent_audit/audit_quadrature.py',
 'checks/combined_response/check.py',
]

def compare(a,b,path=''):
    if isinstance(a,dict):
        assert isinstance(b,dict) and set(a)==set(b), ('keys',path)
        for k in a:
            if k not in ('runtime_seconds','source_files_sha256'):compare(a[k],b[k],path+'/'+k)
    elif isinstance(a,list):
        assert isinstance(b,list) and len(a)==len(b), ('length',path)
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'/'+str(i))
    elif isinstance(a,float):
        assert isinstance(b,(int,float)) and math.isfinite(a) and math.isfinite(b), ('type/finite',path)
        assert math.isclose(a,b,rel_tol=5e-12,abs_tol=5e-12), ('numeric',path,a,b)
    else:
        assert a==b, ('exact',path,a,b)

def validate_source_hashes(root, value):
    # Hashes identify bytes of each run's actual sources. A timed replay has
    # different source bytes; numerical equivalence is checked independently.
    if isinstance(value,dict):
        for name,digest in value.get('source_files_sha256',{}).items():
            assert hashlib.sha256((root/'checks'/name).read_bytes()).hexdigest()==digest, ('source hash',name)
        for child in value.values():validate_source_hashes(root,child)
    elif isinstance(value,list):
        for child in value:validate_source_hashes(root,child)

def main():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    for item in manifest['files']:
        path=ROOT/item['path']
        assert path.is_file(), ('missing',item['path'])
        data=path.read_bytes()
        assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'], ('hash',item['path'])
    expected={str(p.relative_to(ROOT)):json.loads(p.read_text()) for p in (ROOT/'checks').rglob('*.json')}
    for value in expected.values():validate_source_hashes(ROOT,value)
    with tempfile.TemporaryDirectory(prefix='cst_interference_replay_') as tmp:
        target=Path(tmp)/'package'
        shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
        for program in PROGRAMS:
            result=subprocess.run([sys.executable,'-B',str(target/program)],cwd=target,env=env,text=True,capture_output=True,timeout=180)
            if result.returncode:
                print(result.stdout[-6000:]);print(result.stderr[-6000:])
                raise RuntimeError('Failed: '+program)
            print('PASS',program)
        for name,original in expected.items():
            reproduced=json.loads((target/name).read_text())
            validate_source_hashes(target,reproduced)
            compare(original,reproduced,name)
    print('PASS:',len(manifest['files']),'file hashes;',len(PROGRAMS),'programs;',len(expected),'JSON outputs reproduced.')
    print('Physical geometry dynamics remains NOT_DERIVED. Numerical replay is not a full floating-point error certificate.')

if __name__=='__main__':main()
