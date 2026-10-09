# X6 M1.12 — Unified validation runner

**Release status: HOLD.** PR #2 remains draft; no merge or Actions workflow was triggered.

## New executable entrypoint

```bash
python tests/python/run_validation.py
```

This sequentially runs the historical manifest verifier, static UI preflight,
exact rational Python fixtures, Julia reference fixtures and HTTP-origin
Playwright smoke test. It writes `x6-evidence/local_validation.json`.

Every check reports `PASS`, `FAIL`, or `NOT_EXECUTED`. Overall status
is `PASS` only when all five checks pass; otherwise the runner exits nonzero.
Missing Julia or Playwright is reported as `NOT_EXECUTED`, not a PASS.
A present but broken browser installation is a FAIL, not a skip.
The script does not create GitHub Actions workflows or release tags.

## Current independent evidence

- Prior isolated Python analytic checks: 5/5 reference and 140/140
  complete-graph boundary cases PASS (not a full repository CI run).
- Direct `curl` from the local execution container to
  `raw.githubusercontent.com`: FAIL (DNS resolution).
- Local Chromium binary and Python Playwright package: present.
- New combined runner against complete Git checkout: **NOT_EXECUTED**.
- Julia executable: **NOT_AVAILABLE** in local execution container.
- Actual X6 HTTP-origin Chromium qualification: **NOT_EXECUTED**.
- Full repository SHA-256 manifest check: **NOT_EXECUTED**.

## How to reproduce

On a machine with the source branch checked out:

```bash
git switch x6-source-preview
python -m pip install -r requirements-test.txt
python -m playwright install chromium
python tests/python/run_validation.py
```

Install Julia separately for the numerical reference. Attach
`x6-evidence/local_validation.json` and runtime versions to the PR.
The original archive manifest excludes generated outputs and the separately
authorized validation workflow; new files are outside the historical hash
scope and must be covered by a future versioned release manifest.

Do not merge PR #2 until the runtime checks, license, security review and
scientific scope are approved.
