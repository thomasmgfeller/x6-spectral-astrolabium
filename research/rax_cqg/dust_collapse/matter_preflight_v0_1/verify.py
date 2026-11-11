#!/usr/bin/env python3
"""Verify source identity, package hashes and isolated exact-algebra replay."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def main():
    for item in json.loads((ROOT/'provenance.json').read_text())['sources']:
        data=(ROOT/item['local_path']).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert blob==item['git_blob_sha'],item['local_path']
        assert hashlib.sha256(data).hexdigest()==item['sha256'],item['local_path']
    if (ROOT/'SHA256SUMS.json').exists():
        manifest=json.loads((ROOT/'SHA256SUMS.json').read_text())
        actual={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts
                and p.suffix not in ('.pyc','.zip') and p.name!='SHA256SUMS.json'}
        assert actual==manifest['files'],'Package inventory or hash mismatch'
    with tempfile.TemporaryDirectory() as tmp:
        out=Path(tmp)
        subprocess.run([sys.executable,str(ROOT/'analyze.py'),'--outdir',str(out)],check=True)
        expected=sorted((ROOT/'results').glob('*.json'))
        actual=sorted((out/'results').glob('*.json'))
        assert [p.name for p in expected]==[p.name for p in actual]
        for a,b in zip(expected,actual):assert a.read_bytes()==b.read_bytes(),a.name
    print('PASS: four pinned source files, package hashes when present, two byte-identical replay files.')
    print('No physical matter kernel computed; physical gates HOLD.')

if __name__=='__main__': main()
