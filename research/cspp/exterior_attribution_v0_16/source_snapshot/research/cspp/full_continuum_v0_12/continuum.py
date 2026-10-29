"""Independent full spacetime detector average for the unchanged compact KG source.

Time integration is an exact sine-propagator endpoint difference. Detector
space and source azimuth are integrated analytically. Bessel truncation and
source-edge truncation have separate uniform bounds; remaining radial
integrals use validated Acb quadrature with entire/meromorphic callbacks.
"""
from functools import lru_cache
from math import comb, factorial
from flint import arb, acb, fmpq as Q, fmpq_poly as Poly, ctx


def require(ok,msg):
    if not ok:raise ArithmeticError(msg)


def integral(f,lo,hi,tol='1e-22'):
    z=acb.integral(f,acb(lo),acb(hi),abs_tol=arb(tol),rel_tol=arb(tol),eval_limit=200000,depth_limit=100)
    require(z.is_finite(),'QUADRATURE_HOLD: nonfinite result')
    return z


def inflate(z,error):
    er=arb(0,arb(error).abs_upper())
    return acb(z)+acb(er,er)


@lru_cache(None)
def detector_poly(tau_string,regime,degree=16,mass=1):
    """4 R times the spatial integral of the truncated sine Green kernel."""
    require(regime in ('full','partial','outside'),'kernel regime')
    if regime=='outside':return Poly([])
    tau=Q(tau_string);b=Q(1,2);R=Poly([0,1]);low=R-b
    upper=R+b if regime=='full' else Poly([tau])
    p=Poly([]) if regime=='full' else b*b-(R-tau)**2
    for n in range(degree+1):
        term=Poly([])
        for j in range(n+1):
            coeff=Q(comb(n,j))*(-1)**j*tau**(2*(n-j))
            def primitive(r):
                return ((b*b-R*R)*r**(2*j+2)/Q(2*j+2)
                        +2*R*r**(2*j+3)/Q(2*j+3)-r**(2*j+4)/Q(2*j+4))
            term+=coeff*(primitive(upper)-primitive(low))
        p-=Q(mass*mass,2)*(-Q(mass*mass,4))**n/Q(factorial(n)*factorial(n+1))*term
    return p


def gaussian_moments(lo,hi,n,k=4,d=Q(3,2)):
    """Entire moments integral_l^u R^n exp(-ik R²/(2d)) dR."""
    lo=acb(lo);hi=acb(hi)
    if k==0:return [(hi**(j+1)-lo**(j+1))/(j+1) for j in range(n+1)]
    beta=acb(0,-Q(k)/(2*d));root=(-beta).sqrt()
    el=(beta*lo*lo).exp();eh=(beta*hi*hi).exp()
    out=[arb.pi().sqrt()/(2*root)*((root*hi).erf()-(root*lo).erf())]
    if n:out.append((eh-el)/(2*beta))
    for j in range(2,n+1):out.append((hi**(j-1)*eh-lo**(j-1)*el-(j-1)*out[j-2])/(2*beta))
    return out


def polynomial_integral(poly,lo,hi,k=4):
    if not len(poly):return acb(0)
    moments=gaussian_moments(lo,hi,len(poly)-1,k)
    return sum(acb(c)*z for c,z in zip(poly.coeffs(),moments))


def bessel_series_tail(tau,degree=16,mass=1):
    x=arb(mass*mass)*arb(tau)**2/4
    first=x**(degree+1)/(factorial(degree+1)*factorial(degree+2))
    ratio=x/((degree+2)*(degree+3))
    require(ratio<1,'Bessel geometric remainder condition')
    return first/(1-ratio)


