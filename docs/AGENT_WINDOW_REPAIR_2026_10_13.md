# Agent operating-window repair — 13 October 2026

The maintainer requested repair of the agents and extension through the coming
Sunday. The common exclusive cutoff is **2026-10-18T22:00:00Z**, equivalent to
**19 October 2026 at 00:00:00 Europe/Zurich**: Sunday 18 October is included.
This is an operating change, not a new scientific result or release qualification.

## Diagnosis and scope

- The existing math configuration spanned about 110.23 hours, while its loader
  rejected anything above 72 hours. It therefore failed before research began.
- Math configuration and the three cron/date guards now cover 11–18 October.
  The loader still rejects nonpositive windows and windows over eight days.
  The 90-second search budget, 120-second configurable ceiling, case budget,
  seed, application digest and scientific algorithms are unchanged.
- Daily data/source jobs keep their 15/25-minute admission reserves. Math
  admission reserves six minutes for its five-minute job. The full-date guards
  reject expired manual runs and prevent an annual October restart. Scheduling
  can be delayed by GitHub; a cron entry is not evidence of execution.
- Workflow timeouts are operational limits, not a hard real-time guarantee.
  The math process also checks its UTC cutoff and monotonic compute budget.

## Source-inventory repair

The original 17-file research baseline and its canonical map digest
`91fb5b68fd04650be82e272d4ea607a8eda0f52165e3e65fb5555d20a5fd1c66` remain
in `SIGNAL_LAB_SOURCE_MANIFEST.json` as `protected_research_baseline`.
Exactly five new digests are explicitly pinned in `tools/build_signal_lab.py`:
three agent workflows, the math configuration and the math config reader.
The current map is `protected_research`; regeneration refuses unapproved drift.
The application, numerical algorithms, source adapters and dependency pins have
not changed. This inventory establishes content consistency, not authenticity.

The separately authorised Apache-2.0 activation had left old metadata hashes in
use. `SHA256_REPOSITORY.json` and `LICENSE_ACTIVATION_MANIFEST.json` are retained
unchanged. `LICENSE_SOURCE_MANIFEST.json` now checks current licensing metadata,
including the historical activation record itself. Only the three explicitly
superseded historical document hashes are delegated to that current inventory.
The README has advanced since activation; its old digest remains in that dated
record and its current bytes are checked separately.

The Sagnac inventory entry for `experiments/photonic-two-qubit/LICENSES.md` is
updated from `05ed5a5f76951ac146000fb576d76ba7c374ad82eefd4e1a8df095628599fa97`
to the exact activation-record digest
`aaa0e888de729dce3fd753aca4b2328c758808e89daacfb9bd8fd0a83525c8ea`.
No license text or scientific application code was modified by this repair.
The build tool still refuses any unrelated Sagnac/photonic source drift.

## Verification and follow-up

Regression tests execute the actual pre-checkout guards just before the start,
on Sunday, at the admission-reserve boundary, after the cutoff and in 2027.
Math tests exercise the eight-day ceiling and the disabled/expired states.
Provenance tests reject forged current or historical inventories and changed
licensing document bytes. Local test results and GitHub workflow artifacts are
reported separately; a successful schedule guard alone is not a successful
research run.

Local verification on 13 October: 33 agent/operating-limit tests and 16
provenance tests passed; an actual bounded math run produced a PASS report with
all five tracks. Signal Lab build, repository inventory, core, 25 evidence tests
and 198 NumPy/SciPy reference checks passed. Its local browser test could not
launch because the browser download was truncated; no local browser PASS is
claimed. GitHub qualification of the published commit is checked separately.

Daily review/monitoring and the separate shutdown automation were updated to the same
cutoff (review 19:00, error-only monitor 09:00 Europe/Zurich, through Sunday). Shutdown removes cron triggers while retaining manual triggers and
existing results; a later explicit extension must be checked before cleanup.
The full-date guards stop new work even if external cleanup is delayed.
