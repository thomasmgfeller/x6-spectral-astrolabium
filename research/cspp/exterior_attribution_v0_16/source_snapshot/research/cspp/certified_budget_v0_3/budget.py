"""Certified mean for ONE Gaussian witness; conservative correlated variance bound."""
from flint import arb, acb
from balls import plan, integrate, real_value, encode, ceil_upper

def gaussian_tail(ell, H, L):
    q = arb(ell)**-4
    return 56 * arb.pi() * q * L**2 * (-arb(H)**2 / (4*L**2)).exp()

def mean_witness(ell, L=2):
    if not (arb(ell)>0 and arb(L)>0):
        raise ValueError('positive physical scales required')
    q = arb(ell)**-4
    c = (arb.pi()*q/24).sqrt()
    a = 4*(q/6).sqrt()
    cfg = plan()['gaussian']
    delta, Y = arb(cfg['y_lower']), arb(cfg['y_upper'])
    def f(y, analytic):
        # K_0,K_1 have a negative-real-axis cut. A positive real part is a
        # sufficient domain certificate for every complex ball requested here.
        if not y.real > 0:
            return acb('nan')
        z = y/(2*c*L**2)
        y2 = y*y
        P = 1 - 9*y2 + 8*y2*y2 - 4*y2*y2*y2/3
        return y * P * (-y2).exp() * (z.bessel_k(1)-z.bessel_k(0))
    core = real_value(integrate(f, delta, Y))
    low = 8*arb.pi().sqrt()*q*L**2*delta*(1+9*delta**2+8*delta**4+4*delta**6/3)
    T = arb.pi().sqrt()*Y.erfc()/2
    high_integral = T
    for j, coeff in enumerate([9, 8, arb(4)/3], 1):
        T = Y**(2*j-1)*(-Y*Y).exp()/2 + (2*j-1)*T/2
        high_integral += coeff*T
    high = 8*arb.pi().sqrt()*q*L**2*high_integral
    value = a*(-1+12*core) + arb(0, (low+high).upper())
    return value, {'lower_y_tail': encode(low), 'upper_y_tail': encode(high),
                   'integrated_core': encode(core)}

def volume(H):
    return arb.pi()*arb(H)**4/24

def variance_upper(ell, H, rho):
    """E|B-E B|² for any deterministic field |phi|<=1 in D_H.

    Not a sum of independent layer variances. rho>=ell^-4 is mandatory.
    The exact rational moment factors are I1/V²=1/20, I2/V³=1/105.
    """
    q, rho = arb(ell)**-4, arb(rho)
    if not rho >= q:
        raise ValueError('inadmissible smoothing: rho < ell_k^-4')
    V = volume(H)
    return (arb(8)/3)*q**3/rho*(256*V + 40*q*V**2
        + arb(125)/4*q*q/rho*V**2 + arb(125)/21*q*q*V**3)

def sufficient_density(ell, H, sigma_absolute):
    """Conservative sufficient density, NOT an estimated or necessary density."""
    q, V = arb(ell)**-4, volume(H)
    C = arb(8)/3*q**3*(256*V+arb(285)/4*q*V**2+arb(125)/21*q*q*V**3)
    rho = max(ceil_upper(q), ceil_upper(C/arb(sigma_absolute)**2))
    if not variance_upper(ell,H,rho) <= arb(sigma_absolute)**2:
        raise ArithmeticError('sufficient-density bound failed')
    return rho

def compute():
    p = plan(); cfg = p['gaussian']; L = cfg['L']; target = -arb(2)/L**2
    denom = -target; rows = []
    for ell in cfg['ell_k']:
        mean, meta = mean_witness(ell,L)
        bias = abs(mean-target)/denom
        H = next((h for h in cfg['H_candidates']
                  if gaussian_tail(ell,h,L)/denom <= arb(cfg['relative_boundary_goal'])), None)
        if H is None:
            raise ArithmeticError('no predeclared domain meets tail goal')
        tail = gaussian_tail(ell,H,L)/denom
        sigma = arb(cfg['relative_stochastic_RMS_goal'])*denom
        rho = sufficient_density(ell,H,sigma)
        V, q = volume(H), arb(ell)**-4
        rms_upper = ((bias.upper()+tail.upper())**2 + variance_upper(ell,H,rho)/denom**2).sqrt()
        narrow = mean.rad()/denom <= arb(cfg['reference_radius_goal'])
        bias_ok = bias <= arb(cfg['relative_bias_goal'])
        rms_lower = max(arb(0),bias.lower()-tail.upper())
        if not narrow:
            status = 'QUADRATURE_HOLD'
        elif bias_ok:
            status = 'WITNESS_BIAS_WITHIN_ALLOCATION'
        elif bias > arb(cfg['relative_bias_goal']):
            status = 'WITNESS_BIAS_EXCEEDS_ALLOCATION'
        else:
            status = 'BIAS_UNDECIDED'
        rows.append({'ell_k':ell,'H':H,'mean_infinite':encode(mean),
            'relative_bias':encode(bias),'relative_boundary_bound':encode(tail),
            'witness_status':status,'epsilon_admissibility_rho_min':encode(q),
            'expected_N_admissibility_min':encode(q*V),
            'rho_sufficient_for_stochastic_RMS':str(rho),
            'expected_N_at_sufficient_density':encode(rho*V),
            'relative_RMS_upper_at_sufficient_density':encode(rms_upper),
            'relative_RMS_lower_at_any_admissible_density':encode(rms_lower),
            'witness_RMS_target_impossible_at_chosen_H':bool(rms_lower > arb(cfg['relative_total_RMS_goal'])),
            'single_witness_total_RMS_within_goal':bool(narrow and rms_upper <= arb(cfg['relative_total_RMS_goal'])),
            'admissibility_alone_exceeds_expected_point_budget':bool(q*V > p['resource_screen']['expected_point_budget']),
            'scope':'one Gaussian witness; no E4 or all-field qualification',**meta})
        print('budget',ell,status,flush=True)
    return {'rows':rows,'variance_bound_scope':'bounded fields on fixed finite D_H, rho>=ell_k^-4',
        'density_bound_type':'sufficient only; looseness is not an impossibility proof',
        'G1':'HOLD','G2':'NOT_RUN','G3':'NOT_RUN','confirmation_seed_used':False}
