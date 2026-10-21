"""Fixed-landmark Lorentz distance-consistency candidate; no truth/field input.
SPDX-License-Identifier: Apache-2.0

The objective is a correlated-count working loss, NOT a likelihood certificate.
Local optimization never establishes global optimality or nonembeddability.
"""
import numpy as np
from scipy.optimize import minimize

ETA = np.array([-1., 1., 1.])
TARGET = np.array([0., 0., 0., -2., 2., 2., 0., 0., 0.])


def design(x):
    t, a, b = np.asarray(x).T
    return np.array([t, a, b, t*t, a*a, b*b, t*a, t*b, a*b])


def weights(x, scale):
    d = design(x)
    condition = float(np.linalg.cond(d))
    if not np.isfinite(condition) or condition > 1e5:
        raise ValueError('design condition')
    n = len(x)
    h = np.eye(n) + np.ones((n, n))
    kkt = np.block([[h, d.T], [d, np.zeros((9, 9))]])
    sol = np.linalg.solve(kkt, np.r_[np.zeros(n), TARGET])
    a = sol[:n]
    residual = float(max(np.max(np.abs(d@a-TARGET)), np.max(np.abs(h@a+d.T@sol[n:]))))
    if residual > 1e-7:
        raise ValueError('KKT certificate')
    return np.r_[-a.sum(), a]/scale**2, dict(condition=condition, kkt_residual=residual)


def order_check(x, order):
    x = np.vstack((np.zeros(3), x))
    delta = x[None, :, :]-x[:, None, :]
    predicted = (delta[:, :, 0] > 0) & (np.sum(delta*delta*ETA, axis=2) < 0)
    r = np.asarray(order, bool)
    return dict(passed=bool(np.array_equal(predicted, r)),
                missing=int(np.sum(r & ~predicted)), extra=int(np.sum(predicted & ~r)))


def order_constraints(order, margin):
    r = np.asarray(order)
    if r.ndim != 2 or r.shape[0] != r.shape[1] or not np.isin(r, [0, 1]).all():
        raise ValueError('complete binary order required')
    r = r.astype(bool)
    if np.diag(r).any() or (r & r.T).any() or ((r.astype(int)@r.astype(int) > 0) & ~r).any():
        raise ValueError('strict transitive order required')
    n = len(r)
    pairs = np.array([(i, j) for i in range(n) for j in range(i+1, n)])
    i, j = pairs.T
    comparable = r[i, j] | r[j, i]
    signs = np.where(comparable, -1., 1.)
    future = np.argwhere(r)

    def fun(v):
        z = np.vstack((np.zeros(3), v.reshape(n-1, 3)))
        delta = z[j]-z[i]
        return np.r_[signs*np.sum(delta*delta*ETA, axis=1)-margin**2,
                     z[future[:, 1], 0]-z[future[:, 0], 0]-margin]

    def jac(v):
        z = np.vstack((np.zeros(3), v.reshape(n-1, 3)))
        grads = 2*signs[:, None]*(z[j]-z[i])*ETA
        ans = np.zeros((len(pairs)+len(future), n, 3))
        rows = np.arange(len(pairs))
        ans[rows, j] += grads
        ans[rows, i] -= grads
        rows = np.arange(len(future))+len(pairs)
        ans[rows, future[:, 1], 0] += 1
        ans[rows, future[:, 0], 0] -= 1
        return ans[:, 1:].reshape(len(ans), -1)
    return fun, jac


def geometry(row):
    s = row['scale']
    cert = row['certificate']
    h = np.asarray(cert['gram'])/s**2
    transform = np.asarray(cert['transform'])*s
    # These positions reproduce H and V in the inherited Lorentz frame.
    landmarks = (transform@h).T
    original = (np.asarray(cert['transform'])@np.asarray(cert['vectors'])).T/s
    future = row['support'].index(row['temporal'][1])
    if original[future, 0] < 0:
        landmarks[:, 0] *= -1
    anchors = np.vstack((np.zeros(3), landmarks))
    count = {tuple(sorted(pair)): n for pair, n in zip(cert['interval_pairs'], cert['interval_counts'])}
    nodes = [row['root']]+row['landmarks']
    counts = np.array([[count[tuple(sorted((a, b)))] for a in nodes] for b in row['support']], float)
    q = (counts/(row['rho']*np.pi/12))**(2/3)/s**2
    # Delta-method scale for a fixed Poisson interval. Used only to balance
    # residuals: selection and interval overlaps invalidate independent errors.
    sigma = (2/3)*q/np.sqrt(np.maximum(counts, 1))
    return anchors, q, sigma


def loss_functions(anchors, q, sigma):
    def components(v):
        x = v.reshape(-1, 3)
        delta = x[:, None, :]-anchors[None, :, :]
        predicted = -np.sum(delta*delta*ETA, axis=2)
        residual = (predicted-q)/sigma
        return delta, predicted, residual
    def fun(v):
        return .5*float(np.sum(components(v)[2]**2))
    def jac(v):
        delta, _, residual = components(v)
        return np.sum((-2*delta*ETA)*(residual/sigma)[:, :, None], axis=1).ravel()
    return fun, jac, components


def correct(row, cfg):
    anchors, q, sigma = geometry(row)
    initial = np.asarray(row['initial_features'])
    feasible = np.asarray(row['feasible_features'])
    fun, jac, components = loss_functions(anchors, q, sigma)
    cons, cjac = order_constraints(row['observed_order'], cfg['margin'])
    # Also preserve the existing causal relation to each fixed landmark.
    # Its direction is not in this archived interface; no orientation claim
    # is made for landmark pairs, only positive timelike squared length.
    def causal(v):
        return components(v)[1].ravel()-cfg['margin']**2
    def causal_jac(v):
        delta = components(v)[0]
        result = np.zeros((len(initial), 4, len(initial), 3))
        for j in range(len(initial)):
            result[j, :, j, :] = -2*delta[j]*ETA
        return result.reshape(len(initial)*4, -1)
    result = minimize(fun, feasible.ravel(), jac=jac, method='SLSQP',
                      constraints=[dict(type='ineq', fun=cons, jac=cjac),
                                   dict(type='ineq', fun=causal, jac=causal_jac)],
                      options=dict(maxiter=cfg['maxiter'], ftol=cfg['ftol']))
    x = result.x.reshape(-1, 3)
    slacks = min(float(np.min(cons(result.x))), float(np.min(causal(result.x))))
    order = order_check(x, row['observed_order'])
    accepted = bool(result.success and slacks >= -cfg['feasibility_tolerance'] and
                    order['passed'] and fun(result.x) <= fun(feasible.ravel())+1e-8)
    out = dict(status='UNRESOLVED', features=x.tolist(), solver_success=bool(result.success),
               message=str(result.message), iterations=int(result.nit), minimum_slack=slacks,
               order=order, initial_loss=fun(initial.ravel()), feasible_loss=fun(feasible.ravel()),
               final_loss=fun(result.x), root_shell_residual_before=components(initial.ravel())[2][:, 0].tolist(),
               root_shell_residual_after=components(result.x)[2][:, 0].tolist())
    if accepted:
        try:
            w, certificate = weights(x, row['scale'])
            out.update(status='ACCEPTED', weights=w.tolist(), weight_certificate=certificate)
        except (ValueError, np.linalg.LinAlgError) as exc:
            out['reason'] = str(exc)
    return out