def endpoint(tau_string,degree=16,hcut_string='1/64',mass=1,k=4):
    """Integral_D S_m(tau) f_scaled dx, f_scaled=e*exp(-1/h)*exp(ikz)."""
    tau=Q(tau_string);d=Q(3,2);b=Q(1,2);hc=arb(hcut_string)
    require(tau>=0 and hc>0 and hc<1,'positive time and source cutoff')
    core_radius=arb('1/2')*(1-hc).sqrt()
    cuts=[tau-b,tau+b]
    splits=sorted(set(abs(c-d) for c in cuts if 0<abs(c-d)<Q(1,2)))
    edges=[arb(0)]+[arb(s) for s in splits if arb(s)<core_radius]+[core_radius]
    total=acb(0);segments=[]
    for sl,su in zip(edges[:-1],edges[1:]):
        sm=(sl+su)/2
        # Topology is decided on the real segment, outside analytic callbacks.
        inside=[c for c in cuts if arb(d)-sm<arb(c)<arb(d)+sm]
        labels=['left']+inside+['right']
        rmid=[arb(d)-sm]+[arb(c) for c in inside]+[arb(d)+sm]
        regs=[]
        for l,u in zip(rmid[:-1],rmid[1:]):
            m=(l+u)/2
            regs.append('full' if m<arb(tau-b) else 'outside' if m>arb(tau+b) else 'partial')
        polys=[detector_poly(str(tau),reg,degree,mass) for reg in regs]
        def f(s,analytic):
            h=1-4*s*s
            if h.contains(0):return acb('nan')
            rr=[acb(d)-s]+[acb(c) for c in inside]+[acb(d)+s]
            angular=sum(polynomial_integral(p,l,u,k) for p,l,u in zip(polys,rr[:-1],rr[1:]))
            return s*(1-1/h).exp()*(acb(0,Q(k)/(2*d))*(d*d+s*s)).exp()*angular
        z=integral(f,sl,su)
        total+=arb.pi()/(2*arb(d))*z
        segments.append({'source_radius_bounds':[str(sl),str(su)],'regimes':regs})
    volume=arb.pi()/6;t=arb(tau)
    # Average over detector volume; uniform bounds before averaging over time.
    source_tail=volume*(t+mass*mass*t**3/6)*(1-1/hc).exp()
    series_tail=volume*mass*mass*t**3/6*bessel_series_tail(t,degree,mass)
    return {'core':total,'source_tail':source_tail,'series_tail':series_tail,'segments':segments}


def normalization(hcut_string='1/64'):
    hc=arb(hcut_string);b=arb('1/2')*(1-hc).sqrt()
    def f(s,analytic):
        h=1-4*s*s
        if h.contains(0):return acb('nan')
        return 4*arb.pi()*s*s*(-2/h).exp()
    core=integral(f,0,b)
    require(core.imag.contains(0),'real normalization integral')
    tail=arb.pi()/6*(-2/hc).exp()
    norm=core.real+arb(0).union(tail)
    require(norm>0,'positive original source norm')
    return 1/norm.sqrt(),core.real,tail


def full_detector(bits=128,degree=16,hcut='1/64'):
    ctx.prec=bits
    endpoints={t:endpoint(t,degree,hcut) for t in ['7/4','2','9/4']}
    A,norm,normtail=normalization(hcut)
    windows=[]
    for lo,hi in [('7/4','2'),('2','9/4')]:
        a,b=endpoints[lo],endpoints[hi];den=(arb(hi)-arb(lo))*arb.pi()/6
        core=(b['core']-a['core'])/den
        edge=(b['source_tail']+a['source_tail'])/den
        series=(b['series_tail']+a['series_tail'])/den
        certified=inflate(core,edge+series)
        windows.append({'initial_time_shifted_window':[lo,hi],'normalized_core':core,
                        'normalized_value':certified,'physical_value':certified*A/arb(1).exp(),
                        'source_tail_upper':edge,'bessel_tail_upper':series,
                        'quadrature_and_arithmetic_radius':max(core.real.rad(),core.imag.rad())})
    return {'endpoints':endpoints,'windows':windows,'normalization_A':A,
            'normalization_core':norm,'normalization_tail_upper':normtail}
