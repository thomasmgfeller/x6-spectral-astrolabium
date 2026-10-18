# Covariance-aware de Sitter information planning

Scope: four-dimensional de Sitter, uniform physical-volume sampling,
independent clouds conditional on an externally chosen N. The dimensionless
target is q = R T². Absolute curvature requires an independent proper-time
scale T. Unknown sampling density still admits conformal density twins.

For F_k = C_k / choose(N,k), p = (1/10, 1/350, 1/29400), define
y_k = F_k/p_k - 1. The published conditional RSS first-order expansion,
restricted by R00 = -R/4, gives E[y] = b q + remainder,
b = (1/90, 1/42, 1/27). This is a local expansion, not an exact finite-q law.
See Roy, Sinha & Surya, https://arxiv.org/abs/1212.0631 and the repository's
fixed-N derivation, which makes the conditional normalization explicit.

For positive definite covariance Sigma, minimizing w' Sigma w subject to
w' b = 1 gives w = Sigma^-1 b / (b' Sigma^-1 b). This is minimum variance
among these linear estimators under the first-order model and a supplied
covariance, not Fisher information or a general Cramer-Rao bound.
We compare C2 alone, C2+C3 and C2+C3+C4. Weights use only published flat
pilot clouds at the same N and are fixed for every curved holdout cell.
The full covariance retains overlap and correlation of chains within a cloud.
No independence assumption between individual chains is made.

For M independent, equally distributed clouds, the mean estimator has
variance w' Sigma w / M. The planning count for half-width delta is
ceil(z_.975² * w' Sigma w / delta²). This is a plug-in normal approximation
for sampling noise, not a finite-sample coverage guarantee. Covariance
estimation uncertainty and bias are not included in that count. Repeated
overlapping diamonds cannot be substituted for independent clouds; larger N
is not equivalent to more clouds. Bias w' remainder persists as M grows.

The planning data were already public and inspected: their reanalysis is
descriptive. Only the new seed namespace, fixed estimators and fresh test
are prospective. A single primary comparison tests whether the upper end
of a paired percentile bootstrap 95% interval for RMSE(GLS234)/RMSE(C2)
at N=128, h=.5 is <= .9. This is an approximate bootstrap procedure.
Other cells and GLS23 are descriptive. Negative estimates are retained.
No tuning, clipping, reseeding, optional enlargement or early stopping.

The h=.5 cell has H*T about .511: finite-curvature remainder is a real
limitation. Independent pair quadrature quantifies the C2 expectation bias
at each tested h. C3/C4 remainders remain unbounded; empirical mean-bias
intervals (Student approximation with Bonferroni over twelve comparisons)
do not prove a uniform remainder bound. A positive RMSE comparison alone
does not qualify curvature confidence intervals or a curved proper-time clock.
