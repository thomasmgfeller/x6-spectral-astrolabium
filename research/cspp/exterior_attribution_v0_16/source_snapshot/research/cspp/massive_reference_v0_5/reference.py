"""Validated off-centre compact-source KG amplitudes in source coordinates."""
import sys
from pathlib import Path
from functools import lru_cache
import numpy as np
from flint import arb, acb, ctx

HERE = Path(__file__).resolve().parent
BASE = HERE.parent/'certified_budget_v0_3'
sys.path.append(str(BASE))
import balls
import source as previous


def integrate(f, a, b):
    # Return nonfinite balls to the calling integrator, never raise in callbacks.
    return acb.integral(f, a, b, abs_tol=arb('1e-25'), rel_tol=arb('1e-25'),
                        eval_limit=20000, depth_limit=100)


def geometry(point):
    if len(point) != 4 or not all(np.isfinite(float(v)) for v in point):
        raise ValueError('finite four-coordinate point required')
    tau = abs(arb(float(point[0]))+1)
    x = [arb(float(v)) for v in point[1:]]
    R = sum(v*v for v in x).sqrt()
    return tau, x, R


def spherical_mean(point, A):
    a,k,hc=previous.parameters(); tau,x,R=geometry(point)
    b=a*(1-hc).sqrt()
    if tau == 0:
        if R >= a: return acb(0), arb(0)
        return A*(-1/(1-R*R/(a*a))).exp()*acb(0,k*x[2]).exp(), arb(0)
    if abs(R-tau)>=a: return acb(0),arb(0)
    if R == 0:
        return acb(A*(-1/(1-tau*tau/(a*a))).exp()*(k*tau).sinc()),arb(0)
    c=x[2]/R
    upper=(b*b-R*R-tau*tau)/(2*R*tau)
    tail=A*(-1/hc).exp()
    if upper <= -1: return acb(0),tail
    if upper > 1: upper=arb(1)
    def f(u,analytic):
        h=1-(R*R+tau*tau+2*R*tau*u)/(a*a)
        if h.contains(0): return acb('nan')
        return A/2*(-1/h).exp()*acb(0,1).__mul__(k*(x[2]+tau*c*u)).exp()*(-(k*tau)**2*(1-c*c)*(1-u*u)/4).hypgeom_0f1(1)
    return integrate(f,-1,upper),tail


def volume(point,m,A):
    """Return (4 pi)^-1 integral_source f(y) 0F1(3;-m²s²/4) d³y."""
    a,k,hc=previous.parameters();tau,x,R=geometry(point);b=a*(1-hc).sqrt()
    if R == 0: raise ValueError('volume route requires noncentral point')
    c=x[2]/R
    if R >= tau+a: return acb(0),arb(0)
    lo=max(arb(0),R-tau);hi=min(b,R+tau);split=tau-R
    tail=A*a**3/3*(-1/hc).exp()
    if lo>=hi: return acb(0),tail
    edges=[lo]+([split] if lo<split<hi else [])+[hi]
    total=acb(0)
    for l,u in zip(edges[:-1],edges[1:]):
        # A nonexact ball is not <= itself. Decide topology at the segment midpoint.
        full=(l+u)/2 < split
        def f(s,analytic):
            h=1-s*s/(a*a)
            if h.contains(0): return acb('nan')
            v0=acb(-1) if full else (s/(2*R) if tau==R else (R*R+s*s-tau*tau)/(2*R*s))
            def g(q,unused):
                v=v0+(1-v0)*q
                ss=tau*tau-R*R-s*s+2*R*s*v
                return ((1-v0)*(acb(0,1)*k*c*s*v).exp()
                        *(-k*k*s*s*(1-c*c)*(1-v*v)/4).hypgeom_0f1(1)
                        *(-m*m*ss/4).hypgeom_0f1(3))
            # For complex outer balls, directly enclose the integral over q∈[0,1].
            # This is an enclosure of an analytic function, not a midpoint sample.
            broad=analytic or s.real.rad()>arb('1e-10') or s.imag.rad()>arb('1e-10')
            inner=g(acb(arb('0.5','0.5')),False) if broad else integrate(g,0,1)
            return s*s*A/2*(-1/h).exp()*inner
        total+=integrate(f,l,u)
    return total,tail


def off_center(point,m,A):
    if m not in (1,2): raise ValueError('fixed massive matrix supports m=1,2')
    tau,x,R=geometry(point)
    if R==0: raise ValueError('use the existing centre reference')
    K,Ktail,method=previous.kirchhoff(point,A)
    if R>=tau+previous.parameters()[0] or tau==0:
        return K,{'kirchhoff_tail':Ktail,'surface_tail':arb(0),'volume_tail':arb(0),
                  'quadrature_component_radius_upper':max(K.real.rad(),K.imag.rad()),
                  'method':'INITIAL_OR_CAUSAL_SUPPORT'}
    M,Mtail=spherical_mean(point,A);V,Vtail=volume(point,m,A)
    surface=m*m*tau*tau/2;factor=arb(m)**4*tau/8
    # K already contains its old quadrature AND analytic edge radius.
    core=K-surface*M+factor*V
    extra=surface*Mtail+factor*Vtail
    result=balls.inflate(core,extra)
    if not result.is_finite(): raise ArithmeticError('nonfinite enclosure')
    # Conservative error accounting: K's old edge radius is also present in this
    # numerical bound. It is explicitly flagged rather than subtracted unsafely.
    return result,{'kirchhoff_tail':Ktail,'surface_tail':surface*Mtail,
        'volume_tail':factor*Vtail,
        'quadrature_component_radius_upper':max(core.real.rad(),core.imag.rad()),
        'quadrature_bound_includes_legacy_K_tail_and_normalization':True,
        'method':'SOURCE_CENTERED_KG_VOLUME_AND_LIGHTCONE_SURFACE'}


def compute():
    old=np.load(HERE.parent/'scale_calibration_v0_2/results/source.npz')
    query=old['query'][:28];A=previous.normalization(ctx.prec)[0];rows=[]
    for i,p in enumerate(query):
        if np.all(p[1:]==0):continue
        for m in (1,2):
            z,errors=off_center(p,m,A)
            status='WITHIN_RADIUS_GOAL' if max(z.real.rad(),z.imag.rad())<=arb('1e-12') else 'HOLD'
            rows.append({'probe_index':i,'mass':m,'point':p.tolist(),'value':balls.encode(z),
                         'errors':{k:balls.encode(v) if isinstance(v,arb) else v for k,v in errors.items()},
                         'old_Green_absolute_difference_bound':balls.encode((z-acb(complex(old['green'][-1,i,m]))).abs_upper()),
                         'enclosure_status':status})
        print('enclosed probe',i,flush=True)
    if len(rows)!=50:raise RuntimeError('wrong off-centre matrix')
    return {'schema':'cspp.massive-reference/0.5','precision_bits':ctx.prec,
            'normalization_A':balls.encode(A),'rows':rows,'new_amplitudes':50,
            'total_fixed_probe_amplitudes_with_v0_3':84,
            'all_fixed_probe_values_enclosed':all(r['enclosure_status']=='WITHIN_RADIUS_GOAL' for r in rows),
            'scope':'28 fixed propagation/detector point probes times masses 0,1,2; not all 284 archived queries',
            'G1':'HOLD','G2':'NOT_RUN','G3':'NOT_RUN','full_Dirac_detector_reference':'HOLD'}
