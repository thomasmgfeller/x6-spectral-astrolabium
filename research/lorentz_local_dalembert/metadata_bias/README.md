# Metadata-conditioned, moment-preserving operator correction

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
