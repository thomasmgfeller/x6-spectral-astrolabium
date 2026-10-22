"""Fixed inputs and evidence serialization. SPDX-License-Identifier: Apache-2.0"""
import gzip,hashlib,json,sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
PRIOR=HERE.parent/'eligibility_before_cap'
sys.path.insert(0,str(HERE.parent/'stability_followup'))
from models import Alternative,estimate
from fit import input_mask
from inference import four,ETA

def encode(x):
    def native(v):
        if isinstance(v,np.ndarray):return v.tolist()
        if isinstance(v,np.generic):return v.item()
        raise TypeError(type(v).__name__)
    return json.dumps(x,default=native,allow_nan=False,separators=(',',':')).encode()

def save(path,x):
    path.parent.mkdir(parents=True,exist_ok=True);raw=encode(x)
    if path.suffix=='.gz':raw=gzip.compress(raw,mtime=0)
    with path.open('xb') as f:f.write(raw)
    return hashlib.sha256(raw).hexdigest()

def read(path):
    raw=path.read_bytes();return json.loads(gzip.decompress(raw) if path.suffix=='.gz' else raw)

def frozen():
    for name,h in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
