# A full-law upper bound and a stopping theorem for homotheties

SPDX-License-Identifier: Apache-2.0

## Scope and geometry

This experiment is conditional on the selected 21-node order. Take geometry 0
of the exact PR88 witness, physical normalization scale fixed, and compare z
with sz at fixed known Poisson density rho=32768. Unknown absolute landmark
lengths are allowed; the selected-node order is known. A common Lorentz
transformation and translation may place the outer interval centrally in the
physical sampling diamond of duration 3/2. Its duration is about 1.35122 before
scaling. The exact checks ensure it still fits for every candidate considered.

The measurement channel is the 90 recorded B interval counts, their pairwise
overlap counts, and optionally the total B count in that fixed diamond. Neither
embedded point coordinates, the full B causal matrix, arbitrary new intervals,
metadata hashes, nor the probability of obtaining the A selection are included.
The result is not a lower bound for an experiment observing such extra data.
No assertion is made that the new pair belongs to the old realized confidence
set. Statistical two-point bounds do not require that membership.

All 90 intervals are contained in I(3,0), and I(3,0) itself is recorded. Thus
their union is exactly this outer interval. Write U for its expected count and
L for the fixed physical diamond's expected count. In 2+1 Minkowski geometry,

    U = rho*pi*tau³/12;  L = rho*pi*(3/2)³/12.

A dilation multiplies every nonempty interval-membership atom's volume by
a=s³. It preserves order, null-cone sign, the rank of the moment equations,
and all relative membership probabilities. If w is the unique minimum-norm
quadratic moment weight vector, then w_s=w/s²: the linear moment equations
remain zero and the quadratic moments remain the prescribed d'Alembertian
values. Multiplication by 1/s² maps the entire feasible set bijectively and
rescales its norm. The certificate independently solves both exact rational
systems, checks their equality, order and intrinsic conditioning gates.

## Reduction of the entire count channel

Poisson counts on disjoint membership atoms are independent. Conditional on
N_U, their relative counts are multinomial with probabilities invariant under
s. The count outside the union is independent. Therefore the entire observation
with total count can be generated from

    (N_U,N_out) ~ Poi(aU) x Poi(L-aU)

by a Markov kernel independent of s. Conversely, these two counts are available
as the recorded outer count and total minus outer count. The experiments are
statistically equivalent along this family. With total omitted, the experiment
is equivalent to N_U alone. In particular the two-count upper bound is valid
for both versions, regardless of the dependence among overlapping intervals.
This is an exact reduction, not a covariance approximation or independence
assumption on the 90 overlapping counts.

## Hellinger and total variation upper bound

For Poisson means lambda,mu, summing the power series gives affinity
exp(-(sqrt(lambda)-sqrt(mu))²/2). Independence multiplies affinities. Thus the
two-count affinity is exp(-J/2), where

    J = U*(sqrt(a)-1)² + (sqrt(L-aU)-sqrt(L-U))².

Cauchy-Schwarz applied to |sqrt(p)-sqrt(q)|*(sqrt(p)+sqrt(q)) gives
TV <= sqrt(1-affinity²) <= sqrt(J). Rationalizing differences yields the
cancellation-free upper bound used by the certificate, for s>=1 and L>aU:

    J <= U*(a-1)²/(sqrt(a)+1)²
         + (a-1)²*U²/[4*(L-aU)].

The implementation uses upper U, lower L and lower sqrt(a) in denominators,
then an upper rational square root. Directed pi and square-root enclosures
are inherited exact-integer routines. There is no Monte Carlo confidence
qualification or pseudorandomness assumption in this certificate. It remains
a statement within the stipulated Poisson model.

The frozen finite family is s=1+k/10^6 for k=1,...,1000. Select the largest
candidate whose proved TV upper bound is at most 1/4. Deterministic selection
using bounds valid for every candidate has no multiple-testing sampling cost.
This is a reproducibility contract, not externally timestamped preregistration.

## Statistical reconstruction lower bounds

Let D=||w-w_s|| and fix the common normalization ||w||. For any estimator,
turn its output into a nearest-target test. Test error implies estimation error
at least D/2. The optimal equal-prior testing error is (1-TV)/2. Hence

    max_g P_g(||w_hat-w_g|| >= D/2) >= (1-TV)/2.

A stronger direct expected-loss argument uses the common part min(p,q):
pointwise triangle inequality gives a sum of losses at least D, so

    max_g E_g ||w_hat-w_g|| / ||w||
        >= (D/||w||)*(1-TV)/2.

These hold for every estimator and therefore also after taking its infimum.
They are genuine conditional two-point statistical minimax bounds, unlike a
mere confidence-set diameter. They concern the discrete weight vector, not a
smooth-field response, continuum consistency or a prescribed physical sensor.

## Why this family cannot supply a close-law 10% counterexample

For w_s=w/s², the two closed 10%-relative-error balls are disjoint only if

    1-1/s² > 0.1*(1+1/s²), equivalently s²>11/9.

This implies s>11/10 and a>(11/10)³. Use just N_U and classify at the midpoint
of U and aU. Chebyshev bounds the sum of its two errors by

    4*(1+a)/[(a-1)²*U].

The function (1+a)/(a-1)² decreases for a>1. Substituting a=(11/10)³ and a
lower bound for U proves uniformly that every such feasible dilation has
TV >= 0.99597888586393723506 and attainable equal-prior accuracy at least
0.99798944293196861753. The range is nonempty: s=111/100 still fits the physical
diamond and has disjoint 10% balls. This is a stopping theorem for this
homothety family, not a stability theorem for arbitrary shape deformations.
Good binary discrimination also does not itself construct a uniform estimator.

## Reference

L. Leskela, *Information divergences and likelihood ratios of Poisson processes
and point patterns*, arXiv:2404.00294, https://arxiv.org/abs/2404.00294.
The Poisson affinity formula is a special case of the paper's information
divergence formulas. The finite-count proof, reduction, inequalities and
application above are provided here in full; no numerical claim is borrowed.
