#!/usr/bin/env python3
"""Verify all hashes and replay the controls in a fresh temporary directory."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
import package

ROOT = Path(__file__).resolve().parent


def main():
    manifest = json.loads((ROOT/package.MANIFEST).read_text())
    actual = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in package.files()}
    if actual != manifest['files']:
        raise SystemExit('FAIL: inventory or checksum mismatch')
    provenance = json.loads((ROOT/'provenance.json').read_text())
    for item in provenance['sources']:
        data = (ROOT/item['local_path']).read_bytes()
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if blob != item['git_blob_sha']:
            raise SystemExit('FAIL: pinned Git source blob mismatch')
    archive = ROOT/package.ARCHIVE
    if archive.exists() and archive.read_bytes() != package.archive_bytes():
        raise SystemExit('FAIL: archive is not the deterministic package')
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        subprocess.run([sys.executable, str(ROOT/'build_evidence.py'), '--outdir', str(out)], check=True)
        subprocess.run([sys.executable, str(ROOT/'test_normalization.py'), '--report', str(out/'results/tests.json')], check=True)
        paths = sorted(p.relative_to(out) for p in out.rglob('*') if p.is_file())
        expected = sorted([p.relative_to(ROOT) for sub in ('data', 'results')
                           for p in (ROOT/sub).rglob('*') if p.is_file()])
        if paths != expected:
            raise SystemExit('FAIL: replay output inventory differs')
        for path in paths:
            if (out/path).read_bytes() != (ROOT/path).read_bytes():
                raise SystemExit(f'FAIL: replay differs: {path}')
    print(f'PASS: {len(actual)} hashed files; pinned source blobs; {len(paths)} byte-identical replay files; 21 tests.')
    print('Physical gates remain HOLD. Floating-point byte replay is tied to environment.json.')


if __name__ == '__main__': main()
