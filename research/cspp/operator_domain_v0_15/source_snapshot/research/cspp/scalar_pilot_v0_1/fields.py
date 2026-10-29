"""Analytic compact test fields; metric (-,+,+,+), lengths in L0."""
import numpy as np
from scipy.special import expit

NAMES = ['1', 't', 'z', 't2', 'z2', 'tz', 'wave_k0', 'wave_k2', 'wave_k4', 'wave_k8']

def taper(q):
    q = np.asarray(q)
    h, d, dd = (np.zeros_like(q) for _ in range(3))
    h[q <= 1] = 1
    use = (q > 1) & (q < 3)
    s = (q[use]-1)/2
    v = expit(1/s-1/(1-s))
    kp = -1/s**2-1/(1-s)**2
    kpp = 2/s**3-2/(1-s)**3
    h[use] = v
    d[use] = v*(1-v)*kp/2
    dd[use] = v*(1-v)*(kpp+(1-2*v)*kp**2)/4
    return h, d, dd

def fields(x):
    """Return phi and exact Box phi, with shared C-infinity cutoff chi."""
    x = np.asarray(x, dtype=float)
    t, z = x[:, 0], x[:, 3]
    r = np.linalg.norm(x[:, 1:], axis=1)
    ht, dt, ddt = taper(np.abs(t)); hr, dr, ddr = taper(r)
    chi = ht*hr
    ct = np.sign(t)*dt*hr
    over_r = np.divide(dr, r, out=np.zeros_like(r), where=r>0)
    cz = ht*over_r*z
    bc = -ddt*hr+ht*(ddr+2*over_r)
    one, zero = np.ones_like(t), np.zeros_like(t)
    polys = [one, t, z, t*t, z*z, t*z]
    pt = [zero, one, zero, 2*t, zero, z]
    pz = [zero, zero, one, zero, 2*z, t]
    bp = [zero, zero, zero, -2*one, 2*one, zero]
    vals = [chi*p for p in polys]
    boxes = [bc*p+chi*b+2*(-ct*a+cz*c) for p,a,c,b in zip(polys,pt,pz,bp)]
    for k in [0,2,4,8]:
        omega = np.sqrt(k*k+1)
        e = np.exp(1j*(k*z-omega*t))
        vals.append(chi*e)
        boxes.append(e*(bc+chi+2j*(omega*ct+k*cz)))
    return np.asarray(vals).T.astype(complex), np.asarray(boxes).T.astype(complex)

def rms(a, axis=0):
    return np.sqrt(np.mean(np.abs(a)**2, axis=axis))
