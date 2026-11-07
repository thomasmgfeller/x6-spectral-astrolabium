"""Full-past clock-interval reference kernels, not a selected physical CST law."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import factorial
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'inputs'))
import memory as m


def require(ok,message):
    if not ok:raise RuntimeError(message)


@lru_cache(None)
def brute_orders(n):
    """Independent upper-triangle relation enumeration with transitivity filter."""
    return tuple(p for p in product(*(range(1<<j) for j in range(n)))
                 if all(not p[y]&~p[x] for x in range(n) for y in range(x) if p[x]>>y&1))


@lru_cache(None)
def continuations(p,k):
    if k==0:return 1
    return sum(continuations(p+(ideal,),k-1) for ideal in m.ideals(p))


def pow2(exponent):
    return F(2**exponent) if exponent>=0 else F(1,2**(-exponent))


def number_weight_squared(m0,k,alpha):
    # [f_alpha(m0+k)/f_alpha(m0)]^2; no square-root approximations.
    return pow2(-alpha*(m0*k+k*(k-1)//2))


def coefficients(p,cap,alpha=0,q=F(1)):
    return [F(continuations(p,k),factorial(k))*q**k*
            number_weight_squared(len(p),k,alpha) for k in range(cap-len(p)+1)]


def partition(p,h,cap,alpha=0,q=F(1)):
    return sum((c*h**k for k,c in enumerate(coefficients(p,cap,alpha,q))),F(0))


def derivative(p,h,cap,alpha=0,q=F(1)):
    return sum((k*c*h**(k-1) for k,c in enumerate(coefficients(p,cap,alpha,q)) if k),F(0))


def descendants(p,k):
    return tuple(x for x in brute_orders(len(p)+k) if x[:len(p)]==p)


def cut(state,tau):
    p,t,w=state;j=sum(x<=tau for x in t)
    return p[:j],t[:j],w[:j]


def action(state):
    p,t,w=state
    pred=m.with_anchor(p)
    return F(m.gravity(pred)),m.matter(pred,(F(-2),)+t,(F(0),)+w)


def action_by_increments(state):
    p,t,w=state;g=F(1);d=F(0)
    for j in range(len(p)):
        dg,dd=m.increment(m.with_anchor(p[:j]),(p[j]<<1)|1,
                          (F(-2),)+t[:j],t[j],w[j])
        g+=dg;d+=dd
    return g,d


def hazard(p,remaining,cap,alpha=0,q=F(1)):
    if len(p)==cap:return F(0)
    return q*number_weight_squared(len(p),1,alpha)*sum(
        (partition(p+(ideal,),remaining,cap,alpha,q) for ideal in m.ideals(p)),F(0)
    )/partition(p,remaining,cap,alpha,q)


def exponential_tail_bound(x,K):
    require(x>=0 and x<K+2,'Tail ratio must be less than one')
    return x**(K+1)/factorial(K+1)/(1-x/F(K+2))
