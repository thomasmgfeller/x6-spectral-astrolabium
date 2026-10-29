"""Conditional finite-sample tools. No campaign parameters or RNG are set here."""
from flint import arb, acb


def require(ok, message):
    if not ok:
        raise ValueError(message)


def observables(z):
    """Four real components and ten unique raw second moments; one cloud."""
    require(len(z) == 4, 'exactly four paired real components required')
    return list(z) + [z[i]*z[j] for i in range(4) for j in range(i, 4)]


def moments(theta):
    require(len(theta) == 14, 'four means and ten raw moments required')
    m = [arb(x) for x in theta[:4]]
    raw = [[arb(0) for _ in range(4)] for _ in range(4)]
    k = 4
    for i in range(4):
        for j in range(i, 4):
            raw[i][j] = raw[j][i] = arb(theta[k]); k += 1
    C = [[raw[i][j]-m[i]*m[j] for j in range(4)] for i in range(4)]
    mu = [acb(m[r], m[r+2]) for r in range(2)]
    Sigma = [[acb(C[r][s]+C[r+2][s+2], C[r+2][s]-C[r][s+2])
              for s in range(2)] for r in range(2)]
    Pi = [[acb(C[r][s]-C[r+2][s+2], C[r][s+2]+C[r+2][s])
           for s in range(2)] for r in range(2)]
    return mu, Sigma, Pi


def confidence_interval(center, numerical_radius, variance_upper, n, alpha):
    """Chebyshev on iid clouds; variance bound must hold under the tested law."""
    require(isinstance(n, int) and n > 0, 'positive fixed sample size required')
    a, V, alpha = map(arb, (numerical_radius, variance_upper, alpha))
    require(a >= 0 and V >= 0 and alpha > 0 and alpha < 1, 'invalid certificate')
    radius = a + (V/(n*alpha)).sqrt()
    return arb(center) + arb(0, radius.upper())


def classify(confidence, prediction, tolerance):
    """Scalar/complex ball inclusion: overlapping intervals do not imply PASS."""
    tol = arb(tolerance)
    require(tol >= 0, 'nonnegative equivalence margin required')
    difference = confidence - prediction
    if difference.abs_upper() <= tol:
        return 'PASS'
    if difference.abs_lower() > tol:
        return 'REJECT'
    return 'INCONCLUSIVE'


def sufficient_size(V, alpha, beta, margin, prediction_radius, numerical_radius):
    """A conservative sufficient N, never a necessary/universal lower bound.

    margin is separation from the equivalence boundary under the specified
    alternative (or interior agreement). V must bound variance there as well.
    """
    V, alpha, beta, gap, r, a = map(arb, (V, alpha, beta, margin,
                                         prediction_radius, numerical_radius))
    require(V >= 0 and r >= 0 and a >= 0, 'nonnegative bounds required')
    require(0 < alpha < 1 and 0 < beta < 1, 'invalid error probabilities')
    require(gap-r-2*a > 0, 'no finite guarantee from this bound at that margin')
    bound = V*(1/alpha.sqrt()+1/beta.sqrt())**2/(gap-r-2*a)**2
    return max(1, int(bound.upper().ceil().unique_fmpz()))
