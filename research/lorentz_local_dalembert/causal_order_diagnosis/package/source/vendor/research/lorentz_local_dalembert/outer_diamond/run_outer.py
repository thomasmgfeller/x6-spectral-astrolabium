"""Prospective paired trial; all inferences precede validation-field access."""
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
from od_common import HERE, ROOT, config, sources, digest, core, estimator, experiment, weighting, encode
from od_simulation import shell, relation as make_relation
from od_order import PhysicalPoset, root_counts, coverage
from od_controls import check, transport
from intrinsic import infer, calibrate
from run_intrinsic import field_evaluation
from verify_intrinsic import calibrated_compare


def run_cloud(rho, seed, c, ic, cfg, controls=False):
    tick = time.monotonic()
    z, relation, marks, bottom, top = experiment.sprinkle(rho, seed)
    inner_z = z.copy()
    n_inner = len(z)
    probes = [bottom, top]
    inner_relation_hash = digest(relation)
    g0 = core.Poset(relation, marks)
    del relation
    base = estimator.neighborhood(g0, rho, bottom, top, cfg)
    s = weighting.reweight(g0, base, rho, cfg['coefficient_C'])
    colours = np.random.default_rng(seed ^ ic['colour_seed_xor']).integers(0, 2, size=len(z), dtype=np.uint8)
    original = infer(g0, s, rho, probes, colours, ic)
    g = PhysicalPoset(g0.r, marks, probes)
    del g0
    inner_counts = root_counts(g, s, colours)
    frozen = dict(coordinates=digest(inner_z), marks=digest(marks), colours=digest(colours))
    stages = []
    shells = []
    for index, duration in enumerate(c['outer_durations']):
        start = time.monotonic()
        if index:
            more, new_marks, new_colours, meta = shell(rho, seed, index, c['outer_durations'][index-1], duration, c)
            if len(z) + len(more) > c['maximum_points']:
                raise MemoryError('fixed augmented point budget exceeded')
            z = np.vstack((z, more))
            marks = np.r_[marks, new_marks]
            colours = np.r_[colours, new_colours]
            shells.append(meta)
            r = make_relation(z, c['relation_block_rows'])
            g = PhysicalPoset(r, marks, probes)
            del r
        assert digest(z[:n_inner]) == frozen['coordinates']
        assert digest(marks[:n_inner]) == frozen['marks']
        assert digest(colours[:n_inner]) == frozen['colours']
        assert digest(g.r[:n_inner, :n_inner]) == inner_relation_hash
        assert root_counts(g, s, colours) == inner_counts
        inferred = infer(g, s, rho, probes, colours, ic)
        if index == 0:
            calibrated_compare(json.loads(encode(original)), json.loads(encode(inferred)), ic['calibration_replay_tolerance'])
        diagnostic = coverage(g, s, ic)
        checks = transport(g, s, rho, probes, colours, ic, inferred, seed) if controls and index == 1 else None
        stages.append(dict(duration=duration, physical_count=len(z)-2, inference=inferred,
                           coverage=diagnostic, controls=checks, invariant_inner_pass=True,
                           coordinates_sha256=digest(z), relation_sha256=digest(g.r),
                           marks_sha256=digest(marks), colours_sha256=digest(colours),
                           seconds=time.monotonic()-start))
        del g
        gc.collect()
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024 > c['memory_budget_mib']:
            raise MemoryError('fixed peak RSS budget exceeded')
    # All order-only inferences are complete. Only now use true coordinates/fields.
    oracle = None
    if s['status'] == 'ok':
        a0 = np.asarray(s['weights']) * s['tau_m']**2
        mask = [b in s['temporal'] for b in s['support']]
        oracle = calibrate((inner_z[s['support']]-inner_z[s['root']])/s['tau_m'], a0, mask, ic)
        for stage in stages:
            inferred = stage['inference']
            used = oracle['status'] == 'VERIFIED'
            stencils = {'volume_shell': (s['weights'], False, []),
                        'coordinate_oracle': (np.asarray(oracle['weights'])/s['tau_m']**2 if used else s['weights'], used, [] if used else ['unresolved_calibration'])}
            stencils.update({name: (inferred[name]['weights'], inferred[name]['adopted'], inferred[name]['fallback_reasons'])
                             for name in ('intrinsic_raw', 'intrinsic_guarded')})
            stage['arms'] = {name: dict(status='ok', adopted=adopted, fallback_reasons=reasons, weights=weights,
                                       evaluation=field_evaluation({**s, 'weights': weights}, inner_z, ic))
                             for name, (weights, adopted, reasons) in stencils.items()}
    else:
        for stage in stages:
            stage['arms'] = {name: dict(status=s['status'], adopted=False, fallback_reasons=['unavailable_stencil'],
                                       evaluation=dict(status=s['status'])) for name in ic['methods']}
    keys = ['status', 'root', 'chain', 'n', 'm', 'tau_n', 'tau_m', 'temporal', 'support', 'weights']
    selection = {k: s[k] for k in keys if k in s}
    blocked = inner_counts is not None and any(v['count'] < ic['guard_min_interval'] or min(v['halves']) < ic['guard_min_half_interval'] for v in inner_counts)
    if blocked:
        assert not any(stage['arms']['intrinsic_guarded']['adopted'] for stage in stages)
    return dict(rho=rho, seed=seed, inner_physical_count=n_inner-2, selection=selection,
                probes=probes, root_support_counts=inner_counts, immutable_inner_guard_obstruction=bool(blocked),
                frozen_inner=frozen, shells=shells, coordinate_oracle=oracle, stages=stages,
                seconds=time.monotonic()-tick)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--mode', choices=['development', 'test'], required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    c, ic, cfg = config()
    if a.output.exists():
        raise SystemExit('Refusing to overwrite output')
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    hashes = sources()
    if a.mode == 'test':
        for path, digest_ in hashes.items():
            assert hashlib.sha256(subprocess.check_output(['git', 'show', sha+':'+path], cwd=ROOT)).hexdigest() == digest_, 'unfrozen source '+path
    controls = check()
    a.output.mkdir(parents=True)
    e = dict(mode=a.mode, source_commit=sha, source_sha256=hashes, numpy=np.__version__, scipy=scipy.__version__,
             controls=controls, status='RUNNING', records=[])
    def save():
        (a.output/'execution.json').write_text(json.dumps(e, indent=2)+'\n')
    save()
    start = time.monotonic()
    def timeout(signum, frame):
        raise TimeoutError('fixed wall budget exhausted')
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(c['wall_budget_seconds'])
    try:
        for i, rho in enumerate(c['densities']):
            seeds = c['development_seeds'] if a.mode == 'development' else [c['test_seed_base']+100*i+j for j in range(c['test_replicates_per_density'])]
            for j, seed in enumerate(seeds):
                row = run_cloud(rho, seed, c, ic, cfg, controls=j == 0)
                name = f'rho-{rho}-seed-{seed}.json'
                data = encode(row)
                (a.output/name).write_text(data)
                e['records'].append(dict(file=name, sha256=hashlib.sha256(data.encode()).hexdigest()))
                save()
                print(json.dumps(dict(rho=rho, seed=seed, seconds=round(row['seconds'], 2),
                      stages=[dict(T=s['duration'], frame=s['inference']['frame']['status'],
                                   raw=s['arms']['intrinsic_raw']['adopted'], guarded=s['arms']['intrinsic_guarded']['adopted']) for s in row['stages']],
                      inner_guard_obstruction=row['immutable_inner_guard_obstruction'])), flush=True)
        e['status'] = 'COMPLETE'
    except (TimeoutError, MemoryError) as error:
        e.update(status='BUDGET_HOLD', reason=str(error))
    except Exception as error:
        e.update(status='ERROR', reason=repr(error))
        raise
    finally:
        signal.alarm(0)
        e.update(seconds=time.monotonic()-start, peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
        save()
    if e['status'] != 'COMPLETE':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
