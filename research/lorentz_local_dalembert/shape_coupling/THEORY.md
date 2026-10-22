# Shape perturbations with a deterministic joint-law coupling

SPDX-License-Identifier: Apache-2.0

## Fixed experiment

Condition on the selected 21-node order. The base is geometry 0 of the rational
PR88 witness. All four landmarks, the root, physical normalization scale,
known density, and physical sampling diamond remain fixed. Only one of the
16 support points moves. The four fixed landmarks form a nondegenerate affine
frame, so a nonzero support displacement cannot be a common Lorentz isometry,
translation or dilation of the whole configuration. This is a genuine shape
change. The target is the physical minimum-norm quadratic moment weight vector.

The observation consists of the 90 recorded interval counts, their pairwise
or higher-order overlap counts, and optionally the total B point count. The
selected-node order is known and identical. Coordinates, the complete B causal
matrix, extra intervals and the A-selection likelihood are not observations
in this experiment. The result is not automatically valid for those richer
experiments. As in PR94, membership in the earlier realized confidence set is
not asserted or required for a two-point statistical bound.

## Common Poisson coupling

Use the same homogeneous B Poisson cloud for both geometries. Every selected
interval is contained in the fixed outer interval I(3,0). This is certified
from the exact common order. Apply the same rational Lorentz boost to both:

    (t',x',y')=((17t+15x)/8,(15t+17x)/8,y).

It has determinant one. Let A be an upper bound for the area of the spatial
projection of I(3,0) in this frame, using the inherited directed bounding box.
The physical volume factor is scale³. There is no numerical integration.

For a cone with tip v, its future membership is

    f_v(t,x)=t-v_t-||x-v_x|| > 0,

and past membership uses -t+v_t-||x-v_x|| > 0. Moving the tip by d changes either
function by at most eta=|d_t|+||d_x||. If membership changes, the original
function lies in [-eta,eta]. At fixed spatial coordinates this slab has time
length at most 2 eta. Its intersection with the outer interval therefore has
volume at most 2 eta A. There are at most two affected cones for one moved tip;
all intervals incident to it use one of those same cones. Thus their entire
membership-change region has volume at most 4 eta A. No factor of 90 is needed.

For the axis displacements used here, eta=h exactly. The mean number of Poisson
points in the union of changed memberships is at most

    M = 4 rho scale³ A h = C h.

If no point falls there, every interval membership agrees point by point.
Hence all counts and overlaps of any order agree, while the total count agrees
identically under the common cloud. The elementary coupling inequality gives

    TV(P0,P1) <= P(observations differ)
              <= 1-exp(-M) <= M.

For completeness, for any event E, the difference of its two indicator
functions vanishes when observations agree, so the probability difference is
at most the disagreement probability. Taking the supremum proves the coupling
inequality. This proof retains arbitrary dependence among interval counts.
It is a sufficient upper bound and need not be close to the optimal coupling.

## Frozen finite search and exact checks

Budgets are b=1/20,1/10,1/4. For each choose

    h = floor((b/C)*10^12)/10^12,

then displace each of 16 support points in the three boosted coordinate axes
and both signs. These are 288 fixed candidates. The inverse boost generates
exact rational source-frame coordinates. Landmarks, root and outer interval
are unchanged. Every candidate is checked for exact selected-node order and
the inherited separation margin, followed by a rational moment solve.
The strongest lower symmetric relative weight gap selects the witness.
The selected pair also passes exact intrinsic conditioning gates.

Candidate rejection is not silently discarded: all rows are archived, and an
independent audit separates actual order changes from margin-only rejection.
No adaptive enlargement, random search or tuning after seeing a validation set
is performed. There is no validation sampling error in these exact bounds.
The contract/hash freeze is reproducibility evidence, not external preregistration.

## Target separation and statistical interpretation

Write D=||w1-w0|| and r=2D/(||w0||+||w1||). Disjoint 10%-relative-error balls
require r>0.2. With beta a proved TV upper bound, any estimator satisfies

    max_g P_g(||w_hat-w_g|| >= D/2) >= (1-beta)/2,
    max_g E_g ||w_hat-w_g|| / ||w0|| >= (D/||w0||)*(1-beta)/2.

Nearest-target testing proves the probability statement. For expected loss,
integrate the triangle inequality against min(p0,p1), whose mass is 1-TV, then
take half the sum of risks. The normalization ||w0|| is fixed under both laws.
These are conditional statistical bounds for discrete weights, not continuum
error or smooth-field accuracy bounds.

## Outcome and stop

252 candidates satisfy exact order, separation margin and moment rank. Of 36
rejections, 32 change at least one causal relation; four retain the order but
violate the inherited near-null margin (and still have solvable moment systems).
The selected displacement moves node 15 in the positive boosted x direction by
1681989/200000000000. Its TV upper bound is below 1/4, but its symmetric relative
weight gap is only about 0.00365762%. All certified candidate upper gaps are
below the strong threshold. The fixed search stops without a strong pair.

This does NOT rule out close-law shape pairs, nor prove uniform stability.
Unlike PR94's homothety stopping theorem, this is only a negative result for
288 specific perturbations under a conservative coupling certificate.
The single-point family misses coordinated motions, and the slab bound counts
any changed membership as potentially detectable even when aggregated count
laws overlap heavily. A useful next improvement is a bound using intensities
of joint membership atoms (or a certified smoothing inequality), followed by
coordinated deformations. Repeating this same finite search adds no evidence.

## Reference

S. Roch, *Modern Discrete Probability*, Chapter 4, coupling inequality:
https://web.math.wisc.edu/~roch/mdp/roch-mdp-full.pdf . The inequality is proved
above; geometric and numerical claims follow from the repository certificate.
