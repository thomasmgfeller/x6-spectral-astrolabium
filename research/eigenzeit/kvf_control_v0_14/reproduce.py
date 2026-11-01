"""Verify package hashes, run in a clean directory and compare all results."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
import numpy as np

HERE=Path(__file__).resolve().parent


def close(a,b,path='root'):
    if isinstance(a,dict):
        assert isinstance(b,dict) and a.keys()==b.keys(),path
        for k in a:close(a[k],b[k],path+'.'+k)
    elif isinstance(a,list):
        assert isinstance(b,list) and len(a)==len(b),path
        for i,(x,y) in enumerate(zip(a,b)):close(x,y,path+f'[{i}]')
    elif isinstance(a,float):
        assert np.isclose(a,b,rtol=2e-11,atol=2e-13), (path,a,b)
    else:assert a==b,(path,a,b)


def main():
    paths={}
    for line in (HERE/'MANIFEST.sha256').read_text().splitlines():
        sha,path=line.split(None,1)
        assert path not in paths and not Path(path).is_absolute() and '..' not in Path(path).parts
        assert hashlib.sha256((HERE/path).read_bytes()).hexdigest()==sha,path
        paths[path]=sha
    actual={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    assert actual==set(paths)|{'MANIFEST.sha256'},'inventory mismatch'
    origin=json.loads((HERE/'previous/ORIGIN.json').read_text())
    for name,sha in origin['files'].items():assert hashlib.sha256((HERE/'previous'/name).read_bytes()).hexdigest()==sha
    with tempfile.TemporaryDirectory() as work:
        root=Path(work)
        for name in ['certificate.py','model.py','gum.py','run.py','check.py','CONTRACT.json','FREEZE.sha256']:
            shutil.copyfile(HERE/name,root/name)
        env=os.environ.copy();env['OPENBLAS_NUM_THREADS']='1';env['OMP_NUM_THREADS']='1'
        for name in ['certificate.py','run.py','check.py']:
            subprocess.run([sys.executable,'-B',name],cwd=root,env=env,check=True)
        records=['certificate','M0','M1','campaign','controls','check','summary']
        exact=[]
        for name in records:
            p=f'records/{name}.json'
            close(json.loads((HERE/p).read_text()),json.loads((root/p).read_text()),p)
            exact.append((HERE/p).read_bytes()==(root/p).read_bytes())
        raw=list((HERE/'raw').glob('*.npy'))
        for p in raw:
            assert p.read_bytes()==(root/'raw'/p.name).read_bytes(),p.name
        print(json.dumps({'status':'CLEAN_REPLAY_PASS','records_compared':len(records),
                          'records_byte_identical':sum(exact),'raw_files_byte_identical':len(raw),
                          'manifest_files':len(paths)},indent=2))


if __name__=='__main__':main()
