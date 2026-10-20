"""Fresh source-bound clouds; inference is sealed before field evaluation."""
import argparse
import hashlib
import json
import resource
import signal
import subprocess
import time
import numpy as np
import scipy
from cg_common import HERE, ROOT, config, contract, sources, encode, digest
from cg_cloud import run_cloud
from run_calibration import coordinates_only


def evaluate(intrinsic, selected, z, seed):
    if intrinsic['status'] != 'COMPLETE':
        return dict(status=intrinsic['status'])
    c = contract()
    w = np.array(intrinsic['weights'])
    assert hashlib.sha256(w.tobytes()).hexdigest() == intrinsic['weights_seal']
    delta = z[selected['support']]-z[selected['root']]
    field = np.exp(delta[:, 0]/2)*np.cos(delta[:, 1]/2)*np.cos(delta[:, 2]/2)
    noise = np.random.default_rng(np.random.SeedSequence([seed, 823731])).normal(
        scale=c['field_noise_sigma'], size=len(field)+1)
    clean = w@(field-1)/intrinsic['scale']**2
    observed = clean+w@(noise[1:]-noise[0])/intrinsic['scale']**2
    return dict(status='COMPLETE', truth=-.75, clean=clean, observed=observed)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--shard', type=int, choices=[0, 1], required=True)
    args = p.parse_args()
    c = contract()
    destination = HERE/f'test-{args.shard}'
    if destination.exists():
        raise SystemExit('Refusing to overwrite evidence')
    bound = sources()
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    for path, expected in bound.items():
        assert hashlib.sha256(subprocess.check_output(['git', 'show', sha+':'+path], cwd=ROOT)).hexdigest() == expected, path
    frozen = (HERE/'frozen_calibration.json').read_bytes()
    assert json.loads(frozen)['status'] == 'FROZEN'
    assert subprocess.check_output(['git', 'show', sha+':'+str((HERE/'frozen_calibration.json').relative_to(ROOT))], cwd=ROOT) == frozen
    jf, oc, guards, cfg = config()
    destination.mkdir()
    run = dict(status='RUNNING', source_commit=sha, source_sha256=bound,
               calibration_sha256=hashlib.sha256(frozen).hexdigest(), shard=args.shard,
               numpy=np.__version__, scipy=scipy.__version__, records=[])
    def save():
        (destination/'execution.json').write_text(json.dumps(run, indent=2)+'\n')
    start = time.monotonic()
    save()
    def timeout(*args):
        raise TimeoutError('declared wall budget')
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(c['wall_budget_seconds_per_shard'])
    try:
        lo, hi = c['test_seeds']
        for seed in list(range(lo, hi+1))[args.shard::2]:
            row = run_cloud(c['rho'], seed, jf, oc, guards, cfg)
            z = coordinates_only(c['rho'], seed, oc)
            assert digest(z) == row['coordinates_sha256']
            row['evaluation'] = evaluate(row['intrinsic'], row['selection']['selected'], z, seed)
            if row['evaluation']['status'] == 'COMPLETE':
                from cg_relations import check
                w = row['selection']['selected']
                ids = [w['root']]+w['support']
                assert check(z[ids], row['observed_order'])['passed']
            name = f'seed-{seed}.json'
            raw = encode(row)
            (destination/name).write_text(raw)
            run['records'].append(dict(file=name, sha256=hashlib.sha256(raw.encode()).hexdigest()))
            save()
            print(json.dumps(dict(seed=seed, status=row['evaluation']['status'], seconds=row['seconds'])), flush=True)
            if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024 > c['memory_budget_mib_per_shard']:
                raise MemoryError('declared memory budget')
        run['status'] = 'COMPLETE'
    except Exception as e:
        run.update(status='HOLD', reason=repr(e))
        raise
    finally:
        signal.alarm(0)
        run.update(seconds=time.monotonic()-start, peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
        save()


if __name__ == '__main__':
    main()
