# Coordinate replay portability repair (PR97)

SPDX-License-Identifier: Apache-2.0

The original coordinate hashes identify raw float64 arrays. A GitHub replay
failed that byte-level check although the exact selection payload agreed.
Locally disabling NumPy AVX512 dispatch reproduced changed raw hashes on both
replayed A clouds. In 3,769 / 3,783 coordinate components the floating results
changed, with maximum absolute difference 1.1102230246251565e-16. Differences
near a cancellation can span many local ULPs, so an ULP-relative threshold is
not suitable here. The CPU-dispatch experiment reproduces the failure mode;
it does not by itself identify the precise CPU of the failing GitHub runner.

The four verification fixtures recover complete A/B0 arrays for clouds 0 and
31. Every raw array exactly matches its PRE-EXISTING published coordinate
SHA-256. The compressed files merely preserve those verified bytes; no original
evidence, source seeds, coordinate hash or scientific gate is rewritten.
These coordinates are verification-only and do not enter the research inference.

Fresh replay now checks every coordinate against that exact hash-verified
reference with absolute tolerance 2^-50 in simulator units (8 times the largest
observed native-versus-disabled difference). Only then is the fresh coordinate
provenance field normalized for the existing structural comparison. Runtime
and reference hashes and the observed maximum difference are printed whenever
bytes differ. Exact byte identity is no longer claimed for cross-CPU generation.

Crucially, relation hashes, selected IDs/packets, B interval-bit hashes,
integer counts, overlaps and all scientific decisions STILL have to agree
exactly in the existing verifier. A coordinate difference beyond the bound,
a changed discrete measurement, a corrupted reference, NaN, wrong shape or
wrong dtype fails. This is numeric replay with exact measurement agreement,
not acceptance of arbitrary mismatching hashes. Archived evidence hashes remain
strict integrity checks. The pre-existing tolerance for two condition diagnostics
is unchanged.

Controls exercise small roundoff, excess perturbations, nonfinite data and
shape/dtype changes. Both native and AVX512-disabled full legacy CI paths are
run before publication; GitHub CI provides the final platform check.
