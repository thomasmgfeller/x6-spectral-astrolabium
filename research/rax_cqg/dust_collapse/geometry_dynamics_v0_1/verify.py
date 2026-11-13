#!/usr/bin/env python3
"""Check integrity and replay the nine finite programs in an isolated copy."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
SCRIPTS=[
 'source_clock/check.py',
 'physical_sector/check.py',
 'order_variation/check.py',
 'geometry/check.py',
 'geometry/n11_check.py',
 'dynamics_sewing/check.py',
 'dynamics_sewing/check_n11.py',
 'independent_audit/check.py',
 'independent_audit/check_n11.py',
]

def require(value,message):
    if not value:
        raise RuntimeError(message)

def main():
    require(not sys.flags.optimize, 'Do not disable the scientific assertions with python -O.')
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    for entry in manifest['files']:
        data=(ROOT/entry['path']).read_bytes()
        require(len(data)==entry['bytes'], 'Size mismatch: '+entry['path'])
        require(hashlib.sha256(data).hexdigest()==entry['sha256'], 'Hash mismatch: '+entry['path'])
    print(f"PASS: {len(manifest['files'])} original manifest entries.",flush=True)
    source=ROOT/'checks'
    snapshots={p.relative_to(source):p.read_bytes() for p in source.rglob('*.json')}
    with tempfile.TemporaryDirectory(prefix='cst-geometry-replay-') as temp:
        isolated=Path(temp)/'checks'
        shutil.copytree(source,isolated,ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.log'))
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
        for script in SCRIPTS:
            run=subprocess.run([sys.executable,'-B',str(isolated/script)],cwd=temp,
                               env=env,capture_output=True,text=True,timeout=120)
            if run.returncode:
                print(run.stdout);print(run.stderr,file=sys.stderr)
                raise RuntimeError('Scientific replay failed: '+script)
            print('PASS: '+script,flush=True)
        for rel,original in snapshots.items():
            require((isolated/rel).read_bytes()==original,'Replay changed JSON: '+str(rel))
    print(f'PASS: {len(SCRIPTS)} programs; {len(snapshots)} JSON files unchanged.')
    print('Scope: finite stationary geometric action comparison. Physical geometry dynamics remains NOT_DERIVED.')

if __name__=='__main__':
    main()
