"""Deterministic quadrature of the Poisson mean of the unmodified current."""
import csv
import json
import math
from functools import cache
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss

cfg = json.loads(Path("previous_design.json").read_text())
@cache
def unit_gauss(n):
    p,w = leggauss(n)
    return (p+1)/2, w/2

def eta(t, dust):
    return 3*(-np.expm1(np.log1p(-t)/3)) if dust else t

def interval_volume(eta_y,d,v,dust):
    if not dust:
        return np.pi/24 * (d*d*(1-v*v))**2
    left=d*(1-v)/2
    right=d*(1+v)/2
    r=d*v
    vol=0.
    p,w=unit_gauss(6)
    for zone,(lo,hi) in enumerate(((0,left),(left,right),(right,d))):
        width=hi-lo
        for u,weight in zip(p,w):
            s=lo+width*u
            if zone==0:
                lens=4*np.pi/3*s**3
            elif zone==2:
                lens=4*np.pi/3*(d-s)**3
            else:
                lens=np.pi*(d-r)**2*(r*r+2*r*d-3*(2*s-d)**2)/(12*r)
            vol+=weight*width*(1-(eta_y+s)/3)**8*lens
    return vol

def responses(center,pad,dust,order,radial_power=1):
    nodes,weights=unit_gauss(order)
    x=center+pad*nodes[:,None,None]
    y=center-pad*nodes[None,:,None]
    u=nodes[None,None,:]
    v=1-(1-u)**radial_power
    jac=radial_power*(1-u)**(radial_power-1)
    ey=eta(y,dust)
    d=eta(x,dust)-ey
    iv=interval_volume(ey,d,v,dust)
    assert np.all(iv>=0)
    w=(weights[:,None,None]*weights[None,:,None]*weights[None,None,:] *
       jac * pad**2 * (x-y)*4*np.pi*d**3*v**2 * ((1-y)**2 if dust else 1))
    out=[]
    for lam in cfg['flux_intensities']:
        z=lam*iv
        kernel=np.exp(-z)*(1+z*(-9+z*(8-4*z/3)))
        out.append(-2*lam**1.5/math.sqrt(6)*np.sum(w*kernel))
    return out

if __name__=="__main__":
    rows=[]
    for geo in cfg['geometries']:
        for t in cfg['flux_centers']:
            for pad in cfg['flux_padding']:
                runs=[responses(t,pad,geo=='dust',n) for n in cfg['flux_orders']]
                for j,lam in enumerate(cfg['flux_intensities']):
                    a,b,c=[float(res[j]) for res in runs]
                    rows.append(dict(geo=geo,t=t,pad=pad,lam=lam,q32=a,q64=b,q96=c,gap=abs(b-c),
                        passed=(abs(c-1)<=cfg['flux_required_abs_relative_error'] and abs(b-c)<=cfg['flux_max_quadrature_difference_of_mass'])))
    with open('flux.csv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for row in rows:
        if row['geo']=='dust' or row['t']==cfg['flux_centers'][0]:
            print(row['geo'],row['t'],row['pad'],row['lam'],round(row['q96'],7),round(row['gap'],7))
