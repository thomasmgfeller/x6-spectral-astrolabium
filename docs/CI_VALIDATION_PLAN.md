# X6 M1.5 — CI validation plan (NOT EXECUTED)

Status: proposed test matrix. This document is not an installed GitHub Actions workflow.
Installing `.github/workflows/validation.yml` requires separate authorized review:
the previous GitHub App push was rejected for missing workflow permission.

## Reproducible checks

Run from repository root:

1. `python tests/python/verify_manifest.py`
   - PASS_WITH_EXCLUSIONS only if all included manifest hashes match.
   - Explicit exclusions: `.github/workflows/validation.yml` (not installed),
     `tests/python/python_results.local.json` (generated output).
   - The script itself and this plan are new and not part of the original manifest.
2. `python tests/python/independent_audit.py`
   - Five exact rational reference cases; generates a local JSON report.
3. `julia --version && julia tests/julia/reference.jl`
   - Four numerical eigenvalue fixtures, not a formal proof.
4. `python -m pip install -r requirements-test.txt`
   then `python -m playwright install chromium` and
   `python tests/browser/browser_test.py`
   - Chromium qualification smoke test only, not full UI coverage.

## Proposed GitHub Actions matrix (requires separate workflow authorization)

- ubuntu-24.04, Python 3.12: manifest check and rational audit
- ubuntu-24.04, Julia 1.10: numerical reference tests
- ubuntu-24.04, Python 3.12 + Playwright Chromium: browser smoke test
- Upload text/JSON logs as artifacts even on failure; record runtime versions.
- Do not mark missing jobs PASS. Keep statuses PASS / FAIL / NOT_EXECUTED.
- Gate release and merge on review of results; no automatic release.

## Current evidence

- Prior assistant independent reproduction: 5/5 rational fixtures PASS.
- This manifest script: NOT_EXECUTED against a full checked-out repository.
- Checked-in Python script end-to-end: NOT_EXECUTED here.
- Julia: NOT_EXECUTED here.
- Playwright: NOT_EXECUTED here.
- Workflow installation: NOT_ATTEMPTED; earlier GitHub workflow-write denial remains relevant.
- Browser, multilingual, accessibility, security and Wolfram integration: NOT_EXECUTED.

## Scientific boundary

Certificates apply to the explicitly rounded finite rational graph, not
unrounded input signals or physical claims. A green CI result would validate
only the specified fixtures and smoke test, not the entire X6 system.
