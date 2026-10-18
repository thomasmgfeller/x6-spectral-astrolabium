# Local d’Alembertian: independent reproduction track

**Status: source audit and coefficient preflight only. No intrinsic reproduction
or curved-space estimator has yet been completed.** Run `python3 -B
research/lorentz_local_dalembert/preflight.py` to check the final assembly.

Boguñá & Krioukov, [Phys. Rev. D 113, 024046, 22 January 2026](https://doi.org/10.1103/np89-qzjp),
[arXiv:2506.18745v1](https://arxiv.org/abs/2506.18745v1), construct local
neighborhoods from intrinsic temporal and spatial distances. Their numerical
example uses 2+1-dimensional Minkowski space and a scalar-field derivative.
Equations 86–88 assemble temporal and spatial differences. The constant-field
test is exactly zero by construction, so the BD rule -2 B(1) cannot simply be
transferred to this operator to obtain curvature. The simulation's selection
of a central reference event uses a coordinate-based boundary safeguard;
an independently intrinsic reproduction must distinguish this from inference.

## Proposed acceptance sequence

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

This track is separate from the BD finite-budget NO_GO. Its full implementation
is not smuggled into the completed BD benchmark. No changed-curvature run is
authorized by the preflight result. Apache-2.0 original coefficient assembly.
