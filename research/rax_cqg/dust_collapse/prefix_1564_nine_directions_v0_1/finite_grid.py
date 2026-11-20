"""Checks for Gauss nodes/weights and bounded-range elementary functions in binary64."""
from fractions import Fraction as Q
from functools import lru_cache
from math import factorial

import numpy as np

def legendre_pair(n,x):
    # Return P_n and P_(n-1) exactly at a rational value.
    prev,cur=Q(1),x
    for k in range(2,n+1):
        prev,cur=cur,((2*k-1)*x*cur-(k-1)*prev)/k
    return cur,prev

@lru_cache(None)
def checked_rule(n):
    xx,ww=np.polynomial.legendre.leggauss(n)
    ww=ww/2
    eps=Q(1,2**48)
    previous=Q(-1)
    for x0,w0 in zip(xx,ww):
        x,w=Q.from_float(float(x0)),Q.from_float(float(w0))
        lo,hi=x-eps,x+eps
        assert previous<lo<hi<1
        previous=hi
        assert legendre_pair(n,lo)[0]*legendre_pair(n,hi)[0]<0
        p,v=legendre_pair(n,x)
        deriv=abs(n*(v-x*p)/(1-x*x))
        # Two applications of Markov's inequality on [-1,1].
        d1,d2=deriv-n**4*eps,deriv+n**4*eps
        assert d1>0
        low_abs=0 if lo<=0<=hi else min(abs(lo),abs(hi))
        high_abs=max(abs(lo),abs(hi))
        wlo=1/((1-low_abs**2)*d2**2)
        whi=1/((1-high_abs**2)*d1**2)
        assert wlo>0 and wlo*(1+Q(1,10**6))>=w>=whi*(1-Q(1,10**6))
    return xx,ww

def phase(x):
    # Range reduction with a binary64 pi/2, then Taylor polynomials on [-0.79,0.79].
    x=np.asarray(x)
    if np.max(np.abs(x))>4096:raise ValueError('Phase outside the verified range')
    m=np.rint(x/1.5707963267948966).astype(np.int32)
    t=x-m*1.5707963267948966
    s=t*t
    a=(-1.)**7/factorial(15)
    b=(-1.)**7/factorial(14)
    for j in range(6,-1,-1):
        a=(-1.)**j/factorial(2*j+1)+s*a
        b=(-1.)**j/factorial(2*j)+s*b
    sn=t*a
    return (b+1j*sn)*np.array([1,1j,-1,-1j])[m%4]

def sinc(x):
    x=np.asarray(x)
    small=np.abs(x)<.25
    # Avoid division by a small argument. Clamp the polynomial's unused branch.
    z=np.where(small,x,0.)**2
    a=-1./factorial(11)
    for j in range(4,-1,-1):
        a=(-1.)**j/factorial(2*j+1)+z*a
    return np.where(small,a,phase(x).imag/np.where(small,1.,x))

def verify_constants(beta,step):
    d=Q(1,2**48)
    b=Q.from_float(float(beta));s=Q.from_float(float(step))
    assert (b-d)**2<Q(16,6)<(b+d)**2
    assert 19**2*Q(16,6)*(s-d)**4<4<19**2*Q(16,6)*(s+d)**4
    # Rational decimal enclosure of pi from Machin's formula and alternating remainders.
    def atan_bounds(x):
        a=sum((-1)**j*x**(2*j+1)/(2*j+1) for j in range(41))
        return a-x**83/83,a
    a,b=atan_bounds(Q(1,5));c,e=atan_bounds(Q(1,239))
    k=Q.from_float(1.5707963267948966)
    assert k-Q(1,2**52)<8*a-2*e<8*b-2*c<k+Q(1,2**52)
