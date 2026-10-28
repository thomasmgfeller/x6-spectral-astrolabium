# Causal orders and spacetime questions

This research asks what structure is carried by relationships before a spatial drawing is assumed.

[Deutsch](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/causal-orders.md) · [Wiki overview](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/)

Source snapshot: 2026-10-28 · `ed481912b9330a09d02206beff6f6f535bb4ef85`

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
- [Try the proper-time demonstrator (fixed budget; German UI)](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/proper-time.html)
- [Standalone Jupyter notebook with example outputs (German)](https://thomasmgfeller.github.io/x6-spectral-astrolabium/research/lorentz_proper_time_lab/eigenzeit.ipynb)

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

## How does a fixed point count change the curvature formulas?

Update of 18 October 2026: Roy–Sinha–Surya study sampling with a fluctuating point count. Our experiments hold the count fixed. The expected chain counts and their curvature coefficients therefore change through normalization by the physical volume.

The adaptation is derived and checked with 24,576 independent point clouds. An independent integral for two-element chains agrees closely with the corrected prediction. The joint goal of resolving all three leading coefficients within ±5% remains unmet: the three- and four-chain intervals are too wide.

An algebraically invertible formula need not provide a useful measurement. With 128 points and true RT² about 0.12, the tested reconstruction has single-order root mean squared error about 96.53. Chain counts are strongly correlated. No general curvature sensor is qualified, and the density-twin limitation remains.

The contract, seeds and budget were public before the first target run. Full replay reproduces every order and decision. A documented import wrapper repairs a verifier naming conflict without changing frozen sources, data or thresholds. External replication remains open.

- [RSS: Ergebnisse / Results](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/8ee417ba8c44c1f32f4e310a6566168d84982d3a/research/lorentz_rss_fixed_n/RESULTS.md)
- [RSS: Herleitung / Derivation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/8ee417ba8c44c1f32f4e310a6566168d84982d3a/research/lorentz_rss_fixed_n/DERIVATION.md)

## Proper time v0.2: when do more data help?

The new validity map directly calculates 1,176 combinations of model, observed count and interval method. These are not new point clouds or measurements. All 714 combinations within their assumed model class retain at least 95% coverage. Of these, 192 also meet the declared precision gate and 522 remain insufficiently precise. Another 462 are outside the assumed class.

More data do not repair an unknown density error. In the example with half the retention rate inside the inner interval, the unprotected calculation falsely declares at most 10% relative error with about 98.81% probability at 65,536 observed points. This is not a curvature or error-detection rate.

An independently justified bound on mean observed intensity inside versus outside permits a more conservative interval. With a broad ratio range from 0.5 to 2, that interval retains about 97.74% coverage in the same example but refuses the requested 10% precision. This is a justified abstention.

For uniform flat 4D data with true proper time 0.2 of the outer scale, 65,536 is the first passing count on the tested grid. Allowing a ratio from 0.8 to 1.25 raises it to 262,144. These are neither global minimum budgets nor sequential stopping guarantees. The browser demonstrator retains its existing flat model.

- [Results and budget table](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e5840afa7c7865a48766d1a5366210508a7b1f05/research/lorentz_proper_time_validity/RESULTS.md)
- [Derivation and assumptions](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e5840afa7c7865a48766d1a5366210508a7b1f05/research/lorentz_proper_time_validity/DERIVATION.md)

## Curvature: extra chains add little precision here

The new study restricts the problem to a known de Sitter family with one unknown curvature quantity. It combines two-, three- and four-element chains while accounting for their strong correlations within the same event cloud.

Weights were fixed using previously published data. After the protocol was made public, 16,384 independent fresh clouds with 128 events each were generated. In the primary comparison, root mean squared estimation error (RMSE) fell by only 1.37%. The prespecified target of at least 10% was missed.

For weak curvature, the calculation suggests about 1.7 million independent clouds for a nominal relative 20% half-width. At the stronger tested curvature, about 2,700 are suggested. These are approximate noise-only planning counts, not completed large runs or guaranteed precision bounds. Systematic model errors persist.

The next useful approach focuses on two-element chains and a fuller geometric prediction with controlled errors. A qualified curved-spacetime clock has not been achieved. Density assumptions, an independent time scale and external replication remain open.

- [Results and data budgets](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/01430ce5f0a648ad63d611a451f0d0fd7ccb16aa/research/lorentz_de_sitter_information/RESULTS.md)
- [Protocol and sources](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/01430ce5f0a648ad63d611a451f0d0fd7ccb16aa/research/lorentz_de_sitter_information/README.md)

## Curvature intervals: reliable within explicit assumptions

The next step uses only two-element chains. For a specified de Sitter family, the full geometric prediction is computed with exact fractions and a bounded remainder. A mathematical inequality establishes that the prediction can be inverted uniquely throughout the declared range.

Pairs in the same point cloud are dependent. The new error bound accounts for that. With known uniform physical-volume sampling, independent identical clouds and a prespecified fixed data budget, the intervals contain the true model value with at least 95% probability. This follows from the derivation; simulation alone does not prove it.

16,384 fresh point clouds were calculated and fully reproduced. Every tested interval contains its model value, but none meets the required relative 20% precision. At the strongest tested curvature, 4,096 clouds give an interval of about 0.843 to 3.131; the true value is 3.131. The procedure correctly withholds precision qualification.

The conservative design calculation gives very large sufficient budgets for the specified curvatures. These are not necessary minimum counts and were not simulated. The next step is therefore a sharper statistical bound with the same finite-sample protection. Unknown density, freely chosen stopping and a physical clock remain outside the present guarantee.

- [Results and limitations](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e6a5bce4cafe44ddb929da3ae32d9afa4d64eca1/research/lorentz_de_sitter_c2/RESULTS.md)
- [Full derivation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e6a5bce4cafe44ddb929da3ae32d9afa4d64eca1/research/lorentz_de_sitter_c2/DERIVATION.md)

## Sharper intervals: the efficiency gate passes

The new stage retains more information from the binary event that a pair is causally comparable. It still accounts for dependence between pairs in the same cloud. Its KL intervals are never wider than the previous reference. Mathematically justified coverage of at least 95% holds under the same known model assumptions and a prespecified fixed data budget.

The protocol was public before the new calculations. Sufficient planning budgets improve by factors of 2.71 to 2.77 at all three prespecified curvatures. At h=0.5, for example, the count is 31,707 instead of 85,871 independent clouds of 128 points. These are sufficient boundaries for the tested procedures, not proven statistically optimal minimum counts.

77,824 fresh clouds were calculated and fully replayed. At h=0.5 with 16,384 clouds per estimate, all four KL intervals meet the relative 20% precision requirement; the old bound does so once. In the full 65,536-cloud dataset, the relative radius is 4.89% instead of 9.16%. Four groups cannot precisely estimate a success rate, and different group sizes reuse the same observations.

At smaller curvatures, the executed budgets still do not suffice. The prespecified upper model boundary helps at h=0.5. Unknown density and freely chosen stopping remain outside the guarantee; a flat model with different density can have the same relations. External proof review and replication are useful next steps. Further efficiency work needs finite-sample protection before additional large runs.

- [Results and precision limits](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d9bd4d0266faff0fddd70b4067ad4422367f25a1/research/lorentz_de_sitter_kl/RESULTS.md)
- [Derivation and protocol](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d9bd4d0266faff0fddd70b4067ad4422367f25a1/research/lorentz_de_sitter_kl/DERIVATION.md)

## Lower budgets through certified whole-cloud variance

The new stage uses the variability of whole point clouds. This is bounded analytically from the known geometry. The calculation explicitly counts dependence between pairs sharing a point; it does not treat an empirical variance estimate as a guaranteed population bound.

The Bennett bound retains at least 95% coverage in the known uniform model with a prespecified fixed budget. Sufficient budgets improve 2.89–4.10 fold against KL. At h=0.5 the count is 10,981 instead of 31,707 clouds; at h=0.1 it still reaches about 14.2 million. These are sufficient planning boundaries, not optimal minimum counts.

The protocol was public before the target calculations. 45,056 fresh clouds were fully replayed. At h=0.5 with 4,096 clouds per estimate, five of eight Bennett intervals meet the relative 20% target, compared with none of eight KL intervals. In the full 32,768-cloud dataset, the relative radius drops from 8.88% to 4.64%. Different group sizes reuse data, and small numbers of groups cannot precisely estimate a success rate.

A counterexample is retained: in one group of only 256 clouds, Bennett is wider than KL. The two intervals are not intersected or selected by observed width without additional protection. The certified budget gain does not imply that every reported interval is superior.

A separate sphere-lens volume calculation checks the new geometry. A review packet identifies proof obligations and possible errors for external scrutiny. Known density, independent clouds and fixed budgets remain required. The upper model boundary helps at h=0.5; small curvature remains difficult. The next question is how bounded density and time-scale errors affect precision qualification.

- [Results and counterexample](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/78a150f27fdf52187d140f9fcf440ce29c89cb48/research/lorentz_de_sitter_variance/RESULTS.md)
- [External review packet](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/78a150f27fdf52187d140f9fcf440ce29c89cb48/research/lorentz_de_sitter_variance/REVIEW.md)
- [Full derivation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/78a150f27fdf52187d140f9fcf440ce29c89cb48/research/lorentz_de_sitter_variance/DERIVATION.md)

## BD versus C2: why is the extension stopped?

The Benincasa–Dowker reference estimates curvature from event counts in small causal intervals. The completed pilot assumes known physical density and externally specified proper duration T=1 in four-dimensional Minkowski and de Sitter models. Point counts follow an actual Poisson distribution.

384 flat development clouds select smoothing; 6,144 separate clouds form twelve test cells. All 6,528 clouds were fully replayed, with 102 also checked by a second causal predicate. The protocol and sources were frozen locally in Git before the data. Publication follows the run; this is not public preregistration.

In the primary comparison, root mean square error (RMSE) is 14.924 for BD and 0.448 for C2, a ratio of 33.34. RMSE, bias, interval width and flat-bias criteria fail. Coverage and cost criteria pass. The decision is therefore NO_GO for variable-curvature expansion within this budget.

The conclusion has limits: C2 knows the de Sitter family and benefits from clipping at its upper model boundary. At the lowest density, BD has a smaller RMSE in three cells. Nominal Student intervals have no proven 95% coverage; even C2 misses the primary 20% width requirement. This comparison neither refutes the BD continuum limit nor establishes universal C2 superiority.

The original BK coefficient preflight has since been supplemented by a separate intrinsic phase-1/2 pilot, which also fails acceptance. Details follow below. The BD rule −2B(1) is still not a curvature formula for the constant-annihilating BK operator.

- [Results and limits](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/49710201cdb2e2941404266b25e88051a659b08e/research/lorentz_bd_reference/RESULTS.md)
- [Methods and protocol](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/49710201cdb2e2941404266b25e88051a659b08e/research/lorentz_bd_reference/METHODS.md)
- [Verification record](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/49710201cdb2e2941404266b25e88051a659b08e/research/lorentz_bd_reference/VERIFICATION.json)
- [BK phases 1/2: results](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/PHASE12_RESULTS.md)

## BK phases 1/2: what does intrinsic reconstruction deliver?

The local Boguñá–Krioukov pilot implements neighborhoods from longest chains and causal overlaps. Inference receives the causal order, known density and independent random marks for ties. Embedding coordinates are restricted to simulation and evaluation. This first pilot uses flat 2+1-dimensional Minkowski spacetime.

The protocol, followed by implementation and analysis, was publicly fixed before the corresponding data. Six development clouds precede 48 separate test clouds, 16 at each of three densities. Every test cloud was replayed. Product-identity, constant-field, affine-chart and three relabelling checks pass.

At the highest density, relative spatial distance error falls to 0.104, conditional on finding anchors. Meanwhile 87.8 percent of distance estimates are missing on average, and selection recovers only 15.1 percent of the desired local cap events. Good ranking of the remaining pairs therefore does not establish good neighborhood reconstruction.

Only 3 of 16 high-density clouds provide a usable operator. Relative metric RMS error is 3.110 with smooth coordinate fields and 5.524 with intrinsically constructed fields, against a limit of 0.5. Correct signature is obtained in 2 of 16 clouds in either chart. The decision is HOLD_PHASE3.

This is a negative finding for the bounded search and scale plan, not a counterexample to the BK continuum result. A follow-up requires improved search coverage, sufficient populations, a new protocol and fresh test data. The earlier BD-C2 NO_GO is unchanged.

- [Results / Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/PHASE12_RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/phase12/PROTOCOL.md)
- [Data / Daten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/phase12/results/summary.json)

## BK anchor search: more neighbors, but no accurate metric yet

On 19 October the search bottleneck was isolated using 48 fresh point clouds. Previously the code selected 64 anchors before checking their suitability. The revised arm applies the same suitability rules first and then retains up to 64 eligible anchors. The protocol and computational sources were publicly frozen before their respective data.

At the highest density, 16 of 16 clouds now supply usable neighborhoods, compared with 2 of 16 for the legacy search on the same new data. Recall of true neighborhood points rises from 11.5 to 94.9 percent. However, only 68.3 percent of all selected points actually lie within the intended neighborhood.

Metric RMS rises to 7.326 with the revised search, far above the original 0.5 limit. Selecting neighbors by exact simulation distances still yields 6.012. That diagnostic control is not an intrinsic method; it shows that better anchor coverage alone is insufficient. The report separately compares the subset available to both intrinsic methods.

All 48 new test clouds were fully replayed. The outcome is improved search coverage with HOLD_PHASE3 retained. The next step is to diagnose the temporal and spatial moments of the discrete stencil separately. Earlier data, the BD-C2 NO_GO and the terminated background runs remain unchanged.

- [Results / Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/research/lorentz_local_dalembert/anchor_audit/RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/research/lorentz_local_dalembert/anchor_audit/PROTOCOL.md)
- [Data / Daten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/research/lorentz_local_dalembert/anchor_audit/results/summary.json)

## BK moment diagnosis: shell proper times and reference directions

A further 48 fresh clouds test all eight prespecified combinations of three controls: corrected temporal endpoint proper times (T), constant proper time for all shell points (S), and a common time direction for endpoints and shell references (D). Membership is fixed within each arm. All interventions use known simulation coordinates and are diagnostic controls.

At the highest density both arms are available on all 16 clouds. With all controls, relative metric RMS falls from 7.387 to 2.267 with intrinsic neighbor selection, and from 5.893 to 1.002 with an exact distance cap. Both residual errors exceed the original 0.5 limit.

The full factorial allocation assigns substantially larger error reductions to S and D than to T. Temporal endpoints already have nearly correct proper times on average; shells have systematically larger proper times and substantial spread. The exact moment balance also accounts for cancellation between temporal and shell errors.

The prespecified diagnostic criterion passes, while Phase 3 remains on HOLD. At low density the combined control actually worsens the intrinsic arm. The next candidate is intrinsic shell calibration from causal interval counts, together with a study of common reference directions. This needs new development and fresh validation. All 48 clouds were fully replayed; earlier scientific files and the BD-C2 NO_GO remain unchanged.

- [Results / Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/research/lorentz_local_dalembert/moment_audit/RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/research/lorentz_local_dalembert/moment_audit/PROTOCOL.md)
- [Data / Daten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/research/lorentz_local_dalembert/moment_audit/results/summary.json)

## BK shell calibration: an intrinsic weighting improvement

The next trial counts events in causal intervals to estimate the proper time of each selected shell point and constructs inverse-square weights. Neighbors and reference directions stay fixed. The primary candidate requires only the causal order and known density, without embedding coordinates.

The protocol and computational sources were publicly frozen before their corresponding data. Five fixed arms were compared on 48 fresh clouds: original weights, interval weights for shells alone or shells and temporal endpoints, and two controls using exact proper times. The controls do not select different neighbors.

At the highest density the primary candidate reduces metric RMS from 7.089 to 3.765 and normalized affine-field drift from 3.692 to 2.882. All 16 clouds are available. All three prespecified improvement thresholds pass together; the secondary arm is not retrospectively promoted to the primary candidate.

Correct Lorentz signature is still obtained on only 8 of 16 clouds; absolute metric error remains above 0.5 and does not vanish over this density sequence. Phase 3 remains on HOLD. All 48 clouds were numerically replayed; coordinate byte hashes are reported separately. Common reference directions and the remaining first/second moments require a separate protocol and fresh test data.

- [Results / Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_local_dalembert/volume_shell/RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_local_dalembert/volume_shell/PROTOCOL.md)
- [Data / Daten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_local_dalembert/volume_shell/results/summary.json)

## BK: common reference directions and both moments

The new selector uses two existing temporal anchors to estimate a common reference frame from causal interval counts. Each shell chooses its closest reference point in that frame. The previous overlap-based caps and intrinsic shell weights are retained. Embedding coordinates do not enter the primary candidate.

Four prespecified arms are compared on 48 fresh clouds: original weights, the previous volume weights as baseline, the new intrinsic reference selector and a diagnostic selector using exact proper times. The diagnostic changes only selection times; cap distances and shell weights remain intrinsic. It is not an error lower bound.

At the highest density metric RMS changes 4.840 → 3.709, and normalized affine drift changes 3.271 → 3.085. The candidate is available on 16 of 16 clouds, with correct Lorentz signature on 14 of 16. The prespecified decision is COMMON_AXIS_HOLD. Both paired error ratios must improve by at least 25 percent; a closer reference direction alone is insufficient.

The protocol and computational sources, including analysis, were published before their respective data. All 48 target clouds were fully numerically replayed; coordinate byte identity is reported separately. Phase 3 remains on HOLD. Future hypotheses must address first and second moments together under a separate test protocol.

- [Results / Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/common_axis/RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/common_axis/PROTOCOL.md)
- [Data / Daten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/common_axis/results/summary.json)

## BK: joint moments are feasible on dense caps

After the failed reference-direction trial, the next diagnostic asks whether suitable weights on the existing points can simultaneously annihilate linear fields and reproduce the prescribed metric. It uses known simulation coordinates and the target metric. Matching polynomial responses are therefore constraints, not independent evidence for an intrinsic operator.

Two fixed support families are compared: existing caps and complete chain shells. Temporal weights are either fixed, freed with their signs retained, or all weight signs are freed. The objective minimizes total absolute weight. Feasible optima require checked primal and dual witnesses; infeasibility requires a separate separating witness.

At the highest density, 16 of 16 existing caps allow joint moments with unchanged negative temporal weights and nonnegative shell weights. All 16 also satisfy the prespecified mass bound. Mean minimum weight mass is 0.845 of baseline. At the lowest density the fixed rule succeeds on only 3 of 16 clouds; six caps are unavailable and seven have numerical infeasibility witnesses.

All 48 fresh clouds and every available linear program were fully replayed. Nonunique primal and dual vectors may differ, but each must be a valid witness with the same minimum objective. Dense supports leave room for better weight choices; deriving those weights without embedding coordinates and testing independent fields remain open. Phase 3 stays on HOLD.

- [Results / Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/5e164bdc0feaf529af34e019f43dfda949c47302/research/lorentz_local_dalembert/moment_feasibility/RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/5e164bdc0feaf529af34e019f43dfda949c47302/research/lorentz_local_dalembert/moment_feasibility/PROTOCOL.md)
- [Data / Daten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/5e164bdc0feaf529af34e019f43dfda949c47302/research/lorentz_local_dalembert/moment_feasibility/results/summary.json)

## BK: landmark rule fails before calibration

The next fixed trial derives a local frame solely from causal interval counts. Three landmarks are intended to provide the basis for a regularized moment fit. An additional count-noise guard rejects unstable fits. Every failure preserves the previous interval weights.

All 48 preregistered target clouds completed and were fully replayed. Six low-density neighborhoods are unavailable. Every one of the 42 available neighborhoods lacks an eligible landmark triple. Both intrinsic arms therefore adopt new weights on 0 of 48 clouds. At the highest density, all three error ratios remain 1.0; each had to be at most 0.75.

Twenty independent sine and cosine fields are evaluated only after construction. A diagnostic using known simulation coordinates reduces the highest-density field RMS from 27.652 to 0.964. This result belongs to the coordinate-assisted comparator and cannot qualify the unsuccessful intrinsic candidate.

INTRINSIC_MOMENT_HOLD and HOLD_PHASE3 remain. The result rejects this specific landmark rule in the tested regime. No target reached the noise guard, so its empirical effectiveness remains untested. Landmark availability must be examined before a new trial; this trial retains its frozen thresholds and data.

- [Results / Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/694dd9ec0409f35c9c6fd3e835ef187ada72c598/research/lorentz_local_dalembert/intrinsic_moments/RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/694dd9ec0409f35c9c6fd3e835ef187ada72c598/research/lorentz_local_dalembert/intrinsic_moments/PROTOCOL.md)
- [Data / Daten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/694dd9ec0409f35c9c6fd3e835ef187ada72c598/research/lorentz_local_dalembert/intrinsic_moments/results/summary.json)
- [Replay](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/694dd9ec0409f35c9c6fd3e835ef187ada72c598/research/lorentz_local_dalembert/intrinsic_moments/VERIFICATION.json)

## BK: Why a larger landmark search is insufficient

This diagnosis uses the 48 already observed clouds from the failed landmark trial. It is explicitly retrospective. Six neighborhoods remain unavailable; all 42 available supports are searched exhaustively.

Removing the 40-candidate cap still yields no admissible triple. At the highest density, the best minimum mutual interval count is only 2 instead of the required 8. For 31 of 42 neighborhoods, a necessary packing bound already proves impossibility: three sufficiently separated landmarks require at least 27 interior events before the outer boundary.

Restricting coverage to the root alone yields 16 of 16 cases at the highest density. This relaxation does not supply all distances required by the operator. Exact volume proxies from simulation coordinates also yield 0 of 42 full-support triples. Thus neither count noise alone nor the 40-candidate cap is a sufficient explanation on these clouds.

All 48 clouds were fully replayed. A new construction must address common coverage and sufficient causal depth, for example with more outer space or separately developed overlapping frames. This needs development, a public protocol and fresh targets. HOLD_PHASE3 remains; this diagnosis does not qualify a new operator.

- [Report / Bericht](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ac519f5e4a83de0e570680fe4cfeb2da133db351/research/lorentz_local_dalembert/landmark_availability/RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ac519f5e4a83de0e570680fe4cfeb2da133db351/research/lorentz_local_dalembert/landmark_availability/PROTOCOL.md)
- [Full replay / Vollständiger Replay](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ac519f5e4a83de0e570680fe4cfeb2da133db351/research/lorentz_local_dalembert/landmark_availability/VERIFICATION.json)

## BK: More outer space does not suffice for reconstruction

48 fresh point clouds were each examined in three nested diamonds. Inner points, supports, density, weights and acceptance rules remain identical; only independent outer Poisson points are added. Outer time durations 1, 1.25 and 1.5 were fixed in advance.

At the highest density, an unrestricted search finds qualifying landmark triples in 0, 10 and finally 16 of 16 cases. The outer boundary was therefore a real obstruction. In the largest variant, the unchanged 40-candidate search finds triples in only 13 cases; eight admissible frames result. None passes the unchanged stability guard.

All 42 available inner neighborhoods contain at least one required interval with fewer than 16 events. An interval between inner points lies entirely within the inner diamond, so adding outer points cannot increase its count. All eight selected frames also fail the condition-number bound for numerical stability.

The decision is OUTER_DIAMOND_HOLD. Further pure enlargements cannot rescue these fixed supports under the same rules. A successor campaign must first establish joint feasibility of support selection, required counts and stable frames. Adaptive supports and overlapping frames are possible new methods, but neither is validated here. HOLD_PHASE3 remains in force.

- [Report / Bericht](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/research/lorentz_local_dalembert/outer_diamond/RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/research/lorentz_local_dalembert/outer_diamond/PROTOCOL.md)
- [Full replay / Vollständiger Replay](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/research/lorentz_local_dalembert/outer_diamond/VERIFICATION.json)

## BK: Joint support, count and frame feasibility

The successor jointly selects temporal and other support points with a stable reference frame. Its three landmarks may come from both past and future; this is still one frame. The previous count and stability thresholds are unchanged.

| Density | Jointly selected | Also passes second colouring |
| --- | --- | --- |
| 2048 | 0/16 | 0/16 |
| 8192 | 1/16 | 1/16 |
| 32768 | 16/16 | 16/16 |

All 48 target clouds are fresh and generated after the computational sources were publicly frozen. A second random colouring of the same events remained hidden until selection was complete and could not trigger a retry. This tests sensitivity to that colouring; it is not independent physical data or a confidence guarantee.

At the highest density, frame conditions range from 17.5 to 24.8 below the unchanged limit of 100. Supports contain 15–32 events. The lower count-shell scale is about 11.4 percent above the old tau_m; temporal points and actual extent change separately. This is not a universal statement about operator resolution.

JOINT_FEASIBILITY_SUPPORTED means the joint prerequisites can be met in this dense 2+1 reference model. No new operator has been constructed. The next task is to check moment weights with controlled noise amplification before independent derivative tests. HOLD_PHASE3 remains in force.

- [Results / Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/4a6fe9c383e56b5a26f286fba6aa6d8c9263308a/research/lorentz_local_dalembert/joint_feasibility/RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/4a6fe9c383e56b5a26f286fba6aa6d8c9263308a/research/lorentz_local_dalembert/joint_feasibility/PROTOCOL.md)
- [Full replay / Vollständige Wiederholung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/4a6fe9c383e56b5a26f286fba6aa6d8c9263308a/research/lorentz_local_dalembert/joint_feasibility/VERIFICATION.json)

## Scalar series closed: testing the finite detector response next

The scalar CSPP series v0.1–v0.8 is closed for its specified sources, wavelengths, geometries and budgets. The independent G1 test uses 256 fresh clouds: 119 of 120 field/cell tests reject a necessary 10% condition, covering all twelve cells. G1 remains HOLD; Dirac is not cleared. This concerns these models and requirements, not every causal-set theory.

The new v0.9 development benchmark transfers the same fields to a spatially and temporally extended linear detector. Eight previously examined archive clouds produce 80 field/window responses. The method encloses causal boundaries, integration remainders, initial-history rounding and numerical solution errors. Sources and the spatial detector stay fixed; two new time windows are explicitly specified before the calculation.

The result is QUADRATURE_HOLD: 74 of 80 responses miss the declared integration tolerance. The other six responses are exactly zero because the compact H1 initial history contains no nonzero source datum on three clouds. Wide enclosures measure computational uncertainty and do not establish physical noise. Precision comparison, CPU comparison and full replay pass.

The next tasks are to improve detector integration and the compact initial-data adapter. Full spatial pair covariance and an independent fluctuation-transfer prediction remain open. Fresh confirmation clouds, a quantum-gravity interpretation, and mechanical or cosmological applications require their own prerequisites.

- [Closure / Abschluss](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/0ea645c9381979a55bc943f5f5ce1dcc4d39b6ca/research/cspp/detector_transfer_v0_9/CLOSURE.md)
- [Results / Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/0ea645c9381979a55bc943f5f5ce1dcc4d39b6ca/research/cspp/detector_transfer_v0_9/RESULTS.md)
- [Methods / Methoden](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/0ea645c9381979a55bc943f5f5ce1dcc4d39b6ca/research/cspp/detector_transfer_v0_9/METHODS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/0ea645c9381979a55bc943f5f5ce1dcc4d39b6ca/research/cspp/detector_transfer_v0_9/PROTOCOL.json)
- [Checks / Prüfungen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/0ea645c9381979a55bc943f5f5ce1dcc4d39b6ca/research/cspp/detector_transfer_v0_9/results/CHECKS.json)
- [Next step / Anschlussentscheidung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/0ea645c9381979a55bc943f5f5ce1dcc4d39b6ca/research/cspp/detector_transfer_v0_9/NEXT_STEP.md)

## Tighter detector integration and limits of local initial histories

CSPP v0.10 integrates time analytically along causal-cone arrival times. A parametrization with known volume weights covers the entire detector ball. The same eight known clouds, sources, wavenumbers and time windows are tested on three spatial grids specified before the runs. No new sprinklings are generated.

On the finest grid, the 74 nontrivial original intervals are roughly five to six times narrower than in v0.9. This also uses a larger spatial cell budget. Eleven of 80 original integration budgets pass: six zero signals plus five additional nonzero compact signals. All wave controls remain above tolerance. These intervals describe computational uncertainty, not measured quantum noise.

For compact initial data, separate H1/H3 error upper bounds now reach the detector observable. They qualify none of the 32 cases. Large upper bounds are not measured errors or error lower bounds. A separate structural limitation is decisive: all local derivatives vanish outside the compact source. Any finite local Taylor history therefore remains zero when the cloud misses the entire source support. Higher order alone cannot repair that information loss.

In the ideal Poisson model, the empty-history probability at the present density is exactly exp(-21/16), about 26.9 percent. This follows from the source-history region volume, rather than an estimate from eight clouds or a universal quantum-noise constant. A controlled nonlocal initial-data map and integration that better retains shared field dependencies are the next methodological tasks. METHOD_HOLD and G1 HOLD remain in force.

Nine analytic controls and 52,284 precision/CPU enclosure comparisons pass. A disclosed verifier correction removes the false requirement that differently computed error upper bounds enclose the same number. Frozen production sources, field comparisons, raw data and error budgets remain unchanged.

- [Results / Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ed481912b9330a09d02206beff6f6f535bb4ef85/research/cspp/detector_methods_v0_10/RESULTS.md)
- [Methods / Methoden](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ed481912b9330a09d02206beff6f6f535bb4ef85/research/cspp/detector_methods_v0_10/METHODS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ed481912b9330a09d02206beff6f6f535bb4ef85/research/cspp/detector_methods_v0_10/PROTOCOL.json)
- [Adapter limitation / Adaptergrenze](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ed481912b9330a09d02206beff6f6f535bb4ef85/research/cspp/detector_methods_v0_10/ADAPTER_OBSTRUCTION.md)
- [Checks / Prüfungen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ed481912b9330a09d02206beff6f6f535bb4ef85/research/cspp/detector_methods_v0_10/results/CHECKS.json)
- [Verifier amendment / Prüfkorrektur](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ed481912b9330a09d02206beff6f6f535bb4ef85/research/cspp/detector_methods_v0_10/VERIFICATION_AMENDMENT.json)
