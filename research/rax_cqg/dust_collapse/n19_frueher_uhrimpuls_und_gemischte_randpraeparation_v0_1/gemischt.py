"""Relaxed boundary Hessian and validated stationary mixed-boundary solutions."""
from decimal import Decimal
from fractions import Fraction as F
import json

from algebra import box, hull, mid, inv, matvec, prod, correction, solve_box, magnitude
from quelle import DATA, SCALE, Box
from frueh import CLOCK, WEIGHT, PAST, FUT, Z, R

Y, W, ORDER, COEFF, _, WINDOWS = DATA
COLLAR_Y = dict(zip(PAST + FUT, map(F, (-5, -4, -3, F(-11, 6), 2, 3, 4, 5))))
COLLAR_W = {i: F(W[i].lo, SCALE) for i in PAST + FUT + [15, 17]}
assert all(W[i].lo == W[i].hi for i in COLLAR_W)
N = len(CLOCK) + len(WEIGHT)


class Action:
    def __init__(self, mixed):
        self.mixed = mixed
        self.n = N + 2 * mixed
        clock_axes = {i: k for k, i in enumerate(CLOCK)}
        weight_axes = {j: k + len(CLOCK) for k, j in enumerate(WEIGHT)}
        self.edges = []
        for (i, j), c in sorted(COEFF.items()):
            if not c:
                continue
            incidence = {}
            for node, sign in ((i, -1), (j, 1)):
                if node in clock_axes:
                    incidence[clock_axes[node]] = sign
                if mixed and node in PAST:
                    incidence[N] = incidence.get(N, 0) + sign
                if mixed and node == 0:
                    incidence[N+1] = sign
            axes = [(k, v) for k, v in incidence.items() if v]
            self.edges.append((i, j, c, axes, weight_axes.get(j)))

    def fields(self, x):
        cast = box if isinstance(x[0], Box) else mid
        y = {i: cast(v) for i, v in COLLAR_Y.items()}
        w = {i: cast(v) for i, v in COLLAR_W.items()}
        y.update(zip(CLOCK, x[:len(CLOCK)], strict=True))
        w.update(zip(WEIGHT, x[len(CLOCK):N], strict=True))
        if self.mixed:
            for i in PAST:
                y[i] += x[N]
            y[0] += x[N+1]
        return y, w

    def evaluate(self, x, targets=(0, 0)):
        y, w = self.fields(x)
        zero = box(0) if isinstance(x[0], Box) else Decimal(0)
        g = [zero] * self.n
        H = [[zero] * self.n for _ in range(self.n)]
        for k in range(len(CLOCK), N):
            g[k] += 19
        for i, j, c, axes, weight_axis in self.edges:
            d = y[j] - y[i]
            for k, vk in axes:
                g[k] += 2*c*vk*w[j]*d
                for l, vl in axes:
                    H[k][l] += 2*c*vk*vl*w[j]
            if weight_axis is not None:
                g[weight_axis] += c*d*d
                for k, vk in axes:
                    term = 2*c*vk*d
                    H[k][weight_axis] += term
                    H[weight_axis][k] += term
        if self.mixed:
            for k, target in enumerate(targets):
                g[N+k] += 2*target
        return g, H


def propose(model, x, targets=(0, 0)):
    for _ in range(12):
        g, H = model.evaluate(x, targets)
        if max(map(abs, g)) < Decimal('1e-45'):
            return x
        dx = matvec(inv(H), g)
        x = [v - step for v, step in zip(x, dx)]
    raise ArithmeticError('Newton proposal did not converge')


def certify(model, proposal, targets, radius):
    centres = [F(v.quantize(Decimal('1e-30'))) for v in proposal]
    domain = [hull(v-radius, v+radius) for v in centres]
    assert all(box(v).lo == box(v).hi for v in centres)
    _, H = model.evaluate(domain, targets)
    C, q = correction(H)
    g, _ = model.evaluate(list(map(box, centres)), targets)
    residual = max(magnitude(v) for v in matvec(C, g))
    assert residual + q*radius < radius
    return domain, {'radius': str(radius), 'q_inf_upper': str(q),
                    'centre_step_inf_upper': str(residual),
                    'solution_centres': [str(v) for v in centres]}


