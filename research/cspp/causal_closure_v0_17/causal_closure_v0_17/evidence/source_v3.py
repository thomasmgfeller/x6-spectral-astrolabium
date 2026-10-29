"""Bounded compact-source normalization, all massless probes and massive centers.

The omitted bump edge is bounded analytically. Entire 0F1 expressions avoid
introducing square-root branch cuts into Bessel products at angular endpoints.
"""
from functools import lru_cache
import numpy as np
from flint import arb, acb, ctx
from balls import HERE, plan, integrate, inflate, real_value, encode

def parameters():
    p = plan()['source']
    a,k,h = arb(p['radius']), arb(p['carrier']), arb(p['bump_tail_h'])
    if not (a>0 and k>=0 and h>0 and h<=arb(1)/2):
        raise ValueError('source tail proof requires a>0, k>=0, 0<hcut<=1/2')
    return a,k,h

@lru_cache(None)
def normalization(bits):
    if bits != ctx.prec:
        raise ValueError('normalization precision mismatch')
    a, k, hcut = parameters()
    end = a*(1-hcut).sqrt()
    def f(r, analytic):
        h = 1-r*r/(a*a)
        if h.contains(0):
            return acb('nan')
        return 4*arb.pi()*r*r*(-2/h).exp()
    core = real_value(integrate(f, 0, end))
    tail = 4*arb.pi()*a**3/3*(-2/hcut).exp()
    I = core + arb(0, tail.upper())
    if not I > 0:
        raise ArithmeticError('normalization interval not positive')
    A = 1/I.sqrt()
    return A, I, tail

def kirchhoff(point, A):
    a, k, hcut = parameters()
    tau = abs(arb(float(point[0]))+1)
    x = [arb(float(v)) for v in point[1:]]
    R = sum(v*v for v in x).sqrt()
    if tau == 0:
        h = 1-R*R/(a*a)
        if h <= 0:
            return acb(0), arb(0), 'INITIAL_SUPPORT_ZERO'
        return A*(-1/h).exp()*(acb(0,k*x[2])).exp(), arb(0), 'INITIAL_VALUE'
    if abs(R-tau) >= a:
        return acb(0), arb(0), 'HUYGENS_SUPPORT_ZERO'
    if R == 0:
        h = 1-tau*tau/(a*a)
        b = (-1/h).exp()
        value = A*b*((k*tau).cos()-2*tau*tau/(a*a*h*h)*(k*tau).sinc())
        return acb(value), arb(0), 'CENTER_CLOSED_FORM'
    c = x[2]/R
    upper = (a*a*(1-hcut)-R*R-tau*tau)/(2*R*tau)
    if upper > 1:
        upper = arb(1)
    # Before azimuth integration |n_z|<=1 and |tau+R*mu|<=tau+R.
    # e^(-1/h)/h² increases on 0<h<=1/2; hcut=1/64.
    tail = A*(-1/hcut).exp()*(1+k*tau+2*tau*(tau+R)/(a*a*hcut*hcut))
    if upper <= -1:
        return inflate(0,tail), tail, 'TAIL_ONLY_ENCLOSURE'
    def f(mu, analytic):
        h = 1-(R*R+tau*tau+2*R*tau*mu)/(a*a)
        if h.contains(0):
            return acb('nan')
        w = (k*tau)**2*(1-c*c)*(1-mu*mu)
        j0 = (-w/4).hypgeom_0f1(1)
        qj1 = w/2*(-w/4).hypgeom_0f1(2)
        kernel = (1-2*tau*(tau+R*mu)/(a*a*h*h)+acb(0,1)*k*tau*c*mu)*j0-qj1
        return A/2*(-1/h).exp()*(acb(0,1)*k*(x[2]+tau*c*mu)).exp()*kernel
    return inflate(integrate(f,-1,upper),tail), tail, 'ANGULAR_INTEGRAL_WITH_BUMP_TAIL'

def massive_center(point, m, A):
    if any(v != 0 for v in point[1:]):
        raise ValueError('off-center massive reference is deliberately unsupported')
    a,k,hcut = parameters(); tau = abs(arb(float(point[0]))+1); m = arb(m)
    K,_,_ = kirchhoff(point,A)
    if tau == 0:
        return K, arb(0)
    if tau >= a:
        M = arb(0)
    else:
        h = 1-tau*tau/(a*a)
        M = A*(-1/h).exp()*(k*tau).sinc()
    end = a*(1-hcut).sqrt()
    if tau < end:
        end = tau
    def f(r, analytic):
        h = 1-r*r/(a*a)
        if h.contains(0):
            return acb('nan')
        # J2(m sqrt(s²))/s² = m²/8 * 0F1(3; -m²*s²/4), entire in s².
        bessel = m*m/8*(-m*m*(tau*tau-r*r)/4).hypgeom_0f1(3)
        return r*r*A*(-1/h).exp()*(k*r).sinc()*bessel
    value = K-m*m*tau*tau/2*M+m*m*tau*integrate(f,0,end)
    # |J2(z)| <= z²/8 for real z; |sinc|<=1, r<=a on the omitted support.
    tail = m**4*tau*A*a**3/24*(-1/hcut).exp()
    return inflate(value,tail),tail

def compute():
    old = np.load(HERE.parent/'scale_calibration_v0_2/results/source.npz')
    queries = old['query'][:28]
    A,I,norm_tail = normalization(ctx.prec); rows = []
    def append(i,m,value,tail,method):
        goal = arb(plan()['source']['absolute_component_radius_goal'])
        good = value.real.rad() <= goal and value.imag.rad() <= goal
        # Old floats are diagnostics only. They cannot enlarge or certify a ball.
        old_value = complex(old['green'][-1,i,m])
        difference = (value-acb(old_value)).abs_upper()
        rows.append({'probe_index':i,'mass':m,'point':queries[i].tolist(),
            'value':encode(value),'analytic_bump_tail_bound':encode(tail),
            'method':method,'enclosure_status':'WITHIN_RADIUS_GOAL' if good else 'QUADRATURE_HOLD',
            'old_Green_absolute_difference_bound':encode(difference)})
    for i,point in enumerate(queries):
        value,tail,method = kirchhoff(point,A)
        append(i,0,value,tail,method)
        if np.all(point[1:]==0):
            for m in [1,2]:
                value,tail = massive_center(point,m,A)
                append(i,m,value,tail,'CENTER_KG_INTEGRAL_WITH_BUMP_TAIL')
    if len(rows)!=34:
        raise ArithmeticError('wrong fixed reference inventory')
    print('source: 34 amplitudes enclosed',flush=True)
    return {'normalization_A':encode(A),'unnormalized_L2_squared':encode(I),
        'normalization_tail_bound':encode(norm_tail),'rows':rows,
        'covered':'all 28 massless probes and six massive center amplitudes',
        'full_reference_status':'HOLD_OFF_CENTER_MASSIVE_AND_DETECTOR_ERROR_OPEN',
        'not_a_detector_trace_distance_bound':True}
