"""Legendre nodes polished in long double, independently of SciPy weights."""
from functools import cache
import numpy as np
from scipy.special import roots_legendre

@cache
def polished(n):
    x=np.asarray(roots_legendre(n)[0],dtype=np.longdouble)
    for _ in range(4):
        pm=np.ones_like(x); p=x.copy()
        for k in range(2,n+1):
            pm,p=p,((2*k-1)*x*p-(k-1)*pm)/k
        d=n*(pm-x*p)/(1-x*x)
        x=x-p/d
    return (x+1)/2,1/((1-x*x)*d*d)
