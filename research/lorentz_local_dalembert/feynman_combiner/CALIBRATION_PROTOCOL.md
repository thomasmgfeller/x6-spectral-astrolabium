# Minimum-variance weights and independent scalar calibration

Frozen before new clouds; development uses only the 48 already archived clouds.
All moment conditions remain exact. The minimized objective is
sum(a_i^2)+(sum(a_i))^2, the conditional IID field-noise gain including the
shared root field. Unrestricted QP uses an equality-constrained linear solve;
sign-constrained QP uses SLSQP followed by active-face polishing. Every accepted
solution must satisfy separately computed primal/dual KKT conditions. Failed
certificates remain unresolved. Sign infeasibility inherits a checked LP
separator. Reducing this conditional objective does not minimize geometric bias.

The independent pilot uses 32 calibration and 32 held-out high-density physical
Poisson clouds, disjoint seed ranges fixed in calibration_contract.json. Existing
count/frame selection and hidden-colouring guards remain unchanged. Every cloud
is recorded; no seed replacement. Three primary scalar estimates share the same
cloud and field sample: transferred baseline, unrestricted minimum-L1 weights,
and unrestricted minimum-variance weights. The sign-constrained variant remains
a separate diagnostic. This is not three independent physical measurements.

For each cloud, the supplied scalar test field is exp(t/2)cos(x/2)cos(y/2), in
simulation coordinates centred at the selected root; the known d'Alembertian
there is -0.75. Field values/truth are accessed only after intrinsic weights
are sealed. Field noise sigma=0.001 is generated once per event, including
one root noise shared across all differences and all arms. Clean and noisy
responses are both retained. The raw field is a diagnostic probe, not a claim
that an embedding is measured intrinsically. The true-coordinate field is not
used to select supports, weights or infer an intrinsic metric.

Calibration means estimate each arm's bias. Joint centred error covariance is
estimated across independent physical clouds. Test bias correction, simplex
fusion weights and selected single comparator are fixed from calibration only.
The primary comparison is one synthetic independent prior per physical test
cloud, true value plus Gaussian error sigma=0.5, with the same prior used for
all arms. Kalman cross covariance is zero by this explicit construction; this
is not permission to set it to zero on overlapping real sequences. Bias-mean
estimation variance is included by the factor (1+1/n_cal). Covariance/weight
estimation uncertainty and non-Gaussianity are not thereby solved.

The analysis reports raw bias, covariance, correlations, covariance condition,
measurement and posterior RMSE, nominal Gaussian 95% coverage, exact binomial
coverage intervals, NIS/NEES and paired cloud-bootstrap RMSE-ratio intervals
(5000 bootstrap draws, seed 70030000). It also compares conditional field-noise
covariance with actual clean-response variation. No outcome-based retuning.
The naive diagonal-only fusion is an explicit negative control. All failures
remain in availability denominators; accuracy/coverage are conditional on
complete guarded cases. Predictions in absent cases cannot be relabelled as
measurements. No sequential independence or full embedding covariance claim.

Decision and budgets are fixed in the JSON contract. An exploratory empirical
coverage threshold does not establish a population guarantee with 32 clouds.
Even PILOT_SUPPORTED cannot qualify an online filter or curvature. Supports
include future events: this remains an offline experiment. HOLD_PHASE3 remains.
