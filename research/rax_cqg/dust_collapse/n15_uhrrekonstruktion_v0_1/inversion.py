"""Readouts on N15 type 375841 in Y=T/Delta and W=w/Delta units.

Only measured quantities and visible coordinates enter the public functions.
"""
from fractions import Fraction as Q
from math import isqrt

P = (0, 1, 2, 3)
F = (7, 8, 9, 10)
SEAM = (5, 11)
CHAINS = ((4, 5, 14), (6, 11, 12, 13))
INNER = tuple(sorted(v for chain in CHAINS for v in chain))
BY_DEPTH = ((4,6), (5,11), (12,14), (13,))
BY_SUCCESSORS = ((13,14), (5,12), (4,11), (6,))
LAYERS = (1, -9, 16, -8)


def b_at(n):
    return LAYERS[n] if n < 4 else 0


def within_chain(i, j):
    for chain in CHAINS:
        if i in chain and j in chain and chain.index(i) < chain.index(j):
            return b_at(chain.index(j) - chain.index(i) - 1)
    return 0


def from_p(i, j):
    depth = next(d for d, group in enumerate(BY_DEPTH) if j in group)
    return b_at(3-i+depth)


def to_f(i, j):
    successors = next(d for d, group in enumerate(BY_SUCCESSORS) if i in group)
    return b_at(successors+F.index(j))


def future_link(i,j):
    return b_at(j-i-1) if i < j else 0


def future_sums(y, w, slopes):
    # Targets 10,9,8 give a triangular system for successor classes 0,1,2.
    sums = []
    for f in reversed(F[1:]):
        incoming = sum(future_link(g,f)*(y[g]-y[f]) for g in F)
        outgoing = sum(future_link(f,g)*w[g]*(y[f]-y[g]) for g in F)
        row = [b_at(F.index(f)+d) for d in range(4)]
        moment = ((19*slopes[f]+outgoing)/w[f] - incoming
                  + y[f]*sum(c*len(group) for c,group in zip(row,BY_SUCCESSORS)))
        assert row[len(sums)] == -8
        sums.append((moment - sum(c*t for c,t in zip(row,sums)))/(-8))
    return tuple(sums)


def exact_root(q):
    if q < 0:
        raise ValueError('Negative squared distance.')
    n,d = isqrt(q.numerator), isqrt(q.denominator)
    if n*n != q.numerator or d*d != q.denominator:
        raise ValueError('This exact rational implementation requires a rational root.')
    return Q(n,d)


def clocks_from_future(y, w, slopes, density_slopes):
    """Return all five hidden clocks using three clock and two density responses."""
    t0,t1,t2 = future_sums(y,w,slopes)
    clocks = dict(y)
    clocks[4], clocks[12] = t2-y[11], t1-y[5]
    def second_moment(f):
        known = sum(future_link(g,f)*(y[g]-y[f])**2 for g in F)
        return -38*density_slopes[f]-19-known
    split = exact_root(2*second_moment(10)/(-8)-(t0-2*y[10])**2)
    clocks[13],clocks[14] = (t0+split)/2, (t0-split)/2
    rest = sum(to_f(j,7)*(clocks[j]-y[7])**2 for j in INNER if j!=6)
    clocks[6] = y[7]-exact_root((second_moment(7)-rest)/(-8))
    return {j:clocks[j] for j in (4,6,12,13,14)}


def outgoing_density(s, w, curvature):
    incoming = sum(from_p(i,s) for i in P) + sum(within_chain(i,s) for i in INNER)
    return -19*curvature-incoming*w[s]-sum(to_f(s,j)*w[j] for j in F)


def seam_future(s, y, w):
    return sum(to_f(s,j)*w[j]*(y[s]-y[j]) for j in F)


def clock_only(y, w, slopes, total, early, e5, h5, h11):
    """Predict p without E11, without any hidden clock or any density source."""
    t0,t1,t2 = future_sums(y,w,slopes)
    yc = dict(y)
    yc[4],yc[12] = t2-y[11],t1-y[5]
    w14 = outgoing_density(5,w,h5)
    if w14 <= 0:
        raise ValueError('The preparation requires a positive terminal density.')
    l11 = outgoing_density(11,w,h11)
    mass12and13 = total-early-w[5]-w[11]-w14
    w13 = (mass12and13-l11)/10
    w12 = mass12and13-w13
    incoming5 = w[5]*(sum(from_p(i,5)*(y[i]-y[5]) for i in P) + yc[4]-y[5])
    j5 = incoming5-seam_future(5,y,w)-19*e5
    yc[14] = y[5]-j5/w14
    yc[13] = t0-yc[14]
    def coefficient(j):
        return sum(from_p(i,j)*(y[i]-yc[j]) for i in P)
    p = (coefficient(4)*early + coefficient(5)*w[5] + coefficient(11)*w[11]
         + coefficient(12)*w12 + coefficient(13)*w13 + coefficient(14)*w14)/19
    return p, {j:yc[j] for j in (4,12,13,14)}, {12:w12,13:w13,14:w14}


def clock6_from_seam(y, w, e11):
    outgoing = seam_future(11,y,w) + sum(within_chain(11,j)*w[j]*(y[11]-y[j]) for j in (12,13))
    past = sum(from_p(i,11)*(y[i]-y[11]) for i in P)
    return y[11] + (19*e11+outgoing)/w[11]-past
