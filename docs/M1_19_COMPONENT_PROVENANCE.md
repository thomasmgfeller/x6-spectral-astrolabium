# X6 M1.19 — Component-level provenance register

**Status:** DRAFT provenance register, not a legal ownership determination.
**Selected intended license:** Apache-2.0 (NOT YET GRANTED).
**Source:** `x6-source-preview` as inspected 2026-10-09.
**Maintainer statement:** developed with ChatGPT, Copilot and Google AI;
third-party snippet provenance not fully known.

| ID | Component / files | Directly observed purpose | Provenance classification | Next evidence |
| --- | --- | --- | --- | --- |
| APP-01 | `app/index.html` / `pane-signal` | Embedded signal laboratory iframe | AI-assisted owner development reported; third-party reuse unverified | Compare original prompts/drafts and embedded source attribution |
| APP-02 | `app/index.html` / `pane-spectrum` | Embedded spectral laboratory iframe | Same; separate embedded program | Review algorithm sources, code excerpts and notices |
| APP-03 | `pane-guide` | User help and DE/EN/FR content | Origin unverified | Check text translations and borrowed help content |
| APP-04 | `pane-data` | Unified data bridge | Origin unverified | Inspect imports/exports, example data provenance |
| APP-05 | `pane-model` | Explicit signal-to-graph mapping | Model choice documented, implementation origin unverified | Compare mathematical formulas and code lineage |
| APP-06 | `pane-audit`, `release37`, `release38`, `qualification39` | Browser qualification and audit gates | Origin unverified | Trace fixed fixtures and certificate algorithms |
| APP-07 | `release40`, `accept41`, `release42` | Research-preview/acceptance UI | Origin unverified | Check claims, labels and citation metadata |
| TEST-01 | `tests/python/*.py` | Exact rational audit, manifest, runner and tests | AI-assisted project development reported; individual source origins unverified | Compare to prior code and third-party examples |
| TEST-02 | `tests/julia/reference.jl` | Numerical eigenvalue reference | Origin unverified | Review standard library and borrowed snippets |
| TEST-03 | `tests/browser/*.py` | Playwright smoke and HTTP-origin tests | Origin unverified; external Playwright dependency | Record package version/license and source notices |
| DATA-01 | `data/reference_certificate.json` | Fixed graph/certificate fixture | Data origin unverified | Trace generation, inputs, attribution |
| EVID-01 | `evidence/*.json` | Historical execution/manifest evidence | Historical records; independent provenance not established | Match hashes to archived source and execution logs |
| DOC-01 | `README.md`, `docs/*.md`, `CITATION.cff` | Scientific and release documentation | Attribution incomplete | Verify author names, sources, quotations and references |
| INFRA-01 | `.github/**` | CI, issue and PR templates | External GitHub Actions referenced | Verify action license and pinning policy |
| DEP-01 | `requirements-test.txt` | Playwright >=1.50,<2 | Third-party dependency | Verify actual resolved version, license and notices |

## Findings from static source inspection

- `app/index.html` contains 12 named sections (including two embedded
  laboratory iframes), not merely a single isolated script.
- No direct external script/style URL imports detected in the top-level HTML.
- Three inline copyright declarations identify Thomas Gfeller; their
  legal scope and compatibility with intended Apache-2.0 must be reviewed.
- Static patterns do not establish originality or absence of infringement.

## Decision matrix

- **CLEAR:** direct evidence of ownership or suitable upstream license
  documented for the specific component.
- **REVIEW:** plausible origin but not independently verified.
- **EXCLUDE:** known incompatible/uncleared material should be removed,
  replaced or separately licensed before the proposed grant.

At present every APP/TEST/DATA/EVID/DOC component remains **REVIEW**;
external dependencies remain **REVIEW** until their notices are checked.
No component is classified as infringement based on missing provenance.

## Required next actions

1. Trace module history and any third-party snippets in AI-generated outputs.
2. Inventory upstream package/action licenses and distribution obligations.
3. Decide whether data and documentation use Apache-2.0 or separate terms.
4. Confirm human authorship/attribution for CITATION.cff and any NOTICE.
5. Only after clearance, add the authoritative LICENSE and update release
   metadata. Do not rewrite historical SHA-256 evidence.

**PR #2 remains draft; no merge or release.**
