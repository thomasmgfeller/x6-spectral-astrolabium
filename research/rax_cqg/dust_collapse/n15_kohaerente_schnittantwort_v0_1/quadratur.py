"""Coherent amplitudes for the original reference and the two translated clock packets."""
import cmath
from fractions import Fraction as F
from functools import lru_cache
import math

import numpy as np
from modell import (ORDER, PAST, FUTURE, INNER, CUT, EDGES, H, EPS, NARROW,
                    INNER_MEANS, PACKET_MEANS, clocks, dwell)
from kern import gauss, contract

DELTA = (3/722)**0.25
PROFILE = dict(zip(PAST, [76/64,47/64,24/64,8/64]))
SLOTS = (4,5,6)

def settings():
    arms = {'0':(None,0,0,0)}
    for j in SLOTS:
        for s,tag in ((1,'+'),(-1,'-')):
            arms[f'{j}{tag}']=(j,s*float(H),0,0)
    for s,p in ((1,'+'),(-1,'-')):
        for t,q in ((1,'+'),(-1,'-')):
            arms['UV'+p+q]=(None,0,s*float(H),t*float(H))
    return arms

@lru_cache(None)
def rule(n,method):
    if method=='gauss':return gauss(n)
    x=np.cos(np.pi*np.arange(n)/(n-1))[::-1]
    k=np.arange(n)
    w=np.linalg.solve(x[None,:]**k[:,None],np.where(k%2==0,1/(k+1),0))
    return x,w

def average(factors,n,method):
    if method=='gauss':return contract(factors,n,True)
    tensor=np.ones((n,)*7)
    for term in factors:tensor=tensor*term
    for _ in range(7):tensor=np.tensordot(tensor,rule(n,method)[1],axes=(-1,0))
    return tensor.item()

def coefficients(y,slot,move,method):
    # Gauss: two glued actions including a shifted incoming memory on the right only.
    # CC: global action, then add changes to the affected crossing pairs analytically.
    c={j:-.5 for j in ORDER}
    if method=='gauss':
        past=list(ORDER[:CUT][-4:]); memory={i:y[i]+(move if i==slot else 0) for i in past}
        for idx,j in enumerate(ORDER):
            for d in range(1,min(4,idx)+1):
                i=ORDER[idx-d]; b=(1,-9,16,-8)[d-1]
                old=memory[i] if idx>=CUT and i in memory else y[i]
                c[j]=c[j]-(b/38)*(y[j]-old)**2
    else:
        for (i,j),b in EDGES.items():c[j]=c[j]-(b/38)*(y[j]-y[i])**2
        if slot is not None:
            for j in ORDER[CUT:]:
                if (slot,j) in EDGES:
                    c[j]=c[j]+(EDGES[slot,j]/38)*(2*(y[j]-y[slot])*move-move*move)
    return c

def sample(e,u,mass,rho,medium,n,method,arms):
    """One outer quadrature node. Density jitters and the collective past density are integrated analytically."""
    D=DELTA*(4-e); y=clocks(e,u);f=dwell(u)
    packet=medium=='packet'; atom=medium in ('empty','vacuum'); collar=medium!='vacuum'
    c0=coefficients(y,None,0,method); amp={}; unit=np.ones((1,)*7)
    one=[np.ones_like(v) for v in f.values()]
    measure=[8*v for v in f.values()] if not (packet or atom) else one
    scale=1 if packet else D**(7 if atom else 14)
    massnorm=scale*average(measure,n,method);jitter=1/500 if packet else .01
    for key,(slot,s,U,V) in arms.items():
        shifted=dict(y)
        for i in PAST:shifted[i]+=(U+PROFILE[i]*V)/math.sqrt(D)
        c=coefficients(shifted,slot,s/math.sqrt(D),method) if key!='0' else c0
        outer=unit
        if collar:
            p=sum(c[j] for j in PAST)
            outer=np.exp(1j*(rho*p+sum(c[j] for j in FUTURE)/8))*np.sinc((p/32)/np.pi)*unit
        if atom:
            val=average(one+[outer],n,method)
            amp[key]=[scale*val];continue
        factors=[outer]
        for j,weight in zip(INNER,measure):
            centre=mass*D*f[j];phase=centre*c[j]
            factors.append(weight*np.exp(1j*phase)*np.sinc(jitter*phase/np.pi))
        if not packet:
            amp[key]=[scale*average(factors,n,method)];continue
        # Minus and plus are translations of the same underlying base packet.
        if method=='gauss':
            beta=D*float(EPS)*(c0[13]*c[12]-c0[12]*c[13])
            vals=[average(factors+[unit*np.exp(sign*1j*beta)],n,method) for sign in (-1,1)]
        else:
            beta=0
            if slot is not None:
                t=s/math.sqrt(D)
                for j,coef in ((12,c0[13]),(13,-c0[12])):
                    b=EDGES.get((slot,j),0)
                    beta=beta+D*float(EPS)*coef*(b/38)*(2*(y[j]-y[slot])*t-t*t)
            mid=average(factors+[unit*np.cos(beta)],n,method)
            odd=1j*average(factors+[unit*np.sin(beta)],n,method)
            vals=[mid-odd,mid+odd]
        amp[key]=vals
    return massnorm,amp

def amplitudes(mass,rho,medium,n,outer,method,keys=None):
    config={k:v for k,v in settings().items() if keys is None or k in keys}
    packet=medium=='packet';radius=float(NARROW) if packet else 1/64
    centres=PACKET_MEANS if packet else INNER_MEANS;x,w=rule(n,method)
    u=[float(m)+radius*x.reshape((1,)*i+(n,)+(1,)*(6-i)) for i,m in enumerate(centres)]
    if packet:intervals=[(.25,float(NARROW))]
    else:intervals=[(o/DELTA,1/(32*DELTA)) for o in (-1/16,1/16)]
    total=0.;z={k:np.zeros(2 if packet else 1,dtype=complex) for k in config}
    for mid,half in intervals:
        for p,weight in zip(*rule(outer,method)):
            norm,current=sample(mid+half*p,u,mass,rho,medium,n,method,config)
            total+=weight*norm/len(intervals)
            for k,val in current.items():z[k]+=weight*np.array(val)/len(intervals)
    return {k:[complex(v/total) for v in vals] for k,vals in z.items()}

def readout(z):
    phase={k:cmath.phase(v*z['0'].conjugate()) for k,v in z.items()}
    assert max(map(abs,phase.values()))<1
    h=float(H)
    curv=[(phase[f'{j}+']+phase[f'{j}-'])/h**2 for j in SLOTS]
    hidden=19/8*math.fsum(w*c for w,c in zip((47/8,3,1),curv))
    visible=19*math.fsum((1 if k in ('UV++','UV--') else -1)*v for k,v in phase.items() if k.startswith('UV'))/(4*h*h)
    return {'raw':hidden+visible,'inner_three':hidden,'first_four':visible,'min_modulus':min(map(abs,z.values()))}
