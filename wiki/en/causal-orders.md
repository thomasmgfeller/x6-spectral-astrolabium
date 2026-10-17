# Causal orders and spacetime questions

This research asks what structure is carried by relationships before a spatial drawing is assumed.

[Deutsch](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/causal-orders.md) · [Wiki overview](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/)

Source snapshot: 2026-10-17 · `389cb3f688dfbc9d90086bb55c1b5d199b7e9c58`

## Events and their ordering

A causal order describes which events can precede which others. Imagine three tasks: A must happen before B, and B before C. Then A must also precede C. This implication is called transitivity.

Some pairs have no specified ordering. In a causal spacetime interpretation they may be spatially separated. An arbitrary generated network does not automatically justify that physical interpretation.

A Hasse diagram draws only the immediate relationships. The full relation matrix also contains the relationships implied by transitivity. An attractive arrangement of dots on a screen is not a measured geometry.

## Why a spectrum is not the whole story

Renumbering the nodes can make a drawing look different while leaving its structure unchanged. Isomorphism here means there is a one-to-one node correspondence preserving every directed relationship. That correspondence need not be the only possible one.

A fingerprint summarises a structure using a few numbers or frequency counts. Different structures can share the same fingerprint, just as different people can have the same height.

| Project abbreviation | What it represents |
| --- | --- |
| H7 | A specifically defined combination of spectra and counts; not a unique identifier. |
| N1 | Local neighbourhood profiles. |
| Q1 | Spectra of targeted one-point extensions. |
| R2 | Iterative refinement of features of ordered node pairs. |
| P123 | Histograms of common predecessors and successors for sets of one, two and three nodes. |

Published counterexamples expose limits of these summaries. The full directed relation and exact isomorphism checking remain the comparison reference.

## What do fairer controls achieve?

Two generators are easy to distinguish if one produces much denser or taller orders. Comparison pairs were therefore selected with the same node count N, relation count R and height H. Here height is the length of a longest chain, counted in nodes.

In the published primary comparison at N=64, P123 showed no demonstrated incremental benefit: the baseline reached 54.30%, while the combination reached 50.39%. Four of nine comparison cells lacked enough matching pairs and received no performance assessment. This limits a tested method; it does not prove that learning geometry is generally impossible.

- [Matched-control study and original data](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_matched_controls/README.md)
- [Counterexamples and reconstruction limits](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_relational_boundary/README.md)

## Proper time: what has now been tested?

Proper time is the time measured by a clock moving along its path. This experiment concerns the proper-time separation along a straight timelike connection between two marked events in a known flat model with one space dimension and one time dimension (1+1). The target is the ratio theta = tau/T to a specified outer time scale T.

The simple reference V counts the K events strictly between the marked endpoints. With m = N−2 background points, its estimate is sqrt(K/m). Intuitively, a larger time interval contains more points on average in the uniformly sampled model. The endpoints themselves are excluded. The estimator receives neither coordinates nor true test targets.

The first run is published with complete raw data, a report and reproduction code. It contains 6,912 orders: 768 for calibration and 6,144 for testing. The primary evaluation was specified in advance as 1,024 uniform test orders at m=256, or N=258.

| Method | RMSE in the primary comparison |
| --- | --- |
| V: interval point count | 0.031614 |
| D: global density/height regression | 0.177785 |
| C0: fixed constant | 0.176774 |
| L: local longest chain (descriptive) | 0.084021 |

RMSE summarises estimation error; smaller means more accurate here. These values use units of normalised proper time. A value of 0.031614 does not mean 3.16% relative error for every individual event pair. V meets the specified 0.05 limit and all other primary criteria. Its conditional 95% bootstrap interval for RMSE is [0.030068, 0.033199], holding calibration fixed.

D uses only global quantities and no local features tied to the marked endpoints. The gap against D therefore does not establish superiority over every possible estimator. V is an established reference; this experiment demonstrates no incremental spectral benefit.

- [Result report and reproduction](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time/RESULTS.md)
- [Definition, assumptions and original contract](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time/README.md)

## Which limits remain?

