import gzip,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb
HERE=Path(__file__).resolve().parent
def require(ok,message):
    if not bool(ok):raise ArithmeticError(message)
def ball(x):return arb(str(x))
def enc(x):
    x=arb(x);require(x.is_finite(),'finite ball')
    s=x.str(55,more=True);require(arb(s).contains(x),'outward serialization');return s
def write(path,value):
    data=(json.dumps(value,sort_keys=True,indent=None if str(path).endswith('.gz') else 2)+'\n').encode()
    if str(path).endswith('.gz'):
        with gzip.GzipFile(filename=str(path),mode='wb',mtime=0) as f:f.write(data)
    else:Path(path).write_bytes(data)
