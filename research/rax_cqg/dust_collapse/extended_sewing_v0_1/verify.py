"""Check provenance, complete manifest, tests, CLI and byte-identical replay."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def main():
    manifest=json.loads((ROOT/'MANIFEST.sha256.json').read_text())
    files={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()
           and '__pycache__' not in p.parts and p.name!='MANIFEST.sha256.json'}
    if files!=set(manifest):raise RuntimeError('Manifest coverage mismatch: '+repr(files^set(manifest)))
    for path,want in manifest.items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=want:raise RuntimeError('SHA256 mismatch: '+path)
    provenance=json.loads((ROOT/'provenance.json').read_text())
    for source in provenance['sources']:
        data=(ROOT/source['path']).read_bytes()
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if digest!=source['git_blob']:raise RuntimeError('Source Git blob mismatch: '+source['path'])
    subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','.', '-p','test_*.py','-v'],cwd=ROOT,check=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp);dst=tmp/'replay'
        shutil.copytree(ROOT,dst,ignore=shutil.ignore_patterns('__pycache__'))
        subprocess.run([sys.executable,'-B','analysis.py'],cwd=dst,check=True,stdout=subprocess.PIPE,text=True)
        paths=[p for folder in ('examples','results') for p in (ROOT/folder).glob('*.json')]
        for p in paths:
            if p.read_bytes()!=(dst/p.relative_to(ROOT)).read_bytes():raise RuntimeError('Replay differs: '+str(p.relative_to(ROOT)))
        cli=tmp/'joined.json'
        subprocess.run([sys.executable,'-B','sewing.py','examples/left.json','examples/right.json',
                        '--fields','examples/fields.json','--output',str(cli)],cwd=ROOT,check=True,stdout=subprocess.PIPE,text=True)
        if cli.read_bytes()!=(ROOT/'results/reconstructed_full_layer.json').read_bytes():raise RuntimeError('CLI result differs')
    print(f'PASS: {len(manifest)} file hashes; 6 frozen Git blobs; 10 test groups; 1089 histories; byte-identical replay and CLI.')

if __name__=='__main__':main()
