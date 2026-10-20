"""Inference boundary: reconstructed features, counts and observed order only.
No simulator, clean field, noise sample or test truth is available here.
"""
import hashlib
import numpy as np
from cg_common import contract
from feasibility import design
from variance_weights import minimum_variance
from cg_relations import project, check


def prepare(selected, order, guarded):
    if selected is None or not guarded:
        return dict(status='NO_GUARDED_SUPPORT')
    c = contract()
    s = selected['scale']
    x = np.asarray(selected['certificate']['features'], float)/s
    future = selected['support'].index(selected['temporal'][1])
    if x[future, 0] < 0:
        x[:, 0] *= -1
    p = project(np.vstack((np.zeros(3), x)), order, c['projection'])
    out = dict(status='UNRESOLVED', before=check(np.vstack((np.zeros(3), x)), order),
               original_features=x.tolist(), projection=p, scale=s)
    if p['status'] != 'ACCEPTED':
        return out
    repaired = np.array(p['features'])
    weights = []
    certificates = []
    for features in [x, repaired]:
        d = design(features)
        condition = float(np.linalg.cond(d))
        if not np.isfinite(condition) or condition > c['maximum_design_condition']:
            return {**out, 'reason': 'design condition', 'condition': condition}
        try:
            q = minimum_variance(d)
        except np.linalg.LinAlgError:
            return {**out, 'reason': 'singular moment problem'}
        if q['status'] != 'VERIFIED':
            return {**out, 'reason': 'uncertified weights'}
        weights.append(q['weights'])
        certificates.append(q)
    w = np.asarray(weights)
    full = np.column_stack((-w.sum(axis=1), w))/(s*s)
    # The two arms use exactly the same event noise, including the same root.
    noise_cov = c['field_noise_sigma']**2*(full@full.T)
    return {**out, 'status': 'COMPLETE', 'weights': weights, 'certificates': certificates,
            'weights_seal': hashlib.sha256(w.tobytes()).hexdigest(),
            'conditional_field_covariance': noise_cov.tolist()}
