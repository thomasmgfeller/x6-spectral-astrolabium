"""Immutable dependencies and source manifest for the common-axis trial."""
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
    names=['axis_common.py','selection.py','assembly.py','axis_controls.py',
           'run_axis.py','axis_analysis.py','verify_axis.py','contract.json','PROTOCOL.md']
    return {**inherited.sources(),**{str((HERE/n).relative_to(ROOT)):hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in names}}
