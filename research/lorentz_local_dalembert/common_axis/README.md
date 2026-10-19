# Common-axis reference trial

Fixed protocol: `5f05a0a3374e7337138f851d5fde8761da8438a1`.

The coordinate-blind selector reconstructs a common endpoint rest-frame time
from six interval counts, then selects each shell reference by minimum absolute
estimated squared transverse displacement divided by squared proper time.
`axis_shell` is the only primary candidate; `volume_shell` is its fixed baseline.
The exact-time reference selector is a diagnostic comparator only.

Six development clouds completed with software controls passing. No change to
the mathematical rule, seeds, thresholds or parameters followed development.
The source and analysis freeze precedes all target seeds. Development data are
not target evidence and are retained in `development/`.

Run from the repository root with NumPy/SciPy versions pinned by
`research/lorentz_bd_reference/requirements-replay.txt`:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/common_axis/axis_controls.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/common_axis/verify_axis.py
```

`run_axis.py --mode test --output <new-directory>` refuses existing output and
verifies all computational sources against HEAD before generating targets.
The replay checks all targets, source/record hashes and the full summary.
Numeric agreement and coordinate byte identity are separate results.

Time-reversal controls transport the existing root, endpoints and shell sets;
they test the candidate rule and assembled weights conditional on that stencil,
not invariance of the inherited marked-chain midpoint under reversal.
The oracle retains the same positive-count eligibility requirement and changes
only the six scalar times used in reference selection. Tiny negative *exact*
h values are rounded to zero only when displaying diagnostic rapidities, never
in the selector or weights. Always HOLD_PHASE3.
