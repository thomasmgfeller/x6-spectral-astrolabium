"""Read-only offline verification; never refreshes a manifest or result."""
from pathlib import Path
import argparse
import hashlib
import json
import unittest
from core import ROOT
from run_certified import compute
from causation import analyze

def render(value):return json.dumps(value,indent=2,ensure_ascii=False,sort_keys=True)+'\n'

def main(extended=False):
    manifest=json.loads((ROOT/'MANIFEST.sha256.json').read_text())
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
            and '__pycache__' not in p.parts and p.name!='MANIFEST.sha256.json'}
    if actual!=set(manifest):raise SystemExit('Manifest file inventory mismatch')
    for path,digest in manifest.items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=digest:raise SystemExit('Hash mismatch: '+path)
    for item in json.loads((ROOT/'provenance.json').read_text())['files']:
        b=(ROOT/item['local_path']).read_bytes()
        if (hashlib.sha256(b).hexdigest()!=item['sha256'] or
            hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=item['git_blob_sha']):
            raise SystemExit('Upstream blob mismatch: '+item['local_path'])
    suite=unittest.defaultTestLoader.discover(str(ROOT),pattern='test_mixing.py')
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():return 1
    primary=compute(40,128,progress=False)
    if render(primary)!=(ROOT/'results/certified_mixing.json').read_text():raise SystemExit('Primary result replay mismatch')
    if render(analyze(primary))!=(ROOT/'results/causation_diagnostics.json').read_text():raise SystemExit('Causation replay mismatch')
    if extended:
        if render(compute(48,192,progress=False))!=(ROOT/'results/crosscheck_48.json').read_text():raise SystemExit('Extended result replay mismatch')
    print(f'PASS: {result.testsRun} tests; {len(manifest)} file hashes; five upstream blobs; exact primary and causation replay'+('; extended replay' if extended else '')+'.')
    return 0

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--extended',action='store_true');a=p.parse_args()
    raise SystemExit(main(a.extended))
