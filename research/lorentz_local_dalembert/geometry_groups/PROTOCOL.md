# Separate root and spacelike support errors: prospective paired study

## Motivation and scope

PR76 reported 26/29 jointly covered test clouds, an underdispersed standardized
root block (second moment 0.418), and three largest misses on spacelike
support-support intervals. Those observations motivate this successor. All PR74
and PR76 observations are now DEVELOPMENT data, including their old test sets:
128 attempts, 117 complete clouds. No independent result is claimed on them.

The simulator, selection, guards, inferred physical scale and reconstruction
remain unchanged: flat 2+1 Minkowski, rho=32768. The primary candidate is GROUPED;
POOLED is a matched refitted comparator, not the historical PR76 frozen model.
Both receive exactly the same development, calibration and test clouds.
All prior scientific holds remain, regardless of this pilot's outcome.

## Exhaustive observed groups

For each unordered pair among the selected root and support, use observed order
and root identity to assign exactly one group:

1. ROOT: either endpoint is the root, irrespective of causal label.
2. SUPPORT_SPACELIKE: neither endpoint is root and neither order direction holds.
3. SUPPORT_CAUSAL: the remaining support pairs with an observed causal relation.

Group labels never use hidden coordinates or the signs of estimated intervals.
The third group preserves complete coverage; it is not discarded. The focus
groups are ROOT and SUPPORT_SPACELIKE. Both original and relation-projected
reconstructions are evaluated, with one joint score per model and cloud.

The targets are q_ij = (−dt²+dx²+dy²)/s² and root Gram entries
G_ij=(q_0i+q_0j−q_ij)/2, G_ii=q_0i. Their centres and uncertainties are not an
embedding, and need not be jointly realizable as point coordinates.

## Bias and training weights

