"""Independent finite-order audit and full-action quadrature at the packet centres."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json
import sys


# In the standalone archive the frozen old packet definition lives here.
sys.path.insert(0, str(Path(__file__).resolve().parent / 'basis' / 'port'))
import zertifikat as prior

P = (0, 1, 2, 3)
SHORT = (4, 5, 14)
LONG = (6, 11, 12, 13)
F = (7, 8, 9, 10)
V = tuple(range(16))
N = 15
CASES = {'kurzes_ideal': frozenset(P + LONG[:1]), 'stromerhaltendes_ideal': frozenset(P + LONG),
         'vollideal': frozenset(range(15))}
LAYER = (1, -9, 16, -8)


def old_order():
    return {pair for chain in (P + SHORT + F, P + LONG + F) for pair in combinations(chain, 2)}


def add_event(ideal):
    return old_order() | {(i, N) for i in ideal}


def coefficients(nodes, order):
    pred = {i: {k for k, j in order if i == j} for i in nodes}
    succ = {i: {k for j, k in order if i == j} for i in nodes}
    return {(i,j): LAYER[count] for i,j in order
            if (count := len(succ[i] & pred[j])) < len(LAYER)}


def schedules(nodes, order):
    pred = {j: {i for i,k in order if k == j} for j in nodes}
    def extensions(prefix, available):
        if not available:
            yield prefix
        for j in sorted(available):
            if not available.intersection(pred[j]):
                yield from extensions(prefix + (j,), available - {j})
    yield from extensions((), frozenset(nodes))


def slopes(b, y):
    unit = next(iter(y.values()))*0 + 1
    return {j: -unit/2 - sum((v * (y[i] - y[j])**2 for (i,k),v in b.items() if k == j),unit*0)/38
            for j in y}


def rational_geometry():
    before = old_order()
    assert before == prior.ORDER
    ideals = set()
    for mask in range(1 << 15):
        if all(not (mask >> j & 1) or (mask >> i & 1) for i,j in before):
            ideals.add(frozenset(i for i in range(15) if mask >> i & 1))
    hist = {v: 0 for v in (0,) + LAYER}
    no_charge_term = 0
    for ideal in ideals:
        b = coefficients(V, add_event(ideal))
        t = b.get((6,N),0)
        hist[t] += 1
        if t and all((j,N) not in b for j in P):
            no_charge_term += 1
    assert hist == {0:12,1:4,-9:4,16:4,-8:4} and no_charge_term == 10
    pair, _ = prior.centers()
    neutral = {i:(pair['negativ'][0][i]+pair['positiv'][0][i])/2 for i in range(15)}
    neutral[N] = neutral[F[0]] + 4
    assert neutral[N] == 6
    cases = {}
    for name, ideal in CASES.items():
        e = add_event(ideal)
        b = coefficients(V,e)
        starts = {i:q for (i,j),q in b.items() if j == N}
        dref = slopes(b,neutral)[N]
        cents = {}
        for sign,(y,w) in pair.items():
            yc = y | {N:neutral[N]}
            d = slopes(b,yc)[N]
            p = prior.current({j:prior.box(v) for j,v in y.items()},
                              {j:prior.box(v) for j,v in w.items()})[0]
            p_per_w = sum(q*(yc[i]-yc[N]) for i,q in starts.items() if i in P)/Q(19)
            # Signed central difference is exact for this quadratic action.
            # Check p=-dS_hat/dlambda for a common shift of all four input clocks.
            test_density, step = Q(5,13), Q(1,67)
            for edges, clocks, densities, target in (
                    (coefficients(tuple(range(15)),before), y, w, p),
                    (b, yc, w | {N:test_density}, p+test_density*p_per_w)):
                def shifted_action(dx):
                    shifted = {j:t+(dx if j in P else 0) for j,t in clocks.items()}
                    c = slopes(edges,shifted)
                    return sum(densities[j]*c[j] for j in shifted)
                assert (shifted_action(-step)-shifted_action(step))/(2*step) == target
            cents[sign] = {'D_n':str(d),'p_P_N15':str(p),'Delta_p_P_pro_W_n':str(p_per_w)}
        verified = late = 0
        for seq in schedules(V,e):
            labels = {j:997-19*k for k,j in enumerate(seq)}
            # Distinct labels, with opposite numerical orientation to birth order.
            ee = {(labels[i],labels[j]) for i,j in e}
            out = labels[N]
            y_renamed = {labels[i]:v+Q(3,7) for i,v in neutral.items()}
            aa = coefficients(tuple(labels.values()),ee)
            assert { (labels[i],labels[j]):q for (i,j),q in b.items()} == aa
            assert slopes(aa,y_renamed)[out] == dref
            verified += 1
            late += seq[-1] == N
        assert late == 35
        cases[name] = {'koeffizienten_neues_ziel':starts,'D_stern':str(dref),'zentren':cents,
                       'transportierte_lineare_erweiterungen_des_markierten_posets':verified,
                       'davon_mit_n_zuletzt':late}
    return {'anzahl_ideale':len(ideals),'b_6n_haeufigkeit':hist,
            'wirksames_Y6_und_keine_direkte_Eingangskopplung':no_charge_term,'faelle':cases}


def real(q):
    r = Q(q)
    return mp.mpf(r.numerator)/r.denominator


def gauss(n):
    x,w = mp.gauss_quadrature(n,'legendre')
    return list(zip(x,[u/2 for u in w]))


def numeric(precision, structural):
    with mp.workdps(precision):
        mid = real(Q(1,8))
        h = real(prior.H)
        delta = (mp.mpf(3)/722)**(mp.mpf(1)/4)
        # Complete old entrance-density window and old seam, and both new ports.
        gr = gauss(12)
        gw = gauss(8)
        gv = gauss(8)
        pair,_ = prior.centers()
        rows = []
        for name,J in CASES.items():
            full_b = coefficients(V,add_event(J))
            dref = real(structural['faelle'][name]['D_stern'])
            ref = mp.exp(-mp.j*h*dref)
            for z in (Q(0),Q(1,3),Q(-3,5)):
                p = {}
                max_sewing = mp.mpf(0)
                for s,(yc,wc) in pair.items():
                    y = {i:real(v) for i,v in yc.items()}
                    for j in F[1:]:
                        y[j] += h*real(z)
                    y[N] = y[F[0]]+4
                    w = {i:delta*real(wc[i]) for i in SHORT+LONG}
                    for j in F[1:]:
                        w[j] = mid+h*real(z)
                    # Recount on the old order independently for the composed answer.
                    old_c = slopes(coefficients(tuple(range(15)),old_order()),{j:v for j,v in y.items() if j!=N})
                    det = {j:-mp.mpf('0.5') for j in V}
                    for (i,j),b in full_b.items():
                        det[j] -= b*(y[i]-y[j])**2/38
                    old_fixed = sum(w[j]*old_c[j] for j in w)
                    fixed = sum(w[j]*det[j] for j in w)
                    rp = sum(det[i] for i in P)
                    # Evaluate the actual complete N16 phase at both old integration
                    # coordinates. The new density is varied before integrating.
                    phs = [(qr*qw, fixed+(mid+x/32)*rp+(mid+h*t)*det[7])
                           for x,qr in gr for t,qw in gw]
                    old = sum(qr*qw*mp.exp(mp.j*(old_fixed+(mid+x/32)*sum(old_c[i] for i in P)
                                             +(mid+h*t)*old_c[7])) for x,qr in gr for t,qw in gw)
                    numerator = norm = mp.mpf(0)
                    for u,weight in gv:
                        bra = []
                        for k in (-1,1):
                            v = mid+h*(u+k)/2
                            full = sum(q*mp.exp(mp.j*(phase+v*det[N])) for q,phase in phs)
                            sewn = old*mp.exp(mp.j*v*det[N])
                            max_sewing = max(max_sewing,abs(full-sewn))
                            bra.append(full)
                        lo,hi = bra
                        diagonal = abs(lo)**2+abs(hi)**2
                        numerator += weight*mp.im(mp.conj(lo)*ref*hi)
                        norm += weight*diagonal
                    p[s] = mp.mpf('0.5') + numerator/norm
                    oracle = (1+mp.sin(h*(det[N]-dref)))/2
                    assert abs(p[s]-oracle)<mp.mpf('1e-48')
                contrast = p['positiv']-p['negativ']
                assert max_sewing < mp.mpf('1e-48')
                zero = abs(contrast)<mp.mpf('1e-48')
                assert zero == (name == 'vollideal')
                # Normalised two-arm instrument, including its interference term.
                rows.append({'fall':name,'z':str(z),'P_plus_minus_halb':mp.nstr(p['positiv']-mp.mpf('0.5'),22),
                             'P_minus_minus_halb':mp.nstr(p['negativ']-mp.mpf('0.5'),22),
                             'P_plus_minus_P_minus':('Betrag < 1e-48' if zero else mp.nstr(contrast,22))})
        return {'praezision_dezimalstellen':precision,'quadratur_r_w7_neue_halbfenster':[12,8,8],
                'maximale_abweichung_direkt_gegen_verklebung':'< 1e-48',
                'maximale_abweichung_direkter_kreuzterm_gegen_sinus':'< 1e-48','belegungen':rows}


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Ohne -O ausführen.')
    geom = rational_geometry()
    if sys.argv[1:] == ['--struktur']:
        print(json.dumps(geom, indent=2, ensure_ascii=False))
    elif not sys.argv[1:]:
        import mpmath as mp
        print(json.dumps({'struktur': geom, 'quadraturen': [numeric(d, geom) for d in (60, 85)]},
                         indent=2, ensure_ascii=False))
    else:
        raise SystemExit('Zulässig ist --struktur oder der Aufruf ohne Argumente.')
