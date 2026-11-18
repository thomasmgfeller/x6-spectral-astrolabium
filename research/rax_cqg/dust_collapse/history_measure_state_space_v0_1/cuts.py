"""Exact scalar sewing across two finite order ideals, before boundary normalization."""
import argparse
import json
import sys
from itertools import product
from collections import Counter
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "v05"))
import growth

geometry = growth.geometry
MASKS = (1790, 5374)
CUTS = ((4, 5, 6), (4, 5, 13))
LAYERS = (1, -9, 16, -8)


def collar_coordinates(inner):
    dim = 8 + len(inner)
    transform = sp.zeros(dim)
    transform[1:4, :3] = sp.eye(3)
    transform[7:10, 3:6] = sp.eye(3)
    transform[:4, -2] = geometry.BM
    transform[7:11, -1] = geometry.BP
    for k, node in enumerate(inner):
        transform[node, 6+k] = 1
    return transform


def chirps(dim):
    result = sp.zeros(dim)
    result[-2, :3] = -geometry.AM[1:4, :].T
    result[:3, -2] = -geometry.AM[1:4, :]
    result[-1, 3:6] = geometry.AP[:3, :].T
    result[3:6, -1] = geometry.AP[:3, :]
    result[-2, -2] = -geometry.AM.dot(geometry.BM)
    result[-1, -1] = geometry.AP.dot(geometry.BP)
    return result


def action(mask):
    """Return G, inner labels and raw ordered-pair coefficients in v0.4 coordinates."""
    inner, coefficients, _ = growth.layout((6, mask))
    dim = 8 + len(inner)
    hessian = sp.zeros(dim)
    for (i, j), weight in coefficients.items():
        value = sp.Rational(weight, 2)
        hessian[i, i] -= value
        hessian[j, j] -= value
        hessian[i, j] += value
        hessian[j, i] += value
    transform = collar_coordinates(inner)
    return transform.T * hessian * transform + chirps(dim), inner, coefficients


def eliminate(mat, keep, remove):
    block = mat[remove, remove]
    det = block.det()
    if not det:
        raise ArithmeticError("Singular partial Fresnel integral")
    eff = mat[keep, keep] - mat[keep, remove] * block.inv() * mat[remove, keep]
    return eff, det, geometry.inertia(block)


def reduced(mask):
    """Outer Hessian K (x[3], y[3]), determinant and signature of the bulk/gauge block."""
    matrix, _, _ = action(mask)
    return eliminate(matrix, list(range(6)), list(range(6, matrix.rows)))


def edge_rows(pairs, left_edges, right_edges, bridge_edges, left, right):
    # Recount each interval from the two induced orders and the recorded
    # cross relations. A past ideal and its complementary filter are convex.
    edges = left_edges | right_edges | bridge_edges
    nodes = left | right
    for i, j in sorted(pairs):
        if (i, j) in bridge_edges:
            size = (sum((i, k) in left_edges and (k, j) in bridge_edges for k in left)
                    + sum((i, k) in bridge_edges and (k, j) in right_edges for k in right))
        else:
            size = sum((i, k) in edges and (k, j) in edges for k in nodes)
        yield (i, j), LAYERS[size] if size < len(LAYERS) else 0


def piece(rows, coordinates):
    # Each term represents -b_ij (q_j-q_i)^2 / 4 in the action.
    matrix = sp.zeros(coordinates.cols)
    for (i, j), b in rows:
        dq = coordinates[j, :] - coordinates[i, :]
        matrix -= sp.Rational(b, 2) * dq.T * dq
    return matrix


def by_parts(full, indices, reverse=False):
    boundary = list(range(6))
    first, second = reversed(indices) if reverse else indices
    # Noninvertible local Fresnel blocks must retain all Fourier constraints.
    # Congruently eliminate a nonsingular principal minor of the first block.
    selected = list(full[first,first].rref()[1])
    regular = [first[i] for i in selected]
    null = [i for i in first if i not in regular]
    mid, det_a, sig_a = eliminate(full, boundary+second+null, regular)
    n_boundary = len(boundary)
    k = len(null)
    extra = {}
    if k:
        size = mid.rows-k
        assert mid[size:,size:] == sp.zeros(k)
        constraint = mid[size:,:size]
        cols = list(constraint[:,n_boundary:].rref()[1])
        assert len(cols) == k  # solved inside the second part, none imposed on the outer state
        piv = [n_boundary+j for j in cols]
        free = [j for j in range(size) if j not in piv]
        pivot = constraint[:,piv]
        basis = sp.zeros(size,len(free))
        for j,col in enumerate(free):
            basis[col,j] = 1
        solved = -pivot.inv()*constraint[:,free]
        for row,col in enumerate(piv):
            basis[col,:] = solved[row,:]
        assert constraint*basis == sp.zeros(k,len(free))
        # The Fourier delta removes k variables, with Jacobian 1/|det pivot|.
        mid = basis.T*mid[:size,:size]*basis
        jac = pivot.det()
        extra = {"fourier_delta_count":k,
                 "delta_rows_outer_then_second":[list(map(str,row)) for row in constraint.tolist()],
                 "outer_then_second_global_indices":boundary+second,
                 "solved_global_indices":[second[j] for j in cols],
                 "absolute_delta_jacobian":str(1/abs(jac))}
    else:
        jac = sp.Integer(1)
        extra = {"fourier_delta_count":0}
    effective, det_b, sig_b = eliminate(mid,boundary,list(range(n_boundary,mid.rows)))
    # Hyperbolic pairs contribute k positive and k negative directions.
    combined_det = (-1)**k * det_a * jac**2 * det_b
    return effective, combined_det, sig_a+sig_b, {
        "regular_pivot_determinants":list(map(str,(det_a,det_b))),
        "regular_pivot_signatures":list(map(int,(sig_a,sig_b))),**extra}



