# Intrinsic landmark moment calibration

Public protocol before development:
`e20dcf39979a3d19848f95122f5ba7cf94dbc180`.

This fixed experiment derives a local calibration frame from interval counts
and three pairwise comparable landmarks in a common past or future. It keeps
the accepted volume-shell caps and temporal weights. A strictly convex soft
moment fit limits absolute coefficient mass; a conditional two-colour count
stress test guards adoption. All failures fall back explicitly to the unchanged
volume-shell baseline. The true-coordinate arm is diagnostic only.

The inference module imports only NumPy, itertools and math. Simulator
coordinates and the 20 independent validation fields are accessed only after
inference. Known density, dimension 2+1 and a flat model remain assumptions.
Remote landmarks do not establish locality, and conditional thinning is not
a statistical confidence interval or an independent geometry sample.

Six development clouds completed with software and optimization checks passing.
One has no baseline stencil; the other five have no qualifying landmark
candidates on either side. The rule, parameters and gates were not changed
after this finding. The implementation, development records and analysis are
published before any target cloud is generated. Fresh targets must report
unavailability and fallback even if all adoption gates fail.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/intrinsic_moments/verify_intrinsic.py
```

Use the existing pinned `research/lorentz_bd_reference/requirements-replay.txt`.
`run_intrinsic.py --mode test --output <new-directory>` refuses overwrite and
checks every computational source against HEAD. The replay independently checks
stored and recomputed optimization certificates. It compares final weights and
feature invariants; eigenvector signs and iteration counts are not observables.
Earlier baseline tolerances and historical scientific files are unchanged.

The adopted-weight fraction uses all clouds as denominator; paired error scores
use the same available baseline supports and include fallback unchanged. Mean
coefficient mass bounds bounded field-difference errors. The squared coefficient
sum including the root describes ideal independent equal-variance additive
noise only. Neither quantity establishes measured robustness.

Always HOLD_PHASE3. A failure here rejects this specific landmark rule and
support/threshold combination, not intrinsic moment calibration in general.
