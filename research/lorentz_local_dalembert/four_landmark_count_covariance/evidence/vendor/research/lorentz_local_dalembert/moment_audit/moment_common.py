"""Load immutable prior construction; hash the entire computational dependency set."""
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent/'anchor_audit'))
import common as anchor_common
from common import core, encode
import estimator
import experiment
from run_audit import oracle_cap


def config():
    return json.loads((HERE/'contract.json').read_text()), anchor_common.config()[1]


def sources():
    names = ['moment_common.py','moments.py','moment_controls.py','run_moments.py',
             'moment_analysis.py','verify_moments.py','contract.json','PROTOCOL.md']
    return {**anchor_common.sources(), **{
        str((HERE/n).relative_to(ROOT)): hashlib.sha256((HERE/n).read_bytes()).hexdigest()
        for n in names}}
