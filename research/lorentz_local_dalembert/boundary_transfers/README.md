# Boundary-localized transfers: a sharper full-law upper bound

SPDX-License-Identifier: Apache-2.0

**Localization: CERTIFIED. Additional cancellation: HOLD_FULL_PATTERN_LOCALIZATION.**
For the unchanged PR95 pair, the certified TV upper bound improves from
**0.22119921517101921040 to 0.01981978079819577960**. The improvement comes from
spatially restricting the moving-cone strips and retaining the exact Poisson void
probability. **No additional cancellation is certified for the actual pair.**
The symmetric operator gap remains about 0.00365762%; no strong two-point
counterexample, general stability result or reconstruction-accuracy gain follows.

| Spatial grid per cone | Surface rectangles, both cones | Unresolved intensity upper | TV upper |
|---|---:|---:|---:|
| 16 × 16, split at bisector | 544 | 0.02854718880004301911 | 0.02814356767479259583 |
| 32 × 32, split at bisector | 2,112 | 0.02309064538615183931 | 0.02282609654717693203 |
| 64 × 64, split at bisector | 8,320 | 0.02001882707982844326 | 0.01981978079819577960 |

These are rigorous upper bounds on the declared conditional count/overlap law,
not estimates of actual TV. Unresolved intensity is retained, not discarded.
At the final grid 6,398 rectangles lie wholly outside the fixed outer diamond;
1,922 remain unresolved in their complete membership patterns. There are no
fully certified off-diagonal transfer pairs. The exact cone-strip volume is
not known, and the output is not a confidence interval for actual TV.

## Why only two-dimensional integration is needed

Work in the same determinant-one boost frame and physical normalization as
PR95. The selected node moves by h>0 in x, with time and y fixed. Put

    r0(x,y) = sqrt((x-vx)^2+(y-vy)^2),
    r1(x,y) = sqrt((x-vx-h)^2+(y-vy)^2).

Future membership changes only between times vt+r0 and vt+r1; past membership
changes only between vt-r0 and vt-r1. These two strips are disjoint up to null
boundaries. The thickness of each is |r1-r0|, always <=h by the triangle
inequality. This alone improves the old two-sided-slab mean bound 4*rho*s^3*A*h
to 2*rho*s^3*A*h, before any numerical localization.

To avoid subtracting two poorly enclosed radii, use the exact identity

    r1-r0 = [h^2 - 2*h*(x-vx)] / (r1+r0).

Split the spatial rectangle grid at x=vx+h/2, so the numerator has a constant
sign on each cell. Rational interval bounds on its absolute numerator and the
sum of radii enclose the thickness; when a denominator lower bound vanishes,
the upper bound h remains valid. The numerator lower bound divided by the
positive denominator upper bound supplies a lower thickness bound.
Multiply thickness bounds by exact spatial area and rho*s^3. Per-cell intensities
are rounded outward to 30 decimal places before summation, preventing rational
denominator growth while preserving inclusion.

## Coverage and membership certificates

The inherited bounding box contains the fixed outer diamond. The complete
spatial rectangle is partitioned without gaps or overlaps apart from cell edges.
Outside this rectangle there is no observation-sensitive mass. For each spatial
cell and each strip, an enclosing time interval follows from rational bounds on
both radii. All coordinates are rounded outward to multiples of 2^-18.

For any tip enclosed by [a,b] and box [l,u], compute minimum/maximum possible
squared spatial distance. A cone is certainly inside when its minimum signed
time difference is positive and its square exceeds the maximum distance squared.
It is certainly outside when no positive time difference with sufficient square
is possible. These implications are valid over the whole enclosing box.
Signed int64 operations are protected by a coordinate-magnitude assertion;
with magnitudes <10^7, squared differences and their two-term sum cannot overflow.

On the active moving cone, membership is known analytically: throughout the
open strip, original membership is true iff r1>r0, and deformed membership is
its opposite. This holds for both future and past strips. Forcing this one
bit is justified on the strip itself; all other cone bits use enclosing-box
certificates. Spatial/time boundary sets have zero Poisson intensity.

The fixed outer interval I(3,0) is among the observations. A strip cell whose
outer membership is impossible is discarded with proof. If every interval
incident to the active cone is impossible under both geometries, the cell
cannot change any observation. Other intervals have unchanged endpoints or use
the opposite cone, which is false throughout the active strip. Fully known
complete patterns yield a directed transfer intensity enclosure; equal patterns
contribute no change. Every other cell contributes its ENTIRE strip-intensity
upper bound to an unresolved budget R. No independence of interval counts is
assumed. Optional total B count agrees under the common cloud.

## Cancellation accounting, including incomplete tables

Let each known directed transfer t_bc have bounds [L_bc,U_bc]. Incoming and
outgoing sums yield intervals [inL,inU] and [outL,outU] for each atom label.
The known difference is enclosed by [inL-outU,inU-outL]. Unknown transfers have
mean at most R and contribute at most 2R to the L1 intensity difference.
Therefore the balanced residual intensity D obeys

    D <= (1/2)*sum_b max(|inL_b-outU_b|, |inU_b-outL_b|) + R.

An independently valid actual cancellation lower bound is

    C_L = sum_b min(inL_b,outL_b).

Since D = M_actual - sum_b min(in_b,out_b), also D<=M_U-C_L, where M_U bounds
all changed memberships. The runner takes the smaller certified upper bound.
**A difference between two upper bounds is not itself a lower bound on actual
cancellation.** The audit includes uncertain bidirectional transfers specifically
to prevent that error. Unknown transfers can increase cancellation but cannot
invalidate C_L. The Poisson marking coupling from ../paired_atoms/README.md gives
TV<=1-exp(-D); alternating rational Taylor bounds enclose its evaluation.

In this run the transfer table is empty: D_U=M_U=R, C_L=0. Thus the entire gain
is localization, not cancellation. Exact synthetic tests verify that the code
can certify complete labels in both cone directions and that an exact balanced
cycle cancels, but those tests are not actual-pair results.

## Remaining obstruction and next decision

The fixed budget of three spatial grids is exhausted. At level 64, interval
(5,0) remains ambiguous in 1,433 retained cells; (5,1) in 567; (13,0) in 517;
(3,5) in 493; (17,0) in 480. These are internal geometry node indices and counts
of overlapping ambiguities, not disjoint masses or proof of the dominant error.
The next targeted improvement is to bound these other cone functions directly
ON the moving cone surface, retaining correlations between t and (x,y).
The enclosing time box currently loses those correlations. Do not repeat a
full-volume grid or expand the geometry search on the strength of this result.

## Reproduction

From the repository root:

```sh
python3 -B research/lorentz_local_dalembert/boundary_transfers/bt_run.py --verify
python3 -B research/lorentz_local_dalembert/boundary_transfers/bt_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/boundary_transfers/SHA256SUMS
```

The independent scalar audit checks 4,896 rational strip points, including 3,456
points in excluded-domain cells, exact spatial area coverage, synthetic complete
patterns in both directions, exact and uncertain transfer cycles, and retention
of unknown mass. These point checks audit the implementation; interval bounds
and the partition argument establish full coverage. Freeze files pin the
contract, implementation and inherited inputs; they are reproducibility records,
not external preregistration or independent peer review.
