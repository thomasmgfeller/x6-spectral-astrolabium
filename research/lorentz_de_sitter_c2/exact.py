"""Rational geometric series, uniform tails and conservative C2 inversion.

All certification decisions use Fraction/integer arithmetic. Float conversion
is for reporting only. The supported domain is 0 <= h <= 1/2.
"""
from fractions import Fraction as Q
from functools import lru_cache
from math import comb, isqrt

DEGREE = 16
ZMAX = Q(1, 16)
HMAX = Q(1, 2)
LOG40_UPPER = Q(369, 100)


def add(*polys):
    out = {}
    for p in polys:
        for key, value in p.items():
            out[key] = out.get(key, Q(0))+value
    return {key: value for key, value in out.items() if value}


def scale(p, a):
    return {key: value*a for key, value in p.items() if value*a}


def mul(a, b):
    out = {}
    for (i, j), x in a.items():
        for (k, ell), y in b.items():
            key = (i+k, j+ell)
            out[key] = out.get(key, Q(0))+x*y
    return {k: v for k, v in out.items() if v}


def power(p, n):
    out = {(0, 0): Q(1)}
    for _ in range(n):
        out = mul(out, p)
    return out


def kernels():
    """Spatial ordered-pair volumes divided by pi², on four time triangles."""
    a, b, d = {(0, 0): Q(1, 2), (1, 0): Q(1)}, {(0, 0): Q(1, 2), (0, 1): Q(-1)}, {(0, 1): Q(1), (1, 0): Q(-1)}
    small = scale(add(power(a, 6), power(b, 6), power(d, 6),
        scale(mul(power(a, 4), power(b, 2)), -9),
        scale(mul(power(a, 4), power(d, 2)), -9),
        scale(mul(power(a, 3), power(b, 3)), 16),
        scale(mul(power(a, 3), power(d, 3)), 16),
        scale(mul(power(a, 2), power(b, 4)), -9),
        scale(mul(mul(power(a, 2), power(b, 2)), power(d, 2)), 18),
        scale(mul(power(a, 2), power(d, 4)), -9),
        scale(mul(power(b, 4), power(d, 2)), -9),
        scale(mul(power(b, 3), power(d, 3)), 16),
        scale(mul(power(b, 2), power(d, 4)), -9)), Q(1, 18))
    return (scale(mul(power(a, 3), power(d, 3)), Q(16, 9)),
            scale(mul(power(b, 3), power(d, 3)), Q(16, 9)),
            small, scale(mul(power(a, 3), power(b, 3)), Q(16, 9)))


@lru_cache(None)
def monomial(i, j, region):
    # Integrate t^i u^j; u bounds are affine in t.
    bounds = [(Q(-1, 2), Q(0), (Q(1), Q(0)), (Q(0), Q(0))),
              (Q(0), Q(1, 2), (Q(1), Q(0)), (Q(0), Q(1, 2))),
              (Q(-1, 2), Q(0), (Q(0), Q(0)), (Q(1), Q(1, 2))),
              (Q(-1, 2), Q(0), (Q(1), Q(1, 2)), (Q(0), Q(1, 2)))]
    left, right, lower, upper = bounds[region]
    total = Q(0)
    for sign, (slope, intercept) in ((-1, lower), (1, upper)):
        for k in range(j+2):
            total += (sign*Q(comb(j+1, k), j+1)*slope**k*intercept**(j+1-k)
                      *(right**(i+k+1)-left**(i+k+1))/(i+k+1))
    return total


@lru_cache(None)
def coefficients():
    polys = kernels()
    def moment(i, j):
        return 1152*sum((v*monomial(i+a, j+b, r)
                        for r, poly in enumerate(polys) for (a, b), v in poly.items()), Q(0))
    n = []
    for j in range(DEGREE+1):
        k = 2*j
        n.append(4**j*sum((comb(i+3, 3)*comb(k-i+3, 3)*moment(i, k-i)
                          for i in range(k+1)), Q(0)))
    return tuple(n), tuple(Q(2, j+2) for j in range(DEGREE+1))


def evaluate(poly, z):
    out = Q(0)
    for c in reversed(poly):
        out = out*z+c
    return out


def derivative(poly):
    return tuple(i*poly[i] for i in range(1, len(poly)))


