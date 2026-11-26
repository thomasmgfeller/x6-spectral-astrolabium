"""Joint mass and shell control on one analytic LTB solution per sector."""
from fractions import Fraction as F
from math import isqrt
from basis import klassik as ltb

GRID = 10**30
EPS = F(1,100)


def roots(value, power):
    """Rational enclosure, checked by exact exponentiation."""
    if value<0 or power not in (2,3):
        raise ValueError('root domain')
    n=value.numerator*GRID**power//value.denominator
    if power==2:
        k=isqrt(n)
    else:
        lo,hi=0,1<<((n.bit_length()+2)//3+1)
        while hi-lo>1:
            m=(lo+hi)//2
            if m**3<=n:
                lo=m
            else:
                hi=m
        k=lo
    lo=F(k,GRID)
    hi=lo if lo**power==value else F(k+1,GRID)
    assert lo**power<=value<=hi**power
    return lo,hi


def radius_bounds(a,mass):
    # At T*=5 sqrt(5)/6 the squared infall term simplifies to 125*m(a)/(8*a^3).
    s0,s1=roots(F(125,8)*mass*ltb.mass_fraction(a)/a**3,2)
    assert 0<=s0<=s1<1
    return (a*roots((1-s1)**2,3)[0],a*roots((1-s0)**2,3)[1])


def shell_channels(left,right,mass):
    a,b=radius_bounds(left,mass),radius_bounds(right,mass)
    # Return V/(4π) and proper thickness on the same marginally bound dust slice.
    volume_lo=(b[0]**3-a[1]**3)/3
    volume_hi=(b[1]**3-a[0]**3)/3
    length_lo,length_hi=b[0]-a[1],b[1]-a[0]
    assert volume_lo>0 and length_lo>0
    return ((volume_lo*(1-EPS),volume_hi*(1+EPS)),
            (length_lo*(1-EPS),length_hi*(1+EPS)))


def surface(occupied):
    if not any(occupied):
        return None
    k=max(i for i,v in enumerate(occupied) if v)
    if not all(occupied[:k+1]) or k<1 or k+2>=len(occupied):
        raise ValueError('incomplete or disconnected profile')
    return k,k+1


def read_radius(inner,outer):
    (vmin,_),(_,lmax)=inner
    (_,vmax),(lmin,_)=outer
    assert min(vmin,lmax,vmax,lmin)>0
    return roots(vmin/lmax,2)[0],roots(vmax/lmin,2)[1]


def control():
    grid=ltb.GRID
    cases=[]
    # Same comoving inventory is evolved for every readout of each case.
    calibration=F(1,4)
    zero=ltb.charge_interval(ltb.prepare_charge_samples(F(0)))
    assert zero==(0,0)
    qlo,qhi=ltb.charge_interval(ltb.prepare_charge_samples(calibration))
    std=ltb.exterior_standard(calibration)
    gain=(std/qhi,std/qlo)
    for mass in (F(0),calibration,F(4)):
        def occupancy(t):
            return [ltb.evolve(float(a),t,float(mass))[1]>0 for a in grid]
        initial=occupancy(0)
        occupied=occupancy(ltb.END/2)
        assert initial==occupied==[ltb.initial_signal(a,mass)>0 for a in grid]
        pair=surface(occupied)
        if not mass:
            assert pair is None
            continue
        a,b=pair
        q=ltb.charge_interval(ltb.prepare_charge_samples(mass))
        mlo,mhi=gain[0]*q[0],gain[1]*q[1]
        assert F(98,100)*mass<=mlo<=mass<=mhi<=F(102,100)*mass
        inner=shell_channels(grid[a-1],grid[a],mass)
        outer=shell_channels(grid[b],grid[b+1],mass)
        lo,hi=read_radius(inner,outer)
        target=radius_bounds(F(10),mass)
        assert lo<=target[0]<=target[1]<=hi
        # Entire bracket must fit even using inward-rounded limits of the target band.
        assert F(95,100)*target[1]<=lo and hi<=F(105,100)*target[0]
        assert grid[a]<10<=grid[b] and grid[a-1]>5
        decoy=ltb.mass_fraction(F(5))
        assert decoy==F(17,64) and ltb.initial_signal(F(5),mass)>0
        # A gap in the observed material run must be rejected.
        invalid=list(occupied)
        invalid[a//2]=False
        try:
            surface(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError('gap accepted')
        cases.append({'model_mass':str(mass),'mass_interval':list(map(str,(mlo,mhi))),
                      'radius_interval':list(map(str,(lo,hi))),'max_relative_error_upper':
                        str(max(1-lo/target[1],hi/target[0]-1)),
                      'bracketing_station_indices':list(pair),'inner_decoy_mass_fraction':str(decoy),
                      'radial_channels':[[list(map(str,band)) for band in s] for s in (inner,outer)]})
    return {'kind':'classical_LTB_control','vacuum_charge':list(map(str,zero)),'vacuum_surface':None,
            'gain':list(map(str,gain)),'cases':cases}
