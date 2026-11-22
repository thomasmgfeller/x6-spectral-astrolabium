"""Certified local frequencies, positivity bands, and an explicit kernel witness."""
from fractions import Fraction as F
from itertools import combinations
from transport import SLOTS, EDGES, INNER, RANK, CUTS, ORDER, split_pairs
from intervalle import I, S

DELTA=I.of(F(3,722)).sqrt().sqrt()
H=F(1,8)
def hull(a,b):
    return I(a.lo,b.hi)
def absolute(v):
    assert v.lo*v.hi>0
    return v if v.lo>0 else -v

def run():
    # Original positive reference: u_j=k/8, e=1/4, M=1. Let w12=D/8*(1+v/100).
    D=DELTA*F(15,4)
    offset=DELTA/4
    assert I.of(F(1,32)).hi < offset.lo <= offset.hi < I.of(F(3,32)).lo
    rates={'0':I.of(0)}
    for slot in SLOTS:
        lag=INNER.index(12)-INNER.index(slot)
        gap=I.of(F(15,4)*F(lag,8))
        for sign, tag in ((1,'+'),(-1,'-')):
            t=sign*H/D.sqrt()
            link=F(EDGES[slot,12],38)*(2*gap*t-t*t)
            rates[str(slot)+tag] = D*link/800
    gaps = [absolute(a-b) for a,b in combinations(rates.values(),2)]
    assert min(g.lo for g in gaps)>0
    lam = absolute(rates['4+'])
    assert lam.hi < S//10
    # Normalized packet sqrt(3)*v times the cancelling free phase. |A| =
    # sqrt(3) * integral_0^1 v sin(|lambda|v)dv.
    witness = I.of(3).sqrt()*hull(lam/3-lam**3/30,lam/3)
    assert witness.lo > 0
    # Bounds for the entire positive reference support. delta u = Delta*h / D^(3/2).
    dmin = 4*DELTA - F(3,32); dmax=4*DELTA+F(3,32)
    dq=hull(DELTA*H/(dmax*dmax.sqrt()), DELTA*H/(dmin*dmin.sqrt()))
    # min disjoint gap in w11/(DM), either direction; f11 in [7/64,9/64].
    band_gap=F(99,100)*dq/2-F(2,100)*F(9,64)
    assert band_gap.lo>0 and dq.hi < I.of(F(1,16)).lo
    # Symbolically derive which old u coordinates remain in unclosed dwell factors.
    # Only cells 11 and later can depend on a coordinate not yet read.
    def faces(k):
        if k==0 or k==len(INNER):return {}
        return {INNER[k-1]:F(1,2), INNER[k]:F(1,2)}
    cells={}
    for k,j in enumerate(INNER):
        right,left=faces(k+1),faces(k)
        coeff={i:right.get(i,0)-left.get(i,0) for i in INNER}
        if any(coeff[i] for i in (12,13,14)):
            cells[str(j)]={str(i):str(coeff[i]) for i in SLOTS if coeff[i]}
    assert cells=={'11':{'6':'-1/2'},'12':{},'13':{},'14':{}}
    # At each cut keep pending density variables explicit up to their last clock argument.
    open_weights = {}
    for last in CUTS:
        pending = []
        for n,j in enumerate(INNER):
            depends = [i for i,a in faces(n+1).items() if a!=faces(n).get(i,0)]
            depends += [i for i,a in faces(n).items() if a!=faces(n+1).get(i,0)]
            if RANK[j] <= RANK[last] and any(RANK[i]>RANK[last] for i in depends):
                pending.append(j)
        open_weights[str(last)] = pending
    assert list(open_weights.values()) == [[11],[12],[13],[]]
    # At cut 12, only +/-4 need distinct left functions: 5,6 and their target
    # and weight w12 are all present. Lost y4 supplies three distinct frequencies.
    sep12 = absolute(F(-2*EDGES[4,12],38)*(D/8)*(H/D.sqrt())*F(15,4*64))
    assert sep12.lo>0
    for i in (5,6):
        past, ahead = split_pairs(i,12)
        assert all(j in open_weights['12'] for _,j,_ in past)
        assert i in ORDER[RANK[12]-3:RANK[12]+1]
    assert all(12 not in open_weights[str(last)] for last in (13,14))
    # Seven normalized rows exp(i lambda_j v), uniform v on [-1,1].
    # A unit coefficient vector annihilates degrees 0..5. Integral Taylor
    # remainder <= |lambda_j v|^6/6!, ||v^6||_2 = 1/sqrt(13).
    largest = I.of(F(max(x.absmax() for x in rates.values()),S))
    sigma_hi = I.of(7).sqrt()*largest**6/(720*I.of(13).sqrt())
    condition_floor = (1/sigma_hi).lo//S
    assert condition_floor>10**25
    return {'offene_dichten':open_weights,
            'bedingte_mindestraenge':dict(zip(map(str,CUTS),(1,3,7,7))),
            'frequenzbetrag_u4_am_schnitt_12':sep12.rounded(14),
            'konditionszahl_untergrenze_getestete_faser':str(condition_floor),
            'frequenzen_pro_v' :{k:v.rounded(15) for k,v in rates.items()},
            'kleinster_frequenzabstand': I(min(v.lo for v in gaps),min(v.hi for v in gaps)).rounded(15),
            'anzahl_unabhaengiger_funktionale':len(rates),'normierte_nullrichtung_betrag_4plus':witness.rounded(14),
            'normierte_verschiebung_auf_ganzem_traeger':dq.rounded(10),
            'garantierter_abstand_dichteintervalle_untergrenze':band_gap.rounded(10)[0],
            'offene_zellen_und_fruehe_koeffizienten':cells}
