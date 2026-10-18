# Bitwise and numerical reproduction

The original `verify.py`, source-fixation commit, contract and data remain
unchanged. The original environment passed `PASS_FULL_REPLAY` for all 6,528
clouds and 102 independent causal-predicate checks.

The first GitHub run on another host rejected two floating-point operator
values: maximum absolute difference 2.84217094e-14 and relative difference
6.30369105e-16. This is a failure of the original cross-platform bitwise
requirement, not a passed GitHub replay. See
[the original failed run](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/39161389391).

`replay_portable.py` is a separate, explicitly numerical verifier added after
that observation. It retains exact archive and frozen-source SHA-256 checks,
replays every seed, and requires exact Poisson counts, sampler proposal counts,
per-point interval counts and discrete metrics. A second causal predicate
checks the same 102 clouds. Smoothing selection and the final decision are
recomputed and must agree exactly. Both use recomputed operator outputs.

Only finite floating-point fields may differ by at most
`1e-10 + 1e-12 * abs(reference)`. This is a software portability tolerance,
not a statistical error bar or a theorem bounding all machine arithmetic.
It is many orders below the declared scientific screening thresholds.
Negative controls reject a 1e-6 numerical mutation, integer and boolean
changes, a changed decision and nonfinite output. It does not change the
scientific selection, budget, hypotheses or acceptance gates.

Coordinate byte hashes are reported separately. Since the original archive
contains hashes rather than coordinate arrays, a mismatched coordinate hash
cannot establish coordinate-wise numerical agreement. Such a run certifies
replayed integer interval counts and numerical results, not byte-identical
coordinates. The report explicitly states how many hashes match; zero
mismatches must not be assumed.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_bd_reference/replay_portable.py
```

The expected successful status is `PASS_PORTABLE_NUMERICAL_REPLAY`, distinct
from the frozen `PASS_FULL_REPLAY`. The documented bootstrap warning remains
visible. Neither is external scientific replication.
