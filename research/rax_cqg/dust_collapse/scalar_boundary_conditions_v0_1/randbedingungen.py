"""Exakte Rechnung am skalaren Ausgang der 33 eingefrorenen AA-Ordnungen."""
import argparse
import hashlib
import json
from fractions import Fraction as F
from math import gcd, lcm
from pathlib import Path

ROOT = Path(__file__).resolve().parent
B2 = F(8, 3)


def check(test, message):
    if not test:
        raise ValueError(message)


def sources():
    manifest = json.loads((ROOT / "quellen.json").read_bytes())
    inputs = {}
    for name, source in manifest["files"].items():
        data = (ROOT.parent / source["path"]).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        check(source["sha"] == blob, name)
        if name.endswith(".json"):
            inputs[name] = json.loads(data)
    return manifest["commit"], inputs


def transpose(a):
    return list(map(list, zip(*a)))


def dot(x, y):
    return sum(i*j for i, j in zip(x, y, strict=True))


def product(a, b):
    return [[dot(v, w) for w in transpose(b)] for v in a]


def det(a):
    return a[0][0]*a[1][1] - a[0][1]*a[1][0]


def rank(rows):
    a = [list(map(F, r)) for r in rows]
    pos = 0
    for col in range(len(a[0])):
        pivot = next((k for k in range(pos, len(a)) if a[k][col]), None)
        if pivot is None:
            continue
        a[pos], a[pivot] = a[pivot], a[pos]
        for j in range(pos+1, len(a)):
            factor = a[j][col] / a[pos][col]
            a[j] = [x-factor*y for x, y in zip(a[j], a[pos])]
        pos += 1
    return pos


def null_vector(cross):
    a, b = next(row for row in cross if any(row))
    d = lcm(a.denominator, b.denominator)
    v = [int(b*d), int(-a*d)]
    divider = gcd(*v) * (1 if next(i for i in v if i) > 0 else -1)
    return [i//divider for i in v]


def analyse(history, ref):
    h = [list(map(F, row)) for row in history["H0_over_va"]]
    boundary = (0, 1, 3, 4)
    k = [[h[i][j]-h[i][2]*h[2][j]/h[2][2] for j in boundary] for i in boundary]
    check(k == [list(map(F, r)) for r in ref["schur_over_beta"]], "Schur")
    check(all(sum(r)==0 for r in k), "gemeinsame Feldverschiebung")
    left, cross, right = ([r[:2] for r in k[:2]], [r[2:] for r in k[:2]],
                          [r[2:] for r in k[2:]])
    n = rank(cross)
    check(n == ref["cross_rank"] and n in (1, 2), "Rang")
    item = {"order": history["order_code"], "rank": n}
    if n == 2:
        return item
    v = null_vector(cross)
    check(all(dot(r,v)==0 for r in cross), "Postconstraint")
    rv = [dot(r,v) for r in right]
    # Coordinates (y, p/b). The physical constraint is b times this row.
    row = [-z for z in rv] + v
    l_squared = product(left, left)
    metric = [[int(i==j) + B2*l_squared[i][j] for j in range(2)] for i in range(2)]
    d = det(metric)
    inv = [[metric[1][1]/d, -metric[0][1]/d], [-metric[1][0]/d, metric[0][0]/d]]
    t = product(transpose(cross), product(inv, cross))
    q = B2*(t[0][0]+t[1][1])
    check(q > 0 and det(t)==0 and all(dot(r,v)==0 for r in t), "Dämpfung")
    # N = (8 pi^(5/2)/b) * sqrt(factor) is the scalar norm squared per fibre length.
    factor = 1 / (h[2][2]**2 * d * q)
    item.update(null=v, constraint_row=list(map(str,row)), gaussian_q=str(q),
                reduced_squared_norm_factor=str(factor))
    return item


def bracket(r, s):
    return dot(r[:2], s[2:])-dot(r[2:], s[:2])


def run():
    commit, inputs = sources()
    raw = inputs["quellen/aa_hessians.json"]["histories"]
    ref = {h["code"]: h for h in inputs["quellen/domain_certificate.json"]["histories"]}
    check(len(raw)==len(ref)==33 and {h["order_code"] for h in raw}==set(ref), "Familie")
    records = [analyse(h, ref[h["order_code"]]) for h in sorted(raw, key=lambda h:h["order_code"])]
    singular = [r for r in records if r["rank"]==1]
    codes = [r["order"] for r in singular]
    rows = [list(map(F,r["constraint_row"])) for r in singular]
    comm = [[bracket(r,s) for s in rows] for r in rows]
    check(codes==[9116,17308,25372,25496,25500], "Defiziente Ordnungen")
    check(rows[2]==rows[3] and comm[2][4]==10, "axiale Paarung")
    check(rank(rows)==3 and rank(comm)==2, "Ränge der Algebra")
    center = [F(0),F(0),F(1),F(1)]
    check([a+b for a,b in zip(rows[0],rows[1])] == [29*x for x in center]
          and all(bracket(center,r)==0 for r in rows), "Zentrum")
    slopes = [-rows[i][0] for i in (2,4)]
    check(all(rows[i][2:]==[1,-1] and rows[i][1]==-rows[i][0] for i in (2,4)), "Normierung der Achse")
    comm_unit = comm[2][4]/2
    half_gap = comm_unit/2
    return {
        "source_commit": commit, "quadratic_scale_b_squared": str(B2),
        "histories": records, "rank_two_count": len(records)-len(singular),
        "singular_ordering": codes, "row_rank": rank(rows), "bracket_rank": rank(comm),
        "bracket_matrix_over_i_b_primitive_rows": [list(map(str,r)) for r in comm],
        "central_row_in_y_p_over_b": list(map(str,center)),
        "antisymmetric_slopes_over_b": list(map(str,slopes)),
        "commutator_over_i_b_unit_axis": str(comm_unit),
        "sharp_mean_squared_residual_over_b": str(half_gap),
        "optimal_gaussian_decay_over_b": str(half_gap),
        "optimal_gaussian_phase_curvature_over_b": str(sum(slopes)/2),
        "joint_strong_kernel_in_tempered_distributions": "zero",
        "physical_relative_norm_to_empty_branch": "HOLD",
        "physical_P3_pilot_M1_completed": inputs["quellen/clock_record.json"]["physical_P3_comparisons"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = json.dumps(run(), indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.write_text(result, encoding="utf-8")
    else:
        print(result, end="")
