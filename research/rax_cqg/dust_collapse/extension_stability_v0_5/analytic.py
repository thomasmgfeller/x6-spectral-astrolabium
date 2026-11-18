"""Sufficient stability bounds, conditional on the reference success probabilities."""
import argparse
from fractions import Fraction as F
import json
from math import factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RATE = F(48, 10000)
AMPLITUDE = F(36085, 10**6)
DENSITY_DIFFERENCE = F(1812, 10**6)
ANCHOR_NORM = F(1966, 10**5)
MIN_SUCCESS = F(379, 10**6)
MIN_SIGNAL = F(667, 10**8)


def bounds(rate):
    difference = AMPLITUDE + ANCHOR_NORM
    level = 2 * rate * ANCHOR_NORM * difference + (rate * difference) ** 2
    contrast = (2 * rate * DENSITY_DIFFERENCE * (difference + 2 * ANCHOR_NORM)
                + 4 * rate**2 * DENSITY_DIFFERENCE * difference)
    return level, contrast


def calibrated_bounds(rate):
    # Measured four-bin contrasts of the reference cancel before taking norms.
    anchor_contrast = F(669, 10**8)
    anchor_pair_change = F(24, 10**5)
    cross = anchor_pair_change * AMPLITUDE + ANCHOR_NORM * DENSITY_DIFFERENCE
    return (rate * (2-rate) * anchor_contrast + 2*rate*(1-rate)*cross
            + 2*rate**2 * AMPLITUDE * DENSITY_DIFFERENCE)


def check_rephasing(row, cap):
    # Complex Taylor polynomial for exp(ix), x=P0/16. The integral
    # remainder in modulus is at most x**13/13! along the real axis.
    x = F(151, 304)
    cosine = sum((-1)**(k//2) * x**k / factorial(k) for k in range(0,13,2))
    sine = sum((-1)**((k-1)//2) * x**k / factorial(k) for k in range(1,13,2))
    rem = x**13 / factorial(13)
    def pair(lobes):
        return [sum(F.from_float(lobe[j]) for lobe in lobes) for j in (0,1)]
    (lr, li), (hr, hi) = map(pair, row['amplitudes']['lobes'])
    assert hr**2 + hi**2 < 1
    diff_squared = (cosine*hr-sine*hi-lr)**2 + (sine*hr+cosine*hi-li)**2
    assert diff_squared < 2*(cap-rem)**2


def run():
    if not __debug__:
        raise RuntimeError("Keep assertions enabled")
    # beta^2=16/6; (beta*STEP)^2=2*beta/19.
    beta_up = F(1633, 1000)
    assert beta_up**2 > F(16, 6) and AMPLITUDE**2 > F(1, 768)
    eta_squared_up = F(1,768) * F(31,256)**2 * 2*beta_up/19
    assert DENSITY_DIFFERENCE**2 > eta_squared_up
    assert 31**2 * 2/(19*beta_up) > (4*F(3,32))**2

    data = json.loads((ROOT / "upstream/results.json").read_text())
    assert data["branch_order"][:2] == ["N11_7", "N11_1"]
    anchors = {}
    source = json.loads((ROOT / "upstream/v03/upstream/v02_grids.json").read_text())["grids"]
    for tag, grids in data["coherent_readout_grid_matrices"].items():
        successes = [sum(F.from_float(e[i][j]) / 4 for e in matrix[:3]
                         for i in range(2) for j in range(2)) for matrix in grids]
        accepted = [[sum(F.from_float(effect[i][j])/4 for i in range(2) for j in range(2))
                     for effect in matrix[:3]] for matrix in grids]
        p0, p1 = [p + [1-sum(p)] for p in accepted]
        reference_contrast = sum(abs(x-y) for x,y in zip(p0,p1))/2
        assert reference_contrast <= F(669, 10**8)
        pos = {'coarse':-2, 'fine':-1}[tag]
        for name,cap in [('chain', F(165,10**6)), ('one', F(315,10**6))]:
            check_rephasing(source[name][pos],cap)
        signal = successes[0] - successes[1]
        assert signal >= MIN_SIGNAL
        assert min(successes) >= MIN_SUCCESS and max(successes) <= ANCHOR_NORM**2
        anchors[tag] = {"success_probabilities":list(map(str, successes)),
                        "low_minus_high":str(signal)}
    level, contrast = bounds(RATE)
    assert level < MIN_SUCCESS / 10 and contrast < MIN_SIGNAL / 4
    calibrated_rate = F(16,1000)
    calibrated_level, _ = bounds(calibrated_rate)
    calibrated_contrast = calibrated_bounds(calibrated_rate)
    assert calibrated_level < MIN_SUCCESS/10 and calibrated_contrast < MIN_SIGNAL/4
    return {"calibrated_bound":{"joint_fraction":str(calibrated_rate),
                "assumed_rephased_N11_norm_difference_upper":"3/12500",
                "assumed_N11_four_bin_contrast_upper":"669/100000000",
                "level_TV_upper":str(calibrated_level),
                "contrast_half_L1_upper":str(calibrated_contrast)},
            "joint_amplitude_weight_fraction":str(RATE),
            "assumed_upper_reference_norm":str(ANCHOR_NORM),
            "assumed_lower_success":str(MIN_SUCCESS),
            "assumed_lower_absolute_density_signal":str(MIN_SIGNAL),
            "amplitude_norm_upper":str(AMPLITUDE),
            "rephased_density_pair_norm_difference_upper":str(DENSITY_DIFFERENCE),
            "level_TV_upper":str(level), "level_TV_allowed_at_least":str(MIN_SUCCESS / 10),
            "contrast_half_L1_upper":str(contrast), "contrast_allowed_at_least":str(MIN_SIGNAL / 4),
            "dyadic_grid_anchor_checks":anchors}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(run(), indent=2, sort_keys=True) + "\n")
