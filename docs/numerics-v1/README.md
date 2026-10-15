# X6 numerical qualification and scaling finding

**2026-10-15: historical 25/27 FAIL preserved; repaired solver passes the frozen 27/27 suite.**

See the [repair report](repair/REPORT.md) for exact Sage and actual-browser evidence.
The [separate check-4 report](extended/README.md) covers the 120-vertex boundary,
weight contrasts, relabeling and input-order invariance.

This audit concerns the finite positive-weight undirected graph Laplacian in
`app/index.html`, `spectrumFrame`, at commit
`7257e51a8df93ff1722d1116103143cc6c827ef4`. It does not qualify the signal mapping,
Lorentz operators, physical devices, or all graphs accepted by the application.

| Evidence | Result | Provenance |
| --- | --- | --- |
| Check 2: exact matrices/polynomials and numerical eigenvalues | 4/4 cases; 6/6 negative controls PASS | User-supplied SageMath 10.9 log |
| Check 3: eigenvectors, eigenspaces and scaling | **25/27 cases; overall FAIL** | Local Node.js/Python execution; independent matrix reconstruction and LAPACK reference |
| Check 3 checker controls | 11/11 negative and 2/2 positive controls PASS | Local execution |
| Minimal scaling counterexample | **Exactly confirmed** | Observed SageMathCell 10.9 run on two embedded X6 outputs |

## X6-NUM-SCALE-001: false convergence at small weight scales

Input (two vertices and one edge):

```text
v0 v1 0.00000000000000088817841970012523233890533447265625
```

With `w = 2^(-50)`, the exact matrix is `[[w,-w],[-w,w]]`, whose eigenvalues
are `0` and `2w`. The historical X6 revision returns `w,w`, `converged=true` and zero rotations.
The eigenvalue error and eigenvector residual, each scaled by the matrix infinity
norm, are both `1/2`. The topologically computed nullity remains correctly one.

The historical stopping condition uses `max(1, max(abs(diagonal)))`. The fixed floor causes
the solver to terminate before a rotation at this scale. The weight is exactly
representable in binary64; this example does not involve underflow.
A similarly scaled path with 16 vertices also fails.

The earlier four-case PASS remains valid within its stated scope. Its absolute
error floor cannot establish relative accuracy for arbitrarily small matrices.

## Immutable historical evidence

- [Check 2 original reproducible package](historical/check2-original.zip)
- [Check 2 user-supplied Sage output](historical/check2-user-sage-run.txt)
- [Check 3 original complete package](historical/check3-original.zip)
- [Detailed report in German](historical/check3-PRUEFBERICHT.txt)
- [Frozen 27-case contract](historical/check3-contract.json)
- [Local results and controls](historical/check3-local_results.json)
- [Exact Sage confirmation](historical/check3-sage_run.log)
- [Self-contained Sage code](historical/check3-X6_SageMathCell_Pruefung_3.sage)
- [Archive checksums and provenance](historical/ARCHIVE.json)

The original archives retain preparation-time wording, including the then-pending
Sage status in check 2. The separately preserved run logs record subsequent
execution. Historical files will not be rewritten to turn FAIL into PASS.

The original kernel does not export eigenvectors. Check 3 additionally ran a copy
with one observation-only return field, `vector:v`. All original fields matched
the unchanged kernel exactly after timestamps were removed. This is an internal
eigenvector check, not qualification of a public eigenvector-export interface.

## Completed work sequence

1. Historical results and the scaling finding were preserved before repair (PR #26).
2. Scale handling was corrected and targeted regressions added on a separate branch (PR #28).
3. Frozen criteria pass: 27/27 cases, 11/11 negative controls, 2/2 positive
   controls, plus 23 regressions and two exact Sage confirmations.
4. Actual browser input, solver, display, JSON export and error handling pass 37/37 checks.
5. The independent check-4 corpus extends to 120 vertices, weight contrasts,
   relabeling/input-order invariance and explicit unresolved-gap diagnostics (PR #29).

Repeated/clustered eigenvalues are assessed through eigenspace projectors. A
passing cluster check does not resolve every individual eigenvector or a gap
smaller than the numerical acceptance threshold. No general solver proof is claimed.
