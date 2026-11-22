"""Apply the same coverage certificate to remaining individual density centres."""
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as Q
from hashlib import sha256
import json
import sys

from teilung import ROOT, split_row


def evaluate():
    source=json.loads((ROOT/'zeugen.json').read_text())['rows']
    done=json.loads((ROOT/'teilung.json').read_text())['rows']
    keys=sorted(k for k,v in source.items() if not v['witness'] and k not in done)
    cases=[(int(code),Q(rho)) for code,rho in (k.split(';') for k in keys)]
    with ProcessPoolExecutor(max_workers=2) as pool:
        return dict(pool.map(split_row,cases))


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Use Python without -O.')
    digest,name=(ROOT/'restzeilenplan.sha256').read_text().split()
    assert sha256((ROOT/name).read_bytes()).hexdigest()==digest
    result=evaluate()
    if '--emit' in sys.argv:
        print(json.dumps(result,indent=2,sort_keys=True))
    else:
        assert result==json.loads((ROOT/'restzeilen.json').read_text())
        print('PASS', {k:v['passes'] for k,v in result.items()})
