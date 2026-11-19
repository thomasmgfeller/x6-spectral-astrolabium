"""Use the unchanged seven subset certificates with the four new clock disks."""
from functools import lru_cache
from fractions import Fraction as F
from unittest.mock import patch
from reference import ROOT, SOURCE, full, save_json
import bottleneck

GRIDS = ("coarse","fine")
NEW = (339773,524287,45885,45851)

def new_clocks():
    values = {}
    for file in ("clock_339773.json","clock_524287.json","four_parents.json"):
        values.update(full.read(ROOT/file))
    if set(values) != set(map(str,NEW)):
        raise ValueError("Missing clock responses")
    return values

original_inputs = full.inputs

@lru_cache(None)
def inputs(tag):
    names,reach,base,cols,known,mags,radii = original_inputs(tag)
    clock = {**full.read(SOURCE/"uhren.json"), **new_clocks()}
    for mask,row in clock.items():
        j = names.index("N15_"+mask)
        if known[j] is not None or not all(j in r for r in reach):
            raise ValueError(mask)
        amp = [full.cf(complex(*v)) for v in row["rows"][tag]]
        radius = F("1e-7")
        cap = max(map(full.modupper,amp))+radius
        if cap >= mags[j]:
            raise ValueError("Clock disk exceeds original majorant")
        known[j],mags[j],radii[j] = amp,cap,radius
    return names,reach,base,cols,known,mags,radii

def calculate():
    old = full.read(SOURCE/"volltraeger.json")["second"]
    for grid in old["limiting_projections"].values():
        for parent in grid.values():
            first = tuple(int(row[0].split("_")[1]) for row in parent["smallest_cross_terms"][:4])
            if first != NEW:
                raise ValueError(("Published order",first))
    with patch.object(full,"inputs",inputs), patch.object(bottleneck,"inputs",inputs):
        result = full.calculate()
        result["limiting_projections"] = {tag:bottleneck.calculate(tag) for tag in GRIDS}
    return result

if __name__=="__main__":
    save_json(ROOT/"bounds.json",calculate())