Supplementary controls compare uniform orders with a jittered grid at exactly the same node count, relation count and height. At m=64 and m=144, 128 pairs were evaluated per size. At m=256, only 63 of the required 128 pairs were available. This largest supplementary control remains INSUFFICIENT_COMMON_SUPPORT and receives no performance assessment; the threshold was not relaxed afterwards.

- Dimension and outer time scale are supplied, not discovered from the order.
- The same finite order can admit different proper times; estimation remains statistical.
- Results apply to the specified synthetic model. Curved spaces, other dimensions and physical measurements have not been tested by this run.
- External replication and stronger local comparison estimators remain open. Earlier negative P123 results still stand.

## How can the result be checked?

The archive contains all 6,912 complete orders, reference coordinates, marked endpoints and individual predictions. The internal countercheck verifies 27,648 predictions and every order including relabellings. The GitHub workflow reruns the complete study without network access and compares the results. This is internal reproduction, not independent external confirmation.

The result report gives software versions, the source commit and reproduction commands. The original archive and frozen computation remain unchanged. The documentation also distinguishes a dated source commit from independently established public preregistration timing.

- [Countercheck report](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time/results/verification.json)
- [Raw-data inventory and checksums](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time/results/RESULTS.json)
- [Publication and GitHub checks: PR #44](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/44)
- [Causal-Set Lab (separate browser prototype)](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/rax-cqg-lab.html)

## When are proper time and its uncertainty reliable?

The new extension applies to known flat diamonds in d spacetime dimensions. Dimension and time scale must be known, the inner interval must be fully contained, and background points must be independent and uniform in volume. Endpoints and region are fixed before the confirmatory sample. Then K inner points among m background points give the raw estimate tau/S = (K/m)^(1/d).

49,152 new point clouds in d=2,3,4 agree with the declared binomial model. The resulting 95% intervals are conservative. Good coverage does not imply a narrow estimate: at d=4, tau/T=0.1 and m=256, the inner count is zero with probability about 97.47%.

Unknown sampling density, clipped intervals, relation errors or dependent observations can invalidate this uncertainty statement. A valid finite poset does not prove a causality condition for a smooth continuum.

- [Shared overview: assumptions, results and limits](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time_publication/README.md)
- [Containment proof and finite-sample bounds](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time_domain/README.md)

## Sampling until the requested precision is reached

The sequential version allows inspecting results after each batch of fresh independent points and stopping once precision is sufficient. It uses a time-uniform confidence sequence following Howard et al., with a 2.5% time-error budget. Under the assumptions, the probability of reporting relative precision below 10% while the actual error exceeds 10% is at most 2.5%. This is not automatically a conditional guarantee restricted to successful stops.

No finite budget is guaranteed to suffice. BUDGET_EXHAUSTED withholds the precision claim. In the archived 4D count simulations, all 1,024 repetitions per positive case reached the target; median sample sizes were 2,592 locally and 1,673,216 globally. These are observed requirements. The local case assumes a known, fully containing diamond with time scale 0.2T.

A fixed experiment with 480 local points makes a different statement: at true tau/T=0.1, the raw estimate has a 97.34% probability of relative error below 10%. It does not provide the same guarantee under repeated inspection. The published planning note separates these criteria.

- [Time-uniform bound, stopping rule and complete results](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time_sequential/README.md)
- [Reproducible fixed-budget calculation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time_publication/planning.py)

## What can the longest chain warn about?

A one-time comparison of the longest inner chain with fresh reference orders at the same count K examines additional shape information. Observed null-model warnings were 5/512. Deliberately spatially compressed sampling in still-flat geometry produced 506/512 warnings. This demonstrates a density perturbation, not curvature detection.

A warning sets scientific time qualification to WITHHELD_MODEL_WARNING. No warning does not prove the model. The diagnostic has its own 2.5% false-alarm budget; together with the time confidence sequence, the probability of at least one of the two error events is at most 5% under the common null model.

The main simulation uses count batches; an additional run checks actual geometric points. Both new packages were locally frozen before sampling and published afterwards. A repaired JSON serialization failure remains documented with original code and identical raw counts. Internal reproduction and GitHub CI are not independent external replication.

- [Execution history and preserved repair evidence](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time_sequential/EXECUTION_HISTORY.md)
- [Fully reproduce both new experiments](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time_publication/replay.py)
