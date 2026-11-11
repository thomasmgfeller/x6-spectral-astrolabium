"""Read-only, offline verification. Never refreshes the reference manifest."""
from pathlib import Path
import hashlib,json,sys,unittest
from build_evidence import render
ROOT=Path(__file__).resolve().parent
def main():
    manifest=json.loads((ROOT/'MANIFEST.sha256.json').read_text())
    for path,digest in manifest.items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=digest:
            raise SystemExit('Hash mismatch: '+path)
    expected={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()
              and '__pycache__' not in p.parts and p.name!='MANIFEST.sha256.json'}
    if expected!=set(manifest): raise SystemExit('Manifest file set mismatch')
    for f in json.loads((ROOT/'provenance.json').read_text())['files']:
        data=(ROOT/f['local']).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if blob!=f['blob_sha']: raise SystemExit('Upstream blob mismatch: '+f['local'])
    result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.discover(str(ROOT),pattern='test_boundary.py'))
    if not result.wasSuccessful(): return 1
    if render()!=(ROOT/'results/gram_matrices.json').read_text(encoding='utf-8'):
        raise SystemExit('Evidence replay mismatch')
    print(f'PASS: {result.testsRun} tests; manifest, upstream blobs, exact evidence replay.')
    return 0
if __name__=='__main__': sys.exit(main())
