"""Conditional scalar Hilbert sector of two N14 branches under the inherited preparation."""
import argparse
import json
from itertools import combinations
from pathlib import Path
import sys

import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "v05"))
import growth
from abel_check import numerical_state
from cuts import reduced

MASKS = (1790, 5374)


def scalar_image(kernel, omega):
    """Precision divided by beta after the Gaussian integral for a real action kernel."""
    xx, xy, yy = kernel[:3, :3], kernel[:3, 3:], kernel[3:, 3:]
    assert xy.det() != 0
    return (xy.T * (omega - sp.I * xx).inv() * xy - sp.I * yy).applyfunc(sp.cancel)


def expanding_power(kernel, power):
    # From p=-K_xx x-K_xy y and p'=K_yx x+K_yy y.
    xx, xy, yy = kernel[:3,:3], kernel[:3,3:], kernel[3:,3:]
    b = -xy.inv()
    a = b * xx
    transform = a.row_join(b).col_join((xy.T+yy*a).row_join(yy*b))
    j = growth.geometry.symplectic(3)
    assert transform.T * j * transform == j
    trace = (transform**power).trace()
    assert abs(trace) > transform.rows
    return {"power":power, "trace_exact":str(trace), "trace":float(trace),
            "matrix_dimension":transform.rows}


def positivity(omega):
    assert omega.T == omega
    real = omega.applyfunc(sp.re)
    minors = [real[:k, :k].det() for k in (1, 2, 3)]
    assert all(z > 0 for z in minors)
    return minors


def propagated_state(kernel, signature, source, input_state):
    """Metaplectic normalization in the declared canonical coordinates; Fresnel phase retained."""
    beta = 4 / mp.sqrt(6)
    target = scalar_image(kernel, source)
    positivity(target)
    xx, xy = kernel[:3, :3], kernel[:3, 3:]
    sqrt_det = growth.geometry.continued_sqrt(growth.geometry.numeric(source - sp.I * xx))
    det_xy = xy.det()
    factor = mp.sqrt(mp.mpf(int(abs(det_xy.p))) / int(det_xy.q))
    phase = mp.exp(mp.j * int(signature) * mp.pi / 4)
    amplitude = input_state[1] * factor * phase / sqrt_det
    return target, (beta * growth.geometry.numeric(target), amplitude)


def overlap(left, right):
    t = left[0].apply(mp.conj) + right[0]
    return mp.conj(left[1]) * right[1] * (2 * mp.pi)**mp.mpf("1.5") / growth.geometry.continued_sqrt(t)


def complex_pair(x):
    return [float(mp.re(x)), float(mp.im(x))]


def matrix_entries(m):
    return [[complex_pair(m[i, j]) for j in range(m.cols)] for i in range(m.rows)]


def gram(states):
    return mp.matrix([[overlap(left, right) for right in states] for left in states])


