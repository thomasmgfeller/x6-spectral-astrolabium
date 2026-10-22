# Stability follow-up: fixed diagnosis and conditional count test

The completed PR84 experiment is now development data. Its 2.215 variance
ratio, cloud04 concentration and all 13 capped count-eligibility failures were
seen before this freeze. No claim of preregistering those observations is made.

## Separate questions and fixed work

1. Replay all 13 failed original A seeds. Verify the entire archived selection
   record byte-for-byte. Exhaust both complete common predecessor/successor pools
   for the fixed root/support and first three landmarks. Keep all original
   comparability, full16/half4 and Gram/moment conditions. Save one decision and
   a failing relation/count witness or passing packet per candidate. This can
   distinguish a 128-per-side search cap from absence of a feasible fourth
   landmark **in this fixed family**; it says nothing about different supports
   or jointly replacing the first three landmarks. Original failures stay failed.
2. On every one of the old 19 selected configurations and all nine old B draws,
   execute three fixed diagnostic variants: (a) remove only support-support
   order constraints from the original Poisson objective; (b) nonlinear raw-count
   GLS with diagonal covariance; (c) the same GLS with full covariance and
   fixed 5% shrinkage toward its diagonal. All other conditions, start, forward
   mean and budgets are unchanged. Retain raw calculable but order-invalid
   negative controls; these cannot be deployed or counted as qualified.
3. Independently generate nine NEW B clouds per same 19 selected A configurations,
   using seed tag 782071. Compare unchanged four inversion, original joint
   Poisson fit and one prespecified full-covariance GLS candidate. No parameter
   tuning or repeated selection after inspecting results. Always complete this
   bounded conditional test, even if developmental results are unfavorable.

## Covariance-aware candidate

Use exactly the old four-input interval mask. The raw count covariance estimate
C is the matrix of observed interval-intersection counts, including its diagonal
N. Given the Poisson overlap model, C estimates rho times overlap volume, but is
itself random and correlated with the residuals. Fix C_alpha=.95 C+.05 diag(C)
and minimize (lambda(z)-N)^T C_alpha^-1 (lambda(z)-N)/m, where the full nonlinear
forward mean remains rho*pi/12*scale^3*q(z)^(3/2). The 5% is a fixed numerical
regularization choice, not estimated from either test outcomes or truth.

This is regularized plug-in generalized least squares, **not** the exact joint
count likelihood, an unbiased estimator, a calibrated confidence distribution
or a cure for shared-data dependence. No Hessian covariance is reported.
The original constraints, one start, minimum counts and 20-second fit budget
are inherited. Inference receives only packet, counts, overlap matrix and rho.
Simulation coordinates and fields are reserved for post-seal evaluation.

## Conditional gates and interpretation

Contract.json freezes primary B0 and repeats B1-B8. Require at least 16/19
qualified primary candidates and 16 common computable cases; RMSE ratio <=.9
and iid field-noise variance ratio <=1.25 versus old four inversion. Require at
least 14 complete paired repeat groups, mean response-variance ratio <=1.25
versus four and <=.8 versus original Poisson fit on the SAME groups; fit median
<=5s and maximum <=20.5s. All gates required for a conditional development signal.
Use all eligible groups; never discard cloud04 or another outlier from the gate.

Calculate all failure counts, field errors and variances. Primary accuracy is
conditional on common valid weights, not a global loss with abstentions hidden.
Record order qualification separately. Negative-control comparisons with
different availability must state their common group IDs. Conditional repetitions
and four fields do not multiply independent A selections. Results are descriptive
engineering gates, not population significance or coverage statements.

Regardless of result: no global pipeline adoption or new independent-A claim.
HOLD_PHASE3, HOLD_EMBEDDING_COVARIANCE and METADATA_HOLD remain. If the conditional
candidate fails, stop this variant without posthoc retuning. No curved/3+1,
Kalman, physical sensor or old V1 revival claim.

Six synthetic controls precede the local code/input freeze. This is not public
preregistration. The old raw data, sources and prior freezes remain unchanged.

SPDX-License-Identifier: Apache-2.0
