"""Dynamical marginally bound Einstein-dust positive and negative controls."""
from fractions import Fraction as F
from math import sqrt
from dataclasses import dataclass

CELLS = 640
GRID = tuple(F(13*i,CELLS) for i in range(CELLS+1))
END = 5*sqrt(5)/3
INITIAL_EDGE = 10


def mass_fraction(a):
    u = min(F(a,INITIAL_EDGE),F(1))
    return (5*u**3-3*u**5)/2


def initial_signal(a,mass):
    # 4*pi*rho(0,a); exactly rational, including the regular centre.
    return 15*mass/(2*INITIAL_EDGE**3)*max(F(0),1-(a/INITIAL_EDGE)**2)


def evolve(a, time, mass):
    """Return areal radius, 4*pi*rho, R', and dR/dT of the comoving station."""
    if mass == 0:
        return a,0.,1.,0.
    if a <= INITIAL_EDGE:
        q = mass*(5-3*(a/INITIAL_EDGE)**2)/(2*INITIAL_EDGE**3)
        dq = -3*mass*a/INITIAL_EDGE**5
    else:
        q = mass/a**3
        dq = -3*q/a
    w = sqrt(2*q)
    factor = 1 - 1.5*time*w
    assert factor > 0 and dq <= 0
    spatial_scale = factor**(2/3)
    radial_derivative = spatial_scale - a*time*dq/w*factor**(-1/3)
    assert radial_derivative > 0
    density = 15*mass/(2*INITIAL_EDGE**3)*max(0.,1-(a/INITIAL_EDGE)**2)
    density /= spatial_scale**2*radial_derivative
    return a*spatial_scale, density, radial_derivative, -a*w*factor**(-1/3)


@dataclass(frozen=True)
class Station:
    index: int
    radius: float
    signal: float


def locate(samples, inventory):
    # Input contract: complete radial ordering and exposure to the stipulated outer station.
    if ([s.index for s in samples] != list(inventory) or len(samples)<2
        or any(a.radius >= b.radius for a,b in zip(samples,samples[1:]))):
        return {'state':'MISSING_EXPOSURE'}
    if any(s.signal < 0 for s in samples):
        return {'state':'INVALID_SIGNAL'}
    occupied = [k for k,s in enumerate(samples) if s.signal > 0]
    if not occupied:
        return {'state':'VACUUM_CONTROL'}
    end = occupied[-1]
    if occupied != list(range(end+1)):
        return {'state':'DISCONNECTED'}
    if end+1 == len(samples):
        return {'state':'NO_EXTERIOR'}
    inner,outer = samples[end:end+2]
    return {'state':'BRACKET','marks':[inner.index,outer.index],'radius':[inner.radius,outer.radius]}


def rk_radius(initial, mass, time):
    # Integrate the first-order collapse equation independently of the analytical expression.
    def velocity(r):
        return -sqrt(2*mass/r)
    h = time/128
    y = initial
    for _ in range(128):
        k1 = velocity(y)
        k2 = velocity(y + h*k1/2)
        k3 = velocity(y + h*k2/2)
        k4 = velocity(y + h*k3)
        y += h*(k1+2*k2+2*k3+k4)/6
    return y


