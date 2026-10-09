# X6 M1.11 — Browser execution environment and evidence

Status: **HOLD / E2E NOT_EXECUTED**.

## Actual environment probes

- `/usr/bin/chromium`: PRESENT.
- Python Playwright: IMPORTABLE.
- Default Playwright `chromium.launch()`: FAIL — bundled Chromium headless
  shell executable missing from Playwright cache.
- Playwright with `executable_path='/usr/bin/chromium'` and
  `args=['--no-sandbox']`: PASS for an isolated HTML smoke check
  (`#ok` returned `test`). This is **not** an X6 test.
- HTTPS retrieval of X6 `app/index.html` from raw.githubusercontent.com:
  FAIL — DNS resolution failure in execution container.

## Code change

`tests/browser/browser_http_test.py` now uses system Chromium when present
and otherwise falls back to the installed Playwright browser.
When `X6_EVIDENCE_DIR` is set, successful qualification parsing writes
`browser_http_summary.json` and `qualification39.json` before checking
the qualification PASS condition. If navigation or parsing fails earlier,
these files are not guaranteed to exist; capture stdout/stderr separately.

Reproduce from a real checkout:

```bash
python -m pip install -r requirements-test.txt
python -m playwright install chromium
mkdir -p x6-evidence
X6_EVIDENCE_DIR=x6-evidence python tests/browser/browser_http_test.py
```

For strict sandboxing, prefer the bundled Playwright browser on an appropriate
CI runner. The local `--no-sandbox` fallback is only for isolated trusted
test environments, not general browsing of untrusted content.

## Remaining gates

- X6 Chromium end-to-end: **NOT_EXECUTED**
- Julia: **NOT_EXECUTED**
- Full Git checkout SHA-256 verification: **NOT_EXECUTED**
- Wolfram external verification: **NOT_EXECUTED**
- PR #2: remains DRAFT, no merge, no workflow dispatch.

No claim of scientific certification or release readiness is made.
