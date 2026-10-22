"""Joint 4-landmark fit in raw count space, with complete observed order.

Only packet, counts and known density enter inference. No truth or fields.
The sum of marginal Poisson deviances is a COMPOSITE objective: overlaps
make counts dependent. No inverse-Hessian uncertainty is claimed.
SPDX-License-Identifier: Apache-2.0
"""
import sys
import time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

SOURCE = Path(__file__).resolve().parent.parent / 'four_landmark_count_covariance/evidence'
sys.path.insert(0, str(SOURCE))
from inference import ETA, four, four_geometry, normalize, strict_order_check


def input_mask(packet):
    m = len(packet['pairs'])
    mask = np.any(four_geometry(np.ones(m), packet)[2] != 0, axis=(0, 1))
    anchors = set(packet['landmarks'])
    return mask | np.array([a in anchors and b in anchors for a, b in packet['pairs']])


def canonical(points):
    """Fix translations, boosts and spatial rotations using landmarks 0,1,2."""
    z = np.asarray(points, float) - points[0]
    d = z[1]; q = d[0]**2 - d[1:] @ d[1:]
    if q <= 0: raise ValueError('initial gauge pair is not timelike')
    v = d[1:] / d[0]; vv = v @ v; gamma = abs(d[0]) / np.sqrt(q)
    t = gamma * (z[:, 0] - z[:, 1:] @ v)
    spatial = z[:, 1:] + (((gamma-1) * (z[:, 1:] @ v) / vv if vv > 1e-28 else np.zeros(len(z))) - gamma*z[:, 0])[:, None]*v
    r = np.linalg.norm(spatial[2])
    if r < 1e-10: raise ValueError('initial rotation gauge is singular')
    ex = spatial[2] / r; ey = np.array([-ex[1], ex[0]])
    out = np.column_stack((t, spatial @ ex, spatial @ ey))
    out[0] = 0.; out[1, 1:] = 0.; out[2, 2] = 0.
    return out


class Model:
    def __init__(self, packet, counts, rho, cfg):
        self.packet = packet; self.cfg = cfg
        self.nodes = packet['landmarks'] + [packet['root']] + packet['support']
        self.n = len(self.nodes); self.lookup = {a:i for i,a in enumerate(self.nodes)}
        self.free = np.ones((self.n, 3), bool)
        self.free[0] = False; self.free[1, 1:] = False; self.free[2, 2] = False
        self.indices = np.flatnonzero(self.free.ravel())
        pairs = np.array([[self.lookup[a], self.lookup[b]] for a,b in packet['pairs']])
        self.mask = input_mask(packet)
        self.a, self.b = pairs[self.mask].T
        self.counts = np.asarray(counts, float)[self.mask]
        self.factor = rho*np.pi/12 * packet['scale']**3
        self.i, self.j = np.triu_indices(self.n, 1)
        r = np.asarray(packet['full_order'], bool)
        self.causal = r[self.i, self.j] | r[self.j, self.i]
        self.sign = np.where(self.causal, -1., 1.)
        self.direction = np.where(r[self.i, self.j], 1., -1.)[self.causal]

    def pack(self, z): return np.asarray(z).ravel()[self.indices]

    def unpack(self, x):
        z = np.zeros(self.n*3); z[self.indices] = x
        return z.reshape(self.n, 3)

    def interval(self, x, a, b):
        z = self.unpack(x); d = z[b] - z[a]
        s = (d*d) @ ETA
        jac = np.zeros((len(a), self.n, 3)); ix = np.arange(len(a))
        jac[ix, a] = -2*d*ETA; jac[ix, b] = 2*d*ETA
        return s, jac.reshape(len(a), -1)[:, self.indices], d

    def objective(self, x):
        s, ds, _ = self.interval(x, self.a, self.b)
        q = np.maximum(-s, 1e-12); lam = self.factor*q**1.5
        # Numerically stable deviance near its zero, extended outside feasibility.
        u = (lam-self.counts)/self.counts
        value = 2*np.mean(self.counts*(u-np.log1p(u)))
        if not np.isfinite(value):
            value = 2*np.mean(lam-self.counts+self.counts*np.log(self.counts/lam))
        dlam = -1.5*self.factor*np.sqrt(q)[:, None]*ds
        dlam[-s <= 1e-12] = 0.
        grad = 2/len(lam)*(1-self.counts/lam) @ dlam
        return float(value), grad

    def constraints(self, x):
        s, ds, d = self.interval(x, self.i, self.j)
        margin = self.cfg['interval_margin']
        c = self.sign*s-margin
        dc = self.sign[:, None]*ds
        # Timelike interval alone does not determine its observed orientation.
        orient = self.direction*d[self.causal, 0]-self.cfg['time_margin']
        dt = np.zeros((int(self.causal.sum()), self.n, 3)); ix=np.arange(len(dt))
        dt[ix, self.i[self.causal], 0] = -self.direction
        dt[ix, self.j[self.causal], 0] = self.direction
        return np.r_[c, orient], np.vstack((dc, dt.reshape(len(dt), -1)[:, self.indices]))


