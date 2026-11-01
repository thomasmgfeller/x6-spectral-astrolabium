"""Compact-window free-scalar control; dimensionless ell0=c=hbar=1."""
import numpy as np
from scipy.special import spherical_jn, j1
from numpy.polynomial.legendre import leggauss


def space_ft(z):
    z=np.asarray(z,dtype=float)
    out=np.ones_like(z); mask=np.abs(z)>1e-3
    out[mask]=105*spherical_jn(3,z[mask])/z[mask]**3
    out[~mask]=1-z[~mask]**2/18+z[~mask]**4/792-z[~mask]**6/61776
    return out


def time_ft(z):
    z=np.asarray(z,dtype=float)
    out=np.ones_like(z);mask=np.abs(z)>1e-3
    out[mask]=15*spherical_jn(2,z[mask])/z[mask]**2
    out[~mask]=1-z[~mask]**2/14+z[~mask]**4/504-z[~mask]**6/33264
    return out


def time_convolution(v):
    v=np.abs(np.asarray(v))
    return np.where(v<2,5*(2-v)**5*(v**4+10*v**3+36*v*v+40*v+16)/3584,0)


def space_convolution(w):
    w=np.asarray(w)
    return np.where(w<2,35*(2-w)**6*(5*w**5+60*w**4+288*w**3+656*w*w+576*w+192)/(270336*np.pi),0)


def rule(n,lo,hi):
    x,w=leggauss(n)
    return lo+(x+1)*(hi-lo)/2,w*(hi-lo)/2


def spectral(m,T,r=1.,a=.25,b=.1,cutoff=400.,order=32):
    """R only for nonoverlapping time supports; H is the symmetric covariance."""
    if abs(T)<=2*b:raise ValueError('time supports must be strictly ordered')
    x,w=leggauss(order)
    edges=np.linspace(0,cutoff,int(np.ceil(cutoff))+1)
    k=(edges[:-1,None]+edges[1:,None])/2+(edges[1:]-edges[:-1])[:,None]*x/2
    weights=(edges[1:]-edges[:-1])[:,None]*w/2
    om=np.sqrt(k*k+m*m)
    kernel=weights*k*k/om*space_ft(a*k)**2*time_ft(b*om)**2*np.sinc(k*r/np.pi)
    comm=float(np.sum(kernel*np.sin(om*T))/(2*np.pi**2))
    H=float(np.sum(kernel*np.cos(om*T))/(4*np.pi**2))
    return dict(R=comm if T>0 else 0.,Delta_AB=comm,H_AB=H)


def spectral_tail_bound(a=.25,b=.1,cutoff=400.):
    """Uniform absolute R-integral tail, |sinc|,|sin| <= 1 and omega >= k."""
    A=1+6/(a*cutoff)+15/(a*cutoff)**2+15/(a*cutoff)**3
    B=1+3/(b*cutoff)+3/(b*cutoff)**2
    return 105**2*15**2*A*A*B*B/(2*np.pi**2*a**8*b**6*12*cutoff**12)


def position_tail(m,T,r=1.,a=.25,b=.1,order=20):
    if T-2*b<=r+2*a:raise ValueError('not wholly inside the future cone')
    if m==0:return 0.
    w,ww=rule(order,0,2);v,vv=rule(order,0,2);z,zz=rule(order,-1,1)
    # Split the time difference at zero; both convolution pieces are polynomials.
    v=np.concatenate([-v,v]);vv=np.concatenate([vv,vv])
    u2=(T+b*v[None,:,None])**2-(r*r+(a*w[:,None,None])**2+2*r*a*w[:,None,None]*z[None,None,:])
    u=np.sqrt(u2)
    val=-m*j1(m*u)/(4*np.pi*u)
    weights=(4*np.pi*w*w*space_convolution(w)*ww)[:,None,None]*(time_convolution(v)*vv)[None,:,None]*zz[None,None,:]/2
    return float(np.sum(weights*val))


def self_response(m,a=.25,b=.1,cutoff=400.,order=32):
    """K_BB = integral f_B G_R f_B; only the positive half of the time convolution."""
    x,w=leggauss(order);edges=np.arange(int(cutoff)+1)
    k=((edges[:-1,None]+edges[1:,None])/2+x/2).ravel()
    kw=np.broadcast_to(w/2,(int(cutoff),order)).ravel()
    om=np.sqrt(k*k+m*m)
    v,vw=rule(160,0,2)
    inner=np.sin(b*om[:,None]*v[None,:])@(vw*time_convolution(v))
    core=kw*k*k/om*space_ft(a*k)**2
    K=float(np.sum(core*inner)/(2*np.pi**2))
    H=float(np.sum(core*time_ft(b*om)**2)/(4*np.pi**2))
    return dict(K_BB=K,H_BB=H)
