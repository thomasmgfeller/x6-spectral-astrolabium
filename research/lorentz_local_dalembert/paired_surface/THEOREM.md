# Two independently displaced supports: certified rectangle exclusions

SPDX-License-Identifier: Apache-2.0

## Domain and precise question

Keep the inherited reference geometry, density, fixed landmarks/root/outer
diamond, and conditional labelled Poisson count/overlap experiment. Move node
15 by u and node 17 by v in boosted x, keeping boosted times and y fixed:
(u,v) in [-1/10,1/10]^2. Their original-coordinate changes are
(-15u/8,17u/8,0) and (-15v/8,17v/8,0). Unlike the preceding ray, v is not fixed
to a multiple of u. The earlier line45 v=-(292553733423/500000000000)u lies
inside this square, but its certificate alone does not cover the square.

A strong close-law pair would preserve the selected-node order, have symmetric
physical minimum-norm quadratic-moment weight gap >1/5, and full conditional
count/overlap-law TV<=1/4. Each exclusion proves at least one of these three
conditions impossible on its whole rectangle (under the inherited non-null
admissibility conditions). Other inherited admissibility gates can only
further restrict candidates. HOLD is a lack of proof, not such a pair.

## 1. Exact rectangle geometry

Let s_15=u, s_17=v, and other s_i=0. With fixed boosted coordinates,

    q_ij(u,v)=q_ij(0,0)-2(x_j-x_i)(s_j-s_i)-(s_j-s_i)^2.

For distinct i,j the attainable relative displacement interval is exactly
[s_j_lower-s_i_upper, s_j_upper-s_i_lower]. Evaluating the scalar concave
quadratic at both endpoints and its vertex (if internal) gives its exact
rectangle range. In particular q_15,17 includes the mixed term 2uv. It is not
obtained by adding two independent one-endpoint changes. Fixed boosted time
ordering preserves orientation when q>0. A sign contradiction throughout the
rectangle excludes unchanged order; rectangles crossing a sign boundary are
not automatically excluded.

Observed interval intensities have one fixed anchor and at most one moving
support. Their means are C q^(3/2), with C=rho scale^3 pi/12. Rational directed
pi/square-root bounds and exact q extrema give whole-rectangle mean bounds.
These statements apply to the unchanged-order subset, on which the observed
intervals remain inside the fixed outer diamond.

## 2. Exact rank-four operator update in two variables

Let D be the reference 9x16 moment matrix, H=I-11^T/17, S=D H D^T,
Q=S^-1 and lambda=Qb. Select the two changed columns by E. Their changes form
U=[u p_15+u^2 r_15, v p_17+v^2 r_17]. Set V=DHE and K=E^THE. Direct expansion
and the invertible block C=[[0,I],[I,K]] give

    S(u,v)=S+VU^T+UV^T+UKU^T,
    M(u,v)=[[-K,I],[I,0]]+[V,U]^T Q [V,U],
    t(u,v)=[V,U]^T lambda.

M is a symmetric 4x4 polynomial of total degree at most four; mixed monomials
are retained. Where M is invertible, eta=M^-1 t and the exact physical weight
change, including the root weight, is

    delta w=[(R_E-R_D QV) eta_V - R_D QU eta_U]/scale^2.

Here R_D and R_E center the support rows and include the negative column-sum
root row, as in the inherited paired-continuous proof. The determinant lemma
makes invertibility of M equivalent to moment rank for the changed geometry.
The formula is one joint update, not a sum of single-support weight bounds.

Center each rectangle at its exact rational midpoint (m,n) and shift all
polynomial coefficients exactly. With R=M(m,n)^-1 and eta0=R t(m,n), define

    E(x,y)=-R[M(m+x,n+y)-M(m,n)],
    tau(x,y)=R[t(m+x,n+y)-M(m+x,n+y)eta0].

Both have zero constant coefficient. Directed fixed-point interval evaluation
on the centered rectangle bounds all entries. If the supremum row-sum norm of
E is below one, delta eta=tau+E delta eta gives a uniform Neumann bound and
certifies rank throughout the rectangle. Twelve componentwise radius
refinements remain conservative. Substitution in the weight-change polynomial
gives N>=||delta w|| and n1<=||w+delta w||, hence

    symmetric gap <= min(2,2N/(n0+n1)), n0<=||w||.

