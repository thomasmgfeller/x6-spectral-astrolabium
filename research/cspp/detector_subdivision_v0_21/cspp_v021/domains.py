"""Exact rational box counts and conservative normalized detector masses."""
from fractions import Fraction as F
import itertools, math
import numpy as np
from flint import arb
from overlap import point, before, ball

CENTER=(F(0),F(0),F(3,2))
WINDOWS=[(F(3,4),F(1)),(F(1),F(5,4))]

def relation_box_point(center,half,z,box_first=True):
    """All/possible strict causal relations. Possible is a superset."""
    t,*x=center;ht,*hx=half;z=point(z)
    dt=z[0]-t if box_first else t-z[0]
    far=sum((abs(v-w)+h)**2 for v,w,h in zip(x,z[1:],hx))
    near=sum(max(F(0),abs(v-w)-h)**2 for v,w,h in zip(x,z[1:],hx))
    all_yes=dt-ht>0 and (dt-ht)**2>far
    some_possible=dt+ht>0 and (dt+ht)**2>near
    return all_yes,some_possible

def mass_grid(n,fine=128):
    """Volumes of fully-inside fine voxels; no voxel is sampled at a point."""
    if fine%n:raise ValueError('nested grid required')
    lo=2*np.arange(fine,dtype=np.int64)-fine;hi=lo+2
    far=np.maximum(lo*lo,hi*hi)
    near=np.where((lo<=0)&(hi>=0),0,np.minimum(lo*lo,hi*hi))
    inside=(far[:,None,None]+far[None,:,None]+far[None,None,:])<=fine*fine
    possible=(near[:,None,None]+near[None,:,None]+near[None,None,:])<fine*fine
    g=fine//n
    counts=inside.reshape(n,g,n,g,n,g).sum(axis=(1,3,5))
    if not (ball(F(int(inside.sum()),fine**3))<=arb.pi()/6<=ball(F(int(possible.sum()),fine**3))):
        raise ArithmeticError('sphere mass enclosure')
    return counts,{'fine_grid':fine,'inside_voxels':int(inside.sum()),'possible_voxels':int(possible.sum()),
                  'total_voxels':fine**3,'inside_volume':str(F(int(inside.sum()),fine**3)),
                  'possible_volume':str(F(int(possible.sum()),fine**3))}

def detector_cells(n,wi,fine=128):
    masses,meta=mass_grid(n,fine);lo,hi=WINDOWS[wi]
    ht=(hi-lo)/(2*n);hx=F(1,2*n);lag=ht+F(7,4)*hx
    out=[]
    for ix in itertools.product(range(n),repeat=4):
        it,*xyz=ix;t=lo+(hi-lo)*F(2*it+1,2*n)
        x=tuple(c-F(1,2)+F(2*j+1,2*n) for c,j in zip(CENTER,xyz))
        mass=F(int(masses[tuple(xyz)]),fine**3*n)
        out.append({'index':ix,'center':(t,*x),'half':(ht,hx,hx,hx),
          'minus':(t-lag,*x),'plus':(t+lag,*x),'volume_time_fraction':mass,
          'probability_lower':ball(mass)*6/arb.pi()})
    return out,meta

def root_masks(c,q):
    half=(F(1,8),F(1,2),F(1,2),F(1,2)) # fixed v0.20 n=4 partition
    return np.array([relation_box_point(c['center'],half,z,True) for z in q],dtype=np.int16).T

def detector_masks(d,q):
    return np.array([relation_box_point(d['center'],d['half'],z,False) for z in q],dtype=np.int16).T

def whole_detector(wi):
    lo,hi=WINDOWS[wi]
    return {'minus':(lo-F(1,2),*CENTER),'plus':(hi+F(1,2),*CENTER)}
