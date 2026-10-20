"""Simulation evaluation only; explicitly outside the inference boundary."""
import numpy as np
from mb_common import contract


def values(delta, spec):
    a, b, c, px, py = [spec[k] for k in ['a','b','c','px','py']]
    t, x, y = np.asarray(delta).T
    root = np.cos(px)*np.cos(py)
    field = np.exp(a*t)*np.cos(b*x+px)*np.cos(c*y+py)
    truth = -(a*a+b*b+c*c)*root
    return field-root, float(truth)


def evaluate(prepared, selected, z, seed, transfer=False):
    if prepared['status'] != 'COMPLETE':
        return dict(status=prepared['status'])
    cfg = contract()
    specs = cfg['training_fields']+(cfg['transfer_fields'] if transfer else [])
    delta = z[selected['support']]-z[selected['root']]
    full = np.asarray(prepared['full_coefficients'])
    fields = []
    for i, spec in enumerate(specs):
        contrast, truth = values(delta, spec)
        clean = full[:,1:]@contrast
        noise = np.random.default_rng(np.random.SeedSequence([seed,702301,i])).normal(
            scale=cfg['field_noise_sigma'], size=len(contrast)+1)
        prior_error = float(np.random.default_rng(np.random.SeedSequence([seed,702302,i])).normal(
            scale=cfg['prior_sigma']))
        fields.append(dict(name=spec['name'], transfer=i>=len(cfg['training_fields']),
                           truth=truth, clean=clean.tolist(), observed=(clean+full@noise).tolist(),
                           prior_error=prior_error))
    return dict(status='COMPLETE', fields=fields)
