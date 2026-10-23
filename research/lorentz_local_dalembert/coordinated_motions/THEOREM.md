# Coordinated motions: what can actually cancel?

SPDX-License-Identifier: Apache-2.0

## Scope and observation map

Keep the inherited 2+1-dimensional Minkowski experiment, known positive density,
fixed scale, outer diamond and labeled selected-node order. Nodes 0..3 are fixed
nondegenerate landmarks, node 4 the fixed root, and nodes 5..20 movable supports.
The actual 90-count mask contains all 10 pairs among the five fixed nodes and
all 80 support/fixed-node pairs. There are no support/support count intervals
in this mask. The selected-node order still contains their causal relations.
Counts may be correlated; none of the arguments below treats them as independent.

Put G=diag(1,-1,-1), q_a(x)=(x-l_a)^T G (x-l_a)>0, and
mu_a(x)=C q_a(x)^(3/2), C=rho*scale^3*pi/12. All observed intervals here are
timelike. The 90-dimensional mean vector, after a fixed row permutation, has
one constant block and 16 five-dimensional blocks, each depending on only one
support. Cross-support overlaps can depend on several supports, but cannot
remove information already present in an individually observed count.

## Proposition 1: exact finite noncancellation

With the four landmarks fixed and affinely independent, equality of the labeled
count mean vector for two admissible support configurations implies equality of
every support coordinate. The same conclusion holds if their full count laws
are equal.

Proof. Equality of each mean implies equality of q, since C>0 and q>0. For
d=x'-x, direct expansion, with no small-displacement remainder, gives

    Delta q_a - Delta q_0 = -2 (l_a-l_0)^T G d,  a=1,2,3.

Let A have rows -2(l_a-l_0)^T G. Affine independence and invertibility of G imply
det(A)!=0. Therefore d=A^-1(Delta q_a-Delta q_0)_{a=1}^3, which is zero when
all these q values agree. This applies separately to every support. Equality
of the full laws implies equality of their finite marginal expectations. QED.

The exact rational A, inverse and nonzero determinant are archived in
structure.json. The argument also gives the finite geometric bound

    ||d||_infinity <= 2 ||A^-1||_infinity max_{a=0..3}|Delta q_a|.

It is a coordinate bound in the declared frame, not an operator-accuracy bound.
The landmark inverse can be poorly conditioned; changes in operator weights
also depend on moment-system conditioning.

## Proposition 2: no hidden first-order mean-preserving motion

The derivative of the full mean map with respect to the 48 support coordinates
has rank 48 at every admissible geometry in this fixed-landmark setting.

Proof. dmu_a=(3C/2)*sqrt(q_a)*dq_a, with strictly positive multipliers. In each
support block, differences of the q-gradient rows give the three rows of A.
Those span R^3, so that block has column rank three. The 16 blocks have disjoint
column supports, yielding total rank 16*3=48. No numerical SVD or tolerance is
used to infer rank. A derivative of a scalar aggregate can nonetheless vanish:
one equation on many velocities is much weaker than 90 labeled equations. QED.

These propositions specialize the previously known fixed-landmark
identifiability argument to coordinated motions. They are not a new global
stability theorem, and do not rule out approximately indistinguishable pairs.
Moving landmarks, changing labels or discarding individual counts would change
the hypotheses and requires a separate analysis.

## Proposition 3: a marginal obstruction survives other support motions

For any support i and fixed anchor a, the marginal law of the observed count
is Poisson(mu_a(x_i)); it is unaffected by movements of any other support.
Consequently, for every simultaneous admissible deformation,

    TV(P_full,P'_full) >= TV(Poi(mu_a(x_i)),Poi(mu_a(x'_i))).

Proof. For every marginal event E, its inverse image under the coordinate
projection is a full-observation event. Taking suprema gives the inequality.
The interval itself has endpoints a and i only, so other endpoint movements
do not change its volume. No assertion of independence is needed. QED.

This also applies to any subvector involving only fixed nodes and support i.
In particular PR110's two counts I(2,15), I(15,1) remain geometrically disjoint.
If node 15 follows that same negative boosted-x segment h in [45/1024,51/1024],
arbitrary additional support movements preserving the experimental hypotheses
cannot evade the inherited full-law lower bound 0.26376136265637454647.
This is a continuous exclusion for that cylinder of configurations, regardless
of their operator gap. It does not extend PR109's gap-based cells: several small
weight changes could jointly exceed the original 20% gate.

## The fixed paired search

For each of the other 15 supports j and each boosted spatial axis, couple its
motion to node 15. For the count to anchor 0 its derivative with respect to an
axis displacement is 3C*g_i, g_i=(l_0_axis-x_i_axis)*sqrt(q_0(x_i)).
The ideal coefficient c=-g_15/g_j cancels the derivative of the scalar sum
mu_0(x_15)+mu_0(x_j). Use a directed square-root enclosure, round its ratio to
a rational multiple of 1e-12, and normalize the largest speed to one. Retain
both signs. A certified residual bound records the rounding error; exact
cancellation of this scalar derivative is not claimed. At finite h, nonlinear
terms remain, even for the ideal coefficient. This is an intentionally favorable
test of one aggregate-cancellation mechanism, not an optimization over all laws.

The contract fixes 60 rays and seven steps, hence 420 points. Exact causal order,
minimum separation and rational moment rank are tested. Candidates at or below
20% symmetric weight gap cannot meet the strong-pair target. Strong candidates
also receive the existing intrinsic conditioning checks. Their individual
Poisson counts are screened with directed Hellinger lower bounds and, when
needed, at most two inherited certified Poisson CDF events. Every unresolved
case remains HOLD; the screening never establishes full-law closeness.

For a single Poisson count, the affinity is
exp(-(sqrt(mu)-sqrt(nu))^2/2), by direct summation of its PMF series. Since
min(p,q)<=sqrt(pq), TV=1-sum min(p,q)>=1-affinity. A fixed CDF event difference
is another lower bound. Both remain full-law lower bounds under projection.
The code retains the infinite Poisson tail and uses directed integer arithmetic.

## What remains open

Approximate joint-law cancellation or smoothing can still matter. A valid
positive closeness certificate must control the entire dependent observation
law, for example through all membership-atom intensities including unresolved
mass. Equality or near equality of one sum, marginal means, or a fitted Gaussian
surrogate is insufficient. The general finite-error operator modulus remains
open. The present finite search is not continuous coverage of its 60 rays.

## Sources

- Inherited exact experiment and mathematical definitions:
  [PR110](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/110),
  [fixed-landmark identifiability](../stability_information/THEORY.md),
  [joint membership atoms](../joint_atoms/THEORY.md), and
  [joint-event certificate](../joint_ray_obstruction/THEOREM.md).
- L. Leskela, *Information divergences and likelihood ratios of Poisson
  processes and point patterns*, IEEE TIT 70(12), 9084-9101 (2024),
  DOI 10.1109/TIT.2024.3472448,
  https://arxiv.org/abs/2404.00294 . The finite Poisson affinity argument used
  here is derived above; the paper does not establish our geometry or operator
  conclusions. No independence of overlapping interval counts is borrowed.
