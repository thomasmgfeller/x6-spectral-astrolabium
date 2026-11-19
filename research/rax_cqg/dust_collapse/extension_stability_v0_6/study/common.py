"""The frozen v0.5 inputs and deterministic branch naming."""
import json
from pathlib import Path
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
REF = HERE.parent / "reference"
if not REF.is_dir():
    REF = HERE.parents[1] / "extension_stability_v0_5"
sys.path.insert(0, str(REF))
import readout14 as prior
import clock14 as clocks

def load(name):
    return json.loads((REF / name).read_text())

def setup():
    growth = load("growth.json")
    old = load("upstream/results.json")["branch_order"]
    names = old + [f"N14_{m}" for m in growth["sequential_admissible"]]
    reach = []
    for root in prior.ROOT_NAMES:
        known = load("readout14.json")["reachable_non_root"][root]
        children = {f"N14_{m}" for m in growth["by_root"][root]["admissible_end_marked_paths"]}
        reach.append([i for i,s in enumerate(names) if s in children or s in known])
    assert len(names) == 169 and set(reach[0]) | set(reach[1]) == set(range(2,len(names)))
    return names, reach

def archived():
    old = load("upstream/v03/upstream/v02_grids.json")["grids"]
    rows = {f"N11_{m}":old[r] for m,r in [(7,"chain"),(1,"one")]}
    names, _ = setup()
    for name in names:
        size, mask = prior.key(name)
        if size == 4:
            rows[name] = old[f"poset{mask:02}_lift"]
    for file in ["upstream/clocks_all.json","clock14.json","clock14_extra.json"]:
        data = load(file)
        rows.update({s:v["grids"] for s,v in data.get("branches",data).items()})
    assert len(rows)==40
    return rows

def coherent(row):
    return clocks.reference.decode(row["amplitudes"])[0].sum(axis=1)/np.sqrt(2)
