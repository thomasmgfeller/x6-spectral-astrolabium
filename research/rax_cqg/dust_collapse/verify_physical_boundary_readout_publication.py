#!/usr/bin/env python3
"""Check preserved archive/source bytes, then replay the scientific package."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE / 'physical_boundary_readout_v0_1'
STEM = 'CST_DUST_Physikalischer_Rand_Auslesevertrag_v0_1'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--artifacts-only', action='store_true',
                        help='Check publication bytes without repeating the scientific replay.')
    args = parser.parse_args()
    require(not sys.flags.optimize, 'Do not disable scientific assertions with python -O.')
    record = json.loads((HERE / 'physical_boundary_readout_publication.json').read_text())
    for item in record['artifacts']:
        data = (HERE / item['path']).read_bytes()
        require(len(data) == item['bytes'], 'Size mismatch: ' + item['path'])
        require(hashlib.sha256(data).hexdigest() == item['sha256'], 'Hash mismatch: ' + item['path'])
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    expected = set(manifest['files']) | {'MANIFEST.json'}
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
              and '__pycache__' not in p.parts and p.suffix != '.pyc'}
    require(actual == expected, 'Expanded source inventory differs from manifest')
    require(len(expected) == record['original_archive_files'], 'Archive file count differs')
    with zipfile.ZipFile(HERE / 'packages' / (STEM + '_Pruefpaket.zip')) as archive:
        names = archive.namelist()
        require(len(names) == len(expected) and set(names) == expected, 'ZIP inventory mismatch')
        require(archive.testzip() is None, 'ZIP CRC failure')
        for name in sorted(expected):
            data = (ROOT / name).read_bytes()
            require(archive.read(name) == data, 'ZIP/source byte mismatch: ' + name)
            if name != 'MANIFEST.json':
                require(hashlib.sha256(data).hexdigest() == manifest['files'][name],
                        'Manifest mismatch: ' + name)
    require(record['base_commit'] == json.loads((ROOT / 'sources/provenance.json').read_text())['parent_commit'],
            'Parent commit mismatch')
    print(f'PASS: {len(expected)} original ZIP entries and expanded files are byte-identical; '
          'standalone and embedded PDF originals have separate verified hashes.', flush=True)
    if not args.artifacts_only:
        subprocess.run([sys.executable, '-B', str(ROOT / 'verify.py')], check=True)


if __name__ == '__main__':
    main()
