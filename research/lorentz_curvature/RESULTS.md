# Krümmungsbenchmark: Empfindlichkeit verfehlt, Dichteverwechslung exakt

Date: 2026-10-17. **Scientific result:** both prespecified primary sensitivity
gates fail. The joint chain statistic warns in 118/512 strongly curved targets
(23.05%); longest-chain height warns in 5/512 (0.98%). The exact conformal-twin
construction independently rules out universal curvature identification from
order alone when sampling density is unrestricted. A quiet diagnostic is not
a geometry certificate. This is not a physical Planck-scale clock or a
validated curvature sensor.

**Deutsch:** Der vorab festgelegte Versuch mit 8.702 unabhängigen Ordnungen
ist vollständig ausgeführt. Beide Diagnosen verfehlen das verlangte
Empfindlichkeitskriterium. Alle 3.072 gekoppelten Dichtezwillinge liefern bei
unterschiedlicher wahrer Krümmung und Eigenzeit dieselbe Ordnung und dieselben
Entscheidungen. Damit ist ein universeller „Rauchmelder für Krümmung“ ohne
zusätzliche Kenntnis der Beprobung nicht begründet.

## Public freeze and execution

The [complete source and contract](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/31cfd8ca832cffe67942cd198eb2d9d260765f62) were publicly
available at `31cfd8ca832cffe67942cd198eb2d9d260765f62` before the first target invocation.
GitHub's commit timestamp is `2026-10-17T21:04:57Z`; the recorded first-run
start is `2026-10-17T21:05:12.010383+00:00`. This is a public prospective source freeze,
not registration with an independent study registry. The [design](DESIGN.md),
[contract](contract.json) and nine executable/design source hashes in
[provenance](results/provenance.json) were not changed after target inspection.
No target seeds, thresholds or sample sizes were added or replaced.

There are 256 training, 1,023 calibration and 6 × 512 independent target
orders at each of N=64 and N=128: 8,702 independent orders in total. Each
order is conditional on exactly N internal points. This is the conditional
Poisson law, not a random Poisson count. The complete packed relations,
features, coordinate hashes, seeds, proposal counts and scores are in
[records.json.gz](results/records.json.gz). Training and calibration data are
retained alongside every target; paired checks are not extra independent trials.

## Prespecified primary decision

Primary cell: N=128, de Sitter h=1.25, versus uniform flat sampling.
Each method must have conditional null-warning upper bound ≤5% and
conditional alternative-warning lower bound ≥80%. The four selected
one-sided Clopper–Pearson endpoints share a Bonferroni family error of 5%
(1.25% per selected endpoint). The table gives those endpoints, not ordinary
pointwise 95% intervals.

| Method | Flat warnings | Flat upper bound | Curved warnings | Curved lower bound | Decision |
|---|---:|---:|---:|---:|---|
| Joint C2/C3/C4 statistic | 10/512 (1.95%) | 3.82% | 118/512 (23.05%) | 18.99% | Sensitivity not established |
| Longest-chain height | 1/512 (0.20%) | 1.24% | 5/512 (0.98%) | 0.27% | Sensitivity not established |

Both methods satisfy the flat-warning requirement and fail the sensitivity
requirement. Both statuses are `PRIMARY_SENSITIVITY_NOT_ESTABLISHED`.
This is not evidence that all possible detectors fail; it is a failed gate
for these two frozen methods at this finite budget and geometry.

The calibration bank is shared within each N. The intervals describe fresh
independent target draws **conditional on this realized training and bank**.
They do not establish an independent binomial proof of the marginal nominal
2.5% rank level. The two methods are not independent; their union is not a
2.5% test. This experiment does not validate continuous interactive peeking.

## Every target cell

All denominators are 512. Brackets are descriptive, pointwise 95%
Clopper–Pearson intervals for conditional warning rates. They are not a
simultaneous assertion across this table.

| N | Family | Joint warnings and rate [95% interval] | Height warnings and rate [95% interval] |
|---:|---|---|---|
| 64 | `flat_uniform` | 10/512; 1.95% [0.94, 3.56]% | 0/512; 0.00% [0.00, 0.72]% |
| 64 | `de_sitter_025` | 11/512; 2.15% [1.08, 3.81]% | 0/512; 0.00% [0.00, 0.72]% |
| 64 | `de_sitter_075` | 29/512; 5.66% [3.83, 8.03]% | 2/512; 0.39% [0.05, 1.40]% |
| 64 | `de_sitter_125` | 69/512; 13.48% [10.64, 16.74]% | 1/512; 0.20% [0.00, 1.08]% |
| 64 | `flat_spatial_compression` | 510/512; 99.61% [98.60, 99.95]% | 220/512; 42.97% [38.63, 47.38]% |
| 64 | `flat_time_mask` | 0/512; 0.00% [0.00, 0.72]% | 0/512; 0.00% [0.00, 0.72]% |
| 128 | `flat_uniform` | 10/512; 1.95% [0.94, 3.56]% | 1/512; 0.20% [0.00, 1.08]% |
| 128 | `de_sitter_025` | 14/512; 2.73% [1.50, 4.55]% | 0/512; 0.00% [0.00, 0.72]% |
| 128 | `de_sitter_075` | 28/512; 5.47% [3.66, 7.81]% | 1/512; 0.20% [0.00, 1.08]% |
| 128 | `de_sitter_125` | 118/512; 23.05% [19.47, 26.94]% | 5/512; 0.98% [0.32, 2.26]% |
| 128 | `flat_spatial_compression` | 512/512; 100.00% [99.28, 100.00]% | 389/512; 75.98% [72.03, 79.62]% |
| 128 | `flat_time_mask` | 13/512; 2.54% [1.36, 4.30]% | 5/512; 0.98% [0.32, 2.26]% |

