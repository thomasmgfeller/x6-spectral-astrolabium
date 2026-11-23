"""Conditional amplitudes before and after the 11->12 contraction, two quadratures."""
import argparse
import cmath
import json
from itertools import product
from math import pi, sqrt

import numpy as np
from numpy.polynomial.legendre import leggauss
from pruefen import ROOT, ORDER, PAST, INNER, EDGES, DR, DX, HALF, MU, X0, R0, E, COUPLING, u_for, check

DELTA=(3/722)**0.25
D=DELTA*(4-float(E))
H=1/8


def nodes(method, n):
    if method=='gauss':
        v,w=leggauss(n)
        return v,w/2
    v = np.cos(pi*np.arange(n)/(n-1))[::-1]
    # Use the cosine basis to avoid power-basis conditioning.
    k=np.arange(n)
    moments=np.zeros(n)
    moments[::2]=1/(1-k[::2]**2)
    return v,np.linalg.solve(np.cos(np.outer(k,np.arccos(v))),moments)


def coefficients(ys, stop, sign, method):
    last=ORDER.index(stop)
    c={j:-0.5 for j in ORDER[:last+1]}
    if method=='gauss':
        for target_pos,j in enumerate(ORDER[:last+1]):
            for lag,b in enumerate((1,-9,16,-8),1):
                if target_pos>=lag:
                    i=ORDER[target_pos-lag]
                    kick = sign*H/sqrt(D) if (i,j)==(6,12) else 0.
                    c[j]=c[j]-b*(ys[j]-ys[i]-kick)**2/38
    else:
        for (i,j),b in EDGES.items():
            if j in c:
                c[j]=c[j]-b*(ys[j]-ys[i])**2/38
        if stop==12:
            t=sign*H/sqrt(D)
            c[12]=c[12]+EDGES[6,12]*(2*(ys[12]-ys[6])*t-t*t)/38
    return c


def individual(rule,n,stop,sign,arm,mark):
    node,weights=nodes(rule,n)
    inner=[float(v) for v in u_for(R0+arm*DR)]
    inner[0]=float(inner[0])+node/64
    ys={j:float(j-5) for j in PAST}
    ys[3]+=float(E)
    ys.update({j:ys[3]+(4-float(E))*v for j,v in zip(INNER,inner)})
    faces=[0.]+[(a+b)/2 for a,b in zip(inner,inner[1:])]+[1.]
    f={j:b-a for j,a,b in zip(INNER,faces,faces[1:])}
    c=coefficients(ys,stop,sign,rule)
    def flat(centre,radius,freq):
        if rule=='gauss':
            return np.exp(1j*freq*centre)*np.sinc(freq*radius/pi)
        # Direct cubature of each independent flat density in the unsplit exponent.
        q,w=leggauss(10)
        return sum(v/2*np.exp(1j*freq*(centre+radius*t)) for t,v in zip(q,w))
    tag=float(X0+mark*DX)
    check((1-.01)*f[11] < tag-float(HALF) and tag+float(HALF) < (1+.01)*f[11],'Band')
    # Flat tag in x, original unnormalized density bands at 4,5,6; all other
    # omitted constants are positive and equal for the four complex phases.
    total=flat(D*tag,D*float(HALF),c[11])
    weight=1.
    for j in (4,5,6):
        weight=weight*f[j]
        total=total*flat(D*f[j],.01*D*f[j],c[j])
    if stop==12:
        total=total*np.exp(1j*c[12]*D/8)
    result={}
    for rho in (.125,.25):
        amp=np.sum(weights*weight*total*flat(rho,1/32,sum(c[j] for j in PAST)))/np.sum(weights*weight)
        result[str(rho)]=complex(amp)
    return result


def evaluate(rule,n):
    rows={}
    for stop,sign in ((11,0),(12,0),(12,1),(12,-1)):
        arms={(a,b):individual(rule,n,stop,sign,a,b) for a,b in product((-1,1),repeat=2)}
        for rho in ('0.125','0.25'):
            z={key:val[rho] for key,val in arms.items()}
            cross=z[1,1]*z[-1,-1]*(z[1,-1]*z[-1,1]).conjugate()
            rows[f'{stop}|{sign}|{rho}']={'phase':cmath.phase(cross),'min_modulus':min(map(abs,z.values()))}
    return rows


def calc():
    first,second=evaluate('gauss',24),evaluate('cc',25)
    fine=-float(COUPLING)*D*(4-float(E))**2*float(4*R0*DR*2*DX)
    for k,a in first.items():
        check(a['min_modulus']>.9,'Amplitudennullstelle')
        check(abs(a['phase']-second[k]['phase'])<2e-14 and abs(a['min_modulus']-second[k]['min_modulus'])<2e-13,'Quadraturvergleich')
        a['ratio_to_fine']=a['phase']/fine
    for rho in ('0.125','0.25'):
        for s in (-1,1):
            check(abs(first[f'12|{s}|{rho}']['phase']-first[f'12|0|{rho}']['phase'])<2e-14,'Pulsaufhebung')
    return {'gauss24':first,'clenshaw_curtis25':second,'fine_phase':fine}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--json',action='store_true')
    args=p.parse_args()
    data=calc()
    if args.json: print(json.dumps(data,indent=2))
    else:
        ref=json.loads((ROOT/'schnitt.json').read_text())
        for method in ('gauss24','clenshaw_curtis25'):
            for k,v in data[method].items():
                for field,value in v.items():
                    tol=2e-7 if field=='ratio_to_fine' else 2e-13
                    check(abs(value-ref[method][k][field])<tol,'Archivvergleich '+field)
        print('PASS · Zwei Quadraturen, zwei Schnitte, zwei Randdichten und beide Pulsrichtungen')
