# Scaling repair: jacobi-scale-1

The original failure is preserved in [the historical evidence](../README.md).
This change repairs the finite graph eigensolver; it does not change the exact
rational LDL certificates or the archived research source pins.

## Arithmetic changes

1. Form `B = L / max(abs(L_ij))`, handling the exactly zero matrix separately.
2. Apply Jacobi rotations to `B`. Use `hypot` in the rotation and residual norms
   to avoid avoidable squaring overflow/underflow.
3. Stop on off-diagonal magnitude relative to the infinity norm of `B`.
4. Recompute Rayleigh quotients and residuals against `B`, independently of the
   overwritten working diagonal. Scale eigenvalues and residuals back to input units.
5. Report convergence only when the iteration criterion, a dimensionless residual
   check and Frobenius orthogonality check all pass their stated tolerances.

Nonfinite matrices or results are rejected. The original input parser still limits
graphs to 120 vertices. Extremely different weights may lose entries during
normalization; `normalizationUnderflowCount` exposes that loss. A small backward
error does not imply that every tiny positive eigenvalue is resolved.

`positiveGap` uses the exact component count to index the first positive mode.
It reports `UNRESOLVED_AT_TOLERANCE` if its estimate is at or below `1e-12` times
the matrix infinity norm, or `NO_POSITIVE_MODE` for an empty positive spectrum.
`RESOLVED_AT_TOLERANCE` is a numerical diagnostic, not an interval certificate.

The internal historical `version: X6-2.4` string belongs to the existing aggregate
analysis format. `numerical.solverVersion: jacobi-scale-1`, source commit and source
hash identify this numerical revision unambiguously.

## Verification

`tests/numerics/verify_frozen.py` loads the original evaluator and controls directly
from the immutable check-3 ZIP. Numeric tolerances and inputs are unchanged.
Only the source-envelope check is rebound to the new target source. The original
contract still names its original commit, and its hash is retained in each result.

The regression runner re-executes the archived old kernel and requires its known
failure to reproduce, then checks the repaired implementation across scales and
the adjacent binary64 values below, at and above the old stopping threshold.
It also tests the zero matrix, unresolved gaps, normalization underflow, nonfinite
input/result rejection and the 120-vertex limit.

The Chromium workflow fills the actual iframe textarea, clicks Analyze, compares
all 27 displayed spectra with the independent references, downloads three JSON
results and compares their complete contents with the displayed reports. Invalid
input must clear the previous export so stale results cannot be downloaded as the
new analysis. Existing application, Sagnac and Signal Lab checks run separately.

Run from repository root:

```sh
python3 tests/numerics/verify_frozen.py --output numerics-evidence
node tests/numerics/test_regression.cjs > numerics-evidence/regression.json
node tests/numerics/browser.cjs numerics-evidence
```

The browser test requires Playwright; the workflow pins its dependency. Local
development may use `--allow-working-tree`, but published qualification must bind
the unchanged application bytes to an actual source commit. Future broader tests
remain distinct from the frozen 27-case acceptance.

## Active integration pin

The active math-agent app checksum is updated to the exact reviewed repaired app.
Its schedule, limits, seed and research algorithms are unchanged.
`tests/numerics/preservation.py` proves byte equality outside `spectrumFrame` and
of the extracted FFT/filter and signal-to-graph functions against the archived app.
The Signal Lab original 17-file baseline remains immutable; a new exact two-file
amendment binds the repaired app and matching configuration. Tamper-rejection
tests remain enabled. This is a checksum rebind, not a fresh research-agent run.
