"""Immutable dependencies and source manifest for the shell-weight experiment."""
import hashlib
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE.parent/'moment_audit'))
import moment_common as inherited
from moment_common import core,estimator,experiment,encode
from moments import diagnose
from controls import compare


def config():
    return json.loads((HERE/'contract.json').read_text()),inherited.config()[1]


def sources():
    names=['volume_common.py','weighting.py','volume_controls.py','run_volume.py',
           'volume_analysis.py','verify_volume.py','contract.json','PROTOCOL.md']
    return {**inherited.sources(),**{str((HERE/n).relative_to(ROOT)):hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in names}}
