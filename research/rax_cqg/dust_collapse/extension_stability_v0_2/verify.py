"""Verify the supplied files and repeat the numerical campaign in a private directory."""
from fractions import Fraction
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parent
CONTRACT_SHA256 = "b45c76f5b6dfcdc4261ebc679fed5c8e69007ea442eded0a769bd84b4be3e180"


def compare(original, repeated, path=()):
    if isinstance(original, dict):
        assert original.keys() == repeated.keys(), path
        for key, item in original.items():
            compare(item, repeated[key], (*path, key))
    elif isinstance(original, list):
        assert len(original) == len(repeated), path
        for index, (a, b) in enumerate(zip(original, repeated)):
            compare(a, b, (*path, index))
    elif isinstance(original, float) or str(path[-1]).endswith("_exact"):
        a, b = (float(Fraction(x)) for x in (original, repeated))
        # Relative gate ratios involve differences of probabilities near one.
        if not math.isclose(a, b, abs_tol=5e-13, rel_tol=3e-8):
            raise AssertionError((path, a, b))
    else:
        assert original == repeated, path


def main():
    if not __debug__:
        raise RuntimeError("Use ordinary Python so that scientific assertions are active")
    for line in (ROOT / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        assert sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    assert sha256((ROOT / "fibre_contract.json").read_bytes()).hexdigest() == CONTRACT_SHA256
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
    env.pop("PYTHONOPTIMIZE", None)
    with TemporaryDirectory() as tmp:
        grids, result = (Path(tmp) / name for name in ("grids.json", "results.json"))
        for script, args in [("compute_grids.py", [grids]), ("analysis.py", [grids, result])]:
            subprocess.run([sys.executable, "-B", str(ROOT / script), *args], check=True, env=env)
        for new in (grids, result):
            compare(json.loads((ROOT / new.name).read_text()), json.loads(new.read_text()))
    print("PASS: file digests, both enumeration routes, rank screen, full quadrature, "
          "controls, archived outputs, weight bounds and both grid certificates.")


if __name__ == "__main__":
    main()
