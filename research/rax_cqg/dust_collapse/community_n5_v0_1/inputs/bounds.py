"""Exact alpha-dependent majorants for the declared natural-order weights."""
from fractions import Fraction as F
from math import factorial


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def power2(exponent):
    require(isinstance(exponent, int), 'Exact integer exponent required')
    return F(2**exponent) if exponent >= 0 else F(1, 2**(-exponent))


def validate(h, alpha, K):
    require(isinstance(alpha, int) and alpha >= 1, 'Certified implementation requires integer alpha >= 1')
    require(isinstance(K, int) and K >= 0 and h >= 0, 'Nonnegative h and integer cutoff')


def coefficient(count, h, alpha, n):
    validate(h, alpha, n)
    require(isinstance(count, int) and count >= 1, 'Positive exact natural-order count')
    return F(count, factorial(n))*h**n*power2(-alpha*n*(n-1)//2)


def ratio(h, alpha, n):
    """Upper bound on c_(n+1)/c_n, including the at-most 2^n ideals."""
    return h/F(n+1)*power2(-(alpha-1)*n)


def universal_tail(h, alpha, K):
    validate(h, alpha, K)
    first = h**(K+1)/factorial(K+1)*power2(-(alpha-1)*K*(K+1)//2)
    q = ratio(h, alpha, K+1)
    require(q < 1, 'Geometric tail ratio must be less than one')
    return first/(1-q)


def anchored_tail(count_K, h, alpha, K):
    """Tail beyond K, seeded only by the already known exact count N_K."""
    validate(h, alpha, K)
    require(isinstance(count_K, int) and 1 <= count_K <= 2**(K*(K-1)//2),
            'Natural-order count must fit the upper-triangle bound')
    factor = F(count_K, 2**(K*(K-1)//2))
    return factor*universal_tail(h, alpha, K)


def majorant_term(count_K, h, alpha, K, n):
    validate(h, alpha, K)
    require(n >= K, 'Majorant index follows its seed')
    return coefficient(count_K,h,alpha,K)*h**(n-K)*F(factorial(K),factorial(n))*\
        power2(-(alpha-1)*(n*(n-1)-K*(K-1))//2)
