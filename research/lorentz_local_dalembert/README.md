# Local d’Alembertian: independent reproduction track

**Latest bounded result:** [Joint support/count/frame feasibility](joint_feasibility/RESULTS.md) passes all guards and a hidden second colouring on 16/16 fresh high-density clouds (0/16 low, 1/16 middle). Adaptive temporal and other supports, mixed past/future landmarks in one frame, unchanged acceptance thresholds. No operator weights or derivative qualification; **HOLD_PHASE3**.

**Latest trial (19 October 2026): larger outer diamonds; `OUTER_DIAMOND_HOLD`.**
The [paired outer-domain trial](outer_diamond/RESULTS.md) completed 48 fresh
clouds at three nested durations, with identical inner supports and unchanged
guards. At the highest density, uncapped triple availability increases from
0/16 at T=1 to 10/16 at T=1.25 and 16/16 at T=1.5. The original capped search
provides 13/16 triples and 8/16 admissible frames at T=1.5, but 0/16 pass the
guard. All 42 available inner stencils contain a required interval with fewer
than 16 events; causal convexity makes these counts invariant under every
pure outer enlargement. All eight selected frames also fail the condition
bound. Raw diagnostic RMS ratios are 0.822/0.793/0.837; guarded ratios are 1.0.
More outer space alone cannot qualify this construction. `HOLD_PHASE3` remains.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/outer_diamond/verify_outer.py
```

**Previous diagnosis: landmark coverage audited; `HOLD_PHASE3`.**
The 48 archived intrinsic-calibration clouds were examined retrospectively and
fully replayed. Exhaustive uncapped searches still yield 0/42 full-support
triples; exact finite-poset packing bounds certify 31/42 failures. At the
highest density the largest achievable minimum mutual count is 2 (required 8).
Exact-volume proxies also yield 0/42. Root-only relaxation yields 16/16 at high
density but cannot supply the original support distances. Increasing the
candidate cap alone cannot rescue this fixed construction. Read the
[availability diagnosis](landmark_availability/RESULTS.md), including all
conditional relaxations, witness records and limits. This is not fresh
validation or a new operator.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/landmark_availability/verify_audit.py
```

**Preceding trial (19 October 2026): `INTRINSIC_MOMENT_HOLD`; `HOLD_PHASE3`.**
The fixed landmark calibration trial completed 48 fresh target clouds. All 42
available stencils lack an eligible landmark triple; six low-density stencils
are unavailable. Both intrinsic arms adopt 0/48 and fall back unchanged. At the
highest density, all three paired error ratios are 1.0 (required <=0.75).
The count-noise guard is never reached on these targets. The true-coordinate
oracle improves independent fields but is diagnostic only. Read the
[intrinsic-calibration report](intrinsic_moments/RESULTS.md) and full replay.
This closes the specified candidate; it does not rule out intrinsic calibration.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/intrinsic_moments/verify_intrinsic.py
```

**Earlier joint-moment feasibility (19 October 2026):
`CAP_MOMENT_FEASIBILITY_SUPPORTED`; `HOLD_PHASE3`.**
A new publicly frozen coordinate-assisted diagnostic tests six fixed
support/sign policies on 48 fresh clouds. At the highest density,
16/16 original caps permit simultaneous first/second moments with fixed negative
temporal weights and nonnegative shell weights; 16/16 have minimum absolute
weight mass at most twice baseline. Mean minimum-mass ratio: 0.845.
These are fitted constraints using known coordinates and metric, not intrinsic
metric validation. Read the [feasibility report](moment_feasibility/RESULTS.md)
for all policies, certificates, noise-bound limits and full numerical replay.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/moment_feasibility/verify_feasibility.py
```

**Earlier common-axis trial (19 October 2026): `COMMON_AXIS_HOLD`;
`HOLD_PHASE3`.**
A new public protocol selects both shell reference directions in a common
endpoint frame, using only causal interval counts and known density. Four arms
were tested on 48 fresh clouds. At the highest density, the primary candidate
changes metric RMS 4.840 → 3.709 and normalized affine drift
3.271 → 3.085. Correct Lorentz signature: 14/16.
The joint gate requires both errors to improve by 25%; see the
[common-axis report](common_axis/RESULTS.md) for the decision, all denominators,
reference rapidities, exact-time diagnostic and full numerical replay.
Earlier scientific records remain immutable. No flat/curvature qualification.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/common_axis/verify_axis.py
```

**Earlier shell-weight trial (19 October 2026): intrinsic shell weighting improves the
bounded comparison; `HOLD_PHASE3`.**
A new publicly frozen trial uses causal interval counts to set inverse-square
shell weights, retaining the same neighbors and reference directions. On 48
fresh clouds, the primary candidate passes all three improvement gates. At the
highest density, metric RMS falls 7.089 → 3.765 and normalized affine drift
3.692 → 2.882; all 16 clouds are available. Correct Lorentz signature improves
1/16 → 8/16, still insufficient, and metric error remains above 0.5. No embedding
coordinates enter the candidate; exact-time oracle comparators are separate.
Read the [intrinsic shell-weight report](volume_shell/RESULTS.md) for all five
arms, field responses, limits, uncertainty and full numerical replay.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/volume_shell/verify_volume.py
```

**Earlier moment audit (19 October 2026): controls informative; `HOLD_PHASE3`.**
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
