"""Necessary clock enclosures from all causal roots of the seven dust density equations."""
from functools import lru_cache

DUST_ORDER = (4, 5, 6, 11, 12, 13, 14)
SCALE = 10**9


@lru_cache(maxsize=None)
def enclose(old_bounds, stages):
    # All quantities below are integers. A quadratic residual is in units of SCALE^-2.
    bounds = dict(old_bounds)
    proofs = {}
    for j, predecessors, successors, incoming in stages:
        low = max(bounds[i][0] for i in predecessors)
        high = min(bounds[i][1] for i in successors)
        assert low < high
        pending = [(low, high)]
        leaves = []
        contradicted = 0
        while pending:
            left, right = pending.pop()
            dlo = dhi = 19 * SCALE**2
            for i, c in incoming:
                # Every true gap on an incoming edge is positive.
                gap_lo = max(0, left - bounds[i][1])
                gap_hi = max(0, right - bounds[i][0])
                a, b = c * gap_lo**2, c * gap_hi**2
                dlo += min(a, b)
                dhi += max(a, b)
            if dlo > 0 or dhi < 0:
                contradicted += 1
            elif right - left <= 16:
                leaves.append((left, right))
            else:
                mid = (left + right) // 2
                pending.extend(((left, mid), (mid, right)))
        assert leaves
        bounds[j] = min(a for a, b in leaves), max(b for a, b in leaves)
        proofs[j] = dict(initial=(low, high), enclosure=bounds[j],
                         residual_zero_possible=len(leaves), discarded=contradicted)
    return proofs


def dust_clocks(collar, edges, coefficients):
    known = set(collar)
    stages = []
    for j in DUST_ORDER:
        predecessors = tuple(sorted(a for a, b in edges if b == j))
        assert predecessors and set(predecessors) <= known
        successors = tuple(sorted(b for a, b in edges if a == j and b in known))
        assert successors
        incoming = tuple(sorted((i, c) for (i, b), c in coefficients.items() if b == j))
        stages.append((j, predecessors, successors, incoming))
        known.add(j)
    old_bounds = tuple(sorted((j, tuple(v[:2])) for j, v in collar.items()))
    return enclose(old_bounds, tuple(stages))