def estimate(packet, counts, rho, cfg):
    begun = time.monotonic(); out = dict(status='UNRESOLVED', qualified=False)
    counts = np.asarray(counts, float); mask = input_mask(packet)
    if np.min(counts[mask]) < cfg['minimum_count']:
        return dict(status='COUNT_HOLD', qualified=False, seconds=time.monotonic()-begun)
    try:
        q = (counts/(rho*np.pi/12))**(2/3)/packet['scale']**2
        h,z,_,_ = four_geometry(q, packet); transform,_ = normalize(h)
        initial = (transform @ z.T).T
        future = packet['support'].index(packet['temporal'][1])+5
        if initial[future,0] < 0: initial[:,0] *= -1
        initial = canonical(initial)
        model = Model(packet, counts, rho, cfg); x0 = model.pack(initial)
        if np.max(abs(x0)) >= cfg['coordinate_bound']:
            raise ValueError('initial coordinate budget')
        def guard(x):
            if time.monotonic()-begun > cfg['fit_seconds']:
                raise TimeoutError('fit time budget')
        result = minimize(model.objective, x0, jac=True, method='SLSQP',
            bounds=[(-cfg['coordinate_bound'], cfg['coordinate_bound'])]*len(x0),
            constraints=[dict(type='ineq', fun=lambda x:model.constraints(x)[0],
                             jac=lambda x:model.constraints(x)[1])],
            callback=guard, options=dict(maxiter=cfg['max_iterations'], ftol=cfg['ftol']))
        fitted = model.unpack(result.x); c,_ = model.constraints(result.x)
        order = strict_order_check(fitted, packet['full_order'])
        out.update(optimizer_success=bool(result.success), optimizer_message=str(result.message),
                   iterations=int(result.nit), initial_objective=model.objective(x0)[0],
                   objective=float(result.fun), minimum_constraint=float(c.min()), order=order,
                   active_interval_constraints=int(np.sum(c[:len(model.i)] < 1e-6)),
                   coordinates=fitted, fitted_counts=model.factor*np.maximum(-model.interval(result.x, model.a, model.b)[0],0)**1.5)
        if not result.success: raise ValueError('optimizer did not converge')
        if c.min() < -cfg['constraint_tolerance'] or not order['passed']:
            raise ValueError('full order or feasibility failed')
        pairs=np.array([[model.lookup[a],model.lookup[b]] for a,b in packet['pairs']])
        qfit=-np.sum((fitted[pairs[:,1]]-fitted[pairs[:,0]])**2*ETA,axis=1)
        operator = four(qfit,packet)
        if not operator['qualified']: raise ValueError('independent reconstructed order failed')
        out.update(status='WEIGHTS_VALID', qualified=True, weights=operator['weights'],
                   certificate=operator['certificate'], landmark_condition=operator['landmark_condition'])
    except (ValueError, np.linalg.LinAlgError, TimeoutError) as exc:
        out.update(reason=str(exc))
    out['seconds']=time.monotonic()-begun
    return out
