# Fixed overlap refinement on the remaining three-support boxes

SPDX-License-Identifier: Apache-2.0

The experiment, reference, 960 closed terminal boxes and operator bounds are
inherited unchanged from `../triple_tail`. Nodes 15/17/5 move independently
in boosted x over [-1/10,1/10]^3 at one rational reference in 2+1 Minkowski
space. The strong target requires unchanged selected-node order, inherited
admissibility, symmetric physical weight gap>1/5 and full conditional labelled
count/overlap-law TV<=1/4. This is not the full A-selection/B-graph likelihood.

## Selection and stopping rule

The 78 source HOLD boxes comprise 15 without an overlap attempt and 63 with
unsuccessful 64-slice overlap events. In numeric octree-path order, give all 15
missing cases one highest-ranked inherited pair/common-anchor event with 64
closed overlap slices. Then refine every remaining HOLD, up to the fixed
maximum 78, once to 512 slices. Pair, anchor, side, threshold and geometry remain
identical for each refined event. There is no post-result candidate search,
geometric split, operator solve, second resolution increase or budget extension.
All failures remain HOLD. The internal freeze is before new probabilities,
after source results are known; it is not external preregistration.

## Uniform event bound

For two overlapping observed intervals A,B, write N(A)=C+U, N(B)=C+V using
independent Poisson counts on their disjoint atoms. The original counts are
dependent, while N(A)-N(B)=U-V cancels their common count. Uniform exact
geometry bounds give a in[aL,aU], b in[bL,bU] and common intensity
c in[cL,min(aU,bU)]. The positive common-intensity lower bound, when available,
comes from the inherited uniform virtual-tip subset construction. All relative
three-support geometry and its mixed terms are retained.

For every closed slice[l,u] of the full common-intensity range, the exclusive
means are enclosed by

    a-c in[max(0,aL-u),aU-l],
    b-c in[max(0,bL-u),bU-l].

These bounds may contain unattainable combinations, which is conservative.
Monotonicity of P(U-V<=k) in the two exclusive means gives opposite-corner
probability bounds. Directed integer Poisson normalization includes explicit
infinite-tail bounds. Take the minimum of lower endpoints and maximum of
upper endpoints across every slice. Budget failures give[0,1] and do not
yield an exclusion.

The 512-slice partition subdivides each 64-slice interval into eight closed
intervals. Each refined exclusive-mean rectangle is contained in its coarse
parent. This removes only over-enclosure introduced by the finite overlap
partition; the original marginal-mean rectangles and geometric uncertainty
remain. It need not resolve a HOLD box. Raw 512-slice bounds are stored rather
than silently intersected with old certificates; any widening, including
rounding effects or budget failure, is reported as such.

If reference and moved event probabilities lie in[pL,pU] and[qL,qU], then

    TV(full reference law,full moved law)>=max(0,pL-qU,qL-pU).

A lower bound>1/4 excludes the strong target throughout that box. No
independence between the original observed counts is assumed. The cache key
includes stage, slice resolution, pair, anchor, threshold and complete
statistics. Reuse of the same law is not independent evidence. Cache entries
from 64-slice and 512-slice runs cannot be substituted for one another.

## Audit, coverage and limitations

The audit reconstructs the source closed octree and replacement stages. Only
source HOLD records can be replaced, and only with exactly the same box. Thus
all 882 source exclusions and complete closed cube coverage persist. Rational
volume sums ignore shared boundaries only when computing volume; those
boundaries are still covered by the closed certificates. Volume is not
probability. The complete w=0 square theorem remains valid, including points
inside currently HOLD boxes.

Independent fixed-time/spatial-separation geometry checks validate intensity
rectangles and the virtual subset. A separate 110-digit direct PMF sum checks
the integer enclosures diagnostically. The audit verifies every overlap
slice, both cache lookups, unchanged event selection, fine/coarse geometric
nesting and all reported comparisons. Negative controls remove an input or
slice, use a wrong law or resolution, and check a dependent-count example.
Small positive means and zero rates are also checked independently. Complete
replay supplies reproducibility, not additional independent evidence.

Exact uniform interval and integer certificates carry the exclusions; decimal
and point checks are diagnostics. A low TV lower bound does not show that
laws are close. An operator upper bound above 1/5 does not show a strong actual
gap. No claim about arbitrary support motions, other references, physical
continuum accuracy or general stability follows from this fixed pass.
