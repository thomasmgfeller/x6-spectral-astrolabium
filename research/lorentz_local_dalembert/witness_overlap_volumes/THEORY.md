# Actual overlap volumes with a separate numerical error budget

SPDX-License-Identifier: Apache-2.0

This checks the two fixed exact-decimal witness geometries from PR88 against
PR90's original marginal and pairwise-overlap confidence bands. It does not
change those bands, refit a geometry, or prove closeness of full probability
laws. The numerical integration below is **probabilistically enclosed**, not
deterministic quadrature. Its ideal iid sampling assumption and seeded PRNG
implementation are distinguished explicitly.

## 1. Analytic reduction

For intervals I(a,b), I(c,d), their intersection is the set to the causal
future of both lower endpoints and past of both upper endpoints. Delete a
lower endpoint that precedes another lower endpoint, and an upper endpoint
that succeeds another upper endpoint. Causal transitivity makes these exact
set identities. If any retained lower endpoint does not precede any retained
upper endpoint, no positive-volume intersection exists. Null boundaries have
zero volume. With one lower and one upper endpoint, the intersection is a
single Alexandrov diamond; otherwise it requires integration.

For a diamond with q=(Delta t)^2-(Delta x)^2-(Delta y)^2>0, its 2+1 volume is
pi q^(3/2)/12 in normalized coordinates. Multiply by rho*scale^3 to obtain
its mean count. Rational square-root and pi enclosures give deterministic
bounds. Exclusive-region means follow by subtracting these analytic
intersection means from analytic marginal means, retaining outward bounds.

There are 2,701 unordered selected interval pairs: 2,221 are analytically
resolved and 480 require integration (240 distinct endpoint configurations).
Every selected interval is contained in I(3,0), verified from the exact order.
The audit also checks that its physical proper duration is below 1.5, the
original counting-diamond duration. A common Lorentz transformation and
translation therefore place it inside that domain without changing volumes.
The boost t'=(17t+15x)/8, x'=(15t+17x)/8, y'=y is rational, has determinant 1
and preserves the Minkowski quadratic form. All pair intervals and order
relations are checked exactly after the boost.

## 2. A guaranteed finite integration box

Let the containing diamond have endpoints a,b in boosted coordinates and
T=b_t-a_t. Its spatial projection is the ellipse
|r-a_sp|+|r-b_sp|<=T. With spatial center (a_sp+b_sp)/2, its coordinate support
radii are sqrt(T^2-Delta y^2)/2 and sqrt(T^2-Delta x^2)/2. This follows from
ellipse semiaxes T/2 along Delta r and sqrt(T^2-|Delta r|^2)/2 orthogonal to it.
Together with a_t<=t<=b_t these give a containing rectangular box. Directed
square-root bounds and outward lattice rounding preserve containment.

Partition that box into equal cubes of side h=2^-16. Draw cells uniformly
with replacement. Conditional on the fixed geometry, each draw is iid in the
mathematical model. The implementation uses NumPy PCG64 with recorded seeds;
a finite seeded PRNG is not a proof of ideal independence or randomness.

Each rational endpoint is enclosed outward by integer lattice coordinates.
For a full cell, compute minimum/maximum temporal gaps and spatial squared
distances using integer interval arithmetic. It is wholly in the future cone
if its minimum temporal gap is positive and its square exceeds the maximum
spatial squared distance. It is certainly outside if the maximum positive
temporal gap cannot reach the minimum spatial distance. Otherwise mark it
uncertain. The past cone is analogous. All coordinate magnitudes are checked
below 10^7 lattice units, making the squared sums safe within int64.

Inner membership requires the whole cell inside both cones of the interval.
Outer membership allows any not-excluded cell. The inner union is a subset
of the true interval and the outer union contains it, up to null boundaries.
For intersections use inner_i AND inner_j, outer_i AND outer_j. For I_i minus
I_j use inner_i AND NOT outer_j and outer_i AND NOT inner_j. This counts
exclusive parts directly and avoids subtracting noisy integrals. Each union
has volume equal to its number of cells times h^3. Boundary uncertainty is
retained; it is not replaced by a floating-point point-in-cone decision.

