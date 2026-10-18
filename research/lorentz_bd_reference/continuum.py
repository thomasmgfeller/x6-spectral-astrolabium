"""Independent continuum mean: physical sphere-lens quadrature, no layer counts."""
import numpy as np
from numpy.polynomial.legendre import leggauss
from core import geometry

def mean_curvature(h, rho, epsilon, order=64):
    z, w = leggauss(order)
    z, w = (z+1)/2, w/2
    tau = geometry.oracle(h)['proper_time']
    k = rho*epsilon
    integral = 0.
    for left in [-.5, 0.]:
        t = (left+.5*z)[:, None]
        r = (.5-np.abs(t))*z[None, :]
        length = .5-t
        lo, hi = (t+.5-r)/2, (t+.5+r)/2
        v = np.zeros_like(r)
        for region, (a, b) in enumerate([(np.broadcast_to(t, r.shape), lo), (lo, hi), (hi, np.full_like(r, .5))]):
            u = a[..., None]+(b-a)[..., None]*z
            if region == 0:
                spatial = 4*np.pi/3*(u-t[..., None])**3
            elif region == 2:
                spatial = 4*np.pi/3*(.5-u)**3
            else:
                rr, ll = r[..., None], length[..., None]
                spatial = np.pi*(ll-rr)**2*(rr**2+2*rr*ll-3*(2*u-t[..., None]-.5)**2)/(12*rr)
            v += (b-a)*np.sum(w*spatial/(1-h*u)**4, axis=-1)
        xi = k*v/tau**4
        kernel = np.exp(-xi)*(1-9*xi+8*xi**2-4*xi**3/3)
        radial = np.sum(w*4*np.pi*r**2*kernel, axis=1)*(.5-np.abs(t[:, 0]))
        integral += .5*np.sum(w*radial/(1-h*t[:, 0])**4)/tau**4
    return float(-8/np.sqrt(6)*np.sqrt(k)*(-1+k*integral))
