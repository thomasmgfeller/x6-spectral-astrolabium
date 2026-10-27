"""Shared bounded calibration settings; imports immutable v0.1 kernels."""
from pathlib import Path
import hashlib
import importlib.util
import json
import numpy as np

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'scalar_pilot_v0_1'
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
old=load('cspp_scalar_v01',OLD/'scalar.py')
oldref=load('cspp_reference_v01',OLD/'reference.py')
def plan():return json.loads((HERE/'PROTOCOL.json').read_text())
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def digest(a):return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
def write(path,value):Path(path).write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def modes():return np.array([[0.,0.],[.5,0.],[0.,.5],[.5,.5]]) # omega*L, k*L
def gaussian_fields(x,L=2.):
    envelope=np.exp(-np.sum(np.asarray(x)**2,axis=1)/(2*L*L))
    om,k=modes().T/L
    return envelope[:,None]*np.exp(1j*(x[:,3,None]*k-x[:,0,None]*om))
def exact_box(L):
    om,k=modes().T/L
    return -2/L**2+om**2-k**2
def cloud(d,i):
    g=np.random.Generator(np.random.PCG64DXSM(np.random.SeedSequence([1,3,d,i,1,plan()['master_seed']])) )
    n=int(g.poisson(plan()['nu_equivalent_Omega4'][d]))
    if n>plan()['point_cap']:raise RuntimeError('RESOURCE_HOLD: Poisson draw exceeds cap; no redraw')
    # I((-8,0,0,0),(0,0,0,0)) has exactly the volume of Omega4.
    x=old.points(g,n,4.);x[:,0]-=4.
    return np.ascontiguousarray(x)
