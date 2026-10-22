# Baseline numerical replay portability

SPDX-License-Identifier: Apache-2.0

PR98 job 119935291884 passed coordinate/reference comparison but failed the
byte-exact `baseline_selected` assertion. The existing PR97 fix covers raw
coordinate arithmetic, not the derived baseline eigensolver/SVD outputs.

Reproduction: NumPy AVX512 disabled, OPENBLAS_CORETYPE=Haswell and one BLAS
thread. On cloud 0 the only differences from the archive are:

| Field | Changed values | Maximum absolute difference |
|---|---:|---:|
| certificate.transform | 4 | 8.882e-16 |
| certificate.features | 47 | 8.327e-17 |
| certificate.guard.halves[].gram_error | 2 | 3.192e-16 |
| certificate.guard.halves[].feature_error | 1 | 1.388e-17 |
| design.condition | 1 | 3.553e-14 |
| design.singular_values | 9 | 1.776e-15 |
| point_feature_errors | 24 | 3.053e-16 |

`replay_baseline.py` permits the existing 1e-12 relative/absolute numerical
replay tolerance ONLY for these explicit paths and the eigenvalue/condition paths observed in cloud 31. It checks finite float values,
identical container shapes and types. Every other path remains exact, including
root, landmark/support IDs and order, all interval counts, raw Gram/vectors,
scale and scale ratio, ranks, statuses, guard booleans and reasons. Numeric
differences are logged by path with their maximum magnitude. The scientific
selection and decision code is unchanged and runs before this comparison.

Negative controls reject changed IDs/counts/ranks/gates, a scale change of
1e-14, a condition change of 1e-6, NaN and changed array length. The complete
legacy CI is tested on native and Haswell/AVX512-disabled paths. No archived
evidence, simulation, measurement model or scientific threshold is modified.
This supersedes the blanket byte-equality statement for these derived baseline
fields in CI_REPLAY_PORTABILITY.md; its narrower legacy-fourth comparison is
unchanged. The repaired remote replay must pass before merging.

Failure: https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/39810546367/job/119935291884

Cloud 31 additionally changes certificate.eigenvalues (maximum 3.331e-16)
and certificate.condition (1.066e-14). Its largest difference across all
allowed fields is 9.948e-14 in design.condition. Both complete path-level
difference inventories are archived in baseline_portability_audit.json.

The same cloud 31 also changes only the funnel's minimum_lorentz_condition
from 18.097868124632 to 18.097868124631997. This explicit path uses the same
numerical comparison; all funnel counts, scales, choices and decisions remain
exact. The complete funnel difference is included in the audit.
