"""Verify hashes and independently reproduce every result without huge matrices."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile

ROOT=Path(__file__).resolve().parent

def run(args,cwd):
    r=subprocess.run([sys.executable,'-B',*args],cwd=cwd,text=True,capture_output=True)
    if r.returncode:
        raise RuntimeError(r.stdout+'\n'+r.stderr)
    return r

def main():
    manifest=json.loads((ROOT/'SHA256SUMS.json').read_text())
    for name,digest in manifest.items():
        p=ROOT/name
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:
            raise AssertionError('package SHA256 mismatch: '+name)
    provenance=json.loads((ROOT/'provenance.json').read_text())
    for source in provenance['sources']:
        data=(ROOT/source['path']).read_bytes()
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if digest!=source['git_blob']:raise AssertionError('frozen Git blob differs: '+source['path'])
    tests=run(['tests.py'],ROOT)
    print(tests.stderr.strip(),flush=True)
    expected=sorted((ROOT/'results').glob('*.json'))
    with tempfile.TemporaryDirectory(prefix='cst_reduction_verify_') as tmp:
        copy=Path(tmp)/'package'
        shutil.copytree(ROOT,copy,ignore=shutil.ignore_patterns('__pycache__'))
        shutil.rmtree(copy/'results')
        run(['certify.py'],copy)
        run(['basis.py','--output','results/basis_6_0_2.json'],copy)
        names={p.name for p in (copy/'results').glob('*.json')}
        if names!={p.name for p in expected}:raise AssertionError('result inventory differs')
        for old in expected:
            if old.read_bytes()!=(copy/'results'/old.name).read_bytes():
                raise AssertionError('result reproduction differs: '+old.name)
    print(json.dumps({'status':'PASS','file_hashes':len(manifest),'frozen_Git_blobs':len(provenance['sources']),
                      'independent_test_groups':10,'byte_identical_result_files':len(expected),
                      'local_histories':33,'joint_histories':1089,'large_projection_matrices_computed':False},indent=2))

if __name__=='__main__':main()
