"""Finite action, cut geometry, and complete algebraic controls."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'quellen'))
from ordnung import ORDER, INNER, PAST, FUTURE, pairs_from_intervals

EDGES = pairs_from_intervals()
EPS = F(1, 512)
H = F(1, 8)
NARROW = F(1, 16384)
INNER_MEANS = [F(j, 8) for j in range(1, 8)]
PACKET_MEANS = INNER_MEANS.copy()
PACKET_MEANS[2] += F(1, 128)
CUT = ORDER.index(11) + 1
OLDEST = ORDER[CUT - 4]
TARGET = ORDER[CUT]
B = EDGES[OLDEST, TARGET]


def dwell(u):
    faces = [0] + [(u[i] + u[i + 1]) / 2 for i in range(6)] + [1]
    return {j: faces[i + 1] - faces[i] for i, j in enumerate(INNER)}


def clocks(e, u):
    y = {j: j - 5 for j in PAST + FUTURE}
    y[3] += e
    y.update({j: y[3] + (4 - e) * u[i] for i, j in enumerate(INNER)})
    return y


def split_action(y,w,translation):
    pieces = []
    for region, segment in enumerate((ORDER[:CUT], ORDER[CUT:])):
        v = dict(y)
        if region == 1:
            v[OLDEST] += translation
        partial = -sum(w[j] for j in segment) / 2
        for (i,j), b in EDGES.items():
            if j in segment:
                partial -= F(b,38)*w[j]*(v[j]-v[i])**2
        pieces.append(partial)
    return sum(pieces)


def coefficients(y):
    c = dict.fromkeys(ORDER,F(-1,2))
    for (i,j),b in EDGES.items():
        c[j] -= F(b,38)*(y[j]-y[i])**2
    return c


def link_change(gap, step):
    return F(B,38)*(2*gap*step-step**2)


def exact_checks():
    crossing = [(i,j) for (i,j) in EDGES if i==OLDEST and j in ORDER[CUT:]]
    assert crossing==[(4,12)] and B==-8
    # In units of S/D the exterior densities may take any identical values.
    u=PACKET_MEANS; y=clocks(F(1,4),u); f=dwell(u); c=coefficients(y)
    data={}
    for label,(j,k) in {'original':(12,13), 'complement':(13,14)}.items():
        weights=[]
        for sign in (-1,1):
            x=dict.fromkeys(ORDER,F(1,8)); x.update(f)
            x[j]+=sign*EPS*c[k]; x[k]-=sign*EPS*c[j]
            assert all(abs(x[i]/f[i]-1)<F(1,100) for i in INNER)
            weights.append(x)
        assert split_action(y,weights[0],0)==split_action(y,weights[1],0)
        assert all(i in INNER for (i,t) in EDGES if t in (j,k))
        dx={i:weights[1][i]-weights[0][i] for i in INNER}
        for step in (-F(1,5), H, F(2,7)):
            changed=[split_action(y,w,step) for w in weights]
            assert changed[1]-changed[0]==dx[12]*link_change(y[12]-y[4],step)
            for w,z in zip(weights,changed):
                assert z-split_action(y,w,0)==w[TARGET]*link_change(y[TARGET]-y[OLDEST],step)
        assert sum(dx.values()) and dx[13]
        assert (dx[12]!=0)==(label=='original')
        data[label]={'difference_sum_w_over_D':sum(dx.values()),'difference_9w13_over_D':9*dx[13], 'difference_w12_over_D':dx[12]}
    # Basis checks include every density and both signs of the shift; no factor fitted.
    direct_edges=tuple((ORDER[t-d],ORDER[t],(1,-9,16,-8)[d-1]) for t in range(1,15) for d in range(1,min(4,t)+1))
    assert len(direct_edges)==len(EDGES)==50
    for j in ORDER:
        w={v:F(v==j) for v in ORDER}
        for step in (-H,H):
            new=-sum(w.values())/2
            for i,t,b in direct_edges:
                lag=y[t]-y[i]-(step if i==4 and t==12 else 0)
                new-=F(b,38)*w[t]*lag**2
            assert new==split_action(y,w,step)
    return {'cut_after':11,'memory':list(ORDER[CUT-4:CUT]),'affected_edge':crossing,'coefficient':B,'basis_checks':30,'witnesses':data}
