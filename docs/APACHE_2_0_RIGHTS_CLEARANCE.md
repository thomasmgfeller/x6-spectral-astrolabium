# X6 — Apache-2.0 rights clearance (DRAFT; no license granted yet)

**Owner preference:** Apache License, Version 2.0.
**Decision:** HOLD until ownership and third-party rights are confirmed.
**Scope:** repository branch `x6-source-preview` reviewed on 2026-10-09.
This document is an audit checklist, not legal advice or a LICENSE file.

## Repository inventory and evidence

| Component | Observation | Rights status |
| --- | --- | --- |
| `app/index.html` | Single HTML app (~137 KB), two inline iframe srcdoc applications, no external script-src or stylesheet href references found in source scan | AUTHORSHIP UNVERIFIED |
| `tests/python/*.py` | Python rational audit, manifest checks, runner and tests | AUTHORSHIP UNVERIFIED |
| `tests/browser/*.py` | Playwright smoke tests; package dependency in requirements-test.txt | AUTHORSHIP UNVERIFIED; dependency licenses must be reviewed |
| `tests/julia/reference.jl` | Julia numerical reference | AUTHORSHIP UNVERIFIED; runtime/dependency notices to review |
| `data/reference_certificate.json` | Mathematical reference certificate | DATA PROVENANCE / RIGHTS UNVERIFIED |
| `evidence/*.json` | Historical validation records and hashes | DATA PROVENANCE / RIGHTS UNVERIFIED |
| `docs/*.md`, `README.md`, `CITATION.cff` | Project documentation and citation placeholders | AUTHORSHIP / ATTRIBUTION UNVERIFIED |
| `.github/**` | GitHub Actions workflow and issue templates | SOURCE / ACTION LICENSES NOT YET AUDITED |
| `requirements-test.txt` | `playwright>=1.50,<2` | Third-party package; review license and notices |

Static source scanning found no direct external `<script src>` or
`<link href>` references in the main HTML file, but this is **not** a
complete dependency, embedded-code or copyright audit. It cannot prove
that all inline code and documentation are original.

## Owner attestations required before Apache-2.0

1. Identify all human authors, employers, collaborators and external code
   contributors, and confirm rights to sublicense each relevant component.
2. Confirm whether any code, images, fonts, text, datasets or certificates
   were copied, adapted or generated from third-party sources; list original
   licenses, notices and any attribution obligations.
3. Confirm that no confidential, employer-owned or restricted research
   material is included in the public ZIP or extracted repository.
4. Review Python/Playwright, Julia and GitHub Actions dependencies, and
   whether third-party notices or a `NOTICE` file are needed.
5. Decide whether documentation and data will share Apache-2.0 or receive
   separate explicit licensing; document any exclusions.
6. Confirm author names for `CITATION.cff` and copyright attribution.

## Intended next changes, only after clearance

- Add the **unmodified authoritative** Apache License 2.0 text in `LICENSE`.
- Add copyright and SPDX identifiers only where accurate.
- Add `NOTICE` only if required or useful, with verified attribution.
- Update README license status, citation metadata, release checklist and
  any versioned hash manifest without rewriting historical evidence.
- Obtain a new CI PASS and review PR #2 before merge.

**No LICENSE file was added in this step.** Public repository visibility
does not itself grant an open-source license. PR #2 stays draft.
