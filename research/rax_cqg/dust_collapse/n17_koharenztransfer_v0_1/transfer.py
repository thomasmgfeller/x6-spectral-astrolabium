"""Whole-packet decision for the publicly fixed coherent / mixed N17 transfer."""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json
import sys

import zulassung as admission

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "basis/n17"))
import uhrfenster as prior

H, R, M = admission.H, admission.R, admission.DENSITY
P, I, F = admission.P, admission.I, admission.F
box, add, sub, mul, scale = admission.box, admission.add, admission.sub, admission.mul, admission.scale
PHASE_CLOCK = prior.C
PHASE_QUADRATIC = prior.E
FREEZE = "9812f27b3c9b5f385e386ff4454597cea7915c682027b259dc2083bcfaa52ab2"


def check_hidden_error(weights, y, w):
    """Average over the 15 independent inner axes holding all other variables fixed."""
    hidden = set(I + (3,))
    clocks = {**y, 15: box(6, H), 16: box(7)}
    density_max = {j: Q(5, 32) for j in P}
    density_max.update({j: admission.DELTA[1] * w[j][1] for j in I})
    density_max.update({j: M + H for j in F + (15, 16)})
    phase_sup, mean_phase = Q(0), Q(0)
    for j in range(17):
        slope_sup = Q(1, 2)
        for (i, k), layer in weights.items():
            if k != j:
                continue
            time_span = max(map(abs, sub(clocks[i], clocks[j])))
            coeff = Q(abs(layer), 38)
            slope_sup += coeff * time_span ** 2
            variable_ends = int(i in hidden) + int(j in hidden)
            radius = variable_ends * R
            phase_sup += density_max[j] * coeff * (2 * time_span * radius + radius ** 2)
            mean_phase += density_max[j] * coeff * variable_ends * R ** 2 / 3
        if j in I:
            phase_sup += admission.DELTA[1] * R * slope_sup
    return mean_phase + phase_sup ** 2 / 2


def shape_bound(eta, floor):
    # Squared modulus relative to the value at the output-window midpoint.
    assert 0 <= eta < floor <= 1
    return ((1 - eta / floor) ** 2, (1 + eta / floor) ** 2)


def packet_distance(eta, error, floor):
    assert error < floor and eta < floor
    return 2 * eta * error * (1 + 1 / floor) / ((floor - error) * (1 - eta / floor))


def branch(name, shift, rel, paths, geometry):
    order, weights = geometry
    y, w, data = admission.packet(rel, paths, shift)
    y0 = data["Y_center"]
    floor = admission.phase_cone(order, weights, y, w)["dust_amplitude_modulus_lower_per_normalized_mass"]
    assert floor > Q(99, 100)
    first = {i: b for (i, j), b in weights.items() if j == 15}
    last = {i: b for (i, j), b in weights.items() if j == 16}
    assert not set(first).intersection(F) and set(last) <= set(F) | {15}
    assert last[15] == 1 and all((i, 16) not in weights for i in I + P)
    assert prior.H == H and prior.M == M and PHASE_CLOCK == Q(1, 19)
    d0 = -Q(1, 2) - sum(b * (y0[i] - 6) ** 2 for i, b in first.items()) / 38
    a = sum(b * (y0[i] - 6) for i, b in first.items()) / 19
    b = -Q(sum(first.values()), 38)
    slopes = []
    half = H / 16
    for j in range(16):
        t = M - H + (2 * j + 1) * half
        slopes.append(prior.phase_log_derivative(d0, a, b, t, half))
    derivative = (min(lo for lo, _ in slopes), max(hi for _, hi in slopes))

    # G depends on the three varying old outer clocks. J depends on x and v.
    eta_g = H * sum(abs(last.get(i, 0)) * (2 * abs(y0[i] - 7) * H + H ** 2) / 38 for i in F[1:])
    eta_j = H * (abs(PHASE_CLOCK) * H + abs(PHASE_QUADRATIC) * H ** 2)
    ul, uh = shape_bound(eta_g, floor)
    vl, vh = shape_bound(eta_j, floor)
    # E_high E_low double integral of (t-y) over normalized opposite halves is H/4.
    corr = (ul ** 2 * vl / (uh ** 2 * vh), uh ** 2 * vh / (ul ** 2 * vl))
    center = scale(H / 4, mul(derivative, corr))
    error = check_hidden_error(weights, y, w)
    coh_distance = packet_distance(eta_g + eta_j, error, floor)
    mix_distance = packet_distance(eta_g, error, floor)
    return {"packet": name, "clock_slope_coefficients": (d0, a, b), "log_slope": derivative,
            "phase_cone_lower": floor, "eta_old_outer": eta_g, "eta_clock": eta_j,
            "pointwise_hidden_error": error, "coherent_probability_error": coh_distance,
            "mixed_probability_error": mix_distance,
            "center_coherent_minus_mixed": center,
            "whole_coherent_minus_mixed": add(center, box(0, coh_distance + mix_distance))}


def run():
    assert sha256((ROOT / "TRANSFER_42429.md").read_bytes()).hexdigest() == FREEZE
    admitted = admission.run()
    assert admitted["order"] == 42429 and admitted["status"] == "ZUGELASSEN"
    rel, paths, geometries = admission.develop()
    plus = branch("positiv", -Q(1, 128), rel, paths, geometries["viererkette"])
    minus = branch("negativ", Q(1, 128), rel, paths, geometries["viererkette"])
    center = sub(plus["center_coherent_minus_mixed"], minus["center_coherent_minus_mixed"])
    whole = sub(plus["whole_coherent_minus_mixed"], minus["whole_coherent_minus_mixed"])
    assert whole[0] <= center[0] <= center[1] <= whole[1]
    decision = "PASS_NONZERO" if whole[0] > 0 or whole[1] < 0 else "UNRESOLVED_FIRST_GRID"
    return {"type": 42429, "contract_sha256": FREEZE, "branches": [plus, minus],
            "center_contrast": center, "whole_packet_contrast": whole,
            "decision": decision, "slices": 16, "taylor_order": 5}


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run Python with assertions enabled.")
    print(json.dumps(run(), default=str, indent=2, sort_keys=True))