The flat spatial-compression control changes x to x/2, with curvature still
zero. Its high warning rate is sensitivity to a sampling-model violation,
not a curvature hit. The flat time-mask control exposes limited response to
a different observation disturbance. Paired joint-only/height-only counts
are retained in [summary.json](results/summary.json); no superiority test was
prespecified or claimed. These controls are distinct from the earlier proper-
time study's spatial compression by 0.1 and its 506/512 warning count.

## Exact reference and the density twin

The metric is g=a(eta)^2 diag(-1,1,1,1), a=1/(1-h eta), on the fixed
coordinate diamond |x|<1/2-|eta|. The curved sampler is uniform in the
physical volume measure a^4 d eta d^3x. The independent true endpoint clock
is tau=2 atanh(h/2)/h, with tau=1 at h=0. Scalar curvature is R=12 h^2.
Neither the metric parameter nor this reference clock is a detector input.

| h | True endpoint proper time | Scalar curvature R | R tau² | Diamond volume |
|---:|---:|---:|---:|---:|
| 0.00 | 1.000000000 | 0.00 | 0.000000 | 0.130899694 |
| 0.25 | 1.005257713 | 0.75 | 0.757907 | 0.132279414 |
| 0.75 | 1.051276480 | 6.75 | 7.459980 | 0.144630854 |
| 1.25 | 1.173069655 | 18.75 | 25.801733 | 0.179630658 |

The strongest case is an exact de Sitter stress test, not a small-curvature
approximation. Only positive constant curvature is studied; this does not
cover general curvature or Weyl curvature.

For each curved cloud, interpret its identical coordinates under the flat
metric and density proportional to a^4. The true curvature becomes zero
and the endpoint proper time becomes 1, but the sampling law and full order
remain identical. All 3,072 coupled twins match, including every relation,
feature, score and decision. Independent norm-based and squared-cone predicates
agree. The analytic construction in [DESIGN.md](DESIGN.md) proves equality
of order laws; the 3,072 checks test its implementation, not the probability
of a theorem. The ambiguity also persists for unconditioned Poisson processes
if the flat intensity measure matches the curved volume measure.

Therefore the overall status is
`NOT_IDENTIFIABLE_WITH_UNRESTRICTED_SAMPLING_DENSITY`.
Additional independent knowledge of the sampling law is necessary for a
geometrical attribution. Adding order-only features cannot remove this exact
ambiguity.

## Verification and reproduction

- [Geometry and software self-check](selftest-output.json): rational Ricci
  contraction; independent volume and time integration; exhaustive small
  chain counts and relabelings; separate cone predicates and sampler checks.
  Development seeds are separate from target seeds.
- [Archived evidence verification](results/verification.json): 8,702 full
  orders, 26,106 independent chain-count identities, 12,288 ranks, 3,072
  conformal twins and 1,024 deliberately broken transitive relations.
  Every planted relation error was refused before scientific scoring.
- [Original run log](results/run.log) and [complete isolated replay](results/replay.log):
  full records, coordinate hashes, packed relations, scores and scientific
  summaries reproduced. Timing/environment fields are excluded from equality.
- [Archive checksums](results/hashes.json) bind the five original run outputs;
  the repository source inventory additionally binds this report and the
  later verification/replay logs. Earlier proper-time archives are unchanged.

The original target run took 25.05 seconds and peaked at 148,776 KiB RSS
on the recorded Linux environment, within the 600-second and 2-GiB limits.
This observation is not an industrial performance benchmark. Software and
replay status is `PASS_FULL_CURVATURE_REPLAY`; scientific sensitivity remains
failed. Internal verification and CI replay are not external replication.

## Consequences for the proposed clock and “smoke detector”

The flat-model proper-time estimator retains its declared validity domain.
This study supplies known curved reference times, not a calibrated curved-
spacetime time estimator. Relabeling simulated units as Planck units adds no
physical measuring capability. No physical Planck clock has been built.

A future interactive demonstrator can honestly show volume sampling, causal
relations, the two conditional diagnostics and a side-by-side conformal twin.
Its alarm must be called a **model-deviation warning**. Repeated-look error
control would require a separate prospective sequential contract. A slider
must not display the old 98.8% figure as curvature detection performance.

Before another efficacy study, declare what independent sampling/volume
information is available and what geometrical parameter is identifiable.
Then freeze a new design with explicit alternatives, budgets and independent
test data. Increasing N or retuning these methods would be a new study;
neither is used to rescue the present outcome. External replication of this
complete evidence remains open.
