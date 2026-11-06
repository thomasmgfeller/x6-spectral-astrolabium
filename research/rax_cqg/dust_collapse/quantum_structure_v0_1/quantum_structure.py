"""Exact arithmetic for a scoped CST auxiliary-space qualification."""
from fractions import Fraction as Q
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from math import factorial


class I:
    """Closed rational interval; no numerical tolerance or binary floats."""
    def __init__(self, lo, hi=None):
        self.lo=Q(lo);self.hi=Q(lo if hi is None else hi)
        if self.lo>self.hi:raise ValueError('Reversed interval')
    def __add__(self, other):
        other=other if isinstance(other,I) else I(other)
        return I(self.lo+other.lo,self.hi+other.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self, other):return self+-as_i(other)
    def __mul__(self, other):
        other=as_i(other);p=[a*b for a in (self.lo,self.hi) for b in (other.lo,other.hi)]
        return I(min(p),max(p))
    __rmul__=__mul__
    def __truediv__(self, other):
        other=as_i(other)
        if other.lo<=0<=other.hi:raise ValueError('Zero denominator interval')
        return self*I(1/other.hi,1/other.lo)
    def square(self):
        lower=Q(0) if self.lo<=0<=self.hi else min(self.lo**2,self.hi**2)
        return I(lower,max(self.lo**2,self.hi**2))
    def json(self):return [decimal_bound(self.lo,False),decimal_bound(self.hi,True)]


def as_i(x):return x if isinstance(x,I) else I(x)
def decimal_bound(x,upper):
    with localcontext() as c:
        c.prec=32;c.rounding=ROUND_CEILING if upper else ROUND_FLOOR
        return str(Decimal(x.numerator)/Decimal(x.denominator))
def cadd(a,b):return a[0]+b[0],a[1]+b[1]
def cneg(a):return -a[0],-a[1]
def csub(a,b):return cadd(a,cneg(b))
def cmul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def conj(a):return a[0],-a[1]
def cscale(a,n):return a[0]*n,a[1]*n
def cjson(a):return {'real_interval':a[0].json(),'imag_interval':a[1].json()}
def g_interval(a,p):
    a=Q(a);total=(Q(1),Q(0));power=(Q(1),Q(0))
    for k in range(1,p+1):
        power=cmul(power,(Q(0),-a));total=cadd(total,cscale(power,Q(1,factorial(k)*(k+1))))
    re=(1+total[0])/2;im=total[1]/2
    r=abs(a)**(p+1)/(2*factorial(p+1)*(p+2))
    return I(re-r,re+r),I(im-r,im+r)
def matmul(A,B):
    return [[sum_complex([cmul(A[i][k],B[k][j]) for k in range(len(B))])
             for j in range(len(B[0]))] for i in range(len(A))]
def sum_complex(values):
    ans=(Q(0),Q(0))
    for v in values:ans=cadd(ans,v)
    return ans
def adjoint(A):return [[conj(A[j][i]) for j in range(len(A))] for i in range(len(A[0]))]
def real_matrix(A):return [[(Q(x),Q(0)) for x in row] for row in A]
