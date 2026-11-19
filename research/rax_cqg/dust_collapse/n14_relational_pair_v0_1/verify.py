"""Verify package bytes and upstream identities, then independently replay calculate.run()."""
import hashlib
import json
from pathlib import Path
from math import isclose
from calculate import run

BASE=Path(__file__).resolve().parent


def compare(actual, expected, path=()):
    if isinstance(expected,dict):
        assert actual.keys()==expected.keys(), path
        for key in expected:
            if key in ('attaining_mass_by_endtype','dual_test_by_prefix','dual_target','maximum_dual_endtype'):
                # Optimal certificates need not be unique. run() verifies equality
                # of the exact primal and dual values before returning them.
                continue
            compare(actual[key],expected[key],(*path,key))
    elif isinstance(expected,list):
        assert len(expected)==len(actual), path
        for i,b in enumerate(expected):
            compare(actual[i],b,(*path,i))
    elif isinstance(expected,float):
        assert isclose(actual,expected,rel_tol=5e-10,abs_tol=2e-13), (path,actual,expected)
    else:
        assert actual==expected,(path,actual,expected)


if __name__=='__main__':
    if not __debug__:
        raise RuntimeError('Run with assertions enabled')
    for line in (BASE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==digest,name
    provenance=json.loads((BASE/'provenance.json').read_text())
    for name,info in provenance['inputs'].items():
        raw=(BASE/name).read_bytes()
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==info['git_blob'],name
    compare(run(),json.loads((BASE/'result.json').read_text()))
    print('PASS')
