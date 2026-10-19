# Landmark availability diagnosis — 19 October 2026

This is a **retrospective diagnostic** of the 48 archived intrinsic_moments
targets, following PR #65. It is not a fresh validation campaign or a new
operator. The prior outcomes were known when this analysis was designed.
All prior sources, records, thresholds and HOLD decisions remain unchanged.

## Questions and fixed analysis

Condition on each archived root and support. Recreate its sprinkled order and
marks, check their archived hashes, and reproduce the original retained
candidate and eligible-triple counts. Do not refit weights or select targets.
Report all 48 clouds, including six unavailable stencils.

For the common past and common future, exclude the two artificial boundary
events. Examine four point sets: root plus full support; root plus the two
temporal endpoints; root plus the remaining shell support; root alone.
The last three are diagnostic relaxations, not admissible replacements for the
original inference interface. A landmark for a reduced set need not supply the
distances required by the original full support.

For each set report the whole common cone, then candidates having at least
eight strict interior events to every constrained point. Compare all candidates
with the first 40 in the original increasing-mark order. Report comparable
triples at mutual interval-count thresholds 0, 1, 2, 4, 8, 16. The support
threshold stays eight in this sweep. A zero threshold still requires strict
causal comparability. No relaxed threshold is promoted to an operator.

Let W_ab be the interval count for a<b and -1 otherwise, on eligible
candidates. For a threshold k, count triples by

    sum_b indegree_k(b) * outdegree_k(b).

Transitivity and N(a,c)>=N(a,b)+N(b,c)+1 mean that both adjacent edges
passing k imply the third edge passes k. Also report the largest achievable
minimum of all three counts, a witnessing chain, its adjacent/outer counts,
and the longest chain in the threshold-eight graph. This is an exhaustive
finite-poset calculation, not a randomized search or estimate.

## Necessary packing condition

For a future triple s<a<b<c<T, the three disjoint open intervals (s,a),
(a,b), (b,c) and the three landmarks are inside (s,T). If every interval
has at least k events then N(s,T)>=3k+3. Reverse time for a past triple.
This holds for **every** constrained point s. Thus a minimum boundary
interval count below 27 certifies impossibility at k=8. Passing this
necessary condition does not establish existence. The analogous common-cone
condition is at least 2k+3 nonboundary events. Archive both bounds.

## Coordinate diagnostic

After the order calculation, repeat candidate screening and chain counting
using the exact Minkowski interval volumes rho*(pi/12)*tau^3, in place of
observed counts, on the same cloud, support and causal relation. These are
continuum mean-volume proxies, **not conditional expected counts after
selection** and not fresh Poisson observations. The candidates can differ.
Compare capped and uncapped threshold-eight triple availability. This can
help locate finite-sample versus geometric constraints, but cannot identify
boundary effects causally, qualify an intrinsic construction or prove an
asymptotic obstruction. Landmarks outside the simulated diamond are not tested.

## Verification and limits

Brute-force enumeration on small random transitive orders independently checks
triple counts, bottleneck maxima and the threshold-chain algorithm. Exact
chains test the 27-event packing bound. Mark-preserving relabeling and time
reversal are checked on the first available archived cloud at each density.
Replay all 48 records; require all discrete results, witnesses and old-frame
counts to agree exactly. Compare continuum values with atol=1e-9, rtol=1e-9.
Report coordinate byte matches separately. Hash inherited computational
sources and original records, and reject altered inputs.

Wall budget: 1200 seconds; peak RSS budget: 2048 MiB per execution/replay.
No targets are discarded or replaced; an incomplete execution is reported.
Dimension 2+1, flat geometry and known density remain assumptions.
Always retain INTRINSIC_MOMENT_HOLD, HOLD_PHASE3 and BD-C2 NO_GO.
Any subsequent construction needs separate development, a public protocol
and fresh targets. General interval-volume embedding context:
https://arxiv.org/abs/2111.09331 (Johnston); this audit does not reproduce it.
