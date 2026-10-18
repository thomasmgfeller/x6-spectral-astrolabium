"""Rational Bernoulli-KL U-statistic inversion; fixed-budget only."""
from fractions import Fraction as Q
from functools import lru_cache
import importlib.util
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('kl_geometric_reference', ROOT/'research/lorentz_de_sitter_c2/exact.py')
reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)
THRESHOLD = Q(369, 100)
STEPS = 36
DENOMINATOR = 2**64


def round_down(x):
    return Q(x.numerator*DENOMINATOR//x.denominator, DENOMINATOR)


def round_up(x):
    return -round_down(-x)


def small_log(x):
    """log(x), 1 <= x <= 2, positive atanh expansion and rational tail."""
    z = (x-1)/(x+1)
    total, term = Q(0), z
    for j in range(24):
        total += 2*term/(2*j+1)
        term *= z*z
    return total, total+2*term/(49*(1-z*z))


LOG2 = small_log(Q(2))


def log_bounds(x):
    if not isinstance(x, Q) or x <= 0:
        raise ValueError('positive rational logarithm input required')
    k = x.numerator.bit_length()-x.denominator.bit_length()
    factor = Q(2**k) if k >= 0 else Q(1, 2**(-k))
    y = x/factor
    if y < 1:
        k -= 1
        y *= 2
    elif y >= 2:
        k += 1
        y /= 2
    lo, hi = small_log(y)
    a, b = LOG2 if k >= 0 else LOG2[::-1]
    return lo+k*a, hi+k*b


def kl_bounds(u, p):
    if not isinstance(u, Q) or not isinstance(p, Q) or not 0 <= u <= 1 or not 0 < p < 1:
        raise ValueError('rational u in [0,1], p in (0,1) required')
    lo, hi = Q(0), Q(0)
    for weight, denominator in ((u, p), (1-u, 1-p)):
        if weight:
            a, b = log_bounds(weight/denominator)
            lo += weight*a
            hi += weight*b
    return max(Q(0), lo), max(Q(0), hi)


def effective_count(n, clouds):
    if type(n) is not int or type(clouds) is not int or n < 2 or clouds < 1:
        raise ValueError('integer n>=2 and cloud count>=1 required')
    return clouds*(n//2)


@lru_cache(maxsize=8192)
def geometric_probability(h):
    lo, hi = reference.probability(h)
    return round_down(lo), round_up(hi)


def observation_band(pl, pu, effective):
    """Outer union of {u: effective*KL(u,p)<=3.69}, p in [pl,pu]."""
    if not 0 < pl <= pu < 1 or type(effective) is not int or effective < 1:
        raise ValueError('interior probability band and positive count required')
    delta = THRESHOLD/effective
    left, right = Q(0), pl
    if kl_bounds(Q(0), pl)[0] > delta:
        for _ in range(STEPS):
            mid = (left+right)/2
            if kl_bounds(mid, pl)[0] > delta:
                left = mid
            else:
                right = mid
    else:
        left = Q(0)
    lower = round_down(left)
    left, right = pu, Q(1)
    if kl_bounds(Q(1), pu)[0] > delta:
        for _ in range(STEPS):
            mid = (left+right)/2
            if kl_bounds(mid, pu)[0] > delta:
                right = mid
            else:
                left = mid
    else:
        right = Q(1)
    return lower, round_up(right)


def intersect(a, b):
    if a is None or b is None:
        return None
    result = max(a[0], b[0]), min(a[1], b[1])
    return result if result[0] <= result[1] else None


def interval_for_observations(ul, uu, n, clouds):
    """Outer union of KL confidence sets for observations in [ul,uu].

    Intersect with the outer union of Hoeffding sets. Pinsker proves that
    each exact KL set is already inside its Hoeffding set; no alpha split.
    """
    if not isinstance(ul, Q) or not isinstance(uu, Q) or not 0 <= ul <= uu <= 1:
        raise ValueError('ordered rational observation band in [0,1] required')
    effective = effective_count(n, clouds)
    reference.certificate()
    delta = THRESHOLD/effective
    def below(h):
        pu = geometric_probability(h)[1]
        return pu < ul and kl_bounds(ul, pu)[0] > delta
    def above(h):
        pl = geometric_probability(h)[0]
        return pl > uu and kl_bounds(uu, pl)[0] > delta
    if below(reference.HMAX) or above(Q(0)):
        return None
    left, right = Q(0), reference.HMAX
    if below(Q(0)):
        for _ in range(STEPS):
            mid = (left+right)/2
            if below(mid):
                left = mid
            else:
                right = mid
    else:
        left = Q(0)
    lower = left
    left, right = Q(0), reference.HMAX
    if above(reference.HMAX):
        for _ in range(STEPS):
            mid = (left+right)/2
            if above(mid):
                right = mid
            else:
                left = mid
    else:
        right = reference.HMAX
    e = reference.epsilon(n, clouds)
    old_union = reference.invert(ul-e, uu+e)
    return intersect((lower, right), old_union)


@lru_cache(maxsize=8192)
def confidence(total, n, clouds):
    effective_count(n, clouds)
    if type(total) is not int or not 0 <= total <= clouds*comb(n, 2):
        raise ValueError('integer C2 total inside the declared range required')
    u = Q(total, clouds*comb(n, 2))
    return interval_for_observations(u, u, n, clouds)


def design_interval(h, n, clouds, method):
    if method == 'Hoeffding':
        pl, pu = reference.probability(h)
        e = reference.epsilon(n, clouds)
        return reference.invert(pl-2*e, pu+2*e)
    if method != 'KL':
        raise ValueError('unknown method')
    pl, pu = geometric_probability(h)
    ul, uu = observation_band(pl, pu, effective_count(n, clouds))
    return interval_for_observations(ul, uu, n, clouds)


def first_sufficient(h, n, method, maximum):
    """Binary-searched sufficient count, with its adjacent failure checked.

    This locates a certificate boundary; it does not claim a globally optimal
    statistical sample size or minimum over other valid confidence methods.
    """
    def passes(m):
        radius = reference.relative_radius(design_interval(h, n, m, method))
        return radius is not None and radius <= Q(1, 5)
    if h == 0 or not passes(maximum):
        return None
    left, right = 0, maximum
    while right-left > 1:
        mid = (left+right)//2
        if passes(mid):
            right = mid
        else:
            left = mid
    if not passes(right) or (right > 1 and passes(right-1)):
        raise AssertionError('budget boundary failed')
    return right
