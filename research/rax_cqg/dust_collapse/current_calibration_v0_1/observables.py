"""Finite dust-ball reference and conditional count-based measurement adapter."""
import math
import numpy as np
from scipy.stats import chi2, poisson

G = 1.0
R0 = 10.0
WIDTH = 0.5
MASSES = [0.25, 1.0, 4.0]
PROBES = ['whole', 'core', 'bulk', 'rim', 'fixed_R4', 'surface_material', 'surface_total']


def collapse_time(mass):
    return (2/3)*math.sqrt(R0**3/(2*G*mass))


T_END = min(map(collapse_time, MASSES))/2


def radius(mass, time):
    if not 0 <= time < collapse_time(mass):
        raise ValueError('time outside regular collapsing reference')
    return R0*(1-time/collapse_time(mass))**(2/3)


def r_bounds(probe, mass, time):
    r = radius(mass, time)
    if probe == 'whole': return 0., r
    if probe == 'core': return 0., .5*r
    if probe == 'bulk': return .5*r, .8*r
    if probe == 'rim': return .8*r, r
    if probe == 'fixed_R4': return 0., 4.
    if probe == 'surface_material': return r-WIDTH, r
    if probe == 'surface_total': return r-WIDTH, r+WIDTH
    raise ValueError('unknown detector')


def volume(probe, mass, time):
    lo, hi = r_bounds(probe, mass, time)
    return 4*math.pi*(hi**3-lo**3)/3


def mass_fraction_bounds(probe, mass, time):
    r = radius(mass, time)
    lo, hi = r_bounds(probe, mass, time)
    return min(1., max(0., lo/r))**3, min(1., max(0., hi/r))**3


def true_mass(probe, mass, time):
    lo, hi = mass_fraction_bounds(probe, mass, time)
    return mass*(hi-lo)


def particle_mass(probe, mass, time, particles):
    lo, hi = mass_fraction_bounds(probe, mass, time)
    s = (np.arange(particles)+.5)/particles
    count = int(np.count_nonzero((s >= lo) & (s < hi)))
    value = mass*count/particles
    err = 0. if probe == 'whole' else mass/particles
    return value, max(0., value-err), min(mass, value+err), err


def integral_radius_power(mass, lo, hi, power):
    ts = collapse_time(mass)
    a = 1+2*power/3
    return R0**power*ts/a*((1-lo/ts)**a-(1-hi/ts)**a)


def exposure(probe, mass, lo, hi):
    if not 0 <= lo < hi <= T_END:
        raise ValueError('window must lie within the contracted interval')
    fac = {'whole':1., 'core':.5**3, 'bulk':.8**3-.5**3, 'rim':1-.8**3}
    if probe in fac:
        return 4*math.pi/3*fac[probe]*integral_radius_power(mass, lo, hi, 3)
    if probe == 'fixed_R4': return volume(probe, mass, lo)*(hi-lo)
    i2 = integral_radius_power(mass, lo, hi, 2)
    if probe == 'surface_total': return 4*math.pi/3*(6*WIDTH*i2+2*WIDTH**3*(hi-lo))
    i1 = integral_radius_power(mass, lo, hi, 1)
    if probe == 'surface_material': return 4*math.pi/3*(3*WIDTH*i2-3*WIDTH**2*i1+WIDTH**3*(hi-lo))
    raise ValueError('unknown detector')


def window(center, multipliers):
    half = .1*T_END
    return max(0., center-half*multipliers[0]), min(T_END, center+half*multipliers[1])


def garwood(count, alpha):
    if not isinstance(count, (int, np.integer)) or count < 0 or not 0 < alpha < 1:
        raise ValueError('invalid count or error probability')
    lower = 0. if count == 0 else .5*chi2.ppf(alpha/2, 2*count)
    upper = .5*chi2.isf(alpha/2, 2*(count+1))
    return float(lower), float(upper)


def intervals(count, lam, A, mass_interval, alpha):
    if lam <= 0 or A <= 0: raise ValueError('positive calibrated exposure required')
    mlo, mhi = mass_interval
    if not 0 <= mlo <= mhi: raise ValueError('invalid mass interval')
    lo, hi = garwood(count, alpha)
    vlo, vhi = lo/(lam*A), hi/(lam*A)
    rlo = mlo/vhi
    rhi = math.inf if vlo == 0 and mhi > 0 else (0. if mhi == 0 else mhi/vlo)
    return {'volume':(vlo,vhi), 'density':(rlo,rhi),
            'status':'HOLD_ZERO_COUNT' if count == 0 else 'CONDITIONAL_INTERVAL'}


def calibrated_intervals(count, lambda_bounds, exposure_bounds, mass_bounds, alpha):
    """Propagate deterministic calibration bounds; no independence assumption.

    A = Omega4/V3 must be calibrated on the same physical detector/window.
    Statistical uncertainty in calibration needs its own allocated error budget.
    """
    llo, lhi = lambda_bounds
    alo, ahi = exposure_bounds
    mlo, mhi = mass_bounds
    if not all(math.isfinite(x) for x in (llo,lhi,alo,ahi,mlo,mhi)):
        raise ValueError('finite calibration bounds required')
    if not (0 < llo <= lhi and 0 < alo <= ahi and 0 <= mlo <= mhi):
        raise ValueError('ordered calibration bounds required')
    lo, hi = garwood(count, alpha)
    vlo, vhi = lo/(lhi*ahi), hi/(llo*alo)
    return {'volume': (vlo,vhi),
            'density': (mlo/vhi, math.inf if vlo == 0 and mhi > 0 else (0. if mhi == 0 else mhi/vlo)),
            'status': 'HOLD_ZERO_COUNT' if count == 0 else 'CONDITIONAL_CALIBRATION_INTERVAL'}


def interval_inside_count_range(lower, upper, alpha):
    """Counts for which the Garwood interval is contained in [lower,upper]."""
    if lower <= 0 or upper <= lower: raise ValueError('positive ordered limits required')
    nlo = int(poisson.ppf(1-alpha/2, lower))+1
    nhi = int(poisson.ppf(alpha/2, upper))-1
    # Verify/adjust endpoint conventions using an independent chi-square expression.
    while nlo > 0 and garwood(nlo-1,alpha)[0] >= lower: nlo -= 1
    while garwood(nlo,alpha)[0] < lower: nlo += 1
    while garwood(nhi+1,alpha)[1] <= upper: nhi += 1
    while nhi >= 0 and garwood(nhi,alpha)[1] > upper: nhi -= 1
    return nlo, nhi


def miss_probability(mean, nlo, nhi):
    if nhi < nlo: return 1.
    return float(min(1., poisson.cdf(nlo-1,mean)+poisson.sf(nhi,mean)))


def covariance(probe1, probe2, mass, win1, win2, lam):
    # Exact spatial intersection for the nested whole/core probes used in this audit.
    if probe1 not in ('whole','core') or probe2 not in ('whole','core'):
        raise ValueError('this covariance adapter covers nested whole/core only')
    lo, hi = max(win1[0],win2[0]), min(win1[1],win2[1])
    if hi <= lo: return 0.
    probe = 'core' if 'core' in (probe1,probe2) else 'whole'
    return lam*exposure(probe,mass,lo,hi)
