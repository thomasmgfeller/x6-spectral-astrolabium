"""Optional original-source audit: download the 20 pinned KAt archives (~3.4 GB).

Ordinary replay uses the included unchanged selected channels, without network.
This command does not inspect signals, fit thresholds, or evaluate performance.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
BASE = 'https://groups.uni-paderborn.de/kat/BearingDataCenter/'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((ROOT/'data/manifest.json').read_text())
    freeze = json.loads((ROOT/'freeze.json').read_text())
    if hashlib.sha256((ROOT/'data/manifest.json').read_bytes()).hexdigest() != freeze['manifest_sha256']:
        raise ValueError('INPUT_MANIFEST_CHANGED')
    def download(r):
        name = r['bearing_id']+'.rar'
        if r['archive_url'] != BASE+name or '/' in name or '..' in name:
            raise ValueError('UNEXPECTED_SOURCE_URL')
        path = args.output/name
        size, h = 0, hashlib.sha256()
        with urllib.request.urlopen(r['archive_url'], timeout=60) as response, path.with_suffix('.part').open('xb') as f:
            while chunk := response.read(1024*1024):
                size += len(chunk)
                if size > r['archive_bytes']:
                    raise ValueError('SOURCE_TOO_LARGE: '+name)
                h.update(chunk)
                f.write(chunk)
        if size != r['archive_bytes'] or h.hexdigest() != r['archive_sha256']:
            raise ValueError('SOURCE_CHANGED_OR_INCOMPLETE: '+name)
        path.with_suffix('.part').rename(path)
        print('VERIFIED', name, size, flush=True)
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(download, manifest['records']))


if __name__ == '__main__':
    main()
