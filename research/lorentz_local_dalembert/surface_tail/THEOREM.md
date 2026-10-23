# Exact event coverage of the previously untested surface rectangles

SPDX-License-Identifier: Apache-2.0

## Scope and preserved geometry

This stage uses exactly the reference, conditional Poisson experiment, nodes
15/17, independent boosted-x square [-1/10,1/10]^2, 2,104 terminal rectangles,
order and admissibility conditions, weight-gap gate >1/5 and full labelled
count/overlap-law TV gate <=1/4 from `paired_surface/THEOREM.md`.

The parent retains 775 HOLD rectangles. Exactly 744 have no new exact marginal
or overlap event in that parent campaign. Only these 744 enter this stage.
The other 31 HOLDs and all prior exclusions remain unchanged. No new base,
subdivision, operator computation or geometry optimization is introduced.

Every new exclusion proves TV>1/4 uniformly on its rectangle's unchanged-order
subset. It therefore excludes the strong close-law conjunction independently
of its weight gap. The previous continuous geometric/transport/operator
certificates remain part of the combined proof. HOLD is not a close-law pair.

## Fixed marginal events

For every selected rectangle, retain the parent's ranking of observed
single-count intervals by squared separation of their reference/moved mean
bounds divided by the sum of their mean upper bounds. Try at most the first
two; ties use the interval index. No replacement candidate is added when a
budget or mean-separation precondition fails.

Exact rectangle extrema of squared proper time and directed rational pi and
square-root bounds enclose each Poisson mean. For a fixed integer k,
P(Pois(mu)<=k) decreases with mu, so four endpoint CDF bounds enclose the same
event under reference and moved geometries. The inherited directed integer
PMF recurrence includes infinite tails and uncertain normalization. Its
integer threshold is proposed by the existing enclosed likelihood crossing;
when a unique crossing cannot be certified, it uses the declared midpoint
threshold. Event validity does not depend on optimality.

If the lower event-probability difference exceeds 1/4, marginalization gives
a full-law TV obstruction. Overlapping other counts are not factored. Failed
mean-separation, rate or arithmetic-support budgets remain HOLD. The first
successful event stops this rectangle's marginal stage. Identical input
interval index and mean enclosures reuse one exact certificate; cache reuse
changes neither selected candidates nor any bound. Such reuse is not an
independent replicated experiment.

## Bounded overlap stage

Among THIS stage's marginal failures, rank rectangles by the parent's best
common-anchor score: squared separated difference means divided by the sum
of their variance upper bounds. Ties use numeric rectangle path. Try the first
128 rectangles, or all if fewer; one best anchor per rectangle. The threshold
is the floor of the midpoint of the reference/moved difference-mean centers.
All ranking and threshold rules are fixed before new probability evaluation.
The score is a proposal heuristic, not an optimal test or TV bound.

For A,B with common fixed anchor, exact cancellation gives

    D=N(A)-N(B)=N(A minus B)-N(B minus A).

Only these exclusive atoms are independent. Their means a-c,b-c still depend
on c=mu(A intersect B). The inherited rectangle virtual-tip construction bounds
c below, and min(aU,bU) bounds it above. Cover the entire enclosing c interval
by 64 equal closed rational slices. On [l,u], the exclusive means lie in

    [max(0,aL-u),aU-l] and [max(0,bL-u),bU-l].

The event D<=k is decreasing in the positive exclusive mean and increasing in
the negative one, giving two corner bounds per slice. The minimum lower and
maximum upper bounds across all slices enclose the law without assuming
monotonicity in c or substituting a midpoint. Infinite Poisson tails remain
included. A rate, support or precision failure returns [0,1]. Separation from
the reference enclosure lower-bounds full-law TV. Reference laws sharing an
anchor and integer threshold are stored once and referenced by identifier.

## Stop and coverage

Run exactly one marginal pass over all 744 declared inputs, then at most 128
overlap events under the fixed selection rule. Do not increase budgets, alter
thresholds, add anchors, or refine cells after seeing results. All unsuccessful
and untested overlap cases remain HOLD. No claim is made about what a larger
budget would yield.

Reconstruct the parent's exact quadtree, replace only matching selected HOLD
paths, and verify identical rectangle bounds. This preserves the entire closed
square including shared boundaries. New certificates must account for all
744 source paths exactly once in the marginal stage; overlap replacements
must be a subset of its failures. The 31 earlier tested HOLDs stay unchanged.
Exact area sums supplement this structural coverage check. Area fractions
refer solely to this parameter square, not to physical probability or the
fraction of admissible geometries.

The internal contract freeze precedes the first new event evaluation; parent
results are known, so this is not external preregistration. Independent audits
check the source selection, exact geometric bounds, event endpoint means,
probabilities via direct exponential/factorial PMFs, overlap-slice coverage,
state transitions and complete combined coverage. No global stability, full
A-selection/B-graph likelihood, physical continuum accuracy, or actual close-law
counterexample is asserted by this method.
