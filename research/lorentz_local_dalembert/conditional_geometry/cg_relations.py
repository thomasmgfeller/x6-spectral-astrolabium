"""Order-only convex inner approximation, with explicit numerical acceptance.

Related pairs use future Lorentz cones. For incomparable pairs, a fixed spatial
direction from the initial reconstruction gives TWO affine separating planes.
This sufficient feasible region is convex, but need not contain an embedding
of every embeddable order. Solver failure therefore means UNRESOLVED.
"""
import numpy as np
from scipy.optimize import minimize


def validate_order(order):
    r = np.asarray(order)
    if r.ndim != 2 or r.shape[0] != r.shape[1] or not np.isin(r, [0, 1]).all():
        raise ValueError('binary square strict order required')
    r = r.astype(bool)
    if np.diag(r).any() or (r & r.T).any():
        raise ValueError('reflexive or cyclic order')
    if ((r.astype(np.int64) @ r.astype(np.int64) > 0) & ~r).any():
        raise ValueError('transitive closure required; missing is not unknown')
    return r


def check(points, order):
    """Independent squared-interval predicate; no tolerance-created relations."""
    x = np.asarray(points, float)
    r = validate_order(order)
    if x.shape != (len(r), 3) or not np.isfinite(x).all():
        raise ValueError('finite 2+1 coordinates required')
    dt = x[None, :, 0]-x[:, None, 0]
    ds = x[None, :, 1:]-x[:, None, 1:]
    predicted = (dt > 0) & (dt*dt > np.sum(ds*ds, axis=2))
    return dict(missing=int(np.sum(r & ~predicted)), extra=int(np.sum(predicted & ~r)),
                passed=bool(np.array_equal(r, predicted)), pairs=int(len(r)*(len(r)-1)),
                true_relations=int(r.sum()))


def constraints(initial, order, margin):
    n = len(initial)
    related = np.argwhere(order)
    unrelated = np.array([(i, j) for i in range(n) for j in range(i+1, n)
                          if not order[i, j] and not order[j, i]], dtype=int).reshape(-1, 2)
    delta = initial[unrelated[:, 1], 1:] - initial[unrelated[:, 0], 1:]
    norms = np.linalg.norm(delta, axis=1)
    if np.any(norms <= 1e-12):
        raise ValueError('no fixed spatial separator for a coincident incomparable pair')
    directions = delta / norms[:, None]
    i, j = related.T if len(related) else (np.array([], int), np.array([], int))
    a, b = unrelated.T if len(unrelated) else (np.array([], int), np.array([], int))

    def unpack(v):
        return np.vstack((np.zeros(3), v.reshape(n-1, 3)))

    def fun(v):
        x = unpack(v)
        d = x[j]-x[i]
        e = x[b]-x[a]
        sep = np.einsum('ij,ij->i', e[:, 1:], directions)
        return np.r_[d[:, 0]-np.linalg.norm(d[:, 1:], axis=1)-margin,
                     sep-e[:, 0]-margin, sep+e[:, 0]-margin]

    def jac(v):
        x = unpack(v)
        d = x[j, 1:]-x[i, 1:]
        length = np.linalg.norm(d, axis=1)
        u = d/np.maximum(length[:, None], 1e-30)
        grads = [np.column_stack((np.ones(len(i)), -u)),
                 np.column_stack((-np.ones(len(a)), directions)),
                 np.column_stack((np.ones(len(a)), directions))]
        ii, jj = np.r_[i, a, a], np.r_[j, b, b]
        g = np.vstack(grads)
        ans = np.zeros((len(g), n, 3))
        k = np.arange(len(g))
        ans[k, jj] += g
        ans[k, ii] -= g
        return ans[:, 1:, :].reshape(len(g), -1)
    return fun, jac, unpack


def project(points, order, cfg):
    r = validate_order(order)
    initial = np.asarray(points, float)
    if initial.shape != (len(r), 3) or not np.isfinite(initial).all():
        raise ValueError('invalid initial reconstruction')
    initial = initial-initial[0]
    out = dict(status='UNRESOLVED', before=check(initial, r))
    try:
        fun, jac, unpack = constraints(initial, r, cfg['margin'])
    except ValueError as e:
        return {**out, 'reason': str(e)}
    v0 = initial[1:].ravel()
    result = minimize(lambda v: .5*np.sum((v-v0)**2), v0,
                      jac=lambda v: v-v0, method='SLSQP',
                      constraints=[dict(type='ineq', fun=fun, jac=jac)],
                      options=dict(ftol=cfg['ftol'], maxiter=cfg['maxiter']))
    x = unpack(result.x)
    shift = float(np.linalg.norm(x-initial)/max(np.linalg.norm(initial), 1e-12))
    minimum = float(np.min(fun(result.x)))
    after = check(x, r)
    passed = (result.success and minimum >= -cfg['feasibility_tolerance'] and
              shift <= cfg['maximum_relative_shift'] and after['passed'])
    return {**out, 'status': 'ACCEPTED' if passed else 'UNRESOLVED',
            'features': x[1:].tolist(), 'after': after, 'relative_shift': shift,
            'minimum_constraint_slack': minimum, 'iterations': int(result.nit),
            'solver_success': bool(result.success), 'solver_message': str(result.message),
            'objective': float(result.fun)}
