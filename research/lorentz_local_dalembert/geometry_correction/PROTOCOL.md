# Does the grouped uncertainty improve a realizable geometry?

## Fixed scope and evidence boundary

PR77 passed a pilot for invariant prediction-error shapes. That does not identify
a conditional coordinate covariance or justify a Kalman update. This successor
tests the narrower operational question: does using the FULL working matrix in
a constrained offline batch correction reduce invariant reconstruction error?
The simulator, selection and relation projection remain unchanged, flat 2+1,
rho=32768. The grouped/projected model from PR77 is reused byte-for-byte, without
refitting. All historical observations, including PR77 tests, are now available
for development only. They are not new validation observations.

The four fixed variants are BASELINE (relation-projected reconstruction),
UNWEIGHTED, DIAGONAL and FULL. The last three share precisely the same grouped
bias-adjusted target c=q_hat-b_hat. They differ only in the objective precision:
I, diag(K)^(-1), or K^(-1). FULL is primary before seeing any new cloud. The
unconstrained bias centre is reported as a diagnostic; it need not be an embedding.
The corrected variants do not combine independent measurements or double-count
the two historical reconstruction arms. Only the projected arm is used here.

## Geometry, gauge and solver

Root translation is fixed at zero. Construct G=X diag(-1,1,1) X' from the observed
projected features and use its one negative and two positive eigenmodes to choose
a canonical Lorentz gauge. Orient time using the observed causal relations.
Require reconstructed intervals to agree with the input, signature nondegeneracy,
and the exact observed order. The canonical frame is an algorithmic convention,
not an identified physical orientation. Spatial signs/rotations do not change
the objective or the Euclidean trust ball. No true coordinates enter this step.

Minimize (q(X)-c)' W (q(X)-c)/(2m), with W normalized to mean diagonal one for
numerical scaling. Compute full precision by Cholesky solves, not an independence
approximation. Supply the exact interval Jacobian. Use SLSQP with maxiter=300 and
ftol=1e-11, starting from the canonical baseline, with no randomized restarts.
The quartic objective is nonconvex: success is not a global optimality proof.

Constraints reuse the previously audited convex inner region: future cones for
related pairs and fixed spatial separating planes for incomparable pairs. Set
the positive margin to min(1e-4, half the initial minimum cone/separator slack),
so the baseline is feasible. A trust ball limits coordinate displacement to
25% of the canonical baseline norm. This inner region can exclude otherwise
valid embeddings. This experiment tests that specific local algorithm.

Accept only finite solver-success candidates, objective no larger than baseline
(absolute allowance 1e-12), constraint slack >=-1e-8, relative shift <=.25+1e-8,
and an independent strict squared-interval/order predicate with zero missing or
extra relations. Covariance condition above 1e8 or a degenerate canonical frame
causes fallback. Every unsuccessful solve returns the baseline and remains in
every error/coverage denominator; fallbacks are separately counted. Unexpected
execution exceptions or resource failures force a study HOLD, not replacement.

## Separate recalibration and new test

Draw 64 calibration and 64 test seeds independently with replacement from the
32-bit seed population excluding all historical/sentinel seeds through PR77.
Keep repeated new draws. Publish source, model pins, criteria and seeds before
any new simulation; publish calibration observations and frozen radii before any
test simulation. No test-dependent tuning, candidate choice or seed replacement.
Four workers per phase, fixed 2400 seconds and 2048 MiB peak RSS each.

Predictions are sealed before true support coordinates are regenerated. The
truth-free inherited acceptance guard determines the common evaluated cloud set.
Every attempted cloud is archived, including abstentions and solver fallbacks.

Correction changes prediction centres. Therefore recalibrate all four variants
separately, using the SAME new calibration clouds and the PR77 K only as a working
residual scaling. It is NOT the propagated covariance of corrected coordinates.
For each variant use the maximum standardized absolute residual across every
interval, root Gram entry and nonempty observed block mean in the projected arm.
Include all K cross terms when scaling Gram entries and blocks. Use rank
ceil(.95*(n+1)); require n>=48 and a finite rank <=n. This gives the usual marginal
split-conformal bound per fixed variant under exchangeability and the fixed
acceptance rule. It is not a conditional guarantee for a particular order or a
joint guarantee across all variants. Fallbacks are part of the fixed predictor.

## Locked comparison and gates

Primary loss: squared interval error, equally weighted across each nonempty
observed group within a cloud (root, support spacelike, support causal), then
equally across complete clouds. Report square roots of mean losses. No pair is
treated as an independent replicate. Report unweighted interval RMSE, every
group RMSE, order violations, fallback counts, iterations, covariance conditioning,
simultaneous/family coverage with exact binomial intervals and band halfwidths.

Use 4000 paired whole-cloud bootstrap draws, seed 78261021, for FULL/comparator
RMSE ratios versus BASELINE, DIAGONAL and UNWEIGHTED. These percentile 95%
intervals are approximate pilot evidence, not an exact or multiplicity-adjusted
population certification. All variants and all failures are reported.

BATCH_CORRECTION_PILOT_SUPPORTED requires every gate:

- At least 48 complete clouds in each phase; all executions within budgets.
- Every delivered embedding preserves the exact observed order in both phases.
- FULL fallback rate <=10% in each phase.
- FULL observed simultaneous test coverage >=95%.
- FULL/BASELINE primary RMSE <=0.99 (at least 1% practical improvement).
- Paired bootstrap upper endpoint <1 versus BASELINE AND versus DIAGONAL.
- Each FULL group RMSE <=1.05 times its BASELINE counterpart.

Otherwise HOLD_BATCH_CORRECTION. A failed FULL gate cannot be rescued by selecting
UNWEIGHTED or DIAGONAL after the test. HOLD_EMBEDDING_COVARIANCE, HOLD_KALMAN,
HOLD_PHASE3 and METADATA_HOLD remain in all cases. No downstream operator/noise
improvement, online filtering, curved geometry or radial 4D result is asserted.

## Independent numerical controls and replay

Controls include analytic-vs-finite-difference interval Jacobians and objective
gradients, Cholesky quadratic forms versus direct solves, exact zero-residual
fixed points, known feasible scale correction, Lorentz/translation invariance
of canonical intervals, node-permutation invariance, correlated-versus-diagonal
negative control, strict-order rejection, group weights, and decision gates
that reject equal/worse candidates and individual broken requirements.

Replay verifies pins and public ancestry, seed exclusions, all 128 record hashes,
prediction seals, source and calibration execution commits, regenerated truth,
fresh optimization on archived inference inputs, stored-coordinate causality,
all evaluation/calibration/bootstrap decisions and resource limits. It does not
regenerate selection/inference. Compare optimizer-produced invariant centres at
atol=rtol=2e-5 across numerical platforms; iteration counts and coordinate gauges
need not be byte-identical. Other numeric checks use atol=1e-7, rtol=1e-6.
Coordinate byte hashes are diagnostic only. An optimizer-status disagreement or
an invariant difference outside tolerance fails replay and requires disclosure.

Method references: [SciPy SLSQP](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html),
[Cholesky](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.cholesky.html),
and [Lei et al., JASA 2018, section 2.2](https://www.stat.cmu.edu/~ryantibs/papers/conformal.pdf).
The model, practical thresholds and comparison here are prospective hypotheses.
