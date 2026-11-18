"""Exact cylinder and polarization tests in the marked N<=2 reference path space."""
from fractions import Fraction as F
from itertools import product
import json


A = F(1, 4)
B = F(3, 8)
ENDS = (F(1, 2), F(3, 4), F(1))
BETAS = (F(5, 4), F(4, 3))
BIN_WIDTH = F(1, 16)
POSITIVE_MASS = F(1, 2)
PACKET_MASS = 3 * BIN_WIDTH * POSITIVE_MASS
ONE, ZERO, I = (1, 0), (0, 0), (0, 1)
PHASES = {"plus": ONE, "minus": (-1, 0), "plus_i": I, "minus_i": (0, -1)}


def require(condition, label):
    if not condition:
        raise ValueError(label)


def gaussian_product(x, y):
    return x[0]*y[0] - x[1]*y[1], x[0]*y[1] + x[1]*y[0]


def density_at(bin_index, mark, coefficients):
    """Squared amplitude without the common factor 1/PACKET_MASS."""
    if mark == "zero":
        return 0
    psi = ONE if bin_index in (0, 1, 2) else ZERO
    phi = (ZERO, ONE, I, I)[bin_index]
    x = gaussian_product(coefficients[0], psi)
    y = gaussian_product(coefficients[1], phi)
    return (x[0] + y[0])**2 + (x[1] + y[1])**2


def h1(s, horizon, beta):
    # alpha=z=1. The two terminal two-element types each have h=1.
    return 1 + horizon - s if beta is None else beta - s


def direct(horizon, beta, coefficients, effect):
    """Enumerate the final branches; the event is evaluated via the prefix at B."""
    # Ordered clock bin, old density mark, then each possible future.
    # Each of the two possible final orders carries f(2)^2/f(1)^2=1/2.
    # Integrate the second density mark explicitly over the zero and positive strata.
    total = F(0)
    for idx, mark in product(range(4), ("zero", "positive")):
        old_density = density_at(idx, mark, coefficients)
        if effect and (idx not in (1, 2) or mark != "positive"):
            continue
        old_weight = BIN_WIDTH * POSITIVE_MASS * old_density / PACKET_MASS
        continuation = h1(horizon, horizon, beta)
        for population in ("early", "late"):
            length = B - A if population == "early" else horizon - B
            if effect and population == "early":
                continue
            for order, new_mark in product(("chain", "antichain"), ("zero", "positive")):
                continuation += length * F(1, 2) * POSITIVE_MASS
        total += old_weight * continuation / h1(A, horizon, beta)
    return total


def local_gram(effect):
    """Overlap integral of normalized old packets, including positive-mark mass."""
    # psi: old clock (0,3/16], phi: (1/16,1/4] with phase 1 on bin 1,
    # i on bins 2 and 3. Both supported on 0<w<1.
    return (F(2, 3) if effect else F(1)), (F(1, 3), F(1, 3))


def sewn(horizon, beta, coefficients, effect):
    # Analytic integration at B plus one-step transports.
    # If the old birth count is already 2 at B, no further birth is possible.
    norm, cross = local_gram(effect)
    x, y = coefficients
    xy = gaussian_product((x[0], -x[1]), y)
    real_cross = gaussian_product(xy, cross)[0]
    old_norm = (sum(a*a for a in x) + sum(a*a for a in y))*norm + 2*real_cross
    no_birth_at_cut = h1(B, horizon, beta)/h1(A, horizon, beta)
    future_extension = (h1(horizon, horizon, beta) + horizon - B)/h1(B, horizon, beta)
    born_by_cut = (B - A)/h1(A, horizon, beta)
    continuation = no_birth_at_cut * future_extension
    if not effect:
        continuation += born_by_cut
    return old_norm * continuation


def polarize(q):
    return ((q["plus"] - q["minus"]) / 4, (q["minus_i"] - q["plus_i"]) / 4)


def checked_model(beta):
    expected_ratios = ((F(9, 10), F(11, 12), F(13, 14)) if beta is None
                       else ((beta - B)/(beta - A),)*len(ENDS))
    rows = []
    for horizon, ratio in zip(ENDS, expected_ratios):
        results = {}
        for effect in (True, False):
            q = {}
            for name, xy in {"psi": (ONE, ZERO), "phi": (ZERO, ONE),
                             **{name: (ONE, phase) for name, phase in PHASES.items()}}.items():
                direct_value = direct(horizon, beta, xy, effect)
                require(direct_value == sewn(horizon, beta, xy, effect), "sewing " + name)
                q[name] = direct_value
            results[effect] = q
        q = results[True]
        all_q = results[False]
        require(q["psi"] == q["phi"] == F(2, 3)*ratio, "indicator packet diagonals")
        require(all_q["psi"] == all_q["phi"] == 1, "full normalization")
        require(polarize(q) == (ratio/3, ratio/3), "early complex cross term")
        require(polarize(all_q) == (F(1, 3), F(1, 3)), "full overlap")
        normalized = {key: q[key]/all_q[key] for key in PHASES}
        require(normalized["plus"] == normalized["minus_i"] == 3*ratio/4, "plus record")
        require(normalized["minus"] == normalized["plus_i"] == ratio/2, "minus record")
        # Fault injection 1: dephase the preparation, leaving only packet diagonals.
        erased = {key: q["psi"] + q["phi"] for key in PHASES}
        require(polarize(erased) != polarize(q), "packet phase erasure must be detected")
        # Fault injection 2: impose 'no second birth by horizon' where B is required.
        mistaken_ratio = h1(horizon, horizon, beta)/h1(A, horizon, beta)
        require(mistaken_ratio != ratio, "moving readout must be detected")
        rows.append({
            "horizon": str(horizon), "no_birth_until_B": str(ratio),
            "E_packet_diagonal": str(q["psi"]),
            "E_cross_re_im": list(map(str, polarize(q))),
            "full_cross_re_im": list(map(str, polarize(all_q))),
            "E_for_normalized_superpositions": {k: str(v) for k, v in normalized.items()},
            "wrong_no_birth_until_horizon": str(mistaken_ratio),
        })
    return rows


def main():
    models = {"fixed_terminal_reference": checked_model(None)}
    for beta in BETAS:
        models["linear_h_beta_" + str(beta)] = checked_model(beta)
    delta = (BETAS[1] - B)/(BETAS[1] - A) - (BETAS[0] - B)/(BETAS[0] - A)
    require(delta == F(1, 104), "beta source")
    require(delta/3 == F(1, 312), "beta difference of cross terms")
    result = {
        "model_scope": "orthogonal marked path L2; conditional mathematical references only",
        "cuts": {"a": str(A), "b": str(B)},
        "number_of_direct_sewn_quadratic_pairs": 3 * len(ENDS) * 2 * 6,
        "beta_high_minus_low_cross_re_im": [str(delta/3), str(delta/3)],
        "models": models,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
