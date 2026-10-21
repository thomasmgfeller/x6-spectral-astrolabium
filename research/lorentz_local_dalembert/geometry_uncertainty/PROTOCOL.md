# Geometry uncertainty: invariant predictive sets

This prospective successor to PR75 calibrates uncertainty in geometry itself in
the existing flat 2+1, rho=32768 experiment. It does not transfer the result to
the radial 4D experiment. No scalar-field observations enter this study.

## Targets and inference boundary

For the guarded selected root and support, let s be the already inferred scale.
For every unordered pair define q_ij = (-(t_i-t_j)^2 + (x_i-x_j)^2 +
(y_i-y_j)^2)/s^2. These are signed squared intervals, not proper times. A
Lorentz transformation leaves them unchanged. The root Gram entries follow as
G_ij=(q_0i+q_0j-q_ij)/2, with G_ii=q_0i. Original and relation-projected
reconstructions are both covered by one simultaneous, per-cloud score.

Only reconstructed features, observed order, inferred scale and a frozen model
enter predictions. Predictions are sealed before regenerating true coordinates.
The existing full selection, audit and projection pipeline is retained. A failed
guard is an abstention, retained in the record and never replaced. Coverage is
claimed only for this pipeline's COMPLETE population, not for abstentions.

## Development model, fixed before new observations

Reuse the 58 COMPLETE clouds from PR74's 64 archived calibration/test attempts
as explicitly labelled development data. Each cloud receives equal total weight.
Fit each arm's interval bias e=q_hat-q_true by least squares on
X=[1,q_hat,indicator(pair touches root)]. Report the bias separately; the
predictive centre is q_hat-X beta. This is not a corrected realizable embedding.

Let D_aa=sqrt(1+q_hat_a^2). Let A be unordered-pair endpoint incidence with each
of the two entries 1/sqrt(2). Use the positive definite working covariance

    K = D [v_ind I + v_endpoint A A^T + v_cloud 11^T] D.

The endpoint term represents shared-point dependence; the common cloud term is
a deliberately limited proxy for shared reconstruction/landmark uncertainty.
It does not identify separate landmark perturbations or a coordinate posterior.
Fit the three nonnegative components by cloud-balanced Frobenius moment matching
of standardized residual outer products, with v_ind >= 1e-8. Mean fitting and
variance fitting use the same development data; subsequent independent conformal
calibration absorbs prediction error without assuming Gaussian geometry errors.

Propagate K linearly to every root Gram entry and to seven observable block
means: all pairs, root pairs, support pairs, causal pairs, spacelike pairs,
near pairs (abs(q_hat)<=1) and far pairs. Causal labels come from observed order.
Skip only empty blocks; report their actual cloud counts. The Gram covariance
uses all cross terms. No independence of pairs, Gram entries or arms is assumed
in the joint score. No cross-arm covariance matrix is estimated.

## Prospective sampling and two public freezes

Draw 32 calibration and 32 test seeds independently with replacement from the
32-bit seed population excluding every historical seed in PR74's schedule and
its historical exclusions. Preserve duplicate newly drawn seeds if any. Publish
source, exact development model, seed schedule and source pins before running a
new cloud. Four workers per phase, fixed 1800 seconds and 2048 MiB RSS per worker;
save every outcome. A resource or execution failure forces HOLD, without retries
or replacement observations in this protocol.

On each accepted calibration cloud, the score is the maximum absolute residual
divided by predicted standard deviation across BOTH arms, ALL intervals, ALL
root Gram entries and ALL nonempty block means. Let n be the number accepted,
k=ceil((n+1)*0.95); q is the kth smallest cloud score. If n<24 or k>n, HOLD.
Publish this scalar calibration and the source-freeze certificate before any
test cloud is generated. Freeze again; never refit from test outcomes.

All predictive intervals are centre +/- q*standard_deviation. Under independent
exchangeable clouds from the fixed eligible seed population and the fixed
truth-free acceptance rule, this provides at least k/(n+1) marginal simultaneous
coverage for a new accepted cloud, averaged over calibration and test draws.
It is not conditional coverage for each order, fixed calibration realization,
support size, or geometry. Finite seed simulation, known sprinkling law and fixed
physical scale remain assumptions. This is predictive calibration, not a
confidence interval for estimated model parameters.

## Locked evaluation and interpretation

Report all attempts, acceptance, simultaneous and family-specific coverage,
exact two-sided 95% Clopper-Pearson interval for test-cloud joint coverage,
widths in normalized signed-square units (and physical s^2 units), raw/bias-
adjusted error, covariance components, condition numbers, and standardized block
means and second moments. The effective replication count is CLOUDS, never pairs.
Report coverage by support count and reconstructed design condition using
development medians as fixed cutpoints; report out-of-development-range clouds.
These small subgroups are descriptive, not conditional-coverage certificates.

For each arm, screen the uninflated working covariance against fixed tolerances:
absolute standardized block mean <=0.5 and second moment in [0.5,2], plus
cloud-balanced pointwise standardized second moment in [0.5,2]. Empty blocks
are disclosed. Failure means WORKING_COVARIANCE_SCREEN_FAILED. Passing is only a
screen, not statistical identification of a conditional covariance. Conformal
coverage cannot rescue a covariance-shape claim. Also report the variance ratio
for each block under K versus diagonal(K), to expose shared-error effects.

Minimum 24 accepted calibration and test clouds, valid source chronology and
numerical replay permit INVARIANT_CALIBRATION_COMPLETED. Coverage itself is
reported as observed; there is no post-hoc success threshold or model search.
HOLD_EMBEDDING_COVARIANCE, HOLD_PHASE3 and historical METADATA_HOLD remain. No
covariance-weighted projection, Kalman step, new density or dimension is enabled.

## Verification

Replay archived inference inputs, truth targets, model fit, calibration, scores,
summary and all record hashes without rerunning selection. Verify public commit
ancestry and frozen-file contents. Numeric float equality uses atol=1e-8,
rtol=1e-7; regenerated floating-point byte hashes are diagnostic only. Controls
cover Lorentz invariance, scale normalization, exact Gram transformation and
cross-covariance, positive definiteness, endpoint dependence versus a diagonal
negative control, bias/zero-error fixtures, conformal rank and no-truth inference.

Method: Lei et al., *Distribution-Free Predictive Inference for Regression*,
JASA 2018, https://www.stat.cmu.edu/~ryantibs/papers/conformal.pdf . The score is
cloud-level and vector-valued targets are handled by the single maximum score.
