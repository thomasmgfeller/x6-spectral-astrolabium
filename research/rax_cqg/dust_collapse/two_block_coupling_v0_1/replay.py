#!/usr/bin/env python3
from pathlib import Path
import tempfile, subprocess, sys, hashlib, json
root=Path(__file__).resolve().parent
names=('gluing_and_memory.json','frozen_collar_exclusions.json','retuned_stationary_family.json','verification.json')
with tempfile.TemporaryDirectory(prefix='cst-two-block-replay-') as d:
    out=Path(d)/'results'
    subprocess.run([sys.executable,'-B',str(root/'analyze.py'),str(out)],check=True,capture_output=True)
    checks={}
    for name in names:
        expected=(root/'results'/name).read_bytes()
        actual=(out/name).read_bytes()
        if actual!=expected: raise ValueError('Replay differs: '+name)
        checks[name]=hashlib.sha256(actual).hexdigest()
    print(json.dumps({'replay':'PASS','byte_identical':checks},sort_keys=True))
