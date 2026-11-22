"""Affine enclosures on a fixed binary grid. The residual has no sign constraint."""
from fractions import Fraction as Q

SCALE = 1 << 72


class Form:
    __slots__ = ("center", "coeff", "rest", "radius")

    def __init__(self, center, coeff, rest):
        self.center = center
        self.coeff = coeff
        self.rest = rest
        self.radius = sum(map(abs, coeff.values())) + rest

    @classmethod
    def parameter(cls, lo, hi, key=None):
        lo, hi = Q(lo), Q(hi)
        assert lo <= hi and (key is not None or lo == hi)
        center = ((lo + hi) * SCALE / 2).__floor__()
        half = ((hi - lo) * SCALE / 2).__floor__()
        # Enclose the error of the affine map at both ends. It is linear in the noise.
        rest = max(abs(lo * SCALE - (center - half)),
                   abs(hi * SCALE - (center + half))).__ceil__()
        return cls(center, {key: half} if half else {}, rest)

    def __add__(self, other):
        out = self.coeff.copy()
        for key, value in other.coeff.items():
            out[key] = out.get(key, 0) + value
        return Form(self.center + other.center, out, self.rest + other.rest)

    def __neg__(self):
        return Form(-self.center, {k: -v for k, v in self.coeff.items()}, self.rest)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        # Keep the first derivative in each shared parameter. Charge all higher-order
        # terms and all fixed-grid rounding errors to a symmetric residual.
        numer = self.center * other.center
        center, rounding = divmod(numer, SCALE)
        coeff = {}
        for k in self.coeff.keys() | other.coeff.keys():
            numer = self.center * other.coeff.get(k, 0) + other.center * self.coeff.get(k, 0)
            term, remainder = divmod(numer, SCALE)
            if term:
                coeff[k] = term
            rounding += remainder
        residual = (abs(self.center) * other.rest + abs(other.center) * self.rest
                    + self.radius * other.radius + rounding)
        return Form(center, coeff, -(-residual // SCALE))

    def ends(self):
        return Q(self.center - self.radius, SCALE), Q(self.center + self.radius, SCALE)


def fixed(x):
    return Form.parameter(x, x)


def phase_box(tube, edges, tile, rho, clock_boxes=None, inlet_box=None):
    import support
    _, centers, radius, eta, _, _ = tube
    dlo, dhi = support.DELTA
    ebox = [offset / d for offset in tile for d in (dlo, dhi)]
    e = Form.parameter(min(ebox), max(ebox), 'e')
    duration = fixed(4) - e
    mass_duration = fixed(4) * Form.parameter(dlo, dhi, 'delta') * duration
    if clock_boxes is None:
        clock_boxes = {j:(c-radius, c+radius) for j,c in centers.items()}
    if inlet_box is None:
        inlet_box = (rho-Q(1,32),rho+Q(1,32))
    u = {j: Form.parameter(*limits, ('u',j)) for j,limits in clock_boxes.items()}
    # Reconstruct the affine dwell fractions directly from consecutive path midpoints.
    paths = tube[0]
    shares = dict.fromkeys(support.I, fixed(0))
    half = fixed(Q(1, 2))
    for path in paths:
        cuts = [fixed(0)] + [(u[a] + u[b]) * half for a, b in zip(path, path[1:])] + [fixed(1)]
        for j, left, right in zip(path, cuts, cuts[1:]):
            shares[j] = shares[j] + (right - left)

    clock = {j: fixed(j - 5) for j in support.PAST + support.FUTURE}
    clock[3] = clock[3] + e
    weights = dict.fromkeys(support.FUTURE, fixed(Q(1, 8)))
    weights.update(dict.fromkeys(support.PAST, Form.parameter(*inlet_box, 'rho')))
    for j in support.I:
        clock[j] = clock[3] + duration * u[j]
        weights[j] = (mass_duration * shares[j] * fixed(Q(1, len(paths)))
                      * Form.parameter(1 - eta, 1 + eta, ('jitter', j)))
    terms = [fixed(1) for _ in range(15)]
    for a, b, weight in edges:
        diff = clock[b] - clock[a]
        terms[b] = terms[b] + diff * diff * fixed(Q(weight, 19))
    total = sum((weights[j] * terms[j] for j in range(15)), fixed(0))
    return (fixed(Q(-1, 2)) * total).ends()
