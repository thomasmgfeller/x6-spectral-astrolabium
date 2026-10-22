# CI comparison portability repair

SPDX-License-Identifier: Apache-2.0

The new exact stability certificate passed GitHub job 119817071644 in run
39776616442. The same PR's inherited eligibility-before-cap check failed in
job 119817071714 at its byte-equality assertion for a freshly recomputed
analysis JSON. Controls and scientific decisions agreed. The remote legacy
RMSE was 1.7308231132065 versus archived 1.7308231132065004; the predicted
variance was 6.8339305041481175 versus 6.83393050414815. These last-bit
differences arise in floating reductions across numerical environments.

The CI wrapper now compares JSON structure, types, strings, booleans, integer
counts and decision gates exactly. Only finite float values use a 1e-12
absolute/relative tolerance. Negative controls reject changed decisions,
counts, numeric types, schema, list lengths, nonfinite floats and a 1e-8
metric perturbation. The archived package hashes are still checked exactly.

No scientific input, archived result, threshold, frozen experiment code or
analysis algorithm is changed. Only the post-freeze CI comparison wrapper and
its current checksums are updated. The new stability search and certificate
do not depend on this wrapper and their frozen inputs remain unchanged.

Failure source: https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/39776616442/job/119817071714
