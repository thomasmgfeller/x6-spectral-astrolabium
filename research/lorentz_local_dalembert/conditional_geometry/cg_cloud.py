"""Frozen search copied from PR69; adds an order-only inference boundary.
Only simulator/evaluation functions receive true coordinates.
"""
import gc, hashlib, time
import numpy as np
from cg_common import *
from run_joint import core, estimator, experiment, weighting, PhysicalPoset, shell, relation, frame, ETA, select, audit, witness_check, transport
from cg_inference import prepare
def run_cloud(rho, seed, c, oc, guards, cfg, do_transport=False):
    start = time.monotonic()
    z, r, marks, bottom, top = experiment.sprinkle(rho, seed)
    ni = len(z); probes = [bottom, top]
    # The old chain builder must retain the labelled top as a successor. In the
    # unit diamond neither endpoint can be an interior event, so ordinary
    # Poset reproduces the previous baseline without counting any probe.
    gi = core.Poset(r, marks)
    baseline = weighting.reweight(gi, estimator.neighborhood(gi, rho, bottom, top, cfg), rho, cfg['coefficient_C'])
    root, chain = baseline['root'], baseline['chain']
    old_scale = baseline['tau_m']
    del gi, r
    colours = np.random.default_rng(seed ^ guards['colour_seed_xor']).integers(0, 2, size=ni, dtype=np.uint8)
    for index, (lo, hi) in enumerate(zip(oc['outer_durations'][:-1], oc['outer_durations'][1:]), 1):
        zz, mm, cc, meta = shell(rho, seed, index, lo, hi, oc)
        z = np.vstack((z, zz)); marks = np.r_[marks, mm]; colours = np.r_[colours, cc]
    if len(z) > c['maximum_points']:
        raise MemoryError('fixed point budget exhausted')
    g = PhysicalPoset(relation(z, c['relation_block_rows']), marks, probes)
    g.probes_for_check = probes
    inner = [i for i in range(ni) if i not in probes]
    old = frame(g, baseline, rho, probes, colours, guards)
    inferred = select(g, root, chain, inner, probes, colours, rho, c, guards, old_scale)
    selection_seal = hashlib.sha256(encode(inferred).encode()).hexdigest()
    # First generation/access of hidden recolouring: no selection retries below.
    audit_colours = np.random.default_rng(np.random.SeedSequence([seed, c['audit_colour_seed_tag']])).integers(0, 2, size=g.size, dtype=np.uint8)
    audited = audit(g, inferred['selected'], audit_colours, rho, guards)
    assert hashlib.sha256(encode(inferred).encode()).hexdigest() == selection_seal
    direct = witness_check(g, inferred['selected'], colours, audit_colours, rho, guards, c)
    transported = transport(g, root, chain, inner, probes, colours, rho, c, guards, old_scale, inferred, seed) if do_transport else None
    # Read the observed order before coordinate-only diagnostics; never infer it
    # from hidden coordinates in the inference path.
    selected = inferred['selected']
    ids = [selected['root']]+selected['support'] if selected is not None else []
    observed_order = g.r[np.ix_(ids, ids)].astype(bool)
    intrinsic = prepare(selected, observed_order, audited['passed'])
    # Coordinate-only diagnostics begin after selection and the immutable audit.
    diagnostic = None
    w = inferred['selected']
    if w is not None:
        dx = z[w['support']]-z[root]
        truth = dx@ETA@dx.T
        features = np.asarray(w['certificate']['features'])
        estimate = features@ETA@features.T
        tau = np.sqrt(np.maximum(0., -np.diag(truth)))
        diagnostic = dict(lorentz_gram_relative_error=float(np.linalg.norm(estimate-truth)/max(np.linalg.norm(truth), 1e-12)),
                          support_proper_times=[float(tau.min()), float(tau.max())],
                          max_abs_coordinate_time=float(np.max(np.abs(dx[:, 0]))),
                          max_coordinate_radius=float(np.max(np.linalg.norm(dx[:, 1:], axis=1))),
                          interpretation='simulation-frame extent; diagnostic only, no operator/metric qualification')
    result = dict(rho=rho, seed=seed, physical_count=len(z)-2, inner_physical_count=ni-2,
                  original_support_status=baseline['status'], original_frame_status=old['status'],
                  original_guard_pass=old['status'] == 'ok' and old['guard']['passed'],
                  original_guard=old.get('guard'), selection=inferred, selection_seal=selection_seal,
                  audit=audited, joint_pass=bool(inferred['selected'] is not None and audited['passed']),
                  observed_order=observed_order, intrinsic=intrinsic,
                  direct_control=direct, transport_control=transported, coordinate_diagnostic=diagnostic,
                  coordinates_sha256=digest(z), relation_sha256=digest(g.r), marks_sha256=digest(marks),
                  colours_sha256=digest(colours), audit_colours_sha256=digest(audit_colours),
                  seconds=time.monotonic()-start)
    del g
    gc.collect()
    return result

