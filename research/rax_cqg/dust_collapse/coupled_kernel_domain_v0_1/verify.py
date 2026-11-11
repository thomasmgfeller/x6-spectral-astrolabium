"""Manifest, original Git blob identities, tests and byte-identical replay."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def main():
    manifest=json.loads((ROOT/'MANIFEST.sha256.json').read_text())
    for path,want in manifest.items():
        data=(ROOT/path).read_bytes()
        if hashlib.sha256(data).hexdigest()!=want:
            raise RuntimeError('SHA256 mismatch: '+path)
    files={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()
           and '__pycache__' not in p.parts and p.name!='MANIFEST.sha256.json'}
    if files!=set(manifest):
        raise RuntimeError('Manifest coverage mismatch: '+repr(files^set(manifest)))
    subprocess.run([sys.executable,'-B','test_domain.py'],cwd=ROOT,check=True)
    with tempfile.TemporaryDirectory() as tmp:
        dst=Path(tmp)/'domain_certificate.json'
        subprocess.run([sys.executable,'-B','domain_analysis.py',str(dst)],cwd=ROOT,check=True)
        if dst.read_bytes()!=(ROOT/'results/domain_certificate.json').read_bytes():
            raise RuntimeError('Result replay differs')
    print(f'PASS: {len(manifest)} file hashes; 9 source blobs; 11 test groups; byte-identical replay.')

if __name__=='__main__':
    main()
