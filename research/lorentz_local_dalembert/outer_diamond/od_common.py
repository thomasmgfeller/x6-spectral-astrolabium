"""Frozen dependencies and configuration for the outer-domain intervention."""
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / 'intrinsic_moments'))
import im_common as inherited
from im_common import core, estimator, experiment, weighting, encode


def config():
    intrinsic, neighborhood = inherited.config()
    return json.loads((HERE / 'contract.json').read_text()), intrinsic, neighborhood


def sources():
    paths = sorted(p for p in HERE.iterdir() if p.suffix == '.py' or p.name in ('PROTOCOL.md', 'contract.json'))
    return {**inherited.sources(), **{str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}


def digest(array):
    return hashlib.sha256(array.tobytes()).hexdigest()
