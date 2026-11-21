"""Exact envelope for every binary effect on the specified flat output Hilbert space."""
from fractions import Fraction as Q
from math import isqrt
from zertifikat import B,F,H,I,P,RADIUS,DELTA,add,box,coefs,sub


def root_interval(q):
    scale = 10**34
    i = isqrt(q.numerator*scale**2//q.denominator)
    low,high = Q(i,scale), Q(i+1,scale)
    assert low**2<=q<high**2
    return low,high


def packet_approximation(center,phase):
    y0,w0 = center
    varying = I+(3,)
    y = {j:box(y0[j],RADIUS if j in varying else H if j in F[1:] else 0) for j in y0}
    c = coefs(y)
    # At fixed external z and common entrance density, bound the total phase
    # perturbation and its signed average over the 15 independent symmetric axes.
    uniform = DELTA[1]*RADIUS*sum(max(map(abs,c[j])) for j in I)/2
    mean_bias = Q(0)
    for (i,j),b in B.items():
        n = int(i in varying)+int(j in varying)
        dy = n*RADIUS
        w = Q(5,32) if j in P else Q(1,8)+H if j in F else DELTA[1]*w0[j]
        coef = abs(b)*w/38
        uniform += coef*(2*max(map(abs,sub(y[i],y[j])))*dy+dy**2)
        mean_bias += coef*n*RADIUS**2/3
    amplitude_error = mean_bias+uniform**2/2
    norm_lower = 1-(phase[1]-phase[0])**2/8
    assert norm_lower>0
    return {'phasenabweichung_sup':uniform,'phasenmittel_betrag_max':mean_bias,
            'amplitudenfehler_max_je_paketmass':amplitude_error,
            'spurabstand_zum_normierten_zentrum_max':2*amplitude_error/norm_lower}


def compare(paired,regions):
    err = {s:packet_approximation(v,regions[s]['staubphase']) for s,v in paired.items()}
    budget = sum(e['spurabstand_zum_normierten_zentrum_max'] for e in err.values())
    pos,neg = [regions[s]['D7_zentrum_minus_referenz'] for s in ('positiv','negativ')]
    yp,wp = paired['positiv']
    yn,wn = paired['negativ']
    assert [v for v in yp if yp[v]!=yn[v]]==[6]
    assert all(B.get((6,j),0)==0 for j in F[1:])
    assert all(wp[j]==wn[j] for j in P+F)
    # At the centers the only z-dependent relative phase is (pos-neg)*w7.
    x = (pos-neg)*H
    assert 0<x<1
    sinc_low = 1-x*x/6
    sinc_high = sinc_low+x**4/120
    ideal_t = root_interval(1-sinc_high**2)[0],root_interval(1-sinc_low**2)[1]
    trace = (ideal_t[0]-budget,ideal_t[1]+budget)
    # Same port on ideal states: differences of sin(theta)/2.
    phases = pos*H,neg*H
    sine_error = sum(abs(t)**3/6 for t in phases)/2
    port = box(x/2,budget+sine_error)
    assert trace[0]>0 and port[0]>0
    ratio = port[0]/trace[1],port[1]/trace[0]
    assert Q(86,100)<ratio[0]<ratio[1]<1
    # U=exp(i*kappa*M_w7) relates the ideal states. Duhamel's bound is
    # ||U* E U-E|| <= |kappa| ||[M_w7,E]||. The actual port has norm h/2.
    kappa = pos-neg
    comm_min = (port[0]-budget)/kappa
    assert Q(99999,100000)*H/2 < comm_min <= H/2
    return {'paketfehler':err,'maximale_P_differenz_aller_binaeren_effekte':trace,
            'P_differenz_fester_port_enger':port,'anteil_am_optimum':ratio,
            'maximale_P_differenz_fuer_alle_mit_w7_kommutierenden_effekte':budget,
            'betrag_kommutator_fester_port':H/2,
            'kommutator_untergrenze_fuer_gleichen_kontrast':comm_min}
