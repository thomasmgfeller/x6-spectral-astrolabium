"""Declared AA control experiment. Exact finite geometry and certified scalar phases."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
from collections import defaultdict
import json
from flint import arb, acb

ROOT=Path(__file__).resolve().parent
BOUNDARY=(0,1,3,4)

def relations(code):
    return {(i,j) for i in range(5) for j in range(5) if code&(1<<(5*i+j))}

def histories():
    optional=[(i,j) for i in (0,1) for j in (2,3,4)]+[(2,3),(2,4)]
    answer=[]
    for flags in product((0,1),repeat=8):
        rel={p for p,on in zip(optional,flags) if on}
        if any((i,k) not in rel for i,j in rel for j2,k in rel if j==j2):continue
        if not any((i,2) in rel for i in (0,1)):continue
        if not any((2,j) in rel for j in (3,4)):continue
        if not all(any((i,j) in rel for j in (3,4)) for i in (0,1)):continue
        if not all(any((i,j) in rel for i in (0,1)) for j in (3,4)):continue
        answer.append(sum(1<<(5*i+j) for i,j in rel))
    return sorted(answer)

def pair_coefficients(code):
    rel=relations(code)
    return [(i,j,(1,-9,16,-8)[sum((i,z) in rel and (z,j) in rel for z in range(5))])
            for i,j in sorted(rel)]

def h0(code):
    h=[[Q(0) for j in range(5)] for i in range(5)]
    for i,j,c in pair_coefficients(code):
        h[i][i]-=Q(c,2);h[j][j]-=Q(c,2)
        h[i][j]+=Q(c,2);h[j][i]+=Q(c,2)
    return h

def reference_h0():
    hs=[h0(c) for c in histories()]
    return [[sum(h[i][j] for h in hs)/len(hs) for j in range(5)] for i in range(5)]

def interpolate_h0(code,coupling):
    lam=Q(coupling)
    if not 0<=lam<=1:raise ValueError('coupling must lie in [0,1]')
    ref=reference_h0();actual=h0(code)
    return [[ref[i][j]+lam*(actual[i][j]-ref[i][j]) for j in range(5)] for i in range(5)]

def f4(code):return 5-sum(c for i,j,c in pair_coefficients(code))

def boundary_group():
    answer=[]
    for a,b in product((0,1),repeat=2):
        p=list(range(5))
        if a:p[0],p[1]=p[1],p[0]
        if b:p[3],p[4]=p[4],p[3]
        answer.append(p)
    return answer

def relabel(code,p):return sum(1<<(5*p[i]+p[j]) for i,j in relations(code))

def orbits():
    out=defaultdict(list)
    for code in histories():out[min(relabel(code,p) for p in boundary_group())].append(code)
    return dict(sorted(out.items()))

def beta():return 4/arb(6).sqrt()

def scalar_ground(h,epsilon=0):
    """A00 with h=M/beta. Square roots follow right-half-plane Gaussian pivots.

    h0 packets contribute 1/pi; all four boundary fields are integrated.
    The interior is integrated first with z=epsilon+i*alpha. At epsilon=0
    the declared Abel limit is evaluated analytically, not approximated.
    """
    b=beta();m=[[b*arb(str(v)) for v in row] for row in h]
    alpha=-m[2][2]
    if not alpha>0:raise ValueError('interior gap must be strictly positive')
    z=acb(epsilon,alpha)
    mat=[[acb(int(i==j),-m[x][y])+m[2][x]*m[2][y]/z
          for j,y in enumerate(BOUNDARY)] for i,x in enumerate(BOUNDARY)]
    # At epsilon=0 this is I-i*(M_BB+J^T J/alpha).
    determinant_root=acb(1);pivots=[]
    for k in range(4):
        pivot=mat[k][k]
        if not pivot.real>0:raise ValueError('Gaussian pivot not certified in right half-plane')
        pivots.append(pivot)
        determinant_root*=pivot.sqrt(analytic=True)
        for i in range(k+1,4):
            for j in range(k+1,4):mat[i][j]-=mat[i][k]*mat[k][j]/pivot
    factor=4*arb.pi()*(2*arb.pi()).sqrt()/z.sqrt(analytic=True)/determinant_root
    return factor,pivots,alpha

def E(k):
    """Entire positive-density factor, regular also when k contains zero."""
    u=k/2
    return acb(0,-u).exp()*u.sinc()

def dust_error(code,n,rho=2):
    """Analytic error of the exact 5D normalized tensor GL rule.

    Derived from Chebyshev coefficients, positive weights and degree 2n-1
    exactness; does not use a difference of quadrature rules as a bound.
    """
    r=arb(rho);a=(r+1/r)/2;b=(r-1/r)/2
    degrees=[sum(abs(c) for i,j,c in pair_coefficients(code) if k in (i,j)) for k in range(5)]
    exponent=beta()*b*(a+1)/2
    result=arb(3).sqrt()/2*r**(-2*n)/(1-1/r)*sum((exponent*w).exp() for w in degrees)
    return result,degrees

def pack(z,digits=30):
    z=acb(z)
    return {'real':z.real.str(digits,more=True),'imag':z.imag.str(digits,more=True)}

def unpack(record):return acb(arb(record['real']),arb(record['imag']))

def widen(z,error):
    rad=error.upper()
    return acb(z.real+arb(0,rad),z.imag+arb(0,rad))

def experiment_geometry():
    return {'history_count':len(histories()),'orbit_count':len(orbits()),
            'orbits':{str(k):v for k,v in orbits().items()},
            'reference_h0':[[str(x) for x in row] for row in reference_h0()]}
