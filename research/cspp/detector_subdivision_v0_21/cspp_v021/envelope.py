"""Exact decreasing suffix envelope for the unchanged layer weight."""
from fractions import Fraction as F
from functools import lru_cache
import math, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'vendor_v020'))
from kernel import weight, signed_expectation
from flint import arb

N=95
P=[F(1),-F(9,15)-F(8,225)-F(8,10125),F(8,225)+F(12,10125),-F(4,10125)]
def shift(p,n):
    return [sum(p[j]*math.comb(j,k)*n**(j-k) for j in range(k,len(p))) for k in range(len(p))]
def certificate():
    neg=shift(P,N)
    delta=shift([F(15,16)*x-y for x,y in zip(shift(P,1),P)],N)
    if not(all(x<0 for x in neg) and all(x>0 for x in delta)):
        raise ArithmeticError('infinite suffix proof failed')
    return {'threshold':N,'P_95_plus_x':list(map(str,neg)),
            'r_P_96_plus_x_minus_P_95_plus_x':list(map(str,delta))}
certificate()
SUFFIX=[F(0)]*(N+1);SUFFIX[N]=abs(weight(N))
for i in reversed(range(N)):SUFFIX[i]=max(abs(weight(i)),SUFFIX[i+1])
def H(n):return SUFFIX[n] if n<=N else -weight(n)
@lru_cache(None)
def coefficients(n):
    return [arb(str((H(k)+weight(k))/math.factorial(k-n))) for k in range(n,N)]
def expected_H(n,mu):
    """E H(n+Pois(mu)); point mu may be an enclosing Arb ball."""
    if n<0 or mu.lower()<0:raise ValueError('nonnegative arguments required')
    correction=arb(0)
    for c in reversed(coefficients(n)):correction=correction*mu+c
    return -signed_expectation(n,mu)+(-mu).exp()*correction
def upper(nlo,mulo):
    # H decreases, so this lower-left corner dominates ALL joint (n,mu).
    mu=max(arb(0),mulo.lower())
    e=expected_H(int(nlo),mu)
    if not e.is_finite():raise ArithmeticError('finite envelope expectation')
    return min(arb(str(SUFFIX[0])),max(arb(0),e.upper()))