def convolution(a, b):
    out = [Q(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def tails(z):
    """Absolute N, V and z-derivative tails after degree 16; uniform to z."""
    if not isinstance(z, Q) or not 0 <= z <= ZMAX:
        raise ValueError('rational z in [0,1/16] required')
    j = DEGREE+1
    ratio = z*Q((2*j+9)*(2*j+8), (2*j+2)*(2*j+1))
    first = Q(comb(2*j+7, 7), 10)*z**j
    en = first/(1-ratio)
    enp = Q(0) if z == 0 else (j*first/z)/(1-ratio*Q(j+1, j))
    ev = Q(2, j+2)*z**j/(1-z)
    evp = Q(0) if z == 0 else (Q(2*j, j+2)*z**(j-1))/(1-z*Q(j+1, j))
    return en, ev, enp, evp


@lru_cache(None)
def certificate():
    n, v = coefficients()
    np, vp = derivative(n), derivative(v)
    a, b = convolution(np, v), convolution(n, vp)
    d = [x-2*y for x, y in zip(a, b)]
    poly_lower = d[0]+sum((min(Q(0), c)*ZMAX**i for i, c in enumerate(d) if i), Q(0))
    en, ev, enp, evp = tails(ZMAX)
    norm = lambda p: evaluate(tuple(abs(x) for x in p), ZMAX)
    error = norm(np)*ev+enp*(norm(v)+ev)+2*(norm(n)*evp+en*(norm(vp)+evp))
    lower = poly_lower-error
    # exp(3.69) > 40 from a finite positive Taylor sum, hence ln(40) < 3.69.
    term, exp_lower = Q(1), Q(1)
    for k in range(1, 30):
        term *= LOG40_UPPER/k
        exp_lower += term
    if not lower > 0 or not exp_lower > 40:
        raise AssertionError('rational certification failed')
    probability_width = 2*en+(norm(n)+en)*(2*ev+ev*ev)
    return dict(monotone_numerator_lower=lower, numerator_tail=en, volume_tail=ev,
                numerator_derivative_tail=enp, volume_derivative_tail=evp,
                probability_enclosure_width_upper=probability_width,
                log40_upper=LOG40_UPPER, exp_lower=exp_lower)


@lru_cache(maxsize=4096)
def probability(h):
    if not isinstance(h, Q) or not 0 <= h <= HMAX:
        raise ValueError('rational h in [0,1/2] required')
    n, v = coefficients()
    z = h*h/4
    en, ev, _, _ = tails(z)
    a, b = evaluate(n, z), evaluate(v, z)
    return max(Q(0), (a-en)/(b+ev)**2), min(Q(1), (a+en)/b**2)


@lru_cache(maxsize=4096)
def q_bounds(h):
    if not isinstance(h, Q) or not 0 <= h <= HMAX:
        raise ValueError('rational h in [0,1/2] required')
    x = h/2
    a = sum((x**(2*j+1)/(2*j+1) for j in range(20)), Q(0))
    tail = x**41/(41*(1-x*x))
    return 48*a*a, 48*(a+tail)**2


def epsilon(n, clouds):
    if type(n) is not int or n < 2 or type(clouds) is not int or clouds < 1:
        raise ValueError('integer n>=2 and independent cloud count>=1 required')
    square = LOG40_UPPER/(2*clouds*(n//2))
    denominator = 2**40
    target = square*denominator**2
    top = isqrt(target.numerator//target.denominator)
    if Q(top*top) < target:
        top += 1
    return Q(top, denominator)


def invert(lower, upper):
    """Outer enclosure of {h in domain: p(h) in [lower,upper]} or None."""
    certificate()
    if not isinstance(lower, Q) or not isinstance(upper, Q) or lower > upper:
        raise ValueError('ordered rational probability bounds required')
    if lower > probability(HMAX)[1] or upper < probability(Q(0))[0]:
        return None
    lo, hi = Q(0), HMAX
    if lower > probability(Q(0))[1]:
        for _ in range(36):
            mid = (lo+hi)/2
            if probability(mid)[1] < lower:
                lo = mid
            else:
                hi = mid
    else:
        lo = Q(0)
    left = lo
    lo, hi = Q(0), HMAX
    if upper < probability(HMAX)[0]:
        for _ in range(36):
            mid = (lo+hi)/2
            if probability(mid)[0] > upper:
                hi = mid
            else:
                lo = mid
    else:
        hi = HMAX
    return left, hi


def confidence(total_c2, n, clouds):
    if type(total_c2) is not int or type(n) is not int or type(clouds) is not int:
        raise ValueError('integer inputs required')
    e = epsilon(n, clouds)
    maximum = clouds*comb(n, 2)
    if not 0 <= total_c2 <= maximum:
        raise ValueError('C2 count outside valid range')
    observed = Q(total_c2, maximum)
    return invert(observed-e, observed+e)


def relative_radius(interval):
    if interval is None:
        return None
    left, right = q_bounds(interval[0])[0], q_bounds(interval[1])[1]
    return Q(1) if left == 0 else (right-left)/(right+left)
