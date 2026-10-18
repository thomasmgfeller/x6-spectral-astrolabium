"""Source binding and data serialization for the frozen C2 confidence study."""
import hashlib
import gzip
import importlib.util
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load_dependency(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT/relative)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


geometry = load_dependency('c2_geometry', 'research/lorentz_curvature/geometry.py')
quadrature = load_dependency('c2_quadrature', 'research/lorentz_rss_fixed_n/quadrature.py')


def contract():
    return json.loads((HERE/'contract.json').read_text())


def dump(path, value):
    raw = (json.dumps(value, indent=2, allow_nan=False)+'\n').encode()
    path.write_bytes(gzip.compress(raw, mtime=0) if path.suffix == '.gz' else raw)


def read(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sources(ref):
    result = {}
    for name in contract()['frozen_paths']:
        raw = (ROOT/name).read_bytes()
        historic = subprocess.check_output(['git', 'show', f'{ref}:{name}'], cwd=ROOT)
        if raw != historic:
            raise ValueError('frozen source changed: '+name)
        result[name] = hashlib.sha256(raw).hexdigest()
    return result


def seed(label):
    return int.from_bytes(hashlib.sha256((contract()['seed_namespace']+'/'+label).encode()).digest()[:16], 'big')


def relation_hash(c):
    import numpy as np
    return hashlib.sha256(np.packbits(c.reshape(-1), bitorder='little').tobytes()).hexdigest()


def fraction_record(q):
    return dict(exact=str(q), approximate=float(q))


def interval_record(interval):
    from fractions import Fraction as Q
    from exact import q_bounds, relative_radius
    if interval is None:
        return dict(status='MODEL_DOMAIN_INCOMPATIBLE', h=None, q=None, relative_radius=None,
                    harmonic_center=None)
    l, u = q_bounds(interval[0])[0], q_bounds(interval[1])[1]
    rad = relative_radius(interval)
    return dict(status='QUALIFIED_20PCT' if rad <= Q(1, 5) else 'ABSTAIN_PRECISION',
                h=[str(x) for x in interval], q=[fraction_record(x) for x in (l, u)],
                relative_radius=fraction_record(rad),
                harmonic_center=fraction_record(2*l*u/(l+u)) if l > 0 else None)
