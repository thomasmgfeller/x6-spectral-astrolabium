"""Explicit dependency and source binding for the conditional-geometry pilot."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(BASE/'feynman_combiner'))
sys.path.insert(0, str(BASE/'joint_feasibility'))
sys.path.insert(0, str(BASE/'moment_feasibility'))
from jf_common import config, sources as inherited_sources, encode, digest


def contract():
    return json.loads((HERE/'contract.json').read_text())


def sources():
    paths = [HERE/p for p in ['cg_common.py', 'cg_cloud.py', 'cg_inference.py',
             'cg_relations.py', 'cg_run.py', 'cg_calibrate.py', 'cg_analyze.py',
             'test_controls.py', 'contract.json', 'PROTOCOL.md']]
    paths += [BASE/'feynman_combiner'/p for p in
              ['run_calibration.py', 'variance_weights.py', 'fusion.py', 'analyze_calibration.py']]
    paths += [BASE/'moment_feasibility'/p for p in ['feasibility.py', 'contract.json']]
    return {**inherited_sources(), **{str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
