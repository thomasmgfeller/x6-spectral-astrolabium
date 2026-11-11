"""Verify source identities and replay exact evidence in a temporary directory."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
from package import ROOT, MANIFEST, files


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    manifest = json.loads((ROOT/MANIFEST).read_text())
    actual = {str(p.relative_to(ROOT)) for p in files()}
    require(actual == set(manifest), 'Unexpected or missing package files')
    for name, expected in manifest.items():
        data = (ROOT/name).read_bytes()
        require(hashlib.sha256(data).hexdigest() == expected, 'Hash mismatch: '+name)
    provenance = json.loads((ROOT/'provenance.json').read_text())
    for source in provenance['sources']:
        data = (ROOT/source['local_path']).read_bytes()
        require(hashlib.sha256(data).hexdigest() == source['sha256'],
                'Pinned SHA-256 mismatch: '+source['local_path'])
        blob = b'blob '+str(len(data)).encode()+b'\0'+data
        require(hashlib.sha1(blob).hexdigest() == source['git_blob_sha'],
                'Pinned Git blob mismatch: '+source['local_path'])
    with tempfile.TemporaryDirectory(prefix='cst_scalar_verify_') as td:
        subprocess.run([sys.executable, str(ROOT/'build_evidence.py'), '--out', td],
                       check=True, cwd=ROOT)
        for name in ('checks.json','aa_hessians.json'):
            require((Path(td)/name).read_bytes() == (ROOT/'results'/name).read_bytes(),
                    'Recomputed evidence mismatch: '+name)
    contract = json.loads((ROOT/'action_contract.json').read_text())
    require(set(contract['physical_gates'].values()) == {'HOLD'}, 'Unexpected gate state')
    require(contract['physical_matrix_status'] == 'NOT_CONSTRUCTED',
            'Unexpected physical matrix claim')
    print(json.dumps({'status':'PASS', 'hashed_files':len(manifest),
                      'pinned_sources':len(provenance['sources']),
                      'replayed_results':2, 'physical_gates':'HOLD'}))


if __name__ == '__main__':
    main()
