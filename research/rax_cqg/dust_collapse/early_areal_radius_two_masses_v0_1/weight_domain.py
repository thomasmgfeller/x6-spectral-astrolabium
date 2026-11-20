"""Project finite exchangeable N15 weights and verify exact conditional end-weight maxima."""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "inputs/CST_DUST_Praefix_1564_Vier_Marken_v0_1.zip"
SOURCE_HASH = "72c671b458f2d2d0681cfe84b21faf1fbdb1f13fd7b0fdba4e50d7088f2a90f3"

def find_extremum(rows, wanted, cost, keys):
    import numpy as np
    import sympy as sp
    from scipy.optimize import linprog
    from scipy.sparse import csc_matrix
    A = np.asarray(rows, dtype=int)
    opt = linprog(-np.array(cost), A_eq=csc_matrix(A), b_eq=np.array(wanted,float),
                  bounds=(0,None), method="highs",
                  options={"primal_feasibility_tolerance":1e-10, "dual_feasibility_tolerance":1e-10})
    assert opt.success
    support = np.flatnonzero(opt.x > 1e-12)
    sub = sp.Matrix(A[:,support])
    pivots = list(sub.T.to_DM().rref()[1])
    assert len(pivots) == len(support)
    exact = sub[pivots,:].inv() * sp.Matrix([wanted[i] for i in pivots])
    assert min(exact) >= 0 and sub*exact == sp.Matrix(wanted)
    dual = [F(float(-y)).limit_denominator(1000000) for y in opt.eqlin.marginals]
    return {"primal":{",".join(map(str,keys[i])):str(value) for i,value in zip(support,exact) if value},
            "dual":{str(i):str(y) for i,y in enumerate(dual) if y}}

def execute(search):
    from extension import MASK, build_columns, load_inputs, marked_three
    from verify import deletion_catalogue
    data, residual, weights, catalog = load_inputs()
    reps, codes, parents, _ = marked_three(data, residual, weights)
    columns = build_columns(reps, codes, catalog)
    assert set(columns) == deletion_catalogue(codes,catalog)
    keys = sorted(columns)
    prefixes = sorted(parents)
    ids = sorted({j for j,orbit in reps.values() if any((raw & MASK)==1564 for raw in orbit)})
    assert (len(keys),len(prefixes),len(ids)) == (928,72,10)
    coarse, local = [], []
    for column in keys:
        counts, ends = Counter(), Counter()
        for rep in column:
            end, orbit = reps[rep]
            assert 6 % len(orbit) == 0
            for raw in orbit:
                p = raw & MASK
                counts[p] += 6 // len(orbit)
                if p == 1564:
                    ends[end] += 6 // len(orbit)
        assert sum(counts.values()) == 24 and sum(ends.values()) == counts[1564]
        coarse.append(counts)
        local.append(ends)
    wanted = [24*parents[p] for p in prefixes]
    path = HERE / "weight_certificates.json"
    if search:
        rows = [[col[p] for col in coarse] for p in prefixes]
        certs = {str(j):find_extremum(rows,wanted,[c[j] for c in local],keys) for j in ids}
        path.write_text(json.dumps(certs,indent=2)+"\n")
    certs = json.loads(path.read_text())
    assert set(certs) == set(map(str,ids))
    maxima = {}
    vectors = []
    key_index = {k:i for i,k in enumerate(keys)}
    for j in ids:
        doc = certs[str(j)]
        primal = {key_index[tuple(map(int,k.split(",")))]:F(v) for k,v in doc["primal"].items()}
        dual = {prefixes[int(k)]:F(v) for k,v in doc["dual"].items()}
        assert min(primal.values()) > 0 and sum(primal.values()) == 1
        for p in prefixes:
            assert sum(x*coarse[i][p] for i,x in primal.items()) == 24*parents[p]
        for col, end in zip(coarse,local):
            assert sum(v*dual.get(p,0) for p,v in col.items()) >= end[j]
        value = sum(x*local[i][j] for i,x in primal.items())
        assert value == sum(24*parents[p]*y for p,y in dual.items())
        vec = [sum(x*local[i][k] for i,x in primal.items())/(24*parents[1564]) for k in ids]
        assert sum(vec)==1 and min(vec)>=0
        vectors.append(vec)
        maxima[str(j)] = str(value/(24*parents[1564]))
    # Fraction-only row reduction of the nine differences from the first feasible vector.
    basis = {}
    for vector in vectors[1:]:
        diff = [x-y for x,y in zip(vector,vectors[0])]
        for k in sorted(basis):
            diff = [x-diff[k]*y for x,y in zip(diff,basis[k])]
        pivot = next((k for k,d in enumerate(diff) if d),None)
        if pivot is not None:
            basis[pivot] = [v/diff[pivot] for v in diff]
    return {"certified_affine_dimension_lower_bound":len(basis),"projection_columns":len(keys),"older_prefix_masses":len(prefixes),
            "conditional_maxima":maxima,"conditional_minima":{str(j):"0" for j in ids},
            "minimum_proof":"At least two different certified conditional unit vectors attain 1. For every coordinate a different such unit vector attains 0."}

def run(search=False):
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_HASH
    with TemporaryDirectory() as tmp, ZipFile(SOURCE) as z:
        for name in ["extension.py","verify.py","catalog.json","CST_DUST_Praefix_1564_Selektionsgleichung_v0_1_Pruefpaket.zip"]:
            z.extract(name,tmp)
        sys.path.insert(0,tmp)
        try:
            result = execute(search)
        finally:
            sys.path.pop(0)
    assert list(result["conditional_maxima"].values()).count("1") >= 2
    return result

if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Use Python with assertions enabled.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--search", action="store_true")
    print(json.dumps(run(parser.parse_args().search),indent=2))
