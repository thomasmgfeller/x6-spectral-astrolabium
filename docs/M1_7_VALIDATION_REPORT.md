# X6 M1.7 — Validation and provenance checkpoint

Status: **HOLD / NOT RELEASE-READY**. Branch: `x6-source-preview`.
No merge, release or GitHub Actions workflow execution was requested or performed.

## Completed in this milestone

- Checked PR #2: draft, unmerged; preview source branch is active.
- Added `tests/browser/browser_http_test.py`, a new HTTP-origin Chromium
  smoke test. It serves `app/index.html` via an ephemeral loopback port,
  uses `page.goto`, checks HTTP 200, three tabs, the qualification output,
  browser page errors, and closes the browser/server in `finally` blocks.
- Preserved the original `tests/browser/browser_test.py` bytes for historical
  archive provenance.
- Extended the manifest verifier's *declared new-file allowlist*. The original
  SHA-256 manifest is unchanged; it is **not** a hash certificate for newly
  added files.

## Execution evidence

| Gate | Result | Meaning |
| --- | --- | --- |
| Python rational reference (previous M1.6) | PASS 5/5 | Only the named fixtures |
| GitHub PR / source inventory | PASS | Metadata and file paths reviewed |
| New HTTP-origin browser smoke test | NOT_EXECUTED | Requires local checkout and Playwright/Chromium |
| Original browser smoke test | NOT_EXECUTED | Requires local checkout and Playwright/Chromium |
| Julia reference | NOT_EXECUTED | Julia runtime not available in this milestone |
| Manifest verifier end-to-end | NOT_EXECUTED | Full checkout not available |
| Wolfram export/certificate | NOT_EXECUTED | No external kernel execution |
| GitHub Actions CI | NOT_EXECUTED | Workflow-write permission not granted |
| Full X6 functional/security/accessibility | NOT_EXECUTED | Out of scope for this checkpoint |

## Reproduction commands

```bash
git clone https://github.com/thomasmgfeller/x6-spectral-astrolabium.git
cd x6-spectral-astrolabium
git switch x6-source-preview
python tests/python/verify_manifest.py
python tests/python/independent_audit.py
julia tests/julia/reference.jl
python -m pip install -r requirements-test.txt
python -m playwright install chromium
python tests/browser/browser_http_test.py
```

Record runtime versions and exact output. A `PASS_WITH_EXCLUSIONS` manifest
result means only original included files matched the historical archive hashes.
New scripts/docs are not covered by that historical manifest.

## Next acceptance gates

1. Run both Python scripts in a real Git checkout; inspect the generated report.
2. Run Julia numerical fixtures and HTTP-origin Chromium smoke test.
3. Review JS, browser security, dependencies and licensing.
4. Separately authorize and review the CI workflow; do not bypass GitHub's
   workflow-write permission requirement.
5. Keep PR #2 draft until the evidence and license decisions are reviewed.

## M1.8 follow-up — independently executed analytic stress cases

Execution environment: isolated Python container (not a GitHub checkout).
A faithful copy of the checked-in rational Laplacian / positive-definiteness
functions was tested against analytic complete-graph spectra.

- Original five reference fixtures: **5/5 PASS**.
- Complete graphs with n=2..8, 20 deterministic rational weights per n:
  **140/140 PASS** (seed 20261009).
- For each graph with known spectral gap n*w, tested three bounds:
  n*w-1/100000 accepted, n*w rejected, n*w+1/100000 rejected.
- This is 420 boundary assertions across 140 analytic cases.
- These checks are numerical-program execution with exact Fraction arithmetic,
  not a formal proof of the implementation for arbitrary inputs.
- Full repository clone was attempted but blocked by DNS resolution for
  github.com in the execution container.
- Julia: NOT_EXECUTED (runtime absent).
- Browser smoke: NOT_EXECUTED (full app unavailable in the local checkout).
- SHA-256 full checkout: NOT_EXECUTED.

**Release decision remains HOLD.** No workflow or release triggered.
