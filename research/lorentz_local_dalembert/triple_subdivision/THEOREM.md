# One octree subdivision of the remaining three-support region

SPDX-License-Identifier: Apache-2.0

The reference, conditional labelled count/overlap experiment, physical
minimum-norm operator and admissibility conditions are inherited from
`../triple_overlap_refinement`. Nodes 15,17,5 move independently in boosted x
over [-1/10,1/10]^3 in 2+1 Minkowski space; the other 18 selected nodes remain
fixed. The strong target is unchanged selected-node order, inherited
admissibility, symmetric physical operator-weight gap>1/5 and full-law
TV<=1/4 simultaneously. This is not the full A-selection/B-graph likelihood.

## Fixed selection and budgets

Split every one of the 56 source HOLD boxes exactly once at all three rational
midpoints. Evaluate all 448 closed children in numeric octree-path order.
Keep all 904 source exclusions unchanged. There is no second splitting round.
For each child use the inherited sequence: safe source-square projection,
node 5 count-law strips, uniform order contradiction, then joint operator
enclosure. Every remaining child receives at most two inherited geometry-ranked
marginal events, stopping at first success. Every remaining failure receives
exactly one highest-ranked pair/common-anchor difference event with 512 closed
overlap intervals. Both event-stage cell budgets are 448, so neither truncates
the remaining inputs. No event retuning, additional pair, new resolution or
post-result budget extension is allowed. Failures remain HOLD.

The contract, implementation, audit and source evidence are internally frozen
before the first child classification or probability evaluation. Source results
are known. This is not external preregistration. Reused cached certificates
are not independent replications.

## Geometry and joint operator bound

For independent boosted-x displacements s_i, the exact interval polynomial is

    q_ij = q_ij(0) - 2 dx_ij (s_j-s_i) - (s_j-s_i)^2.

Its exact box range is obtained from the relative-displacement endpoints and
the concave quadratic vertex. All mixed pair terms are retained. Fixed boosted
time and transverse coordinates determine time orientation. Only a uniform
sign contradiction with the reference order excludes a whole box; a possibly
changed order remains unresolved at that gate.

The inherited joint rank-at-most-six formula changes the three moment columns
simultaneously. With D the 9x16 moment matrix, H=I-11^T/17, Q=(DHD^T)^-1,
V=DHE, U the three changed columns and K=E^T HE,

    D' H D'^T = D H D^T + V U^T + U V^T + U K U^T.

The six-dimensional polynomial update and its inverse include all cross terms;
summing independent one-support weight changes would be incorrect. The
inherited fixed-point Neumann enclosure with 12 radius refinements bounds
every physical weight change throughout each child. A symmetric gap upper
bound<=1/5 excludes the strong target. An upper bound>1/5 does not prove a
strong actual gap. Rank or enclosure failure remains HOLD. Complete algebra
and the uniform bound are derived in `../triple_cube/THEOREM.md`.

Only source-square count-law/order witnesses whose endpoints avoid node 5
are projected. Old two-dimensional operator-gap exclusions are not transported
off w=0. Node5 strips use only node 5 and fixed-anchor counts. Closed rational
projection and strip covers are checked independently. The full w=0 square
theorem remains valid, even inside a HOLD child.

## Count-law bounds and closed coverage

Exact geometric intensity rectangles and directed Poisson CDF sums give
uniform marginal-event intervals. For overlapping intervals A,B, decompose
N(A)=C+U and N(B)=C+V into independent Poisson counts on disjoint atoms;
then N(A)-N(B)=U-V. The original observed counts are dependent. The inherited
uniform virtual-tip subset bounds their common intensity from below.
The full allowed common-intensity range is covered by 512 closed slices;
opposite-corner monotonicity bounds each exclusive-mean rectangle. Infinite
Poisson tails are included. Budget failures return [0,1] and cannot exclude.
Details are in `../triple_tail/THEOREM.md`.

For reference and moved event intervals [pL,pU], [qL,qU],

    TV(full reference law,full moved law)>=max(0,pL-qU,qL-pU).

A bound>1/4 excludes the target throughout the child. Cache keys contain the
labelled event and all statistics; reference and moved lookups are checked.
All new overlap laws use the same fixed 512-slice contract.

The eight closed children exactly cover each parent with disjoint interiors;
faces remain included in the adjacent certificates. Replacing 56 leaves with
448 yields 1352 terminal boxes, retaining all 904 source exclusions. Exact
rational volumes sum to the same 1/125 cube volume. Volume fractions are not
probabilities and a HOLD box is not a counterexample.

The independent audit reconstructs the source tree and all child boxes, checks
all 210 pairwise interval ranges per child, direct nine-moment weight solves
at every finite-enclosure center and all eight corners of the first eight
such children, exact cover and cache identities, and independent 100/110-digit
PMFs. Missing-child/input/slice, wrong-cache, small-mean, zero-rate and
dependence controls are included. Point and decimal checks are diagnostics;
uniform exact interval/integer certificates carry the exclusions. Full replay
adds reproducibility, not independent evidence. Arbitrary support motions,
other references, continuum accuracy and general stability remain open.
