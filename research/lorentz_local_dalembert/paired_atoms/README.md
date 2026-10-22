# Paired membership transfers: sharper same-pair certificate

SPDX-License-Identifier: Apache-2.0

**SHARPER_SAME_PAIR_COUPLING_CERTIFIED; HOLD_TRANSFER_LOCALIZATION.**
The unchanged PR95 geometry pair now has the certified full count-channel bound
**TV <= 0.22119921517101921040**, versus the previous linear upper bound
0.24999999774322784776. The roughly 11.52% reduction comes solely from evaluating
`1-exp(-M)` instead of `M`, an inequality already proved in PR95. It is not a new
geometrical integration result, an observed TV, or an 11.52% estimator improvement.

The symmetric operator gap remains only about **0.00365762%**, far below the
20% strong-pair threshold. No strong counterexample or global stability result
has been obtained. The earlier joint-atom volume-resolution HOLD is unchanged.

## What the paired formulation adds

For a common physical domain, let `t_bc` be the Poisson intensity of the region
whose complete interval-membership pattern is b before and c after deformation.
Let `m_b=t_bb`, `out_b=sum_{c!=b}t_bc`, `in_b=sum_{c!=b}t_cb`.
Then the two atom intensities are `lambda_b=m_b+out_b` and
`mu_b=m_b+in_b`. Therefore the difference is **in_b-out_b**: common mass cancels
exactly, even if it is large or poorly resolved. All 90 counts and their overlaps
are deterministic functions of these Poisson atoms. Their dependencies remain.
The outer interval and its complement are fixed as in PR95; optional total B
count adds only common outside mass. No unobserved membership class is discarded.

Write `d_b=abs(in_b-out_b)` and `J=sum_b(sqrt(lambda_b)-sqrt(mu_b))^2`.
For every b,

    (sqrt(lambda_b)-sqrt(mu_b))^2 <= d_b,
    (sqrt(lambda_b)-sqrt(mu_b))^2 <= d_b^2/(4*m_b)  if m_b>0.

The second inequality follows by multiplying the root difference by the root
sum, whose square is at least 4*m_b. Summing the smaller valid bound gives J_U.
The Poisson affinity derivation in ../joint_atoms/THEORY.md gives
`TV <= sqrt(1-exp(-J)) <= min(1,sqrt(J_U))`. Validated lower m and upper d also
suffice for this termwise bound. The current routine accepts exact finite tables;
it does not pretend to have integrated the actual geometry's transfer table.

Equal total intensity implies `D=sum_b d_b/2 <= sum_{b!=c}t_bc = M_actual`.
Another coupling uses independent common Poisson atom counts with rates
min(lambda_b,mu_b), plus one shared K~Poisson(D). Mark its K residual events
according to each law's residual label probabilities. Each marginal has the
correct independent Poisson atom counts by Poisson splitting. If K=0 the entire
vectors agree, hence `TV <= 1-exp(-D)`. D=0 means equal laws.
Bidirectional transfers can therefore change pointwise memberships while leaving
all aggregate count laws identical. This is a finite control, not a claim about
the repository geometry pair.

## Actual pair and exact numerical enclosure

Reuse the rational displacement, slab area and density from PR95 without moving
any point further or searching new geometries. Its already proved switched-region
bound is `M_actual <= M=C*h < 1/4`. Thus `D<=M` and
`TV <= 1-exp(-M)`. The code encloses this expression using alternating rational
Taylor sums through degrees 80 and 81. For 0<=M<=1, successive term magnitudes
decrease, so the even sum bounds exp(-M) above and the odd sum below. Reported
endpoints are rounded outward. The interval displayed in summary.json encloses
**1-exp(-M)**, not the unknown actual TV from below.

The equal-prior best testing accuracy is at most 0.61059960758550960520.
The two-point error probability at half the unchanged tiny target gap is at least
0.38940039241449039480. These statements concern the declared conditional count
channel, not complete point clouds, continuum operators or a 10% error guarantee.

## What remains missing and the stop rule

PR100 provides 48 positive atom lower-volume labels at its final resolution.
These separate lower volumes alone do not identify the off-diagonal transfer
support or its signed balance. They must not be treated as common diagonal
intensities or as proof that all transferred mass has positive background.
With only a global transfer budget and unspecified additional labels, abstract
atom models can place the budget into two unbacked labels. This explains why
those inputs alone do not certify an additional smoothing gain; it is not a
realizable-geometry counterexample or an impossibility theorem.

Stop global uniform-grid refinement. The next numerical task is a certified
integration restricted to the moving cone boundaries, with joint labels on both
sides, signed transfer balances and a retained budget for unclassified transfers.
Do not expand the geometry search before a transfer-localization certificate
shows an additional gain on this unchanged pair.

## Reproduction and controls

From the repository root:

```sh
python3 -B research/lorentz_local_dalembert/paired_atoms/pa_run.py --verify
python3 -B research/lorentz_local_dalembert/paired_atoms/pa_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/paired_atoms/SHA256SUMS
```

Controls: exact two-label positive-background example; balanced two-way transfer
with exactly equal laws; zero-background labels retained; identity; invalid
negative intensities and diagonal transfers rejected. Six independent Decimal
exponential checks use precision 100 and absolute tolerance 1e-90 (the rational
Taylor enclosure supplies the proof). The toy bound 0.07088902 is deliberately
more conservative than the exact-intensity PR100 toy bound; neither is an
actual-pair atom result. Inputs, outputs and source are hash-pinned.
