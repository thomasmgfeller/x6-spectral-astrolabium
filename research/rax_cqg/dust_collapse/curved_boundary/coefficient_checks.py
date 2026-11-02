"""Exact rational checks of local residues, and independent flat finite-part limit."""
from fractions import Fraction as Q
from math import pi,sqrt
import numpy as np
from common import nodes
from prediction import A,angular_residue,local

def check_series(h):
    # S=(1+h*w)^2 D^3, H=D^4 a_m^8 times the diamond moment polynomial.
    d1=(1-2*h)/3
    d2=Q(5,27)*(1-3*h+3*h**2)
    m1=(2*h-1)/6
    m2=-(h*h+(1-h)**2)/18
    S1=2*h+3*d1
    S2=h*h+3*d2+3*d1*d1+6*h*d1
    H1=4*d1+8*m1
    H20=4*d2+6*d1*d1+8*m2+28*m1*m1+32*d1*m1+Q(7,45)
    H21=-Q(14,135)
    assert S1==1 and S2==Q(8,9)-h and H1==0 and H20==Q(16,135)
    residue=(S2-2*H20)/32+(-2*H21)/16
    assert residue==(Q(16,15)-h)/32
    return residue
for h in map(Q,[0,'1/5','1/2','3/4',1]): check_series(h)
assert (check_series(Q(0))+check_series(Q(1)))/2==Q(17,960)
assert abs(A+17*sqrt(6)/(10*pi))<1e-14
for p,f in [(.2,.3),(.7,.31),(.45,.45)]:
    nodes01,weights=nodes(96)
    h0=p/(p+f)
    invsq=0.
    for l,r in [(0,h0),(h0,1)]:
        h=l+(r-l)*nodes01;W=np.minimum(p/h,f/(1-h))
        invsq+=(r-l)*np.dot(weights,W**-2)
    b=pi/24
    flat=(4*pi/sqrt(6))/b**2*invsq/64
    assert abs(flat-2*sqrt(6)/pi*(p**-2+f**-2-(p+f)**-2))<1e-10
print('Exact local coefficients and three flat finite parts verified.')
