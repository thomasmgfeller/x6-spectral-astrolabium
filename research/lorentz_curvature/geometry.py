"""Exact conformal de Sitter model and iid conditional-on-N volume sampler."""
import math
import numpy as np
from scipy.integrate import quad


def require(ok, message):
    if not ok:
        raise ValueError(message)


def scale_factor(eta, h):
    require(0 <= h < 2, '0 <= h < 2 required on this coordinate diamond')
    return 1.0 / (1.0 - h*np.asarray(eta))


def oracle(h):
    require(0 <= h < 2, 'invalid h')
    tau = 1.0 if h == 0 else 2*math.atanh(h/2)/h
    integrand = lambda t: (4*math.pi/3)*(.5-abs(t))**3/(1-h*t)**4
    volume = sum(quad(integrand, a, b, epsabs=1e-13, epsrel=1e-13)[0]
                 for a, b in [(-.5, 0), (0, .5)])
    return dict(h=h, proper_time=tau, scalar_curvature=12*h*h,
                ricci_time_orthonormal=-3*h*h, volume=volume,
                H_tau=h*tau, R_tau_squared=12*(h*tau)**2)


def flat_points(rng, n):
    # Half-width has density proportional to width^3; spatial radius is uniform in a 3-ball.
    width = .5*rng.random(n)**.25
    eta = np.where(rng.integers(0, 2, n) == 0, -1., 1.)*(.5-width)
    direction = rng.normal(size=(n, 3))
    norm = np.linalg.norm(direction, axis=1)
    require(bool(np.all(norm > 0)), 'zero direction; no silent reseed')
    radius = width*rng.random(n)**(1/3)
    return np.column_stack((eta, direction*(radius/norm)[:, None]))


def sample(rng, n, family):
    require(type(n) is int and 4 <= n <= 128, 'declared N range is 4..128')
    h = family['h']
    require(0 <= h < 2, 'invalid curvature parameter')
    points, accepted, proposed = [], 0, 0
    while accepted < n:
        batch = max(256, 4*(n-accepted))
        x = flat_points(rng, batch)
        if h:
            # dV_g = a(eta)^4 d^4x; envelope a(.5)^4.
            keep = rng.random(batch) <= ((1-h*.5)/(1-h*x[:, 0]))**4
        else:
            keep = np.ones(batch, dtype=bool)
        if 'eta_min' in family:
            keep &= x[:, 0] >= family['eta_min']
        selected = x[keep][:n-accepted]
        points.append(selected)
        accepted += len(selected)
        proposed += batch
        require(proposed <= 1000000, 'sampler budget exhausted')
    x = np.concatenate(points)
    if 'spatial_factor' in family:
        x[:, 1:] *= family['spatial_factor']
    return x[np.argsort(x[:, 0], kind='stable')], proposed


def relation(x):
    require(x.ndim == 2 and x.shape[1] == 4 and bool(np.all(np.isfinite(x))), 'finite 4D points required')
    dt = x[None, :, 0]-x[:, None, 0]
    dx = x[None, :, 1:]-x[:, None, 1:]
    return (dt > 0) & (dt*dt > np.sum(dx*dx, axis=-1))


def flat_density_twin_relation(x, h):
    # Independent pair predicate; metric interpretation is flat and density is a^4.
    require(0 <= h < 2, 'invalid h')
    n = len(x)
    c = np.zeros((n, n), dtype=bool)
    for i in range(n):
        delta = x-x[i]
        c[i] = delta[:, 0] > np.sqrt(np.einsum('ij,ij->i', delta[:, 1:], delta[:, 1:]))
    return c
