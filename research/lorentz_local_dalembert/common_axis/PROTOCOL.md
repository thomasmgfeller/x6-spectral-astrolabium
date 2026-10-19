# Common-axis reference trial — frozen 19 October 2026

The accepted shell-weight development candidate reduced second-moment error,
but retained large first moments and incorrect time-quadratic responses. This
bounded trial tests a common reference frame for both shell centres. It does
not fit weights to coordinate fields or declare flat/curvature qualification.
All earlier research directories remain immutable.

## Intrinsic rule, fixed before development

Keep the marked longest-chain root r, shell depth m, endpoint depth n, temporal
endpoints a (past) and b (future), nominal times and balanced64 overlap estimator
from the preceding audit. On each full longest-chain shell, consider only x
strictly inside I(a,b). Estimate every required proper time by
q(u,v) = [N(u,v)/(rho*pi/12)]^(1/3), using strict interior counts. Require all
five counts for (a,b), (a,r), (r,b), (a,x), (x,b), as well as (r,x), to be positive.
The first three are common to all candidates. No pseudocount or fitted correction.

Define

    dt(x) = [q(a,x)^2 - q(x,b)^2 - q(a,r)^2 + q(r,b)^2] / [2*q(a,b)]
    h(x)  = dt(x)^2 / q(r,x)^2 - 1.

In exact flat geometry, dt is the time displacement from r in the rest frame
of b-a, and h = sinh(rapidity)^2 is the squared transverse separation divided
by squared proper time from r. The frame axis need not pass through r: taking
the difference cancels its spatial offset. In particular, this does not assume
that the two marked temporal endpoints are collinear with r.

Require dt>0 on the future shell and dt<0 on the past shell. Choose the x with
minimum |h|; break exact ties by the transported iid mark. Negative h estimates
are retained and penalized by magnitude, never clipped. This is a fixed noisy
nearest-axis heuristic, not an unbiased estimator. Archive every candidate's
counts, dt, h, score and rejection status. If common counts fail or either side
has no eligible candidate, that candidate stencil is unavailable. Do not fall
back to the old centre. Rebuild the caps around the new centres with unchanged
balanced64 distance, radius, minimum population and weight construction.

This aligns the reference choice in a shared local frame. It neither moves
points nor guarantees balanced finite-sample first moments. The temporal
endpoints and their chain-time weights remain unchanged.

## Fixed arms and coordinate boundary

* raw: unchanged balanced64 stencil and chain-time weights; context only.
* volume_shell: previous intrinsic shell weights on old centres; sole baseline.
* axis_shell: new intrinsic centres, same inverse-square volume shell weights;
  sole primary candidate.
* oracle_axis_shell: same new selection rule with exact embedding proper times
  substituted ONLY for the six reference-selection times. Cap distances and
  shell weights remain intrinsic. Diagnostic comparator, never a fallback winner
  or theoretical lower bound.

The intrinsic selector accepts only relation/count access, marks, shell members,
root/endpoints and known density. It must not import coordinates, sampler,
evaluation fields or optimization packages. A pure score helper may accept
scalar times; only the separate runner constructs oracle times.

## Fixed execution and observables

Publish this protocol before six development clouds, then publish implementation
AND analysis before 48 new targets (16 each at densities 2048, 8192, 32768).
All seeds, thresholds and budgets are fixed in contract.json. Development may
fix software defects, but cannot change the mathematical rule or parameters.
No replacement clouds, post-test fixes, parameter search or optional stopping.
Archive all statuses, selections, weights, input hashes and resource use.
An error or exhausted budget produces HOLD with its partial record.

Reuse the frozen field evaluator: M=1/2 sum w dX dX^T, metric error
||M-eta||/sqrt(3), A=B(t,x,y), and dimensionless drift tm*||A||/sqrt(3).
Archive dimensional A, all linear/quadratic fields, constant and exp(t+x+y),
Lorentz signatures, product identity and affine tensor transformation law.
All norms use the original diamond frame; they are not Lorentz-invariant norms.
Report actual reference rapidities in the shared endpoint frame, estimated h
errors, negative-h frequency and cap populations. These are evaluation-only.

At the highest density, axis_shell must have >=80% availability, paired metric
RMS <=75% of volume_shell RMS AND paired affine drift RMS <=75% of baseline.
Both ratios use exactly their common available clouds. Missing clouds stay in
the availability denominator. Report every arm at every density and paired
squared-error reductions with cloud-level standard errors. Do not pool shell
points as independent replications. These are descriptive improvement gates,
not confidence-certified tests or convergence criteria.

Complete execution, budgets, software controls and all three gates yield
COMMON_AXIS_IMPROVED; otherwise COMMON_AXIS_HOLD. Always HOLD_PHASE3, even if
the candidate improves. The inherited absolute metric threshold 0.5 and broader
flat acceptance requirements remain unmet unless separately demonstrated.
Never promote the oracle arm. Failure stops this candidate at this budget.

## Controls and replay

Verify the score identity independently on exact Minkowski fixtures including
an off-axis root, translations, a Lorentz boost and time reversal. Verify zero
counts, sign rejection, negative-h handling, mark tie-breaking and permutation.
Check density scaling: multiplying rho by 8 halves estimated times but leaves
h, candidate order and selected references unchanged. Relabel and reverse one
development and target cloud per density; transported marks must preserve the
intrinsic selections and weights. Check the coordinate-blind source boundary.
Reusing a reference must reproduce the baseline stencil exactly.

Replay all 48 targets, verify public source/record hashes and recompute the full
summary. Discrete outputs and relation/mark hashes exact; numerical tolerance
atol=1e-10, rtol=1e-9. Report coordinate byte equality separately from numerical
replay. Do not claim bitwise portability or independent external replication.
