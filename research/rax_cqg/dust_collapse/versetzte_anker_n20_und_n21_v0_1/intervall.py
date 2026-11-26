"""Small directed-decimal interval kernel. Integers count units of 10^-12."""
from fractions import Fraction
from math import isqrt

Q=10**12

class I:
    def __init__(self,l,h):
        if not isinstance(l,int) or not isinstance(h,int) or l>h: raise ValueError((l,h))
        self.l,self.h=l,h
    @classmethod
    def enclose(cls,a,b=None):
        a=Fraction(a)*Q
        b=Fraction(b)*Q if b is not None else a
        return cls(a.numerator//a.denominator,-((-b.numerator)//b.denominator))
    def __add__(self,b):
        if isinstance(b,int):return I(self.l+b*Q,self.h+b*Q)
        return I(self.l+b.l,self.h+b.h)
    __radd__=__add__
    def __neg__(self):return I(-self.h,-self.l)
    def __sub__(self,b):return self+(-b)
    def __rsub__(self,b):return b+(-self)
    def __mul__(self,b):
        if isinstance(b,int):return I(min(self.l*b,self.h*b),max(self.l*b,self.h*b))
        vals=[x*y for x in (self.l,self.h) for y in (b.l,b.h)]
        return I(min(vals)//Q,-((-max(vals))//Q))
    __rmul__=__mul__
    def __truediv__(self,b):
        if isinstance(b,int): b=I.enclose(b)
        if b.l<=0<=b.h:raise ZeroDivisionError
        vals=[(x*Q,y) for x in (self.l,self.h) for y in (b.l,b.h)]
        return I(min(x//y for x,y in vals),max(-((-x)//y) for x,y in vals))
    def sq(self):
        low=0 if self.l<=0<=self.h else min(self.l**2,self.h**2)
        return I(low//Q,-((-max(self.l**2,self.h**2))//Q))
    def sqrt(self):
        if self.l<0:raise ValueError('sqrt')
        low=isqrt(self.l*Q);high=isqrt(self.h*Q)
        return I(low,high+(high*high<self.h*Q))
    def split(self):
        k=(self.l+self.h)//2
        if not self.l<k<self.h:raise ValueError('exhausted')
        return I(self.l,k),I(k,self.h)
    def endpoints(self):return [str(Fraction(self.l,Q)),str(Fraction(self.h,Q))]
    def haszero(self):return self.l<=0<=self.h

def span(bounds):
    return I(min(t.l for t in bounds),max(t.h for t in bounds))
