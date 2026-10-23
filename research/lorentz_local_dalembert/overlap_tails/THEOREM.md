# Uniform Poisson difference events with unknown overlap

SPDX-License-Identifier: Apache-2.0

## Experiment and claim

Use the inherited conditional Poisson experiment, fixed outer diamond, fixed reference geometry and the 60 frozen signed paired rays. The observed labels include both intervals from the moving nodes to each common fixed anchor. This stage only replaces the 38 HOLD cells from `paired_tail`; it does not change the reference, ray coefficients, order condition, symmetric weight-gap gate (>1/5), or full labelled count/overlap-law TV gate (<=1/4).

All geometric statements below are restricted to configurations preserving the inherited selected-node order. Counts then have the stated interval intensities within the fixed outer diamond. No independence of overlapping observed counts is assumed. This is not a full A-selection or B-graph likelihood statement.

## Exact cancellation of the shared atom

For two observed intervals A,B, write a=mu(A), b=mu(B), c=mu(A intersect B). Poisson increments on disjoint sets give independent variables

    U=N(A minus B) ~ Poisson(a-c), V=N(B minus A) ~ Poisson(b-c).

The observed statistic D=N(A)-N(B)=U-V exactly cancels the shared count. Independence applies to U,V, not to N(A),N(B). The distribution of D still depends on c through its two exclusive intensities.

For a whole displacement cell, inherited exact quadratic extrema, rational square-root and pi enclosures provide a in [aL,aU], b in [bL,bU]. The future/past virtual-tip construction in `paired_family/THEOREM.md` provides L<=c by placing an interval inside A intersect B throughout the cell. Also c<=min(a,b)<=U0=min(aU,bU).

Partition the ENTIRE interval [L,U0] into 64 equal closed rational slices. For a slice [l,u], every feasible pair of exclusive means belongs to

    a-c in [max(0,aL-u), aU-l],
    b-c in [max(0,bL-u), bU-l].

The rectangles may contain infeasible combinations; enlarging the feasible set is conservative. Shared slice boundaries are harmless. If L=U0, repeated degenerate slices are harmless.

## Uniform event probability

For integer k, the event E={U-V<=k} is decreasing in U and increasing in V. Coupling Poisson variables by independent nonnegative increments proves these monotonicities. Therefore on each exclusive-rate rectangle its lower bound is computed at (V_lower,U_upper), and its upper bound at (V_upper,U_lower).

The inherited `joint_ray_obstruction/jr_run.py` evaluates these independent-atom probabilities by directed integer relative-PMF recurrences about the mode. Finite sums include rigorous infinite-tail bounds in both normalization and omitted event mass. The frozen 80-digit grid and support/width budgets either return certified bounds or a [0,1] HOLD enclosure. No floating point or truncated-tail approximation enters a certificate.

The minimum of all slice lower bounds and maximum of all slice upper bounds enclose P(E) uniformly over the original cell. In particular, this construction assumes NO monotonicity in c, performs NO midpoint substitution for c, and discards NO unknown-overlap region.

Let reference and moved event enclosures be [pL,pU], [qL,qU], both computed with the same anchor, difference sign and integer threshold. Then

    TV(full reference law, full moved law)
      >= |P(E)-Q(E)| >= max(0,pL-qU,qL-pU).

The event is measurable in the already observed labelled counts. Extra overlap labels or total-count observations cannot weaken this lower bound. A lower bound strictly greater than 1/4 excludes the strong-gap/close-law conjunction throughout this cell, regardless of its weight gap. All output decimal bounds are rounded outward.

## Frozen selection and stop

For each of the inherited 38 cells, rank common-anchor statistics by exact squared mean separation divided by the sum of the inherited variance upper bounds, breaking ties by anchor index. Choose the integer threshold as the floor of the midpoint of the two mean-interval centers. Try at most the first two anchors and stop on the first certified TV>1/4. These are deterministic proposal rules, not optimality claims. Each analytic enclosure is uniform independently of proposal selection; no empirical multiple-testing inference is used.

No new displacement subdivision, threshold retuning, overlap-slice adaptation or extra anchor search follows evaluation. A budget failure or an insufficient lower bound remains HOLD. Combined coverage is obtained by replacing precisely the old HOLD cells in the inherited complete covers; independent auditing reconstructs all 30 lines, hence 60 signed rays, including the separately certified node-15/node-5 x line.

This theorem justifies the certificate method, not an anticipated numerical outcome. Even complete exclusion would apply only to these 30 one-dimensional fixed-base paired lines with h in [-0.1,0.1]. Arbitrary two-support deformations, motions of three or more supports, other reference geometries, global operator stability and continuum accuracy remain outside this result.
