"""Publication binding and deterministic input provenance."""
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
from fractions import Fraction as Q
from core import reference

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('kl_geometry_sampler', ROOT/'research/lorentz_curvature/geometry.py')
geometry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(geometry)


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
    out = {}
    for name in contract()['frozen_paths']:
        raw = (ROOT/name).read_bytes()
        if raw != subprocess.check_output(['git', 'show', f'{ref}:{name}'], cwd=ROOT):
            raise ValueError('frozen source mismatch: '+name)
        out[name] = hashlib.sha256(raw).hexdigest()
    return out


def seed(label):
    return int.from_bytes(hashlib.sha256((contract()['seed_namespace']+'/'+label).encode()).digest()[:16], 'big')


def relation_hash(c):
    import numpy as np
    return hashlib.sha256(np.packbits(c.reshape(-1), bitorder='little').tobytes()).hexdigest()


def fraction_record(value):
    return dict(exact=str(value), approximate=float(value))


def interval_record(interval):
    if interval is None:
        return dict(status='MODEL_DOMAIN_INCOMPATIBLE', h=None, q=None, radius=None, center=None)
    lower, upper = reference.q_bounds(interval[0])[0], reference.q_bounds(interval[1])[1]
    radius = reference.relative_radius(interval)
    return dict(status='QUALIFIED_20PCT' if radius <= Q(1, 5) else 'ABSTAIN_PRECISION',
        h=[str(v) for v in interval], q=[fraction_record(v) for v in (lower, upper)],
        radius=fraction_record(radius), center=fraction_record(2*lower*upper/(lower+upper)) if lower > 0 else None)
