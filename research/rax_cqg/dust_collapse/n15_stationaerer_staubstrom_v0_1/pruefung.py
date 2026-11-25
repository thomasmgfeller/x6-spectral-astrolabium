"""Interval certificates for the positive classical interior of the frozen dust action."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json
import sys

from intervall import Box, SCALE, box

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'quellen'))
import support
import variation
from gluing import encode

I, P, FUT = support.I, support.PAST, support.FUTURE
DENSITY = F(1,8)
WINDOWS = {'links':(-F(3,8),-F(3,25)), 'rechts':(F(3,25),F(3,8))}


def model(code):
    _, relation = support.geometry(code)
    # Recompute the interval counts directly on this labelled order.
    nodes = P + I + FUT
    kernel = (1,-9,16,-8)
    edges = {}
    for i,j in relation:
        n = sum((i,v) in relation and (v,j) in relation for v in nodes)
        if n < len(kernel):
            edges[i,j] = kernel[n]
    return relation, edges


def minimal_clock(e):
    return (e.square()-4*e-2)/(2*(1+e))


def check_local_equations():
    # Larger rational windows contain the complete original physical offset divided by Delta.
    for (actual_lo,actual_hi), (lo,hi) in zip(support.WINDOWS, WINDOWS.values()):
        ends = [x/d for x in (actual_lo,actual_hi) for d in support.DELTA]
        assert lo < min(ends) and max(ends) < hi
    for side,(lo,hi) in WINDOWS.items():
        for n in range(256):
            e = Box.hull(lo+(hi-lo)*F(n,256),lo+(hi-lo)*F(n+1,256))
            # One minimal predecessor, linear equation in y; evaluate the shift y-a.
            numer = (((e+36)*e-44)*e-96)*e-8
            denom = 4*(1+e)*((17*e+18)*e-2)
            assert (numer/denom).hi < 0
            # Two incomparable minimal predecessors. Discriminant of 10 y^2 - 2H y + C.
            if side == 'links':
                disc_num = (((62*e+248)*e+313)*e+130)*e-15
                assert disc_num.hi < 0
            else:
                # C_2(a)<0 puts the two roots strictly on opposite sides of a.
                at_a_num = (((2*e+8)*e-5)*e-26)*e+3
                assert at_a_num.hi < 0


def local_witness(rel, side):
    past = {j:{i for i in I if (i,j) in rel} for j in I}
    mins = {j for j in I if not past[j]}
    for j,parents in past.items():
        if not parents or not parents <= mins:
            continue
        k = len(parents)
        if k == 1:
            return 'one_predecessor_reverses_clock', j
        if k >= 4:
            return 'no_past_collar_and_positive_squares', j
        if k == 2 and side == 'links':
            return 'fork_no_real_clock', j
        if k == 2 and not any((j,v) in rel for v in I):
            return 'terminal_fork_needs_negative_density', j
    return None


class Inconclusive(Exception):
    """This cell may need a finer offset interval."""


def exclude_cell(rel, edges, e, specialized=True):
    """Exclude every causal clock-root branch, then test the gradient equations backwards."""
    past = {j:[i for i in P+I if (i,j) in rel] for j in I}
    inputs = {j:[(i,b) for (i,v),b in edges.items() if v==j] for j in I}
    inner_past = {j:tuple(i for i in I if i in past[j]) for j in I}
    outputs = {j:[(v,b) for (i,v),b in edges.items() if i==j] for j in I}
    clocks = {0:box(-5),1:box(-4),2:box(-3),3:e-2,**{i:box(i-5) for i in FUT}}

    def densities(y, moments):
        w = dict.fromkeys(FUT,box(DENSITY))
        for j in reversed(I):
            outgoing = sum(b*w[v]*(y[v]-y[j]) for v,b in outputs[j])
            h = moments[j]
            # H*w = -outgoing. Even when division is singular it may exclude a positive density.
            residue = Box.hull(0,1)*h + outgoing
            if residue.lo > 0 or residue.hi < 0:
                return True
            if h.lo <= 0 <= h.hi:
                w[j] = Box.hull(0,1)
                continue
            solved = (-outgoing)/h
            if solved.hi <= 0 or solved.lo >= SCALE:
                return True
            w[j] = solved.intersection(Box.hull(0,1))
        return False

    def visit(n, y, moments):
        if n == len(I):
            return densities(y,moments)
        j=I[n]
        terms = inputs[j]
        degree = sum(b for _,b in terms)
        # Shift the origin to a known predecessor to reduce interval dependency.
        base = y[past[j][-1]]
        moment = sum(b*(y[i]-base) for i,b in terms)
        const = 19 + sum(b*(y[i]-base).square() for i,b in terms)
        if specialized and not inner_past[j]:
            roots = [(minimal_clock(e), 1+e)]
        elif specialized and len(inner_past[j])==2 and all(not inner_past[i] for i in inner_past[j]):
            # Within the right window only the larger root can follow its predecessors.
            assert e.lo >= box(F(3,25)).lo
            poly = (((62*e+248)*e+313)*e+130)*e-15
            if poly.hi < 0:
                return True
            half_gap = (2*poly).sqrt_nonnegative_part()/(1+e)
            center = -8 + 16*e + 2*minimal_clock(e)
            roots = [((center+half_gap)/10,-half_gap)]
        elif degree:
            rad = moment.square()-degree*const
            if rad.hi < 0:
                return True
            root = rad.sqrt_nonnegative_part()
            roots = [(base+(moment+v)/degree,-v) for v in (-root,root)]
        elif moment.lo <= 0 <= moment.hi:
            # A denominator containing zero never certifies exclusion by itself.
            possible = Box(max(y[i].lo for i in past[j]),y[7].hi)-base
            resid = const-2*moment*possible
            if resid.lo>0 or resid.hi<0:
                return True
            raise Inconclusive
        else:
            roots = [(base+const/(2*moment),moment)]
        lower = max(y[i].lo for i in past[j])
        for candidate,h in roots:
            if candidate.hi <= lower or candidate.lo >= y[7].hi:
                continue
            bounded = candidate.intersection(Box(lower,y[7].hi))
            if all(v in FUT for v,_ in outputs[j]) and h.hi<=0:
                # Original future row (1,-9,16,-8), uniform density, sum b*Y = -1.
                assert [edges.get((j,v),0) for v in FUT]==[1,-9,16,-8]
                continue
            if not visit(n+1,{**y,j:bounded},{**moments,j:h}):
                return False
        return True
    try:
        return visit(0,clocks,{})
    except Inconclusive:
        return False


def cover(rel,edges,lo,hi,depth=0,specialized=True):
    if exclude_cell(rel,edges,Box.hull(lo,hi),specialized):
        return [depth]
    if depth==20:
        raise RuntimeError("Unresolved offset interval",lo,hi)
    mid=(lo+hi)/2
    return cover(rel,edges,lo,mid,depth+1,specialized)+cover(rel,edges,mid,hi,depth+1,specialized)


def census():
    check_local_equations()
    rows = {}
    for code in support.catalogue():
        rel,edges=model(code)
        rows[code]={}
        for side,(lo,hi) in WINDOWS.items():
            witness=local_witness(rel,side)
            if witness:
                rows[code][side]={'motif':witness[0],'event':witness[1]}
            else:
                depths=Counter(cover(rel,edges,lo,hi))
                rows[code][side]={'dyadic_leaf_depths':dict(sorted(depths.items()))}
    return rows


if __name__=='__main__':
    data=census()
    print(json.dumps(data,indent=2))
