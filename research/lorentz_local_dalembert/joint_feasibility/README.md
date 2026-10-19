# Joint intrinsic support/count/frame feasibility

This bounded 2+1 Minkowski study tests whether adaptive supports and a single
Lorentz frame can simultaneously meet the unchanged interval-count and
thinning-stability guards. It follows the [outer-diamond obstruction](../outer_diamond/RESULTS.md).

- [Results and scope](RESULTS.md)
- [Protocol](PROTOCOL.md) and [fixed constants](contract.json)
- [Development history](DEVELOPMENT.md)
- [Fresh-cloud summary](results/summary.json)
- [Complete local replay](VERIFICATION.json)

Public final computational freeze, before the fresh targets:
`8717861f6c2f13371e8bb5a5deaf5597be9d5688`.
Initial public protocol: `8647afdc5177600251faf2cc08e3674568d6b5ee`.

The root and marked chain remain fixed. Both temporal and other supports are
chosen by count scale. Landmark triples may combine past and future events;
every required interval remains causal and physically counted. The original
full-count 16, half-count 4, Gram condition 100 and stability 0.25 guards remain.
The auxiliary second colouring is hidden until the support/frame selection is
complete and cannot trigger retries. It is not an independent physical sample.

## Reproduce

Use Linux/POSIX, Python 3.12, g++/C++17 and a complete repository history.
From the repository root:

```sh
python3 -m pip install -r research/lorentz_bd_reference/requirements-replay.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/joint_feasibility/verify_joint.py
```

The verifier checks the public computational source, stored certificates,
direct interval-count oracles and every fresh cloud. Discrete selections and
relations must agree exactly; floating-point comparisons use the predeclared
tolerance. Coordinate-byte hashes are reported separately. Runtime must remain
within 1,800 seconds and peak RSS within 2,048 MiB on the reference platform.

## Boundaries

Adaptive supports change resolution and any future operator. Rank nine of a
quadratic design does not prove that sign-constrained moment weights exist or
that their noise amplification is acceptable. No differential operator is
calibrated in this experiment. Derivative accuracy, intrinsic metric recovery,
locality/convergence, 3+1 and curvature remain open; `HOLD_PHASE3` remains.

A failed capped search is not an impossibility theorem. A successful witness
is conditional on the declared geometry, known density, count thresholds and
two auxiliary colourings; it is not a uniform robustness or confidence guarantee.
