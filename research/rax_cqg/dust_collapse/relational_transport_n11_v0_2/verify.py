"""Offline replay of the finite-cut construction; run without Python optimization."""
from pathlib import Path
import hashlib
import json
import math
import shutil
import subprocess
import sys
import tempfile
import clock_law
import flat_dust
import n11
import record

ROOT=Path(__file__).resolve().parent


def compare(actual,archived,tolerance):
    if isinstance(archived,dict):
        assert actual.keys()==archived.keys()
        for k in actual:
            compare(actual[k],archived[k],tolerance)
    elif isinstance(archived,list):
        assert len(actual)==len(archived)
        for x,y in zip(actual,archived):
            compare(x,y,tolerance)
    elif isinstance(archived,float):
        assert math.isclose(actual,archived,abs_tol=tolerance,rel_tol=0)
    else:
        assert actual==archived


def read(name):
    return json.loads((ROOT/name).read_bytes())


def variance_replay():
    with tempfile.TemporaryDirectory() as folder:
        temp=Path(folder)
        (temp/"sources").mkdir()
        for src,dest in [("sources/v01_exact.py","exact.py"),("sources/ward_clock.py","sources/ward_clock.py"),
                         ("sources/readout.json","sources/readout.json")]:
            shutil.copyfile(ROOT/src,temp/dest)
        p=subprocess.run([sys.executable,"-B","exact.py"],cwd=temp,check=True,capture_output=True,text=True)
        assert json.loads(p.stdout)==read("sources/v01_exact.json")


if __name__=="__main__":
    if not __debug__:
        raise SystemExit("Run verify.py without -O to enable verification.")
    for f in read("provenance.json")["files"]:
        data=(ROOT/f["local"]).read_bytes()
        assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\x00"+data).hexdigest()==f["blob"]
    variance_replay()
    # JSON normalization is only for returning native tuples as lists.
    assert json.loads(json.dumps(clock_law.compute()))==read("clock_law.json")
    compare(n11.compute(),read("n11.json"),5e-9)
    compare(record.compute(),read("record.json"),5e-9)
    compare(flat_dust.compute(),read("flat_dust.json"),1e-12)
    print("PASS: variance, exact cut law, N11 composition, binary record, fixed 1+3 amplitude.")
    print("Physical stage 6 HOLD; physical P3 histories 0.")
