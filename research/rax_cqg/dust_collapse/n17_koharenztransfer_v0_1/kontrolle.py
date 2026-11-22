"""Finite whole-packet bounds for a Fourier measurement of the N16 clock."""
from fractions import Fraction as Q
import json
from pathlib import Path
import sys

SOURCE = Path(__file__).resolve().parent / "basis" / "n17"
sys.path.insert(0, str(SOURCE))
import uhrfenster as window

cap, n16, old = window.cap, window.n16, window.old
H, M = cap.H, cap.M
CASE = "stromerhaltend"


def check_center_factorization(family, first, final):
    """Check exactly which moving old variables can reach each new phase."""
    yp, wp = family["positiv"]
    yn, wn = family["negativ"]
    assert {i for i in yp if yp[i] != yn[i]} == {6}
    assert all(wp[i] == wn[i] for i in old.P + old.F)
    # The only old future density with a differing slope is w7. Its own
    # slope has no dependence on Y8,Y9,Y10. Old entrance/inner terms also
    # have no such dependence, so their relative phases factor out.
    assert all(old.B.get((6, j), 0) == 0 for j in old.F[1:] + old.P)
    assert all(old.B.get((i, j), 0) == 0 for i in old.F[1:]
               for j in old.P + old.I + (7,))
    assert not set(first) & set(old.F)
    assert not set(first) & set(old.P)
    assert set(final) <= set(old.F) | {15}
    assert final[15] == 1
    assert n16.YN == 6 and cap.Y16 == 7


def uniform_branch(center, old_reference, first, final):
    clock, _ = center
    region = old.whole_cell(center, old_reference)
    base = n16.budget(first, center, region)
    hidden = old.I + (3,)

    # Shift of the old hidden-clock phase perturbation at fixed x. The
    # additional term is odd in the hidden displacement, so its mean is 0.
    extra = sum((M + H) * abs(weight) * 2 * H * old.RADIUS / 38
                for i, weight in first.items() if i in hidden)
    point_error = (base["max_mittlere_phasenabweichung"] +
                   (base["max_phasenfehler"] + extra) ** 2 / 2)
    cone, receipt_distance, current = window.branch_bound(
        CASE, center, old_reference, first, final)
    # For fixed x remove its t-dependent carrier in BOTH compared outputs.
    # This is done only for the within-x bound, never before coherent summation.
    eta = H * cap.relative_slope_span(final, clock, cap.Y16)
    assert Q(99, 100) < cone <= 1 and 0 <= point_error < cone and eta < cone
    anchor_error = eta * point_error * (1 + 1 / cone) / (cone - point_error)
    distance = 2 * anchor_error / (1 - eta / cone)
    assert distance <= receipt_distance

    # |d S/dx| from both births, before all other integrations; uniform
    # on the full original support, without removing any x-dependent carrier.
    first_derivative = Q(0)
    for i, weight in first.items():
        width = old.RADIUS if i in hidden else H if i in old.F[1:] else 0
        first_derivative += abs(weight) * (abs(clock[i] - n16.YN) + width + H)
    final_derivative = abs(final[15]) * (abs(n16.YN - cap.Y16) + H)
    lipschitz = (M + H) * (first_derivative + final_derivative) / 19
    norm_lower = (cone - point_error) ** 2
    # Relative to the common clock + final system AFTER prior operations.
    # Parseval: nonzero clock-mode mass equals integrated clock variance.
    rejected_mass = lipschitz ** 2 * H ** 2 / 3
    receipt_loss = rejected_mass / norm_lower
    assert Q(0) <= receipt_loss < 1 and 0 < norm_lower <= 1
    return {
        "current": current,
        "center_modulus_lower": cone,
        "whole_amplitude_error": point_error,
        "fixed_clock_anchoring_eta": eta,
        "bin_probability_error_uniform_in_clock": distance,
        "dust_norm_mixed_interval": [norm_lower, Q(1)],
        "dust_norm_coherent_interval": [norm_lower, Q(1)],
        "clock_amplitude_lipschitz_bound": lipschitz,
        "clock_mode_zero_relative_success_interval": [1 - receipt_loss, Q(1)],
    }


def run():
    ideal = n16.CASES[CASE]
    _, _, final = cap.geometry(ideal)
    first = n16.new_edges(ideal)
    coherent_frozen = json.loads((SOURCE / "uhrfenster.json").read_text())[CASE]
    sharp_frozen = json.loads((SOURCE / "ergebnis.json").read_text())[CASE]
    assert cap.schur_scalar(ideal, final)["nonzero_at_final_scalar_zero"]
    results = {}
    for label, q in (("original", old.STEP), ("transfer", old.STEP / 2)):
        neutral, family = n16.packet_family(q)
        check_center_factorization(family, first, final)
        ref = -n16.old_coefficient(neutral)[7] / 2
        branches = {name: uniform_branch(center, ref, first, final)
                    for name, center in family.items()}
        assert branches["positiv"]["current"][0] > 0 > branches["negativ"]["current"][1]
        error_sum = sum(s["bin_probability_error_uniform_in_clock"]
                        for s in branches.values())
        mixed = old.box(Q(0), error_sum)
        coherent = window.evaluate(CASE, q)["whole_gap"]
        assert tuple(coherent) == tuple(map(Q, coherent_frozen[label]["whole_gap"]))
        sharp = cap.packets(CASE, ideal, final, q)["closed_all_binary_effects_upper"]
        assert sharp == Q(sharp_frozen[label]["closed_all_binary_effects_upper"])
        difference = old.sub(coherent, mixed)
        assert difference[1] < 0 and mixed[0] <= 0 <= mixed[1]
        results[label] = {
            "q_abs": q,
            "branches": branches,
            "delta_coherent_whole": coherent,
            "delta_mixed_center": Q(0),
            "delta_mixed_whole": mixed,
            "delta_coherent_minus_delta_mixed_whole": difference,
            "delta_sharp_whole_any_binary": old.box(Q(0), sharp),
        }
    return results


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Prüfung ohne -O ausführen.")
    print(json.dumps(run(), indent=2, sort_keys=True, default=str))
