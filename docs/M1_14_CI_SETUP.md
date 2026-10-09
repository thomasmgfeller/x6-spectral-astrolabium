# X6 M1.14 — GitHub Actions validation installation (requires owner authorization)

**State:** CI workflow proposed; NOT INSTALLED, NOT EXECUTED.
**PR #2:** remains draft and must not be merged solely to enable CI.

## Why manual authorization is required

An earlier GitHub Actions run was rejected when the GitHub App attempted to
create `.github/workflows/validation.yml` without workflow-write permission.
This must not be bypassed. The repository owner should install the workflow
through an authorized GitHub web editor or a credential with explicit
workflow permissions, after reviewing its contents.

## Proposed workflow

Save the following file as `.github/workflows/x6-validation.yml` on a
separate owner-authorized test branch (not directly on `main`):

```yaml
name: X6 Validation
on:
  workflow_dispatch:
  pull_request:
    paths:
      - 'app/**'
      - 'tests/**'
      - 'data/**'
      - 'SHA256_REPOSITORY.json'
      - '.github/workflows/x6-validation.yml'
permissions:
  contents: read
jobs:
  python:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v6
        with:
          python-version: '3.12'
      - name: Integrity and rational checks
        run: |
          python tests/python/verify_manifest.py
          python tests/python/static_ui_preflight.py
          python tests/python/independent_audit.py
          python -m unittest discover -s tests/python -p 'test_validation_runner.py' -v
  julia:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v5
      - uses: julia-actions/setup-julia@v2
        with:
          version: '1.10'
      - name: Numerical eigenvalue reference
        run: julia tests/julia/reference.jl
  browser:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v6
        with:
          python-version: '3.12'
      - name: Install Playwright
        run: |
          python -m pip install -r requirements-test.txt
          python -m playwright install --with-deps chromium
      - name: X6 HTTP qualification smoke
        env:
          X6_EVIDENCE_DIR: x6-evidence
        run: python tests/browser/browser_http_test.py
      - name: Preserve browser evidence
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: x6-browser-evidence
          path: x6-evidence/
          if-no-files-found: warn
```

## Required verification

1. Review the workflow for action pinning, package supply-chain policy,
   token permissions and the branch on which it will execute.
2. Install through a separately authorized account; do not attempt to
   bypass workflow-write denial through the existing connector.
3. Run it on a test branch containing the X6 sources. Merely installing
   on `main` without the source files would cause failures.
4. Attach GitHub run URL, versions and artifact hashes to PR #2.
5. Treat Julia numerical PASS as a numerical cross-check, not an exact proof.
6. Release decision stays HOLD until licensing, security and scientific
   validation are reviewed.

**No workflow has been created or run by this milestone.**
