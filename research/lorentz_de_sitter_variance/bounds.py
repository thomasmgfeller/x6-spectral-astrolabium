"""Bennett inversion for independent complete-cloud C2 means."""
from fractions import Fraction as Q
from functools import lru_cache
from math import comb
from common import kl,reference
from moments import certificate

THRESHOLD=Q(369,100)
STEPS=48

def bennett_bounds(e,v):
    if not isinstance(e,Q) or not isinstance(v,Q) or e<0 or v<=0:raise ValueError('nonnegative rational deviation and positive variance required')
    lo,hi=kl.log_bounds(1+e/v)
    return max(Q(0),(v+e)*lo-e),max(Q(0),(v+e)*hi-e)

@lru_cache(maxsize=1024)
def radius(v,m):
    if not isinstance(v,Q) or not 0<v<=Q(1,4) or type(m) is not int or m<1:raise ValueError('valid variance bound and cloud count required')
    target=THRESHOLD/m
    left,right=Q(0),Q(1)
    if bennett_bounds(right,v)[0]<=target:return right
    for _ in range(STEPS):
        mid=(left+right)/2
        if bennett_bounds(mid,v)[0]>target:right=mid
        else:left=mid
    assert bennett_bounds(right,v)[0]>target
    return right

def epsilon(n,m):
    if type(n) is not int or n<2:raise ValueError('integer n>=2 required')
    return radius(Q(certificate(n)['uniform_variance_upper']),m)


def confidence(total,n,m):
    e=epsilon(n,m)
    if type(total) is not int or not 0<=total<=m*comb(n,2):raise ValueError('valid integer C2 total required')
    u=Q(total,m*comb(n,2))
    return reference.invert(u-e,u+e)

def design_interval(h,n,m):
    pl,pu=reference.probability(h);e=epsilon(n,m)
    return reference.invert(pl-2*e,pu+2*e)

def sufficient(h,n,maximum):
    def passed(m):
        radius=reference.relative_radius(design_interval(h,n,m))
        return radius is not None and radius<=Q(1,5)
    if h==0 or not passed(maximum):return None
    left,right=0,maximum
    while right-left>1:
        mid=(left+right)//2
        if passed(mid):right=mid
        else:left=mid
    assert passed(right) and (right==1 or not passed(right-1))
    return right
