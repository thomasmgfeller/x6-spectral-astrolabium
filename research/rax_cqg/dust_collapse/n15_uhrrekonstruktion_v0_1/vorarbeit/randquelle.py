"""Fixed sources for the normalized dust action on the N15 entrance chain."""
from fractions import Fraction as Q

LAYERS = (1, -9, 16, -8)
PAST = (0, 1, 2, 3)
UNIFORM = (1, 1, 1, 1)


def edge_weight(interval_size):
    return LAYERS[interval_size] if interval_size < len(LAYERS) else 0


DEPTH_ROWS = tuple(tuple(edge_weight(3 - i + d) for i in PAST) for d in range(4))


def solve_profile():
    """Solve the upper-triangular incidence system with response -64 per depth."""
    profile = [Q(0)] * 4
    for d in reversed(range(4)):
        row = DEPTH_ROWS[d]
        profile[d] = (Q(-64) - sum(row[j] * profile[j] for j in range(d + 1, 4))) / row[d]
    return tuple(profile)


PROFILE = solve_profile()


def translate(y, a, first, b, second):
    shifted = list(y)
    for i in PAST:
        shifted[i] += a * first[i] + b * second[i]
    return shifted


def mixed_response(evaluate, y, h, k, first=UNIFORM, second=PROFILE):
    """Accept an action oracle at fixed fields. No current or density inputs."""
    if h == 0 or k == 0:
        raise ValueError('Both source steps must be nonzero.')
    numerator = sum(s * t * evaluate(translate(y, s*h, first, t*k, second))
                    for s in (1, -1) for t in (1, -1))
    return numerator / (4*h*k)


def visible_sum(evaluate, y, h, k):
    return Q(19, 64) * mixed_response(evaluate, y, h, k)
