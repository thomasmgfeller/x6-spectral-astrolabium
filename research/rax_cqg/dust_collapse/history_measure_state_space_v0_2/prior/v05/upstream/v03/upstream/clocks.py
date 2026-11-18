"""Ordered quadrature of the declared normalized compact clock/density integrals."""
from functools import lru_cache
import numpy as np
from geometry import order, P, F

BETA = 4 / np.sqrt(6)
STEP = np.sqrt(2 / (19 * BETA))
RHO = (1/8,1/4)


@lru_cache(None)
def quadrature(n):
    x,w=np.polynomial.legendre.leggauss(n)
    return x,w/2


def density_factor(C):
    return (1+np.exp(-0.25j*C)*np.sinc(C/(4*np.pi)))/2


def weights(name,t,n):
    inner,coeffs,gravity=order(name)
    x,w=quadrature(n)
    times={j:(j-5)*STEP for j in (*P,*F)}
    times[3]=t
    def C(j):
        return 1+BETA/2*sum(v*(times[j]-times[i])**2 for (i,end),v in coeffs.items() if end==j and v)
    bp=sum(C(j) for j in P)
    # A lift is attached to both collars but incomparable with every old internal
    # event. Its density factor and all its future-row contributions separate.
    extra=1
    if 11 in inner:
        assert all((11,i) not in coeffs and (i,11) not in coeffs for i in (4,5,6))
        times[11]=1.5*x
        extra_bf=BETA/2*sum(coeffs[11,j]*(times[j]-times[11])**2 for j in F)
        extra=w @ (density_factor(C(11))*np.exp(-1j*extra_bf/16))
        coeffs={ij:v for ij,v in coeffs.items() if 11 not in ij}
    times[5]=1.5*x[:,None]; times[6]=1.5*x[None,:]
    plane=w[:,None]*w[None,:]
    value=0j
    for k in range(n):
        times[4]=1.5*x[k]
        part=np.exp(-1j*sum(C(j) for j in F)/16)
        for j in (4,5,6):
            part=part*density_factor(C(j))
        value+=w[k]*np.sum(plane*part)
    return bp, np.exp(1j*gravity)*value*extra


def direct_lift(t,n):
    """Check the separated four-inner-variable integral by direct 4D quadrature."""
    inner,b,F4=order("chain_lift")
    x,w=quadrature(n)
    times={j:(j-5)*STEP for j in (*P,*F)}
    times[3]=t
    for k,j in enumerate(inner):
        shape=[1]*4
        shape[k]=n
        times[j]=(1.5*x).reshape(shape)
    def C(j):
        return 1+BETA/2*sum(v*(times[j]-times[i])**2 for (i,end),v in b.items() if end==j and v)
    a=np.exp(-1j*sum(C(j) for j in F)/16)
    for j in inner:
        a=a*density_factor(C(j))
    for j in inner:
        a=np.tensordot(w,a,axes=([0],[0]))
    return np.exp(1j*F4)*a


def amplitudes(name,n,m):
    x,w=quadrature(m)
    norm=np.sqrt((2*(1/32)/3)*(1/32))
    lobes=[[],[]]
    comp=[]
    for k in (-1,1):
        sample=[weights(name,-2*STEP+k/16+t/32,n) for t in x]
        b,v=np.array([s[0] for s in sample]),np.array([s[1] for s in sample])
        for j,r in enumerate(RHO):
            phase=np.exp(-0.5j*r*b)*np.sinc(b/(64*np.pi))
            lobes[j].append(norm * ((w*phase) @ v))
    # Compensating the past-density phase inside the density integral removes it pointwise.
        comp.append(norm*(w @ v))
    return np.array(lobes), sum(comp)/np.sqrt(2), weights(name,-2*STEP,n)
