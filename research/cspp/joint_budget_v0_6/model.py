"""Joint rho/ell/H certificates for a fixed L=2 Gaussian necessary witness."""
from functools import lru_cache
from fractions import Fraction
from math import factorial
from pathlib import Path
import sys
from flint import arb,ctx
HERE=Path(__file__).resolve().parent
sys.path.append(str(HERE.parent/'certified_budget_v0_3'))
sys.path.append(str(HERE.parent/'variance_budget_v0_4'))
import balls
import budget as previous_mean
import variance


def a(x):
    if isinstance(x,Fraction):return arb(x.numerator)/x.denominator
    return arb(x)


def gamma_moment(j,absolute=False):
    if not absolute:
        return -a(j*(j-1)*(j-2))/12*(a(j+1)/2).gamma()
    coeff=[a(1),a(9),a(8),a(Fraction(4,3))]
    return sum(c*(a(j+2*l+1)/2).gamma()/2 for l,c in enumerate(coeff))


def outside_boundary(ell,H,L=2,order=12):
    """Signed mu_infinity-mu_DH; finite Gamma series + two absolute remainders.

    Extend y from [0,c*v²] to [0,infinity), expand exp[-y²/(4L²c²v²)],
    and bound the artificial wedge separately. No numerical double quadrature.
    """
    ell,H,L=map(a,(ell,H,L))
    if not(ell>0 and H>0 and L>0) or order<0:raise ValueError('positive scales and nonnegative order required')
    q=ell**-4;c=(arb.pi()*q/24).sqrt();d=4*L*L;x=H*H/d
    G=[(-x).exp(),x.expint(1)]
    for j in range(2,order+5):G.append((x**(1-j)*(-x).exp()-G[-1])/(j-1))
    def I(j):return d**(1-j)/2*G[j]  # integral v^(1-2j) exp(-v²/d) dv
    total=arb(0)
    for n in range(order+1):
        total+=(-1)**n/(a(factorial(n))*(d*c*c)**n)*(gamma_moment(2*n)*I(n)
             -2/c*gamma_moment(2*n+1)*I(n+1)+gamma_moment(2*n+2)/c**2*I(n+2))
    n=order+1
    rem=(gamma_moment(2*n,True)*I(n)+2/c*gamma_moment(2*n+1,True)*I(n+1)
          +gamma_moment(2*n+2,True)/c**2*I(n+2))/(factorial(n)*(d*c*c)**n)
    Y=c*H*H;T=variance.gaussian_tail_moments(Y,8)
    U=lambda j:T[j]+9*T[j+2]+8*T[j+4]+a(Fraction(4,3))*T[j+6]
    wedge=U(0)*I(0)+2/c*U(1)*I(1)+U(2)/c**2*I(2)
    pref=4*arb.pi().sqrt()*q
    error=pref*(rem.abs_upper()+wedge.abs_upper())
    return pref*total+arb(0,error.abs_upper()),{'series_remainder':pref*rem.abs_upper(),
        'artificial_wedge':pref*wedge.abs_upper(),'order':order}


def lower_box(ell,H,vl,vh,L=2):
    """v0.4 first-chaos proof with the stated radial shell; fail closed."""
    ell,H,vl,vh,L=map(a,(ell,H,vl,vh,L))
    if not(ell>0 and H>0 and L>0 and vl>0 and vh>vl):raise ValueError('positive valid lower-box inputs required')
    q=ell**-4;c=(arb.pi()*q/24).sqrt()
    xl,xh=a(3),a('31/10');gap=vl-xh/(c*vl)
    if not(ell>0 and L>0 and vl>0 and vh>vl and gap>0 and vh<H):return None
    T=variance.gaussian_tail_moments(xl,8)
    tail=sum(a(coef)*(T[k+2]-2*xl*T[k+1]+xl*xl*T[k]) for k,coef in [(0,10),(2,25),(4,12),(6,Fraction(4,3))])
    indirect=12/gap*arb.pi().sqrt()*L*(vl/(2*L)).erfc()/(4*xl)*tail
    direct=404*(-(vh*vh+(xh/(c*vl))**2)/(4*L*L)-xh*xh).exp()
    response=direct-indirect
    if not response>0:return None
    vol=(xh-xl)*(vh-vl)*arb.pi()/(2*c)*gap**2/vh
    lower=a(Fraction(8,3))*q**3*vol*response**2
    return lower,{'vl':vl,'vh':vh,'direct_min':direct,'indirect_max':indirect,'response_min':response,'box_volume_min':vol}


