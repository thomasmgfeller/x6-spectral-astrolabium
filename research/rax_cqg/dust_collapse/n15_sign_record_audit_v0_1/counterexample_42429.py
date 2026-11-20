"""Exact charge-sign counterexample in the finite N15 preparation of PR 336.

Run with Python 3.9+. Optionally supply the unpacked PR 336 study directory
to check that the primary chain witness gives this order positive weight.
All arithmetic used to decide signs or verify inequalities is rational.
"""
import argparse
import json
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path


CODE = 42429
PAST = (0, 1, 2, 3)
INNER = (4, 5, 6, 11, 12, 13, 14)
FUTURE = (7, 8, 9, 10)
MASS = Q(1, 4)
E = Q(1, 4)  # e = delta / Delta
CENTER = dict(zip(INNER, (Q(n, 5) for n in (1, 2, 1, 3, 4, 2, 3))))
PATHS = ((4, 5, 11, 12), (4, 5, 14), (4, 13), (6, 13))


def build_order():
    rel = set(combinations(PAST, 2)) | set(combinations(FUTURE, 2))
    rel.update(product(PAST, INNER + FUTURE))
    rel.update(product(INNER, FUTURE))
    rel.update(edge for bit, edge in enumerate(combinations(INNER, 2))
               if CODE & (1 << bit))
    assert all((a, d) in rel for a, b in rel for c, d in rel if b == c)
    return rel


def order_paths(rel):
    nodes = (3,) + INNER + (7,)
    covers = {(a, b) for a, b in rel if a in nodes and b in nodes
              and not any((a, c) in rel and (c, b) in rel for c in nodes)}

    def walk(path):
        if path[-1] == 7:
            yield path[1:-1]
        else:
            for a, b in sorted(covers):
                if a == path[-1]:
                    yield from walk(path + (b,))

    return tuple(walk((3,)))


def source_charge(rel, u):
    """Compute p/M by the oriented BD edge current and midpoint dwell cells."""
    paths = order_paths(rel)
    assert paths == PATHS
    height = max(map(len, paths))
    assert all(CENTER[v] == Q(max(p.index(v) + 1 for p in paths if v in p),
                              height + 1) for v in INNER)
    f = dict.fromkeys(INNER, Q(0))
    for path in paths:
        cuts = [Q(0)] + [(u[a] + u[b]) / 2 for a, b in zip(path, path[1:])] + [Q(1)]
        for v, lo, hi in zip(path, cuts, cuts[1:]):
            f[v] += (hi - lo) / len(paths)

    def bd(i, v):
        count = sum((i, k) in rel and (k, v) in rel for k in range(15))
        return (1, -9, 16, -8)[count] if count < 4 else 0

    assert all(bd(i, j) == 0 for i in PAST for j in FUTURE)
    yp = {i: i - 5 + (E if i == 3 else 0) for i in PAST}
    yi = {v: -2 + E + (4 - E) * u[v] for v in INNER}
    current = sum(f[v] * bd(i, v) * (yp[i] - yi[v]) for v in INNER for i in PAST)
    return (4 - E) * current / 19, f


def action_difference(u):
    """Reconstruct the shifted quadratic action using explicit path cells and BD rows."""
    mid = lambda a, b: (u[a] + u[b]) / 2
    a, b, c = mid(4, 5), mid(5, 11), mid(11, 12)
    h, j, k = mid(5, 14), mid(4, 13), mid(6, 13)
    # Total cell lengths over the four equally weighted paths in PATHS.
    lengths = (2*a+j, (b-a)+(h-a), k, c-b, 1-c, (1-j)+(1-k), 1-h)
    f = [length / 4 for length in lengths]
    # For an inner node with d inner predecessors, the interval cardinalities
    # from past nodes 0..3 are respectively d+3,d+2,d+1,d.
    rows = ((-8,16,-9,1), (0,-8,16,-9), (-8,16,-9,1), (0,0,-8,16),
            (0,0,0,-8), (0,0,-8,16), (0,0,-8,16))
    yp = (-5, -4, -3, -2 + E)

    def shifted(t):
        # t shifts all past clocks in units of Delta. This is the varying
        # part of S_d/(M Delta). All terms independent of t cancel.
        total = Q(0)
        for v, cell, row in zip(INNER, f, rows):
            y = -2 + E + (4 - E) * u[v]
            total += cell * sum(coef * (y - past - t)**2 for coef, past in zip(row, yp))
        return -(4 - E) * total / 38

    step = Q(1, 11)
    return (shifted(-step) - shifted(step)) / (2 * step), dict(zip(INNER, f))


def check_interior(rel, u, f):
    # Delta^4 = 3/722 and D = Delta*(4-e). Strict rational brackets suffice.
    dlo, dhi = Q(1, 4), Q(13, 50)
    assert dlo**4 < Q(3, 722) < dhi**4
    assert Q(1, 32) < E * dlo and E * dhi < Q(3, 32)
    assert all(0 < u[v] < 1 and abs(u[v] - CENTER[v]) < Q(1, 64) for v in INNER)
    assert all(u[a] < u[b] for a, b in rel if a in INNER and b in INNER)
    assert min(f.values()) > 0 and sum(f.values()) == 1
    # Both fields use the band centres w_v = M D f_v, so they are strictly
    # inside their +-1% density bands. Even the top of each band is below 1.
    assert (1 + Q(1, 100)) * MASS * dhi * (4 - E) * max(f.values()) < 1
    # Original compact raw clock box. Past, inner, future clocks are between
    # Y=-5 and Y=5, in units of Delta.
    assert 5 * dhi < Q(3, 2)


def run(study):
    if not __debug__:
        raise RuntimeError("Run without -O so all assertions are active")
    result = {"order": CODE, "marked_mass": str(MASS), "delta_over_Delta": str(E),
              "inner_event_order": INNER, "clock_center": [str(CENTER[v]) for v in INNER],
              "cases": []}
    if study is not None:
        chain = json.loads((study / "chain.json").read_text())
        weight = Q(chain["law"][str(CODE)])
        assert weight == Q(1, 10**8)
        result["primary_chain_weight"] = str(weight)
    rel = build_order()
    for delta_u, expected in ((Q(-1, 128), Q(1863, 155648)),
                              (Q(1, 128), Q(-327, 155648))):
        u = dict(CENTER)
        u[11] += delta_u
        current, cells = source_charge(rel, u)
        quotient, direct_cells = action_difference(u)
        assert cells == direct_cells
        check_interior(rel, u, cells)
        assert current == quotient == expected
        result["cases"].append({"change_u11": str(delta_u), "p_over_M": str(current),
                                "p": str(MASS * current)})
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("study", type=Path, nargs="?", help="Optional PR 336 study directory")
    run(parser.parse_args().study)
