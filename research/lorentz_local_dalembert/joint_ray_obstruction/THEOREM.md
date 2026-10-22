# A joint event closes the remaining continuous ray interval

SPDX-License-Identifier: Apache-2.0

## Statistical experiment and geometric independence

Keep the conditional Poisson count/overlap experiment of PR95–109: the density,
reference geometry, selected nodes, outer diamond and count definitions are fixed.
Only node 15 moves in the negative boosted x direction; its boosted time stays
fixed. Write

    A_h = I(z_2,z_15(h)),  B_h = I(z_15(h),z_1),
    X_h = N(A_h),          Y_h = N(B_h).

Both counts are already observed (indices 2 and 3 among the 90 counts). Every
point of A_h is strictly before the tip z_15(h), and every point of B_h is
strictly after it. Their intersection is empty. Thus, **under each fixed
geometry**, X_h and Y_h are independent Poisson random variables with the
respective interval means. No independence is assumed between other counts,
and no independence between observations from two different geometries is needed.
This argument would not apply to two overlapping Alexandrov intervals.

The fixed event is

    E = {Y - 2 X <= 787}.

The same map of the same measured coordinates is used under both geometries.
By the definition of total variation and projection onto these two counts,

    TV(P_full(0),P_full(h)) >= P_0(E) - P_h(E).

It is sufficient to bound this one signed event difference. No optimality claim
for this event, equality with full-law TV, or independent interval approximation
is required.

## Whole-interval geometric enclosures

For h in [45/1024,51/1024], the inherited exact boosted quadratic q(h) for
each interval has extrema at its endpoints or its vertex. Both q-ranges remain
positive. The volume and mean in the inherited 2+1-dimensional model are

    V(I) = pi * q^(3/2) / 12,
    mean = rho * scale^3 * V(I).

Outward rational pi and square-root enclosures give simultaneous mean intervals
for every h in this continuous interval. Separate enclosures can lose dependence
between the two means; taking a containing rectangle is conservative.

For independent Poisson X,Y, P(Y-2X<=787) is increasing in the mean of X and
decreasing in the mean of Y. This follows by adding independent Poisson
increments to either variable. Therefore an enclosing rectangle
lambda_X in [a,b], lambda_Y in [c,d] gives

    F(a,d) <= P(E) <= F(b,c).

Apply this to both the reference and moved geometries. If the reference lower
event probability minus the moved upper probability exceeds 1/4, the full-law
TV gate is impossible throughout the entire remaining interval.

## Directed probability computation with retained infinite tails

For a Poisson mean mu>0, let m=floor(mu), set the unnormalized weight w_m=1,
and use

    w_(j-1) = w_j * j/mu,   w_(j+1) = w_j * mu/(j+1).

All integer weights on a 10^-80 grid are rounded downward/upward at every
step. Downward recurrence reaches zero; upward recurrence stops at K. If u_K
is the upper grid weight, the omitted infinite sum is bounded in the same grid
units by

    R <= ceil(u_K * mu/(K+1) / (1-mu/(K+2))).

The ratios in the remaining tail are at most mu/(K+2)<1. Hence the exact
normalizer is enclosed by Z_L=sum(w_L) and Z_U=sum(w_U)+R. The mu=0 distribution
is handled exactly.

For the event, conditional summation gives

    F(mu_X,mu_Y) = sum_(j>=0) p_X(j) * CDF_Y(787+2j).

The finite lower numerator is the sum of products of lower X weights and lower
Y prefix weights; divide it by Z_X,U * Z_Y,U. The upper numerator uses upper
weights and divides by Z_X,L * Z_Y,L. Add R_X/Z_X,L for omitted X values, and
cap the result at 1. The Y tail is retained in its normalizer; all required
prefix thresholds are inside the stored Y support. Thus **neither infinite
tail is discarded**. All final displayed decimal intervals are outward rounded.

## Composition with PR109 and stopping rule

PR109 already supplies a gap-free continuous cover of all 64 fixed-base rays.
Its only 30 HOLD leaves lie in the one interval addressed here. A uniform
joint-event exclusion of that interval combines with PR109's operator, order
and marginal-law certificates to exclude the full declared family.

This is a family-specific obstruction to the conjunction

    same selected-node order AND symmetric weight gap >20% AND TV<=1/4.

It is not a quantitative global reconstruction-stability theorem. Pairs of
non-reference deformations, coordinated node movements and other base clouds
remain outside the domain. The auxiliary energy class from PR109 is not used
to obtain this result, and the physical continuum questions remain open.

Only one fixed joint event is evaluated. A failed certificate would retain
HOLD without changing its threshold, introducing new observations or silently
extending the search budget. Probability computations are deterministic; there
is no Monte Carlo confidence level or Gaussian approximation in the proof.

The full-count interpretation and marginalization were established in the
repository's [Poisson testing](../poisson_testing/README.md),
[joint atom](../joint_atoms/README.md), and
[continuous certificate](../continuous_energy/THEOREMS.md) packages.
