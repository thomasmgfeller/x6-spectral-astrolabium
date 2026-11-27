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


def n25_orders(rel):
    """P22={0}, old past of 24 is the principal ideal of the partner."""
    old_ideals = ideals(rel, 22)
    for q in (18, 19):
        b = {i for i, j in rel if j == q} | {q}
        for a in old_ideals:
            if 0 in a and a <= b:
                ext = rel | {(0, 22), (22, 23), (22, 24), (23, 24)}
                ext |= {(i, 23) for i in a} | {(i, 24) for i in b}
                yield q, a, ext


def coefficients(rel, n):
    return {(i, j): LAYERS[min(4, sum((i, h) in rel and (h, j) in rel
                                      for h in range(n)))]
            - Fraction((i, j) in DEVICE, 10**11) for i, j in rel}


def minimal_anchor_orders(rel):
    """Old past of terminal 24 is exactly the principal ideal of q."""
    all_pasts = ideals(rel, 22)
    for q, a, base in n25_orders(rel):
        for p in all_pasts:
            if 0 in p and q not in p and p <= a:
                yield q, p, a, base | {(i, 22) for i in p}
