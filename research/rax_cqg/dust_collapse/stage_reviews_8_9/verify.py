"""Reference checks for CST-DUST reviews 8 and 9, using exact fractions."""
from fractions import Fraction as F
from itertools import combinations, product
from math import isqrt

LEVELS = (4, 8, 16, 32, 64)
HALF_WIDTHS = (F(1, 8), F(1, 4), F(1, 2))


def check(condition, message):
    if not condition:
        raise ValueError(message)


def clock_and_volume():
    # In the P3 units T_end/T_s(M) = sqrt(M)/4.
    end_fractions = []
    for mass in (F(1, 4), F(1), F(4)):
        root = F(isqrt(mass.numerator), isqrt(mass.denominator))
        check(root**2 == mass, "irrational mass root")
        end_fractions.append(root / 4)
    check(end_fractions == [F(1, 8), F(1, 4), F(1, 2)], "P3 end times")

    times = (F(3, 4), F(7, 8), F(1), F(9, 8), F(5, 4))
    formal_volumes = [(1 - t)**2 for t in times]
    check(formal_volumes == [F(1, 16), F(1, 64), 0, F(1, 64), F(1, 16)], "volume polynomial")
    check(1 / formal_volumes[1] == 64, "precritical dust density")
    routes = [(times[0], *cuts, times[-1]) for size in range(4)
              for cuts in combinations(times[1:-1], size)]
    check((len(routes), sum(F(1) in path for path in routes)) == (8, 4), "clock partitions")
    print("8 · P3 ends at 1/8, 1/4, 1/2 of T_s. Proposed cuts: 8 paths, 4 through u=1.")


def two_quantum_steps():
    # a denotes an unmeasured intermediate path and b the final orthogonal record.
    branches = list(product((0, 1), repeat=2))
    vectors = [[F((-1)**(a * b), 2) if j == b else F(0) for j in (0, 1)]
               for a, b in branches]
    gram = [[sum(x*y for x, y in zip(left, right)) for right in vectors] for left in vectors]
    fine_diagonal = sum(gram[i][i] for i in range(4))
    check(fine_diagonal == sum(map(sum, gram)) == 1, "normalization")
    for outcome in (0, 1):
        paths = [i for i, (_, b) in enumerate(branches) if b == outcome]
        diagonal = sum(gram[i][i] for i in paths)
        measure = sum(gram[i][j] for i in paths for j in paths)
        check(diagonal == F(1, 2) and measure == 1 - outcome, "interference at final record")
    print("8 · The two final records have measures 1 and 0, each with path diagonal sum 1/2.")


def inverse_moments():
    # Coefficients for alpha=kappa=hbar=1, beta=1/2 in regularity_v0_2.
    a, j, energy = F(7, 4), F(7, 2), F(79, 20)
    time = j / (4 * energy)
    volume = a - 2*j*time + 4*energy*time**2
    check((time, volume) == (F(35, 158), F(77, 79)), "Dirichlet minimum")
    for n in range(1, 21):
        epsilon = F(1, 2**n)
        moment = epsilon**2 / epsilon**2 + (1 - epsilon**2)
        check(moment == 2 - epsilon**2, "small-volume atom")
    print("9 · Dirichlet minimum 77/79 at 35/158. Two-atom inverse moment equals 2-epsilon^2.")


def window_average(level, half_width):
    # Exact trapezoidal integral over the two linear pieces of the triangle.
    support_radius = F(1, level**2)
    check(support_radius <= half_width, "triangle exceeds the integration window")
    area = 2 * F(level, 2) * support_radius
    return area / (2 * half_width)


def smoothing():
    for level, width in product(LEVELS, HALF_WIDTHS):
        check(window_average(level, width) == 1 / (2*level*width), "fixed-width average")
    last = tuple(window_average(64, width) for width in HALF_WIDTHS)
    check(last == (F(1, 16), F(1, 32), F(1, 64)), "finest window averages")
    print("9 · At n=64 the peak is 64 and the three window averages are 1/16, 1/32 and 1/64.")


def spherical_reference():
    # In the effective exterior f(r)=1-2m/r+2m*b^3/r^4, m=GM and b=r_*.
    # f' has the sign of r^3-4b^3. At its minimum, for b=2m, (1-f_min)^3=27/256.
    lower, upper = F(527529606, 10**9), F(527529607, 10**9)
    check((1-upper)**3 < F(27, 256) < (1-lower)**3, "exterior minimum enclosure")
    # Identity in v between degree-two polynomials; three distinct samples suffice.
    for v in (F(0), F(1), F(3, 2)):
        check(1 + (1-v)*(-1-v) == v*v, "normalized null expansions")
    print("9 · Effective exterior: 0.527529606 < f_min < 0.527529607; expansion identity holds.")


if __name__ == "__main__":
    clock_and_volume()
    two_quantum_steps()
    inverse_moments()
    smoothing()
    spherical_reference()
