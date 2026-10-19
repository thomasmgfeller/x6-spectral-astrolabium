"""Prospective feasibility experiment; audit and geometry follow selection."""
import argparse
import gc
import hashlib
import json
import resource
import signal
import subprocess
import time
from pathlib import Path
import numpy as np
import scipy
from jf_common import HERE, ROOT, config, sources, core, estimator, experiment, weighting, encode, digest, PhysicalPoset, shell, relation
from joint import select, audit
from intrinsic import frame, ETA
from jf_controls import check, witness_check, transport


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
                  direct_control=direct, transport_control=transported, coordinate_diagnostic=diagnostic,
                  coordinates_sha256=digest(z), relation_sha256=digest(g.r), marks_sha256=digest(marks),
                  colours_sha256=digest(colours), audit_colours_sha256=digest(audit_colours),
                  seconds=time.monotonic()-start)
    del g
    gc.collect()
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--mode', choices=['development', 'test'], required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing to overwrite evidence')
    c, oc, guards, cfg = config()
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    bound = sources()
    if args.mode == 'test':
        for path, expected in bound.items():
            assert hashlib.sha256(subprocess.check_output(['git', 'show', sha+':'+path], cwd=ROOT)).hexdigest() == expected, 'unfrozen source '+path
    controls = check()
    args.output.mkdir(parents=True)
    execution = dict(mode=args.mode, source_commit=sha, source_sha256=bound, controls=controls,
                     numpy=np.__version__, scipy=scipy.__version__, records=[], status='RUNNING')
    def save():
        (args.output/'execution.json').write_text(json.dumps(execution, indent=2)+'\n')
    save(); start = time.monotonic()
    def timeout(signum, stack):
        raise TimeoutError('fixed wall budget exhausted')
    signal.signal(signal.SIGALRM, timeout); signal.alarm(c['wall_budget_seconds'])
    try:
        for i, rho in enumerate(c['densities']):
            seeds = c['development_seeds'] if args.mode == 'development' else [c['test_seed_base']+100*i+j for j in range(c['test_replicates_per_density'])]
            for j, seed in enumerate(seeds):
                row = run_cloud(rho, seed, c, oc, guards, cfg, do_transport=(rho == c['densities'][0] and j == 0))
                name = f'rho-{rho}-seed-{seed}.json'; data = encode(row)
                (args.output/name).write_text(data)
                execution['records'].append(dict(file=name, sha256=hashlib.sha256(data.encode()).hexdigest()))
                save()
                print(json.dumps(dict(rho=rho, seed=seed, seconds=round(row['seconds'], 2),
                      frames=[s.get('frames') for s in row['selection']['shells']], selected=row['selection']['status'],
                      joint_pass=row['joint_pass'])), flush=True)
                if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024 > c['memory_budget_mib']:
                    raise MemoryError('fixed memory budget exhausted')
        execution['status'] = 'COMPLETE'
    except (TimeoutError, MemoryError) as error:
        execution.update(status='BUDGET_HOLD', reason=str(error))
    except Exception as error:
        execution.update(status='ERROR', reason=repr(error)); raise
    finally:
        signal.alarm(0)
        execution.update(seconds=time.monotonic()-start, peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
        save()
    if execution['status'] != 'COMPLETE':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
