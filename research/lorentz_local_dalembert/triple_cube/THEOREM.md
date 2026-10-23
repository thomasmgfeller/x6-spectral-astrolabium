# Three independent support displacements: finite-budget uniform certificates

SPDX-License-Identifier: Apache-2.0

## Experiment and claim boundary

Keep the fixed rational 2+1 Minkowski reference, density 32768, scale, four
landmarks, root, outer diamond, 90 labelled observed count intervals, physical
minimum-norm quadratic-moment weights and admissibility gates of
`paired_surface/THEOREM.md`. Select nodes (15,17,5): retain the previous pair
and add the smallest support index not already selected. No search over third
nodes is performed. Independently displace them in boosted x by (u,v,w) in
[-1/10,1/10]^3, with boosted times and y fixed. Original-coordinate changes are
(-15s/8,17s/8,0) for the corresponding s. The other 18 points remain fixed.

The strong target requires unchanged selected-node order, the inherited
admissibility gates, symmetric physical weight gap >1/5, and full conditional
labelled count/overlap-law TV<=1/4 simultaneously. Uniform order contradiction,
weight-gap upper bound <=1/5 or TV lower bound >1/4 excludes this target.
HOLD means unresolved, not a counterexample. Volume fractions below refer to
this declared parameter cube, not a probability or an admissibility fraction.

## Exact geometry in three variables

Write s_15=u, s_17=v, s_5=w and other s_i=0. Lorentz invariance and fixed
boosted times give

    q_ij(s)=q_ij(0)-2(x_j-x_i)(s_j-s_i)-(s_j-s_i)^2.

For distinct i,j, the relative-displacement range on a box is exactly
[s_j,L-s_i,U, s_j,U-s_i,L]. The concave scalar quadratic reaches its extrema
at its two endpoints and its vertex if internal. This includes the mixed
terms 2uv, 2uw and 2vw for the three moving pairs. No sum of one-endpoint
ranges is substituted. Fixed boosted times preserve orientation whenever
q>0. A uniform sign contradiction excludes unchanged order; a box crossing
a sign boundary is not excluded for that reason.

For an observed interval, q>0 gives intensity rho scale^3 pi q^(3/2)/12.
Directed rational pi/square-root enclosures and the exact q extrema bound its
mean. These count statements hold on the unchanged-order subset, where the
relevant intervals remain in the fixed outer diamond.

## Joint rank-at-most-six operator update

Let D be the reference 9x16 moment matrix, H=I-11^T/17, S=DHD^T, Q=S^-1
and lambda=Qb. Let E select the three changed columns. The exact column
changes are U=[u p_15+u^2 r_15, v p_17+v^2 r_17, w p_5+w^2 r_5]. Put
V=DHE and K=E^THE=I_3-11^T/17. Direct expansion gives

    S(s)=S+VU^T+UV^T+UKU^T.

With L=[V,U], C=[[0,I],[I,K]] and C^-1=[[-K,I],[I,0]], define

    A(s)=C^-1+L^T Q L,  t(s)=L^T lambda.

A is a symmetric 6x6 polynomial matrix of total degree at most four.
The determinant identity det S(s)=det S det C det A(s) shows that an
invertible A certifies full moment rank. When eta=A^-1 t,

    lambda(s)=lambda-Q L eta,
    delta w=[(R_E-R_D QV) eta_V - R_D QU eta_U]/scale^2.

R_D and R_E are the centered moment/selector rows including the root row:
for supports subtract the column sum divided by 17, while the root row is
the negative column sum divided by 17. The lower block of A eta=t implies
eta_V=U^T lambda(s), which verifies the weight formula directly. This is one
joint update; the inverse couples all three parameters.

Center each box at its exact rational midpoint m and shift every monomial
exactly. Let R=A(m)^-1, eta0=R t(m),

    B(x)=-R[A(m+x)-A(m)],
    tau(x)=R[t(m+x)-A(m+x)eta0].

Both constant coefficients vanish exactly. Directed fixed-point interval
arithmetic encloses them throughout the centered box. If the upper row-sum
norm beta of B is below one, delta eta=tau+B delta eta yields an initial
uniform radius max|tau|/(1-beta). Twelve componentwise conservative radius
updates then bound delta eta. Substituting into the weight formula encloses
all 17 physical weight changes, including the root. If N bounds their norm
above, n0 bounds the reference norm below and n1 bounds the moved norm below,

    g = 2||w(s)-w(0)||/(||w(s)||+||w(0)||)
      <= min(2, 2N/(n0+n1)).

