"""Replay the local N14 census, labelled paths, quadratures and certificates."""
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent


def compare(expected, actual, path=()):
    if type(actual) is not type(expected):
        raise AssertionError((path, type(expected), type(actual)))
    if isinstance(expected, dict):
        assert expected.keys() == actual.keys(), path
        for key in expected:
            compare(expected[key], actual[key], (*path, key))
    elif isinstance(expected, list):
        assert len(expected) == len(actual), path
        for i, (left, right) in enumerate(zip(expected, actual)):
            compare(left, right, (*path, i))
    elif isinstance(expected, float):
        # Discrete choices and rational decisions are checked exactly by the
        # scientific routines. This tolerance is for stored floats only.
        assert math.isclose(expected, actual, rel_tol=3e-8, abs_tol=5e-13), (path, expected, actual)
    else:
        assert expected == actual, (path, expected, actual)


def run():
    if not __debug__:
        raise RuntimeError("Keep Python assertions enabled")
    for line in (ROOT/"SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        assert digest == hashlib.sha256((ROOT/name).read_bytes()).hexdigest(), name
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", OMP_NUM_THREADS="1")
    env.pop("PYTHONOPTIMIZE", None)
    with TemporaryDirectory() as tmp:
        dest = Path(tmp)
        def replay(script, args, name):
            print("Checking", name, flush=True)
            subprocess.run([sys.executable, "-B", str(ROOT/script), *args, str(dest/name)],
                           env=env, check=True)
            compare(json.loads((ROOT/name).read_text()), json.loads((dest/name).read_text()))
        g = dest/"growth.json"
        replay("growth.py", [], "growth.json")
        replay("exchange.py", ["--growth", g, "--output"], "exchange.json")
        replay("analytic.py", [], "analytic.json")
        replay("clock14.py", [g], "clock14.json")
        replay("clock14.py", ["--remaining-width3", g], "clock14_extra.json")
        base = ["--growth", g, "--clock", dest/"clock14.json"]
        replay("readout14.py", [*base,"--points",ROOT/"readout14.json","-o"], "readout14.json")
        replay("readout14.py", [*base,"--extra",dest/"clock14_extra.json",
                               "--points",ROOT/"readout14_extra.json","-o"], "readout14_extra.json")
    print("PASS: N14 census, S3 marginals, analytic bounds, ten N14 clocks and two finite-grid readouts.")


if __name__ == "__main__":
    run()
