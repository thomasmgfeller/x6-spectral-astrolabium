"""Boundary amplitudes with a coherent pass/fail gate on the two shifted clocks."""
from functools import lru_cache
from pathlib import Path
import cmath,math,sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent/'quellen'))
import kern
from auslese import settings
from geometrie import addresses

BASE=Path(__file__).resolve().parent
PORTS=addresses(kern.ORDER,set(kern.INNER))

@lru_cache(None)
def rule(n,method):
    if method=='gauss':return kern.gauss(n)
    # Independent interpolatory Clenshaw-Curtis rule, including endpoints.
    x=np.cos(np.pi*np.arange(n)/(n-1))[::-1];powers=np.arange(n)
    weights=np.linalg.solve(x[np.newaxis,:]**powers[:,np.newaxis],np.where(powers%2==0,1/(powers+1),0.))
    return x,weights

def product_mean(factors,n,method):
    # Each axis is contracted at its last appearance. Control uses a full tensor.
    if method=='cc':
        joint=np.ones((n,)*7,dtype=np.result_type(*factors));w=rule(n,method)[1]
        for elem in factors:joint=joint*elem
        for _ in range(7):joint=np.tensordot(joint,w,axes=(-1,0))
        return joint.item()
    return kern.contract(factors,n,True)

def cell(n,off,src,gate,sector,mass,rho,method,gate_source=None):
    d=4*kern.DELTA-off;root=math.sqrt(d);a,b,u,v,t=map(float,src)
    shifts=dict(zip(PORTS,(a,b)))
    gate_shifts=shifts if gate_source is None else dict(zip(PORTS,gate_source[:2]))
    r=1/64; width={'open':math.inf,'wide':7/128,'strict':r}[gate]
    x,_=rule(n,method);coords={};fraction=1.
    for i,j in enumerate(kern.INNER):
        move=kern.DELTA*float(gate_shifts.get(j,0))/(d*root)
        lo=max(-r,-width-move);hi=min(r,width-move)
        if hi<=lo:return (0j,0.)
        fraction*=(hi-lo)/(2*r);centre=(i+1)/8
        coords[j]=centre+(lo+hi)/2+(hi-lo)/2*x.reshape((1,)*i+(n,)+(1,)*(6-i))
    y={j:float(j-5) for j in kern.PAST+kern.FUTURE};y[3]+=off/kern.DELTA
    y.update({j:y[3]+(d/kern.DELTA)*coords[j]+shifts.get(j,0)/root for j in kern.INNER})
    for j in kern.PAST:y[j]+=(u+v*kern.V[j])/root
    cs=list(coords.values()); faces=[0]+[(left+right)/2 for left,right in zip(cs,cs[1:])]+[1]
    positive=sector=='positive';collar=sector!='vacuum';phase_factors=[];measure_factors=[];past=0.
    for idx,j in enumerate(kern.ORDER):
        g=-.5*kern.UNIT
        for i,k in kern.links_to(idx):g=g-(k/38)*(y[j]-y[i])**2
        if j in kern.PAST:
            past=past+g
            if j==kern.PAST[-1] and collar:phase_factors.append(np.exp(1j*rho*past)*kern.sinc(past/32))
        elif j in kern.FUTURE:
            if collar:phase_factors.append(np.exp(.125j*g))
        else:
            k=kern.INNER.index(j);f=faces[k+1]-faces[k];factor=8*f if positive else np.ones_like(f)
            measure_factors.append(factor)
            w=mass*d*f
            phase_factors.append(factor*np.exp(1j*w*g)*kern.sinc(.01*w*g) if positive else factor)
    scale=fraction*d**(14 if positive else 7)
    amp=scale*product_mean(phase_factors,n,method)*cmath.exp(1j*t*(-7/8 if collar else 0)/d)
    return amp,float(scale*product_mean(measure_factors,n,method))

def spectrum(sector,mass,rho,gate,n,k,method='gauss'):
    points,weights=rule(k,method);amps={};passes={};lobes={};rows=settings()
    for name,(src,_) in rows.items():
        by_lobe=[]
        for mid in (-1/16,1/16):
            parts=[cell(n,mid+p/32,src,gate,sector,mass,rho,method) for p in points]
            by_lobe.append((sum(w*z[0]/2 for w,z in zip(weights,parts)),sum(w*z[1]/2 for w,z in zip(weights,parts))))
        amps[name]=sum(t[0] for t in by_lobe);passes[name]=sum(t[1] for t in by_lobe);lobes[name]=[t[1] for t in by_lobe]
    norm=passes['0'];z={k:v/norm for k,v in amps.items()};phase={k:cmath.phase(v/z['0']) for k,v in z.items()}
    return {'raw':math.fsum(float(w)*phase[k] for k,(_,w) in rows.items()),'max_relative_angle':max(map(abs,phase.values())),
            'min_modulus':min(map(abs,z.values())), 'kernels':{k:[v.real,v.imag] for k,v in z.items()},
            'admitted':{k:v/norm for k,v in passes.items()},'admitted_by_lobe':{k:[x/t for x,t in zip(v,lobes['0'])] for k,v in lobes.items()}}
