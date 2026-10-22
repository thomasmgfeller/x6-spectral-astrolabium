# Eligibility before candidate cap: fresh paired test — HOLD

**22 October 2026. Selection logic corrected; the new-cloud benefit is too small
for the frozen gate. Full-order operator qualification remains 1/32.**

The early cap diagnosed in [PR #86](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/86)
was a real search limitation. The corrected selector first checks causal
comparability and full/half interval counts, then keeps the first 128 eligible
points per direction. It retains the same geometry gates and ranking. Every
previously accepted candidate remains available; this follows from the stable
prefix-subset argument in [PROTOCOL.md](PROTOCOL.md).

That deterministic improvement is distinct from its practical effect on unseen
data. The independent campaign completed 32 new A clouds and 180 distinct B
clouds: 162 paired old/new records plus 18 candidate-only records, or 342 arm
records in total. Old and new arms share the same A and the same B points; the
fourth landmark changes on 15 of the 18 common selected A configurations.
All failures are retained, and no settings were changed after observing data.

## Frozen primary results

| Quantity | Old selector | Eligibility before cap | Decision |
|---|---:|---:|---|
| Selected A frames / 32 | 18 | 20 | Fails required 26 |
| Gained / lost selections | — | 2 / 0 | Fails required >=6 gains |
| One-sided paired exact tail | — | 0.25 | Fails <=0.05 |
| Full-order qualified B0 / 32 | 1 | 1 | Fails required 26 |
| Common computable B0 pairs | 17 | 17 | Passes >=16 |
| Operator RMSE, same 17 pairs | 1.730823 | 1.728230 | Ratio 0.998502; essentially unchanged |
| IID field-noise variance, same pairs | 1.820263 | 1.752905 | Ratio 0.962995 |
| Complete paired B1..B8 groups | 12 | 12 | Fails required 16 |
| Mean repeat response variance, those 12 groups | 7.119152 | 6.305466 | Ratio 0.885705 |
| Candidate B0 covariance calibration | — | 16 groups; empirical/predicted 1.131310 | Bounded variance check passes |
| Selector time, median / max seconds | 0.0375 / 0.0661 | 0.0593 / 0.2879 | Within 2 / 5 second limits |

The 11.43% lower repeat variance is descriptive on 12 complete paired groups,
not a validated population improvement. Candidate covariance calibration uses
16 candidate-only eligible groups; these are a different subset from the 12
paired comparison groups. Its passing ratio is not a confidence-interval
coverage result and does not lift the embedding-covariance HOLD.

All-available B0 RMSE is 1.741812 for 19 computable candidate cases and
1.730823 for 17 old cases. These different subsets cannot establish a paired
accuracy improvement. Across all B replicates the old arm has 149 valid-weight,
11 count-HOLD and 2 unresolved records; the candidate has 168 valid-weight,
8 count-HOLD and 4 unresolved records. Valid weights alone do not establish
causal-order consistency. Complete machine-readable decisions and per-case
values are in [analysis.json](analysis.json).

**SELECTION_HOLD and OPERATOR_HOLD.** The corrected selector is available as a
versioned research implementation; historical frozen evidence is unchanged.
HOLD_PHASE3, HOLD_EMBEDDING_COVARIANCE and METADATA_HOLD remain. No curved/3+1,
physical-sensor, Kalman, global-optimizer or uncertainty-coverage qualification.
The previously rejected Poisson/GLS estimators are not revived by this trial.

## What the remaining failures show

[Post-freeze descriptive diagnosis](failure-diagnosis.json), reproduced by
`diagnose.py`, identifies the next concrete limitations:

- Ten configurations have **no count-eligible fourth point** anywhere in the
  complete tested common cones for their frozen root/support/first-three
  landmarks. Expanding the cap alone cannot repair these ten cases.
- Two configurations fail the inherited hidden-colour base audit before the
  fourth-landmark search. They are retained as failures.
- All **60 distinct mismatched primary pairs** of the 19 computable candidate
  systems involve support/support relations. The improved landmark search
  does not resolve the support-geometry reconstruction problem.

Across 30 base-audit-passing A clouds, 75,650 candidates were inventoried:
70,147 incomparable, 3,749 below full-count threshold, 6 below half-count
threshold, and 1,748 count-eligible. Some successful configurations have more
than 128 count-eligible points per side (maximum 440), so geometry search is
still capped there. The ten failed fourth-landmark cases have zero eligible
points, so their count-feasibility exhaustion is complete **within this fixed
family only**. It does not exclude other support/landmark families.

A future experiment should jointly choose the first three and fourth landmarks
with support feasibility in view, then independently test operator geometry.
This is a next hypothesis, not a tested rescue or permission to relax gates.

## Reproducibility and checks

The local freeze at 2026-10-22T09:51:32.196658+00:00 contains 82 code/configuration/
control/provenance hashes. The contract fixed seeds, budgets, metrics and gates
before the first new A/B cloud. This is **not public preregistration**. An initial
import-name collision stopped before entering the campaign; its original
sources/freeze/log are archived in `preflight-import-abort.zip`. The module was
renamed, imports checked and source refrozen. No data attempt was replaced;
see [PRE_DATA_CORRECTION.json](PRE_DATA_CORRECTION.json).

Seven synthetic controls pass, including 32,764 exhaustive finite prefix cases,
an exact-geometry early-cap counterexample, full/half-count negative controls,
moment rejection and node relabeling. The fixture is not a Poisson draw.

The [post-run audit](verification.json) passes for all 317 valid-weight systems,
761 accepted candidate frames and all 75,650 inventory entries. Maximum direct
moment residual is 1.36e-10; relative alternate weight-solve difference is
1.36e-9; covariance reconstruction difference is 3.55e-15. The original A
simulation and B0 counts replay exactly on configurations 0 and 31. All 32 A
hashes differ from 64 prior A hashes, and 180 B hashes differ from 504 prior B
hashes. This is internal verification, not an external Sage/Wolfram replication.

The two workers finished all 16 attempts each in 332.9 and 338.0 seconds, within
their fixed 1800-second/3000-MiB limits. Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0;
one BLAS thread. Raw observations, complete overlap matrices, propagated
covariances, failure witnesses, full selected orders, sealed truth bindings,
worker logs and decision scripts are included.

From the repository root, use a fresh environment and run:

```sh
python -m pip install -r research/lorentz_local_dalembert/eligibility_before_cap/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research/lorentz_local_dalembert/eligibility_before_cap/ci_check.py
```

This checks evidence hashes, reruns controls, reproduces the frozen analysis,
performs the alternate algebra/inventory audit and replays the first/last A and
B0. The Lorentz BD GitHub workflow now includes this specific audit job;
technical CI success is compatible with the recorded scientific HOLD.

For a full campaign replay without overwriting evidence:

```sh
python research/lorentz_local_dalembert/eligibility_before_cap/prepare_replay.py /tmp/eigenzeit-eligibility-replay
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
python /tmp/eigenzeit-eligibility-replay/eligibility_before_cap/runner.py 0
python /tmp/eigenzeit-eligibility-replay/eligibility_before_cap/runner.py 1
python /tmp/eigenzeit-eligibility-replay/eligibility_before_cap/analyze.py
python /tmp/eigenzeit-eligibility-replay/eligibility_before_cap/verify.py
```

The worker commands may run concurrently with sufficient memory. Inference
and data should reproduce; wall-clock times and container paths may differ.
The complete parent [PR #86 CI record](PARENT_CI_COMPLETION.json) is included;
this publication triggers new CI and cannot inherit its completion status.
