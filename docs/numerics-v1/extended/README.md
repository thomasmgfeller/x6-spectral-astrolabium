# Check 4: expanded numerical qualification

**PASS: 30/30 graph cases, 6/6 metamorphic checks, 8/8 gap diagnostics,
and 4/4 checker controls (three negative, one positive).**

Executed on GitHub Actions after the local 30/30 PASS. The GitHub numerical
workflow also repeats the frozen 27 cases and 13 controls, all 23 targeted
regressions, and all 37 actual-browser checks successfully.

- [Complete check-4 results](evidence/extended-results.json)
- [Full raw X6 matrices, spectra and observed vectors, gzip JSON](evidence/extended-output.json.gz)
- [Source, checkout and artifact provenance](evidence/provenance.json)
- [Repeated frozen results](evidence/replay-frozen-results.json), [regressions](evidence/replay-regression.json), [browser reports](evidence/replay-browser-results.json)

| Largest observed error across 30 cases | Value | Limit |
| --- | ---: | ---: |
| Matrix-scaled eigenvalue error | 2.042810e-14 | 1e-12 |
| Matrix-scaled residual | 5.517572e-14 | 1e-12 |
| Frobenius orthogonality error | 1.674757e-13 | 1e-12 |
| Relative reconstruction error | 1.511914e-13 | 1e-12 |
| Cluster-projector Frobenius error | 3.202840e-11 | 1e-7 |

Ten cases use exactly 120 vertices. Exporting the full corpus through both kernel
variants took 521.86 seconds in CI (543.71 seconds locally). This is corpus runtime,
not single-graph UI latency; browser responsiveness at 120 vertices was not measured.

The corpus and runner were published at commit
`acd50895d24e17295603b27de32b64a028a2ca85` before the GitHub qualification run.
They contain 30 deterministic cases with 16–120 vertices, two fixed random seeds,
exact dyadic weights, path scales 2^-500 and 2^500, repeated eigenvalues,
multiple components, and bridges as small as 2^-50.

Six cases test relabeling, declaration order, edge order/direction, and splitting
an edge into two parallel half-weight edges. Comparisons use eigenspace projectors
rather than signed individual eigenvectors. Eight explicit gap-status checks
cover resolved, unresolved and absent positive modes.

The unchanged historical check-3 evaluator checks exact matrices and nullity,
eigenvalue error, independently recomputed residuals, orthogonality,
reconstruction, and cluster projectors. Matrix-scaled tolerances remain 1e-12;
projector tolerance remains 1e-7. The new metamorphic checks use the same limits.
Three negative controls and one sign-flip positive control test the added checks.

## Reproduce

```sh
python3 tests/numerics/verify_extended.py --output extended-evidence
```

The command runs the actual extracted application twice (original public result
and observation-only vectors), verifies exact parity, and archives raw outputs
as deterministic gzip. The contract, application, evaluator and output hashes
are recorded with the source commit. CI additionally reruns the original frozen
suite, targeted regressions and real Chromium UI tests.

## Interpretation

A passing tiny-bridge case can still have `UNRESOLVED_AT_TOLERANCE`: its exact
combinatorial nullity is known, but the smallest positive numerical mode is too
small to resolve at the acceptance threshold. This is not an interval certificate.
The 120-node checks exercise the current boundary; they do not prove correctness
for all inputs. Timing covers this environment and corpus only. Signal mapping,
physical functionality, deployment hardware and sensor measurements are outside
this qualification.

Historical FAIL evidence remains in [the original archive](../historical/).
The separately merged repair passed [all seven triggered integration workflows](repair-integration.json).
