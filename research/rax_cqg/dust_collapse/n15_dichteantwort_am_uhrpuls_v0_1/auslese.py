"""Two endpoint intensities and the selective four-corner inlet response after integration."""
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as F
from itertools import product
import cmath
import json
import math
import numpy as np
from randquelle import H, INNER, PAST, FUTURE, ROOT, profile
from modell import clocks,dwell
from quadratur import rule,average,coefficients

DELTA=(3/722)**.25
PROFILES={j:{i:float(v) for i,v in profile(j).items()} for j in (5,11)}
corners={'ref':(0,0),**{a+b:(s,t) for a,s in [('+',1),('-',-1)] for b,t in [('+',1),('-',-1)]}}
arms={'null':0,'plus':1,'minus':-1}

def calc(case):
    mass,n,outer,method,*extra=case
    target=extra[0] if extra else 11
    modes=(0,1,2) if extra else (0,1)
    V=PROFILES[target]
    x,_=rule(n,method)
    u=[(k+1)/8+x.reshape((1,)*k+(n,)+(1,)*(6-k))/64 for k in range(7)]
    f=dwell(u)
    keys=[(rho,alpha,a,cc) for rho in (.125,.25) for alpha in modes for a in arms for cc in corners]
    z=dict.fromkeys(keys,0j);norm=0.;h=float(H)
    one=np.ones((1,)*7)
    for mid in (-1/16,1/16):
        for node,ow in zip(*rule(outer,method)):
            e=(mid+node/32)/DELTA;D=DELTA*(4-e);y=clocks(e,u)
            w=ow*(D**(14 if mass else 7))/2
            norm+=w*average([8*f[j] for j in INNER],n,method) if mass else w
            for arm,s in arms.items():
                t=s*h/math.sqrt(D)
                for cc,(a,b) in corners.items():
                    yy=dict(y)
                    for j in PAST: yy[j]+=(a+b*V[j])*h/math.sqrt(D)
                    c=coefficients(yy,6,t,method)
                    past=sum(c[j] for j in PAST);future=sum(c[j] for j in FUTURE)/8
                    edge=one*np.exp(1j*future)
                    for alpha in modes:
                        parts=[edge]
                        if mass:
                            for j in INNER:
                                size=f[j]
                                if alpha and j==11:size=size-DELTA*t/(2*D)
                                if alpha==2 and j==5:size=size+DELTA*t/(2*D)
                                phase=mass*D*size*c[j]
                                parts.append(8*size*np.exp(1j*phase)*np.sinc(phase/(100*np.pi)))
                        else:
                            parts.extend(np.ones_like(cell) for cell in f.values())
                        integral=w*average(parts,n,method)*np.sinc(past/(32*np.pi))
                        for rho in (.125,.25):
                            z[rho,alpha,arm,cc]+=integral*np.exp(1j*rho*past)
    rows={}
    for rho,alpha in product((.125,.25),modes):
        zr={a:{cc:z[rho,alpha,a,cc]/norm for cc in corners} for a in arms}
        density={}; intens={}
        for arm,row in zr.items():
            phases={cc:cmath.phase(v*row['ref'].conjugate()) for cc,v in row.items()}
            assert max(map(abs,phases.values()))<1
            density[arm]=19*sum(a*b*phases[cc] for cc,(a,b) in corners.items())/(4*h*h)
            intens[arm]=abs(row['ref'])**2
        balance=(intens['minus']-intens['plus'])/(intens['minus']+intens['plus'])
        rows[str(F(rho))+'|'+str(alpha)]={'intensitaeten':intens,'asymmetrie':balance,'dichte':density,
            'dichtedifferenz':density['minus']-density['plus'],
            'amplituden':{a:{cc:[v.real,v.imag] for cc,v in row.items()} for a,row in zr.items()}}
    label=f'{F(mass)}|{method}{n}x{outer}'
    return (label+'|'+str(target) if extra else label),rows

def run():
    cases=[(m,n,k,method) for m in (0,.25,1,4) for method,n,k in [('gauss',5,10),('cc',5,9)]]
    with ProcessPoolExecutor(max_workers=3) as pool:return dict(pool.map(calc,cases))

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
