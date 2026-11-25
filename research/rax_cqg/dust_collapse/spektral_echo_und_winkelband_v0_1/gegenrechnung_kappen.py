"""Verified continuum cap for two published kinematic geometries, not a finite or LTB graph."""
from fractions import Fraction as F
from math import isqrt

T = F(1, 1000)
RES = 10 ** 22
def sqrt_bounds(q):
    lo = isqrt(q.numerator * RES ** 2 // q.denominator)
    return (F(lo, RES), F(lo + 1, RES))
def H(x):
    assert 0 <= x <= 1
    return x ** 3 * (10 + x * (-15 + 6 * x))
def inverse_radius(t,model):
    lo, hi = sqrt_bounds(F(9, 125))
    def sq(v):
        s = t * v
        d = F(199, 5000) * H(F(1, 2) + s) + F(161, 625) * (1 if model == 'A' else H(64 * s))
        return 1 / (100 * (1 - d))
    return (sqrt_bounds(sq(lo))[0], sqrt_bounds(sq(hi))[1])
def cap(model,n=2048):
    # h=1/Rsurf is increasing over the interval; the left/right node sums enclose its integral.
    samples = [inverse_radius(T * i / n, model) for i in range(n + 1)]
    assert samples[0][0] >= F(1, 10) and samples[-1][1] <= F(1, 8)
    wall_lo = T / n * sum((x[0] for x in samples[:-1]))
    wall_hi = T / n * sum((x[1] for x in samples[1:]))
    # f<=1 gives 1/R(t,r) <= h(t) 10/r; if r>=10, 10/r<=1.
    # Else r>=10-T>9 and 10/r<=1+|r-10|/9.
    # For E=integral rdot², |r-10|<=sqrt(T E); sqrt(1-rdot²)<=1-rdot²/2.
    # Thus excess angle over integral h is <= max_{E>=0} T^(3/2) sqrt(E)/72 - E/20.
    # This equals 5*T^3/72^2.
    return (wall_lo, wall_hi + 5 * T ** 3 / 72 ** 2)
def sin_bounds(x):
    return (x - x ** 3 / 6, x - x ** 3 / 6 + x ** 5 / 120)
def ratio(n=2048):
    a, b = (cap('A', n), cap('B', n))
    lo = (sin_bounds(a[0])[0] / sin_bounds(b[1])[1]) ** 2
    hi = (sin_bounds(a[1])[1] / sin_bounds(b[0])[0]) ** 2
    assert lo > F('1.35654026') and hi < F('1.35654036')
    return (a, b, (lo, hi))
if __name__=='__main__':
    for pair in ratio():
        print(*map(float, pair))
