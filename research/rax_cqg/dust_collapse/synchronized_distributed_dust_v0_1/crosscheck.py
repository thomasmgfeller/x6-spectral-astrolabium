"""Certify strict support pointwise at the four collar endpoints, independently of the minimax audit."""
import argparse
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


VERTICES = tuple(range(7))
PAIRS = tuple(combinations(VERTICES, 2))
OFFSETS = tuple(Fraction(i, 32) for i in (-3, -1, 1, 3))
RATIONAL_GRID = 100_000_000
DELTA_LO = Fraction(25_389_024_476_933, 100_000_000_000_000)
DELTA_HI = DELTA_LO + Fraction(1, 100_000_000_000_000)
assert DELTA_LO**4 < Fraction(3, 722) < DELTA_HI**4


def polytope(order):
    """Enumerate maximal pairwise-comparable subsets directly in the seven-event order."""
    comparable = {p for bit, p in enumerate(PAIRS) if order & (1 << bit)}
    chains = []
    for length in reversed(range(1, 8)):
        for candidate in combinations(VERTICES, length):
            if all(p in comparable for p in combinations(candidate, 2)):
                if not any(set(candidate).issubset(chain) for chain in chains):
                    chains.append(candidate)

    # Residence fractions are (constant + coefficients @ u) / denominator.
    denominator = 2 * len(chains)
    coefficients = np.zeros((7, 7), dtype=np.int64)
    constant = np.zeros(7, dtype=np.int64)
    for chain in chains:
        for i, event in enumerate(chain):
            if i + 1 == len(chain):
                constant[event] += 2
            else:
                coefficients[event, event] += 1
                coefficients[event, chain[i + 1]] += 1
            if i:
                coefficients[event, chain[i - 1]] -= 1
                coefficients[event, event] -= 1
    assert sum(constant) == denominator and not coefficients.sum(axis=0).any()

    # A @ u + margin <= b + dependent * cap, where cap = 1/(M D).
    eye = np.eye(7, dtype=np.int64)
    order_rows = [eye[i] - eye[j] for i, j in sorted(comparable)]
    A = np.vstack([eye, -eye, *order_rows, coefficients, -coefficients])
    b = np.concatenate([np.ones(7, dtype=np.int64), np.zeros(7 + len(order_rows), dtype=np.int64),
                        -constant, constant])
    dependent = np.zeros(len(b), dtype=np.int64)
    dependent[-14:-7] = denominator
    return A, b, dependent


def strict_support(poly, mass, offset):
    """The LP proposes witnesses. Integer and rational inequalities certify every answer."""
    A, b, dependent = poly
    cap_lo = 1 / (mass * (4 * DELTA_HI - offset))
    cap_hi = 1 / (mass * (4 * DELTA_LO - offset))
    limits = b + dependent * float((cap_lo + cap_hi) / 2)
    solution = linprog([0] * 7 + [-1], A_ub=np.column_stack([A, np.ones(len(b))]),
                       b_ub=limits, bounds=[(0, 1)] * 7 + [(None, None)], method='highs')
    if not solution.success:
        raise ArithmeticError(solution.message)
    if solution.x[-1] > 0:
        clocks = np.rint(solution.x[:-1] * RATIONAL_GRID).astype(np.int64)
        if any(n < 0 or n > RATIONAL_GRID for n in clocks):
            raise ArithmeticError('Witness outside clock box')
        residual = RATIONAL_GRID * b - A @ clocks
        for r, d in zip(residual, dependent):
            if int(r) * cap_lo.denominator + RATIONAL_GRID * int(d) * cap_lo.numerator <= 0:
                raise ArithmeticError('Uncertified strict witness')
        return True
    # Any nonnegative mixture y of rows gives the upper bound below on
    # sum(y)*margin, using the explicit bound 0 <= u <= 1 for the residual.
    y = np.maximum(0, np.rint(-solution.ineqlin.marginals * RATIONAL_GRID)).astype(np.int64)
    assert y.sum() > 0
    upper = int(y @ b - np.minimum(y @ A, 0).sum()) + int(y @ dependent) * cap_hi
    if upper > 0:
        raise ArithmeticError('Uncertified empty support')
    return False


def audit(catalog):
    ranks = json.loads(catalog.read_text())['ranks_pure_free_mixed']
    keys = sorted(int(k) for k, (pure, _, mixed) in ranks.items() if pure == mixed == 0)
    masses = [Fraction(1, 4), Fraction(1), Fraction(4)]
    patterns = {m: Counter() for m in masses}
    heavy_by_type = {}
    for order in keys:
        poly = polytope(order)
        for m in masses:
            # At fixed clocks smaller D only decreases the required density.
            if strict_support(poly, m, OFFSETS[0]):
                pattern = '1111'
            elif not strict_support(poly, m, OFFSETS[-1]):
                pattern = '0000'
            else:
                middle = [strict_support(poly, m, d) for d in OFFSETS[1:-1]]
                pattern = '0' + ''.join(str(int(s)) for s in middle) + '1'
            assert list(pattern) == sorted(pattern)
            patterns[m][pattern] += 1
            if m == 4:
                heavy_by_type[str(order)] = pattern
    return {'heavy_by_type':heavy_by_type, 'type_count': len(keys), 'increasing_delta': [str(d) for d in OFFSETS],
            'strict_support_patterns': {str(m): dict(sorted(c.items())) for m, c in patterns.items()}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('catalog', type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.catalog), indent=2))
