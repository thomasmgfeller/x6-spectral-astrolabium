"""Exact finite-domain Poisson expectation, evaluated by deterministic quadrature.

The formula is exact. Floating-point quadrature is NOT an interval certificate.
"""
from functools import lru_cache
import numpy as np
from scipy.special import roots_legendre, gammaincc, gamma
from common import modes

@lru_cache(None)
def nodes(n):return roots_legendre(n)
def mapped(n,a,b):
    x,w=nodes(n);return (a+b)/2+(b-a)*x/2,(b-a)*w/2
def integral(ell,H,L,n,ymax=8.):
    q=ell**-4;c=np.sqrt(np.pi*q/24)
    cut=min(H,np.sqrt(ymax/c));edges=[0.,cut]+([H] if cut<H else [])
    total=np.zeros(4,complex);om,k=modes().T/L
    z,w=nodes(n);unit=(z+1)/2;unit_w=w/2
    for a,b in zip(edges[:-1],edges[1:]):
        v,vw=mapped(n,a,b)
        upper=np.minimum(c*v*v,ymax)
        y=upper[:,None]*unit[None,:]
        s=y/(c*v[:,None]);u=(v[:,None]+s)/2;r=(v[:,None]-s)/2
        xi=y*y;polynomial=1-9*xi+8*xi**2-4/3*xi**3
        measure=np.pi/(2*c)*(v[:,None]-s)**2/v[:,None]
        kernel=measure*np.exp(-xi)*polynomial*np.exp(-(u*u+r*r)/(2*L*L))
        quadrature=vw[:,None]*upper[:,None]*unit_w[None,:]
        for j in range(4):
            total[j]+=np.sum(quadrature*kernel*np.exp(1j*om[j]*u)*np.sinc(k[j]*r/np.pi))
    return 4/np.sqrt(6)*np.sqrt(q)*(-1+q*total)
def tail_bounds(ell,H,L,ymax=8.):
    """Analytical absolute bounds, ordinary floating-point evaluation recorded.

    Outside-domain bound: 56*pi*q*L^2*exp(-H^2/(4L^2)).
    y-truncation bound: 8*sqrt(pi)*q*L^2*integral_ymax^inf
    exp(-y^2)*(1+9y^2+8y^4+4/3*y^6) dy.
    Neither term bounds the remaining numerical quadrature error.
    """
    q=ell**-4
    tail=sum(a*.5*gamma(j+.5)*gammaincc(j+.5,ymax*ymax) for j,a in enumerate([1.,9.,8.,4/3]))
    return {'outside_H_analytic_bound_float':float(56*np.pi*q*L*L*np.exp(-H*H/(4*L*L))),
            'y_truncation_analytic_bound_float':float(8*np.sqrt(np.pi)*q*L*L*tail)}
