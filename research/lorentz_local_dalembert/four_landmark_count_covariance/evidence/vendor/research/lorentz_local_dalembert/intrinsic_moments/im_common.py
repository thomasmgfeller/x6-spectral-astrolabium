"""Immutable dependencies of the intrinsic landmark calibration trial."""
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
    names=['im_common.py','intrinsic.py','im_controls.py','run_intrinsic.py',
           'im_analysis.py','verify_intrinsic.py','contract.json','PROTOCOL.md']
    return {**inherited.sources(),**{str((HERE/n).relative_to(ROOT)):hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in names}}
