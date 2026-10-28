"""Explicit imports of frozen predecessors; no predecessor source is modified."""
import gzip, hashlib, importlib.util, json, sys
from pathlib import Path
import numpy as np
from flint import arb, acb, ctx

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
V07=HERE.parent/'scalar_propagation_v0_7'
sys.path.insert(0,str(V07))
from common import old,check,sha,digest,write,balls,load
import geometry
legacy_fields=load('v08_legacy_fields',HERE.parent/'scalar_pilot_v0_1/fields.py')
def plan():return json.loads((HERE/'PROTOCOL.json').read_text())
def pack(z):
    z=acb(z);check(z.is_finite(),'finite enclosure')
    s=[z.real.str(45,more=True),z.imag.str(45,more=True)]
    check(arb(s[0]).contains(z.real) and arb(s[1]).contains(z.imag),'outward decimal serialization')
    return s
def unpack(s):return acb(arb(s[0]),arb(s[1]))
def gzwrite(path,data):
    with open(path,'wb') as raw:
        with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as f:
            f.write(json.dumps(data,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode())
def gzread(path):
    with gzip.open(path,'rt') as f:return json.load(f)
def norm(z):
    return ((sum(x.abs_lower()**2 for x in z)/len(z)).sqrt().lower(),
            (sum(x.abs_upper()**2 for x in z)/len(z)).sqrt().upper())
def real_interval(lo,hi):return [pack(lo),pack(hi)]
def freeze_check():
    doc=json.loads((HERE/'FREEZE.json').read_text())
    for name,d in doc['files'].items():check(sha(HERE/name)==d,'frozen source '+name)
    return doc

class Recorded:
    def __init__(self,g):self.g=g;self.h=hashlib.sha256()
    def __getattr__(self,name):
        def call(*a,**kw):
            out=getattr(self.g,name)(*a,**kw);v=np.asarray(out)
            self.h.update(name.encode()+v.dtype.str.encode()+str(v.shape).encode()+np.ascontiguousarray(v).tobytes())
            return out
        return call

def draw(d,i):
    p=plan();entropy=[2,8,1,d,i,1,p['rng']['master_seed']]
    g=Recorded(np.random.Generator(np.random.PCG64DXSM(np.random.SeedSequence(entropy))))
    n=int(g.poisson(p['nu'][d]))
    x=old.points(g,n) if n<=p['resources']['max_points_per_cloud'] else None
    return x,{'entropy':entropy,'N':n,'rng_draw_output_sha256':g.h.hexdigest()}
