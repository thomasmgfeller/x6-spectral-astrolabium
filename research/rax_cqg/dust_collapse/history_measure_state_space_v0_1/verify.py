"""Reproduce the stage 3/4 tests from the archived finite N14 data."""
import hashlib
import json
import math
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent


def compare(left, right, path=()):
    assert type(left) is type(right), path
    if isinstance(left, dict):
        assert left.keys() == right.keys(), path
        for k in left:
            compare(left[k], right[k], (*path,k))
    elif isinstance(left, list):
        assert len(left) == len(right), path
        for i,(a,b) in enumerate(zip(left,right)):
            compare(a,b,(*path,i))
    elif isinstance(left, float):
        # Close-to-zero residuals in diagnostics may vary at machine precision.
        # The full-family second differences are much smaller than ordinary
        # readout values, so compare those outputs on their own absolute scale.
        floor = 2e-20 if path[0] == 'descent' else 2e-13
        assert math.isclose(left, right, abs_tol=floor, rel_tol=3e-8), (path,left,right)
    else:
        assert left == right, (path,left,right)


def main():
    if not __debug__:
        raise RuntimeError("Run with Python assertions enabled")
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        h,n=line.split('  ',1)
        assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h, n
    env=dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    env.pop('PYTHONOPTIMIZE', None)
    with TemporaryDirectory() as tmp:
        dest=Path(tmp)
        for name in ('weights','local_growth','memory','cuts','sector','response','descent'):
            filename=name+'.json'
            args=[]
            if name=='response':
                args=['--sector', dest/'sector.json']
            if name=='descent':
                args=['--inputs',dest]
            print('Checking',name,flush=True)
            subprocess.run([sys.executable,'-B',str(ROOT/(name+'.py')),*args,str(dest/filename)],
                           env=env,check=True)
            compare(json.loads((ROOT/filename).read_text()),
                    json.loads((dest/filename).read_text()), (name,))
    print('PASS: both growth candidates, cuts, scalar sector, coherent readout and full-family differences.')


if __name__ == '__main__':
    main()
