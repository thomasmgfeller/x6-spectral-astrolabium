"""Independent geometric quadrature for C2 in a 4D conformal diamond.

No RSS coefficients enter this module. Integrate the spatial intersection of
the future ball of x and past ball of q at each conformal time u.
"""
from functools import lru_cache
import numpy as np
from numpy.polynomial.legendre import leggauss


@lru_cache(None)
def nodes(order):
    z, w = leggauss(order)
    return (z+1)/2, w/2


def volume(h, order=32):
    z, w = nodes(order)
    total = 0.
    for left in [-.5, 0.]:
        t = left+.5*z
        total += .5*np.sum(w*(4*np.pi/3)*(.5-np.abs(t))**3/(1-h*t)**4)
    return float(total)


def pair_probability(h, order=32):
    if not (0 <= h < 2) or order < 4:
        raise ValueError('0 <= h < 2 and quadrature order >= 4 required')
    z, w = nodes(order)
    integral = 0.
    for left in [-.5, 0.]:
        t = (left+.5*z)[:, None]
        radius = (.5-np.abs(t))*z[None, :]
        L = .5-t
        lo = (t+.5-radius)/2
        hi = (t+.5+radius)/2
        future_volume = np.zeros_like(radius)
        for region, (a, b) in enumerate([(np.broadcast_to(t, radius.shape), lo),
                                         (lo, hi), (hi, np.full_like(radius, .5))]):
            u = a[..., None]+(b-a)[..., None]*z
            if region == 0:
                spatial = (4*np.pi/3)*(u-t[..., None])**3
            elif region == 2:
                spatial = (4*np.pi/3)*(.5-u)**3
            else:
                r = radius[..., None]
                length = L[..., None]
                spatial = np.pi*(length-r)**2*(r*r+2*r*length-3*(2*u-t[..., None]-.5)**2)/(12*r)
            future_volume += (b-a)*np.sum(w*spatial/(1-h*u)**4, axis=-1)
        radial = np.sum(w[None, :]*4*np.pi*radius**2*future_volume, axis=1)*(.5-np.abs(t[:, 0]))
        integral += .5*np.sum(w*radial/(1-h*t[:, 0])**4)
    return float(2*integral/volume(h, order)**2)
