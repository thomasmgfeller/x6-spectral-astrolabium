"""Inference sees only reconstructed geometry and frozen calibration, never truth.

It outputs weights before any field access. Conditional noise is recomputed for
all actual weights, not inherited from the uncorrected operator.
"""
import numpy as np
from mb_common import contract
from feasibility import design, TARGET

ARMS = ['original', 'metadata', 'projected', 'projected_metadata',
        'constant_ablation', 'projected_constant_ablation']


def basis(intrinsic, arm):
    x = np.asarray(intrinsic['original_features'] if arm == 0 else
                   intrinsic['projection']['features'], float)
    a = np.asarray(intrinsic['weights'][arm], float)
    d = design(x)
    h = np.eye(len(a))+np.ones((len(a), len(a)))
    gain = float(a@h@a)
    _, singular, vt = np.linalg.svd(d, full_matrices=True)
    assert singular[-1] > 1e-12*singular[0]
    null = vt[len(d):].T
    t, xx, yy = x.T
    raw = np.column_stack((t*(xx*xx+yy*yy), (-t*t+xx*xx+yy*yy)**2))
    q0 = null@(null.T@raw)
    gram = q0.T@h@q0
    ev, u = np.linalg.eigh(gram)
    available = bool(ev[0] > 1e-12*max(ev[-1], 1e-30))
    q = q0@(u@np.diag(1/np.sqrt(ev))@u.T) if available else np.zeros_like(q0)
    if available:
        np.testing.assert_allclose(d@q, 0, atol=1e-8)
        np.testing.assert_allclose(q.T@h@q, np.eye(2), atol=1e-8)
    v = contract()['field_noise_sigma']**2*gain/intrinsic['scale']**4
    m = np.log([v, singular[0]/singular[-1], len(a)])
    return dict(a=a, q=q, gain=gain, metadata=m, design=d,
                available=available, scale=intrinsic['scale'])


def fit(samples, ridge, use_metadata):
    """Each sample is one cloud, containing all six field contrasts/errors."""
    meta = np.array([s['basis']['metadata'] for s in samples])
    center, spread = meta.mean(axis=0), meta.std(axis=0)
    spread = np.where(spread > 1e-12, spread, 1.)
    matrices, targets = [], []
    for s in samples:
        b = s['basis']
        m = np.r_[1., (b['metadata']-center)/spread] if use_metadata else np.ones(1)
        response = s['contrasts']@b['q']*np.sqrt(b['gain'])/b['scale']**2
        matrices.append(np.einsum('fj,k->fjk', response, m).reshape(len(response), -1))
        targets.append(s['errors'])
    x, y = np.vstack(matrices), np.concatenate(targets)
    # Standardize regression columns using training data only; zero columns are inert.
    scales = np.sqrt(np.mean(x*x, axis=0))
    scales = np.where(scales > 1e-12, scales, 1.)
    xs = x/scales
    beta = np.linalg.solve(xs.T@xs/len(y)+ridge*np.eye(x.shape[1]), xs.T@y/len(y))/scales
    return dict(use_metadata=use_metadata, ridge=ridge, center=center.tolist(),
                spread=spread.tolist(), minimum=meta.min(axis=0).tolist(),
                maximum=meta.max(axis=0).tolist(), beta=beta.reshape(2, -1).tolist())


def corrected(b, model):
    m = b['metadata']
    ood = bool(np.any(m < np.array(model['minimum'])-1e-10) or
               np.any(m > np.array(model['maximum'])+1e-10))
    if ood or not b['available']:
        return b['a'].copy(), dict(ood=ood, null_available=b['available'], clipped=False,
                                  alpha=[0., 0.], noise_ratio=1.)
    features = np.r_[1., (m-model['center'])/model['spread']] if model['use_metadata'] else np.ones(1)
    alpha = np.array(model['beta'])@features
    norm = float(np.linalg.norm(alpha))
    cap = np.sqrt(contract()['maximum_noise_variance_ratio']-1)
    clipped = bool(norm > cap)
    if clipped:
        alpha *= cap/norm
    a = b['a']-np.sqrt(b['gain'])*(b['q']@alpha)
    np.testing.assert_allclose(b['design']@a, TARGET, atol=2e-6, rtol=0)
    gain = float(a@a+a.sum()**2)
    ratio = gain/b['gain']
    assert ratio <= contract()['maximum_noise_variance_ratio']+1e-7
    return a, dict(ood=ood, null_available=True, clipped=clipped,
                   alpha=alpha.tolist(), noise_ratio=ratio)


def prepare(intrinsic, models):
    if intrinsic['status'] != 'COMPLETE':
        return dict(status=intrinsic['status'])
    b = [basis(intrinsic, i) for i in [0, 1]]
    weights, diagnostics = {}, {}
    for arm, names in enumerate([['original','metadata','constant_ablation'],
                                 ['projected','projected_metadata','projected_constant_ablation']]):
        weights[names[0]] = b[arm]['a']
        for name in names[1:]:
            weights[name], diagnostics[name] = corrected(b[arm], models[name])
    a = np.array([weights[name] for name in ARMS])
    full = np.column_stack((-a.sum(axis=1), a))/intrinsic['scale']**2
    noise = contract()['field_noise_sigma']**2*(full@full.T)
    return dict(status='COMPLETE', arms=ARMS, weights=a.tolist(),
                full_coefficients=full.tolist(), conditional_field_covariance=noise.tolist(),
                metadata=[v['metadata'].tolist() for v in b], diagnostics=diagnostics,
                scale=intrinsic['scale'])
