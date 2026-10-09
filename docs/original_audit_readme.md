# X6 v4.3 — Independent community acceptance kit

**Status: release candidate; no full scientific release approval.** The bundled HTML is the actual v4.2 application, not a newly certified v4.3 binary. v4.3 is the community validation milestone.

## Reproducible tasks

1. Run `python independent_audit.py` (Python standard library only). Inspect `python_results.json` and verify all five cases; introduce deliberately false bounds and verify rejection.
2. Run `julia julia_reference.jl` with Julia 1.9+. This checks independent floating-point eigenvalues, **not** formal rational certificates. Report Julia version and BLAS vendor.
3. Run `python browser_test.py` after installing Playwright and Chromium. Record OS, browser version, output and any errors. The script checks the qualification gate in the real browser, not all UI controls.
4. Independently inspect `reference_certificate.json`. Do not trust a certificate just because its JSON says PASS. Rebuild the Laplacian from the edge list and verify the exact rational inequalities.
5. Review translations and accessibility manually in DE, EN, FR, including keyboard navigation, error messaging, exports and user help.

## Acceptance gates

- Python 5/5 reference cases PASS, including invalid bounds and disconnected graph.
- Julia 4/4 reference cases PASS with tolerances documented.
- Chromium qualification all checks PASS and zero uncaught page errors.
- Exported certificate independently verified with exact rational arithmetic.
- Security and data integrity review: no invented external execution claims.

If any gate fails, mark `FAIL`, include minimal reproduction, expected and actual outputs, environment and relevant code revision. `NOT_EXECUTED` is never equivalent to `PASS`.

## Scope limits

The exact rational certification is valid only for the explicitly rounded graph Laplacian. A signal-to-graph mapping is a model choice, not a causal or quantum-gravity theorem. This kit does not independently validate the physical signal model or Temperley–Lieb algorithms. External volunteers or AI systems must actually run the tests; creating this package does not assign them tasks or obtain their results.
