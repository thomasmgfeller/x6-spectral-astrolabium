"""Initial states and independent analytic image controls; kappa=1."""
import numpy as np
from scipy.integrate import quad


def full(q, case, time=0., derivative=False):
    h, s2 = case['hbar'], case['sigma']**2
    q=np.asarray(q)
    result=np.zeros_like(q,dtype=complex)
    D=1-1j*h*time/s2
    for c in case['components']:
        centre=c['q']-2*c['p']*time
        v=(c['amplitude']*np.exp(1j*c['phase'])
           *(2*np.pi*s2)**(-.25)/np.sqrt(D)
           *np.exp(-(q-centre)**2/(4*s2*D)+1j*c['p']*(q-c['q'])/h+1j*c['p']**2*time/h))
        if derivative:v*=-(q-centre)/(2*s2*D)+1j*c['p']/h
        result+=v
    return result


def image_state(q,case,time=0.,bc='D',derivative=False):
    sign=-1 if bc=='D' else 1
    if derivative:sign=-sign
    return full(q,case,time,derivative)+sign*full(-np.asarray(q),case,time,derivative)


def integrate(function,case,L=32.):
    points=sorted({max(0.,min(L,c['q']+m*case['sigma']))
                   for c in case['components'] for m in (-6,-2,0,2,6)})
    return quad(function,0,L,points=points,epsabs=2e-12,epsrel=2e-12,limit=500)


def early_moments(case,bc='D'):
    psi=lambda q:image_state(q,case,bc=bc)
    prime=lambda q:image_state(q,case,bc=bc,derivative=True)
    norm,en=integrate(lambda q:float(abs(psi(q))**2),case)
    a,ea=integrate(lambda q:float(q*q*abs(psi(q))**2),case)
    j,ej=integrate(lambda q:float(2*case['hbar']*q*np.imag(np.conj(psi(q))*prime(q))),case)
    e,ee=integrate(lambda q:float(case['hbar']**2*abs(prime(q))**2),case)
    a,j,e=a/norm,j/norm,e/norm
    return {'norm_raw':norm,'A':a,'J':j,'E':e,'T_b':j/(4*e),
            'V_b':a-j*j/(4*e),'uncertainty_lower_bound':case['hbar']**2/(4*e),
            'quadrature_error_estimates':[en,ea,ej,ee]}
