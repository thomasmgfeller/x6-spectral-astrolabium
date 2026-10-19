# Larger outer diamonds restore triples, not guarded reconstruction

19 October 2026. **OUTER_DIAMOND_HOLD; HOLD_PHASE3 remains in force.**
All 48 fresh target clouds completed at three nested outer durations: 144
paired variants. Six low-density stencils are unavailable; all 42 available
inner stencils are retained, with unchanged supports, density, weights,
marks, colours, inner scale, count thresholds and stability requirements.

## The outer-domain intervention works at the combinatorial level

At the primary density rho=32768, each denominator includes all 16 clouds:

| Outer duration T | Full-support triple exists, uncapped | Triple in original 40-candidate search | Admissible Lorentz frame | Raw calibration adopted | Guarded calibration adopted |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1.00 | 0/16 | 0/16 | 0/16 | 0/16 | 0/16 |
| 1.25 | 10/16 | 0/16 | 0/16 | 0/16 | 0/16 |
| 1.50 | 16/16 | 13/16 | 8/16 | 8/16 | 0/16 |

Every uncapped positive result has a stored explicit threshold-eight witness.
Negative results exhaust all eligible middle vertices and predecessor/successor
pairs. At densities 2048 and 8192, uncapped triple availability remains zero
at every tested outer duration (10/16 and 16/16 available stencils respectively).

This paired intervention establishes that the outer-domain restriction is a
real finite-sample obstruction to triple existence at high density. It does
not establish reconstruction accuracy. The original 40-candidate cap becomes
a further bottleneck in the enlarged domain, although it was not the cause
of failure on the original supports inside D(1). The two findings are compatible.

## An invariant inner obstruction remains

All **42/42 available inner stencils** have at least one root-to-support
interval with fewer than the guard's required 16 physical interior events.
The minimum full counts per cloud range from 2 to 4 at rho=2048, 3 to 7 at
rho=8192, and 5 to 14 at rho=32768.

For fixed a,b in the closure of the original causal diamond, including its
labelled endpoints when used as probes, transitivity gives

    p <= a < b <= q  implies  I(a,b) subset I(p,q) = D(1).

Adding Poisson points only outside D(1) therefore cannot change N(a,b), or
either of its fixed half-colour counts. Every such inner count was checked
at all three durations. Consequently **no purely outer enlargement can make
these same 42 stencils pass the unchanged full-interval guard**, even beyond
the tested T=1.5. This is a conditional obstruction for these fixed supports
and this declared guard; it is not a universal physical minimum-count theorem.

The eight selected frames at T=1.5 also all fail the condition-number bound
of 100. All eight fail the full and half-count gates, six fail Gram stability,
and one fails a half-sample Lorentz-signature check. Thus fixing only inner
count availability would not by itself qualify the observed frames.

## Independent fields and the frozen decision

At rho=32768, T=1.5, paired RMS ratios to the identical volume-shell baseline
are computed over all 16 available clouds, including every fallback:

| Method | Independent fields | Metric error | Affine drift | Adopted |
| --- | ---: | ---: | ---: | ---: |
| Intrinsic raw, diagnostic | 0.822288 | 0.793120 | 0.837192 | 8/16 |
| Intrinsic guarded, primary | 1.000000 | 1.000000 | 1.000000 | 0/16 |

The fixed primary requirements were at least 13/16 guarded adoptions and all
three guarded ratios <=0.75. Availability passes; adoption and all three
error gates fail. Even the unguarded diagnostic arm misses each 0.75 ratio.
Raw improvement is not a licence to remove the guard after observing results.
All stored calibration certificates and algebra checks pass; this verifies
the computations, not the scientific success criteria.

## Reproduction and provenance

- Protocol published before development: `43df0adeb08cbe7095fc991d140cd1c96ae32327`.
- Initial implementation: `91e212aed9ac87a8f15a672a2fb15642cf50730e`.
- Final computational freeze published before targets: `4c7442dcc239c23f57dd9105d2a2d0bc28031c5e`.
- All six development clouds replay identically after the component-wise
  relation optimization; the 18 relation/mark/colour hashes agree. Both
  development generations are retained. Streaming checksum controls verify
  the subsequent removal of a full-matrix checksum copy. See
  [development record](DEVELOPMENT.md) and [development replay](DEVELOPMENT_VERIFICATION.json).
- Target batch: **376.236 seconds**, **1329.453 MiB** peak RSS; limits were
  1800 seconds, 2048 MiB and 35000 augmented points per cloud.
- Independent controls include 3600 scalar relation comparisons, 393 direct
  interval counts, exclusion of 24 artificial-probe interior incidences,
  60 brute-force finite orders, sampler moments and 500 shell-count checks,
  plus inherited calibration/algebra and enlarged-cloud transport checks.
- [Full replay evidence](VERIFICATION.json) records all 48 clouds and 144
  variants, exact discrete decisions and separate coordinate-byte comparisons.

Run from the repository root with the complete Git history and pinned replay
requirements installed:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/outer_diamond/verify_outer.py
```

Full [contract](contract.json), [protocol](PROTOCOL.md),
[execution manifest](results/execution.json), [summary](results/summary.json)
and per-cloud records are included. Old artificial endpoints remain labelled
probes when needed; they never contribute to Poisson interval counts. No
coordinates or evaluation fields enter intrinsic inference.

## Decision

Close pure outer enlargement as a remedy for these frozen supports and the
unchanged guard. Do not spend another target batch only enlarging T or lifting
the candidate cap: neither can change the demonstrated inner-count obstruction.

Before a successor experiment, jointly check intrinsic support selection,
all required interval counts and frame conditioning for feasibility. Adaptive
supports could address the inner-count issue but change the operator and
resolution. Multi-frame reconstruction could address common coverage and
conditioning but does not automatically repair insufficient inner counts.
Both require separately specified methods, development data and fresh tests;
neither is validated here. Known density, flat 2+1, locality, convergence,
3+1, curvature and external replication remain the existing claim boundaries.
