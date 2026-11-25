"""Exact certificates for midpoint-cell capacities on a synchronized finite cut."""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from math import isqrt
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
I = (4, 5, 6, 11, 12, 13, 14)
PAST = (0, 1, 2, 3)
FUTURE = (7, 8, 9, 10)
MASSES = (Q(1, 4), Q(1), Q(4))
WINDOWS = ((Q(-3,32), Q(-1,32)), (Q(1,32), Q(3,32)))
# Delta^4 = 3/722 follows from beta=4/sqrt(6), Delta^2=2/(19 beta).
UNIT = 10**18
floor_delta = isqrt(isqrt(3 * UNIT**4 // 722))
DELTA = (Q(floor_delta, UNIT), Q(floor_delta+1, UNIT))
assert DELTA[0]**4 <= Q(3,722) < DELTA[1]**4


def catalogue():
    data = json.loads((HERE / "inputs/catalog.json").read_text())
    return sorted(int(k) for k, (a, _, b) in data["ranks_pure_free_mixed"].items()
                  if a == b == 0)


def geometry(code):
    rel = set(combinations(PAST, 2)) | set(combinations(FUTURE, 2))
    rel.update(product(PAST, I+FUTURE))
    rel.update(product(I, FUTURE))
    rel.update(edge for bit, edge in enumerate(combinations(I, 2)) if code & (1 << bit))
    return I, rel


def paths_and_edges(rel):
    nodes = (3,) + I + (7,)
    covers = [(a,b) for a,b in rel if a in nodes and b in nodes and
              not any((a,c) in rel and (c,b) in rel for c in nodes)]
    paths = []
    def visit(path):
        if path[-1] == 7:
            paths.append(tuple(path[1:-1]))
        else:
            for a,b in sorted(covers):
                if a == path[-1]:
                    visit(path+[b])
    visit([3])
    assert set().union(*map(set, paths)) == set(I) and all(paths)
    return paths, sorted((a,b) for a,b in covers if a in I and b in I)


def fractions_on_paths(paths, u):
    total = dict.fromkeys(I, Q(0))
    for path in paths:
        cuts = [Q(0)] + [(u[a]+u[b])/2 for a,b in zip(path, path[1:])] + [Q(1)]
        for v, l, r in zip(path, cuts, cuts[1:]):
            total[v] += (r-l)/len(paths)
    return [total[v] for v in I]


def system(code):
    _, rel = geometry(code)
    paths, covers = paths_and_edges(rel)
    # Unknowns are seven normalized clock readings and the largest dwell fraction z.
    # Each affine cell length has endpoint 0, 1 or a midpoint of consecutive events.
    rows, rhs = [], []
    def append(terms, right):
        row = [Q(0)] * 8
        for j, value in terms:
            row[j] += value
        rows.append(row)
        rhs.append(Q(right))
    for i in range(7):
        append([(i,-1)],0)
        append([(i,1)],1)
    for a,b in covers:
        append([(I.index(a),1), (I.index(b),-1)],0)
    for v in I:
        constant = 0
        terms = []
        for path in paths:
            if v not in path:
                continue
            i = path.index(v)
            for sign, neighbor in [(1,i+1),(-1,i-1)]:
                if 0 <= neighbor < len(path):
                    terms.extend([(I.index(v), Q(sign,2*len(paths))),
                                  (I.index(path[neighbor]), Q(sign,2*len(paths)))])
                elif sign == 1:
                    constant += Q(1,len(paths))
        append([*terms,(7,-1)],-constant)
    return paths, rows, rhs


def dot(a,b):
    return sum((x*y for x,y in zip(a,b) if x and y), Q(0))


def verify(code, cert):
    paths, rows, rhs = system(code)
    x = tuple(map(Q, cert["primal"]))
    y = dict((int(i), Q(value)) for i,value in cert["dual"].items())
    assert len(x) == 8 and all(0 <= i < len(rhs) and w <= 0 for i,w in y.items())
    assert all(dot(row,x) <= b for row,b in zip(rows,rhs))
    for j in range(8):
        assert sum(rows[i][j]*w for i,w in y.items()) == (j == 7)
    assert sum(rhs[i]*w for i,w in y.items()) == x[7]
    # Direct dwell evaluation at strict interior clocks, independent of the affine rows.
    witness = {v:Q(i+1,8) for i,v in enumerate(I)}
    f = fractions_on_paths(paths,witness)
    assert sum(f) == 1 and min(f) > 0
    assert [dot(row[:7],witness.values())-b for row,b in zip(rows[-7:],rhs[-7:])] == f
    return x[7]


def open_at(m, offset, optimum):
    # Strict capacity. All archived comparisons separate from equality.
    low, high = [m * (4*d-offset) * optimum for d in DELTA]
    assert high < 1 or low > 1
    return high < 1


def statuses(optimum):
    data = {}
    for m in MASSES:
        lobes = []
        for left,right in WINDOWS:
            a,b = [open_at(m,d,optimum) for d in (left,right)]
            lobes.append("all" if a else "partial" if b else "empty")
        whole = ("all" if lobes == ["all","all"] else
                 "empty" if lobes == ["empty","empty"] else "partial")
        data[str(m)] = {"lobes":lobes, "packet":whole}
    return data


def summarize(certs):
    types = catalogue()
    assert len(types) == 1048 and set(map(str,types)) == set(certs)
    counts = {str(m):Counter() for m in MASSES}
    lobe_counts = {str(m):Counter() for m in MASSES}
    optima = Counter()
    for code in types:
        opt = verify(code,certs[str(code)])
        optima[str(opt)] += 1
        observed = statuses(opt)
        assert certs[str(code)]["support"] == observed
        for m, status in observed.items():
            counts[m][status["packet"]] += 1
            lobe_counts[m]["/".join(status["lobes"])] += 1
    return {"types":len(types),"packet_counts":counts,"lobe_counts":lobe_counts,
            "minimax_dwell_fraction_histogram":optima}
