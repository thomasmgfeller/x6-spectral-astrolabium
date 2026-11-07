"""Rationally enclosed Gauss-Legendre nodes and rigorous tensor remainders."""
from functools import lru_cache
from fractions import Fraction as F
from math import comb,cos,pi,factorial
import intervals_fp as fp


def require(ok,message):fp.require(ok,message)


def integer_poly(coeff,num,den):
    value=coeff[-1];power=den
    for c in reversed(coeff[:-1]):value=value*num+c*power;power*=den
    return value


def seed(q,j):
    x=cos(pi*(j+0.75)/(q+0.5))
    for _ in range(12):
        a,b=1.0,x
        for k in range(2,q+1):a,b=b,((2*k-1)*x*b-(k-1)*a)/k
        dp=q*(x*b-a)/(x*x-1);dx=b/dp;x-=dx
        if abs(dx)<1e-16:break
    return (x+1)/2


def root_interval(q,j,coeff):
    bits=30;den=1<<bits;center=round(seed(q,j)*den);radius=1024
    while True:
        lo=max(0,center-radius);hi=min(den,center+radius)
        sl=integer_poly(coeff,lo,den);sh=integer_poly(coeff,hi,den)
        if sl*sh<0:break
        radius*=2;require(radius<den,'Root sign bracket')
    while hi-lo>1:
        mid=(lo+hi)//2;sm=integer_poly(coeff,mid,den)
        require(sm!=0,'Even-order root is not a dyadic endpoint')
        if sl*sm<0:hi=mid;sh=sm
        else:lo=mid;sl=sm
    while bits<fp.BITS:
        lo*=2;hi*=2;den*=2;bits+=1;mid=lo+1;sm=integer_poly(coeff,mid,den)
        require(sm!=0,'Non-dyadic Legendre root')
        if sl*sm<0:hi=mid;sh=sm
        else:lo=mid;sl=sm
    require(sl*sh<0 and hi-lo==1,'Certified root bracket')
    return fp.I(lo,hi)


@lru_cache(None)
def rule(q):
    coeff=[(-1)**(q-k)*comb(q,k)*comb(q+k,k) for k in range(q+1)]
    nodes=sorted((root_interval(q,j,coeff) for j in range(q)),key=lambda x:x.lo)
    require(all(0<x.lo<x.hi<fp.S for x in nodes) and
            all(a.hi<b.lo for a,b in zip(nodes,nodes[1:])),'All q roots isolated')
    weights=[]
    for u in nodes:
        x=2*u-1;a=fp.ONE;b=x
        for k in range(2,q+1):a,b=b,((2*k-1)*x*b-(k-1)*a)/k
        dp=q*(x*b-a)/(x*x-1)
        weight=fp.ONE/((1-x*x)*dp*dp)
        require(weight.lo>0,'Positive Gaussian weight');weights.append(weight)
    exactness=0
    for k in range(2*q):
        value=sum((w*(x**k) for x,w in zip(nodes,weights)),fp.ZERO)
        require(value.contains(F(1,k+1)),'Certified Gaussian monomial exactness');exactness+=1
    return nodes,weights,{'order':q,'root_sign_brackets':q,'positive_weights':q,
        'monomial_checks':exactness,'nodes':[x.endpoints() for x in nodes],
        'weights':[x.endpoints() for x in weights]}


def derivative_majorants(D,A,max_order):
    out=[F(1),D]
    for k in range(2,max_order+1):out.append(D*out[-1]+2*A*(k-1)*out[-2])
    return out


def error_bound(q,D,A,coordinate,n):
    k=2*q;H=derivative_majorants(D,A,k)
    B=factorial(n)*sum((comb(k,l)*F(factorial(coordinate),factorial(coordinate-l))*H[k-l]
                        for l in range(coordinate+1)),F(0))
    C=F(factorial(q)**4,(2*q+1)*factorial(2*q)**3)
    return C*B


def select_orders(bounds,mu,tolerance,n):
    qs=[]
    for j in range(n):
        for q in range(8,65,2):
            worst=max(error_bound(q,abs(mu)*x[j]['D'],abs(mu)*x[j]['A'],j,n) for x in bounds)
            if worst<=tolerance/(2*n):qs.append(q);break
        else:raise RuntimeError('Declared Gaussian order budget insufficient')
    errors=[sum((error_bound(q,abs(mu)*b[j]['D'],abs(mu)*b[j]['A'],j,n)
                 for j,q in enumerate(qs)),F(0)) for b in bounds]
    return qs,errors
