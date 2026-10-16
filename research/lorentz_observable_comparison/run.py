"""Freeze-bound, resource-limited comparison and verification runner."""
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
SOURCES = ['contract.json', 'produce.py', 'check.py', 'run.py']


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n')


def freeze_check():
    frozen = json.loads((HERE/'freeze.json').read_text())
    require(frozen['sources'] == {name: digest(HERE/name) for name in SOURCES}, 'code/contract freeze mismatch')
    publication = json.loads((HERE/'publication.json').read_text())
    commit = publication['source_freeze_commit']
    for name in SOURCES+['freeze.json']:
        raw = subprocess.check_output(['git', 'show', commit+':research/lorentz_observable_comparison/'+name], cwd=ROOT)
        require(hashlib.sha256(raw).hexdigest() == digest(HERE/name), 'published freeze mismatch')
    return commit


def child(phase, directory):
    cfg = json.loads((HERE/'contract.json').read_text())['resources']
    resource.setrlimit(resource.RLIMIT_AS, (cfg['memory_bytes'],)*2)
    resource.setrlimit(resource.RLIMIT_CPU, (cfg['phase_seconds'], cfg['phase_seconds']+1))
    if phase == 'produce':
        import produce
        produce.run(directory)
    else:
        import check
        check.run(directory)


def phase(name, directory, log):
    seconds = json.loads((HERE/'contract.json').read_text())['resources']['phase_seconds']
    started = time.perf_counter()
    with log.open('w') as output:
        subprocess.run([sys.executable, '-B', '-O', str(HERE/'run.py'), '--child', name, str(directory)],
                       stdout=output, stderr=subprocess.STDOUT, timeout=seconds, check=True,
                       env={**os.environ, 'PYTHONHASHSEED': '0'})
    return time.perf_counter()-started


def run(directory):
    commit = freeze_check(); require(not directory.exists(), 'fresh output directory required')
    directory.parent.mkdir(parents=True, exist_ok=True)
    producer_log = directory.parent/(directory.name+'-producer.log')
    checker_log = directory.parent/(directory.name+'-checker.log')
    started = datetime.now(timezone.utc).isoformat()
    try:
        first = phase('produce', directory, producer_log)
        second = phase('check', directory, checker_log)
        producer_log.rename(directory/'producer.log'); checker_log.rename(directory/'checker.log')
        files = ['records.jsonl', 'draws.json', 'summary.json', 'timing.json', 'verification.json', 'producer.log', 'checker.log']
        save(directory/'RESULTS.json', {'schema': 'x6.observable-comparison-run/1', 'status': 'PASS_FINITE_COMPARISON',
             'source_freeze_commit': commit, 'freeze_sha256': digest(HERE/'freeze.json'), 'started_utc': started,
             'completed_utc': datetime.now(timezone.utc).isoformat(), 'python': platform.python_version(), 'platform': platform.platform(),
             'seconds': {'producer': first, 'checker': second}, 'files': {f: digest(directory/f) for f in files},
             'scope': 'Finite known corpus and fixed biased sample, not general reconstruction or physical validation.'})
        print((directory/'RESULTS.json').read_text())
    except Exception as exc:
        directory.mkdir(parents=True, exist_ok=True)
        save(directory/'INCONCLUSIVE.json', {'status': 'INCONCLUSIVE', 'started_utc': started, 'error': str(exc)})
        raise


def verify(directory):
    commit = freeze_check(); saved = json.loads((directory/'RESULTS.json').read_text())
    require(saved['status'] == 'PASS_FINITE_COMPARISON', 'run not complete')
    require(saved['source_freeze_commit'] == commit and saved['freeze_sha256'] == digest(HERE/'freeze.json'), 'freeze binding')
    for f, expected in saved['files'].items():
        require(digest(directory/f) == expected, 'artifact hash '+f)
    old = (directory/'verification.json').read_bytes()
    temp_log = directory.parent/(directory.name+'-recheck.log')
    phase('check', directory, temp_log)
    require((directory/'verification.json').read_bytes() == old, 'countercheck report changed')
    temp_log.unlink()
    print(json.dumps({'status': 'PASS_REPRODUCED_FINITE_COMPARISON', 'source_freeze_commit': commit}))


def selftest():
    # Only toy n<=3 inputs; never reads target corpora or challenge seeds.
    import produce
    import check
    toys = [[[0]], [[0, 1], [0, 0]], [[0, 1, 1], [0, 0, 0], [0, 0, 0]], [[0, 1, 1], [0, 0, 1], [0, 0, 0]]]
    for c in toys:
        timing = {k: 0.0 for k in ['H7', 'D', 'M11', 'N1', 'Q1']}
        require(produce.features(c, timing) == check.compute(c), 'toy algorithm mismatch')
        check.invariance(c)
    require(len(check.negative_controls()) == 6, 'toy rejection controls')
    print('PASS_TOY_ONLY_NO_TARGET_COMPARISON')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); options = parser.add_mutually_exclusive_group(required=True)
    options.add_argument('--freeze', action='store_true'); options.add_argument('--selftest', action='store_true')
    options.add_argument('--run', type=Path); options.add_argument('--verify', type=Path); options.add_argument('--child', nargs=2)
    args = parser.parse_args()
    if args.freeze:
        save(HERE/'freeze.json', {'schema': 'x6.observable-comparison-freeze/1', 'created_utc': datetime.now(timezone.utc).isoformat(),
             'status': 'FROZEN_BEFORE_FIRST_TARGET_COMPARISON', 'sources': {name: digest(HERE/name) for name in SOURCES}})
    elif args.selftest:
        selftest()
    elif args.child:
        child(args.child[0], Path(args.child[1]))
    elif args.run:
        run(args.run)
    else:
        verify(args.verify)