def radius_test():
    inventory = [*range(len(GRID))]
    trials = []
    conservation_error = 0.
    fixed_sphere_gains = {}
    for mass in (F(0),F(1,4),F(1),F(4)):
        marks = []
        fixed_masses = []
        for x in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
            t = float(x)*END
            stations = []
            for i,a in enumerate(GRID):
                radius,signal,jacobian,_ = evolve(float(a), t, float(mass))
                conserved = signal*radius**2*jacobian
                initial = float(initial_signal(a,mass)*a*a)
                conservation_error = max(conservation_error,abs(conserved-initial))
                stations.append(Station(i,radius,signal))
            measured = locate(stations,inventory)
            if mass == 0:
                assert measured['state']=='VACUUM_CONTROL'
                trials.append({'M':str(mass),'x':str(x),**measured})
                continue
            assert measured['state']=='BRACKET'
            marks.append(measured['marks'])
            # Locate a fixed Eulerian sphere by bisection in the strictly increasing R(t,a).
            left,right = 0.,13.
            for _ in range(55):
                mid = (left+right)/2
                if evolve(mid,t,float(mass))[0] < 6:
                    left = mid
                else:
                    right = mid
            fixed_masses.append(float(mass*mass_fraction(F((left+right)/2))))
            target = rk_radius(10.,float(mass),t)
            exact = evolve(10.,t,float(mass))[0]
            lo,hi = measured['radius']
            err = max(abs(lo/target-1),abs(hi/target-1))
            assert lo <= target <= hi and err <= .05 and abs(target-exact)<1.e-9
            trials.append({'M':str(mass),'x':str(x),**measured,'rk_target':target,
                           'max_relative_endpoint_error':err})
        if mass:
            assert len(set(map(tuple,marks)))==1
            assert all(cur>prev for prev,cur in zip(fixed_masses,fixed_masses[1:]))
            fixed_sphere_gains[str(mass)] = fixed_masses[-1]-fixed_masses[0]
    assert conservation_error < 1e-12
    # Negative controls use only station records, without a mark for the true surface.
    half = len(stations)//2
    hole = list(stations)
    s = hole[half]
    hole[half] = Station(s.index,s.radius,0.)
    assert locate(hole,inventory)['state']=='DISCONNECTED'
    assert locate(stations[:half],inventory)['state']=='MISSING_EXPOSURE'
    assert locate(stations[:half],inventory[:half])['state']=='NO_EXTERIOR'
    assert locate(stations[:half]+stations[half+1:],inventory)['state']=='MISSING_EXPOSURE'
    return {'observations':trials,'grid_cells':CELLS,
            'max_abs_conservation_residual':conservation_error,
            'mass_gain_at_fixed_R6':fixed_sphere_gains,
            'null_flux_inner_decoy_mass_fraction':str(mass_fraction(F(5))),
            'negative_controls':['DISCONNECTED','MISSING_EXPOSURE','NO_EXTERIOR','MISSING_EXPOSURE'],
            'max_relative_endpoint_error':max(r.get('max_relative_endpoint_error',0) for r in trials)}


def prepare_charge_samples(mass):
    # Separate simulated channel, calibrated only through the positive reference.
    return [(a,initial_signal(a,mass)) for a in GRID]


def charge_interval(samples):
    # The declared initial density is nonincreasing; exact shell Darboux bounds.
    lower = upper = F(0)
    for (a,left),(b,right) in zip(samples,samples[1:]):
        assert b>a and left>=right>=0
        volume = (b**3-a**3)/3
        lower += right*volume
        upper += left*volume
    return lower,upper


def exterior_standard(mass):
    # Independent readout variable U^2 at the fixed exterior station, T=0.
    a = GRID[-1]
    velocity_squared = 2*(mass*mass_fraction(a))/a
    velocity = evolve(float(a),0.,float(mass))[3]
    assert abs(velocity**2-float(velocity_squared)) < 1.e-12
    return a*velocity_squared/2


def mass_test():
    # Gain cannot see any transfer target. No surface estimator participates.
    calibration_mass = F(1,4)
    vacuum = charge_interval(prepare_charge_samples(F(0)))
    assert vacuum==(0,0)
    qlo,qhi = charge_interval(prepare_charge_samples(calibration_mass))
    ref = exterior_standard(calibration_mass)
    gain = (ref/qhi, ref/qlo)
    held = []
    for mass in (F(1),F(4)):
        low,high = charge_interval(prepare_charge_samples(mass))
        inferred = (gain[0]*low,gain[1]*high)
        expected = exterior_standard(mass)
        relative = [v/expected-1 for v in inferred]
        assert -F(2,100) <= relative[0] <= 0 <= relative[1] <= F(2,100)
        held.append({'external_mass':str(expected),'mass_bounds':list(map(str,inferred)),
                     'relative_error_bounds':list(map(float,relative))})
    return {'vacuum_charge':[0,0],'one_standard':str(ref),'reference_charge':list(map(str,(qlo,qhi))),
            'gain_interval':list(map(str,gain)),'held_out':held}
