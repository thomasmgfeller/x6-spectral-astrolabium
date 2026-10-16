"""Frozen-source runner. Failed or limited runs remain explicitly inconclusive."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCES = ['research/lorentz_matched_controls/'+name for name in
           ['contract.json', 'common.py', 'analysis.py', 'produce.py', 'check.py', 'matched_tests.py', 'run.py', 'compare.py', 'requirements.txt']] + ['research/lorentz_matching_geometry/'+name for name in ['core.py', 'geometry.py']]


def require(ok, why):
    if not ok:
        raise ValueError(why)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n')


def freeze():
    import matched_tests
    toy = matched_tests.run()
    require(not (HERE/'freeze.json').exists(), 'do not overwrite an existing source freeze')
    save(HERE/'freeze.json', dict(schema='x6.matched-controls-freeze/1',
         created_utc=datetime.now(timezone.utc).isoformat(), status='BEFORE_TARGET_GENERATION',
         sources={p: sha(ROOT/p) for p in SOURCES}, toy_checks=toy))


def source_check(ref):
    cfg = json.loads((HERE/'contract.json').read_text())
    frozen = json.loads((HERE/'freeze.json').read_text())
    require(frozen['sources'] == {p: sha(ROOT/p) for p in SOURCES}, 'changed frozen sources')
    for p in SOURCES+['research/lorentz_matched_controls/freeze.json']:
        raw = subprocess.check_output(['git', 'show', ref+':'+p], cwd=ROOT)
        require(hashlib.sha256(raw).hexdigest() == sha(ROOT/p), 'frozen commit mismatch '+p)
    for p, h in cfg['generators']['source_sha256'].items():
        require(sha(ROOT/p) == h, 'changed historical input '+p)
    return cfg


def run(directory, ref):
    cfg = source_check(ref)
    require(not directory.exists(), 'fresh output directory required')
    directory.mkdir(parents=True)
    started = datetime.now(timezone.utc).isoformat()
    limits = cfg['resources']
    def bound():
        resource.setrlimit(resource.RLIMIT_AS, (limits['memory_bytes'],)*2)
        resource.setrlimit(resource.RLIMIT_CPU, (limits['phase_seconds'], limits['phase_seconds']+1))
    env = {**os.environ, 'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1', 'PYTHONHASHSEED': '0'}
    times = {}
    try:
        phases = [('produce', [str(HERE/'produce.py')]), ('check', [str(HERE/'check.py')])]
        for name, command in phases:
            begin = time.perf_counter()
            with (directory/(name+'.log')).open('w') as log:
                subprocess.run([sys.executable, '-B', '-O', *command, str(directory)],
                               stdout=log, stderr=subprocess.STDOUT, check=True,
                               timeout=limits['phase_seconds'], preexec_fn=bound, env=env)
            times[name] = time.perf_counter()-begin
            print(name+' completed', flush=True)
        import numpy
        save(directory/'RESULTS.json', dict(schema='x6.matched-controls-run/1', status='PASS_BOUNDED_STUDY',
             source_commit=ref, started_utc=started, completed_utc=datetime.now(timezone.utc).isoformat(),
             sources=json.loads((HERE/'freeze.json').read_text())['sources'], phase_seconds=times,
             python=platform.python_version(), numpy=numpy.__version__, platform=platform.platform(),
             network_scope='No computational network calls; OS network isolation separately enforced in CI only.',
             files={p.name: sha(p) for p in sorted(directory.iterdir()) if p.is_file()}))
    except Exception as exc:
        save(directory/'INCONCLUSIVE.json', dict(status='INCONCLUSIVE', started_utc=started, error=str(exc)))
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--freeze', action='store_true')
    group.add_argument('--selftest', action='store_true')
    group.add_argument('--run', type=Path)
    parser.add_argument('--source-ref')
    args = parser.parse_args()
    if args.freeze:
        freeze()
    elif args.selftest:
        import matched_tests
        print(json.dumps(matched_tests.run(), indent=2))
    else:
        require(args.source_ref is not None, '--source-ref required')
        run(args.run, args.source_ref)
