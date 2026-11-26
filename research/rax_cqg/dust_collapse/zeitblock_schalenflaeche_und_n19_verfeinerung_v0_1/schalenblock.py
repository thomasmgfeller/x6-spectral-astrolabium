"""Rational enclosures for same-history, finite-duration comoving shell observations."""
from fractions import Fraction as F
from basis import klassik as ltb
from klassische_kontrolle import roots, radius_bounds, surface, control

X = F(1, 2)
H = F(1, 64)
EPS = F(1, 100)
R0 = F(10)


def radius_and_means(a, mass, h):
    """Return intervals for mean R, mean R^3, and the midpoint R^3."""
    k2 = F(125, 2)*mass*ltb.mass_fraction(a)/a**3
    kl, ku = roots(k2, 2)
    if ku == 0:
        return (a, a), (a**3, a**3), (a**3, a**3)
    # Evaluate R(x) and its time average at bounding k. Both decrease with k.
    def at(k):
        left, right, mid = 1-k*(X-h), 1-k*(X+h), 1-k*X
        assert 0 < right <= left
        pl, pu = roots(left**5, 3)
        ql, qu = roots(right**5, 3)
        factor = 3*a/(10*h*k)
        mean_r = (factor*(pl-qu), factor*(pu-ql))
        # Independent upper/lower Darboux sums for the mean radius. R decreases
        # throughout this positive-mass control interval.
        boundaries = [1-k*(X-h+h*j/4) for j in range(9)]
        samples = [roots(t*t,3) for t in boundaries]
        dar_lo = a*sum(v[0] for v in samples[1:])/8
        dar_hi = a*sum(v[1] for v in samples[:-1])/8
        assert dar_lo <= mean_r[0] <= mean_r[1] <= dar_hi
        mid_r3 = a**3 * mid**2
        mean_r3 = a**3 * (mid**2 + k**2*h**2/3)
        # Simpson's rule is exact for this quadratic in x.
        assert mean_r3 == a**3 * (left**2 + 4*mid**2 + right**2)/6
        return mean_r, mean_r3, mid_r3
    low, high = at(ku), at(kl)
    return (low[0][0],high[0][1]),(low[1],high[1]),(low[2],high[2])


def sub(high, low):
    return high[0]-low[1], high[1]-low[0]


def instruments(a, b, mass, h):
    r1, v1, m1 = radius_and_means(a, mass, h)
    r2, v2, m2 = radius_and_means(b, mass, h)
    length = sub(r2, r1)
    volume = tuple(v/3 for v in sub(v2, v1))
    mid = tuple(v/3 for v in sub(m2, m1))
    bias = F(125, 18)*mass*(ltb.mass_fraction(b)-ltb.mass_fraction(a))*h**2
    assert max(volume[0], mid[0]+bias) <= min(volume[1],mid[1]+bias)
    assert length[0] > 0 and volume[0] > 0
    def observed(bounds):
        return [bounds[0]*(1-EPS), bounds[1]*(1+EPS)]
    return {'volume':observed(volume), 'thickness':observed(length),
            'ideal_volume':volume,'ideal_mid_volume':mid,'volume_time_bias':bias}


def radius_from_block(inner, outer, max_displacement):
    # Integral of R² d(ell) dT divided by integral of d(ell) dT is a weighted mean.
    lower = roots(inner['volume'][0]/inner['thickness'][1], 2)[0]-max_displacement
    upper = roots(outer['volume'][1]/outer['thickness'][0], 2)[1]+max_displacement
    assert 0 < lower < upper
    return lower, upper


def time_block():
    parent = control()
    gains = {r['model_mass']:r['mass_interval'] for r in parent['cases']}
    end_upper = 5*roots(F(5),2)[1]/3
    # Assume a common surface speed bound of 1 in G=c=1. Verify it for both
    # controls on the whole larger window via 2M/R <= 1 at its right endpoint.
    for m in (F(1,4),F(4)):
        k_high = roots(F(125,2)*m/R0**3,2)[1]
        assert R0*roots((1-k_high*(X+H))**2,3)[0] > 2*m
    assert surface([False]*len(ltb.GRID)) is None
    cases = []
    for mass in (F(1,4),F(4)):
        occ = [ltb.initial_signal(a, mass) > 0 for a in ltb.GRID]
        k, j = surface(occ)
        assert k == 492 and j == 493
        # The comoving occupation sign follows the initial signal on the entire block:
        # 1 - k(a)*x > 0 and k(a) non-increasing, so R'(a) > 0. This uniform upper
        # bound on k(a)^2 also covers the centre by continuity.
        assert F(125,2)*5*mass/(2*R0**3)*(X+H)**2 < 1
        assert ltb.mass_fraction(F(5)) == F(17,64) and ltb.initial_signal(F(5),mass) > 0
        assert any(ltb.initial_signal(a,mass)>0 for a in ltb.GRID if a>5)
        target = radius_bounds(R0, mass)
        by_side = [[],[]]
        trials = []
        for h in (H,H/2):
            channels = [instruments(ltb.GRID[a],ltb.GRID[b],mass,h)
                        for a,b in [(k-1,k),(j,j+1)]]
            for sets, reading in zip(by_side,channels):
                sets.append(reading)
            low, high = radius_from_block(*channels, h*end_upper)
            assert low <= target[0] <= target[1] <= high
            assert F(95,100)*target[1] <= low and high <= F(105,100)*target[0]
            trials.append({'half_window':h,'radius':[low,high],'motion_guard':h*end_upper,
                           'max_relative_error_upper':max(1-low/target[1],high/target[0]-1),
                           'inner':channels[0], 'outer':channels[1]})
        for full, half in by_side:
            assert full['volume_time_bias'] == 4*half['volume_time_bias']
            l,h = (4*half['ideal_volume'][0]-full['ideal_volume'][1])/3,(4*half['ideal_volume'][1]-full['ideal_volume'][0])/3
            ml,mh = full['ideal_mid_volume']
            assert max(ml,l) <= min(mh,h)
        assert by_side[0][0]['volume_time_bias']>0 and by_side[1][0]['volume_time_bias']==0
        cases.append({'M':str(mass),'initial_mass_band':gains[str(mass)],'reference_radius':target,'blocks':trials})
    return {'cases':cases, 'common_surface_speed_bound':'1','fraction_within_decoy':'17/64',
            'vacuum_surface':None,'zero_flux_decoy_rejected_by_positive_exterior_occupancy':True,
            'station_count':len(ltb.GRID),'boundary_bracket_indices':[492,493]}
