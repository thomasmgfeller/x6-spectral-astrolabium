"""Absolute curved high-density coefficient. No reference amplitudes as input."""
import math
import json
from pathlib import Path
import numpy as np
from scipy.special import digamma
from common import b,nodes,geometry,write_rows

A=-17*math.sqrt(6)/(10*math.pi)
r0=1/32; r1=1/16
Zdouble=-17/3840
G=-b**-2
D=-math.log(b)+digamma(2)+11/3
fp0=-2*r0*(digamma(4)-digamma(-1.5))
fp1=-2*r1*(digamma(3)-digamma(-.5))

def local(h):
    a2=(16/15-h)/32
    fp2=(8/9-h-32/135)*fp0+28/135*fp1+(-16*r0+14*r1)/135
    return a2,fp2

def angular_residue(h,w):
    S,H=geometry(h,w)
    t1,t2,t3=[c/H[0] for c in H[1:4]]
    l1=-2*t1
    l2=-2*t2+3*t1*t1
    l3=-2*t3+6*t1*t2-4*t1**3
    return -.5*S/H[0]**2*(-1/16-l1/8-l2/2+l3)

def regular_w(h,w):
    a2,_=local(h)
    remainder=(angular_residue(h,w)-r0*(1+w)-a2*w*w)/w**3
    # Evaluate the divided difference around zero by a convergent Cauchy series.
    phase=np.exp(2j*math.pi*np.arange(48)/48)
    radius=.18
    vals=angular_residue(h,radius*phase)
    taylor=np.fft.fft(vals,axis=1).real/48
    small=0.
    for k in range(17,2,-1):
        small=small*w+taylor[:,k,None]/radius**k
    return np.where(w<.035,small,remainder)

def constant(p,f,n=64):
    grid,weights=nodes(n)
    split=p/(p+f)
    single=0.
    for left,right in [(0,split),(split,1)]:
        h=(left+(right-left)*grid)[:,None]
        W=np.minimum(p/h,f/(1-h))
        w=W*grid[None,:]
        a2,fp2=local(h)
        regular=(regular_w(h,w)*weights[None,:]).sum(axis=1,keepdims=True)*W
        term=-r0/(2*W**2)-r0/W+a2*np.log(W)-fp2/4+regular
        single+=(right-left)*np.dot(weights,term[:,0])
    return 4*math.pi/math.sqrt(6)*G*(single+D*Zdouble)

if __name__=='__main__':
    cfg=json.loads(Path('design.json').read_text())
    rows=[]
    for s,P,F in cfg['windows']:
        U=1-s
        B=constant(P/U,F/U)
        check=constant(P/U,F/U,96)
        for lam in cfg['intensities']:
            L=lam*U**4
            dust=1+(A*math.log(L)+B)/math.sqrt(L)
            flat=1+2*math.sqrt(6)/(math.pi*math.sqrt(lam))*(1/P**2+1/F**2-1/(P+F)**2)
            rows.append(dict(s=s,P=P,F=F,lam=lam,L=L,A=A,B=B,B_resolution=abs(B-check),pred=dust,
                             pred_flat=flat,pred_no_log=1+B/math.sqrt(L)))
    write_rows('predictions.csv',rows)
    print([(r['s'],r['P'],round(r['B'],6),round(r['pred'],6)) for r in rows if r['lam']==3000000])
    print('B quadrature gap',max(r['B_resolution'] for r in rows))
