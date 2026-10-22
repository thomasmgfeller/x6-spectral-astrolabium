# Frozen bounded joint raw-count development test

Date: 2026-10-22. This is a local freeze, not public preregistration.
The previous archive and its causal-order diagnosis are known development data.
The separate 32-selection campaign uses previously ungenerated seeds. No
replacement selections, optimizer restarts or adaptive thresholds are allowed.

## Candidate and distinction from rejected V1

All four landmarks, root and support nodes move jointly in a flat 2+1 Minkowski
embedding. Fix translation at landmark 0, boost landmark 1 onto the time axis,
and rotate landmark 2 onto the first spatial axis. Initial coordinates use the
unchanged four-landmark inversion. Invalid initial signature, insufficient
counts or coordinate budget exhaustion cause abstention, not hidden repair.

For every counted interval used by the old four-landmark estimator, let
q = -(z_b-z_a)^T eta (z_b-z_a), in the inherited scale s. The raw forward mean is
lambda = rho*(pi/12)*s^3*q^(3/2). Minimize the mean marginal Poisson deviance
2*mean(lambda-N+N*log(N/lambda)). The scalar N^(2/3) transform is used only for
initialization, not as the loss target. This avoids fitting a biased transformed
mean; it does NOT prove an unbiased final nonlinear constrained estimate.

Overlapping counts are dependent. This is a COMPOSITE objective, not a joint
independent-Poisson likelihood, and its optimum/Hessian supplies no calibrated
uncertainty. Original overlap matrices are retained. New count-cloud repetitions
preserve actual correlations and provide a conditional empirical comparison.

All unordered pairs must match the complete observed causal order: timelike
pairs have squared interval <= -1e-8 and correct time direction with dt >=1e-8;
unrelated pairs have squared interval >=1e-8. Exact null pairs are outside this
finite positive-margin candidate. There is one SLSQP start, 250 iterations,
ftol 1e-9, 20-second callback budget, canonical coordinate bounds +/-100.
Solver success, feasibility, independent strict directed-order reconstruction,
and the inherited Gram/moment/KKT gates are all required. No global optimality
claim. See contract.json for all numbers.

This differs from rejected V1: no fixed three-landmark metric, no diagonal
distance-correction objective, joint four-landmark movement, and all directed
orders including landmarks. V1's rejection remains in force. The new method
still belongs to constrained geometric estimation and must demonstrate utility.

## Execution and separation

1. Synthetic controls: exact-mean oracle recovery, independent differences of
   objective and all constraints, time reversal negative control, minimum-count
   hold, input-mask equivalence, gauge preservation and node relabeling.
2. Freeze code, protocol, contract, controls and inherited source hashes. Replay
   all 32 old attempts with their 18 available B0 configurations descriptively.
   Do not tune from this replay. Run all 32 fresh A selections with unchanged
   selection policy and nine independent B replicates per successful A.
3. Seal inference records before exporting simulator truth. Evaluate B0
   operator RMSE, linear response, signed interval RMSE, availability, iid field
   noise cost and execution cost; B1-B8 conditional variance separately.

The primary comparison is new fit versus old four inversion on their common
valid B0 cases, even when the old inversion failed order. This is a conditional
diagnostic comparison, NOT a deployable qualified-baseline comparison. Report
the both-qualified subset separately and all failures in the full denominator.
All original three-baseline weights are also retained in the records.

The fixed engineering gates require >=26/32 qualified B0 fits and common cases,
RMSE and linear-response ratios <=0.9, mean iid field-noise variance ratio <=1.25,
median fit <=5s, maximum <=20.5s, >=16 complete B1-B8 comparison groups and their
mean response variance ratio <=1.25. Every gate is necessary. A PASS is only a
development signal. Missing/failed records or budget exhaustion cause HOLD.

Enforced order is input consistency and cannot be counted as independent
validation. Four analytic fields and repeated B clouds are not independent A
samples. Cluster bootstrap resamples common A cases; it is descriptive for this
small selected sample and does not establish population or coverage guarantees.

HOLD_PHASE3, HOLD_EMBEDDING_COVARIANCE, METADATA_HOLD remain regardless of the
outcome. No curved/3+1, Kalman, physical sensor or exact joint likelihood claim.

SLSQP interface reference: https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html
Actual package versions and code hashes are recorded by the runner and freeze.

SPDX-License-Identifier: Apache-2.0
