"""Source-bound, separate successor experiment; previous sources stay frozen."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(BASE/'conditional_geometry'))
from cg_common import config, encode, digest, sources as inherited_sources


def contract():
    return json.loads((HERE/'contract.json').read_text())


def sources():
    names = ['mb_common.py', 'mb_model.py', 'mb_fields.py', 'mb_calibrate.py',
             'mb_run.py', 'mb_analyze.py', 'test_controls.py', 'verify.py',
             'contract.json', 'PROTOCOL.md']
    return {**inherited_sources(), **{str((HERE/n).relative_to(ROOT)):
            hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in names}}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n')