A bound <=1/5 excludes a strong pair. Failure of the sufficient contraction
condition remains unresolved; it is not a singularity claim. All coefficient
cancellations occur in exact fractions before interval rounding.

## 3. Transport of earlier count-law exclusions

A previous one-support event using only intervals between that support and
fixed anchors has the same marginal distribution when the other support moves.
Therefore its TV lower bound transfers pointwise to the full current law.
No joint independence of other observed counts is needed. This applies to
145 archived source strips assembled from continuous-energy single-count
certificates and two node-15 disjoint past/future joint events. Only LAW
exclusions transfer; previous one-support GAP exclusions do not.

A rectangle projection may be covered by a union of certified strips. Their
events may differ: at each parameter point at least one source lower bound
applies, so the minimum source TV bound remains uniform. Exact endpoint
coverage and unchanged event geometry are checked. This does not require one
common event for the entire rectangle.

## 4. New law tests and overlap dependence

For common-anchor intervals A,B, the inherited virtual-tip construction uses
our two-dimensional exact q bounds to place a smaller interval in A intersect
B uniformly. With dt the fixed support time separation and qmin their squared
interval lower bound, a nonnegative delay bounded by
sqrt(dt^2-qmin)-dt suffices. Moving the later tip forward (future anchor) or the
earlier tip backward (past anchor) yields the subset. Its q lower bound is
q_tip,anchor,min - 2 duration delay + delay^2 when delay<duration and this is
positive; otherwise the common-intensity lower bound is zero.

Thus Var[N(A)-N(B)] <= aU+bU-2cL. The inherited integer-threshold Cantelli event
and marginal Hellinger tests yield whole-rectangle full-law lower bounds.
Fixed-budget exact marginal CDF tests use the same mean rectangles and
infinite-tail-preserving directed PMF machinery as previous certificates.

For the final bounded overlap stage, D=N(A)-N(B)=U-V with independent disjoint
exclusive atoms U~Pois(a-c), V~Pois(b-c). The common c is not fixed or assumed
known. Cover its entire feasible enclosing interval [cL,min(aU,bU)] by 64
closed rational slices. Each slice encloses a-c and b-c in a rectangle. The
CDF event D<=k is decreasing in the U mean and increasing in the V mean, so
two monotone corners bound it. The minimum lower and maximum upper bound over
all slices bound the unknown overlap law. No monotonicity in c is assumed.
Reference/moved event separation lower-bounds the full observation-law TV.
The frozen routine returns [0,1] on rate/support/precision budget failure.

## 5. Coverage, budgets and reporting

The 32x32 initial grid exactly covers the closed square. In each of at most
three rounds, split at most 128 HOLD parents, ordered by descending area then
numeric path, into their four exact closed midpoint quadrants. Archive parents,
children and split history. Reconstructing this tree proves coverage; area
sums alone are not a coverage proof. Shared boundaries remain included.

After geometric/transport/Cantelli/Hellinger classification, try at most two
exact marginal events on the first 128 terminal HOLD rectangles by the same
priority. Then try one highest-ranked common-anchor overlap event on at most
32 remaining HOLD rectangles. Ranking uses squared mean separation divided by
a variance upper bound; overlap k is the floor of the midpoint of the two
mean-interval centers. These are proposal rules, not optimality claims.

No extra refinement, threshold sweep or budget extension follows evaluation.
Every unsuccessful or untested terminal rectangle remains explicitly HOLD.
Area fractions refer to the chosen (u,v) parameter square, not to probabilities,
physical frequencies, or the fraction of admissible geometries. Even zero
HOLD would settle only this square from this reference, not arbitrary spatial
axes, more supports, other references or a general stability theorem.

## Freeze and checks

The contract, scientific algorithms, proof and input sources are internally
hashed before the first rectangle classification. Historical PR115 evidence
and exact algebra controls at three points are known; no gap or law scan on
the new domain precedes the freeze. This is not external preregistration.
The independent audit checks direct nine-moment solves, two-variable mixed
terms, causal subset inequalities, probability expressions, transported event
geometry and complete tree coverage. It does not replace whole-cell proofs
with samples. No full A-selection/B-graph likelihood or continuum claim is made.
