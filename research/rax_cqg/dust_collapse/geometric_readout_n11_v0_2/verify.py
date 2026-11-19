"""Rebuild the N11 Gaussian record and replay the dust and clock interventions."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import geometry
import records

HERE=Path(__file__).resolve().parent


def source_checks():
    for name,source in geometry.read(HERE/"sources.json").items():
        data=(HERE/"sources"/name).read_bytes()
        assert hashlib.sha256(data).hexdigest()==source["sha256"]
    with tempfile.TemporaryDirectory() as tmp:
        script=Path(tmp)/"check.py"
        shutil.copyfile(HERE/"sources/canonical_check.py",script)
        subprocess.run([sys.executable,"-B",str(script)],check=True,stdout=subprocess.DEVNULL)
        assert geometry.read(Path(tmp)/"results.json")==geometry.read(HERE/"sources/canonical.json")


def compare_rows(a,b):
    if isinstance(a,dict):
        assert a.keys()==b.keys()
        for k in a: compare_rows(a[k],b[k])
    elif isinstance(a,list):
        assert len(a)==len(b)
        for x,y in zip(a,b): compare_rows(x,y)
    elif isinstance(a,float):
        records.close(a,b)
    else: assert a==b


if __name__=="__main__":
    if not __debug__: raise RuntimeError("Run with Python assertions enabled")
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true",help="write the rebuilt result")
    args=parser.parse_args()
    source_checks()
    boundary=geometry.compute()
    eta=boundary["two_modes"]["7,8"]["balanced_efficiency"]
    rec=records.compute(eta)
    result={"boundary":boundary,"records":rec,"scope":"Conditional N11 scalar quotient; physical 5A HOLD."}
    path=HERE/"results.json"
    if args.write: path.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    else: compare_rows(result,geometry.read(path))
    print("Verified canonical reduction, gauge lift, single-mode obstruction, three two-mode witnesses,")
    print("three-mode bound, coherent balances, dust and clock controls on all three grids.")
