"""Independent 3+1 KG Cauchy reference using spherical means and a Bessel tail.

All amplitudes remain complex. Convergence checks are not rigorous remainders.
"""
from functools import lru_cache
import numpy as np
from scipy.special import roots_legendre, j0, j1, jv
from common import oldref

A=oldref.source_norm()[0];RADIUS=.5;CARRIER=4.
@lru_cache(None)
def nodes(n):return roots_legendre(n)
def bump(r2):
    r2=np.asarray(r2);out=np.zeros_like(r2);good=r2<RADIUS**2
    out[good]=np.exp(-1/(1-r2[good]/RADIUS**2));return out
def spherical_means(x,radii,n):
    """M_r f(x)=(4*pi)^-1 integral_S2 f(x+r*n) dOmega, phi integral analytic."""
    x=np.asarray(x,float);radii=np.asarray(radii,float);result=np.zeros(radii.shape,complex)
    R=float(np.linalg.norm(x));zero=radii==0
    result[zero]=A*bump(np.array([R*R]))[0]*np.exp(1j*CARRIER*x[2])
    if R==0:
        return A*bump(radii*radii)*np.sinc(CARRIER*radii/np.pi)
    use=(radii>0)&(np.abs(R-radii)<RADIUS)
    if not use.any():return result
    r=radii[use,None];c=x[2]/R;s=np.sqrt(max(0.,1-c*c))
    hi=np.minimum(1.,(RADIUS**2-R*R-r*r)/(2*R*r))
    z,w=nodes(n);mu=-1+(hi+1)*(z[None,:]+1)/2
    f=bump(R*R+r*r+2*R*r*mu)
    phase=np.exp(1j*CARRIER*(x[2]+r*c*mu))
    azimuth=j0(CARRIER*r*s*np.sqrt(np.maximum(0.,1-mu*mu)))
    result[use]=A/2*np.sum(f*phase*azimuth*w[None,:]*(hi+1)/2,axis=1)
    return result
def kirchhoff(x,tau,n):
    """d/dtau[tau*M_tau f], evaluated analytically inside angular quadrature."""
    x=np.asarray(x,float);R=float(np.linalg.norm(x));tau=float(tau)
    if tau==0:return complex(A*bump(np.array([R*R]))[0]*np.exp(1j*CARRIER*x[2]))
    if abs(R-tau)>=RADIUS:return 0j
    if R==0:
        h=1-tau*tau/RADIUS**2;b=np.exp(-1/h)
        derivative=-2*tau/RADIUS**2/h**2*b
        return complex(A*(b*np.cos(CARRIER*tau)+tau*derivative*np.sinc(CARRIER*tau/np.pi)))
    c=x[2]/R;s=np.sqrt(max(0.,1-c*c));hi=min(1.,(RADIUS**2-R*R-tau*tau)/(2*R*tau))
    z,w=nodes(n);mu=-1+(hi+1)*(z+1)/2
    r2=R*R+tau*tau+2*R*tau*mu;h=1-r2/RADIUS**2
    b=bump(r2);derivative=np.zeros_like(h);good=h>0
    derivative[good]=-2*tau*(tau+R*mu[good])/RADIUS**2/h[good]**2
    a=s*np.sqrt(np.maximum(0.,1-mu*mu));q=CARRIER*tau*a
    kernel=(1+derivative+1j*CARRIER*tau*c*mu)*j0(q)-CARRIER*tau*a*j1(q)
    return complex(A/2*np.sum(w*(hi+1)/2*b*np.exp(1j*CARRIER*(x[2]+tau*c*mu))*kernel))
def j2_over_s2(m,s2):
    s2=np.asarray(s2,float);result=np.empty_like(s2);small=m*m*s2<1e-8
    result[small]=m*m/8-m**4*s2[small]/96+m**6*s2[small]**2/3072
    z=m*np.sqrt(s2[~small]);result[~small]=jv(2,z)/s2[~small]
    return result
def evaluate(query,n):
    answer=np.zeros((len(query),3),complex);z,w=nodes(n)
    for i,p in enumerate(query):
        tau=abs(float(p[0])+1);x=p[1:];R=float(np.linalg.norm(x))
        if R>=RADIUS+tau:continue
        K=kirchhoff(x,tau,n);M=spherical_means(x,np.array([tau]),n)[0]
        answer[i,0]=K
        if tau==0:answer[i,:]=K;continue
        lo=max(0.,R-RADIUS);hi=min(tau,R+RADIUS)
        # Split where the full sphere stops being inside the source ball.
        split=RADIUS-R
        edges=[lo]+([split] if lo<split<hi else [])+[hi]
        integrals=np.zeros(2,complex)
        for a,b in zip(edges[:-1],edges[1:]):
            rr=(a+b)/2+(b-a)*z/2;ww=(b-a)*w/2
            means=spherical_means(x,rr,n)
            for j,m in enumerate([1.,2.]):
                integrals[j]+=np.sum(ww*rr*rr*j2_over_s2(m,tau*tau-rr*rr)*means)
        answer[i,1:]=K-np.array([1.,4.])*tau*tau/2*M+np.array([1.,4.])*tau*integrals
    return answer
