"""Reference and checks shared by the independent boundary constructions."""
from fractions import Fraction as F
import json


def nominal(early):
    from gemischt import Action
    from quelle import hull
    ref=json.loads((early/'Randpraeparation.json').read_bytes())['reference']
    x=list(map(F,ref['solution_centres']))
    r=F(ref['radius'])
    return x,Action(False).fields([hull(v-r,v+r) for v in x])


def gradients(y,w):
    from gemischt import COEFF
    from quelle import box
    G={i:box(0) for i in y}
    D={j:box(19) for j in y}
    for (i,j),c in COEFF.items():
        gap=y[j]-y[i]
        flow=c*w[j]*gap
        G[i]+=flow
        G[j]-=flow
        D[j]+=c*gap*gap
    return G,D


def check(y,w,J=0,require_windows=True):
    from gemischt import ORDER,WINDOWS,CLOCK,WEIGHT
    from quelle import SCALE
    G,D=gradients(y,w)
    assert all(G[i].contains_zero() for i in CLOCK)
    assert all((D[j]-(J if j==16 else 0)).contains_zero() for j in WEIGHT)
    assert all(y[i].hi < y[j].lo for i,j in ORDER)
    assert all(0<w[j].lo<=w[j].hi<SCALE for j in y if j not in (15,17))
    assert all(w[j].lo==w[j].hi==0 for j in (15,17))
    passed=True
    for end in (F(2),y[7]):
        x={i:(v+F(11,6))/(end+F(11,6)) for i,v in y.items()}
        for (lo,hi),expected in zip(WINDOWS,(16,18)):
            matches=sorted(i for i,v in x.items() if w[i].hi>0 and lo*SCALE<=v.hi and v.lo<=hi*SCALE)
            inside=matches==[expected] and lo*SCALE<x[expected].lo<=x[expected].hi<hi*SCALE
            if not inside:
                assert x[expected].hi<lo*SCALE or x[expected].lo>hi*SCALE
            passed &= inside
    if require_windows:
        assert passed
    return passed
