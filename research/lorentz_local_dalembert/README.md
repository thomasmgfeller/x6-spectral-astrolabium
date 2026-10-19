# Local d’Alembertian: independent reproduction track

**Current status (19 October 2026): moment controls informative; `HOLD_PHASE3`.**
A second publicly frozen follow-up tests temporal scale, shell proper times and
reference directions in all eight combinations on 48 fresh clouds. At the
highest density the metric RMS falls from 7.387 to 2.267 with all three controls;
with exact cap selection it falls from 5.893 to 1.002. Both exceed the inherited
0.5 limit. Shell and direction controls explain much more reduction than
endpoint-time calibration. These interventions use simulation coordinates;
no new intrinsic estimator is qualified. At low density the combined control
can worsen the error. Read the [moment diagnosis](moment_audit/RESULTS.md),
including complete factorial results, uncertainty and full replay.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/moment_audit/verify_moments.py
```

**Earlier anchor audit (19 October 2026): coverage improved; `HOLD_PHASE3`.**
A publicly frozen paired follow-up on 48 fresh clouds fixes the search-cap
ordering problem. At the highest density, usable neighborhoods rise from 2/16
to 16/16 and true-cap recall from 11.5% to 94.9%. Selection precision is only
68.3%, however, and metric RMS is 7.326 (limit 0.5); exact cap selection still
gives 6.012. This is a coverage improvement, not metric qualification.
Read the [anchor-search audit](anchor_audit/RESULTS.md), including paired
comparisons, controls, uncertainty and the full replay.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/anchor_audit/verify_audit.py
```

**Original phase-1/2 pilot (18 October 2026), retained below:**
The bounded 2+1 Minkowski pilot includes longest chains, causal-overlap spatial
neighborhoods, the BK operator, product-identity metric extraction and an
exploratory intrinsic chart. All 48 held-out clouds have been replayed. Scientific
acceptance fails: at the highest density only 3/16 clouds provide a usable
stencil; relative metric RMS errors are 3.110 for smooth coordinate fields and
5.524 for intrinsic fields, against the prespecified 0.5 limit. No curved-space
estimator or continuum-limit reproduction is established.

Read [results and limitations](PHASE12_RESULTS.md),
[the publicly frozen protocol](phase12/PROTOCOL.md) and
[implementation decisions](phase12/IMPLEMENTATION.md). The original
`PREFLIGHT.json` is retained as a historical assembly-only result.

```sh
python3 -m pip install -r research/lorentz_bd_reference/requirements-replay.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/phase12/verify.py
```

Requires Python 3.12, NumPy, SciPy, a C++17 compiler and full Git history.
Expected software result: `PASS_NUMERICAL_REPLAY`, 48 clouds. Expected scientific
decision: `HOLD_PHASE3`. Coordinate hashes are reported separately from numerical
agreement; the local archived replay matches all 48. Marks travel with events
in relabelling controls; no canonical frame of an unmarked poset is claimed.

Boguñá & Krioukov, [Phys. Rev. D 113, 024046, 22 January 2026](https://doi.org/10.1103/np89-qzjp),
[arXiv:2506.18745v1](https://arxiv.org/abs/2506.18745v1), construct local
neighborhoods from intrinsic temporal and spatial distances. Their numerical
example uses 2+1-dimensional Minkowski space and a scalar-field derivative.
Equations 86–88 assemble temporal and spatial differences. The constant-field
test is exactly zero by construction, so the BD rule -2 B(1) cannot simply be
transferred to this operator to obtain curvature. The simulation's selection
of a central reference event uses a coordinate-based boundary safeguard;
an independently intrinsic reproduction must distinguish this from inference.

## Research acceptance sequence (historical plan, now partly implemented)

1. Implement longest-chain proper time with explicit edge/vertex convention,
   relabelling invariance, finite-density bias and independent replay.
2. Implement the cited causal-overlap spatial-distance construction. Coordinates
   may evaluate errors but may not select estimator neighborhoods. Record empty
   neighborhoods and boundary failures, without silent replacement.
3. Freeze new development/test seeds and a compute budget before target runs.
   Test constants, affine fields, temporal/spatial quadratics, mixed terms and
   smooth exponential fields. Keep dimensions and scale regimes explicit.
4. Compare error, uncertainty, failures and costs over a density sequence with
   physical neighborhoods shrinking while their populations increase. A single
   finite-density PASS cannot establish convergence.
5. Only after a successful flat reproduction, specify curved benchmarks and
   the precise continuum target. Curvature extraction needs a separate argument.

This track is separate from the unchanged BD finite-budget NO_GO. The new
phase-1/2 implementation does not retroactively alter that benchmark. Phase 3
remains stopped by the new pilot's own gates. Apache-2.0 original implementation.
