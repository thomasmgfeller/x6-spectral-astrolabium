"""Rigorous finite-N pair bounds under the ideal physical-volume model.
The exact fractions enclose normalizing integrals on a common aligned null chart.
"""
from fractions import Fraction as Q
from math import comb,isqrt
from scipy.integrate import dblquad
import numpy as np

def sqrt_box(x, scale):
    bottom = isqrt((x.numerator*scale**2)//x.denominator)
    lo = Q(bottom,scale)
    return lo, lo if lo*lo==x else Q(bottom+1,scale)

def delta(h):
    zlo,zhi=sqrt_box(1-h*h/4,2**90)
    return (1-zhi)/(1+zhi),(1-zlo)/(1+zlo)

def moment(k):
    def a(n):
        return Q(0) if n%2 else Q(1,n+1)
    return 3*(a(k+2)*a(k)-a(k+1)**2)

def cross(di,dj,degree=12):
    lower=upper=Q(0)
    for n in range(degree+1):
        def coefficient(x,y):
            return sum((i+1)*(n-i+1)*x**i*y**(n-i) for i in range(n+1))
        m=moment(n)
        a=m*coefficient(di[0],dj[0])
        b=m*coefficient(di[1],dj[1])
        lower+=min(a,b)
        upper+=max(a,b)
    d=max(di[1],dj[1])
    omitted=degree+1
    tail=comb(omitted+3,3)*d**omitted/(1-d*Q(omitted+4,omitted+1))
    return lower-tail,upper+tail

def bounds(hi,hj,n):
    di,dj=delta(hi),delta(hj)
    fij=cross(di,dj)
    fii=cross(di,di)
    fjj=cross(dj,dj)
    assert fij[0]>0 and fii[0]>0 and fjj[0]>0
    squared_affinity_lower=fij[0]**2/(fii[1]*fjj[1])
    tv2=1-squared_affinity_lower**n
    tv_upper=sqrt_box(tv2,10**6)[1]
    # Independent double integral in normalized null coordinates on [-1,1]^2.
    def quad(a,b):
        i,j=float(sum(a)/2),float(sum(b)/2)
        def f(v,u):
            return 3/8*(v-u)**2/((1-i*u*v)*(1-j*u*v))**2
        return dblquad(f,-1,1,lambda u:-1,lambda u:1,epsabs=2e-13,epsrel=2e-13)[0]
    for interval,x,y in [(fij,di,dj),(fii,di,di),(fjj,dj,dj)]:
        value=quad(x,y)
        assert float(interval[0])-3e-14 <= value <= float(interval[1])+3e-14
    # In chart coordinates a=1/2, U,V in [-a,a]; F acts on each null coordinate.
    for h in (hi,hj):
        h=float(h); k=h/(1+np.sqrt(1-h*h/4)); b=k/4
        for u in np.linspace(-.5,.5,13):
            for v in np.linspace(u,.5,11):
                fu,fv=(u+b)/(1+k*u),(v+b)/(1+k*v)
                scale=(1-k*k/4)/((1+k*u)*(1+k*v))
                direct=scale/(1-h*(fu+fv)/2)
                analytic=(1+k*k/4)/(1-k*k*u*v)
                assert abs(direct-analytic)<2e-15
    return dict(h_i=str(hi),h_j=str(hj),n=n,tv_upper=float(tv_upper),
                max_power_at_5pct=float(tv_upper+Q(1,20)),
                squared_affinity_lower_decimal=float(squared_affinity_lower),
                method='outward on grid 1e-6; exact rational moments to degree 12 and absolute tail',
                delta_i=[str(i) for i in di],delta_j=[str(j) for j in dj])
