# Bounded refinement of the remaining paired-surface overlap laws

SPDX-License-Identifier: Apache-2.0

## Fixed experiment and target

All geometry, observed intervals, physical operator weights and admissibility
gates are inherited from `paired_surface/THEOREM.md`. The only moving supports
are nodes 15 and 17, independently displaced in boosted x by u,v in
[-1/10,1/10]. The other 19 labelled nodes stay fixed. This is one rational
reference in 2+1 Minkowski space, not an arbitrary support configuration.

The target conjunction is unchanged selected-node order, the inherited
admissibility conditions, symmetric physical operator-weight gap >1/5, and
full conditional labelled count/overlap-law total variation <=1/4. An order
contradiction, a uniform weight-gap upper bound <=1/5, or a uniform full-law
TV lower bound >1/4 excludes it. The implication is conditional on the
declared count experiment, not on a full A-selection/B-graph likelihood.

`surface_tail` leaves 31 rectangles of area 1/409600 each. Sixteen lack an
overlap event; fifteen have one unsuccessful 64-slice event. The latter have
common-intensity slice widths about 3.4, which widen both exclusive-rate
enclosures. This motivates refining that nuisance-parameter cover. It does
not prove in advance that refinement will exclude any rectangle.

## Event and uniform bound

For two observed intervals A,B sharing a fixed anchor, write

    D = N(A)-N(B) = N(A minus B)-N(B minus A).

Only the two disjoint exclusive atoms are independent Poisson variables. With
interval means a,b and unknown common intensity c, their means are a-c,b-c.
The inherited exact virtual-tip construction supplies a uniform lower bound
cL, while cU=min(aU,bU). Both mean ranges and the lower overlap bound hold
over the whole closed parameter rectangle, on the unchanged-order subset.

Partition [cL,cU] into n equal closed rational slices. On a slice [l,u], use

    positive rate in [max(0,aL-u),aU-l],
    negative rate in [max(0,bL-u),bU-l].

The probability of D<=k decreases with its positive rate and increases with
its negative rate. Two corner evaluations enclose it on each slice; taking
the minimum lower and maximum upper bounds over all slices is valid for
every possible c. No monotonicity in c, plug-in overlap estimate, or
independence of the original overlapping counts is assumed.

Directed integer Poisson recurrences retain normalization uncertainty and
infinite tails. Failed rate/support/precision budgets give [0,1] and HOLD.
If the reference and moved event-probability enclosures have separation
greater than 1/4, data processing yields full-law TV>1/4. This is a deterministic
uniform event certificate, not a fitted or repeatedly sampled hypothesis test.

The 512-slice cover is an eightfold rational subdivision of the 64-slice
cover. Every fine exclusive-rate rectangle is contained in its coarse parent.
This removes some interval over-enclosure without changing the physical
experiment, admissible nuisance interval or event. Finite arithmetic still
uses outward enclosures; a finer cover need not produce an exclusion.

## Frozen selection and stop

First apply one inherited best-anchor event with 64 slices to each of the
sixteen missing-event rectangles, in numeric path order. Rank common anchors
by squared separation of reference/moved difference-mean ranges divided by
the sum of variance upper bounds, ties by anchor index. Use the floor of the
midpoint of the two difference-mean centers as integer k. This ranking is
only a proposal rule. It makes no optimality claim.

Then apply the identical anchor/threshold rule once with 512 slices to EVERY
remaining HOLD among the original 31 (at most 31), again in numeric path
order. A previously failed event is not replaced by another anchor or
threshold. Do not add marginal events, geometric subdivision, operator solves,
extra slice levels, threshold sweeps, new geometries or a post-result budget
extension. All remaining failures stay HOLD. Reference certificates may be
reused only when stage, anchor and threshold all match. A 64-slice certificate
must never stand in for a 512-slice certificate.

The internal freeze occurs before new probabilities are evaluated. Parent
results are known and inform the 512-slice choice; this is not an external
preregistration. No claim is made about untested larger budgets.

## Combined coverage and audit

Reconstruct the original exact quadtree and both prior replacement stages.
Replace only declared HOLD paths with identical rectangle bounds. All 2,073
old exclusions are preserved verbatim. The same 2,104 closed rectangles cover
the entire square, including shared boundaries. Area equality supplements
structural coverage; it is not alone a cover proof. Area is parameter area,
not a physical probability or a fraction of admissible configurations.

If every remaining rectangle is excluded, the target conjunction is impossible
on this entire fixed-reference two-parameter square. This is a uniform result
for two independent support displacements. It does not extend automatically
to other references, directions, supports, domains, larger TV allowances, smaller weight-gap
gates, or the full selection/graph likelihood, and is not a general stability
theorem. If any HOLD remains, the square stays unresolved there. Neither
outcome supplies a close-law counterexample or a continuum-accuracy result.

The audit independently reconstructs quadratic geometry ranges, whole-rectangle
virtual-subset bounds, exclusive-rate corners, complete overlap coverage,
eightfold refinement containment, cache identity, event thresholds, source
coverage and all state transitions. Direct 110-digit exponential/factorial
PMFs cross-check the exact directed recurrence; they are diagnostic numerical
checks, while the rational/integer enclosures carry the proof. Missing inputs,
missing slices and wrong-resolution cache records must be rejected. Exact
small-rate controls, a zero-rate control and a dependence counterexample
supplement the full deterministic replay.
