# Coordinate-byte portability: preserved failure and bounded repair

Date: 2026-10-17. This is a **post-run software portability addendum**.
It does not change the frozen experiment, the first-run archive, seeds,
thresholds, sample sizes or either failed scientific sensitivity gate.

## Observed failure

The original strict replay passed on the originating runtime and again in
a fresh local checkout. GitHub Actions job
[117506531208](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/39070367903/job/117506531208)
then verified the original and fresh archives and reproduced the fitted
models and scientific summaries, but failed the first coordinate-byte hash
comparison: `all records/0/points_sha256 value`.
The [complete failing log](results/ci-coordinate-failure.log) is retained.
The subsequent records had not yet been compared when that check stopped.
Consequently the failed job alone does not establish full record equality.

NumPy CPU dispatch provides a directly reproduced mechanism for this
failure. Disabling AVX512F changes the first cloud hash while changing its
largest coordinate difference by only 8.326672684688674e-17. A SHA-256 hash
detects those changed bytes; it does not measure their numerical size.
The first job does not identify its exact CPU instruction path, so the
dispatch explanation for that remote job remains an inference until its
hashes match the explicitly checked variant in the supplementary replay.

## Complete coordinate comparison

`coordinate_portability.py` reconstructs every original cloud using the
unchanged source and archived seed. It first requires the original byte hash
and every packed causal relation to agree. It retains those coordinates in
a temporary array, then starts a new interpreter with
`NPY_DISABLE_CPU_FEATURES=AVX512F` and compares **every coordinate**.

- 8,702 clouds and 835,392 four-dimensional points compared.
- Maximum absolute coordinate difference: 2.220446049250313e-16.
- Supplementary absolute tolerance: 1e-14 in the fixed coordinate units.
  This software tolerance was introduced after the portability failure;
  it is not a prospectively specified scientific test threshold.
- 8,696 coordinate hashes change; six remain identical.
- All full causal relations and proposal counts remain identical.

The resulting [finite hash inventory](results/coordinate-variant.json.gz)
binds the original records archive and source commit. It lists only the
directly checked per-case alternatives. It is an internal computational
check, not a formal rounding-error proof or independent external replication.

## Two distinct replay claims

The original `reproduce.py`, `verify.py`, geometry, statistics, contract and
all other frozen sources remain byte-identical to `31cfd8c`.

1. `reproduce.py` still demands the original coordinate bytes and reports
   `PASS_FULL_CURVATURE_REPLAY` only if that stricter condition holds.
2. `reproduce_portable.py` reruns the unchanged experiment and retains the
   original checks for full relations, all features, seeds, proposal counts,
   fitted banks, scores, p-values, decisions, summaries and source hashes.
   For each coordinate hash it accepts only the original hash or that
   case's explicitly bounded alternate hash. Unknown hashes fail. It reports
   the accepted variant count and `PASS_PORTABLE_CURVATURE_REPLAY` separately.

The supplemental matcher rejects an unknown coordinate hash, a hash moved
to a different case, and a changed packed relation. It does not discard
coordinate provenance or broadly ignore floating-point fields. Existing
numeric comparison tolerances in the frozen verifier remain unchanged.
The CI entry now runs this supplementary replay, followed by the source
inventory. The original strict checker remains available for auditing.
Other CPU/library paths may still fail rather than being silently accepted.

```sh
# Scientific replay with only explicitly verified coordinate variants:
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_curvature/reproduce_portable.py

# Original, stricter byte-identical replay:
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_curvature/reproduce.py

# Recreate the supplementary inventory on the original compatible runtime:
python3 -B research/lorentz_curvature/coordinate_portability.py /tmp/new-coordinate-variant.json.gz
```

**Deutsch:** Der ursprüngliche GitHub-Check scheiterte an einer
Koordinaten-Prüfsumme. Alle Punktwolken wurden zusätzlich zwischen zwei
NumPy-Rechenpfaden verglichen; die größte Abweichung beträgt etwa 2,22e-16,
bei identischen Kausalrelationen. Der ergänzte Replay akzeptiert nur diese
konkret geprüften Varianten. Originalcode, Rohdaten und wissenschaftliches
Negativergebnis bleiben erhalten. Das ist eine dokumentierte technische
Nachbesserung nach dem Versuch, keine neue Präregistrierung.
