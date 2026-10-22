# Budgeted refinement of unresolved surface cells

SPDX-License-Identifier: Apache-2.0

**ADAPTIVE_SURFACE_CERTIFIED.** On the unchanged PR95 pair, the certified TV
upper bound improves from **0.01894939530593638801 to 0.01706315569576179848**,
about **9.95% tighter**. The unresolved transfer-intensity upper bound decreases
by about **49.73%**, from 0.01282469835364486998 to 0.00644704023662276662.
No additional observations or geometries are introduced. The small operator gap
remains about 0.00365762%; this is not improved reconstruction accuracy, a strong
pair, or a global stability result.

| Stage | Additional cell evaluations | Certified transfer leaves | Unresolved intensity upper | TV upper |
|---|---:|---:|---:|---:|
| PR104 exact replay | 0 | 659 | 0.01282469835364486998 | 0.01894939530593638801 |
| Round 1 | 4,096 | 1,890 | 0.00815576970936222918 | 0.01733000031466076426 |
| Round 2 | 8,192 | 3,514 | 0.00644704023662276662 | 0.01706315569576179848 |

The final 88 directed transfer pairs yield a certified actual cancellation lower
bound of 0.00115369180193147903. Total changed-intensity upper bound:
0.01860396766226083874. Balanced residual-intensity upper bound:
0.01721040880919169700. Thus this step improves both geometric localization and
signed transfer accounting. It does not measure actual TV or actual cancellation.

## Fixed rule and budget

1. Reconstruct the 8,320 strip rectangles of PR104's 64×64 grid, including its
   spatial-bisector split and both cone directions. Classification, complete
   transfer table and TV bound must reproduce PR104 exactly. Initially 1,263
   cells have unresolved complete membership patterns.
2. Rank unresolved leaves by their certified transfer-intensity upper bound,
   decreasing; break ties by lexicographic cell ID. Select exactly 1,024 leaves.
3. Split each selected spatial rectangle at both exact rational midpoints into
   four disjoint children. Evaluate only those children with the unchanged
   correlation-preserving cone tests and inherited box exclusions.
4. Repeat once, for **8,192 additional evaluations in total**, then stop.

Known transfers, outside-domain exclusions and any other resolved cells are
locked: they are neither refined nor recalculated as part of the two rounds.
Selection depends on deterministic bounds in the known model, not noisy observed
data. No sequential statistical coverage correction or new sampling assumption
is invoked. The contract/source freeze is reproducibility metadata, not external
preregistration.

## Coverage and intensity accounting

Each selected parent is an unresolved leaf and is removed exactly once. Its four
children cover the same spatial rectangle up to zero-area edges and have the
same cone side. The strip over a spatial point is unchanged by subdivision.
Therefore the child strips cover exactly the parent's strip, with no additional
volume and no double-counting. The cone bisector cannot be crossed by refinement
because it was already a seed-grid boundary.

Each leaf has one state: outside the outer diamond, no affected interval,
unchanged pattern, certified directed transfer, or unresolved. The underlying
whole-cell certificates and outward rational thickness bounds are inherited from
PR103/104. Only complete directed transfers contribute intensity lower bounds.
Every unresolved leaf contributes its ENTIRE upper intensity to the residual R.
When a parent is refined, its unresolved budget is replaced by the child budgets;
the parent is never added again. Locked transfer contributions remain unchanged.

For each atom, incoming/outgoing intensity intervals and their lower bounds are
aggregated from the current leaves. The two valid balanced-residual bounds and
Poisson void inequality are exactly those derived in
[the surface-correlation package](../surface_correlations/README.md). Retaining
the best bound across the archived stages is valid: all are deterministic upper
bounds for the same pair and observation law. The numerical lower transfer bounds
and cancellation certificate never decrease in this run, and this is checked.

There are **4,189 unresolved leaves** at the end, more than the 1,263 original
unresolved cells because parents were split into smaller cells. Their combined
intensity upper bound is about half as large. Leaf counts alone are not a measure
of remaining uncertainty. Final partition: 14,464 leaves (6,761 excluded,
3,514 certified transfers, 4,189 unresolved). Total evaluated cells including the
seed replay: 16,512. These are computational cells, not new Poisson observations.

## Independent audit

The archive contains every evaluated cell ID/state/mass, all transfer labels and
the exact parent lists for both rounds. The audit reconstructs cell rectangles
from IDs independently, verifies each selection against the priority rule,
requires all four fresh children, checks exact area preservation and locks all
previously resolved certificates. Missing children and a dropped refinement round
must be rejected. This partition audit checks coverage and bookkeeping in addition
to the earlier cone proofs.

The intensity and cancellation ledgers are reconstructed independently from leaf
records. Newly certified leaves are sampled across cone directions and refinement
depths; direct scalar causal membership under both geometries is checked at
interior points. Point checks audit implementation; the inherited rational
interval algebra provides whole-cell coverage. See audit.json for exact counts.

## Stop and next decision

The prescribed two-round budget is exhausted. The second round lowers the TV
upper bound from about 0.0173300 to 0.0170632, a smaller marginal gain than the
first. Do not silently extend this grid run. A subsequent experiment should first
compare remaining intensity with the maximum achievable benefit of further
localization, or test whether common positive atom background can sharpen the
full-law bound using the now-certified transfer table. A larger geometry search
requires its own declared contract and admissibility checks.

## Reproduce

Run from the repository root:

```sh
python3 -B research/lorentz_local_dalembert/adaptive_surface/as_run.py --verify
python3 -B research/lorentz_local_dalembert/adaptive_surface/as_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/adaptive_surface/SHA256SUMS
```

The same conditional 90-interval/overlap experiment, known density and fixed
outer diamond apply. This is not a claim about full point-cloud observations,
continuum operator accuracy, or physical validation.
