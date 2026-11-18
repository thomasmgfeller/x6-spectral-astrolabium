"""Check the original files and repeat the production run in one local process at a time."""
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT=Path(__file__).resolve().parent
CONTRACT='40962cb379afe1f8544d96625136b9a6475f97a745fe1d3f86770d2b8568dca7'


def compare(a,b,path=()):
    if isinstance(a,dict):
        assert a.keys()==b.keys(),path
        for k in a:
            compare(a[k],b[k],(*path,k))
    elif isinstance(a,list):
        assert len(a)==len(b),path
        for i,(x,y) in enumerate(zip(a,b)):
            compare(x,y,(*path,i))
    elif isinstance(a,float):
        assert isinstance(b,(int,float)) and math.isclose(a,b,rel_tol=3e-8,abs_tol=5e-13),(path,a,b)
    else:
        assert a==b,(path,a,b)


def main():
    if not __debug__:
        raise RuntimeError('Run with assertions active')
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,path=line.split('  ',1)
        assert sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    assert sha256((ROOT/'study.json').read_bytes()).hexdigest()==CONTRACT
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE',None)
    with TemporaryDirectory() as tmp:
        clock=Path(tmp)/'clocks_all.json';result=Path(tmp)/'results.json'
        for script,args in [('quadrature.py',[clock]),('analysis_full.py',[clock,result])]:
            subprocess.run([sys.executable,'-B',str(ROOT/script),*args],env=env,check=True)
        for p in (clock,result):
            compare(json.loads((ROOT/p.name).read_text()),json.loads(p.read_text()))
    print('PASS: hashes, all 23 N13 clock/readout branches, four path laws, exact threshold bounds '
          'and fixed-marginal full-replacement maxima on both production grids.')


if __name__=='__main__':
    main()