def volume(H):return arb.pi()*a(H)**4/24


def encode(x):return balls.encode(a(x))


def finite_mode_direct(ell,H,omega=0,k=0,L=2):
    """Independent triangular null-coordinate quadrature, no domain truncation."""
    from flint import acb
    ell,H,L,omega,k=map(a,(ell,H,L,omega,k))
    if not(ell>0 and H>0 and L>0 and omega.is_finite() and k.is_finite()):raise ValueError('finite modes and positive scales required')
    q=ell**-4;c2=arb.pi()*q/24
    def integrate(f,left,right):
        return acb.integral(f,left,right,abs_tol=arb('1e-19'),rel_tol=arb('1e-19'),eval_limit=20000,depth_limit=80)
    def f(v,analytic):
        def g(z,unused):
            xi=c2*v**4*z**2
            P=1-9*xi+8*xi**2-4*xi**3/3
            return (arb.pi()/2*v**3*(1-z)**2*(-xi-v**2*(1+z**2)/(4*L**2)).exp()*P
                    *(acb(0,1)*omega*v*(1+z)/2).exp()*(k*v*(1-z)/2).sinc())
        if analytic or v.real.rad()>arb('1e-10') or v.imag.rad()>arb('1e-10'):
            return g(acb(arb('1/2','1/2')),False)
        return integrate(g,0,1)
    out=4*(q/6).sqrt()*(-1+q*integrate(f,0,H))
    if not out.is_finite() or max(out.real.rad(),out.imag.rad())>arb('1e-12'):
        raise ArithmeticError('finite mean quadrature failed radius goal')
    return out


def finite_mean_direct(ell,H,L=2):
    value=finite_mode_direct(ell,H,L=L)
    if not value.imag.contains(0):raise ArithmeticError('non-real witness mean')
    return value.real


def boundary_direct(ell,H,L=2,T=32):
    """Independent bounded rectangular double integral for c*H²>=8.

    Integrates y in [0,8], v in [H,T]; old absolute cone-tail bounds control
    the two omitted pieces. This is a validation route, not the Gamma series.
    """
    from flint import acb
    ell,H,L,T=map(a,(ell,H,L,T));q=ell**-4;c=(arb.pi()*q/24).sqrt()
    if not(c*H*H>=8 and T>H and ell>0):raise ValueError('rectangle proof requires cH²>=8 and T>H')
    def integral(f,left,right):
        return acb.integral(f,left,right,abs_tol=arb('1e-24'),rel_tol=arb('1e-24'),eval_limit=10000,depth_limit=80)
    def f(y,analytic):
        def g(v,unused):
            s=y/(c*v)
            return (v-s)**2/v*(-(v*v+s*s)/(4*L*L)).exp()
        if analytic or y.real.rad()>arb('1e-10') or y.imag.rad()>arb('1e-10'):
            inner=acb(0)
            for j in range(32):
                mid=H+(T-H)*arb(2*j+1)/64;rad=(T-H)/64
                inner+=g(acb(arb(mid,rad.abs_upper())),False)*(T-H)/32
        else:inner=integral(g,H,T)
        xi=y*y
        return (-xi).exp()*(1-9*xi+8*xi*xi-4*xi**3/3)*inner
    core=4*arb.pi().sqrt()*q*integral(f,0,8)
    tails=variance.gaussian_tail_moments(arb(8),6)
    highy=8*arb.pi().sqrt()*q*L**2*(tails[0]+9*tails[2]+8*tails[4]+a(Fraction(4,3))*tails[6])
    highv=previous_mean.gaussian_tail(ell,T,L)
    out=core.real+arb(0,(highy+highv).abs_upper())
    if not core.imag.contains(0) or not out.is_finite() or not out.rad()<arb('1e-12'):
        raise ArithmeticError('independent boundary quadrature too broad')
    return out
