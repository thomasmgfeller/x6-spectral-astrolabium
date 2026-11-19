"""Independent four-outcome check for the four new pure daughter choices at 5%."""
from basis import HERE, REFERENCE, full
from teiltraeger import names_and_reach
from uhrtest import MASKS
from fractions import Fraction
import numpy as np

def calculate():
    names, reach = names_and_reach()
    grams = np.load(HERE / "gram.npy")
    bound_data = full.read(HERE / "volltraeger.json")["second"]
    clocks = full.read(HERE / "uhren.json")
    detail = {}
    for tag in ("coarse", "fine"):
        full_names, _, _, _, known, _, _ = full.inputs(tag)
        parent = np.array([[complex(*z) / 2 for z in state] for state in known[:2]])
        detail[tag] = {}
        for mask in MASKS:
            name = f"N15_{mask}"
            j = names.index(name)
            if not all(j in group for group in reach) or name not in full_names:
                raise ValueError(name)
            effects = grams[:, [0, 1, j]][:, :, [0, 1, j]]
            amps = [complex(*v) for v in clocks[str(mask)]["rows"][tag]]
            distributions, references = [], []
            def probabilities(state):
                accepted = np.einsum("i,kij,j->k", state.conj(), effects, state)
                if np.max(abs(accepted.imag)) > 1e-15:
                    raise ArithmeticError("Non-real readout")
                return np.r_[accepted.real, 1 - sum(accepted.real)]
            for d in (0, 1):
                b = np.r_[parent[:, d], 0j]
                x = .95 * b
                x[-1] = .05 * amps[d]
                references.append(probabilities(b))
                distributions.append(probabilities(x))
            refs, obs = np.array(references), np.array(distributions)
            baseline_success = refs[:, :3].sum(axis=1)
            levels = .5 * abs(obs - refs).sum(axis=1) / baseline_success
            density_ref = refs[1] - refs[0]
            change = obs[1] - obs[0] - density_ref
            contrast = abs(change).sum() / abs(density_ref).sum()
            success_diff = sum(obs[1,:3] - obs[0,:3])
            if not (max(levels) <= .1 and contrast <= .25 and success_diff < 0):
                raise ArithmeticError((tag, name, levels, contrast, success_diff))
            detail[tag][str(mask)] = {"relative_level_change": levels.tolist(),
                                      "relative_contrast_change": float(contrast),
                                      "success_difference": float(success_diff)}
        # Check the identification of the active lower polynomial at the last
        # certified point directly from the stored rational success projection.
        constants = bound_data["proof_constants"][tag][-1]
        p, lower = map(Fraction, (constants["p"][1], constants["lo"][1]))
        for key in ("bound_fraction", "next_fraction_not_certified_by_this_bound"):
            t = Fraction(bound_data[key])
            level = 1 - ((1-t)**2*p + 2*t*(1-t)*lower)/p
            reported = Fraction(bound_data["metrics"][tag][str(t)][1])
            if level != reported:
                raise ArithmeticError("Active success loss differs from certificate")
    return detail

if __name__ == "__main__":
    from basis import save_json
    save_json(HERE / "einzeltests.json", calculate())
