# Data layout

All coordinates are float64 in (t,x,y,z) order, time-sorted, in L0 units.
All states/operator evaluations are complex128. Arrays are loaded using
`numpy.load(path, allow_pickle=False)`. JSON records contain no NaN.

For size-bounded GitHub transport, `reference.npz` is stored as four raw binary
parts, listed in `results/REFERENCE_ARCHIVE.json`. `prepare_reference.py`
reassembles and checks the exact original bytes. The audit and report call it
automatically. This is packaging only: no reference values, source locks or
scientific results change. The reconstructed file is generated and Git-ignored;
`run.py all --out /tmp/...` still writes the original complete NPZ directly.

- `clouds.npz`: `dD_rII` contains the inner Poisson cloud for density index
  D=0..3 and realization II=00..15. The eight `dD_rII_outer` arrays contain
  the same complete inner cloud plus its independently sampled Ω5\Ω4 shell.
- `RUNS.json`: all 64 planned identities, seed entropy vectors, counts,
  statuses, runtime and SHA-256 of contiguous array bytes. Counts use int32
  little-endian on the recorded platform and sentinel -1 for noncausal pairs.
  Dense interval matrices are rebuilt rather than archived.
- `metrics.npz/operator`: shape (4,16,3,32,10), axes density, realization,
  epsilon, probe, field. Field order is the six polynomial fields followed by
  four mass-1 waves, as listed in `RESULTS.json`.
- `metrics.npz/propagation`: shape (4,16,3,28,8). Columns 0..3 are
  manufactured waves k=0,2,4,8; 4..6 are the compact-source m=0,1,2 fields;
  column 7 is the response to unit history with m=1 and zero forcing.
- `metrics.npz/residual`: shape (4,16,3), maximum normalized algebraic
  backward residual over the mass blocks. It is not a forward error bound.
- `metrics.npz/outer_operator`: shape (8,3,32,10); outer-index mapping in
  `RUNS.json`. The same epsilon order (1,.25,.0625) applies throughout.
- `metrics.npz/probes`, `exact_phi`, `exact_box`: fixed 32 coordinates and
  corresponding analytical references. Probes 0..20 are the primary inner
  set, 21..27 the detector diagnostics, 28..31 the boundary diagnostics.
- `reference.npz/dD_rII_coarse` and `_fine`: (N,3) source-field reference
  amplitudes. Rows at t>=1 are **NaN because they were not evaluated** and
  are never used by the propagator. This is distinct from a failed run.
  `probes_coarse` and `probes_fine` contain 28×3 finite reference values.
  `query` archives the concatenated evaluated coordinates (inner clouds
  truncated at t<1, in run order, followed by the 28 probes).
- `RESULTS.json`: complete 12-cell matrix, primary normalized operator
  errors and propagation diagnostics. `DIAGNOSTICS.json` additionally gives
  all probe groups, source-reference disagreement and paired boundary changes.
- `REFERENCE.json` retains REFERENCE_HOLD; `COMPUTE.json` records resources
  and runtime versions. `AUDIT.json` reports software replay, not science gates.

No probabilities, density matrices, detector integrals or RGB are inferred
from these scalar amplitudes. Historical contract/source locks are not
rewritten by the results. `amendment_01` preserves the sampler correction
and the exact identity checks for all unaffected primary arrays.
