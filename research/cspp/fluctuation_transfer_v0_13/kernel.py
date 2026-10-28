"""Exact finite coefficient extraction for joint smoothed Poisson layer weights.

Atoms are disjoint measurable regions with independently Poisson counts.
Replicated factors use independent thinning marks on the SAME base process.
This is an exact expectation, not independent interval or Gaussian closure.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb, factorial
from flint import arb,acb,fmpq,fmpq_poly as Polynomial

C=(1,-9,16,-8)

def ball(x):
    return arb(x.numerator)/x.denominator if isinstance(x,F) else arb(x)

def require(ok,msg):
    if not ok:raise ArithmeticError(msg)

def palm(coefficients,epsilon,shift):
    require(isinstance(shift,int) and shift>=0,'nonnegative Palm count')
    out=[ball(v) for v in coefficients];e=ball(epsilon)
    for _ in range(shift):out=[(1-e)*v+e*(out[j+1] if j+1<len(out) else 0) for j,v in enumerate(out)]
    return out

def weight(n,epsilon=F(1,16),shift=0):
    require(n>=0 and isinstance(n,int),'nonnegative count')
    e=ball(epsilon);n+=shift
    return sum(c*comb(n,j)*e**j*(1-e)**(n-j) for j,c in enumerate(C) if j<=n)

class JointWeights:
    def __init__(self,atoms,epsilon=F(1,16),shifts=(0,1,0,0)):
        # atom: (set of interval indices, exact mean).
        self.atoms=[(frozenset(mask),ball(mean)) for mask,mean in atoms]
        self.epsilon=ball(epsilon);self.shifts=tuple(shifts);self.cache={}
        require(0<self.epsilon<=1,'epsilon range')
        require(all(mean>=0 for mask,mean in self.atoms),'positive atom intensities')

    def moment(self,powers):
        powers=tuple(powers)
        if powers in self.cache:return self.cache[powers]
        factors=[i for i,n in enumerate(powers) for _ in range(n)]
        p=len(factors)
        if p==0:return arb(1)
        e=self.epsilon;r=1-e;g0=arb(0);g={}
        for atom,mean in self.atoms:
            active=sum(1<<j for j,i in enumerate(factors) if i in atom)
            d=active.bit_count();g0+=mean*(r**d-1)
            sub=active
            while sub:
                k=sub.bit_count()
                g[sub]=g.get(sub,arb(0))+mean*e**k*r**(d-k)
                sub=(sub-1)&active
        # G(z)=g0+sum_nonempty_S g[S] product_{j in S} z_j.
        # If F=exp(G), n_j F_n=sum_{S contains j} g[S] F_{n-1_S}.
        zero=(0,)*p
        @lru_cache(None)
        def coefficient(n):
            if n==zero:return g0.exp()
            j=next(j for j,v in enumerate(n) if v)
            available=sum(1<<i for i,v in enumerate(n) if v)
            out=arb(0)
            for mask,v in g.items():
                if mask&(1<<j) and mask&available==mask:
                    out+=v*coefficient(tuple(a-((mask>>i)&1) for i,a in enumerate(n)))
            return out/n[j]
        cc=[palm(C,e,self.shifts[i]) for i in factors]
        out=arb(0)
        for n in product(range(4),repeat=p):
            factor=arb(1)
            for j,k in enumerate(n):factor*=cc[j][k]
            out+=factor*coefficient(n)
        require(out.is_finite(),'finite joint moment')
        self.cache[powers]=out
        return out

# Rational 4D overlap volumes for vertical timelike intervals at distance d.
# Each spatial slice is a 3-ball; its lens volume is a cubic polynomial in t.
def vertical_overlap_over_pi(start1,end1,start2,end2,d,stop=None):
    a,b,c,e,d=map(fmpq,(start1,end1,start2,end2,d))
    require(b>a and e>c and d>=0,'valid timelike intervals')
    lo=max(a,c);hi=min(b,e)
    if stop is not None:hi=min(hi,fmpq(stop))
    if hi<=lo:return fmpq(0)
    t=Polynomial([0,1]);breaks=sorted(set([lo,hi]+[x for x in [(a+b)/2,(c+e)/2] if lo<x<hi]))
    total=fmpq(0)
    for l,u in zip(breaks[:-1],breaks[1:]):
        m=(l+u)/2;r1=t-a if m<(a+b)/2 else b-t;r2=t-c if m<(c+e)/2 else e-t
        cuts=[l,u]
        for q in [r1+r2-d,r1-r2-d,r2-r1-d]:
            if len(q)>1 and q[1]:
                z=-q[0]/q[1]
                if l<z<u:cuts.append(z)
        cuts=sorted(set(cuts))
        for x,y in zip(cuts[:-1],cuts[1:]):
            m=(x+y)/2;v1=r1(m);v2=r2(m)
            if d>=v1+v2:continue
            if d<=abs(v1-v2):poly=fmpq(4,3)*(r1 if v1<=v2 else r2)**3
            else:poly=(r1+r2-d)**2*(d*d+2*d*(r1+r2)-3*(r1-r2)**2)/(12*d)
            ant=Polynomial([0]+[v/fmpq(i+1) for i,v in enumerate(poly.coeffs())])
            total+=ant(y)-ant(x)
    return total

def control_atoms():
    # A=I((-2,0),(0,0)), B=I((-2,.5),(1,.5)),
    # C=I((0,0),(1,.5)) subset B, disjoint A.
    # H=(A intersection B) intersection {t<=-1}.
    va=fmpq(2)**4/24;vb=fmpq(3)**4/24;vc=(1-fmpq(1,2)**2)**2/24
    overlap=vertical_overlap_over_pi(-2,0,-2,1,fmpq(1,2))
    history=vertical_overlap_over_pi(-2,0,-2,1,fmpq(1,2),-1)
    regions=[({0},va-overlap),({0,1},overlap-history),({0,1,3},history),({1},vb-overlap-vc),({1,2},vc)]
    require(all(v>0 for mask,v in regions),'positive exact atom volumes')
    # Original density rho=3/pi, so all atom means are rational.
    return [(mask,F(int((3*v).numerator),int((3*v).denominator))) for mask,v in regions],{
        'A_over_pi':str(va),'B_over_pi':str(vb),'C_over_pi':str(vc),
        'A_intersection_B_over_pi':str(overlap),'history_overlap_over_pi':str(history)}


def pair_weight_covariance(volume1,volume2,overlap,rho,epsilon,shift1=0,shift2=0):
    v1,v2,o,rho=map(ball,(volume1,volume2,overlap,rho))
    require(v1>=o and v2>=o and o>=0 and rho>0,'consistent overlap')
    law=JointWeights([({0},rho*(v1-o)),({1},rho*(v2-o)),({0,1},rho*o)],epsilon,(shift1,shift2))
    m1=law.moment((1,0));m2=law.moment((0,1));joint=law.moment((1,1))
    return m1,m2,joint,joint-m1*m2


def mecke_connected_pair(volume1,volume2,overlap,rho,epsilon,shift1=0,shift2=0):
    """Off-diagonal Poisson sum integrand: shifted joint minus UNSHIFTED means.

This differs from covariance of two weights under a fixed Palm-shifted law.
Passive observation points are not inserted into the background process.
"""
    _,_,joint,_=pair_weight_covariance(volume1,volume2,overlap,rho,epsilon,shift1,shift2)
    a,b,_,_=pair_weight_covariance(volume1,volume2,overlap,rho,epsilon,0,0)
    return joint-a*b
