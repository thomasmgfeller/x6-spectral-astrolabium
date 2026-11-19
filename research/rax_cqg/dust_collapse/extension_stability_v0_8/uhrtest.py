"""Evaluate the N15 clock responses in two successive projection tests."""
from basis import HERE, build, direct_packet, layout, tails
from tempfile import TemporaryDirectory
from unittest.mock import patch
from argparse import ArgumentParser
import numpy as np

FIRST = (47037, 45950)
SECOND = (46509, 46525)
MASKS = FIRST + SECOND
GRIDS = {"coarse": (32, 6), "fine": (48, 8), "control": (64, 10)}

def calculate(masks):
    results = {}
    # The previously verified width-five sink contraction depends solely on layout.
    with TemporaryDirectory() as temp, patch.object(tails.prior.growth, "layout", layout):
        library = build(temp)
        for mask in masks:
            key = (7, mask)
            direct = direct_packet(key)
            factorized = tails.packet(key, 4, 3, library)
            small_error = float(max(abs(factorized - direct)))
            if small_error >= 1e-13:
                raise ArithmeticError((mask, "Cartesian control", small_error))
            values = {}
            for tag, (n, m) in GRIDS.items():
                values[tag] = tails.packet(key, n, m, library)
                print(mask, tag, values[tag], flush=True)
            changes = [float(max(abs(values[b] - values[a]))) for a, b in
                       (("coarse", "fine"), ("fine", "control"))]
            if max(changes) >= 1e-7:
                raise ArithmeticError((mask, "grid refinement", changes))
            results[str(mask)] = {
                "rows": {tag: [[z.real, z.imag] for z in row] for tag, row in values.items()},
                "cartesian_error": small_error, "grid_changes": changes,
            }
    return results

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(HERE / "uhren.json"))
    parser.add_argument("--round", type=int, choices=(1, 2))
    args = parser.parse_args()
    selected = {1: FIRST, 2: SECOND}.get(args.round, MASKS)
    from basis import save_json
    save_json(args.out, calculate(selected))
