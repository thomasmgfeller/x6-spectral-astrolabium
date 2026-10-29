"""Poisson/BD variance bounds for a fixed Gaussian witness in a 4D diamond.

All budget decisions use python-flint Arb balls. No empirical variance, fitted
density law, or unverified quadrature is used in the reported certificates.
See METHODS.md for the proof and the remaining looseness of the bounds.
"""
from fractions import Fraction
from math import comb, factorial
from flint import arb

C = (1, -9, 16, -8)
D = (-10, 25, -24, 8)
E = (25, -24, 8)
EPSILON_CAP = Fraction(1, 2**20)


def ball(x):
    if isinstance(x, Fraction):
        return arb(x.numerator) / x.denominator
    return arb(x)


def weight(n, epsilon, coefficients=C):
    """Binomially smoothed finite layer sequence; supports exact Fractions."""
    if not isinstance(n, int) or n < 0 or not 0 <= epsilon <= 1:
        raise ValueError('nonnegative integer n and epsilon in [0,1] required')
    return sum(c * comb(n, k) * epsilon**k * (1-epsilon)**(n-k)
               for k, c in enumerate(coefficients) if k <= n)


def joint_kernel(left, right, u, v, shared):
    """E[left[K] right[L]], K=A+C, L=B+C, shared=E C.

    Parameters u=q*Vy, v=q*Vv, shared=q*epsilon*overlap. Palm endpoint
    insertions must first be applied to the coefficient arrays (see palm).
    Scalars are real here; complex fields enter the spatial integral.
    """
    u, v, shared = map(ball, (u, v, shared))
    if not (u >= 0 and v >= 0 and shared >= 0 and u >= shared and v >= shared):
        raise ValueError('require 0 <= shared <= min(u,v)')
    out = arb(0)
    for k, ck in enumerate(left):
        for j, dj in enumerate(right):
            for r in range(min(k, j)+1):
                out += (ball(ck)*ball(dj)*(u-shared)**(k-r)*(v-shared)**(j-r)
                        *shared**r/(factorial(k-r)*factorial(j-r)*factorial(r)))
    return (-(u+v-shared)).exp()*out


def palm(coefficients, epsilon, shift):
    if shift not in (0, 1):
        raise ValueError('pairwise Palm shift must be 0 or 1')
    if not shift:
        return coefficients
    return tuple((1-epsilon)*x + epsilon*(coefficients[i+1] if i+1<len(coefficients) else 0)
                 for i, x in enumerate(coefficients))


def integrated_second_moment(coefficients, power, epsilon):
    """Integral_0^infty y^power E[w_e(Pois(y²/e))²] dy.

    Analytic at epsilon=0. The integrand has a nonnegative square-sum
    representation. Signed polynomial terms are integrated exactly by Gamma.
    An epsilon ball encloses the whole designated smoothing range.
    """
    e = ball(epsilon)
    if not 2-e > 0:
        raise ValueError('Gamma integral requires epsilon < 2')
    out = arb(0)
    for r in range(len(coefficients)):
        for i in range(len(coefficients)-r):
            for j in range(len(coefficients)-r):
                b = arb(r+i+j) + arb(power+1)/2
                out += (coefficients[i+r]*coefficients[j+r]*e**r*(1-e)**(i+j)
                        *b.gamma()/(2*(2-e)**b*factorial(r)*factorial(i)*factorial(j)))
    return out


def sqrt_moment_envelope(coefficients, epsilon_cap):
    """Integral y*R(y)dy, where R majorizes sqrt(H_e(y²))."""
    e = ball(epsilon_cap)
    if not (e > 0 and e <= 1):
        raise ValueError('epsilon cap must be in (0,1]')
    out = arb(0)
    for r in range(len(coefficients)):
        for j in range(len(coefficients)-r):
            b = arb(2+r+2*j)/2
            out += (e**(arb(r)/2)*abs(coefficients[j+r])*b.gamma()
                    /(2*(1-e/2)**b*arb(factorial(r)).sqrt()*factorial(j)))
    return out


