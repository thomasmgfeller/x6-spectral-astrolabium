# Metadata-conditioned, moment-preserving operator correction

**Completed evidence: 32/32 records, 29 complete measurements; METADATA_HOLD.**
The [results](RESULTS.md) show transfer RMSE reductions of 3.18% before and
0.26% after relation projection. Both miss the frozen 5% improvement target;
both primary 95% cloud-bootstrap intervals include no improvement. The
scientific HOLD is independent of the resource telemetry gap described below.

The original public numerical freeze is `3f6109f4bfb9424352893406e0ba92ddfe6ef858`.
After an operational interruption, the [resumption procedure](RESUMPTION.md)
was frozen at `69f989dc19172c938ce0e2afc7ff6c6e808eea4c`. All 27 original
records remain byte-identical in `interrupted_clouds.zip`, including three
without guarded support. Only missing seeds 70210027–70210031 were computed,
with unchanged numerical sources, calibration and statistical criteria.
`continuation_clouds.zip` contains those five records and their execution logs;
`test_clouds.zip` is the lossless combined archive. `checkpoint.json` remains
the historical interruption record, not the current completion status.

**Original process total time and peak RSS are unknown.** The original execution
and budget gates remain UNVERIFIED (boolean false), regardless of the complete
record set. `summary.json` separates measured continuation values from explicit
lower bounds and unknown full measurements. The original RUNNING execution
logs are preserved unchanged; combined logs say RESUMED_COMPLETE.

Five control groups, the full calibration refit and the local strict numerical
replay pass. All 32 coordinate bytehashes match locally. Passive
[matrix diagnostics](matrix_diagnostics.json) find no row-rank loss among the
58 available moment matrices. They examine stored endpoints, not every solver
iteration, and do not define a stochastic geometry measurement Jacobian.
The [embedding-covariance audit](EMBEDDING_COVARIANCE_AUDIT.md) documents the
separate prerequisites for covariance-weighted relation repair. **HOLD_PHASE3.**

Follow-up to [conditional noise and relation repair](../conditional_geometry/RESULTS.md).
This pilot tests a restricted version of adaptive bias compensation: weights
change in the nullspace of the reconstructed moment equations. Constants,
linearity and quadratic moment conditions are preserved; conditional field-noise
variance is recomputed and capped at 1.25 times the corresponding original arm.

Read the [frozen protocol](PROTOCOL.md), [contract](contract.json), and
[fitted calibration](frozen_model.json). All previous 96 clouds are development:
64 for fitting, 32 for residual calibration. The test uses 32 new seeds, six
seen probe fields and four untrained transfer probes. All splitting and
resampling is by cloud. No embedding covariance or online qualification.
The relation projection is unchanged and isotropic. **HOLD_PHASE3.**

Reproduce controls from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 python -B research/lorentz_local_dalembert/metadata_bias/test_controls.py
```

Replay the published resumed evidence:

```sh
OPENBLAS_NUM_THREADS=1 python -B research/lorentz_local_dalembert/metadata_bias/resume_evidence.py --verify
```

The adapter assembles the two raw archives in a temporary directory, checks all
original bytes and source hashes, and invokes the unchanged frozen verifier.
Only resource reporting/gates are conservatively overridden; all statistical
metrics and gates use the original analyzer. It also replays the passive matrix
diagnostics. Portable CI output uses an ignored `.local.json` file, preserving
the published local strict replay record.
Add `--strict` for exact sampler coordinate bytehashes; the default numerical
replay explicitly counts bytehash mismatches and uses predeclared tolerances.
Neither mode repeats the expensive full frame search. To regenerate that search,
use a separate checkout of the pre-test freeze and run `mb_run.py --shard 0`
and `mb_run.py --shard 1`, then `mb_analyze.py`. Existing evidence is never replaced.
Python 3.12 and the pinned NumPy/SciPy dependencies in
`research/lorentz_bd_reference/requirements-replay.txt` are the reference runtime.

The mathematical construction and all selection choices are in PROTOCOL.md.
This is a bounded experimental design, not a novelty or convergence claim.

The full training/model-selection/residual-calibration replay is recorded in
`calibration_verification.json`. To repeat it, use a separate checkout, move its
`frozen_model.json` and `residual_calibration.zip` aside, run `mb_calibrate.py`,
and compare the regenerated model parameters and CV scores with the original.
This repeats the same implementation; it is not an external validation.