Each cloud has total weight one; each nonempty group within it has equal total
weight. POOLED bias uses [1,q_hat,root_indicator], GROUPED uses separate
[1,q_hat] coefficients in each of the three groups. Fit a ridge-stabilized least
squares system, with penalty 1e-8 * trace(X'WX)/dimension.

Choose one bias shrinkage factor per model and reconstruction arm from
[0,.25,.5,.75,1] by leave-one-WHOLE-cloud-out development risk, using the same
group-balanced squared loss. Break ties within 1e-12*max(1,min_risk) in favour of
the smallest factor. Refit coefficients on all development clouds. This finite
selection is entirely internal to development; new calibration/test clouds do
not choose the correction, the groups, the basis or any hyperparameter.

## Positive definite structured uncertainty

Let D_aa=sqrt(1+q_hat,a²), A be pair-endpoint incidence with two 1/sqrt(2)
entries per row, P=A A', and m_g be each group indicator vector. All working
matrices have K=D(sum v_k B_k)D, v_k>=0. Independent components have floor 1e-8.

POOLED uses the three PR76 forms I, P, 11'. GROUPED uses ten forms:

- Three group independent matrices diag(m_g).
- One common endpoint matrix P, retaining correlations ACROSS groups.
- Two group-specific endpoint matrices diag(m_g) P diag(m_g) for support
  spacelike and support causal pairs.
- Three group cloud matrices m_g m_g'.
- One common signed-scale matrix u u', where u=q_hat/D.

The last term becomes q_hat q_hat' in physical normalized interval coordinates,
allowing negative covariance between opposite-sign intervals while remaining
positive semidefinite. Omitting the root-only endpoint kernel avoids exact
redundancy: it equals (diag(m_root)+m_root m_root')/2.

Fit nonnegative variance coefficients by Frobenius moment matching of the
post-shrinkage standardized error outer product. For cloud c, with per-pair
fitting weights w, transform every basis and target by sqrt(w) on both axes.
This gives equal total weight to every nonempty group-pair block and equal
weight to clouds. Normalize the component Gram system before NNLS. Both models
use the same weighting. This is a WORKING prediction-error second-moment shape;
mean error is assessed separately. It is not an identified conditional covariance
of coordinates, nor a posterior for a particular observed order. The comparator
does not isolate grouping alone: the grouped package also adds a signed scale
mode and group-dependent bias/correlation structure.

## Joint calibration targets

Propagate K with all cross terms to every root Gram entry and to the seven
previous observable block means (all, root, support, causal, spacelike, near,
far; near means abs(q_hat)<=1), plus SUPPORT_SPACELIKE and SUPPORT_CAUSAL means.
The root group mean is already the root block. Empty blocks are omitted and
their counts disclosed. No pair, block, Gram entry or reconstruction arm is
treated as an independent replicate.

For each model, the score is the largest absolute standardized residual across
both arms, all intervals, Gram entries and nonempty block means. With n accepted
calibration clouds, choose rank k=ceil((n+1)*.95) and the kth score. At least 48
accepted clouds and finite k<=n are required. Each model receives its own radius
on the SAME calibration sample; intervals are centre +/- radius*predicted_sd.

Under independent exchangeable cloud draws and the fixed truth-free guard,
coverage is at least k/(n+1), marginal over calibration and a new accepted cloud,
for EACH model separately. There is no joint 95% claim across the two models,
no conditional guarantee for every order or subgroup, and no coverage claim for
abstentions. The primary model is fixed in advance, avoiding test-based selection.

## Data isolation and budgets

Draw 64 new calibration seeds and 64 new test seeds independently with replacement
from the 32-bit population excluding every historical seed through PR76 (259
exclusions including sentinel seeds). Keep any repeated new draw rather than
resampling. Publish exact source, model, seed schedule and file pins before
generating a new cloud. Publish calibration records and both frozen radii before
generating any test cloud. Source ancestry must survive a merge commit.

Four workers, 16 attempts per worker per phase; wall limit 1800 seconds and peak
RSS limit 2048 MiB per worker. Save every outcome. No replacement of rejected
clouds, no resource-driven retry, no stopping after an attractive result. An
execution/resource failure forces HOLD. Predictions use only reconstructed
features, observed order, inferred scale and the frozen model, and are sealed
before truth is regenerated. The old full selection/reconstruction is retained.

## Locked evaluation and gates

Report attempts, abstentions, joint and family coverage with exact two-sided
95% Clopper-Pearson intervals, widths, group raw/adjusted RMSE, normalized block
means and second moments, group pointwise standardized moments, covariance
conditioning and shared/diagonal block variance ratios. Stratify descriptively
by development medians of support count and observed design condition; disclose
out-of-development-range clouds. Every aggregate weights clouds equally.

The unchanged shape tolerance is |mean z|<=.5 and mean z² in [.5,2]. Apply it to
each nonempty block and each group's cloud-balanced pointwise moments, in both
arms. At least 48 contributing clouds are required for each screen. These are
pilot screens, not confidence statements for a conditional covariance.

The prespecified paired focus metric is the average, across both arms and the
two focus blocks, of abs(log(mean z_block²)). Lower is better. Bootstrap whole
test clouds in matched pairs 2000 times using seed 77261021; report the percentile
95% interval of grouped-minus-pooled distortion. This is approximate bootstrap
evidence; no finite-sample type-I guarantee is asserted.

GROUP_MODEL_PILOT_SUPPORTED requires ALL of:

- At least 48 complete calibration and test clouds.
- Grouped observed simultaneous test coverage >=95%.
- Every grouped block and group shape screen passes in both arms.
- The paired focus-distortion interval lies entirely below zero.

Otherwise the decision is HOLD_GROUP_MODEL. In all cases retain
HOLD_EMBEDDING_COVARIANCE, HOLD_PHASE3 and historical METADATA_HOLD. No production
geometry correction, anisotropic projection, Kalman update or transfer to 4D is
enabled. A pilot pass would not empirically certify populations-wide 95% coverage.
No test outcome may alter thresholds, replace seeds, select a different model,
or change the reported primary decision.

## Verification and provenance

Replay source hashes and public ancestry, all development fitting/shrinkage,
all fresh predictions, regenerated truth coordinates, scores, radii, summaries,
paired bootstrap and record hashes. Selection/inference inputs are archived and
not regenerated by the replay. Numeric tolerances are atol=1e-8, rtol=1e-7;
floating byte hashes of regenerated coordinates are diagnostic only.

Analytic controls include the inherited eight checks and fourteen new groups:
exhaustive grouping, independent PSD factorization, Gram cross terms, signed
scale negative covariance, cross-group endpoint dependence, group/cloud weights,
observed-order classification, Lorentz-invariant covariance, leave-one-cloud-out
zero bias, zero error, conformal rank, the inference-only signature, shape-screen
negative controls, and paired-improvement direction/negative controls.

Split-conformal basis: Lei et al., *Distribution-Free Predictive Inference for
Regression*, JASA 2018, section 2.2,
https://www.stat.cmu.edu/~ryantibs/papers/conformal.pdf . The particular structured
model, comparison and pilot gates are this study's prespecified hypotheses.
