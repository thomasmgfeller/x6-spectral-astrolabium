"""Check the package, upstream Git objects and a fresh reconstruction of the study."""
from hashlib import sha1,sha256
import json
from math import isclose
from pathlib import Path
from run import compute

BASE=Path(__file__).resolve().parent


def compare(actual,expected,path=()):
    if isinstance(expected,dict):
        assert actual.keys()==expected.keys(),path
        for k in expected:
            compare(actual[k],expected[k],(*path,k))
    elif isinstance(expected,list):
        assert len(actual)==len(expected),path
        for i,(left,right) in enumerate(zip(actual,expected)):
            compare(left,right,(*path,i))
    elif isinstance(expected,float):
        assert isclose(actual,expected,rel_tol=2e-10,abs_tol=1e-13),(path,actual,expected)
    else:
        assert actual==expected,(path,actual,expected)


if __name__=='__main__':
    if not __debug__:
        raise RuntimeError('Keep assertions enabled')
    for line in (BASE/'SHA256SUMS').read_text().splitlines():
        checksum,name=line.split('  ',1)
        assert sha256((BASE/name).read_bytes()).hexdigest()==checksum,name
    provenance=json.loads((BASE/'provenance.json').read_text())
    for name,record in provenance['inputs'].items():
        data=(BASE/name).read_bytes()
        assert sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==record['git_blob'],name
    compare(compute(),json.loads((BASE/'result.json').read_text()))
    print('PASS — prefix 1564')
