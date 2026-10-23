# Finite-count events on the remaining paired intervals

The input is exactly the 574 unresolved subcells of PR113, belonging to 24
signed directions. All previously excluded cells remain unchanged. The model
is the fixed-density conditional 90-labelled-interval Poisson experiment,
with landmarks 0–3 and root 4 fixed; it is not the full A-selection or B-graph
likelihood. Each candidate moves two supports along one boosted spatial axis.
All boosted times remain fixed. Every law assertion below concerns the subset
preserving the reference selected-node causal order, so all observation
intervals stay inside the fixed outer sampling diamond.

An exclusion is a full-law TV lower bound strictly greater than 1/4. Combined
with earlier order and operator-gap exclusions, this rules out the conjunction
of unchanged selected order, symmetric operator-weight gap >1/5, and TV<=1/4.
An unresolved event test or arithmetic budget failure remains HOLD.

## A common event on the narrow negative-x strip

For the single displacement of node 15 along negative boosted x with magnitude
s in [7/160,45/1024], keep the existing observable event

N(I(15,1)) - 2 N(I(2,15)) <= 787.

The two intervals lie strictly after and strictly before node 15, respectively,
and therefore are disjoint up to measure-zero boundaries. Independent Poisson
increments apply to these two counts. The endpoints other than node 15 are
fixed. Moving another support changes neither interval nor their joint law.
For a paired line with node-15 velocity v, its displacement lies in the strip
if the entire mapped interval s=-v*h lies within [7/160,45/1024]. The proof
checks this inclusion exactly, not by sampling. The source event is unchanged;
its probability bound is recomputed on this newly declared whole strip.

## Marginal and disjoint joint events

Each recorded single count is Poisson, regardless of its correlations with the
other 89 counts. Its mean range follows from the exact quadratic extrema of
q(h), directed square-root/pi bounds, and rho*scale^3*pi*q^(3/2)/12. For two
disjoint mean enclosures, the inherited likelihood-crossing rule chooses an
integer threshold k, using a rigorous logarithm enclosure or the predeclared
midpoint fallback. CDF monotonicity in the mean gives the same event {N<=k}
under both laws. Its probability separation lower-bounds full-law TV.

Additional joint candidates use only I(2,n) and I(n,1) for one moving support
n. Their constant boosted times prove disjointness throughout the cell. X is
whichever interval has the smaller base mean, Y the other. With coefficient
a in {1,2,3}, consider {Y-aX<=k}. It is increasing in X and decreasing in Y,
so rectangular mean bounds reduce to two monotone endpoint evaluations.
Other interval counts may overlap arbitrarily; their independence is not used.

The fixed candidate-ranking score is the squared separation of the two
mean enclosures for Y-aX divided by the sum of their upper variances. The
threshold is the floor of the midpoint of the two mean-enclosure centers.
This is a deterministic geometric proposal rule, not itself a probability
bound or an optimal-event claim. At most two such candidates are evaluated
per input cell, after at most two marginal events ranked by squared square-root
mean separation. Events and rankings depend on candidate geometries, not on
realized Poisson data. Every retained exclusion has its own rigorous uniform
probability separation; no empirical multiple-testing claim is involved.

## Probability arithmetic and infinite tails

The inherited exact routines put relative PMF mass 1 at floor(mu). Directed
integer recurrences on a 10^-80 grid bound every downward and upward weight.
All downward masses are included. The omitted upward tail is bounded by its
first possible mass times a geometric-series factor with ratio
mu/(upper+2)<1. The tail is retained in normalization; for the joint event the
uncomputed X tail is additionally retained in the event upper bound.

Thus finite support does not silently replace a Poisson law by a renormalized
truncation. A fixed mean/support/precision budget failure supplies no exclusion.
The probability width caused by a whole-cell mean range is distinct from the
much smaller numerical enclosure error at each fixed mean. Independent decimal
PMF sums audit the implementation; they do not supply the rigorous bound.

## Exhaustive input coverage and limits

Contracts, code, this proof and source evidence are hashed before evaluation.
All 574 inherited HOLD subcells receive exactly one record. No new bisection,
direction, density change, threshold search or second optimization pass is
allowed by this contract. Initial successes and failures are both archived.
Old exclusions plus all new records cover the original domains. Signed-ray
closure is asserted only when its entire retained HOLD cover is eliminated.

Even if all 60 rays close, this proves only a union of 30 fixed one-dimensional
lines from one reference geometry. It is not an open multidimensional region,
arbitrary-pair stability, a general finite-error stability theorem, or a
physical accuracy result.
