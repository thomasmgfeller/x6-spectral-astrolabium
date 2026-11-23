"""Ordinary closure of clock 5 at event 13 on two genuine dust wave packets."""
import argparse
import cmath
import json
from itertools import product
from math import pi, sqrt
import numpy as np
from numpy.polynomial.legendre import leggauss
from schnitt import D, E, HALF, X0, DX, H, nodes
from pruefen import ROOT, ORDER, PAST, INNER, EDGES, check


def amplitude(method,n,pulse,arm,tag,neutral=False):
    t,weights=nodes(method,n)
    width=1/(72*D*(4-float(E))**2)
    u=[1/8+t[:,None]/64,.25+arm*width+float(HALF)*t[None,:],.375,.5,.625,.75,.875]
    faces=[0]+[(a+b)/2 for a,b in zip(u,u[1:])]+[1]
    f=dict(zip(INNER,[b-a for a,b in zip(faces,faces[1:])]))
    y={j:float(j-5) for j in PAST}
    y[3]+=float(E)
    y.update({j:y[3]+(4-float(E))*a for j,a in zip(INNER,u)})
    before=ORDER[:ORDER.index(13)+1]
    c={j:-.5 for j in before}
    step=pulse*H/sqrt(D)
    if method=='gauss':
        for k,j in enumerate(before):
            for d,weight in enumerate((1,-9,16,-8),1):
                if d<=k:
                    i=ORDER[k-d]
                    old=y[i]+(step if i==6 and j in (12,13) else 0)
                    c[j]=c[j]-(weight/38)*(y[j]-old)**2
    else:
        for (i,j),b in EDGES.items():
            if j in c: c[j]=c[j]-(b/38)*(y[j]-y[i])**2
        for j in (12,13):
            c[j]=c[j]+(EDGES[6,j]/38)*(2*(y[j]-y[6])*step-step**2)
    if neutral:
        # Change only the (5,11) square, keeping both physical windows and all other pairs.
        y5_centre=y[3]+(4-float(E))/4
        c[11]=c[11]+(9/38)*((y[11]-y5_centre)**2-(y[11]-y[5])**2)
    dens_nodes,dens_weights=leggauss(10)
    def integrate(lo,halfwidth,freq):
        if method=='gauss':
            return np.exp(1j*freq*lo)*np.sinc(halfwidth*freq/pi)
        return sum(weight/2*np.exp(1j*freq*(lo+halfwidth*z)) for z,weight in zip(dens_nodes,dens_weights))
    val=np.exp(1j*c[13]*D/8)*integrate(D*float(X0+tag*DX),D*float(HALF),c[11])
    for j in (4,5,6,12):
        v=D*f[j]
        val=val*f[j]*integrate(v,v/100,c[j])
    ww=weights[:,None]*weights[None,:]
    return {str(rho): complex(np.sum(val*ww*integrate(rho,1/32,sum(c[j] for j in PAST)))) for rho in (.125,.25)}


def calc(method,n,neutral=False):
    rows={}
    for pulse in ((0,) if neutral else (0,1,-1)):
        values={(arm,tag):amplitude(method,n,pulse,arm,tag,neutral) for arm,tag in product((-1,1),repeat=2)}
        for rho in ('0.125','0.25'):
            z={k:v[rho] for k,v in values.items()}
            selector={}
            intensities={}
            for mark in (-1,1):
                a,b=z[-1,mark],z[1,mark]
                i_minus,i_plus=abs(a-1j*b)**2,abs(a+1j*b)**2
                selector[mark]=(i_minus-i_plus)/(i_minus+i_plus)
                intensities[str(mark)]=[i_minus,i_plus]
            phase=cmath.phase(z[1,1]*z[-1,-1]*(z[-1,1]*z[1,-1]).conjugate())
            rows[f'{pulse}|{rho}']={'mixed_phase':phase,
                                    'balance_low':selector[-1], 'balance_high':selector[1],
                                    'difference_in_balance':selector[1]-selector[-1],
                                    'intensities_common_scale':intensities,
                                    'min_modulus_common_scale':min(map(abs,z.values()))}
    return rows


def compute():
    a,b=calc('gauss',20),calc('cc',21)
    for k,row in a.items():
        for field in ('mixed_phase','difference_in_balance','balance_low','balance_high'):
            check(abs(row[field]-b[k][field])<8e-14, 'Unabhängige Quadratur '+field)
        for label in ('-1','1'):
            check(np.allclose(row['intensities_common_scale'][label],b[k]['intensities_common_scale'][label],
                              rtol=2e-13,atol=0),'Intensitäten')
        check(row['min_modulus_common_scale']>1e-4 and abs(row['mixed_phase'])>1e-7,'Kontrollnenner')
    return {'gauss20':a,'cc21':b}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',action='store_true')
    args=p.parse_args()
    data=compute()
    if args.json: print(json.dumps(data,indent=2))
    else:
        ref=json.loads((ROOT/'ausgang.json').read_text())
        for method,entries in data.items():
            for key,row in entries.items():
                for field in ('mixed_phase','balance_low','balance_high','difference_in_balance','min_modulus_common_scale'):
                    check(abs(row[field]-ref[method][key][field])<1e-13,'Archivvergleich '+field)
                for label in ('-1','1'):
                    check(np.allclose(row['intensities_common_scale'][label],ref[method][key]['intensities_common_scale'][label],
                                      rtol=2e-13,atol=0),'Archivierte Intensität')
        print('PASS · Gewöhnliche Verklebung bis 13, zwei Präparationsphasen, beide Quadraturen')
