"""Verify inventory and frozen sources, run from fresh directory, compare raw and records."""
import hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent


def compare(a,b,path=''):
    if isinstance(a,dict):
        assert a.keys()==b.keys(),path
        for k in a:compare(a[k],b[k],path+'/'+k)
    elif isinstance(a,list):
        assert len(a)==len(b),path
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'/'+str(i))
    elif isinstance(a,(int,float)) and not isinstance(a,bool):
        np.testing.assert_allclose(a,b,rtol=2e-10,atol=2e-12,err_msg=path)
    else:assert a==b,path


def run():
    expected={p:h for h,p in (l.split(None,1) for l in (ROOT/'MANIFEST.sha256').read_text().splitlines())}
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST.sha256'}
    assert actual==set(expected)
    for p,h in expected.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
    source=['CONTRACT.json','FREEZE.sha256','model.py','certificate.py','gum.py','run.py','check.py','reproduce.py','requirements.txt']
    with tempfile.TemporaryDirectory() as temp:
        work=Path(temp)
        for folder in ['raw','records']: (work/folder).mkdir()
        for p in source:shutil.copy2(ROOT/p,work/p)
        env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
        for p in ['run.py','check.py']:subprocess.run([sys.executable,'-B',p],cwd=work,env=env,check=True,stdout=subprocess.DEVNULL)
        records=['certificate','M0','M1','campaign','summary','check'];byte_equal=0
        for p in records:
            x=ROOT/'records'/f'{p}.json';y=work/'records'/f'{p}.json'
            compare(json.loads(x.read_text()),json.loads(y.read_text()),p)
            byte_equal+=x.read_bytes()==y.read_bytes()
        raw=list((ROOT/'raw').glob('*.npy'))
        for p in raw:assert p.read_bytes()==(work/'raw'/p.name).read_bytes(),p.name
    print(json.dumps(dict(status='CLEAN_REPLAY_PASS',records_compared=len(records),records_byte_identical=byte_equal,raw_files_byte_identical=len(raw),manifest_files=len(expected)),indent=2))


if __name__=='__main__':run()
