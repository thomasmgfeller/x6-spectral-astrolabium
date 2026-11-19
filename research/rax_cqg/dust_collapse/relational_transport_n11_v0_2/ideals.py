"""Cut rectangles for independent clock marks on a finite, transitively closed order."""
from itertools import product
from math import prod


def ideals(predecessors):
    n = len(predecessors)
    return [mask for mask in range(1 << n)
            if all((pred & mask)==pred for i,pred in enumerate(predecessors) if mask & (1<<i))]


def frontier(ideal, predecessors):
    return {i for i,pred in enumerate(predecessors) if not ideal & (1<<i) and pred & ideal == pred}


def cut_cell(predecessors, ideal, s, lo, hi):
    front = frontier(ideal,predecessors)
    return tuple((lo,s) if ideal & (1<<i) else (s,hi) if i in front else (lo,hi)
                 for i in range(len(predecessors)))


def intersect(a,b):
    return tuple((max(x,u),min(y,v)) for (x,y),(u,v) in zip(a,b,strict=True))


def volume(cell):
    return prod(max(0,hi-lo) for lo,hi in cell)


def paths(predecessors,cuts,lo,hi):
    options = ideals(predecessors)
    for chain in product(options,repeat=len(cuts)):
        if any(a & b != a for a,b in zip(chain,chain[1:])):
            continue
        cell = ((lo,hi),)*len(predecessors)
        for ideal,s in zip(chain,cuts,strict=True):
            cell = intersect(cell,cut_cell(predecessors,ideal,s,lo,hi))
        if volume(cell)>0:
            yield chain,cell


def minkowski_order():
    points = [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
    events = [(0,*p) for p in points]+[(3,*[-v for v in p]) for p in points]
    pred = []
    for j,(t,*x) in enumerate(events):
        mask = 0
        for i,(s,*y) in enumerate(events):
            interval = (t-s)**2-sum((a-b)**2 for a,b in zip(x,y))
            if i != j:
                assert interval != 0
            if t>s and interval>0:
                mask |= 1<<i
        pred.append(mask)
    assert pred == [0]*4+[15^(1<<k) for k in range(4)]
    return events,tuple(pred)
