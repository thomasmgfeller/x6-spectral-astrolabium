"""Final slope audit on rays in the time rectangle; scaled coordinates, extended precision."""
import math
import json
from pathlib import Path
import numpy as np
from common import b,coeff,write_rows
from precision import polished
from prediction import A
def ray_flux(p,f,L,n,cap):
    grid,weights=polished(n);t=grid[None,None,:]
    ans=np.longdouble(0)
    for low,high in [(0,p/(p+f)),(p/(p+f),1)]:
        for i in range(0,n,6):
            hh=low+(high-low)*grid[i:i+6,None,None]
            W=np.minimum(p/hh,f/(1-hh))
            w=W*grid[None,:,None]**2
            ay=(1+hh*w)**(np.longdouble(1)/3)
            ax=(1-(1-hh)*w)**(np.longdouble(1)/3)
            d_over_w=3/(ay*ay+ay*ax+ax*ax)
            D=w*d_over_w
            am=(ay+ax)/2
            e=(D/(3*am))**2
            pp=[sum(coeff(j,k)*e**(j+k) for j in range(5-k)) for k in range(5)]
            fac=b*L*D**4*am**8
            limit=np.minimum(1.,cap/np.sqrt(fac*pp[0]))
            q=limit*(1-t)*(1+t);geom=pp[-1]
            for c in pp[-2::-1]: geom=c+(1-q)*geom
            z=fac*q**2*geom
            phi=np.exp(-z)*(1+z*(-9+z*(8-4*z/3)))
            ang=np.sum(weights[None,None,:]*2*limit*t*np.sqrt(1-q)*phi,axis=2,keepdims=True)
            val=(w**5*(1+hh*w)**2*d_over_w**3*ang*2*W*grid[None,:,None])
            ans+=(high-low)*np.sum(weights[i:i+6,None,None]*weights[None,:,None]*val)
    return float(-4*math.pi/math.sqrt(6)*L**1.5*ans)

if __name__=='__main__':
    cfg=json.loads(Path('logcheck_design.json').read_text());U=1-cfg['s']
    rows=[]
    for P,F in cfg['windows']:
        for lam in cfg['intensities'][-2:]:
            v0=ray_flux(P/U,F/U,lam*U**4,112,13)
            v1=ray_flux(P/U,F/U,lam*U**4,160,12)
            rows.append(dict(P=P,F=F,lam=lam,R112=v0,R160=v1))
            print(rows[-1],flush=True)
    write_rows('ray_audit.csv',rows)
    for i in [0,2]:
        lo,hi=rows[i:i+2]
        for field in ['R112','R160']:
            v=U**2*(math.sqrt(hi['lam'])*(hi[field]-1)-math.sqrt(lo['lam'])*(lo[field]-1))/math.log(hi['lam']/lo['lam'])
            print(lo['P'],field,'slope',v,'target',A)