def schur(H):
    interior = [row[:N] for row in H[:N]]
    cols = [solve_box(interior, [row[k] for row in H[:N]]) for k in (N, N+1)]
    K = [[-(H[i][N+j] - prod(H[i][:N], cols[j]))/2 for j in range(2)]
         for i in (N, N+1)]
    assert (K[0][1] - K[1][0]).contains_zero()
    determinant = K[0][0]*K[1][1] - K[0][1]*K[1][0]
    assert determinant.hi < 0
    return K, determinant


def validate_state(model, domain):
    y, w = model.fields(domain)
    assert all(y[i].hi < y[j].lo for i, j in ORDER)
    assert all(0 < w[i].lo <= w[i].hi < SCALE for i in WEIGHT+PAST+FUT)
    assert all(w[i].lo == w[i].hi == 0 for i in (15, 17))
    charts = {}
    for name, origin, end in [('fixed', box(F(-11, 6)), box(2)),
                              ('collar', y[3], y[7])]:
        times = {i: (t-origin)/(end-origin) for i,t in y.items()}
        for (low,high), expected in zip(WINDOWS, (Z,R)):
            marks = sorted(i for i,t in times.items()
                           if w[i].hi > 0 and t.hi >= low*SCALE and t.lo <= high*SCALE)
            assert marks == [expected]
            t = times[expected]
            assert low*SCALE < t.lo and t.hi < high*SCALE
        charts[name] = {str(j): times[j].data() for j in (Z,R)}
    return charts


def evaluate_mixed():
    fixed, mixed = Action(False), Action(True)
    guess = [mid(Y[i]) for i in CLOCK] + [mid(W[i]) for i in WEIGHT]
    base = propose(fixed, guess)
    base_box, base_cert = certify(fixed, base, (0, 0), F(1,10**24))
    assert all(old.lo <= v.lo <= v.hi <= old.hi for old, v in zip(
        [Y[i] for i in CLOCK]+[W[i] for i in WEIGHT], base_box))
    # Mean-value uniqueness also identifies the root within the archived enclosure.
    _, archived_hessian = fixed.evaluate([Y[i] for i in CLOCK] + [W[i] for i in WEIGHT])
    _, archive_q = correction(archived_hessian)
    base_cert['q_uniqueness_archived_box'] = str(archive_q)
    validate_state(fixed, base_box)
    g, H = mixed.evaluate(base_box + [box(0), box(0)])
    base_momenta = [-v/2 for v in g[N:]]
    K, det = schur(H)
    g, _ = mixed.evaluate(base + [Decimal(0), Decimal(0)])
    proposal_p = [-v/2 for v in g[N:]]
    cases = []
    for delta in (F(0), -F(1,10**6), F(1,10**6)):
        target = [base_momenta[0], base_momenta[1] + delta]
        ptarget = [proposal_p[0], proposal_p[1] + mid(delta)]
        x = propose(mixed, base+[Decimal(0), Decimal(0)], ptarget)
        domain, cert = certify(mixed, x, target, F(1,10**13))
        windows = validate_state(mixed, domain)
        if delta:
            assert all(not v.contains_zero() for v in domain[N:])
        cases.append({'delta_G0': str(delta), 'delta_sum_G': '0', 'proof': cert,
                      'a': domain[N].data(), 'b': domain[N+1].data(), 'window_times': windows})
    return {'nominal_e': '1/6', 'reference': base_cert, 'reference_momenta':
            [v.data() for v in base_momenta], 'relaxed_jacobian':
            [[v.data() for v in row] for row in K], 'determinant': det.data(),
            'clock_axes': CLOCK, 'weight_axes': WEIGHT, 'mixed_cases': cases,
            'physical_P3': {'NOT_RUN': 60}}


if __name__ == '__main__':
    print(json.dumps(evaluate_mixed(), indent=2, sort_keys=True))
