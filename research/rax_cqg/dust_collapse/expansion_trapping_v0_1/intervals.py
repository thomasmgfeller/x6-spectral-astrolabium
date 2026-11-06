"""Outward Decimal interval arithmetic for rational operations (60 digits).

No binary floating-point number enters a certified computation. Fractional
reference powers are enclosed by exact rational bisection, not libm.
"""
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction

PRECISION=60


def down(fn):
    with localcontext() as c:
        c.prec=PRECISION;c.rounding=ROUND_FLOOR
        return fn()


def up(fn):
    with localcontext() as c:
        c.prec=PRECISION;c.rounding=ROUND_CEILING
        return fn()


class I:
    def __init__(self, lo, hi=None):
        if isinstance(lo,float) or isinstance(hi,float):raise TypeError('binary float forbidden')
        self.lo=Decimal(lo);self.hi=Decimal(lo if hi is None else hi)
        if self.lo>self.hi:raise ValueError('inverted interval')

    @classmethod
    def fraction(cls,q):
        q=Fraction(q);n=Decimal(q.numerator);d=Decimal(q.denominator)
        return cls(down(lambda:n/d),up(lambda:n/d))

    @classmethod
    def coerce(cls,x):
        return x if isinstance(x,I) else cls.fraction(x) if isinstance(x,Fraction) else cls(x)

    def __add__(self,other):
        b=self.coerce(other)
        return I(down(lambda:self.lo+b.lo),up(lambda:self.hi+b.hi))
    __radd__=__add__

    def __neg__(self):return I(self.hi.copy_negate(),self.lo.copy_negate())
    def __sub__(self,other):return self+-self.coerce(other)
    def __rsub__(self,other):return self.coerce(other)+-self

    def __mul__(self,other):
        b=self.coerce(other);pairs=[(a,c) for a in (self.lo,self.hi) for c in (b.lo,b.hi)]
        return I(min(down(lambda:a*c) for a,c in pairs),max(up(lambda:a*c) for a,c in pairs))
    __rmul__=__mul__

    def reciprocal(self):
        if self.lo<=0<=self.hi:raise ZeroDivisionError('interval contains zero')
        return I(down(lambda:Decimal(1)/self.hi),up(lambda:Decimal(1)/self.lo))
    def __truediv__(self,other):return self*self.coerce(other).reciprocal()
    def __rtruediv__(self,other):return self.coerce(other)*self.reciprocal()

    def __pow__(self,n):
        if not isinstance(n,int) or n<0:raise ValueError('nonnegative integer power required')
        if n==0:return I(1)
        if n==2:
            lows=[down(lambda:a*a) for a in (self.lo,self.hi)]
            highs=[up(lambda:a*a) for a in (self.lo,self.hi)]
            return I(0 if self.lo<=0<=self.hi else min(lows),max(highs))
        return self*(self**(n-1))

    def absolute(self):
        a,b=self.lo.copy_abs(),self.hi.copy_abs()
        return I(0 if self.lo<=0<=self.hi else min(a,b),max(a,b))

    def inflate(self,amount):
        a=self.coerce(amount).absolute().hi
        return self+I(a.copy_negate(),a)

    def contains(self,other):
        b=self.coerce(other);return self.lo<=b.lo and self.hi>=b.hi

    def bounds(self):return [str(self.lo),str(self.hi)]

    def middle_float(self):
        return float(down(lambda:(self.lo+self.hi)/2))


def cube_root_rational(q,iterations=100):
    q=Fraction(q)
    if not 0<=q<=1:raise ValueError('reference root outside [0,1]')
    if q in (0,1):return I(q.numerator)
    lo,hi=Fraction(0),Fraction(1)
    for _ in range(iterations):
        mid=(lo+hi)/2
        if mid**3<=q:lo=mid
        else:hi=mid
    return I(I.fraction(lo).lo,I.fraction(hi).hi)
