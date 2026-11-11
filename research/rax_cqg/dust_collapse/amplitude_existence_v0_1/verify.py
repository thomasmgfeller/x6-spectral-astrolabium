"""Read-only offline integrity and mathematical checks; never rewrites references."""
from pathlib import Path
import hashlib
import json
import sys
import unittest
from existence import rendered

ROOT=Path(__file__).resolve().parent

def main():
    manifest=json.loads((ROOT/'MANIFEST.sha256.json').read_text())
    actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()
            and '__pycache__' not in p.parts and p.name!='MANIFEST.sha256.json'}
    if actual!=set(manifest):raise SystemExit('Manifest file set mismatch')
    for path,digest in manifest.items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=digest:
            raise SystemExit('Hash mismatch: '+path)
    for item in json.loads((ROOT/'provenance.json').read_text())['files']:
        data=(ROOT/item['local_path']).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if blob!=item['git_blob_sha'] or hashlib.sha256(data).hexdigest()!=item['sha256']:
            raise SystemExit('Upstream content mismatch: '+item['local_path'])
    result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.discover(str(ROOT),pattern='test_existence.py'))
    if not result.wasSuccessful():return 1
    if rendered()!=(ROOT/'results/existence_certificate.json').read_text(encoding='utf-8'):
        raise SystemExit('Evidence replay mismatch')
    print(f'PASS: {result.testsRun} tests; {len(manifest)} file hashes; five upstream blobs; exact evidence replay.')
    return 0

if __name__=='__main__':sys.exit(main())
