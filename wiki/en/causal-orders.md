# Causal orders and spacetime questions

This research asks what structure is carried by relationships before a spatial drawing is assumed.

[Deutsch](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/causal-orders.md) · [Wiki overview](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/)

Source snapshot: 2026-10-17 · `6ac1363b6d3e0bcef6f863320290e3826977952a`

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

## Did the curvature smoke detector pass?

The new experiment studies 4D de Sitter spacetime with known positive curvature. It uses 64 or 128 events per order, three curvature strengths and separate flat controls. The contract, thresholds and sample sizes were publicly frozen before the first target run. All 8,702 orders are archived and fully reproduced internally.

| Diagnostic at N=128 | Flat reference | Strongest curvature case |
| --- | --- | --- |
| Joint 2-/3-/4-chain statistic | 10/512 warnings (1.95%) | 118/512 warnings (23.05%) |
| Longest chain | 1/512 warnings (0.20%) | 5/512 warnings (0.98%) |

Both methods satisfy the prespecified false-alarm requirement but miss the sensitivity target. The required upper false-alarm bound was at most 5%, and the lower detection bound at least 80%. The four selected one-sided bounds share a family error budget of 5%. These intervals condition on the fitted training and shared calibration bank.

The result is PRIMARY_SENSITIVITY_NOT_ESTABLISHED. Passing software replay does not change that result. The earlier 506/512 figure concerned a different density disturbance in flat geometry; it is not a curvature detection rate. A quiet diagnostic does not prove that spacetime is flat.

Software addendum: the first GitHub replay failed on coordinate bytes that differ slightly between NumPy CPU paths. Comparing every cloud found at most 2.22e-16 absolute difference and identical full causal relations. A supplementary checker accepts only explicitly verified variants. The original strict check, failure log and negative scientific result are preserved.

- [Complete results and every target cell](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_curvature/RESULTS.md)
- [Prespecified experiment contract](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_curvature/contract.json)
- [Documented portability repair](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_curvature/PORTABILITY.md)

## Why can a density disturbance resemble curvature?

Imagine the same point cloud under two models. In the first it is uniform in the physical volume of a curved spacetime. In the second it lies in flat spacetime but is sampled with a time-dependent density. For the conformal twins constructed here, every causal relation agrees exactly. Curvature and true proper time nevertheless differ.

All 3,072 coupled twins confirm the analytic construction. These are identity checks, not extra independent trials. With unrestricted unknown sampling density, no method using these orders alone can uniquely distinguish the two models. More features of the same order cannot remove this ambiguity.

A useful demonstrator can show model-deviation warnings and compare the twins. A Planck-unit display would convert a simulated scale; it does not build a physical Planck-time measuring device. New geometrical claims first need independent knowledge of sampling or volume. Repeated interactive testing needs a separately prespecified error-control plan.

- [Geometry and proof of density confounding](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_curvature/DESIGN.md)
- [Reproduction and next acceptance gate](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_curvature/README.md)
