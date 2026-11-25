"""Analytical four-volumes, Poisson acceptance thresholds and design probabilities."""
from fractions import Fraction as Q
from functools import lru_cache
from math import pi
from itertools import product
from pathlib import Path
import sys
import numpy as np
from scipy.stats import poisson
from auslese import END, TICKS, TAIL, LAMBDA0
sys.path.insert(0,str(Path(__file__).resolve().parent/'basis'))
from geometrie import deformation, volume, sphere

TARGETS=(Q(1,4),Q(1,2),Q(3,4))
CASES=tuple(product(TARGETS,('A','B')))
NS=(16,32,64,128,256)
MS=(32,64,128,256,512,1024)
FACTORS=tuple(2**k for k in range(13))


def primitive(x):
    if x<=0: return Q(0)
    if x>=1: return x-Q(1,2)
    return x**6-3*x**5+Q(5,2)*x**4


def average_d(z,case,a,b):
    shift=1 if case=='A' else 0
    fast=(primitive(64*(b-z)+shift)-primitive(64*(a-z)+shift))/64
    return (Q(199,5000)*(primitive(b)-primitive(a))+Q(161,625)*fast)/(b-a)


def four_volume(z,case,a,b,lo,hi):
    """T and r factors in native units. Time integral is exact rational."""
    d=average_d(z,case,a,b)
    return 4*pi*1000*END*float(b-a)*float(volume(d,hi)-volume(d,lo))


@lru_cache(maxsize=None)
def layout(n,m):
    h=Q(1,m)
    step=Q(1,TICKS)
    # A rational outer enclosure of one tick of radial error divided by R0.
    radial_guard=Q(373,100)*step/10
    assert float(radial_guard)>END/TICKS/10
    v0=[];vi=[];vo=[];truth=[]
    for z,case in CASES:
        w=Q(1,n)
        base_in=four_volume(z,case,z,z+h,1-w,Q(1))
        base_out=four_volume(z,case,z-h,z,Q(1),1+w)
        inner=four_volume(z,case,z+step,z+h-step,1-w+radial_guard,Q(1))
        outer=four_volume(z,case,z-h-step,z+step,Q(1),1+w+radial_guard)
        assert 0<inner<base_in and 0<base_out<outer
        vi.append(inner);vo.append(outer);v0.append([base_in,base_out])
        truth.append(float(100*sphere(deformation(case,z,z),Q(1))))
    norm=4*pi*(10/n)*(END/m)
    ideal=np.sqrt(np.array(v0)/(norm*np.array(truth)[:,None]))
    assert np.all(ideal[:,0]<=1) and np.all(ideal[:,1]>=1)
    return np.array(vi),np.array(vo),np.array(truth),norm,float(np.max(abs(ideal-1)))


def screen(n,m):
    vi,vo,r2,norm,operator=layout(n,m)
    densities=LAMBDA0*np.array(FACTORS)[:,None]
    lower_boundary=densities*norm*r2*.95**2*1.01
    upper_boundary=densities*norm*r2*1.05**2*.99
    # Invert monotone Garwood limits as integer thresholds using Poisson tails.
    kmin=poisson.isf(TAIL,lower_boundary).astype(np.int64)+1
    kmax=poisson.ppf(TAIL,upper_boundary).astype(np.int64)-1
    small=poisson.cdf(kmin-1,densities*vi*.99)
    large=poisson.sf(kmax,densities*vo*1.01)
    joint=np.maximum(0.,1-(small+large).sum(axis=1)-2*TAIL*len(CASES))
    return joint,operator


def select():
    by_factor={f:[] for f in FACTORS}
    for n,m in product(NS,MS):
        power,op=screen(n,m)
        for f,p in zip(FACTORS,power):
            by_factor[f].append({'factor':f,'n':n,'m':m,'joint_lower':float(p),'operator':op})
    rows={}; winners={}
    for name,cap in (('total',1.),('operator_cap',.0075)):
        rows[name]=[]
        for f,group in by_factor.items():
            ok=[r for r in group if r['operator']<=cap]
            best=max(ok,key=lambda r:r['joint_lower'])
            rows[name].append(best)
            if best['joint_lower']>=.95 and name not in winners:
                winners[name]=best
    return winners,rows

if __name__=='__main__':
    import json
    w,rows=select()
    print(json.dumps(w,indent=2))
    for group,val in rows.items():
        print(group,[(r['factor'],round(r['joint_lower'],4),r['n'],r['m']) for r in val[:10]])
