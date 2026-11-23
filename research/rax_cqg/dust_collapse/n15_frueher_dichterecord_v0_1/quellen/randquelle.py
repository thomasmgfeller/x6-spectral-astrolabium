"""Exterior mixed source for w11/D, and support of a past density record."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'quellen'))
from ordnung import ORDER, PAST, INNER, FUTURE, pairs_from_intervals
from intervalle import I, S
from modell import H

EDGES=pairs_from_intervals()
ETA=F(1,100)
RADIUS=F(1,64)
DELTA=I.of(F(3,722)).sqrt().sqrt()

def profile(target=11):
    v={}
    for j,i in zip(reversed(INNER[:4]),reversed(PAST)):
        known=sum(EDGES.get((k,j),0)*z for k,z in v.items())
        v[i]=(-F(j==target)-known)/EDGES[i,j]
    return {i:v[i] for i in PAST}

def fine_check():
    v=profile()
    y={i:F(k*k+5,29) for k,i in enumerate(ORDER)}
    def action(unit,u,p,t):
        ys={i:z+(u+p*v[i] if i in PAST else 0) for i,z in y.items()}
        return -F(1,2)-sum(F(b,38)*(ys[j]-ys[i]-(t if i==6 and ORDER.index(j)>ORDER.index(11) else 0))**2
                            for (i,j),b in EDGES.items() if j==unit)
    columns=[]
    for j in ORDER:
        x=-sum(b*(int(t in PAST)-int(i in PAST))*(v.get(t,0)-v.get(i,0))
               for (i,t),b in EDGES.items() if t==j)
        assert x==int(j==11)
        for step in (0,H,-H):
            a=19*sum(s*p*action(j,s*H,p*H,step) for s,p in product((-1,1),repeat=2))/(4*H**2)
            assert a==x
        columns.append(int(x))
    return {'vektor_in_reihenfolge_0_bis_3':list(map(str,v.values())), 'basisdichten':columns,'anzahl_endliche_vergleiche':45}

def support_check():
    dmin=4*DELTA-F(3,32); dmax=4*DELTA+F(3,32)
    qlo=DELTA*H/(dmax*dmax.sqrt())
    qhi=DELTA*H/(dmin*dmin.sqrt())
    lo,hi=F(qlo.lo,S),F(qhi.hi,S)
    # f_min=(a-u6)/2 <= 1/8. f_max=(b-u6)/2 <= 9/64.
    span=2*RADIUS
    # Bottom/top two thirds of the u12 interval; worst jitter in the translated band.
    plus=(1+ETA)*(lo-2*span/3)/2-2*ETA*F(1,8)
    minus=(1-ETA)*(lo-2*span/3)/2-2*ETA*F(9,64)
    assert min(plus,minus)>0
    # At fixed other clock coordinates only f11' and f13 vary with u12.
    # They vary monotonically in opposite directions by span/2. For any two
    # points, max product ratio is bounded by the larger individual ratio.
    min_factor=min(F(7,64)-hi/2,F(7,64))
    max_ratio=1+span/(2*min_factor)
    probability=2/(2+max_ratio)
    assert probability>F(63,100)
    return {'pulsversatz_in_u':[qlo.rounded(12)[0],qhi.rounded(12)[1]],
            'abstand_zum_frueheren_band_auf_je_zwei_dritteln':{'plus_mindestens':I.of(plus).rounded(12)[0],
            'minus_mindestens':I.of(minus).rounded(12)[0]},
            'untergrenze_anteil_im_positiven_verschobenen_mass':I.of(probability).rounded(12)[0]}

def run():
    return {'quelle':fine_check(),'vergangenheit':support_check()}
