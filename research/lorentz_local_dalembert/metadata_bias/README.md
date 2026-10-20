# Metadata-conditioned, moment-preserving operator correction

**Checkpoint: interrupted after 27/32 clouds; no final analysis.**
The public pre-test freeze is `3f6109f4bfb9424352893406e0ba92ddfe6ef858`.
24 recorded clouds have complete measurements; three lack guarded support.
Seeds 70210027–70210031 are still missing. The tool interruption ended both
processes before their finalizers; the original RUNNING execution logs are
preserved byte-for-byte in `interrupted_clouds.zip`. See `checkpoint.json`
for record hashes and explicit limitations. No final transfer improvement,
runtime-budget pass, or new scientific qualification is claimed.

Implemented controls and full calibration refit pass. The new test is incomplete;
the previous scientific HOLD remains. The [embedding-covariance audit](EMBEDDING_COVARIANCE_AUDIT.md)
documents the separate prerequisites for covariance-weighted relation repair.

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

After result artifacts are published:

```sh
OPENBLAS_NUM_THREADS=1 python -B research/lorentz_local_dalembert/metadata_bias/verify.py
```

The verifier extracts the archived test files without overwriting differences.
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
