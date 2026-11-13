#!/usr/bin/env python3
"""Verify the unchanged end-boundary package and replay it in isolation."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE / 'boundary_coherence_v0_1'
STEM = 'CST_DUST_Kohaerente_Endrandmessung_v0_1'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def verify():
    record = json.loads((HERE / 'boundary_coherence_publication.json').read_text())
    for item in record['artifacts']:
        data = (HERE / item['path']).read_bytes()
        require(len(data) == item['bytes'], 'Artifact size: ' + item['path'])
        require(hashlib.sha256(data).hexdigest() == item['sha256'],
                'Artifact hash: ' + item['path'])
    entries = json.loads((ROOT / 'MANIFEST.json').read_text())['files']
    paths = {entry['path'] for entry in entries} | {'MANIFEST.json'}
    require(len(paths) == len(entries) + 1, 'Duplicate manifest path')
    for entry in entries:
        data = (ROOT / entry['path']).read_bytes()
        require(len(data) == entry['bytes'], 'Size: ' + entry['path'])
        require(hashlib.sha256(data).hexdigest() == entry['sha256'],
                'Hash: ' + entry['path'])
    with zipfile.ZipFile(HERE / 'packages' / (STEM + '_Pruefpaket.zip')) as archive:
        expected = {ROOT.name + '/' + p for p in paths}
        require(archive.testzip() is None, 'ZIP CRC failure')
        require(len(archive.namelist()) == len(expected)
                and set(archive.namelist()) == expected, 'ZIP inventory mismatch')
        for path in paths:
            require(archive.read(ROOT.name + '/' + path) == (ROOT / path).read_bytes(),
                    'ZIP/source mismatch: ' + path)
    print(f'PASS: {len(entries)} manifest entries and {len(paths)} exact ZIP/source pairs.', flush=True)
    with tempfile.TemporaryDirectory(prefix='cst-boundary-coherence-') as temporary:
        isolated = Path(temporary) / ROOT.name
        isolated.mkdir()
        for path in paths:
            target = isolated / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, target)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        subprocess.run([sys.executable, '-B', str(isolated / 'checks/run_all.py')],
                       cwd=temporary, env=env, check=True, timeout=120)
        for path in paths:
            require((ROOT / path).read_bytes() == (isolated / path).read_bytes(),
                    'Replay changed frozen file: ' + path)
    print('PASS: seven finite programs; all frozen files reproduced byte-for-byte.')
    print('Inherited amplitude quadrature was not rerun; physical geometry remains HOLD.')


if __name__ == '__main__':
    verify()
