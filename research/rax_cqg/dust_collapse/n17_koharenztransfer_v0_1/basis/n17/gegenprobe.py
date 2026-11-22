"""Independent Hasse reconstruction, complex Schur elimination and center quadrature.

Optional dependencies: SymPy and mpmath. Exact matrix checks; empirical center
checks are diagnostic and are not the proof of the whole-packet bounds.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import sys

import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'basis'))
from pakettest import packet_family  # shared packet definition only
from zertifikat import STEP

P=(0,1,2,3)
I=(4,5,6,11,12,13,14)
F=(7,8,9,10)
CHAIN_A=(4,5,14)
CHAIN_B=(6,11,12,13)
LAYER=(1,-9,16,-8)
N=17


def rebuild(name):
    links=set()
    for path in (P+CHAIN_A+F,P+CHAIN_B+F):
        links.update(zip(path,path[1:]))
    parent={'minimal':6,'stromerhaltend':13,'abgeschirmt':10}[name]
    links.add((parent,15))
    links.add((15,16))
    if name != 'abgeschirmt':
        links.add((10,16))
    future={i:{j for a,j in links if a==i} for i in range(N)}
    for v in range(N):
        for i in range(N):
            if v in future[i]:
                future[i] |= future[v]
    past={j:{i for i in range(N) if j in future[i]} for j in range(N)}
    coeff={(i,j):LAYER[k] for i in range(N) for j in future[i]
           if (k:=len(future[i]&past[j]))<4}
    assert past[16]==set(range(16))
    # Lower and upper baseline closure represented without assuming numeric time order.
    assert not any(i in future[i] for i in range(N))
    return coeff


def complex_schur(weights):
    transform=sp.zeros(N)
    for i in range(3):
        transform[P[i+1],i]=1
        transform[F[i],3+i]=1
    for i,j in enumerate(I):
        transform[j,6+i]=1
    bm=(-46,-32,-16,0)
    am=(-128,241,119,-232)
    for i in range(4):
        transform[P[i],13]=bm[i]
        transform[F[i],14]=-bm[3-i]
    transform[15,15]=transform[16,16]=1
    raw=sp.zeros(N)
    for (i,j),b in weights.items():
        for u,s in [(i,1),(j,-1)]:
            for v,t in [(i,1),(j,-1)]:
                raw[u,v]-=sp.Rational(b*s*t,2)
    g=transform.T*raw*transform
    # The canonical incoming/outgoing phases in the frozen H3 frame.
    for j in range(3):
        g[13,j]-=am[j+1]; g[j,13]-=am[j+1]
        g[14,3+j]+=am[3-j]; g[3+j,14]+=am[3-j]
    g[13,13]-=sum(a*b for a,b in zip(am,bm))
    g[14,14]-=sum(a*b for a,b in zip(am,bm))
    precision=sp.diag(*([1]*6+[0]*11))-sp.I*g
    inv=precision[:15,:15].inv(method='DM')
    effective=(precision[15:,15:]-precision[15:,:15]*inv*precision[:15,15:]).applyfunc(sp.cancel)
    return str(g[6:15,6:15].det(method='domain-ge')), effective


def quad_case(name, weights, deformed, precision, order):
    with mp.workdps(precision):
        def real(v):
            q=Q(v)
            return mp.mpf(q.numerator)/q.denominator

        mid=real(Q(1,8)); h=real(Q(1,2**20))
        delta=(mp.mpf(3)/722)**(mp.mpf(1)/4)
        neutral,family=packet_family(deformed)
        xs,ws=mp.gauss_quadrature(order,'legendre')
        cells=[(x,w/2) for x,w in zip(xs,ws)]
        def mean_phase(slope,m,r):
            return mp.expj(slope*m)*mp.sinc(slope*r)

        def slopes(y):
            out=[mp.mpf('-0.5') for _ in range(N)]
            for (i,j),w in weights.items():
                out[j]-=w*(y[i]-y[j])**2/38
            return out
        nr=[real(neutral[i]) for i in range(15)]+[mp.mpf(6),mp.mpf(7)]
        dref=slopes(nr)[15]
        ts=(mid-h,mid,mid+h)
        closed,kept={},{}
        for sign,(y0,w0) in family.items():
            acc=[mp.mpc(0) for _ in ts]; low=mp.mpc(0); high=mp.mpc(0)
            for cs in product(cells,repeat=3):
                y=[real(y0[i]) for i in range(15)]+[mp.mpf(6),mp.mpf(7)]
                for j,(x,_) in zip(F[1:],cs):
                    y[j]+=h*x
                d=slopes(y)
                g=mp.fprod(w for _,w in cs)*mp.expj(delta*sum(real(w0[i])*d[i] for i in I))
                g*=mean_phase(sum(d[i] for i in P),mid,real(Q(1,32)))
                g*=mp.fprod(mean_phase(d[i],mid,h) for i in F)
                for a,t in enumerate(ts):
                    acc[a]+=g*mp.expj(t*d[16])*mean_phase(d[15],mid,h)
                low+=g*mp.expj(mid*d[16]+(mid-h/2)*d[15])
                high+=g*mp.expj(mid*d[16]+(mid+h/2)*d[15])
            assert min(abs(z) for z in acc)>mp.mpf('0.99')
            closed[sign]=[v/acc[1] for v in acc]
            kept[sign]=mp.mpf('.5')+mp.im(mp.expj(-h*dref)*mp.conj(low)*high)/(abs(low)**2+abs(high)**2)
        residual=max(abs(a-b) for a,b in zip(closed['positiv'],closed['negativ']))
        assert residual<mp.mpf(10)**(-precision+5)
        return residual, kept['positiv']-kept['negativ']


def main():
    manuscript=json.loads((ROOT/'ergebnis.json').read_text())
    for case,result in manuscript.items():
        weights=rebuild(case)
        assert {str(i):b for (i,j),b in weights.items() if j==16}==result['incoming_weights']
        det,eff=complex_schur(weights)
        assert det==result['scalar']['hidden_det']
        for i,j in product(range(2),repeat=2):
            assert str(sp.re(eff[i,j]))==result['scalar']['real_quadratic_over_beta'][i][j]
            assert str(-sp.im(eff[i,j]))==result['scalar']['phase_quadratic_over_beta'][i][j]
        for label,q in [('original',STEP),('transfer',STEP/2)]:
            errors=[]
            for digits,count in [(60,2),(85,3)]:
                residual,gap=quad_case(case,weights,q,digits,count)
                with mp.workdps(digits):
                    low,high=map(Q,result[label]['retained_N16_detector_signed_interval'])
                    assert mp.mpf(low.numerator)/low.denominator<gap<mp.mpf(high.numerator)/high.denominator
                errors.append(mp.nstr(residual,4))
            print(f'PASS {case} {label}: Schurblock exakt; Zentrenrest (60/85 Stellen) {errors}; Referenzport {mp.nstr(gap,10)}')


if __name__=='__main__':
    if not __debug__: raise RuntimeError('Run without -O')
    main()
