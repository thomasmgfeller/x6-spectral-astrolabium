"""Independent finite-intensity expected flux, in the original fixed time units."""
import json
import math
from pathlib import Path
import numpy as np
from common import b,nodes,coeff,write_rows
from lens_reference import eta,interval_volume

def physical_expectation(s,P,F,lam,n,lens=False,cap=15.,node_rule=nodes):
    v,weights=node_rule(n)
    radial=v[None,None,:]
    y=s-P*v[None,:,None]
    ey=eta(y,True)
    result=0.
    for first in range(0,n,12):
        stop=min(n,first+12)
        x=s+F*v[first:stop,None,None]
        d=eta(x,True)-ey
        am=1-(ey+d/2)/3
        e=(d/(3*am))**2
        poly=[sum(coeff(j,k)*e**(j+k) for j in range(5-k)) for k in range(5)]
        fac=b*lam*d**4*am**8
        # All coefficients in powers of (1-q) are nonnegative; poly[0] is a lower bound.
        qmax=np.minimum(1.,cap/np.sqrt(fac*poly[0]))
        q=qmax*(1-radial)*(1+radial)
        if lens:
            z=lam*interval_volume(ey,d,np.sqrt(1-q),True)
        else:
            val=poly[-1]
            for c in poly[-2::-1]: val=c+(1-q)*val
            z=fac*q*q*val
        kernel=np.exp(-z)*(1+z*(-9+z*(8-4*z/3)))
        angular=np.sum(weights[None,None,:]*(2*qmax*radial)*np.sqrt(1-q)*kernel,axis=2,keepdims=True)
        value=(x-y)*(1-y)**2*d**3*angular
        result+=np.sum(weights[first:stop,None,None]*weights[None,:,None]*value)
    return float(-4*math.pi/math.sqrt(6)*lam**1.5*P*F*result)

if __name__=='__main__':
    cfg=json.loads(Path('design.json').read_text())
    rows=[]
    for s,P,F in cfg['windows']:
        for lam in cfg['intensities']:
            r1=physical_expectation(s,P,F,lam,64)
            r2=physical_expectation(s,P,F,lam,96)
            r3=physical_expectation(s,P,F,lam,112,lens=True,cap=13.)
            rows.append(dict(s=s,P=P,F=F,lam=lam,R=r2,order_gap=abs(r1-r2),lens_R=r3,
                             method_gap=abs(r2-r3)))
            print(s,P,F,lam,round(r2,8),round(r1-r2,8),round(r2-r3,8),flush=True)
    write_rows('reference.csv',rows)
