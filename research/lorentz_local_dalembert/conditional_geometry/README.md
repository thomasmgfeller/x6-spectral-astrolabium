# Conditional field noise and relation-compatible reconstruction

Continuation of the [original Feynman/Kalman pilot](../feynman_combiner/CALIBRATION_RESULTS.md).
See [results and limitations](RESULTS.md), [frozen protocol](PROTOCOL.md),
[machine-readable contract](contract.json), and [complete metrics](summary.json).

The exact conditional IID field-noise covariance is computed separately from
clean-response error variation across clouds. A convex inner approximation
repairs missing and extra relations on root/support points, then recomputes and
certifies the operator weights. All original relation labels are retained.
The exact observed order and known field-noise level are assumptions.

All 64 previous clouds are reused as development, explicitly including previous
test clouds. Calibration has 60 joint complete cases. The evaluation uses 32
new independent seeds, after public source/calibration freeze
`b5f8abc48fb74f426247ef77b4b265a77e63b72c`. No seed replacement or test tuning.
Failures remain in availability denominators and use prior-only fallback.

This is an offline scalar one-step study, not a full embedding filter, verified
geometry covariance, online method, or curvature qualification. **HOLD_PHASE3.**

From repository root, with Python 3.12, NumPy 2.3.5 and SciPy 1.17.0:

```sh
python -m zipfile -e research/lorentz_local_dalembert/conditional_geometry/test_clouds.zip research/lorentz_local_dalembert/conditional_geometry
OPENBLAS_NUM_THREADS=1 python -B research/lorentz_local_dalembert/conditional_geometry/test_controls.py
OPENBLAS_NUM_THREADS=1 python -B research/lorentz_local_dalembert/conditional_geometry/verify.py
```

The replay regenerates sampler coordinates, counts every used causal interval
independently, checks QP certificates, repeats the relation correction, and
recomputes fields, noise and statistics. It does not repeat the full frame search.
Summary discrete outputs must match exactly; floating outputs use the disclosed
absolute 1e-10 plus relative 1e-9 tolerance. Coordinate hashes are exact here.
The later verification/presentation additions do not change frozen inference,
calibration or test gates.

For full search regeneration, use a separate checkout of the source freeze
without existing test directories, and run `cg_run.py --shard 0` and
`cg_run.py --shard 1`, followed by `cg_analyze.py`. Calibration can be rebuilt
with `cg_calibrate.py` after moving the existing generated calibration aside
in that separate checkout. No existing evidence is overwritten by the runners.

The standard convex-cone background is described by
[Lobo, Vandenberghe, Boyd & Lebret (1998)](https://stanford.edu/~boyd/papers/socp.html).
No novelty, global solver certificate or external replication is claimed.
