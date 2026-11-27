"""Load the published order and fully define the fixed collar."""
from contextlib import contextmanager
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import sys

ROOT=Path(__file__).resolve().parent
PIN='95072b5b3fd12d4fb1ede57117da4e7eaff19a26efd24fa733f38c801b0a41a1'
PAST=(0,1,2,3)
LATE=(7,8,9,10)
QSTAR=F('0.181585581308965')

@contextmanager
def experiment():
    pkg=ROOT/'basis/Radiuspilot.zip'
    assert sha256(pkg.read_bytes()).hexdigest()==PIN
    with TemporaryDirectory() as work, ZipFile(pkg) as z:
        z.extractall(work)
        sys.path.insert(0,work)
        from pilotfelder import archive
        with archive() as (rows,order,coeff,free,goals):
            row,=(r for kind,choice,r in rows if kind=='Feld' and choice==['y10','w10'] and F(r['source'])==0)
            y,w=([sum(map(F,b))/2 for b in row[k]] for k in ('y','w'))
            assert -sum(goals[1:])==QSTAR
            yield y,w,order,coeff,free
