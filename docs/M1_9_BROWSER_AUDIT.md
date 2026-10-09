# X6 M1.9 — Browser qualification pipeline audit

Status: **HOLD**. Source: `x6-source-preview/app/index.html`.

## Observed directly from GitHub source

- 11/11 required qualification element IDs were present exactly once.
- Two embedded iframe elements and two `srcdoc` attributes.
- `x6-cert-bridge-1` and `CERTIFY` request code are present.
- The `run39` handler sets fixed model samples and requests a certificate
  from the spectral iframe; the bridge uses a 15-second timeout.
- No external `<script src=...>` tags were found by the source inspection.

These observations are **static** and do not prove browser functionality.

## Changes

- Added `tests/python/static_ui_preflight.py` to reproduce the static
  structure checks from a real repository checkout.
- Updated `tests/browser/browser_http_test.py` to wait for the spectral
  iframe document to reach `readyState === "complete"` before clicking
  the qualification button. This mitigates an obvious initialization race;
  it does not prove the iframe's application-level bridge is ready.
- Preserved the historical `tests/browser/browser_test.py` and original
  `SHA256_REPOSITORY.json` unchanged.
- New test files are not covered by the original archive hash manifest.

## Test status

| Check | Status |
| --- | --- |
| Direct source inspection of 11 UI IDs | PASS (11/11) |
| Bridge/schema static presence | PASS (source inspection) |
| Static preflight script in a checkout | NOT_EXECUTED |
| Chromium HTTP end-to-end | NOT_EXECUTED |
| Julia | NOT_EXECUTED |
| Historical SHA-256 manifest against full checkout | NOT_EXECUTED |
| Browser security, translations and accessibility | NOT_EXECUTED |

## Reproduction

```bash
python tests/python/static_ui_preflight.py
python tests/python/verify_manifest.py
python -m pip install -r requirements-test.txt
python -m playwright install chromium
python tests/browser/browser_http_test.py
```

Collect Chromium and Playwright versions, stdout/stderr and the JSON
qualification output. Keep PR #2 draft until the actual runtime tests and
other release gates pass. Do not confuse the browser's `allPassed` local
gate with independent scientific certification.

## M1.10 — Sandbox iframe compatibility correction

**Static bug found:** `#spectrumFrame` uses `sandbox="allow-scripts allow-downloads allow-modals"`
without `allow-same-origin`. Therefore parent-page JavaScript cannot inspect
`frame.contentDocument.readyState`; the earlier HTTP test readiness wait would
time out even if the iframe loaded successfully.

**Correction committed:** `tests/browser/browser_http_test.py` now waits
through Playwright's `frame_locator("#spectrumFrame").locator("body")` rather
than attempting forbidden parent-page DOM access. This preserves the iframe
sandbox boundary. The app itself and historical test fixture were not changed.

**Execution limitations:** Browser/Chromium runtime was available in the
isolated environment, but the complete application could not be downloaded
there: DNS lookup of raw.githubusercontent.com failed. GitHub connector source
inspection was available; full browser E2E remains **NOT_EXECUTED**.
Julia and full manifest checkout verification also remain **NOT_EXECUTED**.

**Release decision: HOLD.** No GitHub Actions workflow was run and PR #2
remains draft.
