# X6 M1.18 — Source provenance and license audit

**Selected intended license:** Apache License 2.0.
**Current decision:** RIGHTS CLEARANCE INCOMPLETE. No LICENSE or blanket
Apache-2.0 grant added. PR #2 remains draft and unmerged.

## Method and scope

- Read the full `app/index.html` source through the connected GitHub
  repository (approximately 137 KB), the tracked file inventory, dependency
  manifest, and existing provenance/licensing documents.
- Static source scan for remote script/style references, network access,
  licensing notices, dynamic code execution, embedded base64 assets and
  apparent external imports. This is not an exhaustive copyright similarity
  search and cannot establish originality.
- The owner stated that X6 was developed with ChatGPT, Copilot and Google AI,
  but could not affirm that all outputs are free of third-party material.

## Findings

| Area | Observation | Assessment |
| --- | --- | --- |
| HTML script/style imports | No `<script src>` or `<link href>` references found | No direct external imports detected; does not establish authorship |
| Inline application | Two `srcdoc` iframes with embedded JavaScript | Large bundled code; attribution/origin not proven |
| Copyright strings | Three embedded strings: `© 2026 Thomas Gfeller. All rights reserved.` | Review consistency with intended Apache-2.0 grant; don't remove without approval |
| External network | Localhost endpoint `http://127.0.0.1:8765`, `fetch` in optional Julia adapter | Not an external vendor library; security/CORS review still needed |
| Dynamic execution | No literal `eval(` or `new Function(` found | Limited static signal only |
| Base64 embedded assets | No `data:image/font/application;...base64` found | Limited static signal only |
| Browser test dependency | `playwright>=1.50,<2` | Confirm third-party license/NOTICE obligations and resolved package version |
| Julia reference | Uses `LinearAlgebra` from Julia standard library | Confirm Julia runtime distribution and notices if redistributed |
| GitHub workflows | Use actions/checkout, setup-python, setup-julia, upload-artifact | Review upstream license and pinned revisions before release |
| Data/evidence | JSON fixtures and historical certificates | Confirm dataset origin, citation and reuse rights |
| Project documents | Maintainer attribution/citation still incomplete | Do not assert exclusive authorship or full rights clearance |

## Important interpretation

The static scan did **not** identify a clearly embedded third-party
JavaScript package, but cannot rule out copied snippets or generated
derivatives. The owner's inability to certify origin is a legitimate
unknown, not evidence of infringement. Apache-2.0 applies only to material
the licensor is authorized to license; its patent provisions should also
be reviewed before adoption.

## Remediation / release gate

1. Prepare a source-attribution register covering the major HTML sections,
   embedded iframe scripts, tests, docs, data and historical evidence.
2. Review AI-assisted development history and any pasted code where available.
3. Verify third-party licenses and notices for Playwright and GitHub Actions.
4. Decide which datasets and documents, if any, are excluded from Apache-2.0.
5. Confirm contributor/employer claims, attribution and `CITATION.cff`.
6. Only after clearance, commit the authoritative Apache-2.0 LICENSE and
   applicable NOTICE; review any `All rights reserved` notices in context.
7. Run CI again; keep stable release HOLD until scientific/security gates pass.

**No LICENSE file added. No merge performed.**
