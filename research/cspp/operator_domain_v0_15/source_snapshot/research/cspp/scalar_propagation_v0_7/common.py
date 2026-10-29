"""Shared paths and explicit integrity helpers; predecessor sources stay unchanged."""
import hashlib,importlib.util,json,sys
from pathlib import Path
import numpy as np
from flint import arb,acb,ctx
HERE=Path(__file__).resolve().parent
PILOT=HERE.parent/'scalar_pilot_v0_1'
sys.path.append(str(HERE.parent/'certified_budget_v0_3'))
import balls
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
old=load('v07_legacy_scalar',PILOT/'scalar.py')
def check(ok,label):
    if not bool(ok):raise RuntimeError('HOLD: '+label)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def digest(a):return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
def write(path,obj):Path(path).write_text(json.dumps(obj,ensure_ascii=False,allow_nan=False,indent=2)+'\n')
def protocol():return json.loads((HERE/'PROTOCOL.json').read_text())
def upper(x):return float(arb(x).upper())
def cb(z):return acb(complex(z))
def rms_ball(values):return (sum(z.abs_lower()**2 for z in values)/len(values)).sqrt(),(sum(z.abs_upper()**2 for z in values)/len(values)).sqrt()
