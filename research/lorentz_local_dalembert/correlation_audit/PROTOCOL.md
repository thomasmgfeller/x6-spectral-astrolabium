# Correlation diagnosis after the PR78 correction hold

SPDX-License-Identifier: Apache-2.0

## Status and scope

This is a **development-only** audit of all 128 archived PR78 attempts in flat
2+1 geometry at rho=32768. The 59 complete old calibration clouds and 55 complete
old test clouds are now development observations. The 14 abstentions remain in
the attempt accounting. No result here is a new independent statistical test,
and no correction is released by this protocol. The known PR78 failure motivated
this diagnosis; the present candidate grid and continuation gate are committed
before running these new interventions, not before the historical observations.

The frozen PR77 grouped/projected model, bias, PR78 canonical initialization,
constraints, trust region, optimizer and fallbacks remain unchanged. This
separates covariance correlations from marginal variances within one fixed
local correction algorithm. It does not separate all possible physical sources
of geometry error, prove global optimality, or qualify a 4D reconstruction.

## Fixed interventions

Let K be the frozen model's working residual covariance and D=diag(diag(K)).
Every candidate preserves all marginal variances:

1. Four fixed shrinkage values: K_lambda=D+lambda(K-D), lambda=0.1,0.25,0.5,0.75.
2. `within_groups`: keep only principal blocks for observed root, support
   spacelike and support causal pairs; set between-group entries to zero.
3. Replace one active correlated component C_k by its diagonal:
   K_new=K-C_k+diag(diag(C_k)). The five components are cross-group endpoint,
   support-spacelike endpoint, support-spacelike cloud, support-causal cloud,
   and signed common scale. The two fitted zero correlated components are
   checked as no-ops analytically, without redundant real-cloud solves.

Each component is positive semidefinite and the independent components have
strictly positive floors. Shrinkage is a convex combination of positive definite
matrices; block removal is a direct sum of positive definite principal blocks;
component replacement leaves positive floors and adds a nonnegative diagonal.
Consequently every candidate is positive definite. Numerical controls verify
this and preservation of the diagonal. K's condition number above 1e8 triggers
baseline fallback. Every failed local solve also remains as a baseline fallback
in the loss and fallback denominator. Bias-centred targets and solver settings
are identical across candidates. Predictions have no truth argument and are
sealed before truth-based evaluation.

Baseline, unweighted, diagonal and full references are reused from the archived
PR78 predictions; they are not eligible candidates for the continuation gate.
There are ten candidates and 114 complete clouds: 1140 new local solves, zero
new simulations. Four workers receive global indices w,w+4,... over old
calibration then old test. Each has a 1800-second wall and 2048-MiB RSS budget.
An incomplete worker means HOLD, not selective omission of its records.

## Fixed summaries and mechanistic checks

The primary squared loss gives equal total weight to each nonempty observed
pair group within a cloud, then equal weight to each complete cloud. RMSE is
the square root of that mean. Per-group RMSE, fallback and order counts are
also reported, separately in both historical blocks and pooled development.

For baseline error e=q_baseline-q_truth and step delta=q_candidate-q_baseline,
the exact identity is DeltaMSE=2<e,delta>_w+<delta,delta>_w. The cross term shows
error alignment; the positive step term shows movement cost. This is a loss
identity, not a claim that these terms are independent random errors.

Project delta onto q_baseline: a=<q,delta>_w/<q,q>_w. Report a and the fraction
a^2<q,q>_w/<delta,delta>_w (zero for negligible steps). Report the condition of
the candidate's covariance; baseline and unweighted use the identity convention
with condition 1. For full K, diagonalize R=K/(sd sd^T), sort eigenvalues, and
report mean squared bias-adjusted whitened residuals within the lowest quarter,
middle half and highest quarter of modes, then cloud summaries. These are
descriptive diagnostics; they do not create another threshold or release gate.

The signed scale component is v q q^T. Set K0=K-v q q^T and b=q^T K0^-1 q.
The rank-one inverse identity gives (q^T K^-1 q)/b=1/(1+v b). Verify numerically
before any common precision normalization. This proves attenuation in that
quadratic direction, not empirical harm by itself. Only intervention outcomes
can describe its effect on this fixed constrained local algorithm.

## Development continuation rule fixed before the audit

Each candidate must pass every condition in **both old blocks separately**:

- At least 48 complete clouds.
- RMSE/baseline <=0.99 (at least 1% practical improvement).
- RMSE/diagonal <=1.0.
- Each group RMSE/baseline <=1.05.
- Zero delivered order violations.
- At most 10% fallback among complete clouds.

If multiple candidates qualify, select the lowest pooled group-balanced RMSE;
absolute ties within 1e-12 follow the contract order. Also report the lowest
descriptive RMSE candidate even if none qualifies. Pooled performance cannot
rescue failure in one historical block. Reference variants cannot be promoted
post hoc. No bootstrap on these reused data is called independent evidence.

If none qualifies: `STOP_CORRELATION_CORRECTION_SCREEN`; stop this correction
family after the diagnostic report and numerical replay, with no fresh study.
If one qualifies: `PROCEED_TO_FRESH_CONFIRMATION` authorizes preparation only.
A separate subsequent source/model/seed freeze must specify a prospective
64-cloud calibration and 64-cloud independent test protocol before drawing
new data. This audit supplies no numerical claim about that unperformed study.

`HOLD_BATCH_CORRECTION`, `HOLD_EMBEDDING_COVARIANCE`, `HOLD_KALMAN`,
`HOLD_PHASE3`, and `METADATA_HOLD` remain. No covariance for embedding
coordinates, Kalman release, operator conclusion or radial 4D qualification
follows from this screen. Reconstruction and discretization error claims from
earlier studies are not revised by reusing their successor data here.

## Provenance and replay

`source_pins.json` hashes the inherited sources, model, archived observations,
and this contract/protocol/implementation. Its public commit precedes the new
diagnostic runs. `source_freeze.json` records that commit. Execution archives
contain all 128 attempts and prediction seals. Replay independently recomputes
1140 local solves, regenerates 114 truth point sets, verifies source ancestry,
hashes, loss identities, exact order, summaries and all continuation gates.
Optimizer comparisons are on invariant intervals (atol=rtol=2e-5), not arbitrary
coordinate gauges. Numerical replay validates reproducibility, not statistical
independence. The inherited selector and inference are archived rather than
rerun; this limitation is explicit.

Background: [Ledoit and Wolf (2004)](https://doi.org/10.1016/S0047-259X(03)00096-4)
motivates covariance shrinkage generally. This fixed diagonal-target grid is
not their optimal estimator and inherits no optimality guarantee. Linear
systems use the inherited Cholesky path documented by
[SciPy cho_solve](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.cho_solve.html).
