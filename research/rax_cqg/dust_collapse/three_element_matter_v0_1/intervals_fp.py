"""Outward fixed-point interval arithmetic; every endpoint is an integer / 2**160."""
from fractions import Fraction as F
from math import factorial

BITS=160
S=1<<BITS


def require(ok,message):
    if not ok:raise RuntimeError(message)


def ceildiv(a,b):return -((-a)//b)


class I:
    __slots__=('lo','hi')
    def __init__(self,lo,hi=None):
        self.lo=lo;self.hi=lo if hi is None else hi
        require(self.lo<=self.hi,'Ordered interval')
    @classmethod
    def rational(cls,x):
        x=F(x);return cls(x.numerator*S//x.denominator,ceildiv(x.numerator*S,x.denominator))
    def __add__(self,other):
        b=as_i(other);return I(self.lo+b.lo,self.hi+b.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,other):return self+-as_i(other)
    def __rsub__(self,other):return as_i(other)+-self
    def __mul__(self,other):
        if isinstance(other,int):return I(self.lo*other,self.hi*other) if other>=0 else -self*(-other)
        b=as_i(other)
        if self.lo>=0 and b.lo>=0:lo,hi=self.lo*b.lo,self.hi*b.hi
        else:
            values=(self.lo*b.lo,self.lo*b.hi,self.hi*b.lo,self.hi*b.hi);lo=min(values);hi=max(values)
        return I(lo//S,ceildiv(hi,S))
    __rmul__=__mul__
    def __truediv__(self,other):
        if isinstance(other,int):
            require(other!=0,'Nonzero integer divisor')
            return I(self.lo//other,ceildiv(self.hi,other)) if other>0 else -self/(-other)
        b=as_i(other);require(b.lo>0 or b.hi<0,'Interval divisor excludes zero')
        if b.hi<0:return (-self)/(-b)
        pairs=[(self.lo*S,b.lo),(self.lo*S,b.hi),(self.hi*S,b.lo),(self.hi*S,b.hi)]
        return I(min(a//d for a,d in pairs),max(ceildiv(a,d) for a,d in pairs))
    def __pow__(self,n):
        require(isinstance(n,int) and n>=0,'Nonnegative integer power')
        out=ONE;base=self
        while n:
            if n&1:out=out*base
            n//=2
            if n:base=base*base
        return out
    def widen(self,radius):return I(self.lo-radius,self.hi+radius)
    def contains(self,x):
        x=F(x);return self.lo*x.denominator<=x.numerator*S<=self.hi*x.denominator
    def midpoint(self):return F(self.lo+self.hi,2*S)
    def radius(self):return F(self.hi-self.lo,2*S)
    def endpoints(self):return [F(self.lo,S),F(self.hi,S)]


def as_i(x):return x if isinstance(x,I) else I.rational(x)
ZERO=I(0);ONE=I(S)


def atan_enclosure(den):
    total=sum((F((-1)**k,(2*k+1)*den**(2*k+1)) for k in range(80)),F(0))
    remainder=F(1,161*den**161)
    return I.rational(total).widen(0),I.rational(total+remainder)


_a,_b=atan_enclosure(5);_c,_d=atan_enclosure(239)
PI=16*I(_a.lo,_b.hi)-4*I(_c.lo,_d.hi)
require(F(PI.lo,S)>3 and F(PI.hi,S)<F(22,7),'Coarse rational Machin enclosure')


def cis(t):
    """Enclose exp(i*t) by interval range reduction and real Taylor remainders."""
    t=as_i(t);k=round(F(2*(t.lo+t.hi),PI.lo+PI.hi));x=t-PI*k/2
    require(max(abs(x.lo),abs(x.hi))<=S,'Reduced phase bounded by one')
    x2=x*x;c=ONE;s=x;tc=ONE;ts=x
    for j in range(1,17):
        tc=-(tc*x2)/((2*j-1)*(2*j));ts=-(ts*x2)/((2*j)*(2*j+1))
        c=c+tc;s=s+ts
    c=c.widen(ceildiv(S,factorial(34)));s=s.widen(ceildiv(S,factorial(35)))
    return ((c,s),(-s,c),(-c,-s),(s,-c))[k%4]


def density_characteristic(t):
    """Enclose 1/2 + 1/2*integral_0^1 exp(-i*t*w) dw, including its t=0 limit."""
    t=as_i(t)
    if max(abs(t.lo),abs(t.hi))<=S:
        re=ONE;im=ZERO;term=ONE
        for k in range(1,37):
            term=term*t/(k+1)
            if k%4==0:re=re+term
            elif k%4==1:im=im-term
            elif k%4==2:re=re-term
            else:im=im+term
        e=ceildiv(S,2*factorial(38))
        return ((ONE+re)/2).widen(e),(im/2).widen(e)
    c,s=cis(t)
    return (ONE+s/t)/2,-((ONE-c)/t)/2


def cmul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def cadd(a,b):return a[0]+b[0],a[1]+b[1]
def cscale(a,b):return a[0]*b,a[1]*b


def audit():
    values=list(map(F,['-7/3','-1','0','1/3','5/2']));checks=0
    for a in values:
        for b in values:
            x=I.rational(a);y=I.rational(b)
            require((x+y).contains(a+b) and (x-y).contains(a-b) and (x*y).contains(a*b),
                    'Signed rational arithmetic controls');checks+=3
            if b:require((x/y).contains(a/b),'Signed interval quotient');checks+=int(bool(b))
    for k,exact in enumerate([(1,0),(0,1),(-1,0),(0,-1),(1,0)]):
        z=cis(PI*k/2)
        require(z[0].contains(exact[0]) and z[1].contains(exact[1]),'Certified quadrant controls')
    z=density_characteristic(ZERO)
    require(z[0].contains(1) and z[1].contains(0),'Density zero-argument limit')
    return {'rational_arithmetic_checks':checks,'quadrant_checks':5,'density_zero_limit':'PASS'}