A bound <=1/5 excludes the target on the box. Failure to invert a midpoint or
to establish sufficient interval contraction stays HOLD_RANK_OR_ENCLOSURE.
It does not establish a singular geometry. Exact coefficient cancellation
precedes interval rounding; sampling is not used to certify a box.

## Safe transport from the completed two-support square

An event whose observed intervals use only nodes15/17 and fixed anchors has
unchanged event geometry and marginal law when node5 moves. Its TV lower
bound therefore transfers by data processing to the larger full law, even
though other observed counts change and may overlap it. An old whole-box
order contradiction also transfers if neither endpoint of its witness pair
is node5. No old weight-gap exclusion is transported away from w=0.

Extract only these eligible closed source rectangles from the complete
2,104-cell parent cover. On any target box, their clipped interiors are
disjoint. If their exact total intersection area equals the projection area,
their union covers the entire closed projection: a missing point in a finite
closed union would have a relative open neighborhood of positive area.
An independent audit also checks coverage by rational u slabs and interval
unions in v. Different source events may certify different subregions; one
common event for the whole projection is unnecessary. Node5 single-count
LAW strips from the earlier continuous-energy campaign transfer similarly
because their endpoints avoid nodes15/17.

The whole w=0 plane retains the previous full-square theorem, including old
gap certificates on that plane. A new HOLD box can contain such already
certified points. This measure-zero plane does not alter reported volumes.

## Bounded new Poisson events

After geometric classification, each selected HOLD box receives at most two
marginal events. Rank observed count intervals by squared separated mean
bounds divided by the sum of mean upper bounds; break ties by interval index.
Use the inherited exact Poisson threshold proposal and directed integer CDF
recurrence, retaining infinite tails. Precondition or rate/arithmetic-budget
failure does not trigger a replacement candidate. Exact identical inputs
may reuse one certificate, without creating independent replicates.

After that stage, each selected remaining HOLD receives one pair/anchor event.
Consider all three moving-node pairs and their common fixed anchors. Rank by
squared separation of difference-mean ranges divided by the sum of variance
upper bounds, then the ordered node pair and anchor index. Choose the integer
threshold as the floor of the midpoint of the difference-mean centers. Ranking
is only a proposal rule, not an optimal test or a TV estimate.

For A,B with a common anchor, D=N(A)-N(B)=N(A minus B)-N(B minus A). Only the
disjoint exclusive atoms are independent. The inherited virtual-tip
construction, using the present exact q ranges, bounds the common intensity
c below. The upper bound is min(aU,bU). Cover this entire enclosing interval
by 64 equal closed rational slices. On [l,u], the exclusive rates are enclosed
by [max(0,aL-u),aU-l] and [max(0,bL-u),bU-l]. Monotonicity of P(D<=k) in each
exclusive rate gives two corner bounds per slice. Their minimum lower and
maximum upper values enclose every possible c. No monotonicity in c, midpoint
substitution or independence of the original overlapping counts is assumed.
Infinite tails and uncertain normalization remain included. Budget failure
returns [0,1]. Event separation lower-bounds full-law TV uniformly.

## Fixed budget, freeze and validation

Start with an exact 8x8x8 grid of closed boxes. Classify in this order:
source projection, node5 law strips, whole-box order contradiction, joint
operator bound, otherwise HOLD. In each of two rounds, split at most 32 HOLD
parents, sorted by descending exact volume then numeric path, into eight
closed midpoint octants. Thus at most 1,024 geometric boxes are evaluated.
Then test at most 64 terminal HOLDs with two marginal events each, and at most
16 remaining HOLDs with one 64-slice pair event each, using the same box
priority. Stop without a post-result extension. Archive all parents, children,
split choices, events and remaining HOLDs. Structural octree reconstruction
proves complete coverage, including boundaries; volume sums supplement it.

The internal freeze precedes the first cube classification and new probability
evaluation. Prior PR118 evidence and six declared exact algebra controls are
known. This is not external preregistration. Controls compare the joint update
with direct nine-moment solves and Gram expansions, exact polynomial shifts,
all three mixed geometry terms and a non-additivity counterexample.

The audit reconstructs all 210 q ranges per evaluated box independently from
fixed times/y and spatial-distance extrema. It checks direct moment solves at
every finite-enclosure box center and the corners of the first eight such
boxes, exact transport dependencies and closed coverage, independent direct
100/110-digit Poisson PMFs, infinite-tail bookkeeping and all state transitions.
Point checks and decimal probabilities are diagnostics; exact uniform interval
and integer enclosures carry the exclusions. Missing-cell, missing-source,
missing-slice and wrong-cache controls supplement deterministic replay.
No general stability, arbitrary multi-support, full A-selection/B-graph
likelihood, continuum-accuracy or actual strong close-law-pair claim follows.
