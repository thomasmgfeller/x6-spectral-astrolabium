# X6 M1.6 — Execution record (2026-10-09)

## Scope and provenance

Source: `tests/python/independent_audit.py` from `x6-source-preview`,
copied as text into a separate local Python environment. This was NOT a
complete Git checkout or GitHub Actions run.

## Executed

- Python standard-library exact rational spectral-gap audit: **PASS 5/5**.
- Cases: path4, triangle, weighted2, rounded_signal_path, disconnected.
- Output: `passed: 5, total: 5` and generated local JSON results.
- The original source file on the branch was not modified by this test.

## Not executed

- `tests/python/verify_manifest.py`: NOT_EXECUTED against full repository checkout.
- Julia numerical reference: NOT_EXECUTED (Julia runtime unavailable).
- Playwright browser smoke test: NOT_EXECUTED (full HTML app not staged locally).
- Wolfram, accessibility, multilingual, cross-browser and full X6 integration:
  NOT_EXECUTED.
- GitHub CI: NOT_EXECUTED (workflow installation requires separate authorization).

## Findings and next actions

1. `tests/browser/browser_test.py` starts an HTTP server but uses
   `page.set_content(...)` rather than navigating to the served URL.
   An HTTP-origin smoke test should use `page.goto(...)` in a separate
   reviewed change and update the manifest hash accordingly.
2. Preserve the original archive SHA-256 manifest as a historical provenance
   record. Any changed tracked source file needs a new versioned manifest
   or an explicitly documented delta; do not silently claim historical
   hashes still match.
3. The source PR remains draft and must not be merged until all release
   gates are evaluated. PASS means only the named fixtures passed.

## Acceptance

Current decision: **HOLD** for stable release. Python reference gate is
partially evidenced; Julia, browser, repository hash integrity and
licensing gates remain open.
