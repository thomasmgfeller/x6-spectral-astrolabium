#!/usr/bin/env python3
"""Preserved archive/source parity and the original isolated scientific replay."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE/'interference_dynamics_v0_1'
STEM='CST_DUST_Interferenz_Dynamik_v0_1'

def require(condition,message):
    if not condition:
        raise RuntimeError(message)

def main():
    require(not sys.flags.optimize,'Do not disable scientific assertions with python -O.')
    record=json.loads((HERE/'interference_dynamics_publication.json').read_text())
    for item in record['artifacts']:
        data=(HERE/item['path']).read_bytes()
        require(len(data)==item['bytes'],'Size mismatch: '+item['path'])
        require(hashlib.sha256(data).hexdigest()==item['sha256'],'Hash mismatch: '+item['path'])
    entries=json.loads((ROOT/'MANIFEST.json').read_text())['files']
    paths={entry['path'] for entry in entries}|{'MANIFEST.json'}
    require(len(paths)==len(entries)+1,'Duplicate manifest path')
    with zipfile.ZipFile(HERE/'packages'/(STEM+'_Pruefpaket.zip')) as archive:
        expected={ROOT.name+'/'+path for path in paths}
        require(archive.testzip() is None,'ZIP CRC failure')
        require(len(archive.namelist())==len(expected) and set(archive.namelist())==expected,'ZIP inventory mismatch')
        for path in paths:
            require(archive.read(ROOT.name+'/'+path)==(ROOT/path).read_bytes(),'ZIP/source mismatch: '+path)
    require((HERE/'reports'/(STEM+'.pdf')).read_bytes()==(ROOT/'report/CST_DUST_Interferenz_Randantwort_Dynamikpruefung_v0_1.pdf').read_bytes(),'PDF copy mismatch')
    print(f'PASS: {len(paths)} exact ZIP/source pairs and identical report copies.',flush=True)
    subprocess.run([sys.executable,'-B',str(ROOT/'verify.py')],check=True)

if __name__=='__main__':main()
