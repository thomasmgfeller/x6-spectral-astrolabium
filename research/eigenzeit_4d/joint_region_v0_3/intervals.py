"""Decimal intervals with directed rounding; no binary float constructors."""
from decimal import Decimal as D, Context, ROUND_FLOOR, ROUND_CEILING

DOWN=Context(prec=60,rounding=ROUND_FLOOR)
UP=Context(prec=60,rounding=ROUND_CEILING)

def precision(n):
    DOWN.prec=UP.prec=n

class I:
    __slots__=('lo','hi')
    def __init__(self,lo=0,hi=None):
        if isinstance(lo,I):self.lo,self.hi=lo.lo,lo.hi;return
        if isinstance(lo,float) or isinstance(hi,float):raise TypeError('binary floats forbidden')
        self.lo=D(lo);self.hi=D(lo if hi is None else hi)
        if not self.lo.is_finite() or not self.hi.is_finite() or self.lo>self.hi:raise ValueError('invalid interval')
    def __add__(self,b):
        b=I(b);return I(DOWN.add(self.lo,b.lo),UP.add(self.hi,b.hi))
    __radd__=__add__
    def __neg__(self):return I(self.hi.copy_negate(),self.lo.copy_negate())
    def __sub__(self,b):return self+-I(b)
    def __rsub__(self,b):return I(b)+-self
    def __mul__(self,b):
        b=I(b)
        return I(min(DOWN.multiply(x,y) for x in (self.lo,self.hi) for y in (b.lo,b.hi)),
                 max(UP.multiply(x,y) for x in (self.lo,self.hi) for y in (b.lo,b.hi)))
    __rmul__=__mul__
    def __truediv__(self,b):
        b=I(b)
        if b.lo<=0<=b.hi:raise ZeroDivisionError('interval contains zero')
        return self*I(DOWN.divide(D(1),b.hi),UP.divide(D(1),b.lo))
    def __rtruediv__(self,b):return I(b)/self
    def square(self):
        upper=UP.multiply(max(self.lo.copy_abs(),self.hi.copy_abs()),max(self.lo.copy_abs(),self.hi.copy_abs()))
        lower=D(0) if self.lo<=0<=self.hi else min(DOWN.multiply(self.lo,self.lo),DOWN.multiply(self.hi,self.hi))
        return I(lower,upper)
    def sqrt(self):
        if self.lo<0:raise ValueError('negative square root')
        # Decimal.sqrt is correctly rounded to nearest; adjacent representable
        # values enclose it irrespective of that nearest rounding direction.
        lower=D(0) if self.lo==0 else DOWN.next_minus(DOWN.sqrt(self.lo))
        upper=D(0) if self.hi==0 else UP.next_plus(UP.sqrt(self.hi))
        return I(lower,upper)
    def __abs__(self):
        if self.lo>=0:return self
        if self.hi<=0:return -self
        return I(0,max(self.lo.copy_abs(),self.hi.copy_abs()))

def lo(x):return x.lo if isinstance(x,I) else x
def hi(x):return x.hi if isinstance(x,I) else x
