"""Pinned dependencies and deterministic evidence serialization.
SPDX-License-Identifier: Apache-2.0
"""
import gzip
import hashlib
import json
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'four_landmark_count_covariance/evidence'
sys.path.insert(0, str(SOURCE))

def encode(value):
    def native(x):
        if isinstance(x, np.ndarray): return x.tolist()
        if isinstance(x, np.generic): return x.item()
        raise TypeError(type(x).__name__)
    return json.dumps(value, default=native, allow_nan=False, separators=(',', ':')).encode()

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = encode(value)
    if path.suffix == '.gz': raw = gzip.compress(raw, mtime=0)
    with path.open('xb') as f: f.write(raw)
    return hashlib.sha256(raw).hexdigest()

def frozen():
    f = json.loads((HERE/'freeze.json').read_text())
    for name, digest in f['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest() == digest, name

def read(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)
