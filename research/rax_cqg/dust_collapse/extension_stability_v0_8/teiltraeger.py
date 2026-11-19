"""Extend the v0.7 pilot Gram matrices and rerun its supporting-plane certificate."""
from argparse import ArgumentParser
import json
from unittest.mock import patch
from basis import HERE, REFERENCE, full, layout
from uhrtest import MASKS
import certificate as previous
import matrices
from projections import overlap
from abel_check import numerical_state
import mpmath as mp
import numpy as np

def names_and_reach():
    names, reach = matrices.names_and_reach()
    ends = full.read(REFERENCE / "catalog.json")["roots"]
    for mask in MASKS:
        idx = len(names)
        for r, name in enumerate(("chain", "one")):
            if str(mask) in ends[name]["ends"]:
                reach[r].append(idx)
        names.append(f"N15_{mask}")
    return names, reach

def extend_gram(output):
    names, _ = names_and_reach()
    original = np.load(REFERENCE / "gram.npy")
    n = original.shape[1]
    mats = np.empty((3, len(names), len(names)), dtype=complex)
    mats[:, :n, :n] = original
    anchors = full.read(REFERENCE / "anchor_rows.json")
    errors = {}
    with mp.workdps(70), patch.object(matrices.geometry, "order", layout):
        states = []
        for j, name in enumerate(names):
            key = matrices.common.prior.key(name)
            status, state = matrices.geometry.kernel(key)
            if status["status"] != "ADMISSIBLE":
                raise ValueError(name)
            states.append(state)
            if j < n:
                continue
            prec, phase = numerical_state(key, mp.mpf("1e-28"))
            abel = float(max(max(abs(x) for x in prec - state[0]), abs(phase - state[1]/abs(state[1]))))
            for i, left in enumerate(states):
                bins = np.asarray(overlap(left, state))
                if i == j:
                    if abs(bins.sum() - 1) > 1e-14:
                        raise ValueError("Scalar normalization")
                    bins = bins.real
                mats[:, i, j] = bins
                mats[:, j, i] = bins.conj()
            frozen = np.array([[complex(*v) for v in row] for row in anchors[str(key[1])]])
            delta = float(np.max(abs(frozen - mats[:, [0, 1, j], j].T)))
            if delta > 1e-14 or abel > 1e-17:
                raise ArithmeticError((name, delta, abel))
            errors[name] = {"anchor_error": delta, "abel_error": abel}
    np.save(output, mats)
    return errors

def certify(gram_directory=HERE):
    clocks = {**full.read(REFERENCE / "clocks.json"),
              **{"N15_" + mask: row for mask, row in full.read(HERE / "uhren.json").items()}}
    def inputs(name):
        data = full.read(matrices.CACHE / "study" / name)
        return {**data, **clocks} if name == "direct.json" else data

    with patch.object(previous.positive, "HERE", gram_directory):
        residuals = previous.positive.verify()
    results = {}
    with patch.object(previous.exact, "jsonread", inputs), patch.object(previous.exact, "setup", names_and_reach), patch.object(previous.exact, "HERE", gram_directory):
        for tag in ("coarse", "fine"):
            results[tag] = {}
            for t in (previous.F(1,20), previous.F(5021,100000)):
                row = previous.exact.verify(tag, t)
                for key in ("evaluated_N14", "abs_bounded_N14"):
                    del row[key]
                results[tag][str(t)] = row
    return {"grids": results, "basis_count": len(names_and_reach()[0]), "N15_direct": len(clocks),
            "positive_congruence_residuals": residuals}

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(HERE / "teiltraeger.json"))
    args = parser.parse_args()
    checks = extend_gram(HERE / "gram.npy")
    results = certify()
    results["scalar_checks"] = checks
    from basis import save_json
    save_json(args.out, results)
