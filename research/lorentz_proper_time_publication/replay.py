"""Replay published evidence without modifying the original sources or results."""
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import numpy as np
from planning import planning

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def compare(left, right, path='root'):
    if isinstance(left, dict):
        require(isinstance(right, dict) and left.keys() == right.keys(), path+' keys')
        for key in left:
            compare(left[key], right[key], path+'/'+key)
    elif isinstance(left, list):
        require(isinstance(right, list) and len(left) == len(right), path+' length')
        for i, (a, b) in enumerate(zip(left, right)):
            compare(a, b, path+'/'+str(i))
    elif isinstance(left, float):
        require(isinstance(right, (float, int)) and math.isclose(left, right, rel_tol=1e-11, abs_tol=1e-13), path+' value')
    else:
        require(left == right, path+' value')


def read(path):
    return json.loads(path.read_text())


def arrays_equal(a, b):
    with np.load(a, allow_pickle=False) as first, np.load(b, allow_pickle=False) as second:
        require(set(first.files) == set(second.files), 'count archive keys')
        for key in first.files:
            require(np.array_equal(first[key], second[key]), 'count archive: '+key)


def check_repair():
    package = RESEARCH/'lorentz_proper_time_sequential'
    original = package/'results-incomplete-serialization'
    old = read(original/'freeze.json')['sha256']
    new = read(package/'results/freeze.json')['sha256']
    require(old.keys() == new.keys(), 'repair freeze keys')
    changed = [key for key in old if old[key] != new[key]]
    require(changed == ['run.py'], 'repair source scope')
    before = (original/'run_original.py').read_bytes()
    require(hashlib.sha256(before).hexdigest() == old['run.py'], 'original run hash')
    after = (package/'run.py').read_bytes()
    old_expr = b'"rejections": sum(p <= contract["alpha_chain"] for p in pvals)'
    new_expr = b'"rejections": int(sum(p <= contract["alpha_chain"] for p in pvals))'
    require(before.count(old_expr) == 1 and before.replace(old_expr, new_expr) == after,
            'repair must be exactly the documented JSON scalar conversion')
    arrays_equal(original/'batch_counts.npz', package/'results/batch_counts.npz')


def run():
    check_repair()
    compare(read(HERE/'planning.json'), planning(), 'fixed-sample planning')
    reports = []
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    with tempfile.TemporaryDirectory(prefix='x6-proper-time-replay-') as scratch:
        scratch = Path(scratch)
        for name in ['lorentz_proper_time_domain', 'lorentz_proper_time_sequential']:
            package = RESEARCH/name
            published = package/'results'
            archived = scratch/(name+'-archive')
            fresh = scratch/(name+'-replay')
            shutil.copytree(published, archived)
            subprocess.run([sys.executable, '-B', str(package/'verify.py'), str(archived)], check=True, env=env)
            compare(read(published/'verification.json'), read(archived/'verification.json'), name+'/verification')
            subprocess.run([sys.executable, '-B', str(package/'run.py'), str(fresh)], check=True, env=env)
            subprocess.run([sys.executable, '-B', str(package/'verify.py'), str(fresh)], check=True, env=env)
            a, b = read(published/'summary.json'), read(fresh/'summary.json')
            # Only execution metadata is excluded; no scientific field is dropped.
            for key in ['elapsed_seconds', 'seconds', 'python', 'numpy', 'scipy']:
                a.pop(key, None); b.pop(key, None)
            compare(a, b, name+'/summary')
            if name.endswith('_domain'):
                compare(read(published/'counts.json'), read(fresh/'counts.json'), name+'/counts')
            else:
                arrays_equal(published/'batch_counts.npz', fresh/'batch_counts.npz')
                compare(read(published/'integration_demo.json'), read(fresh/'integration_demo.json'), name+'/geometry')
            reports.append(name)
    print(json.dumps(dict(status='PASS_PUBLISHED_EVIDENCE_AND_REPLAY', packages=reports,
                          repaired_run_history='VERIFIED', fixed_sample_planning='VERIFIED',
                          external_replication=False), indent=2))


if __name__ == '__main__':
    run()
