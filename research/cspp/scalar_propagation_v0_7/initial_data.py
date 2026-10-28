"""Cauchy jets, explicit P1/P3 history extension and independent exact wave fields."""
import numpy as np
from flint import arb,acb,ctx
from common import load,HERE,check
reference=load('v07_massive_reference',HERE.parent/'massive_reference_v0_5/reference.py')
source=reference.previous

def wave(point,k):
    t,z=arb(float(point[0]))+1,arb(float(point[3]));w=(arb(k*k)+1).sqrt()
    f=(acb(0,k*z)).exp();g=-acb(0,w)*f
    return (acb(0,k*z-w*t)).exp(),f,g,-w*w*f,-w*w*g

def bump_jets(point,m,A):
    a,k,_=source.parameters();r2=sum(arb(float(x))**2 for x in point[1:]);h=1-r2/(a*a)
    if h<=0:return acb(0),acb(0),acb(0),acb(0)
    check(h>0,'initial compact support decided')
    z=arb(float(point[3]));f=A*(-1/h).exp()*acb(0,k*z).exp()
    lap=-6/(a*a*h*h)-8*r2/(a**4*h**3)+4*r2/(a**4*h**4)-k*k-acb(0,4*k*z/(a*a*h*h))
    return f,acb(0),(lap-m*m)*f,acb(0)

def extension(point,jets,order):
    check(order in [1,3],'declared adapter order');t=arb(float(point[0]))+1
    f,g,l2,l3=jets;return f+t*g+(t*t*l2/2+t**3*l3/6 if order==3 else 0)

def exact_bump(point,m,A):
    if m==0:return source.kirchhoff(point,A)[0]
    if all(x==0 for x in point[1:]):return source.massive_center(point,m,A)[0]
    return reference.off_center(point,m,A)[0]

def float_wave_history(x,k,order):
    tau=x[:,0]+1.;w=np.sqrt(float(k*k+1));f=np.exp(1j*k*x[:,3]);g=-1j*w*f
    return f+tau*g+(tau*tau*(-w*w*f)/2+tau**3*(-w*w*g)/6 if order==3 else 0)

def float_bump_history(x,m,order,A):
    a=.5;k=4.;r2=np.sum(x[:,1:]**2,axis=1);h=1-r2/(a*a);f=np.zeros(len(x),complex);lap=np.zeros(len(x),complex);use=h>0
    v=h[use];z=x[use,3];rr=r2[use]
    f[use]=A*np.exp(-1/v)*np.exp(1j*k*z)
    lap[use]=(-6/(a*a*v*v)-8*rr/(a**4*v**3)+4*rr/(a**4*v**4)-k*k-4j*k*z/(a*a*v*v)-m*m)*f[use]
    return f+(x[:,0]+1)**2*lap/2 if order==3 else f
