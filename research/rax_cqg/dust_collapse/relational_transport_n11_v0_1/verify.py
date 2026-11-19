"""Replay the complete calculation and compare with the archived JSON."""
import json
from pathlib import Path
from math import isclose
import exact
import compare
import audit

ROOT = Path(__file__).resolve().parent


def compare_tree(actual, reference):
    if isinstance(reference,dict):
        assert actual.keys()==reference.keys()
        for key,item in reference.items():
            compare_tree(actual[key],item)
    elif isinstance(reference,list):
        assert len(actual)==len(reference)
        for a,b in zip(actual,reference):
            compare_tree(a,b)
    elif isinstance(reference,float):
        assert isclose(actual,reference,abs_tol=compare.TOL,rel_tol=0), (actual,reference)
    else:
        assert actual==reference


if __name__=="__main__":
    assert exact.compute()==json.loads((ROOT/"exact.json").read_text())
    compare_tree(compare.compute(),json.loads((ROOT/"numerical.json").read_text()))
    compare_tree({"individual_rectangles_checked":48,"rectangle_max_abs_error":audit.mask_check(),
                  "moment_max_abs_error":audit.moment_check()},json.loads((ROOT/"audit.json").read_text()))
    print("PASS: exact moments, exclusion, positive conditional gluing, endpoint and cell comparisons.")
    print("Physical relational transport: HOLD.")
