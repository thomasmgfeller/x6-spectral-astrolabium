"""Outward fixed-point intervals and first derivatives, using integer arithmetic.
SPDX-License-Identifier: Apache-2.0
"""
from fractions import Fraction as F
T=10**30

def ceildiv(a,b):return -((-a)//b)
class I:
    def __init__(self,x=0,hi=None,raw=False):
        if raw:self.lo,self.hi=x,hi
        elif isinstance(x,I):self.lo,self.hi=x.lo,x.hi
        else:
            a=F(x);b=a if hi is None else F(hi)
            self.lo=a.numerator*T//a.denominator;self.hi=ceildiv(b.numerator*T,b.denominator)
        assert self.lo<=self.hi
    def __add__(self,o):
        if isinstance(o,D):return NotImplemented
        o=I(o);return I(self.lo+o.lo,self.hi+o.hi,raw=True)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo,raw=True)
    def __sub__(self,o):return self+-I(o)
    def __rsub__(self,o):return I(o)+-self
    def __mul__(self,o):
        if isinstance(o,D):return NotImplemented
        o=I(o);p=[a*b for a in [self.lo,self.hi] for b in [o.lo,o.hi]]
        return I(min(p)//T,ceildiv(max(p),T),raw=True)
    __rmul__=__mul__
    def inv(self):
        assert not self.lo<=0<=self.hi,'zero denominator'
        return I(T*T//self.hi,ceildiv(T*T,self.lo),raw=True)
    def __truediv__(self,o):return self*I(o).inv()
    def __rtruediv__(self,o):return I(o)*self.inv()
    def __pow__(self,n):
        assert n>=0;r=I(1)
        for _ in range(n):r=r*self
        return r
    def mag(self):return max(abs(self.lo),abs(self.hi))
    def mid(self):return I((self.lo+self.hi)//2,(self.lo+self.hi)//2,raw=True)
    def floatmid(self):return float(F(self.lo+self.hi,2*T))
    def contains(self,x):return F(self.lo,T)<=x<=F(self.hi,T)

class D:
    def __init__(self,v=0,d=0):
        if isinstance(v,D):self.v,self.d=v.v,v.d
        else:self.v,self.d=I(v),I(d)
    def __add__(self,o):o=D(o);return D(self.v+o.v,self.d+o.d)
    __radd__=__add__
    def __neg__(self):return D(-self.v,-self.d)
    def __sub__(self,o):return self+-D(o)
    def __rsub__(self,o):return D(o)+-self
    def __mul__(self,o):o=D(o);return D(self.v*o.v,self.d*o.v+self.v*o.d)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=D(o);v=self.v/o.v
        return D(v,(self.d-v*o.d)/o.v)
    def __rtruediv__(self,o):return D(o)/self
    def __pow__(self,n):
        assert n>=0;r=D(1)
        for _ in range(n):r=r*self
        return r

def matvec(A,x):return [sum(a*b for a,b in zip(row,x)) for row in A]
def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]

def verified_solve(A,b,Q,refinements=12):
    n=len(A);E=[[I(int(i==j))-v for j,v in enumerate(row)] for i,row in enumerate(mm(Q,A))]
    M=[[e.mag() for e in row] for row in E];eta=max(sum(row) for row in M)
    assert eta<T,'Neumann contraction failed'
    x=[q.mid() for q in matvec(Q,b)]
    residual=matvec(Q,[v-a for v,a in zip(b,matvec(A,x))]);a=[v.mag() for v in residual]
    radius=ceildiv(max(a)*T,T-eta);r=[radius]*n
    for _ in range(refinements):
        r=[min(old,ai+ceildiv(sum(m*v for m,v in zip(row,r)),T)) for old,ai,row in zip(r,a,M)]
    return [I(v.lo-ri,v.hi+ri,raw=True) for v,ri in zip(x,r)],F(eta,T)
