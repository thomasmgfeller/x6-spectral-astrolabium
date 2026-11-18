"""Check package integrity, regenerate results, and compare exact/float fields."""
import hashlib
import json
import math
from pathlib import Path
import sys

import abel_check
import run

ROOT=Path(__file__).resolve().parent


def compare(a,b,path=""):
    if type(a)!=type(b):
        raise AssertionError(f"type mismatch: {path}")
    if isinstance(a,dict):
        assert a.keys()==b.keys(),path
        for key in a: compare(a[key],b[key],f"{path}/{key}")
    elif isinstance(a,list):
        assert len(a)==len(b),path
        for i,(x,y) in enumerate(zip(a,b)): compare(x,y,f"{path}/{i}")
    elif isinstance(a,float):
        tol=5e-10 if "first_gate_loss_lambda" in path else 5e-12
        assert math.isfinite(b) and abs(a-b)<=tol,path
    else:
        assert a==b,path


if __name__=="__main__":
    if not __debug__: raise SystemExit("Enable assertions for the replay.")
    for row in (ROOT/"SHA256SUMS").read_text().splitlines():
        digest,filename=row.split("  ",1)
        assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==digest,filename
    reference=json.loads((ROOT/"results.json").read_text())
    compare(reference,run.main())
    compare(json.loads((ROOT/"abel_results.json").read_text()),abel_check.check())
    print("PASS: archive digests, rank certificates, all probabilities, weight scan and Abel cross-check.")
