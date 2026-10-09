# X6 M1.16 — Release readiness decision record

**Decision: HOLD for stable release.** Do not merge PR #2 or create a stable
tag merely because the narrow CI suite passes.

## Verified technical evidence

- Previous CI run 37992186426: Python, Julia and Chromium jobs SUCCESS.
- Current run 37992793675 at initial inspection: Julia and Python SUCCESS;
  Chromium IN_PROGRESS. A pending job is not a PASS.
- The CI Python job includes archive SHA-256 verification, static UI structure,
  rational fixtures and runner unit tests.
- Julia checks four floating-point reference eigenvalues.
- Chromium checks the browser's local qualification pipeline. It does not
  independently certify every generated mathematical result.
- Earlier independent exact rational fixtures: 5/5 PASS.
- Historical SHA-256 checks have explicitly excluded files; post-archive
  files require a separate release manifest.

## Unresolved mandatory decisions

1. **License / IP:** `docs/LICENSE_OPTIONS.md` explicitly grants no license.
   Verify authorship and third-party dependencies; choose a license and
   approve authoritative LICENSE text before a redistributable stable release.
2. **Citation metadata:** `CITATION.cff` has no verified authors/ORCID/DOI.
3. **Security:** browser message origins, sandbox assumptions, user-supplied
   data handling and any Julia/Wolfram backend require independent review.
4. **Testing:** full functional coverage, Firefox/WebKit, accessibility,
   translation completeness, extreme numeric inputs and fuzzing are not
   established by the current smoke tests.
5. **Scientific scope:** exact certificates cover finite rounded rational
   graph Laplacians, not unrounded signal inputs or physical quantum gravity.

## Gate policy

- `PASS`: check actually executed and succeeded.
- `FAIL`: check actually executed and failed.
- `NOT_EXECUTED`: no runtime evidence.
- `PENDING`: execution in progress or owner decision outstanding.
- Overall release status stays `HOLD` until license, security and
  scientific scope have been reviewed and the release checklist approved.

## Follow-up

Inspect the final conclusion and job logs for run 37992793675.
If all jobs succeed, prepare a **research-preview** merge review separately
from any claim of stable scientific certification. PR #2 remains draft.