def upper_coefficient(ell, L=2, epsilon_cap=EPSILON_CAP):
    """Returns K with Var F <= K/rho for rho >= q/epsilon_cap.

    The bound holds on any finite causally convex D_H for the specified
    Gaussian envelope. The field tail is integrated over the whole past cone;
    this is an upper bound, not a replacement of the finite-domain model.
    """
    ell, L, e0 = map(ball, (ell, L, epsilon_cap))
    if not (ell > 0 and L > 0 and e0 > 0 and e0 <= 1):
        raise ValueError('positive scales and epsilon cap <=1 required')
    q = ell**-4
    # The radius rounds outwards. This contains every epsilon in [0,e0].
    e_range = arb(e0/2, e0/2)
    scale = (24*arb.pi()).sqrt()*L**2/q.sqrt()
    A = scale/2*integrated_second_moment(C, 0, e_range)
    B = scale/(2*q)*integrated_second_moment(D, 2, e_range)
    Cenv = scale/q.sqrt()*(sqrt_moment_envelope(D, e0)
                          + e0*sqrt_moment_envelope(E, e0))
    if not (A > 0 and B > 0 and Cenv > 0):
        raise ArithmeticError('positive enclosure not established')
    # A,B are enclosures for a range of epsilons, not estimates.
    K = arb(8)/3*q**3*(A.upper().sqrt()
        +(q*e0*B.upper()+q*q*Cenv**2).sqrt())**2
    return K, {'A_upper': A.upper(), 'B_upper': B.upper(),
               'C_upper': Cenv.upper(), 'epsilon_cap': e0, 'rho_regime_min': q/e0}


def gaussian_tail_moments(a, maximum):
    """T_n(a)=integral_a^infinity x^n exp(-x²)dx, via exact recurrence."""
    a = ball(a)
    ex = (-a*a).exp()
    out = [arb.pi().sqrt()*a.erfc()/2, ex/2]
    for n in range(2, maximum+1):
        out.append((a**(n-1)*ex+(n-1)*out[n-2])/2)
    return out[:maximum+1]


def local_lower_coefficient(ell=Fraction(1, 8), H=20, L=2):
    """Certified first-chaos restriction on x in [3,3.1], v in [1.9,2.1].

    Returns k>0 with Var F >= k/rho for every admissible rho>=q.
    No quadrature: the proof uses Gamma/erfc tails and a geometric cap bound.
    The fixed box need not work for other scales; an undecidable sign fails.
    """
    ell, H, L = map(ball, (ell, H, L))
    if not (ell > 0 and L > 0 and H > 0):
        raise ValueError('positive physical scales required')
    q = ell**-4
    c0 = (arb.pi()*q/24).sqrt()
    xl, xh, vl, vh = map(arb, ('3', '31/10', '19/10', '21/10'))
    gap = vl-xh/(c0*vl)
    if not (gap > 0 and vh < H):
        raise ArithmeticError('fixed lower-bound box is outside this diamond')
    T = gaussian_tail_moments(xl, 8)
    tail = sum(ball(coeff)*(T[k+2]-2*xl*T[k+1]+xl*xl*T[k])
               for k, coeff in [(0, 10), (2, 25), (4, 12), (6, Fraction(4, 3))])
    indirect = (12/gap * arb.pi().sqrt()*L*(vl/(2*L)).erfc()/(4*xl)*tail)
    # -P(x²) is increasing for x>=3. It equals 404 at x=3.
    direct = 404*(-(vh*vh+(xh/(c0*vl))**2)/(4*L*L)-xh*xh).exp()
    h_min = direct-indirect
    if not h_min > 0:
        raise ArithmeticError('this box does not certify a nonzero response')
    box_volume_min = (xh-xl)*(vh-vl)*arb.pi()/(2*c0)*gap**2/vh
    coefficient = arb(8)/3*q**3*box_volume_min*h_min**2
    if not coefficient > 0:
        raise ArithmeticError('positive variance lower bound not established')
    return coefficient, {'direct_absolute_min': direct, 'indirect_absolute_max': indirect,
                         'response_absolute_min': h_min, 'box_volume_min': box_volume_min}


def volume(H):
    return arb.pi()*ball(H)**4/24


def sufficient_density(K, ell, sigma=Fraction(7, 200), epsilon_cap=EPSILON_CAP):
    q, sigma, e0 = ball(ell)**-4, ball(sigma), ball(epsilon_cap)
    if not sigma > 0:
        raise ValueError('positive RMS allocation required')
    ceil = lambda x: int(x.upper().ceil().unique_fmpz())+1
    rho = max(ceil(q/e0), ceil(K/sigma**2))
    if not (K/rho <= sigma**2 and ball(rho) >= q/e0):
        raise ArithmeticError('sufficient-density inequality not certified')
    return rho


def encode(x):
    x = ball(x)
    return {'ball': x.str(55), 'midpoint_display_only': float(x.mid()),
            'radius_display_only': float(x.rad())}
