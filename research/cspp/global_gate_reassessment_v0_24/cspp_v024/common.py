import gzip,json
from pathlib import Path
from flint import arb
HERE=Path(__file__).resolve().parent
def require(ok,message):
    if not bool(ok):raise ArithmeticError(message)
def enc(x):
    x=arb(x);require(x.is_finite(),'finite interval');s=x.str(55,more=True)
    require(arb(s).contains(x),'outward serialization');return s
def read(name):
    p=HERE/name
    if p.suffix=='.gz':
        with gzip.open(p,'rt') as f:return json.load(f)
    return json.loads(p.read_text())
def write(name,data):
    p=HERE/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,indent=2,sort_keys=True,ensure_ascii=False)+'\n')
def close(a,b,tolerance='1e-24'):
    a=arb(a);b=arb(b)
    require(abs(a-b).upper()<=arb(tolerance)*(1+abs(a).upper()+abs(b).upper()),'arithmetic consistency')
