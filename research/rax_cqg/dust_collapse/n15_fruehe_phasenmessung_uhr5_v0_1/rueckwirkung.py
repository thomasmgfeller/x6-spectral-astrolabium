"""Interval enclosure of the instrument inserted into the ordinary cut contraction."""
import argparse
import json
from fractions import Fraction as F
from math import ceil
from modelltest import ROOT, D, K, E, H, X0, DX, STEP, EDGES, ORDER, INNER_MEANS, I, S, clocks, dwell, require
from intervalle import C, cis, gaussian, sinc

N=24
JS=(4,5,6)
IUNIT=C(0,1)


def majorant():
    # Valid for either packet independently; a mixed arm uses the centre phase
    # from the outgoing arm and the centred real density jitters from the incoming arm.
    uerr=[F(4,64),F(3,2500)+4*H,0,0,0,0,0]
    inner=(4,5,6,11,12,13,14)
    rad=dict.fromkeys(ORDER,0)
    rad.update({j:K*z for j,z in zip(inner,uerr)})
    y=clocks(E,INNER_MEANS)
    fc=dwell(INNER_MEANS)
    df={4:(uerr[0]+uerr[1])/2,5:uerr[0]/2,6:uerr[1]/2,12:0}
    bound=F(0)
    for j in (4,5,6,11,12,13):
        cabs=F(1,2)
        cim=F(0)
        for (i,end),w in EDGES.items():
            if end==j:
                gap=abs(y[j]-y[i])+rad[i]+rad[j]
                cabs+=F(abs(w),38)*gap**2
                cim+=F(abs(w),19)*gap*(rad[i]+rad[j])
        if j in df:
            require(fc[j]+df[j]<1,'Volumen')
            bound+=F(101,100)*((fc[j]+df[j])*cim+df[j]*cabs)
        else:
            bound+=(X0+DX+H if j==11 else F(1,8))*cim
    require(D.hi<S and bound<1,'Cauchy-Majorante')
    m=3**ceil(bound)
    return bound,4*F(m,4**(2*N))/(1-F(1,4))


def parts(arm,z4,z5):
    u=list(map(I.of,INNER_MEANS));u[0]+=z4/64;u[1]+=arm*STEP+H*z5
    y=clocks(E,u);f=dwell(u)
    c={j:I.of(F(-1,2)) for j in (4,5,6,11,12,13)}
    for (i,j),w in EDGES.items():
        if j in c:c[j]-=F(w,38)*(y[j]-y[i])**2
    vol=I.of(1);phi=I.of(0)
    for j in JS:
        arg=D*f[j]*c[j]
        vol*=f[j]*sinc(arg/100);phi+=arg
    gamma=D*c[11]
    theta12=D*f[12]*c[12]
    return vol*sinc(gamma*H),gamma,f[12]*sinc(theta12/100),phi+gamma*X0+theta12+D*c[13]/8


def integrals(err):
    out={(a,b,h):C(0) for a in (-1,1) for b in (-1,1) for h in (-1,1)}
    grid=gaussian(N)
    for z4,w4 in grid:
        for z5,w5 in grid:
            data={a:parts(a,z4,z5) for a in (-1,1)}
            for a,b,h in out:
                vin,gamma,_,_=data[a]
                _,_,vout,phi=data[b]
                term=cis(phi+h*DX*gamma).scale(w4*w5*vin*vout)
                out[a,b,h]=out[a,b,h]+term
    return {k:z.pad(err) for k,z in out.items()}


def mod2(z):
    return (z*z.conj()).re


def run():
    bound,err=majorant()
    j=integrals(err)
    rows={}
    baseline=None
    for eta in (F(0),F(1,2),F(1)):
        coeff=(1+I.of(1-eta**2).sqrt())/2
        balance={}
        for h in (-1,1):
            z0,z1=j[-1,-1,h],j[1,1,h]
            w0,w1=IUNIT*j[-1,1,h],(IUNIT*j[1,-1,h]).scale(-1)
            def intensity(t):
                return coeff*mod2(z0+t*z1)+(1-coeff)*mod2(w0+t*w1)
            im=intensity(IUNIT.scale(-1));ip=intensity(IUNIT)
            balance[h]=(im-ip)/(im+ip)
        diff=balance[1]-balance[-1]
        if eta==0: baseline=diff
        frac=I.of(1) if eta==0 else diff/baseline
        rows[str(eta)]={'balance_difference':diff.rounded(19),'fraction_of_original':frac.rounded(13)}
    return {'n':N,'exponent_bound':str(bound),'amplitude_remainder':str(err),'strengths':rows}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',action='store_true')
    args=p.parse_args();out=json.dumps(run(),indent=2)+'\n'
    if args.json:print(out,end='')
    else:
        require(out==(ROOT/'rueckwirkung.json').read_text(),'Archiv')
        print('PASS · Pulsfreier Intensitätskontrast mit Messung für drei Stärken eingeschlossen')
