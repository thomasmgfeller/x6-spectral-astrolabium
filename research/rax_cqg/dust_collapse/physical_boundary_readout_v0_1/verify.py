#!/usr/bin/env python3
"""Hash validation and isolated scientific replay. No network or paid services."""
from pathlib import Path
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
JOBS = [
    ('checks/canonical_scalar/check.py', 'checks/canonical_scalar/results.json'),
    ('checks/canonical_scalar/gaussian_outputs.py', 'checks/canonical_scalar/gaussian_outputs.json'),
    ('checks/history_measure/check.py', 'checks/history_measure/results.json'),
    ('checks/independent_audit/check.py', 'checks/independent_audit/results.json'),
    ('checks/independent_audit/contract_checks.py', 'checks/independent_audit/contract_results.json'),
    ('checks/independent_audit/reduced_kernel.py', 'checks/independent_audit/reduced_kernel_results.json'),
    ('checks/variational_boundary/check.py', 'checks/variational_boundary/results.json'),
    ('checks/ward_clock/check.py', 'checks/ward_clock/results.json'),
    ('checks/independent_audit/coherent_gaussian.py', 'checks/independent_audit/coherent_gaussian_results.json'),
    ('checks/local_detector/check.py', 'checks/local_detector/results.json'),
]
DECIMAL = re.compile(r'[+-]?(?:\d+\.\d*|\d*\.\d+)(?:[eE][+-]?\d+)?\Z')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(root):
    return {str(p.relative_to(root)): digest(p) for p in root.rglob('*') if p.is_file()
            and p.name != 'MANIFEST.json' and '__pycache__' not in p.parts and p.suffix != '.pyc'}

def dependencies(obj, root):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'dependencies':
                for name, h in v.items():
                    if digest(root / name) != h:
                        raise AssertionError(f'Stale dependency hash: {name}')
            else:
                dependencies(v, root)
    elif isinstance(obj, list):
        for v in obj:
            dependencies(v, root)

def same(a, b, path='root'):
    if isinstance(a, dict):
        if not isinstance(b, dict) or a.keys() != b.keys():
            raise AssertionError(f'Keys differ: {path}')
        for k in a:
            # Volatile wall time; hashes independently checked against actual dependency files.
            if k not in {'runtime_seconds', 'dependencies'}:
                same(a[k], b[k], path + '.' + k)
    elif isinstance(a, list):
        if not isinstance(b, list) or len(a) != len(b):
            raise AssertionError(f'List differs: {path}')
        for i, (x, y) in enumerate(zip(a, b)):
            same(x, y, f'{path}[{i}]')
    elif isinstance(a, bool) or a is None or isinstance(a, int):
        if type(a) != type(b) or a != b:
            raise AssertionError(f'Exact value differs: {path}: {a!r} vs {b!r}')
    elif isinstance(a, float) or (isinstance(a, str) and DECIMAL.fullmatch(a)):
        try:
            x, y = float(a), float(b)
        except (TypeError, ValueError):
            raise AssertionError(f'Non-numeric value: {path}') from None
        if not math.isfinite(x) or not math.isfinite(y) or not math.isclose(x, y, rel_tol=5e-12, abs_tol=5e-12):
            raise AssertionError(f'Numerical value differs: {path}: {a!r} vs {b!r}')
    elif a != b:
        raise AssertionError(f'Exact value differs: {path}: {a!r} vs {b!r}')

def main():
    if sys.flags.optimize:
        raise SystemExit('Do not disable scientific assertions with python -O.')
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    actual = inventory(ROOT)
    if actual != manifest['files']:
        bad = sorted(k for k in set(actual) | set(manifest['files']) if actual.get(k) != manifest['files'].get(k))
        raise AssertionError('Manifest differs: ' + ', '.join(bad))
    provenance = json.loads((ROOT / 'sources/provenance.json').read_text())
    for source in provenance['sources']:
        if digest(ROOT / source['path']) != source['sha256']:
            raise AssertionError('Parent source hash mismatch: ' + source['path'])
    expected = {}
    for _, name in JOBS:
        expected[name] = json.loads((ROOT / name).read_text())
        dependencies(expected[name], ROOT)
    with tempfile.TemporaryDirectory(prefix='cst-boundary-replay-') as tmp:
        work = Path(tmp) / 'package'
        shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
        for script, output in JOBS:
            (work / output).unlink()
            proc = subprocess.run([sys.executable, '-B', script], cwd=work, env=env,
                                  text=True, capture_output=True, timeout=300)
            if proc.returncode:
                raise RuntimeError(f'{script}\n{proc.stdout}\n{proc.stderr}')
            result = json.loads((work / output).read_text())
            dependencies(result, work)
            same(expected[output], result, output)
            print('PASS ' + script, flush=True)
    print(json.dumps({'status': 'PASS', 'manifest_files': len(actual),
                      'replayed_programs': len(JOBS), 'compared_outputs': len(JOBS),
                      'parent_commit': provenance['parent_commit'],
                      'relative_tolerance': 5e-12, 'absolute_tolerance': 5e-12,
                      'full_physical_geometrodynamics_derived': False}, indent=2))

if __name__ == '__main__':
    main()
