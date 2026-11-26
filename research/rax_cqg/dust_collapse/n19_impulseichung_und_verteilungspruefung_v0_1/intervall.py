"""Exact rational closed intervals in SI and model units."""
from fractions import Fraction as F
from dataclasses import dataclass
from math import isqrt

@dataclass(frozen=True)
class I:
    lo: F
    hi: F

    def __post_init__(self):
        if self.lo>self.hi:raise ValueError('interval limits reversed')

    def __add__(self,other):
        o=interval(other)
        return I(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__

    def __neg__(self):
        return I(-self.hi,-self.lo)

    def __sub__(self,other):
        return self+(-interval(other))

    def __rsub__(self,other):
        return interval(other)+(-self)

    def __mul__(self,other):
        o=interval(other)
        v=[a*b for a in (self.lo,self.hi) for b in (o.lo,o.hi)]
        return I(min(v),max(v))
    __rmul__=__mul__

    def __truediv__(self,other):
        o=interval(other)
        if o.lo<=0<=o.hi:raise ZeroDivisionError('reference interval includes zero')
        return self*I(1/o.hi,1/o.lo)

    def __rtruediv__(self,other):
        return interval(other)/self

    def overlaps(self,other):
        o=interval(other)
        return max(self.lo,o.lo)<=min(self.hi,o.hi)

    def intersect(self,other):
        return I(max(self.lo,other.lo),min(self.hi,other.hi))

    def inside(self,other):
        o=interval(other)
        return o.lo<=self.lo<=self.hi<=o.hi

    def square(self):
        lo=0 if self.lo<=0<=self.hi else min(self.lo**2,self.hi**2)
        return I(F(lo),max(self.lo**2,self.hi**2))

    def sqrt(self):
        if self.lo<0:raise ValueError('negative lower bound')
        scale=10**85
        def lower(x):return F(isqrt(x.numerator*scale**2//x.denominator),scale)
        u=lower(self.hi)
        return I(lower(self.lo),u if u*u==self.hi else u+F(1,scale))

    def data(self):return [str(self.lo),str(self.hi)]


def interval(x):
    if isinstance(x,I):return x
    if isinstance(x,(list,tuple)) and len(x)==2:return I(F(x[0]),F(x[1]))
    return I(F(x),F(x))


def around(center,radius):
    center,radius=F(center),F(radius)
    return I(center-radius,center+radius)


def relative(center,eps):
    c=F(center)
    return around(c,abs(c)*F(eps))


def pi_bounds():
    # Machin's identity with exact alternating-series enclosures.
    def arctan_inv(q):
        n=42
        s=sum((F((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(n)),F(0))
        return I(s,s+F(1,(2*n+1)*q**(2*n+1)))
    return 16*arctan_inv(5)-4*arctan_inv(239)
