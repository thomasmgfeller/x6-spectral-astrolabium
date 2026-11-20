"""Recompute the paired endpoint contrasts and one-shot decision rate from PR 336."""
import csv
import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

STUDY = Path(__file__).resolve().parent / "studie"
sys.path.insert(0, str(STUDY))
from model import combined_laws, gram


def positive_probability(amplitudes, weights, metric):
    vectors = weights[:, None] * amplitudes
    norms = (vectors.conj() * (metric @ vectors)).sum(axis=0).real
    assert norms.sum() > 0
    return norms[3:].sum() / norms.sum()


def paired_differences(amplitudes, weights, alternative, metric):
    reference = positive_probability(amplitudes, weights[0], metric)
    return [float(100 * (positive_probability(amplitudes, q, metric) - reference))
            for q in (weights[1], alternative)]


def check_ensemble():
    keys, weights = combined_laws()
    chains = json.loads((STUDY / "chain.json").read_text())
    primary = chains["law"]
    other = chains["alternative_same_N13"]["law"]
    assert set(primary) == set(other)
    change = {key: Fraction(other[key]) - Fraction(primary[key]) for key in primary}
    assert sum(change.values()) == 0
    increases = sum(x > 0 for x in change.values())
    decreases = sum(x < 0 for x in change.values())
    assert (len(change), increases, decreases) == (206, 25, 21)
    alternative = weights[0] + np.array([float(change.get(str(key), 0) / 2) for key in keys])
    with np.load(STUDY / "scalars.npz") as scalar:
        idx = np.searchsorted(scalar["keys"], keys)
        assert np.array_equal(scalar["keys"][idx], keys)
        metric = gram(list(zip(scalar["precision"][idx], scalar["factor"][idx])))
    result = {}
    with np.load(STUDY / "combined_raw.npz") as raw:
        assert list(raw["keys"]) == keys
        result["seeds"] = raw["seeds"].tolist()
        for j, size in enumerate(raw["sizes"]):
            samples = raw["amp"][:, j, 0, 0]  # M = 1/4 and r = 1/8
            result[str(size)] = {
                "pooled_amplitudes": paired_differences(samples.mean(axis=0), weights,
                                                        alternative, metric),
                "individual_scrambles": [paired_differences(a, weights, alternative, metric)
                                         for a in samples],
            }
    with (STUDY / "distribution.csv").open(newline="") as stream:
        rows = [r for r in csv.DictReader(stream) if r["chain_extension"] == "primary"
                and r["initial_density_center"] == "0.125" and r["one_edge_A_over_B"] == "1:1"]
    assert {r["tagged_M"] for r in rows} == {"0.25", "1", "4"} and len(rows) == 3
    bins = ["p_lt_minus1", "minus1_le_p_lt_minus0.25", "minus0.25_le_p_lt0",
            "0_lt_p_lt_0.25", "0.25_le_p_lt_1", "p_ge_1"]
    for row in rows:
        assert abs(sum(float(row[b]) for b in bins) - 1) < 1e-12
    result["one_shot_accuracy_equal_priors"] = sum(max(float(r[b]) for r in rows)
                                                   for b in bins) / 3
    result["chain_weight_changes"] = {"increased": increases, "decreased": decreases}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    check_ensemble()
