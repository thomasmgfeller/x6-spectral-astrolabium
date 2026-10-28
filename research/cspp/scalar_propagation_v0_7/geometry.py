"""Full endpoint relations and interval counts for exact archived binary64 inputs."""
import ctypes,subprocess,tempfile
from fractions import Fraction
from pathlib import Path
import numpy as np
from common import HERE,check,sha
_lib=None
CALLBACK=ctypes.CFUNCTYPE(ctypes.c_int,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double))
@CALLBACK
def exact_sign(a,b):
    d=[Fraction(float(b[k]))-Fraction(float(a[k])) for k in range(4)]
    q=d[0]*d[0]-sum(v*v for v in d[1:])
    return 1 if q>0 else -1 if q<0 else 0
def library():
    global _lib
    if _lib is None:
        path=Path(tempfile.gettempdir())/('cspp_v07_exact_'+sha(HERE/'geometry.cpp')[:20]+'.so')
        subprocess.run(['g++','-O2','-std=c++17','-fno-fast-math','-ffp-contract=off','-shared','-fPIC',str(HERE/'geometry.cpp'),'-o',str(path)],check=True)
        _lib=ctypes.CDLL(str(path));P=ctypes.c_void_p
        _lib.set_exact_sign.argtypes=[CALLBACK];_lib.set_exact_sign(exact_sign)
        _lib.causal_inventory.argtypes=[P,ctypes.c_int,P,ctypes.c_int,P,P,P,P,P]
        _lib.causal_inventory.restype=ctypes.c_int
        _lib.relation.argtypes=[P,P,P];_lib.relation.restype=ctypes.c_int
        _lib.region_membership.argtypes=[P,ctypes.c_int,ctypes.c_double,P,P]
    return _lib
def inventory(x,p,full=True):
    x=np.ascontiguousarray(x,dtype=np.float64);p=np.ascontiguousarray(p,dtype=np.float64)
    check(x.ndim==p.ndim==2 and x.shape[1]==p.shape[1]==4,'4D coordinates')
    check(np.isfinite(x).all() and np.isfinite(p).all(),'finite exact dyadic coordinates')
    check(np.all(np.diff(x[:,0])>=0),'time ordering')
    # Prevent overflow and subnormal intermediate issues in the fast filter;
    # all actual project coordinates satisfy this elementary range guard.
    check(np.max(np.abs(x),initial=0)<2**100 and np.max(np.abs(p),initial=0)<2**100,'coordinate magnitude guard')
    n,m=len(x),len(p);w=(n+63)//64
    c=np.empty((n,n),dtype=np.int32) if full else None;pc=np.empty((m,n),dtype=np.int32)
    past=np.empty((n,w),dtype=np.uint64);ppast=np.empty((m,w),dtype=np.uint64);stats=np.zeros(3,dtype=np.int64)
    rc=library().causal_inventory(x.ctypes.data,n,p.ctypes.data,m,c.ctypes.data if full else None,pc.ctypes.data,past.ctypes.data,ppast.ctypes.data,stats.ctypes.data)
    check(rc==0,'IEEE binary64 required')
    return c,pc,past,ppast,{'comparisons':int(stats[0]),'exact_fallbacks':int(stats[1]),'exact_null_pairs':int(stats[2])}
def relation(a,b):
    a=np.array(a,dtype=np.float64);b=np.array(b,dtype=np.float64);s=np.zeros(3,dtype=np.int64)
    check(np.isfinite(a).all() and np.isfinite(b).all() and a.shape==b.shape==(4,),'finite relation inputs')
    return bool(library().relation(a.ctypes.data,b.ctypes.data,s.ctypes.data)),s.tolist()

def region(x,h):
    x=np.ascontiguousarray(x,dtype=np.float64);mask=np.empty(len(x),np.uint8);stats=np.zeros(3,np.int64)
    check(x.ndim==2 and x.shape[1]==4 and np.isfinite(x).all() and h in [4,5],'declared exact domain input')
    library().region_membership(x.ctypes.data,len(x),h,mask.ctypes.data,stats.ctypes.data)
    return mask,stats.tolist()
