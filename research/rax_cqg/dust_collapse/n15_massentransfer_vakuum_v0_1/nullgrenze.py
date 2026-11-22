"""Certified inner-atom and positive-limit responses, independent of the tensor quadrature."""
import json
from collections import defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from math import isqrt
from pathlib import Path
import sys
from auslese import settings
from intervalle import I,C,S,gaussian,cis,sinc,angle
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'quellen'))
from ordnung import PAST,INNER,FUTURE,ORDER

EDGES={(i,j): (1,-9,16,-8)[t-k-1] for k,i in enumerate(ORDER)
       for t,j in enumerate(ORDER) if 1<=t-k<=4}
LATE=INNER[-4:]
U=dict.fromkeys(PAST,1)
V=dict(zip(PAST,[Q(n,64) for n in (76,47,24,8)]))

@lru_cache(None)
def polynomial():
    """Polynomial for product(8*f), after averaging the first three clocks."""
    poly={(0,)*7:Q(1)}
    for j in range(7):
        constant=Q(3,2) if j in (0,6) else Q(1)
        slopes=[(0,1),(1,1)] if j==0 else ([(5,-1),(6,-1)] if j==6 else [(j-1,-1),(j+1,1)])
        new=defaultdict(Q)
        for powers,w in poly.items():
            new[powers]+=constant*w
            for k,sgn in slopes:
                key=list(powers);key[k]+=1
                new[tuple(key)]+=sgn*w/16
        poly=new
    out=defaultdict(Q)
    for k,v in poly.items():
        if any(ki%2 for ki in k[:3]):continue
        for ki in k[:3]:v/=ki+1
        out[k[3:]]+=v
    assert max(max(p) for p in out)==2
    return [(k,I.of(v)) for k,v in out.items() if v]

def moments(c0,c1,c2):
    # Expand exp(i c1*x+i c2*x²) about x=0. At radius 4 its modulus is < exp(4).
    assert 4*c1.absmax()+16*c2.absmax()<=4*S
    a=[C(1)]
    for j in range(1,41):
        t=a[-1].scale(c1)
        if j>=2:t=t+a[-2].scale(2*c2)
        a.append(C(-t.im/j,t.re/j))
    phase=cis(c0)
    vals=[]
    for k in (0,1,2):
        z=C(0)
        for j in range(k%2,41,2):z=z+a[j].scale(Q(1,k+j+1))
        vals.append(phase*z.pad(Q(1,2**74)))
    return vals

def factored(inner):
    unit=[v[0] for v in inner]
    atom=unit[0]*unit[1]*unit[2]*unit[3]
    weighted=C(0)
    for k,w in polynomial():
        val=inner[0][k[0]]*inner[1][k[1]]*inner[2][k[2]]*inner[3][k[3]]
        weighted=weighted+val.scale(w)
    return atom,weighted

def fixed_offset(delta,off):
    e=off/delta;D=4*delta-off
    inv=1/D.sqrt();clockwidth=(4-e)/64
    future=I.of(Q(-1,4))
    for (i,j),b in EDGES.items():
        if i in FUTURE and j in FUTURE:future-=Q(b*(j-i)**2,304)
    @lru_cache(None)
    def past_response(u,v,rho):
        y={j:I.of(j-5)+(e if j==3 else 0)+(u+V[j]*v)*inv for j in PAST}
        g=I.of(-2)
        for (i,j),b in EDGES.items():
            if j in PAST:g=g-Q(b,38)*(y[j]-y[i])**2
        return cis(rho*g).scale(sinc(g/32))
    @lru_cache(None)
    def inner_moments(j,shift):
        centre=I.of(-2)+e+(4-e)*Q(INNER.index(j)+1,8)+shift*inv
        c0,c1,c2=I.of(0),I.of(0),I.of(0)
        for f in FUTURE:
            b=Q(-EDGES.get((j,f),0),304)
            diff=f-5-centre
            c0=c0+b*diff**2
            c1=c1-2*b*diff*clockwidth
            c2=c2+b*clockwidth**2
        return moments(c0,c1,c2)
    @lru_cache(None)
    def future_response(a,b):
        return factored([inner_moments(j,a if j==11 else b if j==13 else 0) for j in LATE])
    out={}
    for label,(shifts,_) in settings().items():
        a,b,u,v,t=shifts
        common=cis(future-Q(7,8)*t/D)
        atom,limit=future_response(a,b)
        for rho in (Q(1,8),Q(1,4)):
            pq=common*past_response(u,v,rho)
            out[rho,'empty',label]=(pq*atom).scale(D**7)
            out[rho,'limit',label]=(pq*limit).scale(D**14)
    return out

def solve():
    root=isqrt(isqrt(3*S**4//722));delta=I(root,root+1)
    assert (delta.lo**4)*722<=3*S**4<(delta.hi**4)*722
    vals=defaultdict(lambda:C(0))
    for x,w in gaussian(80):
        for centre in (-Q(1,16),Q(1,16)):
            for key,z in fixed_offset(delta,I.of(centre)+x/32).items():
                vals[key]=vals[key]+z.scale(w/2)
    # Uniform Cauchy bound 2^100 at radius 2 in normalized outer coordinate.
    # Positive normalized Gaussian rule exact through degree 159, double tail.
    tail=Q(1,2**58)
    rows={}
    for rho,sector in product((Q(1,8),Q(1,4)),('empty','limit')):
        z0=vals[rho,sector,'0'].pad(tail)
        result=I.of(0);angles={};floor=None
        for key,(_,weight) in settings().items():
            z=vals[rho,sector,key].pad(tail)
            phi=I.of(0) if key=='0' else angle(z*z0.conj())
            result=result+weight*phi
            angles[key]=phi.rounded(18)
            # All complex rectangles here stay away from zero; an unnormalized lower bound.
            lower=max(0,z.re.lo,-z.re.hi,z.im.lo,-z.im.hi)
            floor=lower if floor is None else min(lower,floor)
        assert floor>0
        rows[f'{rho}|{sector}']={'mass_interval':result.rounded(14),'phase_intervals':angles,
                                 'unnormalized_modulus_floor':str(Q(floor*10**8//S,10**8))}
    return rows

if __name__=='__main__':print(json.dumps(solve(),sort_keys=True,indent=2))
