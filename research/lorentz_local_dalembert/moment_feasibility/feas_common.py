"""Immutable dependencies for the coordinate-assisted feasibility audit."""
import hashlib
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE.parent/'volume_shell'))
import volume_common as inherited
from volume_common import core,estimator,experiment,encode,compare
from run_volume import evaluate
import weighting

def config():
    return json.loads((HERE/'contract.json').read_text()),inherited.config()[1]

def sources():
    names=['feas_common.py','feasibility.py','feas_controls.py','run_feasibility.py',
           'feas_analysis.py','verify_feasibility.py','contract.json','PROTOCOL.md']
    return {**inherited.sources(),**{str((HERE/n).relative_to(ROOT)):hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in names}}
