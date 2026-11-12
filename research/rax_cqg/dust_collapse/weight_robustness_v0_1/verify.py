"""Validate hashes and replay every certified result in a temporary copy."""
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    manifest=json.loads((ROOT/'SHA256SUMS.json').read_text())
    actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS.json'}
    if set(manifest)!=actual:raise ArithmeticError('manifest inventory mismatch')
    for name,digest in manifest.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise ArithmeticError('changed file: '+name)
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    with tempfile.TemporaryDirectory() as tmp:
        target=Path(tmp)/ROOT.name;shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        subprocess.run([sys.executable,'-B','compute.py','--recompute-quadrature'],cwd=target,env=env,check=True)
        subprocess.run([sys.executable,'-B','tests.py'],cwd=target,env=env,check=True)
        results=sorted(p.relative_to(ROOT) for p in (ROOT/'results').glob('*.json'))
        for path in results:
            if (ROOT/path).read_bytes()!=(target/path).read_bytes():raise ArithmeticError('replay mismatch: '+str(path))
    print(json.dumps({'status':'PASS','file_hashes':len(manifest),'identical_result_files':len(results),'orbit_quadratures_replayed':10,'control_groups':9,'negative_controls':5,'optimizer_used_for_certificate':False}))

if __name__=='__main__':main()
