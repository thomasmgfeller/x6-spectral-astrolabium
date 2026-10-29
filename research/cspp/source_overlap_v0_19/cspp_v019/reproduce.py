"""Verify immutable package files and reproduce scientific JSON in isolation."""
import hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
RESULTS=('BOUNDS_384.json','BOUNDS_512.json','CHECKS.json')


def main():
    manifest=(HERE/'SHA256SUMS').read_text().splitlines()
    for line in manifest:
        digest,name=line.split('  ',1)
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=digest:
            raise RuntimeError('Package hash mismatch: '+name)
    with tempfile.TemporaryDirectory(prefix='cspp-v019-') as temp:
        root=Path(temp)
        for name in ['source_norms.py','kernel.py','run.py','verify.py','PROTOCOL.json','PROVENANCE.json']:
            shutil.copy2(HERE/name,root/name)
        shutil.copytree(HERE/'evidence',root/'evidence');(root/'results').mkdir()
        for args in [['run.py','--bits','384'],['run.py','--bits','512'],['verify.py']]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=root,text=True,capture_output=True)
            if p.returncode:raise RuntimeError(str(args)+'\n'+p.stdout+'\n'+p.stderr)
        for name in RESULTS:
            if json.loads((root/'results'/name).read_text())!=json.loads((HERE/'results'/name).read_text()):
                raise RuntimeError('Scientific JSON differs: '+name)
    print(json.dumps({'status':'PASS','package_hashes':len(manifest),'exact_reproductions':list(RESULTS)},indent=2))


if __name__=='__main__':main()
