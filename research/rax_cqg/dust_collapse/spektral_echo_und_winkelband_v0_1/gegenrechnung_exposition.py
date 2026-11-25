"""Certified probability of at least one angle-band pair in an iid uniform S² sample.

Let g be the number of unordered pairs with angle in [theta-w,theta+w].
g=0 makes the calibrated fraction undefined. For g>=1 the fraction exists
provided all required direction-independent causal observations are available;
this guarantee alone gives no accuracy for an inferred radius.

For fixed center the band occupies fraction p=sin(theta)*sin(w) of S².
Write s_n=P(g=0 for the first n centers), k=n-1. Conditional on the
old centers, the new point has no hit with probability 1-U, where U is the
normalized area of the union of their k bands. Hence
       (1-kp) s_(n-1) <= s_n <= (1-kp) s_(n-1) + choose(k,2)*p².
On the left use U<=kp. On the right use the two-term Bonferroni lower bound
for U, then upper bound each intersection term times the indicator of old
emptiness by the bare intersection. The unconditional area of intersection
of two bands has expectation p², by conditioning on the test point and
integrating over the two independent centers. No Poisson approximation,
conditional-independence assumption, or independence of all edges enters.
Use only n such that 1-kp>=0 to iterate monotonically. The probability of
exposure is nondecreasing since adding a point preserves existing hits.

Bounds are rounded outwards on an integer grid. Underlying model means
independent uniform directions on a round sphere, exact angle calibration,
complete observation, and no conditional recruitment of probe pairs.
"""
from fractions import Fraction
from math import ceil, comb

def exposure_details(coverage=Fraction(19,20), grid=10**26, limit=1000000):
    theta = Fraction(1, 9200)
    width = theta / 200
    def sine(t):
        low = t - t ** 3 / 6
        return (low, low + t ** 5 / 120)
    a, b = sine(theta)
    c, d = sine(width)
    p_lo = grid * a * c // 1
    p_hi = ceil(grid * b * d)
    assert 0 < p_lo <= p_hi < grid and (limit - 1) * p_hi < grid
    target = coverage.denominator - coverage.numerator
    lower = upper = grid
    first_possible = None
    audit = {}
    for n in range(2,limit+1):
        k = n - 1
        old = (lower, upper)
        lower = lower * (grid - k * p_hi) // grid
        upper = min(grid, -(-(upper * (grid - k * p_lo) + comb(k, 2) * p_hi * p_hi) // grid))
        assert 0 <= lower <= upper
        if first_possible is None and lower*coverage.denominator<=grid*target:
            first_possible = n
            audit[str(n - 1)] = old
            audit[str(n)] = (lower, upper)
        if upper*coverage.denominator<=grid*target:
            audit[str(n - 1)] = old
            audit[str(n)] = (lower, upper)
            return {'min_probes_interval':[first_possible,n], 'grid':grid, 'p_band_interval':[p_lo,p_hi],
                    'p_empty_intervals':audit}
    raise ValueError('sufficient endpoint not found inside limit')

def exposure(coverage=Fraction(19,20), grid=10**26, limit=1000000):
    return tuple(exposure_details(coverage, grid, limit)['min_probes_interval'])

if __name__=='__main__':
    import json
    result = exposure_details()
    assert result['min_probes_interval'] == [318471, 318478]
    print(json.dumps(result, indent=2))
