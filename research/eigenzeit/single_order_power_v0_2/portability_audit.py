"""Reconstruct and compare the two coordinate variants used for the replay checks."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "package"))
from examples import DESIGN, generate, seed

def capture(directory):
    directory.mkdir(parents=True, exist_ok=True)
    for method in ("full_order", "matching"):
        for h in DESIGN["model_h"]:
            rng = np.random.Generator(np.random.PCG64(seed(method, h, "sample")))
            x, _ = generate(DESIGN[method]["n"], 0.0 if h == "0" else 0.5, rng)
            rng = np.random.Generator(np.random.PCG64(seed(method, h, "labels")))
            np.save(directory / (method + h.replace("/", "_") + ".npy"), np.asarray(x[rng.permutation(len(x))], dtype="<f8"))

def compare(original, baseline):
    rows = []
    for case in json.loads((ROOT / "package/examples.json").read_text()):
        method, h = case["method"], case["h"]
        name = method + h.replace("/", "_") + ".npy"
        a, b = np.load(original / name), np.load(baseline / name)
        if a.shape != b.shape or a.shape != (case["n"], 4):
            raise ValueError(name + ": array shape")
        if hashlib.sha256(a.tobytes()).hexdigest() != case["coordinates_sha256"]:
            raise ValueError(name + ": original coordinate digest")
        maximum = float(np.abs(a - b).max())
        if not maximum <= 2**-52:
            raise ValueError(name + ": coordinate difference")
        row = dict(method=method, h=h, coordinates_sha256=hashlib.sha256(b.tobytes()).hexdigest(),
                   changed_components=int(np.count_nonzero(a != b)), max_absolute_difference_hex=maximum.hex())
        if method == "matching":
            pairs = np.random.Generator(np.random.PCG64(seed(method, h, "matching"))).permutation(len(a)).reshape(-1, 2)
            def answers(x):
                d = x[pairs[:, 0]] - x[pairs[:, 1]]
                return abs(d[:, 0]) > np.linalg.norm(d[:, 1:], axis=1)
            left, right = answers(a), answers(b)
            if not np.array_equal(left, right) or int(left.sum()) != case["count"]:
                raise ValueError(name + ": matching results")
            row["queried_comparabilities_sha256"] = hashlib.sha256(np.packbits(left, bitorder="little").tobytes()).hexdigest()
        rows.append(row)
    return rows

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--capture", type=Path)
    group.add_argument("--compare", type=Path, nargs=2)
    args = p.parse_args()
    if args.capture is not None:
        capture(args.capture)
    else:
        print(json.dumps(compare(*args.compare), indent=2))