def clock_monomials(rows):
    # Endpoint j carries density rho_j. These are the coefficients in
    # sum b_ij rho_j (T_j-T_i)^2, apart from a common model prefactor.
    out = Counter()
    for (i,j), b in rows:
        out[j,j,j] += b
        out[j,i,i] += b
        out[j,min(i,j),max(i,j)] -= 2*b
    return out


def sewn(mask, ideal):
    full, inner, coefficients = action(mask)
    reference, determinant, signature = reduced(mask)
    edges = set(coefficients)
    left = set(geometry.P) | set(ideal)
    right = set(geometry.F) | (set(inner) - set(ideal))
    assert left.isdisjoint(right) and len(left | right) == full.rows
    assert not (edges & set(product(right, left)))
    edge_l = edges & set(product(left, left))
    edge_r = edges & set(product(right, right))
    bridges = edges & set(product(left, right))
    assert len(edge_l | edge_r | bridges) == len(edges)
    t = collar_coordinates(inner)
    def recover(terms):
        return list(edge_rows(terms, edge_l, edge_r, bridges, left, right))
    all_rows = [recover(terms) for terms in (edge_l, edge_r, bridges)]
    assert dict(x for group in all_rows for x in group) == coefficients
    # F4 = number of events minus the sum of pair coefficients. All node
    # constants in the dust rows C_j occur once under this disjoint split.
    gravity = [len(left)-sum(b for _,b in all_rows[0]),
               len(right)-sum(b for _,b in all_rows[1]),
               -sum(b for _,b in all_rows[2])]
    assert sum(gravity) == growth.layout((6,mask))[2]
    dust = Counter()
    for rows in all_rows:
        dust.update(clock_monomials(rows))
    assert dust == clock_monomials(coefficients.items())
    combined = sum((piece(rows, t) for rows in all_rows), chirps(full.rows))
    assert combined == full
    left_fields = [6+k for k, node in enumerate(inner) if node in ideal] + [full.rows-2]
    right_fields = [6+k for k, node in enumerate(inner) if node not in ideal] + [full.rows-1]
    records = {}
    for side, reverse in (("ideal_first", False), ("filter_first", True)):
        k, det, sig, parts = by_parts(combined, (left_fields, right_fields), reverse)
        assert k == reference and det == determinant and sig == signature
        records[side] = parts
    effective_bridges = [(ij,b) for ij,b in all_rows[-1] if b]
    inner_bridges = [(ij,b) for ij,b in effective_bridges if all(node in inner for node in ij)]
    omitted = piece(inner_bridges, t)
    assert omitted != sp.zeros(full.rows)
    indices = list(range(6,full.rows))
    altered = combined-omitted
    if altered[indices,indices].det() == 0:
        control = {"singular_integrated_block": True}
    else:
        changed, d, s = eliminate(altered, list(range(6)), indices)
        error = max(abs(v) for v in changed-reference)
        assert error > 0
        control = {"singular_integrated_block":False, "max_abs_K_difference":str(error),
                   "determinant":str(d), "signature":int(s)}
    return {"inner_past_ideal":list(ideal),
            "F4_ideal_filter_cross":gravity,
            "distinct_nonzero_dust_quadratic_monomials":sum(bool(v) for v in dust.values()),
            "reconstructed_dust_rows":len(left | right), "retained_cross_relations":len(bridges),
            "nonzero_cross_coefficients":len(effective_bridges),
            "nonzero_inner_cross_coefficients":len(inner_bridges),
            "cross_inner_scalar_rank":full[left_fields[:-1],right_fields[:-1]].rank(),
            "sewn":records, "negative_control_without_inner_cross_action":control}


def run():
    result = {}
    for mask in MASKS:
        eff, determinant, sig = reduced(mask)
        result[str(mask)] = {"outer_hessian_xy": [[str(v) for v in row] for row in eff.tolist()],
                             "integrated_dimension":8, "integrated_determinant":str(determinant),
                             "integrated_signature":int(sig),
                             "cuts":[sewn(mask, cut) for cut in CUTS]}
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if not __debug__:
        raise RuntimeError("Keep assertions enabled")
    args.output.write_text(json.dumps(run(),indent=2,sort_keys=True)+"\n")
