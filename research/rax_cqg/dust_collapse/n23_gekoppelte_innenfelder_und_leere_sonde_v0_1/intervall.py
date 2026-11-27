"""Closed rational intervals and a decimal proposal for a rational preconditioner."""
from decimal import Decimal,localcontext
from fractions import Fraction as F

class I:
    def __init__(self,lo=0,hi=None):
        self.l=F(lo);self.h=F(hi) if hi is not None else self.l
        assert self.l<=self.h
    def __add__(self,b):
        if isinstance(b,I):return I(self.l+b.l,self.h+b.h)
        return I(self.l+b,self.h+b)
    __radd__=__add__
    def __neg__(self):return I(-self.h,-self.l)
    def __sub__(self,b):return self+(-b)
    def __rsub__(self,b):return (-self)+b
    def __mul__(self,b):
        if isinstance(b,I):
            vals=(self.l*b.l,self.l*b.h,self.h*b.l,self.h*b.h)
            return I(min(vals),max(vals))
        return I(self.l*b,self.h*b) if b>=0 else I(self.h*b,self.l*b)
    __rmul__=__mul__
    def __truediv__(self,b):
        if not isinstance(b,I):return self*(F(1)/b)
        assert b.l*b.h>0
        return self*I(1/b.h,1/b.l)
    def mid(self):return (self.l+self.h)/2
    def mag(self):return max(abs(self.l),abs(self.h))
    def data(self):return list(map(str,(self.l,self.h)))

def inverse_seed(jac):
    # Rounding only affects the candidate. All subsequent inequalities are exact.
    with localcontext() as ctx:
        ctx.prec=48
        n=len(jac);a=[]
        for i,row in enumerate(jac):
            q=[v.mid() for v in row]
            a.append([Decimal(v.numerator)/Decimal(v.denominator) for v in q]+[Decimal(i==j) for j in range(n)])
        for j in range(n):
            pivot=max(range(j,n),key=lambda i:abs(a[i][j]))
            a[pivot],a[j]=a[j],a[pivot]
            p=a[j][j];assert p
            a[j]=[v/p for v in a[j]]
            for i in range(n):
                if i!=j and a[i][j]:
                    k=a[i][j];a[i]=[u-k*v for u,v in zip(a[i],a[j])]
        return [[(k,F(v).limit_denominator(10**14)) for k,v in enumerate(row[n:]) if abs(v)>Decimal('1e-24')] for row in a]
