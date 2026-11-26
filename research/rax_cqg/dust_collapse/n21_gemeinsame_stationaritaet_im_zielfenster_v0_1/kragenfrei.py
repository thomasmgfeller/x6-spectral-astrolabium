"""Coarser exact rational exclusion using only three density variations."""
from fractions import Fraction as F
from math import isqrt


def square_root_bracket(a,b):
    scale=10**15
    def floor_root(q):
        return isqrt(q.numerator*scale**2//q.denominator)
    low=F(floor_root(a),scale)
    high=F(floor_root(b)+1,scale)
    assert low**2 <= a <= b <= high**2
    return low,high


def density_test(max_load_term):
    # Enlarge the raw-time interval from the fixed-collar calculation.
    low,high=F(23,1000),F(144,1000)
    span=high-low
    max_k=F(1,10**11)
    max_j=F(1,10**6)
    # Uniform in k in [0,max_k] with mismatch -k.
    lo2=low**2+6*low+6-max_j-max_load_term
    hi2=(high**2+6*high+6+max_j)/(1-max_k)
    dmin,dmax=square_root_bracket(lo2,hi2)
    A=35+32*high+8*high**2+span**2-9*dmin**2
    B=19-8*dmin**2+18*span**2+max_load_term
    C=19-8*(dmax+span)**2+(16-max_k)*(-A)
    assert A<0 and B<0 and C>0
    return {'bare_positive_equation_upper':A,'receiver_one_parent_upper':B,
            'receiver_two_parents_lower':C,'sender_gap':[dmin,dmax],
            'load_per_weight_squared_upper':max_load_term}


def comparison(max_velocity,k):
    floor=F(1,10**17)
    return {'zero_pointer_momenta':density_test(F(0)),
            'all_momenta_above_weight_floor':density_test(3*k*max_velocity**2/floor**2),
            'weight_floor':floor,'raw_time_domain':[F(23,1000),F(144,1000)]}
