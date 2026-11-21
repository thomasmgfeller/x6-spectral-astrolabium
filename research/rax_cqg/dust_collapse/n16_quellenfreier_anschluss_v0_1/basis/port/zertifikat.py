"""Exact packet and operator bounds. All intervals have rational endpoints."""
import json
from fractions import Fraction as Q
from hashlib import sha256
from math import isqrt
from pathlib import Path

from basis import density_translation_375841 as ref

ROOT = Path(__file__).resolve().parent
P, I, F = ref.PAST, ref.INNER, ref.FUTURE
ORDER, CHAINS, B = ref.local_geometry()
box, add, sub, mul, sc, square, total = (
    ref.box, ref.plus, ref.minus, ref.times, ref.scale, ref.square, ref.add_all)
H = Q(1,2**20)  # physical future half-width; bin separation
RADIUS = Q(1,2**32)
STEP = Q(1,2**24)
scale = 10**18
lo = isqrt(isqrt(3*scale**4//722))
DELTA = (Q(lo,scale), Q(lo+1,scale))
assert DELTA[0]**4 <= Q(3,722) < DELTA[1]**4


def divide(a,b):
    if b[0] <= 0 <= b[1]:
        raise ValueError('Interval contains a zero divisor.')
    return mul(a,(1/b[1],1/b[0]))


def cells(u):
    result = dict.fromkeys(I,box(0))
    for path in CHAINS:
        cuts = [box(0)] + [sc(Q(1,2),add(u[i],u[j])) for i,j in zip(path,path[1:])] + [box(1)]
        for j,l,r in zip(path,cuts,cuts[1:]):
            result[j] = add(result[j],sc(Q(1,len(CHAINS)),sub(r,l)))
    return result


def coefs(y):
    return {j:add(box(1),sc(Q(1,19),total(sc(b,square(sub(y[i],y[j])))
        for (i,k),b in B.items() if k==j and b))) for j in range(15)}


def current(y,W):
    return sc(Q(1,19),total(mul(W[j],total(sc(B[i,j],sub(y[i],y[j]))
              for i in P)) for j in I))


def centers():
    study = json.loads((ROOT/'basis/pr344_ergebnis.json').read_text())['ergaenzung_gegenpaar_gleicher_wirkung']
    assert Q(study['q'])==STEP
    e = -Q(1,4)
    u = dict(ref.CENTER)
    u[4] += Q(1,128)
    u[6] -= Q(1,128)
    y = {j:Q(j-5) for j in P+F}
    y[3] += e
    y.update({j:-2+e+(4-e)*u[j] for j in I})
    f = cells({j:box(v) for j,v in u.items()})
    x = {j:value[0] for j,value in f.items()}
    x[12] += Q(1,8320)
    x[13] -= Q(1,8320)
    w = {j:Q(1,8)/DELTA[0] for j in P+F}
    w.update({j:(4-e)*x[j]/4 for j in I})
    def action(yy,ww):
        c = coefs({j:box(v) for j,v in yy.items()})
        return -sum(ww[j]*c[j][0] for j in ww)/2
    assert current({j:box(v) for j,v in y.items()},{j:box(v) for j,v in w.items()})==box(0)
    result = {}
    for index,(label,q) in enumerate([('negativ',STEP),('positiv',-STEP)]):
        yy,ww = y.copy(),w.copy()
        yy[6] += 9*q*(y[13]-y[12])/w[11]
        ww[4] -= 10*q
        ww[12] += 9*q
        ww[13] += q
        shift = Q(study['transfer_6_nach_4'][index])
        ww[4] += shift
        ww[6] -= shift
        assert action(yy,ww)==action(y,w)
        p = current({j:box(v) for j,v in yy.items()},{j:box(v) for j,v in ww.items()})
        assert p==box(Q(study['p_fuer_plus_und_minus_q'][index]))
        result[label] = yy,ww
    reference = -coefs({j:box(v) for j,v in y.items()})[7][0]/2
    return result,reference


def whole_cell(center,reference,radius=RADIUS):
    yy,ww = center
    y = {j:box(v, radius if j in I+(3,) else H if j in F[1:] else 0) for j,v in yy.items()}
    W = {j:box(ww[j],radius) for j in I}
    assert all(y[i][1]<y[j][0] for i,j in ORDER)
    e = add(y[3],box(2))
    duration = sub(box(4),e)
    u = {j:divide(sub(add(y[j],box(2)),e),duration) for j in I}
    assert all(ref.CENTER[j]-Q(1,64)<u[j][0]<=u[j][1]<ref.CENTER[j]+Q(1,64) for j in I)
    # The physical entrance offset is Delta*e in the allowed left window.
    offset = mul(DELTA,e)
    assert -Q(3,32)<offset[0]<=offset[1]<-Q(1,32)
    fractions = cells(u)
    for j in I:
        x = divide(sc(4,W[j]),duration)
        assert Q(99,100)*fractions[j][1]<x[0]<=x[1]<Q(101,100)*fractions[j][0]
    c = coefs(y)
    source = sub(sc(-Q(1,2),c[7]),box(reference))
    theta = sc(H,source)
    p = current(y,W)
    past = mul((Q(3,32),Q(5,32)),total(c[j] for j in P))
    inner = total(mul(c[j],mul(DELTA,W[j])) for j in I)
    future = total(mul(c[j],box(Q(1,8),H)) for j in F)
    phase = sc(-Q(1,2),total((past,inner,future)))
    width = phase[1]-phase[0]
    tmax = max(map(abs,theta))
    cosine = 1-(width+tmax)**2/2
    assert cosine>Q(9,10)
    center_d = -coefs({j:box(t) for j,t in yy.items()})[7][0]/2-reference
    center_theta = H*center_d
    phase_cone = 1-width**2/8
    eps = max(abs(v-center_theta) for v in theta)/phase_cone
    assert 0 < eps < 1
    # For r=b/a, |r-exp(i*center_theta)| <= eps. Enclose Im(r)/(1+|r|²).
    sin_error = abs(center_theta)**3/6
    shift = divide(box(center_theta,eps+sin_error),(1+(1-eps)**2,1+(1+eps)**2))
    return {'p':p,'D7_minus_referenz':source,'D7_zentrum_minus_referenz':center_d,
            'staubphase':phase,'kosinus_untergrenze':cosine,'theta':theta,
            'fehler_amplitudenverhaeltnis':eps,'P_Y_plus_minus_halb':shift}


def elementary_checks():
    # Real/imaginary integer pairs. Test (2E+)²=2(2E+) on a basis.
    def twice_project(v):
        a,b,c,d=v
        return (a+d,b-c,c-b,d+a)
    for i in range(4):
        v=tuple(int(k==i) for k in range(4))
        w=twice_project(v)
        assert twice_project(w)==tuple(2*t for t in w)
        assert sum(x*y for x,y in zip(v,w))==1  # diagonal entries of E+ are 1/2
    for a,b in ((1,0),(0,1),(3,4)):
        v=(a,b,a,b)  # literal zero shift with identical reference and signal
        assert sum(x*y for x,y in zip(v,twice_project(v)))==sum(x*x for x in v)


def run():
    plan = (ROOT/'pruefvertrag.json').read_bytes()
    assert sha256(plan).hexdigest()==(ROOT/'pruefvertrag.sha256').read_text().split()[0]
    assert Q(json.loads(plan)['halbbreite'])==RADIUS
    paired,reference = centers()
    regions = {k:whole_cell(v,reference) for k,v in paired.items()}
    a,b = regions['positiv'],regions['negativ']
    for k in ('p','D7_minus_referenz','P_Y_plus_minus_halb'):
        assert a[k][0]>0>b[k][1]
    data = json.loads((ROOT/'basis/pr344_ergebnis.json').read_text())
    delta = b['D7_zentrum_minus_referenz']-a['D7_zentrum_minus_referenz']
    assert delta == Q(data['ergaenzung_gegenpaar_gleicher_wirkung']['delta_D7'])
    # One cone for both branch states at the full output, before bin folding.
    global_width = max(g['staubphase'][1] for g in regions.values())-min(g['staubphase'][0] for g in regions.values())
    assert 1-global_width**2/2>0
    elementary_checks()
    return {'typ':375841,'schritt_der_physischen_zukunftsdichte_w7':H,'halbbreite':RADIUS,
            'D_referenz':reference,'pakete':regions,'P_differenz':sub(a['P_Y_plus_minus_halb'],b['P_Y_plus_minus_halb']),
            'gemeinsamer_phasenkegel_re_kreuzterm_untere_schranke_je_quadrat_paketmass':1-global_width**2/2,
            'P_quelle_aus_und_dephasierung':Q(1,2),
            'physikalisches_randprodukt':'HOLD'}


if __name__=='__main__':
    if not __debug__: raise RuntimeError('Ohne -O ausführen.')
    print(json.dumps(run(),indent=2,default=str,ensure_ascii=False))
