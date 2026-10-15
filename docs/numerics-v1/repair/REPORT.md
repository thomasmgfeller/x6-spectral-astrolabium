# X6 scaling repair qualification — 2026-10-15

The known small-weight defect is repaired in `jacobi-scale-1`.
Source commit: `7715b7d07ec333c838ca6a4f1da503253b75ea8b`.
App SHA-256: `56df754a1c5c3d26022e54b000f0d9e52ab4067d39e6a664556de12bfd7dc071`.
Subsequent integration-pin/documentation commits retain these exact app bytes.

| Executed check | Result | Evidence |
| --- | --- | --- |
| Original frozen check-3 criteria | 27/27 PASS | [Results](evidence/frozen-results.json), [raw outputs with internal vectors](evidence/x6-output.json) |
| Original evaluator controls | 11/11 negative, 2/2 positive PASS | Same results; evaluator and numerical criteria unchanged |
| Targeted regressions, including archived old failure | 23/23 PASS | [Regression log](evidence/regression.json) |
| Exact SageMathCell 10.9, unit and 2^-50 pair | 2/2 PASS | [Executed log](evidence/sage-run.log), [self-contained script](evidence/X6_Sage_Reparatur.sage) |
| Actual Chromium input/display/export/errors | 37/37 PASS; no page errors | [Browser report](evidence/browser-results.json), [run/source provenance](evidence/browser-provenance.json) |
| Other application frames and research kernels | Byte-identical | [Preservation check](evidence/preservation.json) |

Sage recomputes the matrix, eigenvalues and eigenvector residuals in exact rational
arithmetic from the transported binary64 outputs. Both pair cases have relative
eigenvalue error `1/4503599627370496`; the historical relative error was `1/2`.
This is an executed Sage check, distinct from the executed Chromium UI tests.

The browser evidence comes from GitHub's temporary PR merge checkout, not a
standalone checkout of the PR head. Both commits and the identical application
hash are recorded explicitly. Three downloaded JSON files are preserved beside
the browser report and were checked against their displayed reports.

The initial Signal Lab workflow rejected the stale active application pin. The
follow-up integration amendment updates only the app/configuration digests after
proving the unrelated research functions unchanged. Its original protected map
and rejection tests are retained. The PR must pass all triggered workflows before
merge; this report does not treat an earlier failed run as a success.

These are finite software checks, not a proof for every graph, a positive-gap
interval certificate, or evidence of physical functionality. Extreme weight
contrasts can remain unresolved at the reported numerical tolerance.

Historical failure evidence: [check 3](../historical/check3-PRUEFBERICHT.txt).
Repair design and commands: [DESIGN.md](DESIGN.md).
