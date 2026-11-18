"""Exact checks on the real, floating-point readout matrices of each production grid.

Interval control of the continuum clock integrals is a separate question.
"""
from fractions import Fraction
from itertools import product

import numpy as np


def check_weight_class(readout, names, base_names):
    # Treat stored binary64 values as exact rationals and symmetrize the real
    # interference matrices. Antisymmetric components vanish in w^T M w.
    rational = np.vectorize(lambda x: Fraction.from_float(float(x)), otypes=[object])
    matrix = rational(readout)
    matrix = (matrix + matrix.swapaxes(-1, -2)) / 2
    count = len(names)
    base = np.array([Fraction(1, 2) if n in base_names else Fraction(0) for n in names])
    reference = base @ matrix @ base
    delta = sum(matrix[1, :3] - matrix[0, :3])
    row_bounds = [
        delta[i, i] + sum(abs(delta[i, j]) for j in range(count) if j != i)
        for i in range(count)
    ]
    assert max(row_bounds) < 0

    # Each normalized L1 gate is a maximum over signed linear forms.
    # A single signed form >1 on a whole simplex excludes that simplex.
    difference = matrix - reference[:, :, None, None]
    forms = []
    labels = []
    signs = list(product((-1, 1), repeat=4))
    for kind, values, denominator in [
        ("level_rho_1_8", difference[0], sum(reference[0, :3]) / 5),
        ("level_rho_1_4", difference[1], sum(reference[1, :3]) / 5),
        ("density_contrast", difference[1] - difference[0],
         sum(abs(reference[1] - reference[0])) / 4),
    ]:
        for sign in signs:
            forms.append(sum(s * v for s, v in zip(sign, values)) / denominator)
            labels.append((kind, sign))

    children = [i for i, n in enumerate(names) if n not in base_names]
    identity = rational(np.eye(count))
    root = identity[children]
    stack = [("", root)]
    leaves = []
    visited = 0
    while stack:
        path, vertices = stack.pop()
        visited += 1
        # Fast witness selection only. All acceptance decisions use exact
        # fractions for the signed form that was actually selected.
        approx_v = vertices.astype(float)
        coefficients = approx_v @ np.asarray(forms, dtype=float) @ approx_v.T
        which = int(coefficients.min(axis=(1, 2)).argmax())
        lower = min((vertices @ forms[which] @ vertices.T).ravel())
        if lower > 1:
            kind, sign = labels[which]
            leaves.append({
                "path": path, "gate": kind, "outcome_signs": sign,
                "child_weight_vertices": vertices[:, children].astype(float).tolist(),
                "lower_ratio_exact": str(lower), "lower_ratio": float(lower),
            })
            continue
        if len(path) >= 12:
            raise ArithmeticError("Could not exclude this simplex at the requested depth")
        # Longest-edge bisection covers the parent exactly. Ties use row-major order.
        lengths = ((vertices[:, None] - vertices[None, :]) ** 2).sum(axis=-1)
        i, j = map(int, np.unravel_index(lengths.argmax(), lengths.shape))
        midpoint = (vertices[i] + vertices[j]) / 2
        left, right = vertices.copy(), vertices.copy()
        left[i], right[j] = midpoint, midpoint
        stack.extend([(path + "R", right), (path + "L", left)])

    return {
        "matrix_branch_order": names,
        "symmetric_delta_row_upper_bounds": list(map(float, row_bounds)),
        "max_delta_row_upper_bound_exact": str(max(row_bounds)),
        "unrestricted_children_in_order": [names[i] for i in children],
        "full_replacement_simplex_nodes_visited": visited, "excluded_simplices": leaves,
        "uniform_lower_ratio_full_replacement": min(leaf["lower_ratio"] for leaf in leaves),
    }
