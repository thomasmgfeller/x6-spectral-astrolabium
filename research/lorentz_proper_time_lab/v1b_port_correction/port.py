"""Sampling-only Python port and a separately named reconstruction of the old defect.

The PRNG correction preserves JavaScript uint32 semantics. Floating transforms
use Python libm and are checked numerically; cross-runtime bit identity is not
promised. UI validation and confidence-interval inference are outside this module.
"""
import math

MASK = 0xffffffff


def imul(a, b):
    x = ((a & MASK) * (b & MASK)) & MASK
    return x - 2**32 if x >= 2**31 else x


def urshift(x, n):
    return (x & MASK) >> n


class RNG:
    """Corrected port of the commit-pinned JavaScript generator."""
    def __init__(self, seed):
        if type(seed) is not int or not 0 <= seed <= MASK:
            raise ValueError('seed must be an integer in [0, 2**32 - 1]')
        self.state = seed

    def __call__(self):
        self.state = (self.state + 0x6D2B79F5) & MASK
        x = imul(self.state ^ urshift(self.state, 15), 1 | self.state)
        # JS: x ^= x + Math.imul(x ^ (x >>> 7), 61 | x)
        x = (x ^ ((x + imul(x ^ urshift(x, 7), 61 | x)) & MASK)) & MASK
        return ((x ^ urshift(x, 14)) & MASK) / 4294967296


class MissingXorRNG:
    """Reconstruction of the supplied defective port; diagnostic use only."""
    def __init__(self, seed):
        self.state = seed & MASK

    def __call__(self):
        self.state = (self.state + 0x6D2B79F5) & MASK
        x = imul(self.state ^ urshift(self.state, 15), 1 | self.state)
        x = x + imul(x ^ urshift(x, 7), 61 | x)  # Deliberate reproduction of defect.
        return ((x ^ urshift(x, 14)) & MASK) / 4294967296


def normal(random):
    u = max(0.5 / 4294967296, random())
    return math.sqrt(-2 * math.log(u)) * math.cos(2 * math.pi * random())


def cloud(m, d, theta, seed, rng_type=RNG):
    """Port of the supplied coordinate sampler for valid inputs.

    This deliberately retains the original sampler's U=0 boundary behavior,
    so fixing the port cannot conceal a separate defect of the source sampler.
    """
    random = rng_type(seed)
    points, inside = [], []
    for _ in range(m):
        A = .5 * random() ** (1 / d)
        t = (-1 if random() < .5 else 1) * (.5 - A)
        v = [normal(random) for _ in range(d - 1)]
        norm = math.hypot(*v)
        if not norm:
            raise RuntimeError('zero norm')
        radius = A * random() ** (1 / (d - 1))
        point = [t, *[x * radius / norm for x in v]]
        points.append(point)
        inside.append(abs(t) + math.hypot(*point[1:]) < theta / 2)
    return points, inside
