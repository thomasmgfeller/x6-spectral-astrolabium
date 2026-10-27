# Scalar-pilot v0.1: explicit CPU-portability qualification

This companion records a CI finding during publication of CSPP variance v0.4.
It does not change the original v0.1 sampler, archives, audit, tolerances or
scientific gates. The general seed-to-coordinate **bitwise** claim is not met.

The first PR #136 run failed in the unchanged historical audit at
`seed replay d0_r00`:
[failed scalar-pilot job](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/40584916654/job/122473706296).
Locally, the original audit replays all 64 clouds with exact coordinate bytes on
the default CPU path. Disabling AVX-512 reproduces a coordinate-byte mismatch;
the first cloud differs by at most 8.881784197001252e-16 L0. This is the same
class of NumPy arithmetic-dispatch limitation documented for v0.2 in PR #135.

`STREAMS.json` is an explicitly **post-failure** diagnostic capture of RNG-call
outputs on a CPU path reproducing every original inner and outer coordinate
byte. It is not a previously archived raw random stream. The frozen sampler is
executed unchanged; the wrapper records outputs before subsequent transformations.

The new replay contract separately requires:

- Exact hashes of canonical archived coordinates and unchanged primary arrays.
- Exact RNG-call output hashes for all 64 inner clouds and eight paired shells.
- Finite coordinates, matching shapes, and the existing v0.2 engineering screen
  of 2^-48 L0. This screen is not a theorem about exact-real geometry.
- Exact hashes of all regenerated full interval-count matrices, all probe-count
  matrices, and all outer probe-count matrices.
- Exact membership of the active and prescribed-history time regions.
- The original operator/propagation tolerances (absolute 1e-10, relative 1e-11),
  original backward-residual bound 1e-12, original Fourier-probe tolerances and
  exact summary equality.
- All 14 original independent controls and six additional negative controls
  covering archive corruption, excessive coordinate displacement, count changes,
  wrong seeds and changed history membership.

Both local CPU configurations run the complete numerical replay. The result is
`PASS_NUMERIC_REPLAY_NOT_GENERAL_BITWISE_REPRODUCIBILITY`; it does not assert
portable coordinate bytes. All scientific claims remain unchanged: **G1 HOLD**,
no independent confirmation seeds, no certified full E4 or source-reference result.

The default local path reproduces all historical coordinate bytes and all
operator/propagation values exactly. The baseline CPU path retains exact counts
and memberships, with maximum operator difference 9.0994e-13 and maximum
propagation difference 3.8854e-12, within the unchanged original tolerances.

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B \
  research/cspp/scalar_pilot_portability_v0_1/replay.py --output /tmp/pilot-replay.json
NPY_DISABLE_CPU_FEATURES=AVX512F,AVX512_SKX,AVX512_CLX,AVX512_CNL,AVX512_ICL \
  OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B \
  research/cspp/scalar_pilot_portability_v0_1/replay.py --output /tmp/pilot-baseline.json
```

The existing CI package-integrity guard remains in place. CI uses this explicit
numeric companion in both modes; the original bitwise audit remains available
and unchanged for a compatible CPU path. See `results/DEFAULT.json` and
`results/BASELINE_CPU.json` for all per-cloud comparisons and runtime features.
This is a documented qualification of the replay claim, not a silent change to
historical evidence or a mathematical acceptance tolerance.

NumPy documents CPU-dependent dispatch in its
[runtime-dispatch documentation](https://numpy.org/doc/2.4/reference/simd/build-options.html).
The actual comparison uses the pinned NumPy 2.3.5 build and its feature names;
no guarantee from a newer version is assumed.