def run():
    if not __debug__:
        raise RuntimeError("Keep Python assertions enabled")
    mp.mp.dps = 80
    beta = 4 / mp.sqrt(6)
    standard = (beta * mp.eye(3), (beta/mp.pi)**mp.mpf(".75"))
    kernels, omegas, states, rows = [], [], [], {}
    with growth.scalar_layouts():
        for mask in MASKS:
            row, state = growth.geometry.kernel((6, mask))
            K, det_v, signature = reduced(mask)
            assert row["status"] == "ADMISSIBLE" and det_v != 0
            assert signature == row["bulk_gauge_signature"]
            assert row["delta_constraints"] == row["free_directions"] == 0
            assert row["symplectic_both_directions"] and row["legendre_rank"] == 3
            omega, check = propagated_state(K, signature, sp.eye(3), standard)
            direct_error = max(max(abs(z) for z in state[0]-check[0]), abs(state[1]-check[1]))
            assert direct_error < mp.mpf("1e-50")
            abel_rows = []
            for eps in ("1e-16", "1e-28"):
                p, phase = numerical_state((6, mask), mp.mpf(eps))
                abel_rows.append({"epsilon":eps,
                                  "precision_error":float(max(abs(z) for z in state[0]-p)),
                                  "unit_phase_error":float(abs(phase-state[1]/abs(state[1])))})
            assert max(abel_rows[-1][k] for k in ("precision_error","unit_phase_error")) < 1e-17
            kernels.append((K, signature))
            states.append(state)
            omegas.append(omega)
            rows[str(mask)] = {"F4": row["F4"], "integration_rank": row["integration_rank"],
                               "mixed_rank": row["legendre_rank"], "free_directions": 0,
                               "delta_constraints": 0, "symplectic_both_directions": True,
                               "bulk_signature": signature, "leading_real_minors": list(map(str,positivity(omega))),
                               "normalization_constant":complex_pair(state[1]),
                               "first_diagonal_precision_over_beta":str(omega[0,0]),
                               "direct_action_replay_error":float(direct_error), "abel":abel_rows}

    G = gram(states)
    z = G[0, 1]
    assert max(abs(G[i,i] - 1) for i in (0,1)) < mp.mpf("1e-55")
    assert abs(G[1,0] - mp.conj(z)) < mp.mpf("1e-60")
    det_t = (omegas[0].conjugate() + omegas[1]).det()
    q = sp.cancel(64 * positivity(omegas[0])[-1] * positivity(omegas[1])[-1]
                  / (det_t * sp.conjugate(det_t)))
    assert q.is_Rational and 0 < q < 1
    assert abs(abs(z)**4 - mp.mpf(int(q.p))/int(q.q)) < mp.mpf("1e-55")
    D = mp.diag([mp.exp(mp.j*rows[str(mask)]["F4"]) for mask in MASKS])
    Ggravity = D.H * G * D
    bins = growth.geometry.readout(dict(zip(MASKS, states)))
    assert max(abs(sum(bins[:,i,j]) - complex(G[i,j])) for i in (0,1) for j in (0,1)) < 1e-14

    # Probe closure after deliberately identifying y and the next x in the same chart.
    # Each original coordinate-linear symplectic map is unitary with our fixed scalar
    # measure; its isometric action does not imply invariance of a finite output span.
    repeats = {}
    for mask, (K, signature) in zip(MASKS,kernels):
        images = [propagated_state(K,signature,omega,state) for omega,state in zip(omegas,states)]
        inner_error = max(abs(v) for v in gram([state for _,state in images])-G)
        assert inner_error < mp.mpf("1e-50")
        tests = {}
        for source, (omega,state) in zip(MASKS,images):
            diagonal = [omegas[0][0,0],omegas[1][0,0],omega[0,0]]
            # Distinct exponential rates along the real y1 line give a nonzero
            # Vandermonde determinant, proving exact linear independence of three Gaussians.
            assert all(sp.cancel(x-y) != 0 for x,y in combinations(diagonal,2))
            h = mp.matrix([overlap(s,state) for s in states])
            residual = 1 - (h.H * (G**-1) * h)[0]
            assert abs(mp.im(residual)) < mp.mpf("1e-50") and 0 < mp.re(residual) <= 1
            tests[str(source)] = {"image_first_diagonal_precision_over_beta":str(omega[0,0]),
                                  "squared_norm_outside_span":float(mp.re(residual)),
                                  "independent_of_both_first_outputs":True}
        repeats[str(mask)] = {"scalar_isometry_gram_error":float(inner_error),"by_input":tests,
                              "expansion_witness":expanding_power(K, 1 if mask == 1790 else 4)}
    return {"order":list(MASKS), "conditional_scalar_branches":rows,
            "gram_scalar":matrix_entries(G), "gram_gravity_only":matrix_entries(Ggravity),
            "pointer_effects_scalar":[[[complex_pair(b[i,j]) for j in (0,1)] for i in (0,1)] for b in bins],
            "absolute_overlap":float(abs(z)), "absolute_overlap_fourth_power_exact":str(q),
            "eigenvalues":[float(1-abs(z)), float(1+abs(z))],
            "rank":2, "nullity":0, "identity_chart_repetition":repeats,
            "scope":"Three scalar boundary modes, fixed quotient, normalized Gaussian input, unitary scalar branch transports in the declared chart. No full coupled physical inner product or dynamical projection is inferred."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(run(),sort_keys=True,indent=2,allow_nan=False)+"\n")
