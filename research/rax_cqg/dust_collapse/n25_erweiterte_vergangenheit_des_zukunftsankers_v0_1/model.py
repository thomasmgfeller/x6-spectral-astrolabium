"""Order and source conventions of PR 416, for terminal extensions."""
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EMPTY = {15, 17, 20, 22}
COLLAR = {0, 1, 2, 3, 7, 8, 9, 10}
WINDOW = (Fraction(15, 32), Fraction(17, 32))
DEVICE = {(15, 16), (16, 18), (17, 18), (18, 7)}
LAYERS = (1, -9, 16, -8, 0)


def inputs():
    pair = json.loads((ROOT / "input/Vergleichspaar.json").read_text())
    return pair, set(map(tuple, pair["relation"]))


def ideals(rel, n):
    topo = sorted(range(n), key=lambda v: sum(j == v for i, j in rel))
    result = [frozenset()]
    for node in topo:
        past = {i for i, j in rel if j == node}
        result += [p | {node} for p in result if past <= p]
    return sorted(result, key=lambda p: (len(p), sorted(p)))


def coefficients(rel, n):
    return {(i, j): LAYERS[min(4, sum((i, h) in rel and (h, j) in rel
                                      for h in range(n)))]
            - Fraction((i, j) in DEVICE, 10**11) for i, j in rel}



def cases(rel, extra_count=1):
    """Form every chain of three old ideals for a fixed number of extra ancestors of 24."""
    pasts = ideals(rel, 22)
    for partner in (18, 19):
        principal = {partner} | {i for i, j in rel if j == partner}
        for last in pasts:
            if not principal <= last or len(last) != len(principal) + extra_count:
                continue
            extra = tuple(sorted(last - principal))
            for middle in pasts:
                if not middle <= last:
                    continue
                for first in pasts:
                    if not first or partner in first or not first <= middle:
                        continue
                    ext = rel | {(22, 23), (22, 24), (23, 24)}
                    for node, ancestors in ((22, first), (23, middle), (24, last)):
                        ext.update((i, node) for i in ancestors)
                    yield partner, extra, first, middle, last, ext


def boundary_hull(pair):
    """Enclose both actual collar preparations coordinate by coordinate."""
    bounds = {}
    for i in COLLAR:
        intervals = [list(map(Fraction, pair[side]["clock_box"][i])) for side in ("heavy", "light")]
        bounds[i] = [min(v[0] for v in intervals), max(v[1] for v in intervals)]
    return {"clock_box": bounds}
