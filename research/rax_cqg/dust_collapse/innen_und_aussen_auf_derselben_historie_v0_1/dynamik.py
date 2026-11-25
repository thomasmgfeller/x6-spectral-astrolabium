"""Finite strip, rooted growth rates, and interval-certified time evolution."""
from fractions import Fraction as F
from functools import lru_cache
from math import comb,lcm,gcd
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'basis'))
import variation

D=12
# (time difference, signed station displacement, interval coefficient)
STENCIL=tuple([(k,0,b) for k,b in enumerate((0,1,-9,16,-8)) if k]+
              [(12*n,s*n,b) for s in (1,-1) for n,b in enumerate((0,1,-9,16,-8)) if n]+
              [(13,s,16) for s in (1,-1)])
UNIT=10**28


def open_interval(dt,j,k,width):
    # Intersect the future of the emitter with the past of the receiver column by column.
    count=0
    for z in range(max(0,j-dt//D),min(width,j+dt//D)+1):
        lo=D*abs(z-j);hi=dt-D*abs(k-z)
        count+=max(0,hi-lo+1)
    return count-2


def geometry():
    for j in (0,4,47,92,96):
        # Outside these tests, distance >=5 or axial excess >=5 provides at least four
        # explicit intermediate points on a fastest route or on the source worldline.
        for k in range(97):
            for excess in range(6):
                dt=D*abs(k-j)+excess
                if not dt:continue
                n=open_interval(dt,j,k,96) if abs(k-j)<=6 else abs(k-j)-1
                b=variation.kernel(n)
                assert b==next((v for t,x,v in STENCIL if t==dt and x==k-j),0)
    first=sum(dt*b for dt,_,b in STENCIL);second=sum(dt**2*b for dt,_,b in STENCIL)
    assert (first,second)==(391,-83)
    # Sole future occupied receiver at the fourth exterior station of a static edge.
    witness=[(dt,s,b) for dt,s,b in STENCIL if 36+s<=32]
    assert witness==[(48,-4,-8)]
    return {'stencil':STENCIL,'first_moment':first,'second_moment':second,
            'clock_spacing_squared':'19/83','step_residual_over_h':str(F(-8*48,4))}


def poly(r):
    coeff=[F(0)]*49
    for dt,s,b in STENCIL:
        coeff[dt]+=b*dt*r**s
        coeff[0]-=b*dt
    den=lcm(*(v.denominator for v in coeff))
    return [int(v*den) for v in coeff]


def sign_at(co,q):
    # Homogeneous Horner evaluation, no floating-point polynomial evaluation.
    n,d=q.as_integer_ratio()
    v=co[-1];power=d
    for a in reversed(co[:-1]):
        v=v*n+a*power;power*=d
    return (v>0)-(v<0)


def bernstein(co,lo,hi):
    n=len(co)-1
    shifted=[sum(co[k]*comb(k,i)*lo**(k-i) for k in range(i,n+1))*(hi-lo)**i for i in range(n+1)]
    b=[sum(shifted[i]*F(comb(j,i),comb(n,i)) for i in range(j+1)) for j in range(n+1)]
    den=lcm(*(u.denominator for u in b))
    return [int(u*den) for u in b]


def split(b):
    a=list(b);left=[];right=[];n=len(b)-1
    for k in range(n+1):
        left.append(a[0]<<(n-k));right.append(a[-1]<<(n-k))
        a=[x+y for x,y in zip(a,a[1:])]
    def reduce(arr):
        divisor=gcd(*arr)
        return [v//divisor for v in arr]
    return reduce(left),reduce(right[::-1])


def root_bounds(r):
    co=poly(r);lo,hi=F(1,2),F(2)
    def visit(a,b,values,depth):
        assert depth<100 and values[0] and values[-1]  # no rational split root in these cases
        signs=[v>0 for v in values if v]
        changes=sum(s!=t for s,t in zip(signs,signs[1:]))
        if changes==0:return []
        if changes==1:
            sg=sign_at(co,a);assert sg*sign_at(co,b)==-1
            while b-a>F(1,10**32):
                m=(a+b)/2; sm=sign_at(co,m)
                if sm==0:return [(m,m)]
                if sm==sg:a=m
                else:b=m
            return [(a,b)]
        l,u=split(values);m=(a+b)/2
        return visit(a,m,l,depth+1)+visit(m,b,u,depth+1)
    return visit(lo,hi,bernstein(co,lo,hi),0)


def selection():
    rows={}
    for r in (F(1,2),F(2,3),F(3,4),F(4,5),F(7,8),F(15,16),F(31,32),F(63,64),
              *(1-F(1,2**k) for k in range(7,17))):
        bounds=root_bounds(r); rows[str(r)]=[list(map(str,p)) for p in bounds]
        if bounds:
            assert all(hi<1 for lo,hi in bounds)
            selected=max(bounds)
            assert all(hi<selected[0] for lo,hi in bounds if (lo,hi)!=selected)
            return r,selected,rows
    raise ValueError('No mode in the declared grid')


def enclose(x):
    return x.numerator*UNIT//x.denominator,-((-x.numerator*UNIT)//x.denominator)


def multiply(a,b):
    assert a[0]>=0 and b[0]>=0
    return a[0]*b[0]//UNIT,-((-a[1]*b[1])//UNIT)


@lru_cache(maxsize=None)
def power(a,n):
    if not n:return (UNIT,UNIT)
    half=power(a,n//2)
    square=multiply(half,half)
    return multiply(square,a) if n%2 else square


def weight_fn(kind,length,r,q):
    rr=enclose(r);qq=(enclose(q[0])[0],enclose(q[1])[1])
    @lru_cache(maxsize=65536)
    def at(t,j):
        assert t>=0 and 0<=j<=length
        if kind=='vacuum':return (0,0)
        if kind=='uniform' or kind=='step':
            value=UNIT//4 if kind=='uniform' or j<=32 else 0
            return value,value
        exponent=j if kind=='profile' else length-j
        a=multiply(power(qq,t),power(rr,exponent))
        return a[0]//2,-((-a[1])//2)
    return at


def backward_patch(r,q):
    # Blind evolution over 96 time steps on a small open window excised from the large strip.
    # Only the future collar and side data come from the separated solution.
    w=weight_fn('profile',3072,r,q)
    start,stop=38400,38496
    j0,j1=2532,2564
    computed={}
    def fetch(t,j):
        if t>=stop or j<j0 or j>j1:return w(t,j)
        return computed[t,j]
    widest=0
    for t in reversed(range(start,stop)):
        for j in range(j0,j1+1):
            l=u=0
            for dt,k,b in STENCIL:
                low,high=fetch(t+dt,j+k)
                a=b*dt
                if a<0:low,high=high,low
                l+=a*low;u+=a*high
            result=l//391,-((-u)//391)
            expected=w(t,j)
            assert max(result[0],expected[0])<=min(result[1],expected[1])
            widest=max(widest,result[1]-result[0])
            computed[t,j]=result
    return {'interior_fields':len(computed),'ticks':stop-start,'max_enclosure_width':str(F(widest,UNIT))}