## 3. Binomial numerical confidence bounds

For a region, the inner-hit count K_in and outer-hit count K_out each have
binomial marginal laws with n trials and probabilities p_in,p_out. They are
not independent of one another or of other region counts; no such assumption
is used. The true region-volume fraction lies in [p_in,p_out].

For K~Binomial(n,p), for every real t,

log E exp(tK)=n log(1+p(e^t-1))<=np(e^t-1).

Thus the same two-sided Chernoff bound as the prior Poisson construction
applies to lambda=np: P(d(K,lambda)>c)<=2 exp(-c). Its outward quadratic
inversion [L_c(K),U_c(K)] therefore contains lambda with at least this coverage.
At K=0 the upper endpoint c is valid because (1-p)^n<=exp(-np). Truncate the
probability interval to [0,1]. Consequently

box_volume * [L_c(K_in)/n, min(1,U_c(K_out)/n)]

contains the true volume whenever both scalar bounds cover. Multiply by rho
and the physical scale cubed to obtain an enclosure of the actual mean.
Background Chernoff/MGF method: Berkeley Data 140,
https://data140.org/textbook/content/chapter-19/chernoff-bound/ . The binomial
specialization and cell enclosure argument are given here in full.

Use c=24 at every predeclared sample stage n=2^20,2^22,2^24. The simultaneous
numerical family includes two geometries, three stages, inner/outer counts,
480*3 integrated constraints plus 74 analytic marginal controls:

M_num = 2 * 3 * 2 * (480*3+74) = 18,168.

A union bound gives numerical failure probability at most
2 M_num exp(-24) < 0.00000137173288800926. Shared samples, repeated endpoint
configurations and dependent regions do not invalidate the union bound.
Stopping at a declared stage is covered because every possible stage is in
the budget. Unused stages are still budgeted. Extending the budget would need
a new rule. A control failure or unresolved final enclosure yields HOLD.

This numerical guarantee is conditional on the already selected geometries
and observations and concerns only numerical integration. It is distinct
from PR90's >97.7715% repeated-measurement coverage for the confidence set.
Neither percentage is a posterior probability that a geometry is physical.
For a combined failure accounting under both ideal models, add the numerical
failure budget to the original measurement-set failure budget; do not equate
the two or claim independence is needed. Seeded replay verifies reproducibility,
not the ideal-randomness premise of the probability theorem.

## 4. What compatibility proves

For each actual mean, its entire numerical/analytic enclosure is compared
against its original confidence interval. Full containment gives INSIDE,
disjointness gives EXCLUDED, and partial overlap gives UNRESOLVED. Passing
all 8,177 constraints per geometry establishes membership in this particular
pairwise-overlap confidence set, subject to the numerical error event.

It does not establish compatibility with higher-order membership atom counts,
the entire original A/B causal set, or every statistic in the observation law.
It also does not show that the two laws are close in total variation or KL.
Pairwise overlap means determine covariances but not general higher-order
joint Poisson membership structure. A future statistical testing lower bound
requires its own experiment-specific argument.

On the numerical coverage event, both geometries now belong to the actual
pairwise-volume set, rather than merely its necessary mean-difference
relaxation. Their already exact weight separation remains 14.8212849855% in
symmetric relative l2 norm. For any single reported weight vector w_hat,
triangle inequality implies

max(||w_hat-w1||/||w1||,||w_hat-w2||/||w2||)
 >= ||w1-w2||/(||w1||+||w2||) > 0.0741064249.

This is a set-wise uniform recovery lower bound. It is not a statistical
minimax risk statement or failure probability. It excludes a uniform 5%
weight-error guarantee over this set but does **not** exclude 10%. The earlier
adversarial sign field is not automatically in the declared smooth C3 class,
so no smooth-field or continuum-error lower bound is inferred here.
