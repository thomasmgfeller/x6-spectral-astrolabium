#!/usr/bin/env python3
"""Verify archived bytes only; no scientific programs are executed."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def check(condition, message):
    if not condition:
        raise SystemExit('FAIL: ' + message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('downloads', type=Path)
    args = parser.parse_args()
    catalog = json.loads((Path(__file__).parent / 'artifacts.json').read_text())
    assets = 0
    entries = 0
    for package in catalog['packages']:
        for artifact in package['artifacts']:
            path = args.downloads / artifact['filename']
            check(path.is_file(), 'missing ' + artifact['filename'])
            data = path.read_bytes()
            check(len(data) == artifact['bytes'], 'size ' + artifact['filename'])
            check(hashlib.sha256(data).hexdigest() == artifact['sha256'],
                  'SHA-256 ' + artifact['filename'])
            assets += 1
            if artifact['kind'] != 'reproduction_archive':
                continue
            with zipfile.ZipFile(path) as archive:
                check(archive.testzip() is None, 'ZIP CRC ' + artifact['filename'])
                record = package['archive_integrity']
                inventory = json.loads(archive.read(record['original_inventory']))
                if 'files' in inventory and isinstance(inventory['files'], list):
                    expected = [(x['path'], x['sha256'], x.get('bytes'))
                                for x in inventory['files']]
                else:
                    expected = [(p, h, None) for p, h in inventory.items()]
                for name, digest, size in expected:
                    data = archive.read(record['inventory_prefix'] + name)
                    check(hashlib.sha256(data).hexdigest() == digest,
                          artifact['filename'] + ':' + name)
                    check(size is None or len(data) == size, 'member size ' + name)
                    entries += 1
    print(json.dumps({'status': 'PUBLICATION_INTEGRITY_PASS', 'assets': assets,
                      'original_inventory_entries': entries,
                      'scientific_programs_executed': 0}, indent=2))


if __name__ == '__main__':
    main()
