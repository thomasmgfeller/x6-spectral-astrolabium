"""Poisson geometry, interval kernel, smoothed 4D BD operator and retarded solve."""
from pathlib import Path
import ctypes
import hashlib
import json
import subprocess
import tempfile
import numpy as np
from scipy.linalg import solve_triangular

HERE = Path(__file__).resolve().parent
def protocol():
    return json.loads((HERE/'PROTOCOL.json').read_text())
def digest(a):
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
def rng(d, i, scenario=1):
    return np.random.Generator(np.random.PCG64DXSM(np.random.SeedSequence(
        [1,scenario,d,i,1,protocol()['master_seed']])) )
def volume(h):
    return 2*np.pi*h**4/3
def points(g, n, h=4.):
    t = h*(1-g.random(n)**.25)*g.choice([-1.,1.],n)
    direction = g.normal(size=(n,3))
    direction /= np.linalg.norm(direction,axis=1)[:,None]
    r = (h-np.abs(t))*g.random(n)**(1/3)
    x = np.column_stack([t,direction*r[:,None]])
    return np.ascontiguousarray(x[np.argsort(x[:,0],kind='stable')])
def sprinkle(d, i):
    g = rng(d,i)
    n = int(g.poisson(protocol()['nu'][d]))
    if n>protocol()['max_inner_points']: raise RuntimeError('RESOURCE_HOLD: Poisson count cap')
    return points(g,n)
def extend(x,d,i):
    g = rng(d,i,scenario=2)
    rho = protocol()['nu'][d]/volume(4)
    n = int(g.poisson(rho*(volume(5)-volume(4))))
    if n+len(x)>protocol()['max_outer_points']: raise RuntimeError('RESOURCE_HOLD: shell count cap')
    pieces=[]; remaining=n
    while remaining:
        z=points(g,max(256,2*remaining),5)
        z=z[np.abs(z[:,0])+np.linalg.norm(z[:,1:],axis=1)>=4][:remaining]
        pieces.append(z); remaining-=len(z)
    shell=np.concatenate(pieces) if pieces else np.empty((0,4))
    y=np.concatenate([x,shell]); y=y[np.argsort(y[:,0],kind='stable')]
    return np.ascontiguousarray(y)
def probes():
    spatial = [[0.,0.,0.]]
    for j in range(3):
        for sign in [-1,1]:
            v=[0.,0.,0.];v[j]=sign*.5;spatial.append(v)
    inner=np.array([[t,*v] for t in [-.5,0,.5] for v in spatial])
    detector=np.array([[1.,*(np.array(v)*.5+np.array([0,0,1.5]))] for v in spatial])
    boundary=np.array([[-2.,0,0,0],[2.,0,0,0],[0,0,0,2.],[0,0,0,-2.]])
    return np.concatenate([inner,detector,boundary])
_lib=None
def counts(x,p=None,full=True):
    global _lib
    if _lib is None:
        dst=Path(tempfile.gettempdir())/('cspp_scalar_'+hashlib.sha256((HERE/'counts.cpp').read_bytes()).hexdigest()[:16]+'.so')
        subprocess.run(['g++','-O3','-std=c++17','-shared','-fPIC',str(HERE/'counts.cpp'),'-o',str(dst)],check=True)
        _lib=ctypes.CDLL(str(dst))
        _lib.interval_counts.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p]
        _lib.interval_counts.restype=ctypes.c_int64
    x=np.ascontiguousarray(x,dtype=np.float64)
    p=np.ascontiguousarray(probes() if p is None else p,dtype=np.float64)
    if x.ndim!=2 or x.shape[1]!=4 or p.ndim!=2 or p.shape[1]!=4 or not np.isfinite(x).all() or not np.isfinite(p).all() or np.any(np.diff(x[:,0])<0):
        raise ValueError('finite time-sorted 4D coordinates required')
    a=np.empty((len(x),len(x)),np.int32) if full else None
    b=np.empty((len(p),len(x)),np.int32)
    unresolved=_lib.interval_counts(x.ctypes.data,len(x),p.ctypes.data,len(p),a.ctypes.data if full else None,b.ctypes.data)
    if unresolved: raise RuntimeError(f'GEOMETRY_HOLD: {unresolved} unresolved near-null comparisons')
    return a,b
def weights(n,e):
    if not 0<e<=1: raise ValueError('epsilon must lie in (0,1]')
    n=np.asarray(n)
    out=np.zeros(n.shape)
    good=n>=0; z=n[good].astype(float)
    if e==1:
        v=np.zeros(z.shape)
        for k,c in enumerate([1.,-9.,16.,-8.]):v[z==k]=c
    else:
        u=e/(1-e)
        v=(1-e)**z*(1-9*z*u+8*z*(z-1)*u*u-(4/3)*z*(z-1)*(z-2)*u**3)
    out[good]=v
    return out
def scale(rho,e):
    return 4/np.sqrt(6)*np.sqrt(e*rho)
def apply(pc,rho,e,phi,phi_p):
    return scale(rho,e)*(-phi_p+e*weights(pc,e)@phi)
def propagate(c,pc,x,p,rho,e,history,J,Jp,masses):
    """Oracle-history diagnostic: exact prescribed past at t<=-1, not a Cauchy adapter.

    Returns probe amplitudes and normalized algebraic backward residuals.
    Last RHS is a unit history perturbation with zero forcing (m=1).
    """
    active=int(np.searchsorted(x[:,0],p[:,0].max(),side='left'))
    nh=int(np.searchsorted(x[:active,0],-1.,side='right'))
    a=scale(rho,e)
    w=weights(c[:active,:active],e)
    wp=weights(pc[:,:active],e)
    out=np.array(history[:active],copy=True)
    residual=[]
    for m in sorted(set(masses)):
        cols=np.flatnonzero(np.asarray(masses)==m)
        rhs=a*e*w[nh:,:nh]@out[:nh,cols]-J[nh:active,cols]
        mat=-a*e*w[nh:,nh:]
        np.fill_diagonal(mat,a+m*m)
        sol=solve_triangular(mat,rhs,lower=True,check_finite=True)
        out[nh:,cols]=sol
        defect=mat@sol-rhs
        denom=np.abs(mat)@np.abs(sol)+np.abs(rhs)
        residual.append(float(np.max(np.abs(defect)/np.maximum(denom,np.finfo(float).tiny),initial=0)))
    result=(a*e*wp@out-Jp)/(a+np.asarray(masses)**2)[None,:]
    if not np.isfinite(result).all(): raise RuntimeError('NUMERICAL_HOLD: nonfinite propagation')
    return result,max(residual,default=0)
