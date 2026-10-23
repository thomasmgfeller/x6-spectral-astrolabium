# Continuous certificate for two coordinated supports

SPDX-License-Identifier: Apache-2.0

## Fixed family and statistical scope

Start from PR111's exact base, known density, fixed landmarks/root/outer diamond,
90 labeled interval counts and their overlaps. In the rational Lorentz-boosted
frame, node 15 moves by v*h in x, v=250000000000/264451347681, and node 5 by -h.
Their boosted times and y coordinates are fixed. The closed domain is
h in [-1/10,1/10]. Its positive and negative halves equal PR111 rays 1 and 0.
No new base geometry or optimization of velocities is introduced.

The target remains the minimum-norm physical quadratic-moment weight vector,
and the excluded conjunction is unchanged order, symmetric relative weight gap
strictly above 1/5, and full conditional count/overlap-law TV at most 1/4.
This is neither the full A/B-data likelihood nor a physical continuum statement.

## 1. Joint movement of both boundaries

For every pair i,j let v_i,v_j be their boosted spatial velocities (zero on all
other nodes), dx=x_j-x_i, and q0 the reference squared proper time. Exactly,

    q_ij(h) = q0 - 2*dx*(v_j-v_i)*h - (v_j-v_i)^2*h^2.

In particular the two moved endpoints use their relative velocity; treating
this interval as two independent one-endpoint perturbations would lose the
cross term. Evaluate a quadratic at the two cell endpoints and at its vertex
when internal to obtain its exact range. Fixed boosted time ordering gives the
causal orientation whenever q is positive. A complete cell is order-excluded
only when one required sign of q is impossible throughout it. Boundary-null
configurations fail the inherited non-null admissibility conditions as well.

All observed intervals have one fixed endpoint at most one moving endpoint.
Their Poisson means are C*q^(3/2), C=rho*scale^3*pi/12. Directed rational square
roots and pi bounds produce uniform mean enclosures on a cell. Marginalization
transfers any one-count event lower bound to the full observation law without
requiring independence between overlapping counts.

## 2. A rank-four exact moment update

Let D be the reference 9-by-16 moment matrix, H=I-11^T/17, S=D H D^T,
Q=S^-1, b=(0,0,0,-2,2,2,0,0,0)^T and lambda=Qb. The reference is full rank.
Let E be the 16-by-2 selector for the two moved support columns. Their moment
changes form U(h), a 9-by-2 matrix polynomial of degree two, and D(h)=D+U E^T.
Put V=D H E, K=E^T H E. Direct multiplication gives

    S(h) = S + V U^T + U V^T + U K U^T.

For W=[V,U] and C=[[0,I],[I,K]], C^-1=[[-K,I],[I,0]]. Define

    M(h) = C^-1 + W^T Q W,
    t(h) = W^T lambda.

M is a symmetric 4-by-4 matrix polynomial of degree at most four. Whenever
M is invertible, the Woodbury identity gives

    eta=M^-1 t, lambda(h)=lambda-Q W eta.

The determinant lemma gives det S(h)=det S * det C * det M, so verified
invertibility of M certifies moment rank throughout the cell, not only at its
midpoint. Conversely a singular M midpoint is kept unresolved by this method.

Include the root weight through R_D with root row -sum(D_columns)/17 and support
rows D_column-sum(D_columns)/17; define R_E analogously from E. Partition eta
as (eta_V,eta_U). The lower two equations of M eta=t imply U^T lambda(h)=eta_V.
Therefore the exact physical weight change is

    delta w(h) = [(R_E-R_D Q V)*eta_V - R_D Q U(h)*eta_U]/scale^2.

This formula includes the interaction of the two changing columns. It does not
sum previously bounded single-support weight changes.

## 3. Certified solve on a whole cell

For a cell [a,d], take its exact midpoint m and write s=h-m. Compute all shifted
polynomial coefficients exactly before interval evaluation. Let R=M(m)^-1 and
eta0=R t(m). Put

    E(s)=-R*(M(m+s)-M(m)),
    tau(s)=R*(t(m+s)-M(m+s)*eta0).

Both have zero constant coefficient. For delta=eta-eta0 we have
delta=tau+E delta. Directed fixed-point interval arithmetic bounds every entry.
If max_i sum_j sup|E_ij| < 1, the Neumann series proves invertibility uniformly
and gives an initial infinity radius sup||tau||/(1-sup||E||). Componentwise
iterations r_i <- min(r_i, sup|tau_i|+sum_j sup|E_ij|*r_j) remain valid radii.
Failure of this sufficient contraction test is HOLD, not a singularity claim.

Substitute eta0+delta into the exact weight-change polynomial. Its interval
enclosure yields N>=||delta w|| and n1<=||w+delta w||. With certified n0<=||w||,

    symmetric relative gap <= min(2, 2*N/(n0+n1)).

Thus a cell with gap upper at most 1/5 cannot contain a strong counterexample.
All square roots and interval operations use directed bounds. Exact rational
midpoint solves only propose centers; the Neumann residual certifies all h.

## 4. The joint event extends to intervals

Use PR111's unchanged event E={Y-2X<=891}, with X=N(I(2,5)) and Y=N(I(5,1)).
At every h for which these two intervals are timelike, the first lies strictly
before tip 5 and the second strictly after it. The two regions are disjoint
under each geometry, so their counts have the exact product Poisson law.

The probability is increasing in the X mean and decreasing in the Y mean.
Uniform mean enclosures therefore bound P_h(E) on an entire h-cell, including
the focus neighborhood [9/200,11/200]. Separation from the reference event
probability lower-bounds TV of the full observed count/overlap law. No other
interval counts are factored. The inherited numerical routine retains both
infinite Poisson tails and directed integer normalization.

## 5. Coverage is part of the certificate

Start with 64 equal closed cells covering [-1/10,1/10]. Split only unresolved
cells at exact midpoints, with the fixed eight-round/32-parent budget and
deterministic priority. The archive retains parents, children and split history.
Terminal intervals must meet exactly, with the declared outer endpoints.
Each terminal cell has one valid whole-cell exclusion or remains HOLD.
Consequently a cover with no HOLD excludes the entire declared one-dimensional
family. Shared cell endpoints are covered too. No inference is made about the
other 58 paired rays, arbitrary directions or general finite-noise stability.

## Provenance

The algebra above is derived here. Inputs and probability bounds are pinned to
[PR111](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/111),
[the paired point experiment](../coordinated_motions/THEOREM.md), and
[the preceding joint-event certificate](../coordinated_motions/JOINT_NOTE.md).
The internal contract freeze precedes this continuous run; earlier point results
were known. It is not external preregistration or independent peer review.
