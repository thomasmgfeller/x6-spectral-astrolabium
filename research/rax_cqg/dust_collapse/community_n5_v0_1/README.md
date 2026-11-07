# Donated compute: CST-DUST five-element field integrals

**Projektbudget: CHF 0.** Gesucht sind freiwillige Rechenzeit und unabhängige
Nachrechnung auf eigener Hardware oder bereits bewilligten Ressourcen.
Beitragende übernehmen Rechenzeit, Strom und Betrieb selbst; Thomas Gfeller
und dem Projekt dürfen keine Kosten, Rechnungen oder Erstattungspflichten
entstehen. Es werden keine Cloud-Dienste gebucht. Ohne freiwillige Übernahme
bleibt der Hauptlauf offen. Schon ein einzelner reservierter Block hilft.

**Status:** mathematical preparation and short controls complete;
five-element production quadratures **NOT RUN**. All physical gates **HOLD**.
This is a conditional numerical reference model, not a predicted dust-ball
bounce. See [MATHEMATICS.md](MATHEMATICS.md), [plan.json](plan.json) and
[controls_result.json](controls_result.json).

## What volunteers can contribute

- Review the derivation, especially the quadrature and arithmetic budgets.
- Run the short controls independently and return the output and environment.
- Supply a bounded pilot timing on their own CPU.
- Reserve and execute one or more production block IDs after those controls.
- Independently replay another contributor's blocks and maintain a public
  verification list (result hash, block ID, replay hash, environment).

All contributions must be voluntary and without cost to Thomas or the project.
Confirm this in the GitHub issue before reserving work. Use only compute you
are authorized to donate. No billing credentials are needed. There is no
automatic scheduler, network client or background execution in this package.
Source and original documentation are Apache-2.0; preserve notices and submit
only contributions you are entitled to share. Credit contributors in the
result record; no publication authorship is promised automatically.

## Download, check, and measure first

Use the pinned ZIP and SHA-256 in the community issue. Extract it into a new
directory. It is self-contained; no repository clone is needed. Requires
Python 3.10+ (standard library only), Linux and g++ with C++17 and `__int128`.
The local environment is recorded in environment.json; other compilers and
platforms require the same controls before production.

```bash
python3 worker.py list
python3 controls.py > my-controls.json
cmp my-controls.json controls_result.json
```

`list` checks the source manifest and prints job counts. `controls` rebuilds
the exact plan and performs small fixtures, not the production quadratures.
Setup and control runtime depend on the machine. For a pilot:

```bash
python3 worker.py pilot --config h1d4_mu1d4 --donated-compute --out pilot-small.json
```

This compiles locally and evaluates three samples of 64 grid points (start,
middle, end). The output includes measured kernel time and a rough linear
extrapolation. It excludes setup and I/O and is not a guaranteed runtime.
Every individual kernel invocation has a 120-second timeout. Compilation
has a 60-second timeout; Python rule preparation is separate and can be
interrupted. The `--donated-compute` switch acknowledges that all resource
costs are borne by the contributor; it cannot change a provider's billing.

Attach the JSON and CPU model, OS and compiler version to the public issue.
Report any mismatch or timeout before production. A successful pilot does
not establish the full accumulated error budget.

## Production reservation and exact IDs

The pair `(configuration, shard)` is the unique task ID. Do not change plan.json.

| Configuration | h | mu | Valid shard IDs | Priority |
|---|---|---|---|---|
| h1d4_mu1d4 | 1/4 | 1/4 | 0–3 | First small configuration |
| h1d4_mu1d1 | 1/4 | 1 | 0–73 | After independent controls/pilot |
| h1d2_mu1d4 | 1/2 | 1/4 | 0–73 | After independent controls/pilot |
| h1d2_mu1d1 | 1/2 | 1 | 0–6572 | Separate opt-in after its own pilot |

Reserve exact IDs in the issue before starting. Confirm a second contributor
can replay the selected blocks. First complete the small configuration;
then decide how much further donated capacity is available. For **one
reserved block**, e.g. small configuration ID 0:

```bash
python3 worker.py run --config h1d4_mu1d4 --shard 0 --donated-compute --out h1d4_mu1d4-0000.json
```

This command performs only that block, with at most 65,536 tensor points on
one kernel process. It never launches the next block. Return the unedited
JSON, optionally ZIP-compressed, or a failure with its ID and elapsed time.
Output files are never overwritten. Failed jobs are not accepted results;
release or re-reserve their same ID. If a block times out, report it rather
than silently increasing limits or changing the quadrature. A smaller-block
revision would need a new plan identity.

The largest case contains 430,707,200 points; total points are 440,625,920.
No full-run wall-time estimate is asserted before independent pilots.
Complete independent replay requires a second pass of the same computation.

## Independent verification and collection

On the verifier's own resource, with the exact pinned package:

```bash
python3 worker.py verify h1d4_mu1d4-0000.json --donated-compute --out replay-h1d4_mu1d4-0000.json
```

The verifier repeats that whole block and demands identical integer endpoints
and input hash. A local replay by the original producer is reproducibility,
not independent replication; the tool deliberately does not claim independence.
Return the replay file and identity of the original result hash. The public
ledger, not a self-declared JSON flag, establishes who checked which block.

To combine a configuration, put **only its production result JSONs** in a
new directory. Keep pilots, replay files and other configurations separate.

```bash
python3 worker.py collect --config h1d4_mu1d4 returns-small --out collected-small.json
```

The collector rejects duplicates, missing IDs, wrong source/plan/configuration,
invalid intervals, failed normalization and exceeded error budgets. It sums
integer endpoints exactly and adds the quadrature error once. Even a complete
collection is labelled **PROVISIONAL** pending review of all independent
replays. Hash checking alone does not establish the validity of a returned
integral. No channel is silently promoted to a physical PASS.

## Scope of this release

Six inherited mathematical modules are byte-identical to the pinned sources;
provenance.json records Git blob identities. kernel.cpp extends the existing
integer interval kernel to five variables, orders up to 128 and bounded
disjoint grid ranges. New preparation, controls and worker code are included
in manifest.json. No binary is distributed. No production run is triggered
by publishing or opening this package. No GitHub Actions workflow is added.
