"""Verify packaged sources and reconstruct the four N14 memory calculations."""
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text())


def verify_files():
    official = read(ROOT/'upstream_blobs.json')['blobs']
    prior = ROOT/'prior'
    actual = {p.relative_to(prior).as_posix() for p in prior.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts}
    assert actual == set(official), actual.symmetric_difference(official)
    for name, expected in official.items():
        data = (prior/name).read_bytes()
        digest = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert digest == expected, name
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        checksum, name = line.split('  ',1)
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == checksum, name


def compare(expected, result, path):
    assert type(expected) is type(result), path
    if isinstance(expected, dict):
        assert expected.keys() == result.keys(), path
        for k in expected:
            compare(expected[k], result[k], (*path,k))
    elif isinstance(expected, list):
        assert len(expected)==len(result), path
        for i,(a,b) in enumerate(zip(expected,result)):
            compare(a,b,(*path,i))
    elif isinstance(expected, float):
        assert math.isclose(expected,result,rel_tol=2e-8,abs_tol=1e-26), (path,expected,result)
    else:
        assert expected == result, path


def main():
    if not __debug__:
        raise RuntimeError('Run with assertions enabled.')
    verify_files()
    env = dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
    env.pop('PYTHONOPTIMIZE',None)
    with TemporaryDirectory() as scratch:
        for name in ('prediction','candidates','boundary','selection'):
            print('Recomputing',name,flush=True)
            dest = Path(scratch)/(name+'.json')
            subprocess.run([sys.executable,'-B',str(ROOT/(name+'.py')),str(dest)],env=env,check=True)
            compare(read(ROOT/dest.name),read(dest),(name,))
    print('PASS — source identity, exact certificates, endpoint ranks and two-density readout.')


if __name__ == '__main__':
    main()
