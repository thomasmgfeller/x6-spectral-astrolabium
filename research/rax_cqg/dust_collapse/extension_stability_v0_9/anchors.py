"""Total-success overlaps from the three published N14 supporting-plane vectors."""
from unittest.mock import patch
import mpmath as mp
import numpy as np
from reference import ROOT, SOURCE, full, layout, save_json
import matrices
from projections import overlap
from teiltraeger import names_and_reach

SUPPORT = ("N14_734","N14_760","N14_8191")

def calculate():
    catalog = full.read(matrices.ROOT/"catalog.json")
    masks = sorted({int(s) for r in catalog["roots"].values() for s in r["ends"]})
    old_names,_ = names_and_reach()
    g = np.load(SOURCE/"gram.npy")
    old_rows = [old_names.index(s) for s in SUPPORT]
    result = {}
    with mp.workdps(70), patch.object(matrices.geometry,"order",layout):
        anchors = [matrices.geometry.kernel(matrices.common.prior.key(s))[1] for s in SUPPORT]
        for mask in masks:
            status,state = matrices.geometry.kernel((7,mask))
            if status["status"] != "ADMISSIBLE":
                raise ValueError(mask)
            # Save each rounded bin to preserve the exact dyadic sum convention.
            rows = [[(z.real,z.imag) for z in overlap(a,state)] for a in anchors]
            name = "N15_"+str(mask)
            if name in old_names:
                array = np.array([[complex(*z) for z in row] for row in rows])
                if not np.array_equal(array, g[:,old_rows,old_names.index(name)].T):
                    raise ValueError(("Prior anchor row",name))
            result[name] = rows
    if len(result)!=1048:
        raise ValueError("Incomplete geometry set")
    return result

if __name__=="__main__":
    save_json(ROOT/"support_rows.json",calculate())
