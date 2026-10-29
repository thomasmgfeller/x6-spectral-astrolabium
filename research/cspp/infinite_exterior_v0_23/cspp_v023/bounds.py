"""Contour power envelopes and correlation-safe near/far infinite history bounds."""
from functools import lru_cache
from fractions import Fraction as F
from flint import arb,ctx
from common import ball,require,enc,choose

COEFF=[F(1),F(9),F(8),F(4,3)]
SQUARED=[sum((COEFF[i]*COEFF[j] for i in range(4) for j in range(4) if i+j==k),F(0)) for k in range(7)]
SGRID=list(range(8,129,4))
EDGES=[F(5)]+[F(2)**j for j in range(3,49)]

@lru_cache(None)
def gaussian_moment(power,lower,squared,bits):
    require(ctx.prec==bits and lower>=0,'moment precision and domain')
    c=arb(1)/(64 if squared else 128);z=c*ball(lower)*ball(lower)
    co=SQUARED if squared else COEFF
    return sum((ball(a)*(arb(1)/2)**j*z.gamma_upper(arb(power+2*j+1)/2) if squared else ball(a)*z.gamma_upper(arb(power+2*j+1)/2) for j,a in enumerate(co)),arb(0))/(2*c**(arb(power+1)/2))

def kernel_moment(power,L,S,D,squared=False):
    """Integral_(sqrt(L))^infinity s^power H_S(s)^(1 or 2) ds."""
    kappa=arb('4976184375/4294967296');start=ball(L).sqrt();D=D*D if squared else D;kappa=kappa*kappa if squared else kappa
    if L<S*S:
        flat=kappa*(arb(S)**(power+1)-ball(L)**(arb(power+1)/2))/(power+1)
        return flat+D*gaussian_moment(power,F(S),squared,ctx.prec)
    # sqrt(L) can be irrational; use gamma at c*L directly rather than cache a float.
    c=arb(1)/(64 if squared else 128);co=SQUARED if squared else COEFF;z=c*ball(L)
    tail=sum((ball(a)*(arb(1)/2)**j*z.gamma_upper(arb(power+2*j+1)/2) if squared else ball(a)*z.gamma_upper(arb(power+2*j+1)/2) for j,a in enumerate(co)),arb(0))/(2*c**(arb(power+1)/2))
    return D*tail

def full_I0(S,D):return arb('4976184375/4294967296')*S+D*gaussian_moment(0,F(S),False,ctx.prec)

def power_integral(p,L,U,sigma):
    """Exact integral of (tau+sigma) tau^-p, p a rational quarter."""
    p=ball(p);L=ball(L)
    if U is None:
        require(p>2,'integrable last power')
        return L**(2-p)/(p-2)+sigma*L**(1-p)/(p-1)
    U=ball(U)
    return (U**(2-p)-L**(2-p))/(2-p)+sigma*(U**(1-p)-L**(1-p))/(1-p)

class BoundEngine:
    def __init__(self,prior):
        self.M=arb(prior['source_M0']);self.norm=arb(prior['norm_squared']['0']).sqrt()
        a=1/(2*arb.pi()).sqrt();self.beta=a/(16*(1+a));self.rho=3/arb.pi();self.kappa=arb('4976184375/4294967296');self.gamma=self.beta*self.kappa
        self.prefactors={}
        for J in range(1,35):
            p=F(J)-F(3,4);norm=arb(prior['norm_squared'][str(J)]).sqrt();g=ball(2*J-F(3,2)).gamma().sqrt()/(2*arb.pi())
            for j in range(1,16):
                delta=arb(j)/16
                self.prefactors[J,j]=(delta/2).exp()*(1+delta*delta)**J*norm*g/(delta*(1-delta*delta))**ball(p)

    def contour(self,C):
        vals={};audit=[]
        for J in range(1,35):
            candidates={j:v*(arb(j)*C/16).exp() for (jj,j),v in self.prefactors.items() if jj==J}
            j,v=choose(candidates);vals[J]=v
            audit.append({'J':J,'p':str(F(J)-F(3,4)),'delta':str(F(j,16)),'C_power_upper':enc(v)})
        return vals,audit

    def near_bins(self,C,sigma):
        if C<=-arb(1)/2:
            return [arb(0) for _ in EDGES],[{'near_region':'EMPTY_ON_SOURCE_SUPPORT'}]
        coeff,audit=self.contour(C);vals=[];rows=[]
        for i,L in enumerate(EDGES):
            U=EDGES[i+1] if i+1<len(EDGES) else None
            candidates={J:c*power_integral(F(J)-F(3,4),L,U,sigma) for J,c in coeff.items() if U is not None or J>=3}
            if U is not None:candidates[0]=self.M*((ball(U)**2-ball(L)**2)/2+sigma*ball(U-L))
            J,value=choose(candidates);vals.append(value);rows.append({'L':str(L),'U':str(U) if U else 'infinity','J':J,'weighted_field_integral_upper':enc(value)})
        return vals,{'powers':audit,'bins':rows}

    def far(self,L,S,D,sigma):
        m={j:kernel_moment(j,L,S,D) for j in [0,2,4]}
        l1=6*self.beta*self.M*((m[4]-ball(L)**2*m[0])/2+sigma*(m[2]-ball(L)*m[0]))
        q={j:kernel_moment(j,L,S,D,True) for j in [0,2,4,6,8]};H=arb(S*S);l=ball(L)
        coeff=[H*H*sigma,(H*H+2*H*sigma)/2,(2*H+sigma)/3,arb(1)/4]
        # Exactly integrate the nonnegative time polynomial before taking square roots.
        polynomial=sum((c*(q[2*(i+1)]-l**(i+1)*q[0]) for i,c in enumerate(coeff)),arb(0))
        require(polynomial>=0 and l1>=0,'nonnegative exact far integrals')
        l2=self.beta*self.rho*self.norm*(2*arb.pi()*polynomial/(l+H)).sqrt()
        return min(l1.upper(),l2.upper()),{'L1':l1,'L2':l2,'polynomial_integral':polynomial}

    def endpoint(self,C,sigma,qcap,include_tail_grid=False):
        require(sigma>=0 and qcap>=0,'endpoint domain')
        C=C.upper();sigma=sigma.upper();D=16*qcap.exp()
        bins,audit=self.near_bins(C,sigma);suffix=[];acc=arb(0)
        for v in reversed(bins):acc+=v;suffix.append(acc)
        suffix=list(reversed(suffix));cutoffs=[(F(5),0)]
        if include_tail_grid:cutoffs += [(F(2)**j,EDGES.index(F(2)**j)) for j in range(3,41)]
        out=[]
        for L,index in cutoffs:
            candidates={};parts={}
            for S in SGRID:
                near=6*self.beta*full_I0(S,D)*suffix[index];far,comparison=self.far(L,S,D,sigma)
                candidates[S]=near+far;parts[S]={'near_upper':enc(near),'far_upper':enc(far),'far_L1_upper':enc(comparison['L1']),'far_L2_upper':enc(comparison['L2'])}
            S,bound=choose(candidates)
            out.append({'tau_cutoff':str(L),'selected_S':S,'direct_tail_upper':enc(bound),**parts[S]})
        return {'C_upper':enc(C),'sigma_upper':enc(sigma),'q_overlap_cap':enc(qcap),'D_conditional':enc(D),'near_audit':audit,'tail_bounds':out}
