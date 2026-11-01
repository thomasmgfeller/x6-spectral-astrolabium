"""Free scalar control models; hbar=c=1; all lengths relative to ell0."""
from math import exp, sqrt, sin
from scipy.integrate import quad
from scipy.special import dawsn


def positive_integral(mu, r):
    if min(mu,r)<0: raise ValueError('nonnegative mass and separation required')
    def f(z):
        if z==1: return 1.0 if mu==0 else 0.0
        return exp(-mu*mu*z*z/(1-z*z)-r*r*(1-z*z)/4)/2
    return quad(f,0,1,epsabs=2e-13,epsrel=2e-13)[0]


def coherence(mass,r,width=1):
    if width<=0:raise ValueError('positive width required')
    mu,R=mass*width,r/width
    return positive_integral(mu,R)/positive_integral(mu,0)


def momentum_integral(mu,r,t=0,imaginary=False):
    from math import cos
    def f(k):
        omega=sqrt(k*k+mu*mu)
        if omega==0:return 0.0
        sinc=1 if k*r==0 else sin(k*r)/(k*r)
        phase=sin(omega*t) if imaginary else cos(omega*t)
        return k*k/omega*exp(-k*k)*sinc*phase
    return quad(f,0,12,epsabs=2e-13,epsrel=2e-13,limit=200)[0]


def scaled_kvf(mass,r,width=1,eta=.5):
    """Return 4*pi^2*ell0^2 times (HAA,HBB,HAB,DeltaAB), same time centres."""
    mu=mass*width
    factor=exp(-(eta*mu)**2)/(width*width)
    a=factor*positive_integral(mu,0)
    c=factor*positive_integral(mu,r/width)
    return [a,a,c,0.0]


def massless_closed_form(r):
    return 1.0 if r==0 else 2*dawsn(r/2)/r
