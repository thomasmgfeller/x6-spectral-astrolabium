"""Outward integer interval arithmetic for a finite list of scalar functions."""
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from functools import lru_cache
from math import cos, factorial, isqrt, pi

BITS=256
S=1<<BITS

def ceildiv(x,y):
    return -((-x)//y)

class I:
    __slots__=('lo','hi')
    def __init__(self,lo,hi):
        assert lo<=hi
        self.lo,self.hi=lo,hi

    @staticmethod
    def of(value):
        if isinstance(value,I):
            return value
        v=Q(value)*S
        return I(v.__floor__(),v.__ceil__())

    def __add__(self,b):
        b=I.of(b)
        return I(self.lo+b.lo,self.hi+b.hi)
    __radd__=__add__
    def __neg__(self):
        return I(-self.hi,-self.lo)
    def __sub__(self,b):
        return self+(-I.of(b))
    def __rsub__(self,b):
        return I.of(b)+(-self)
    def __mul__(self,b):
        b=I.of(b)
        prod=[self.lo*b.lo,self.lo*b.hi,self.hi*b.lo,self.hi*b.hi]
        return I(min(prod)//S,ceildiv(max(prod),S))
    __rmul__=__mul__
    def __truediv__(self,b):
        b=I.of(b)
        assert b.lo>0 or b.hi<0
        return self*I(S*S//b.hi,ceildiv(S*S,b.lo))
    def __rtruediv__(self,b):
        return I.of(b)/self
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        out=I.of(1);power=self
        while n:
            if n%2:out=out*power
            n//=2
            if n:power=power*power
        return out
    def sqrt(self):
        assert self.lo>=0
        return I(isqrt(self.lo*S),isqrt(self.hi*S)+1)
    def absmax(self):
        return max(-self.lo,self.hi)
    def rounded(self,digits=13):
        grid=10**digits
        return [str(Q(self.lo*grid//S,grid)),str(Q(ceildiv(self.hi*grid,S),grid))]

def widen(x,amount):
    err=I.of(amount).hi
    return I(x.lo-err,x.hi+err)

class C:
    __slots__=('re','im')
    def __init__(self,re,im=0):
        self.re,self.im=I.of(re),I.of(im)
    def __add__(self,b):
        return C(self.re+b.re,self.im+b.im)
    def __mul__(self,b):
        return C(self.re*b.re-self.im*b.im,self.re*b.im+self.im*b.re)
    def scale(self,a):
        return C(self.re*a,self.im*a)
    def conj(self):
        return C(self.re,-self.im)
    def pad(self,e):
        return C(widen(self.re,e),widen(self.im,e))

def cis(x):
    """Taylor on a real interval contained in [-1/4,1/4], then doubling."""
    n=0
    while x.absmax()>S//4:
        x=x/2;n+=1
    t=C(1);out=t
    for j in range(1,33):
        t=C(-t.im*x/j,t.re*x/j)
        out=out+t
    out=out.pad(Q(1,4**33*factorial(33)))
    for _ in range(n):out=out*out
    return out

def sinc(x):
    assert x.absmax()<S
    t=I.of(1);out=t
    for k in range(1,18):
        t=-t*x*x/((2*k)*(2*k+1));out=out+t
    return widen(out,Q(1,factorial(37)))

def angle(z):
    assert z.re.lo>0
    x=z.im/z.re
    assert x.absmax()<S//2
    term=x;out=x
    for k in range(1,40):
        term=-term*x*x;out=out+term/(2*k+1)
    return widen(out,Q(1,2**81*81))

def legendre(k,x):
    a,b=1,x
    if k==0:return a
    for j in range(2,k+1):
        a,b=b,((2*j-1)*x*b-(j-1)*a)/j
    return b

def sign_at(n,x,den):
    a,b=1,x
    for j in range(2,n+1):
        a,b=b,(2*j-1)*x*b-(j-1)**2*den**2*a
    return (b>0)-(b<0)

@lru_cache(None)
def gaussian(n):
    """Seeds only use floating point. All stored brackets and weights are certified."""
    scale=1<<193
    rule=[]
    for k in range(1,n+1):
        with localcontext() as ctx:
            ctx.prec=90
            x=Decimal(str(cos(pi*(k-.25)/(n+.5))))
            for _ in range(10):
                p=legendre(n,x)
                deriv=n*(legendre(n-1,x)-x*p)/(1-x*x)
                x=x-p/deriv
            centre=int(x*scale)
        l,r=centre-2,centre+2
        assert sign_at(n,l,scale)*sign_at(n,r,scale)==-1
        root=I(l*(S//scale),r*(S//scale))
        weight=(1-root*root)/(n**2*legendre(n-1,root)**2)
        assert weight.lo>0
        rule.append((root,weight))
    rule.reverse()
    assert all(a[0].hi<b[0].lo for a,b in zip(rule,rule[1:]))
    assert sum(r[1] for r in rule).lo<=S<=sum(r[1] for r in rule).hi
    return rule
