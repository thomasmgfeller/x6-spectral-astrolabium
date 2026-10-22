# Eigenzeit: operator bounds that retain joint count information

SPDX-License-Identifier: Apache-2.0

**22 October 2026 — all 19 bounds improve; full accuracy still not certified.**

This executes the next step after PR90: use joint difference constraints
inside the operator perturbation calculation, rather than project them back
onto separate marginal intervals. No new clouds, fits or physical assumptions
are introduced. The twentieth packet retains its prior count HOLD.

| Diagnostic | Outcome |
|---|---|
| Cases improved by joint information versus the same box-only transport method | **19 / 19** |
| Remaining contraction upper bound versus box-only transport | **19.28–36.92%** |
| Remaining contraction upper bound versus the original symmetric-box method | **14.60–29.06%** |
| Absolute contraction upper bounds | About **313,119 to 379,748,516**, versus the sufficient requirement **less than 1** |
| Full-set <=10% weight-error certificates | **0 / 19** |
| Inherited simultaneous coverage of the underlying confidence set | Greater than **97.7715%**, unchanged from PR90 |

These percentages describe improvement of a conservative **sufficient bound**.
They are not measured reconstruction error, success probability, necessary
sample-size factors, or a physical gain. Even the smallest bound remains far
above the contraction threshold. Gamma>=1 does not establish instability,
singularity, or impossibility. All scientific HOLDs remain.

## What changed mathematically

1. Transform each mean-difference constraint through q=const*mu^(2/3) using
   its analytic pairwise maximum, enclosed by directed rational arithmetic.
2. Bound each linear form in the intrinsic design and target by an exactly
   balanced, nonnegative transport flow on the difference graph. Summing its
   inequalities certifies an upper bound without trusting a floating optimizer.
3. Apply these joint bounds to the finite linear terms and explicit quadratic
   remainders, then use the existing resolvent/weight-error theorem.

[THEORY.md](THEORY.md) proves all three steps. The ablation retains the same
reference coordinates, exact row pivots and transport procedure in the
box-only and joint runs. It therefore distinguishes the additional value of
joint constraints from the benefit of retaining asymmetric marginal bounds.
No artificially shrunken region is given a coverage claim.

## Scientific implication

The joint conditions now demonstrably improve the operator certificate, but
this single global perturbation estimate remains too conservative to decide
accuracy. Further repetitions of the same estimator cannot resolve that proof
gap. The next discriminating task is to test the earlier witness geometries'
**actual intersection volumes**, with certified integration error, against the
joint count model. That checks whether the ambiguity survives the information
not captured by this outer relaxation. In parallel in a future task, a global
bound would need realizability/rank constraints or a controlled subdivision
of the admissible set, not merely additional optimizer starts.

The C3 field target from PR90 remains distinct. No radius bound over every
admissible geometry, physical field smoothness constant or nodal noise budget
has been manufactured; no continuum-field accuracy is claimed.

## Evidence and replay

[PROTOCOL.md](PROTOCOL.md), [contract.json](contract.json) and [freeze.json](freeze.json)
pin the computation and immediate inputs. This is a posthoc audit of known
archived data. An initial implementation attempt stopped at a domain assertion
before any case was written; the negative-difference extremizer was clamped
to its feasible left endpoint and the corrected code frozen before evaluation.
The mathematical rule and target were unchanged. The independent audit checks
40 endpoint-domain configurations, including capped negative differences.

All twenty records, [summary.json](summary.json), and [audit.json](audit.json)
are included. Four synthetic controls check the concave extremizer, exact flow
gain, zero form, and a feasible perturbation below its bound. Grid comparisons
are numerical sanity checks; the analytic proof and directed arithmetic carry
the guarantee. Every actual transport balance is checked exactly at runtime.

```sh
python -m pip install -r research/lorentz_local_dalembert/finite_poisson_bounds/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research/lorentz_local_dalembert/joint_operator_bounds/jb_run.py --verify
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research/lorentz_local_dalembert/joint_operator_bounds/jb_audit.py --verify
```

Python 3.12 and the prior pinned dependencies are used. [SHA256SUMS](SHA256SUMS)
inventories the package. Old experiments, data and scientific gates are unchanged.
