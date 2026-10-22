# BK anchor-search isolation protocol — 19 October 2026

This new bounded experiment continues phases 1/2 after PR #58. The original
48 clouds are known data; none is used as a fresh test. We isolate one suspected
implementation bottleneck, without retuning the operator or reopening phase 3.

## Fixed comparison

Each independent cloud supplies exactly the same marked poset, maximal chain,
root, time shells, temporal points and scale to three arms:

1. `legacy64`: the byte-unchanged original implementation, which ranks common
   anchors by interval depth and mark, keeps 64, then applies the balance rule.
2. `balanced64`: enumerate all common anchors with the original minimum interval,
   reject zero/one/out-of-table overlaps and apply the unchanged balance rule,
   then retain the first 64 in exactly the original depth/mark order. Aggregate
   with the same median and longest-chain time scale. No relaxed thresholds.
3. `oracle_cap`: a diagnostic control selecting the exact distance cap among the
   SAME discrete shells, using simulator coordinates. All operator coefficients,
   time scales, reference points and minimum populations remain unchanged. This
   arm is explicitly not an intrinsic estimator, not an error lower bound, and
   not a continuum oracle: shell placement, frame wandering and temporal error
   remain. It may perform worse than either estimator.

Inference for the two genuine arms accepts relation, transported independent
marks, endpoint IDs, known rho and the frozen configuration only. Coordinates
are allowed only in the sampler, evaluator and explicitly named oracle control.
All 66/64-style selection counts are observable diagnostics, not tuning inputs.
A stable relabelling check covers both genuine arms at every density.

## Seeds, order and budget

`contract.json` fixes six separate development clouds and 48 new held-out clouds.
All three densities and all seeds are mandatory. The program runs methods in
fixed order (legacy, balanced, oracle); reported timing is descriptive, includes
shared caches, and is not a speedup benchmark. The total run includes sampling,
all three arms and relabelling. Wall limit 600 seconds; measured peak RSS limit
2048 MiB, checked after each cloud (not a kernel memory cap). Budget exhaustion
is a hold with partial data retained, never seed replacement.

The protocol is committed and pushed before development data. Implementation,
tests and analyzer are committed and pushed before target data. Development
runs debug correctness and feasibility only; no parameter grid or winner
selection is authorized by this protocol. Code hashes cover all inherited
inference, sampler and analysis dependencies. All target clouds are replayed.

## Outcomes, denominators and uncertainty

The independent statistical unit is the cloud. Report availability and signature
with ALL clouds in the denominator, Wilson 95% intervals; cap recall, precision,
missing distances, population, conditional time/space/metric/operator/chart errors,
mean/SE/RMS as appropriate. Empty denominators remain missing. Compare availability
with discordant-pair counts and an exact two-sided McNemar/binomial test; report
paired recall change with mean and SE. These are exploratory/descriptive outputs,
not a preregistered population-level superiority theorem. Metric RMS comparisons
also report the common available subset to expose selection effects.

Primary high-density criteria: availability gain at least 0.25, candidate
availability at least 0.80 and mean paired cap recall gain at least 0.25. Only
all three yield `ANCHOR_COVERAGE_IMPROVED`. Otherwise `ANCHOR_SEARCH_HOLD`.
The original 0.5 metric-error limit is retained and prominently reported for
all three arms. Coverage success alone is not phase-2 success. Regardless of
this diagnostic outcome, `HOLD_PHASE3` and the BD-C2 finite-budget NO_GO remain.

## Controls and sources

Check cap-order failure on an explicit finite poset with usable deeper-ranked
anchors, agreement with exhaustive selection, zero/one overlaps, time reversal,
relabelled copies, legacy-wrapper parity and product/affine identities. Replay
must reject changed numeric records; coordinate hashes are reported separately
from numerical/discrete agreement, following the existing portability contract.

The unchanged balance rule is from Boguñá–Krioukov, spatial overlaps,
[arXiv:2401.17376v2, Eq. 34](https://arxiv.org/html/2401.17376v2).
The unchanged operator is from their local d’Alembertian,
[arXiv:2506.18745v1, Eqs. 86–91](https://arxiv.org/html/2506.18745v1),
[Phys. Rev. D 113, 024046](https://doi.org/10.1103/np89-qzjp).
The revised search is our finite-budget implementation choice, not a new
continuum theorem or an independently validated improvement of their method.
