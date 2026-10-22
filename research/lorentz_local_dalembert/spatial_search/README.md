# Larger spatial moves: better close-law pair, strong candidates still unresolved

SPDX-License-Identifier: Apache-2.0

**HOLD_STRONG_PAIR.** A frozen search of **512** single-node spatial moves finds
a certified close-law pair with symmetric operator gap
**0.00043483222811342352–0.00043483222811342353**, or **0.0434832%**.
This is **11.8884 times** the PR95 gap. Its full count/overlap-law total variation
satisfies **TV <= 0.21182678306522136697**, below the 1/4 gate. It remains far below
the **>20%** operator-gap target for disjoint 10% relative-error balls.

There are also **18 admissible sampled candidates with >20% gap**. A subsequent,
explicitly post-search single-count diagnostic certifies **three** as too
distinguishable for the TV gate. **Fifteen remain unresolved**, including the
40.5458% candidate. A TV upper bound of 1 is inconclusive; it is not proof of
distinguishability. We do not exclude strong close-law pairs in this finite grid,
let alone in the continuous geometry family.

| Result | Earlier PR95 pair (PR105/106 certificate) | New selected pair |
|---|---:|---:|
| Boost-frame move of node 15 in +x | 0.000008409945 | 0.0001 |
| Symmetric relative operator gap | 0.00365762% | 0.0434832% |
| Certified TV upper bound | 0.01706315569576179848 | 0.21182678306522136697 |
| Same selected-node order, fixed landmarks/root | Yes | Yes |
| Strong >20% operator gap | No | No |

These are **different pairs**. The larger gap uses more of the statistical budget;
the new TV number is not an improvement on the old pair's TV certificate.

## Frozen finite search and eligibility

[contract.json](contract.json) fixes all 16 support nodes, both spatial axes in
the existing rational boost frame, both signs, and eight positive step lengths
from the PR95 step through 0.1. Each candidate moves exactly one support node.
The outer diamond, sampling density, four landmarks and root remain fixed.

- 512 candidates; **85** change at least one selected-node causal relation and
  are rejected. No rejection is due only to the inherited near-null margin.
- **427** pass exact order/margin and moment-rank checks.
- All passing candidates receive a 16-by-16 boundary integration. At most eight
  candidates with coarse TV upper bound in (1/4,1/2] receive the frozen 64-by-64
  refinement, ranked by operator-gap lower bound and then index.
- **64** pass the TV gate and the exact intrinsic-moment/conditioning gates.
  Selected row **329** moves node 15 in +x by 1/10000.
- Its landmark condition upper bound is **341.9633** and intrinsic moment
  condition upper bound **16028.3598**, both below the inherited 100000 limit.

The selected row's coarse TV bound is 0.2878353. The predetermined refinement
lowers it to 0.2118268 by retaining 1,922 of 8,320 surface rectangles. It uses no
unverified transfer cancellation or background smoothing.

The complete candidate table, exact selected coordinates/weights and selection
record are in [candidates.json.gz](candidates.json.gz), [witness.json](witness.json)
and [summary.json](summary.json). **An upper bound above 1/4 is a certificate
failure, not an admissibility failure of the true law.**

## Why signed-axis localization is valid

After the inherited determinant-one Lorentz boost, a signed spatial permutation
maps each move to +x. The same map is applied to both geometries and to the fixed
outer bounding rectangle. It preserves volume and all Minkowski cone tests.

For the moving tip v and h>0, let r0=|X-v_space| and
r1=|X-v_space-(h,0)|. The future and past changed regions are disjoint strips,
each of thickness |r1-r0|. The identity

    r1-r0 = (h^2 - 2h(x-v_x)) / (r1+r0)

gives an interval enclosure without subtracting close square roots. Splitting
the spatial grid at x=v_x+h/2 fixes its sign. A strip cell can be discarded only
when the inherited whole-box classifier proves it is outside the fixed diamond,
cannot change an affected interval, or has the same complete 90-bit label under
both geometries. **Every remaining cell contributes its upper mass**, including
every unresolved cell. The global 2*rho*scale^3*area*h bound is also retained.

For changed-point intensity M, a shared Poisson process gives

    TV(full count/overlap law) <= 1-exp(-M).

All counts, all overlap counts, and the total number of sampled B points can be
coupled simultaneously. Count independence is not assumed. Exact rational
arithmetic, directed rounding and the inherited exponential enclosure are used;
for M>1 this implementation conservatively returns the trivial TV upper bound 1.

## Diagnose the strong-gap candidates with an actual lower bound

[diagnostic_contract.json](diagnostic_contract.json) explicitly records the
post-search choice to examine **all** 18 order/rank-passing rows with gap >20%.
All 18 also pass the conditioning checks. This diagnostic adds no geometry and
does not alter search steps, rankings or stopping rules.

An interval with squared proper time q has Poisson mean
lambda=rho*scale^3*pi*q^(3/2)/12. For two means lambda and mu, the single-count
affinity is exp(-(sqrt(lambda)-sqrt(mu))^2/2). Marginalization and the Hellinger
inequality therefore give the rigorous **lower** bound

    TV(full joint law) >= TV(single count)
                       >= 1-exp(-(sqrt(lambda)-sqrt(mu))^2/2).

Pi and square roots are enclosed rationally. The largest certified lower bound
among the 90 counts is kept; dependence between different counts is irrelevant.
The exponent is conservatively capped at 1 to stay inside the inherited series
domain. [marginal_diagnostic.json](marginal_diagnostic.json) preserves every result.

| Candidate index | Symmetric operator gap | Certified full-law TV lower bound |
|---|---:|---:|
| 39 | 30.0688% | 0.31978285350835269881 |
| 47 | 21.8451% | 0.34355114096805282508 |
| 295 | 30.0033% | 0.25796680859264318377 |

These three cannot satisfy TV<=1/4. The remaining 15 lower bounds are below 1/4,
which does **not** establish closeness. For example, row 327 has gap 40.5458% and
only the interval **0.18172498 <= TV <= 1** from these certificates.

## Verification and next decision

[audit.json](audit.json) records exact finite-set and refinement-selection checks,
spatial-area coverage, reproduction of the old reference localization, all four
signed spatial frames and **8,160** rational scalar membership checks, including
5,688 points in excluded cells. Samples audit implementation; the interval
inequalities establish whole-cell coverage. Three invalid-input controls and
equal-mean, symmetry and exponential-domain controls are included.

```sh
python -B research/lorentz_local_dalembert/spatial_search/ss_run.py --verify
python -B research/lorentz_local_dalembert/spatial_search/ss_audit.py --verify
python -B research/lorentz_local_dalembert/spatial_search/ss_marginal.py --verify
sha256sum -c research/lorentz_local_dalembert/spatial_search/SHA256SUMS
```

The next useful mathematical step is to sharpen **single-count likelihood-ratio
tail bounds for the 15 unresolved strong candidates** before spending more on
joint-law volume integration or further geometry searches. Only candidates that
survive that inexpensive obstruction should receive a joint-law calculation.

Scope remains conditional on the fixed selected-node order and known density.
The complete B causal matrix, B coordinates, A-selection likelihood, continuum
operator consistency and physical accuracy are not established here. Neither
finite noisy-count stability nor its failure is proved globally.
