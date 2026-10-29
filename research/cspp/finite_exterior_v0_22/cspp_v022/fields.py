"""Uniform compact-source KG envelopes, including the complete wavefront."""
from fractions import Fraction as F
from functools import lru_cache
from flint import arb,acb,ctx
from common import ball,require

@lru_cache(None)
def moments(L2,bits):
    """(b(L), int_L^a r b dr, int_L^a r^3 b dr)."""
    require(bits==ctx.prec and F(0)<=L2<=F(1,4),'moment domain')
    if L2==F(1,4):return arb(0),arb(0),arb(0)
    h=ball(1-4*L2);z=1/h;e=arb(1).exp();b=(1-z).exp()
    J1=e*z.gamma_upper(-1)/8
    J3=e*(z.gamma_upper(-1)-z.gamma_upper(-2))/32
    require(b>0 and J1>0 and J3>0,'positive source moments')
    return b,J1,J3

@lru_cache(None)
def J2(L,bits):
    require(bits==ctx.prec and 0<=L<=F(1,2),'radial source moment')
    if L==F(1,2):return arb(0)
    edge=(arb(63)/64).sqrt()/2
    tail=(1-arb(64)).exp()/24
    if ball(L)>=edge:return arb(0).union(tail)
    def f(r,analytic):
        h=1-4*r*r
        if h.contains(0):return acb('nan')
        return r*r*(1-1/h).exp()
    z=acb.integral(f,acb(ball(L)),acb(edge),abs_tol=arb('1e-30'),rel_tol=arb('1e-30'))
    require(z.is_finite() and z.imag.contains(0),'source moment quadrature')
    return z.real+arb(0).union(tail)

def source_ball_mass(tau,R):
    """Exact radial integral of b over B(x,tau); analytic omitted-edge bound."""
    require(tau>0 and R>=0,'source-ball domain')
    total=4*arb.pi()*J2(F(0),ctx.prec)
    if R+F(1,2)<=tau:return total
    if R>=tau+F(1,2):return arb(0)
    require(R>0,'noncentral partial source ball')
    L=abs(R-tau);_,J1,J3=moments(L*L,ctx.prec)
    j2=J2(L,ctx.prec)
    core=4*arb.pi()*(J2(F(0),ctx.prec)-j2) if tau>R else arb(0)
    partial=arb.pi()/ball(R)*(ball(tau*tau-R*R)*J1+2*ball(R)*j2-J3)
    result=core+partial
    require(result.is_finite(),'finite source intersection mass')
    return result

def absolute_radial_derivative(L2,delta):
    """int_L^a r b(r)/h(r)^2 * |r^2+delta| dr, exact closed form."""
    b,J1,_=moments(L2,ctx.prec);A0=b/8;A2=ball(L2)*b/8+J1/4
    if delta>=-L2:return A2+ball(delta)*A0
    if delta<=F(-1,4):return -A2-ball(delta)*A0
    _,at_zero,_=moments(-delta,ctx.prec)
    return at_zero/2-A2-ball(delta)*A0

def envelope(c,M):
    t0,t1,r0,r1=[c[k] for k in ['tau0','tau1','r0','r1']]
    L1=4*arb.pi()*J2(F(0),ctx.prec)
    if c['kind']=='deep':
        amin=max(F(0),t0*t0-(r1+F(1,2))**2)
        V=ball(t1)*L1/(32*arb.pi())*(-ball(amin)/4).hypgeom_0f1(3)
        W=arb(0);mass=L1
    else:
        require(r0>=F(5,4) and t0>=F(7,4),'wavefront denominator and sign')
        L=max(F(0),r0-t1,t0-r1);b,J1,_=moments(L*L,ctx.prec)
        dlo=t0*t0-r1*r1;dhi=t1*t1-r0*r0
        jd0=absolute_radial_derivative(L*L,dlo);jd1=absolute_radial_derivative(L*L,dhi)
        derivative=max(jd0.upper(),jd1.upper())
        W=(ball(t1)/2-1/ball(t1)+4)*J1/(2*ball(r0))+2*derivative/(ball(r0)*ball(t0))
        mass=source_ball_mass(t1,r0)
        V=ball(t1)*max(arb(0),mass.upper())/(32*arb.pi())
    require(W>=0 and V>=0,'nonnegative complete KG bound')
    U=min(M.upper(),(W+V).upper())
    return U,{'wavefront_upper':W,'volume_upper':V,'source_ball_mass':mass}
