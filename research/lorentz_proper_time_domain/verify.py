"""Separate checks of source fixation, raw results, binomial tails and defects."""
import hashlib
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.stats import binom, binomtest
from domain import (embedding_audit, infer, order_count, probability_limits, validate_order)

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def structural_checks():
    results = []
    def expect(c, valid, reason=None):
        result = validate_order(c)
        require(result["valid"] == valid, str(result))
        if reason:
            require(result["reason"] == reason, str(result))
        results.append(result)
    chain = np.triu(np.ones((4, 4), dtype=bool), 1)
    expect(chain, True)
    expect(np.zeros((4, 4), dtype=bool), True)
    diagonal = chain.copy(); diagonal[1, 1] = True
    expect(diagonal, False, "SELF_RELATION")
    reciprocal = chain.copy(); reciprocal[1, 0] = True
    expect(reciprocal, False, "TWO_CYCLE")
    cycle = np.zeros((3, 3), dtype=bool); cycle[0, 1] = cycle[1, 2] = cycle[2, 0] = True
    expect(cycle, False, "DIRECTED_CYCLE")
    missing = chain.copy(); missing[0, 2] = False
    expect(missing, False, "MISSING_TRANSITIVE_RELATION")
    k, m = order_count(chain, [0, 3])
    require((k, m) == (2, 2), "strict endpoints excluded")
    perm = np.array([2, 0, 3, 1])
    marks = [int(np.flatnonzero(perm == old)[0]) for old in (0, 3)]
    require(order_count(chain[np.ix_(perm, perm)], marks) == (k, m), "relabel invariance")
    points = np.array([[0., -0.1], [0., 0.1]])
    wrong = np.array([[0, 1], [0, 0]])
    expect(wrong, True)
    require(not embedding_audit(wrong, points)["matches_known_embedding"], "false spacelike relation needs geometry")
    twins = np.array([[0, 0, 1], [0, 0, 1], [0, 0, 0]])
    expect(twins, True)
    return {"status": "PASS", "cases": results,
            "mark_exclusion": "PASS", "relabel_invariance": "PASS",
            "valid_poset_can_disagree_with_embedding": "DEMONSTRATED",
            "finite_profile_twins_are_not_continuum_violation": "DEMONSTRATED"}


def verify():
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE/"results"
    contract = json.loads((HERE/"contract.json").read_text())
    freeze = json.loads((output/"freeze.json").read_text())
    for name, digest in freeze["files_sha256"].items():
        require(hashlib.sha256((HERE/name).read_bytes()).hexdigest() == digest, f"source changed: {name}")
    structure = structural_checks()
    alpha = contract["alpha_interval"]
    max_tail_error = 0.0
    for m in (64, 256, 1024):
        lo, hi = probability_limits(m, alpha)
        k = np.arange(m+1)
        # Independently check beta quantiles by binomial-tail equations.
        errors = [np.max(abs(binom.sf(k[1:]-1, m, lo[1:])-alpha/2)),
                  np.max(abs(binom.cdf(k[:-1], m, hi[:-1])-alpha/2))]
        max_tail_error = max(max_tail_error, *map(float, errors))
        require(max(errors) < 2e-11, "binomial-tail inversion")
        require(abs(hi[0] - (1-(alpha/2)**(1/m))) < 2e-14, "K=0 analytic endpoint")
    require(abs(infer(16, 256, 4)["theta_hat"]-0.5) < 1e-15, "fourth root, not square root")
    summary = json.loads((output/"summary.json").read_text())
    counts = json.loads((output/"counts.json").read_text())
    raw = {r["cell"]: r["K"] for r in counts}
    require(len(raw) == len(counts) == len(summary["cells"]) == 24, "unique complete cells")
    compared = 0
    full_checks = 0
    for r in summary["cells"]:
        ks = raw[r["cell"]]
        m, d, theta = r["m"], r["d"], r["theta"]
        require(len(ks) == contract["replicates_per_cell"] and all(type(k) is int and 0 <= k <= m for k in ks), "raw K range/completeness")
        a = theta**d
        lo, hi = probability_limits(m, alpha)
        ncover = sum(lo[k] <= a <= hi[k] for k in ks)
        rmse = math.sqrt(math.fsum(((k/m)**(1/d)-theta)**2 for k in ks)/len(ks))
        bias = math.fsum((k/m)**(1/d)-theta for k in ks)/len(ks)
        require(ncover == r["coverage_count"] and abs(rmse-r["empirical_rmse"]) < 1e-12 and abs(bias-r["empirical_bias"]) < 1e-12, "raw estimate/coverage recomputation")
        # Separate scalar binomial sums (not the vectorized summary routine).
        probability = [float(binom.pmf(k, m, a)) for k in range(m+1)]
        coverage = math.fsum(probability[k] for k in range(m+1) if lo[k] <= a <= hi[k])
        theory_rmse = math.sqrt(math.fsum(probability[k]*((k/m)**(1/d)-theta)**2 for k in range(m+1)))
        require(abs(coverage-r["theory"]["coverage"]) < 1e-12 and abs(theory_rmse-r["theory"]["rmse"]) < 1e-12, "finite sum recomputation")
        require(coverage >= 0.95-1e-12, "conditional coverage")
        require(abs(float(binomtest(sum(ks), len(ks)*m, a).pvalue)-r["tests"]["interval_count_p"]) < 1e-12, "count test recomputation")
        passed = all(p >= r["bonferroni_threshold"] for p in r["tests"].values()) and r["near_boundary_backgrounds"] == 0
        require((r["implementation_check"] == "PASS") == passed, "gate consistency")
        compared += len(ks)
        if r["full_order_crosscheck"]:
            require(r["full_order_crosscheck"]["status"] == "PASS", "full-order crosscheck")
            full_checks += 1
    require(compared == summary["replicates_total"] == 49152 and full_checks == 12, "complete run")
    for r in summary["analytic_grid"]:
        require(r["coverage"] >= 0.95-1e-12 and abs(r["mass_sum"]-1) < 1e-12, "analytic grid coverage/mass")
    report = {"verification": "PASS", "sources_unchanged_since_local_freeze": True,
              "structural_checks": structure, "max_binomial_tail_error": max_tail_error,
              "recomputed_raw_replicates": compared, "full_order_crosschecks": full_checks,
              "scientific_status": summary["status"], "independent_external_replication": False}
    (output/"verification.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    verify()
