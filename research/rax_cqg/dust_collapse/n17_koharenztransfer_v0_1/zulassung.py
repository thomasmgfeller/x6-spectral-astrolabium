"""Outcome-free admission for canonical type 42429, exact rational enclosures."""
from fractions import Fraction as Q
from importlib.util import module_from_spec, spec_from_file_location
from math import isqrt
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "basis"


def load(name, path):
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


witness = load("original42429", BASE / "zeuge42429.py")
matrix = load("previous_scalar", BASE / "n17/basis/skalar.py")
iv = load("previous_interval", BASE / "n17/basis/basis/port/basis/density_translation_375841.py")
box, add, sub = iv.box, iv.plus, iv.minus
scale, mul, square, total = iv.scale, iv.times, iv.square, iv.add_all
P, I, F = witness.PAST, witness.INNER, witness.FUTURE
H, R, HMAX = Q(1, 2**20), Q(1, 2**32), Q(1, 2**18)
M, DENSITY = witness.MASS, Q(1, 8)
DEN = 10**18
DNUM = isqrt(isqrt(3 * DEN**4 // 722))
DELTA = (Q(DNUM, DEN), Q(DNUM + 1, DEN))
assert DELTA[0]**4 <= Q(3, 722) < DELTA[1]**4


def divide(num, den):
    assert den[0] > 0
    return mul(num, (1 / den[1], 1 / den[0]))


def layer_weights(relation):
    return {(a, b): matrix.LAYERS[k] for a, b in relation
            if (k := sum((a, j) in relation and (j, b) in relation for j in range(17))) < 4}


def develop():
    relation = witness.build_order()
    paths = witness.order_paths(relation)
    longest = [p for p in paths if len(p) == max(map(len, paths))]
    assert len(longest) == 1
    # Includes all past collar nodes even if a structurally equivalent labelling is used.
    ideal = set(P + longest[0])
    assert all(i in ideal for i, j in relation if j in ideal)
    geometries = {}
    for name, first_ideal in (("viererkette", ideal), ("abgeschirmt", set(range(15)))):
        full = relation | {(i, 15) for i in first_ideal} | {(i, 16) for i in range(16)}
        assert all((i, k) in full for i, j in full for b, k in full if j == b)
        weights = layer_weights(full)
        assert all((i, j) not in weights for i in P for j in (15, 16))
        assert {(i, j): v for (i, j), v in weights.items() if j < 15} == layer_weights(relation)
        assert weights[15, 16] == 1
        geometries[name] = (full, weights)
    return relation, paths, geometries


def cells(paths, u):
    result = {v: box(0) for v in I}
    for path in paths:
        cuts = [box(0)] + [scale(Q(1, 2), add(u[i], u[j])) for i, j in zip(path, path[1:])] + [box(1)]
        for v, lo, hi in zip(path, cuts, cuts[1:]):
            assert lo[1] < hi[0]
            result[v] = add(result[v], scale(Q(1, len(paths)), sub(hi, lo)))
    return result


def packet(relation, paths, shift):
    u = dict(witness.CENTER)
    u[11] += shift
    current0, dwell = witness.source_charge(relation, u)
    assert witness.action_difference(u) == (current0, dwell)
    witness.check_interior(relation, u, dwell)
    y0 = {i: Q(i - 5) for i in P + F}
    y0[3] += witness.E
    duration0 = 4 - witness.E
    y0.update({j: -2 + witness.E + duration0 * u[j] for j in I})
    w0 = {j: M * duration0 * dwell[j] for j in I}
    y = {j: box(n, R if j in I + (3,) else H if j in F[1:] else 0) for j, n in y0.items()}
    w = {j: box(n, R) for j, n in w0.items()}
    e = add(y[3], box(2))
    assert Q(1, 32) < mul(DELTA, e)[0] < mul(DELTA, e)[1] < Q(3, 32)
    duration = sub(box(4), e)
    us = {j: divide(sub(y[j], y[3]), duration) for j in I}
    assert all(abs(z - witness.CENTER[j]) < Q(1, 64) for j in I for z in us[j])
    assert all(y[i][1] < y[j][0] for i, j in relation)
    assert all(max(map(abs, mul(DELTA, v))) < Q(3, 2) for v in y.values())
    fractions = cells(paths, us)
    for j in I:
        normw = divide(w[j], scale(M, duration))
        assert 0 < Q(99, 100) * fractions[j][1] < normw[0] <= normw[1] < Q(101, 100) * fractions[j][0]
        assert 0 < mul(DELTA, w[j])[0] < mul(DELTA, w[j])[1] < 1
    weights = layer_weights(relation)
    p = scale(Q(1, 19), total(mul(w[j], total(scale(weights.get((i, j), 0), sub(y[i], y[j]))
                                               for i in P)) for j in I))
    assert p[0] <= M * current0 <= p[1] and p[0] * p[1] > 0
    assert (shift < 0) == (p[0] > 0)
    return y, w, {"shift_u11": shift, "Y_center": y0, "W_inner_center": w0,
                  "p_reference": M * current0, "p_complete_packet": p}


def phase_cone(whole_order, weights, y, w):
    # Uniform over the full final density domain, both clock projections and a
    # mixture of sharp clocks. This only tests for a nonzero conditional norm.
    clocks = {**y, 15: box(6, HMAX), 16: box(7)}
    assert all(clocks[i][1] < clocks[j][0] for i, j in whole_order)
    slopes = {j: add(box(-Q(1, 2)), scale(-Q(1, 38), total(
        scale(b, square(sub(clocks[i], clocks[j]))) for (i, k), b in weights.items() if k == j)))
              for j in range(17)}
    # The four input nodes share the same entrance density w_P.
    phase = total([mul((Q(3, 32), Q(5, 32)), total(slopes[j] for j in P))]
                  + [mul(mul(DELTA, w[j]), slopes[j]) for j in I]
                  + [mul(box(DENSITY, H), slopes[j]) for j in F + (15, 16)])
    span = phase[1] - phase[0]
    floor = 1 - span**2 / 8
    assert floor > 0
    return {"dust_phase_span_upper": span, "dust_amplitude_modulus_lower_per_normalized_mass": floor}


def scalar(weights):
    first = {edge: b for edge, b in weights.items() if edge[1] < 16}
    initial = matrix.framed_hessian(16, first)
    g = [row + [Q(0)] for row in initial] + [[Q(0)] * 17]
    for (i, j), b in weights.items():
        if j != 16:
            continue
        direction = [Q(0)] * 17
        if i == 15:
            direction[15] = 1
        else:
            collar = F.index(i)
            if collar < 3:
                direction[3 + collar] = 1
            direction[14] = (0, 16, 32, 46)[collar]
        direction[16] = -1
        for a in range(17):
            for c in range(17):
                g[a][c] -= Q(b, 2) * direction[a] * direction[c]
    hidden, remain = list(range(6, 15)), list(range(6)) + [15, 16]
    det, inv = matrix.det_inverse(matrix.block(g, hidden, hidden))
    links = matrix.block(g, remain, hidden)
    correction = matrix.multiply(matrix.multiply(links, inv), matrix.transpose(links))
    k = [[g[i][j] - correction[a][b] for b, j in enumerate(remain)] for a, i in enumerate(remain)]
    a, c, d = matrix.block(k, range(6), range(6)), matrix.block(k, range(6), [6, 7]), matrix.block(k, [6, 7], [6, 7])
    a2 = matrix.multiply(a, a)
    detg, invg = matrix.det_inverse([[v + (i == j) for j, v in enumerate(row)] for i, row in enumerate(a2)])
    cg = matrix.multiply(matrix.transpose(c), invg)
    real = matrix.multiply(cg, c)
    imag_correction = matrix.multiply(cg, matrix.multiply(a, c))
    phase = [[d[i][j] - imag_correction[i][j] for j in range(2)] for i in range(2)]
    assert det and detg > 0 and real[0][0] >= 0 and real[1][1] >= 0
    assert real[0][1] == real[1][0] and real[0][0] * real[1][1] >= real[0][1]**2
    # At q16=0 the remaining integral is average exp[(-a+i b) q15²] on [-1,1].
    # If b=0 its real part is positive; otherwise sign(b) times the imaginary
    # part is positive by pairing successive lobes of sin(s) against the
    # strictly decreasing positive weight exp(-a*s/abs(b))/sqrt(s).
    assert real[0][0] >= 0
    return {"hidden_det": det, "det_I_plus_A_squared": detg, "real_over_beta": real,
            "phase_over_beta": phase, "positive_finite_conditional_norm": True}


def run():
    relation, paths, geometries = develop()
    packets = {tag: packet(relation, paths, shift)
               for tag, shift in (("positiv", -Q(1, 128)), ("negativ", Q(1, 128)))}
    data = {"order": witness.CODE, "status": "ZUGELASSEN", "target": "NOT_RUN",
            "max_clock_halfwidth": HMAX, "final_density_halfwidth": H, "packet_halfwidth": R,
            "paths": paths, "packets": {s: item[2] for s, item in packets.items()}, "geometries": {}}
    for name, (whole, weights) in geometries.items():
        data["geometries"][name] = {
            "incoming15": {i: b for (i, j), b in sorted(weights.items()) if j == 15},
            "incoming16": {i: b for (i, j), b in sorted(weights.items()) if j == 16},
            "current_change": 0, "scalar": scalar(weights),
            "norm_certificates": {s: phase_cone(whole, weights, y, w) for s, (y, w, _) in packets.items()}}
    return data


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Use Python without -O for the admission checks.")
    print(json.dumps(run(), default=str, sort_keys=True, indent=2))
