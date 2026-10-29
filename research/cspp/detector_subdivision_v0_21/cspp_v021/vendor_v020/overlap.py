"""Lorentz-invariant exact diamond overlap and exact archived interval counts."""
from fractions import Fraction as F
from flint import arb, acb
import numpy as np

B = (F(-5), F(0), F(0), F(0))

def point(p):
    return tuple(F(float(v)) if isinstance(v, (float, np.floating)) else F(v) for v in p)

def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mink(a,b): return a[0]*b[0]-sum(x*y for x,y in zip(a[1:],b[1:]))
def before(a,b):
    q=sub(b,a)
    return q[0]>0 and mink(q,q)>0
def ball(q): return arb(str(q))

def geometry(y,p):
    """Return rho times total, overlap, exterior volumes; rho=3/pi.

    p must be in Omega5. All causal branch decisions use exact rationals.
    """
    y,p=point(y),point(p)
    if not before(B,p) or not before(p,(F(5),F(0),F(0),F(0))):
        raise ValueError('endpoint must lie in Omega5')
    if not before(y,p): return arb(0),arb(0),arb(0),'noncausal'
    v=sub(p,B);w=sub(y,B);z=sub(p,y)
    total=ball(mink(z,z)**2/8)
    if before(y,B) or y==B or (w[0]<=0 and mink(w,w)==0):
        overlap=ball(mink(v,v)**2/8);branch='nested_past'
    elif before(B,y) or (w[0]>=0 and mink(w,w)==0):
        overlap=total;branch='nested_future'
    else:
        h=ball(mink(v,v)).sqrt();u=ball(mink(v,w))/h
        d=(u*u-ball(mink(w,w))).sqrt()
        if not (d>abs(u) and h>u+d):raise ArithmeticError('undecided lens topology')
        overlap=h*(h-u-d)**2*(d*d+d*h-u*u)/(8*d);branch='lens'
    outside=total-overlap
    if branch=='nested_future':outside=arb(0)
    if not (outside>=0 and overlap>=0):raise ArithmeticError('negative volume enclosure')
    return total,overlap,outside,branch

def lens_quadrature(y,p):
    """Independent validated integration of the two spatial spherical caps."""
    y,p=point(y),point(p);v=sub(p,B);w=sub(y,B)
    h=ball(mink(v,v)).sqrt();u=ball(mink(v,w))/h
    d=(u*u-ball(mink(w,w))).sqrt()
    if not(d>abs(u) and h>u+d):raise ValueError('proper lens required')
    def caps(r,R):
        x=(d*d+r*r-R*R)/(2*d)
        a=r-x;b=R-(d-x)
        return a*a*(3*r-a)+b*b*(3*R-b)
    def integral(fn,a,b):
        z=acb.integral(lambda t,analytic:fn(t),acb(a),acb(b),abs_tol=arb('1e-30'),rel_tol=arb('1e-30'))
        if not z.is_finite() or not z.imag.contains(0):raise ArithmeticError('quadrature')
        return z.real
    # rho=3/pi cancels the pi/3 in each spherical cap.
    return (integral(lambda t:caps(t,t-u),(u+d)/2,h/2)
            +integral(lambda t:caps(h-t,t-u),h/2,(h+u+d)/2)
            +integral(lambda t:4*(h-t)**3,(h+u+d)/2,h))

class Archive:
    def __init__(self,x):
        self.x=x;self.q=[point(v) for v in x]
        self.active=[i for i,p in enumerate(self.q) if -1<p[0]<F(5,4) and
          (F(7,4)-p[0])>0 and sum((v-c)**2 for v,c in zip(p[1:],(0,0,F(3,2))))<(F(7,4)-p[0])**2]
        self.p=[self.q[i] for i in self.active]
        self.past=np.array([[before(z,p) for z in self.q] for p in self.p],dtype=bool)
    def counts(self,y):
        y=point(y)
        future=np.array([before(y,z) for z in self.q],dtype=bool)
        return np.sum(self.past & future,axis=1)
