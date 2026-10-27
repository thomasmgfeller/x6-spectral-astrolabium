"""Replay v0.3 in a temporary copy without changing archived evidence."""
from pathlib import Path
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'joint_region_v0_3'


def compare(a, b, path='root'):
    if isinstance(a, dict):
        assert a.keys() == b.keys(), path
        for key in a:
            if key not in ('runtime_seconds', 'environment'):
                compare(a[key], b[key], path + '.' + key)
    elif isinstance(a, list):
        assert len(a) == len(b), path
        for i, (x, y) in enumerate(zip(a, b)):
            compare(x, y, f'{path}[{i}]')
    elif isinstance(a, float):
        assert math.isclose(a, b, rel_tol=1e-8, abs_tol=1e-11), (path, a, b)
    else:
        assert a == b, (path, a, b)


def main():
    for line in (SOURCE / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        assert hashlib.sha256((SOURCE / name).read_bytes()).hexdigest() == digest, name
    with tempfile.TemporaryDirectory(prefix='eigenzeit-joint-replay-') as tmp:
        base = Path(tmp)
        for name in ('joint_region_v0_3', 'poisson_v0_2'):
            shutil.copytree(ROOT / name, base / name, ignore=shutil.ignore_patterns('__pycache__'))
        work = base / 'joint_region_v0_3'
        env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
        for script in ('run.py', 'audit.py'):
            subprocess.run([sys.executable, '-B', str(work / script)], check=True, env=env)
        for name in ('RESULTS.json', 'CERTIFICATES.json', 'AUDIT.json'):
            compare(json.loads((SOURCE / name).read_text()), json.loads((work / name).read_text()), name)
        old = np.load(SOURCE / 'fresh_counts.npz')
        new = np.load(work / 'fresh_counts.npz')
        assert old.files == new.files
        assert np.array_equal(old['cells'], new['cells'])
        np.testing.assert_allclose(old['metrics'], new['metrics'], rtol=1e-8, atol=1e-11, equal_nan=True)
    print('PASS: all 5120 observations, 1910 certificates and HOLD gate reproduced; archived evidence unchanged.')


if __name__ == '__main__':
    main()
