"""Audit the saved means by evaluating the bounded real trigonometric polynomials."""
import argparse,json,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from source import ROOT,reference
from sample_clocks import coordinates
from reference import net,layout
PI=float.fromhex('0x1.921fb54442d18p+1')
def trig(x):
    x=np.asarray(x)
    if np.max(abs(x))>4096:raise ArithmeticError('polynomial argument')
    k=np.rint(x/(PI/2)).astype(np.int64)
    y=x-k*(PI/2)
    if np.max(abs(y))>.786:raise ArithmeticError('range reduction')
    y2=y*y
    co=0.;si=0.
    for p in range(9,-1,-1):
        co=co*y2+(-1)**p/math.factorial(2*p)
        si=si*y2+(-1)**p/math.factorial(2*p+1)
    si=si*y
    even=(k%2)==0
    c=np.where(even,co,si)*np.where(((k+1)//2)%2,-1,1)
    s=np.where(even,si,co)*np.where((k//2)%2,-1,1)
    return c,s
def cis(x):
    c,s=trig(x)
    return c+1j*s
def sinc(x):
    _,s=trig(x)
    return np.divide(s,x,out=np.ones_like(x),where=abs(x)>1e-8)
def density(C):
    u=C/2
    co,si=trig(u)
    denom=np.where(abs(u)>=.25,u,1.)
    re=si/denom
    im=(co-1)/denom
    small=abs(u)<.25
    v=u[small]
    if len(v):
        w=v*v;rr=0.;ii=0.
        for k in range(7,-1,-1):
            rr=rr*w+(-1)**k/math.factorial(2*k+1)
            ii=ii*w+(-1)**(k+1)/math.factorial(2*k+2)
        re[small]=rr;im[small]=v*ii
    return .5*(1+re+1j*im)
def eval_mask(mask,x,t):
    inner,c,gravity=layout((7,mask))
    times={i:(i-5)*net.STEP for i in net.geometry.P+net.geometry.F}
    times[3]=t
    times.update(zip(inner,x.T))
    phase={j:np.ones(len(t)) for j in times}
    for (i,j),v in reversed(list(c.items())):
        if v:
            if abs(v)>16:raise ValueError('edge bound')
            a=times[j]-times[i]; phase[j]+=(net.BETA*v/2)*(a*a)
    past=sum(phase[j] for j in net.geometry.P)
    future=sum(phase[j] for j in net.geometry.F)/16
    z=sinc(past/64)/math.sqrt(768)
    for j in reversed(inner):z=z*density(phase[j])
    return [np.mean(z*cis(gravity-future-.5*r*past)) for r in net.RHO]
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    prev=json.loads((ROOT/'sample.json').read_text());draw=np.fromfile(ROOT/'uniforms_u32le.bin',dtype='<u4').reshape(-1,8)
    assert F(786,1000)**20/math.factorial(20)<F('1e-19')
    result={}
    for tag,data in prev.items():
        x,t=coordinates(draw,tag);errors=[]
        for name,row in data.items():
            vals=eval_mask(int(name[4:]),x,t)
            errors.extend(abs(v-complex(*z)) for z,v in zip(row,vals))
        if max(errors)>1e-12:raise ValueError(('means',tag,max(errors)))
        result[tag]={'complex_means':len(errors),'maximum_difference':float(max(errors))}
    a.out.write_text(json.dumps(result,indent=2)+'\n')
