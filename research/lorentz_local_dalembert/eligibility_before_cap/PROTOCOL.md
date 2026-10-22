# Eligibility before cap: frozen paired fresh-cloud pilot

SPDX-License-Identifier: Apache-2.0

## Hypothesis and fixed intervention

PR #86 diagnosed the early candidate cap on 32 previously used A clouds:
19 old selections and nine additional geometrically feasible configurations.
That result motivated this intervention and is development evidence only.
The GLS candidate from PR #86 remains stopped; its failed gate is not retuned.

The only selection policy change is stable count/comparability filtering before
the cap of 128 candidates per common past/future cone. Inherited root, supports,
first three landmarks, marks, scale, hidden-colour base audit, full-count 16 and
half-count 4 thresholds, Gram condition <=1000, moment rank nine and condition
<=100000, and the final minimum-Gram-condition ranking are unchanged. Selection
uses A alone. Simulation coordinates are confined to simulation and post-seal
evaluation. Full cone scans increase eligibility work; the cap still limits
geometry evaluations. Exhausting this fixed family says nothing about other
roots, support sets or first-three-landmark choices.

Historical frozen modules are immutable. `selector.py` is the corrected version
used by this new campaign; the old implementation is the paired comparator.

## General availability argument

Let P=(p1,...,pn) be one mark-ordered cone after fixed-node/probe exclusion, E the
deterministic comparability/count-eligibility predicate, and k the fixed cap.
The old geometry input is E(P[:k]); the new input is E(P)[:k]. For every old
eligible point pi, i<=k, and its rank within E(P) is at most i. Thus it belongs
to the new input. Identical geometry gates preserve this subset relation.
The union of the two cone inputs also preserves it. Therefore an old accepted
frame cannot disappear and the minimum accepted Gram condition cannot rise.

The selected landmark can change. This argument does NOT imply monotonicity of
B count validity, inferred causal order, operator accuracy, variance, or cost.
It assumes the same ordering, exact eligibility decisions and deterministic
geometry calculations. Ties retain the old stable mark order; unique marks in
the actual experiment are not substituted for geometric information.

## Prospective data and boundary

Before generating any campaign A or B cloud, freeze code, contract, controls,
this protocol and all imported source/configuration dependencies with SHA-256
and UTC timestamp. This is a local freeze, NOT a public preregistration or
external timestamp attestation. Contract/analysis thresholds are fixed now.

- 32 new A seeds 202610220600 through 202610220631, known density 32768,
  flat 2+1 Minkowski, inherited outer diamond duration 1.5.
- Both selectors see exactly the same A and same frozen base selection.
- For every available arm, B0 is primary; B1..B8 measure conditional variance.
  B seed tag 782081 is new. Paired arms use identical B points and retain their
  different interval masks; coordinate hashes must agree for each pair.
- No seed replacements, retries, tuning, alternate frames chosen after seeing
  B, or dropping outliers. A/B failure records remain in the denominator 32.
- Unchanged direct four-landmark inference, full overlap matrices and delta
  covariance. No new Poisson or GLS estimator. Causal-order consistency is
  checked on all selected landmarks/root/supports, including uncounted pairs.
- Inference results are saved and SHA-bound before writing separate truth
  records. The analysis reads truth only after those seals are complete.

The four analytic sine/cosine fields, field noise sigma .001 and all numerical
thresholds are inherited or declared explicitly in `contract.json`. Fields
never enter selection or inference. Primary RMSE averages squared errors over
the four fields on common computable B0 cases, then takes the square root.
Noise variance is sigma^2 ||w||^2, averaged over the same cases. B1..B8 sample
variance (ddof=1) averages across fields and complete paired configurations.
All-available and qualified-subset errors are separately descriptive because
their subsets differ. No unavailable output is imputed as zero error.

## Two decisions

Selection support requires completion of all 32 attempts, >=26 new selections,
no lost old selections, >=6 rescued configurations, one-sided exact paired
discordance tail <=.05, median new selector time <=2 seconds and maximum <=5.
For g gains and l losses, p=sum(comb(g+l,k), k=g..g+l)/2^(g+l). This is the
single declared paired availability test for this pilot, not an adjustment for
the larger sequence of research trials or a general population theorem.

Operator support additionally requires >=26/32 qualified primary new systems,
>=16 common computable B0 pairs, paired RMSE ratio <=1, noise ratio <=1.25,
>=16 complete paired B1..B8 groups, and repeat variance ratio <=1.25. Candidate
covariance calibration needs >=16 groups with computable B0 and complete
B1..B8; ratio of their mean empirical response variance to mean B0 delta
prediction must lie in [.5,2]. This rough variance check is not interval coverage.

Every threshold must pass within its scope. A selection PASS with operator
HOLD permits only the bounded selection finding; no accuracy claim. Either
result retains HOLD_PHASE3, HOLD_EMBEDDING_COVARIANCE and METADATA_HOLD. No
curved/3+1, physical sensor, Kalman or uncertainty-coverage qualification.

## Budget and verification

Two ordinary worker processes, 16 configurations each, fixed 1800 seconds and
3000 MiB peak limit per worker, one BLAS thread. No autonomous agents involved.
Point budgets are inherited. Timeouts, execution errors or exceeded budgets
are HOLD with checkpoints; do not extend budget after inspecting outcomes.

Before freeze: finite exhaustive prefix-subset control, exact synthetic
early-cap counterexample, full/half-count negatives, moment-condition negative,
missing-base HOLD, and node relabeling with preserved marks.

After run: verify freezes, complete candidate inventories and old-candidate
inclusion; independently recalculate accepted Gram/moment systems from stored
counts; validate overlap matrices, moment/weight equations and causal order;
replay first/last A and B0 against unchanged original simulation. Such checks
are internal numerical audits, not an external Sage/Wolfram replication or
proof of statistical consistency. Do not change frozen code to force a PASS.
