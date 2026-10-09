# X6 M1.20 — External dependency license audit

Date: 2026-10-09. Status: **DIRECT LICENSE REVIEW COMPLETED; FINAL CLEARANCE PENDING**.
Intended X6 license: Apache-2.0. No LICENSE added; PR #2 remains draft.

## Verified upstream licenses

| Dependency | X6 usage | Upstream license | Source | Assessment |
| --- | --- | --- | --- | --- |
| Microsoft Playwright Python | `playwright>=1.50,<2` in `requirements-test.txt` | Apache-2.0 | https://github.com/microsoft/playwright-python/blob/main/pyproject.toml | Compatible in principle; version and transitive licenses unresolved |
| Julia language | `tests/julia/reference.jl` runtime | MIT; bundled components separately licensed | https://github.com/JuliaLang/julia/blob/master/LICENSE.md and https://github.com/JuliaLang/julia/blob/master/THIRDPARTY.md | Compatible for running CI; redistribution of binaries requires own notice review |
| actions/checkout | `@v5` | MIT | https://github.com/actions/checkout | Compatible in principle |
| actions/setup-python | `@v6` | MIT | https://github.com/actions/setup-python | Compatible in principle |
| julia-actions/setup-julia | `@v2` | MIT | https://github.com/julia-actions/setup-julia | Compatible in principle |
| actions/upload-artifact | `@v4` | MIT | https://github.com/actions/upload-artifact | Compatible in principle |

Playwright's upstream NOTICE identifies derived Puppeteer code:
https://github.com/microsoft/playwright/blob/main/NOTICE

## Distribution boundary

These tools are used as development or CI dependencies, not automatically
incorporated into the X6 source-code license grant. Apache-2.0 for original
X6 code would not relicense Playwright, Julia, GitHub Actions, or their
bundled components. Preserve upstream notices when distributing copies of
those components, and review any bundled browser binaries separately.

## Open findings

1. `playwright>=1.50,<2` is a version range, not a reproducible lockfile.
   Record resolved version and transitive `pyee` / `greenlet` metadata
   for the exact CI installation.
2. Julia binaries contain third-party components; consult Julia's
   `THIRDPARTY.md` if redistributing Julia itself.
3. Workflow actions use major-version tags rather than immutable commit SHAs.
   Pin vetted commits for hardened release pipelines; Node.js 20 warnings
   were observed for setup-julia@v2 and upload-artifact@v4.
4. Human/AI-assisted source originality, embedded code provenance,
   datasets and documentation remain unverified.
5. Decide scope for code, documentation and data and whether a NOTICE file
   is required; do not copy third-party notices blindly.

## Conclusion

**No obvious conflict was found among the six directly identified upstream
licenses.** This does NOT establish legal clearance of all X6 contents,
transitive dependencies, or AI-generated material. Apache-2.0 remains the
owner's intended license, not an active license grant. Stable release HOLD.

No merge or workflow dispatch requested by this audit.
