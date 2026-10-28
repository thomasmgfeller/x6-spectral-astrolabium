"""Certified, deliberately conservative Cauchy-history remainder bounds.

Finite local Taylor jets of a C-infinity compact source all vanish outside
its support. Increasing local Taylor order cannot repair a missed source.
The bounds below are approximation upper bounds, NOT observed errors.
"""
from collections import defaultdict
from fractions import Fraction
from common10 import arb, acb, previous, check


def add(a,b): return a[0]+b[0],a[1]+b[1]
def mul(a,b): return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]


def derivative(poly,axis):
    """Differentiate P(x,y,z,h^-1)*exp(-1/h)*exp(4iz), h=1-4r²."""
    out=defaultdict(lambda:(0,0))
    for key,c in poly.items():
        p=list(key[:3]);h=key[3]
        terms=[]
        if p[axis]:
            q=p.copy();q[axis]-=1;terms.append(((*q,h),(p[axis],0)))
        q=p.copy();q[axis]+=1
        if h:terms.append(((*q,h+1),(8*h,0)))
        terms.append(((*q,h+2),(-8,0)))
        if axis==2:terms.append((key,(0,4)))
        for target,coef in terms:out[target]=add(out[target],mul(c,coef))
    return {k:c for k,c in out.items() if c!=(0,0)}


def L(poly):
    out=defaultdict(lambda:(0,0),poly)
    for axis in range(3):
        for key,c in derivative(derivative(poly,axis),axis).items():
            out[key]=add(out[key],(-c[0],-c[1]))
    return {k:c for k,c in out.items() if c!=(0,0)}


def polynomials():
    p={(0,0,0,0):(1,0)};out=[p]
    for _ in range(3):p=L(p);out.append(p)
    return out


def norm_over_amplitude(poly):
    """Upper bound ||L^r f||_2/(A/e); triangle bound on exact monomials."""
    total=arb(0)
    for (p,q,r,n),(re,im) in poly.items():
        maximum=(-arb(1)).exp() if n==0 else arb(n)**n*(-arb(n)).exp()
        total+=(arb(re*re+im*im).sqrt()/2**(p+q+r))*maximum
    return (arb.pi()/6).sqrt()*arb(1).exp()*total


def constants():
    ps=polynomials()
    return {1:norm_over_amplitude(ps[2])/(2*(8*arb.pi()).sqrt()),
            3:norm_over_amplitude(ps[3])/(24*(8*arb.pi()).sqrt())}


def history_bounds(x,order,constant):
    check(order in (1,3),'declared Taylor adapters')
    return [constant*(arb(float(row[0]))+1)**(order+1) for row in x]


def support_hits(x):
    return sum(sum(Fraction(float(v))**2 for v in row[1:]) < Fraction(1,4) for row in x)


def transfer_bound(transfer,bounds):
    return sum(w.abs_upper()*b for w,b in zip(transfer,bounds))


def evaluate_polynomial(poly,xyz):
    h=1-4*sum(z*z for z in xyz)
    check(h>0,'interior polynomial evaluation')
    return sum(acb(re,im)*xyz[0]**p*xyz[1]**q*xyz[2]**r/h**n
               for (p,q,r,n),(re,im) in poly.items())
