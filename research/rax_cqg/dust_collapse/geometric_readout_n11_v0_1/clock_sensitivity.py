"""Separate clock-width intervention; preserves the mean and fixes the dust density."""
import argparse
import json

import numpy as np

from verify import HERE, close, contract, packets, read, ward


def probabilities(weights):
    three, one = (float(x) for x in weights)
    failure = 1 - one - three
    assert min(one, three, failure) >= 0
    return {"one_pair":one, "three_pairs":three, "failure":failure, "score":one-three}


def experiment(inner, outer):
    t0 = -2*ward.DELTA
    params = packets.CONTRACT
    h = params["clock_lobe_half_width"]
    x, w = packets.quadrature(outer)
    grid = packets.quadrature(inner)
    distributions = {}
    for name, offsets in (("narrow",[0]),("split",params["clock_offsets_from_affine_T3"])):
        mean = variance = 0.
        branches = np.zeros(2)
        for off in offsets:
            for node, weight in zip(x,w,strict=True):
                delta = off+h*node
                _, v = packets.reduced_weight(t0+delta,inner,grid)
                mass = weight / len(offsets)
                mean += mass*delta
                variance += mass*delta**2
                branches += mass*np.abs(v)**2/4
        close(mean,0)
        distributions[name] = {"variance":float(variance), "coupled":probabilities(branches),
                               "common_C0_dust":probabilities([branches[0],branches[0]])}
    close(distributions["split"]["variance"] - distributions["narrow"]["variance"],1/256)
    distributions["score_shift_split_minus_narrow"] = {
        k:distributions["split"][k]["score"]-distributions["narrow"][k]["score"]
        for k in ("coupled","common_C0_dust")}
    return distributions


def compare_fields(a,b):
    if isinstance(a,dict):
        assert set(a)==set(b)
        for key in a:
            compare_fields(a[key],b[key])
    else:
        close(a,b)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    arg = parser.parse_args()
    assert read(HERE/"clock_control.json")["role"].startswith("Separate")
    results = [experiment(*grid) for grid in contract["grids_inner_outer"]]
    for row in results[:-1]:
        compare_fields(row,results[-1])
    for name in ("coupled","common_C0_dust"):
        primary = read(HERE/"results.json")["fine_grid"]["runs"][name]["low"]
        for outcome in ("one_pair","three_pairs","failure"):
            close(primary[outcome],results[-1]["split"][name][outcome])
    path = HERE/"clock_sensitivity_results.json"
    if arg.write:
        path.write_text(json.dumps(results[-1],indent=2,allow_nan=False)+"\n")
    else:
        compare_fields(results[-1], read(path))
    print(json.dumps(results[-1], indent=2))
