"""Frozen dependency loading and JSON helpers for the isolated audit."""
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LEGACY = HERE.parent / 'phase12'
sys.path.insert(0, str(LEGACY))
import core

def config():
    return json.loads((HERE/'contract.json').read_text()), json.loads((LEGACY/'contract.json').read_text())

def plain(value):
    if isinstance(value, np.ndarray): return value.tolist()
    if isinstance(value, np.generic): return value.item()
    raise TypeError(type(value).__name__)

def encode(value):
    return json.dumps(value, default=plain, allow_nan=False, separators=(',', ':'))+'\n'

def sources():
    names = ['common.py','estimator.py','run_audit.py','audit_analysis.py','controls.py','verify_audit.py','contract.json','PROTOCOL.md']
    paths = [HERE/n for n in names] + [LEGACY/n for n in ['core.py','experiment.py','analyze.py','tests.py','longest.cpp','contract.json']]
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
