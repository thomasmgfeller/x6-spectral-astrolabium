"""Explicit predecessor imports and outward serialization for the detector study."""
import gzip
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from flint import arb, acb, ctx

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
V07 = HERE.parent / 'scalar_propagation_v0_7'
sys.path.insert(0, str(V07))
from common import check, sha, digest, write, old, load
import geometry
import initial_data
import propagation


def plan():
    return json.loads((HERE / 'PROTOCOL.json').read_text())


def pack(z):
    z = acb(z)
    check(z.is_finite(), 'finite detector enclosure')
    out = [z.real.str(45, more=True), z.imag.str(45, more=True)]
    check(arb(out[0]).contains(z.real) and arb(out[1]).contains(z.imag),
          'outward decimal serialization')
    return out


def unpack(z):
    return acb(arb(z[0]), arb(z[1]))


def gzwrite(path, data):
    with open(path, 'wb') as raw:
        with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as f:
            f.write(json.dumps(data, ensure_ascii=False, allow_nan=False,
                               separators=(',', ':')).encode())


def gzread(path):
    with gzip.open(path, 'rt') as f:
        return json.load(f)


def freeze_check():
    doc = json.loads((HERE / 'FREEZE.json').read_text())
    for name, expected in doc['files'].items():
        check(sha(HERE / name) == expected, 'frozen source ' + name)
    return doc


def matrix_hash(rows):
    return hashlib.sha256(json.dumps(rows, separators=(',', ':')).encode()).hexdigest()
