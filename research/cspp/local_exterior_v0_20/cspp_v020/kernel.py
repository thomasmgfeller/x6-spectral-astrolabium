"""Exact conditional layer-weight expectation; no geometry/forcing factorization."""
from fractions import Fraction as F
from functools import lru_cache
import math
from flint import arb

EPS=F(1,16)
R=1-EPS


@lru_cache(None)
def weight(n):
    return sum(F(c*math.comb(n,k))*EPS**k*R**(n-k)
               for k,c in enumerate([1,-9,16,-8]) if k<=n)


def polynomial(n):
    return 1-F(9,15)*n+F(8,225)*n*(n-1)-F(4,10125)*n*(n-1)*(n-2)


@lru_cache(None)
def positive_indices():
    # P(128+x) has four strictly negative coefficients, so P(n)<0 for n>=128.
    coeff=[F(1),-F(9,15)-F(8,225)-F(8,10125),F(8,225)+F(12,10125),-F(4,10125)]
    shifted=[sum(coeff[j]*math.comb(j,k)*128**(j-k) for j in range(k,4)) for k in range(4)]
    if not all(v<0 for v in shifted):raise ArithmeticError('infinite sign certificate')
    return [n for n in range(128) if weight(n)>0],shifted


def signed_expectation(n0,mu):
    z=mu/16
    P=[1-9*z+8*z*z-arb(4)/3*z**3,-9+16*z-4*z*z,16-8*z,arb(-8)]
    return (-z).exp()*sum((arb(str(F(math.comb(n0,j))*EPS**j*R**(n0-j)))*P[j]
                             for j in range(min(n0,3)+1)),arb(0))


def absolute_expectation(n0,mu):
    positive,_=positive_indices()
    correction=sum((arb(str(weight(n)))*mu**(n-n0)/math.factorial(n-n0)
                    for n in positive if n>=n0),arb(0))
    return -signed_expectation(n0,mu)+2*(-mu).exp()*correction


def direct_sum(n0,mu,cutoff=2048):
    prob=(-mu).exp()
    total=arb(0)
    for j in range(cutoff+1):
        total+=prob*abs(arb(str(weight(n0+j))))
        prob*=mu/(j+1)
    k=cutoff+1
    if mu==0:
        tail=arb(0)
    else:
        tail=(-mu).exp()*(arb(1).exp()*mu/k)**k*arb('4976184375/4294967296')
    # One-sided remainder [0,tail], outward rounded as a ball.
    return total+arb(tail/2,tail/2)
