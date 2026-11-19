"""Re-evaluate the original N15 certificate after each round of resolved clock phases."""
from fractions import Fraction as F
from unittest.mock import patch
from argparse import ArgumentParser
from functools import lru_cache
import json
from basis import HERE, REFERENCE, full
import bottleneck
from uhrtest import FIRST, SECOND

def calculate(masks):
    clocks = json.loads((HERE / "uhren.json").read_text())
    radius = F("1e-7")
    old_inputs = full.inputs

    @lru_cache(None)
    def updated(tag):
        names, reach, base, cols, known, mags, radii = old_inputs(tag)
        for number in masks:
            mask = str(number)
            item = clocks[mask]
            j = names.index("N15_" + mask)
            if known[j] is not None or not all(j in group for group in reach):
                raise ValueError("Unexpected reference status or reachability")
            amps = [full.cf(complex(*z)) for z in item["rows"][tag]]
            cap = max(map(full.modupper, amps)) + radius
            if cap > mags[j]:
                raise ValueError("Resolved clock falls outside the inherited bound")
            known[j], mags[j], radii[j] = amps, cap, radius
        return names, reach, base, cols, known, mags, radii

    with patch.object(full, "inputs", updated), patch.object(bottleneck, "inputs", updated):
        result = full.calculate()
        result["limiting_projections"] = {tag: bottleneck.calculate(tag) for tag in ("coarse", "fine")}
    if F(result["bound_fraction"]) <= F(full.read(REFERENCE / "full.json")["bound_fraction"]):
        raise ArithmeticError("No improvement in the full-support bound")
    return result

def both_rounds():
    old = full.read(REFERENCE / "bottleneck.json")
    def leading(data):
        return [[int(name.split("_")[1]) for name, _ in root["smallest_cross_terms"][:2]]
                for grid in data.values() for root in grid.values()]
    if any(tuple(pair) != FIRST for pair in leading(old)):
        raise ValueError("Round one differs from the two published limiting types")
    result = calculate(FIRST)
    if any(tuple(pair) != SECOND for pair in leading(result["limiting_projections"])):
        raise ValueError("Round two differs from the new limiting types")
    return {"first": result, "second": calculate(FIRST + SECOND)}

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(HERE / "volltraeger.json"))
    args = parser.parse_args()
    from basis import save_json
    save_json(args.out, both_rounds())
