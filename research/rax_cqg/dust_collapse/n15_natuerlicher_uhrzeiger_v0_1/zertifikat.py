"""Validated positive-window integrals for the pulse-free clock-5 comparison at 13."""
import argparse
import json
from fractions import Fraction as F
from math import ceil
from pruefen import ROOT, EDGES, ORDER, PAST, INNER, E, HALF, DX, X0, DELTA, check, clocks, dwell, INNER_MEANS
from intervalle import S, I, C, cis, sinc, gaussian, angle

N, RADIUS = 18, 4
K=4-E
D=K*DELTA
STOP=ORDER.index(13)
CLOSED=(4,5,6,12)


def modulus_bound():
    # Both normalized clock arguments may have complex modulus <=4.
    uerr=[F(RADIUS,64),F(3,2500)+RADIUS*HALF,0,0,0,0,0]
    y0=clocks(E,INNER_MEANS)
    yrad={j:0 for j in ORDER}
    yrad.update({j:K*err for j,err in zip(INNER,uerr)})
    f0=dwell(INNER_MEANS)
    frad={4:(uerr[0]+uerr[1])/2,5:uerr[0]/2,6:uerr[1]/2,12:0}
    exponent=F(0)
    for j in (4,5,6,11,12,13):
        cabs=F(1,2); cim=F(0)
        for (i,t),b in EDGES.items():
            if t==j:
                err=yrad[i]+yrad[j]
                upper=abs(y0[j]-y0[i])+err
                cabs+=F(abs(b),38)*upper**2
                cim+=F(abs(b),19)*upper*err
        if j in CLOSED:
            # At e=1/4, D<1. Integrate real relative density jitters.
            wabs=(f0[j]+frad[j])*F(101,100)
            wim=frad[j]*F(101,100)
            check(f0[j]+frad[j]<1,'Volumenfaktor')
        else:
            wabs=X0+DX+HALF if j==11 else F(1,8)
            wim=0
        exponent+=wabs*cim+wim*cabs
    early=sum(-F(1,2)-sum(F(b,38)*(y0[j]-y0[i])**2 for (i,end),b in EDGES.items() if end==j) for j in PAST)
    check(abs(early/32)<1,'Gemeinsamer sinc-Faktor ohne Nullstelle')
    check(D.hi<S,'Dauergrenze')
    majorant=3**ceil(exponent)
    err=4*F(majorant,RADIUS**(2*N))/(1-F(1,RADIUS))
    return exponent,majorant,err


def amplitudes(arm,err):
    grid=gaussian(N)
    s=1/(72*D*K**2)
    result={mark:C(0) for mark in (-1,1)}
    for z4,w4 in grid:
        for z5,w5 in grid:
            u=[I.of(m) for m in INNER_MEANS]
            u[0]+=z4/64
            u[1]+=arm*s+HALF*z5
            y=clocks(E,u); f=dwell(u)
            c={j:I.of(F(-1,2)) for j in INNER}
            for (i,j),b in EDGES.items():
                if j in c and ORDER.index(j)<=STOP:
                    c[j]-=F(b,38)*(y[j]-y[i])**2
            phase=D*c[13]/8
            factor=w4*w5
            for j in CLOSED:
                theta=D*c[j]*f[j]
                phase+=theta
                factor=factor*f[j]*sinc(theta/100)
            factor=factor*sinc(D*HALF*c[11])
            for mark in (-1,1):
                part=cis(phase+D*(X0+mark*DX)*c[11]).scale(factor)
                result[mark]=result[mark]+part
    return {mark:z.pad(err) for mark,z in result.items()}


def run():
    exponent,majorant,err=modulus_bound()
    a,b=amplitudes(-1,err),amplitudes(1,err)
    z={m:b[m]*a[m].conj() for m in (-1,1)}
    phase=angle(z[1]*z[-1].conj())
    bal={m:2*z[m].im/((a[m]*a[m].conj()).re+(b[m]*b[m].conj()).re) for m in (-1,1)}
    diff=bal[1]-bal[-1]
    check(phase.hi<0 and diff.hi<0,'Striktes Vorzeichen')
    return {'gauss_n':N,'complex_radius':RADIUS,'exponent_bound':str(exponent),'modulus_bound':majorant,
            'absolute_amplitude_remainder':str(err),'phase':phase.rounded(13),
            'difference_in_balance':diff.rounded(13)}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',action='store_true')
    args=p.parse_args()
    out=json.dumps(run(),indent=2)+'\n'
    if args.json:print(out,end='')
    else:
        check(out==(ROOT/'zertifikat.json').read_text(),'Archiviertes Zertifikat')
        print('PASS · Pulsfreier Ausgang durch zwei auswärts gerundete Intervalle zertifiziert')
