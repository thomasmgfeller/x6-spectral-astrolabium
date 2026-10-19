"""Source-bound dependencies for the joint feasibility pilot."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / 'outer_diamond'))
import od_common as inherited
from od_common import core, estimator, experiment, weighting, encode, digest
from od_order import PhysicalPoset
from od_simulation import shell, relation


def config():
    outer, intrinsic, neighborhood = inherited.config()
    return json.loads((HERE/'contract.json').read_text()), outer, intrinsic, neighborhood


def sources():
    paths = sorted(p for p in HERE.iterdir() if p.suffix == '.py' or p.name in ('contract.json', 'PROTOCOL.md'))
    return {**inherited.sources(), **{str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
