"""Deterministic provenance and exact interval reporting."""
from pathlib import Path
import gzip,hashlib,json,subprocess
from common import ROOT,load,reference
HERE=Path(__file__).resolve().parent
geometry=load('variance_geometry_sampler','research/lorentz_curvature/geometry.py')
def contract():return json.loads((HERE/'contract.json').read_text())
def read(p):
    raw=p.read_bytes();return json.loads(gzip.decompress(raw) if p.suffix=='.gz' else raw)
def dump(p,value):
    raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode();p.write_bytes(gzip.compress(raw,mtime=0) if p.suffix=='.gz' else raw)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sources(ref):
    result={}
    for name in contract()['frozen_paths']:
        p=ROOT/name;raw=p.read_bytes()
        if raw!=subprocess.check_output(['git','show',f'{ref}:{name}'],cwd=ROOT):raise ValueError('source mismatch: '+name)
        result[name]=digest(p)
    return result
def seed(label):return int.from_bytes(hashlib.sha256((contract()['seed_namespace']+'/'+label).encode()).digest()[:16],'big')
def relation_hash(c):
    import numpy as np
    return hashlib.sha256(np.packbits(c.reshape(-1),bitorder='little').tobytes()).hexdigest()
def value(q):return dict(exact=str(q),approximate=float(q))
def interval_record(interval):
    from fractions import Fraction as Q
    if interval is None:return dict(status='MODEL_DOMAIN_INCOMPATIBLE',h=None,q=None,radius=None)
    r=reference.relative_radius(interval)
    return dict(status='QUALIFIED_20PCT' if r<=Q(1,5) else 'ABSTAIN_PRECISION',h=[str(x) for x in interval],
                q=[value(reference.q_bounds(interval[0])[0]),value(reference.q_bounds(interval[1])[1])],radius=value(r))
