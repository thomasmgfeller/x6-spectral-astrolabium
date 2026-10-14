# X6 Edge Reference 0.1.0

Experimental local reference adapter, licensed under Apache-2.0.
Copyright 2026 Thomas Gfeller.

This small command-line adapter reuses the existing X6 Signal Validation Lab
core and its evidence/replay module. It illustrates one local execution path
towards the [Edge Application Platform](../../docs/perspectives/edge-platform/README.md).
It is not an implementation of the complete platform.

## Run from a fresh checkout

Prerequisite: Node.js 22 or later. No npm packages, server, account or hardware
are required. The exact tested runtime/architecture is in the
[validation record](../../docs/perspectives/edge-platform/VALIDATION.md).

```bash
git clone --branch research/x6-edge-reference https://github.com/thomasmgfeller/x6-spectral-astrolabium.git
cd x6-spectral-astrolabium
node experimental/edge_reference/runner.cjs run experimental/edge_reference/examples/synthetic-signal.json x6-edge-run
node experimental/edge_reference/runner.cjs verify x6-edge-run
node --test experimental/edge_reference/test_runner.cjs
```

The output directory must not exist; its parent must exist. No existing run is
overwritten. Use a different directory for another attempt. Deinstallation is
removal of this checkout and any run directories you intentionally created.

| File | Contents |
| --- | --- |
| `input.json` | Exact bytes of the submitted job |
| `evidence.json` | Existing `x6.signal-lab.evidence/1` envelope: parameters, all generated arrays, four method outputs, diagnostics, methodology and declared source build |
| `run.json` | Completion record, job ID, runtime fingerprint, file/source digests, execution/replay status and per-method quality status |

`run.json` is written last. An interrupted export without this file is incomplete
and cannot pass verification. These files are a local run record, not a
transactional scheduler or signed provenance archive. Timestamps and environment
fields are recorded metadata; verification does not authenticate them.

The supplied job generates a synthetic pulse with seeded noise and compares
identity, centered moving average, FFT low-pass and X6 phase selection. It does
not import physical measurements. Original samples and all method outputs remain
available. A filter can fail its declared quality gates while export/replay succeeds.

## Meaning of results

- `EXECUTED`: the requested software execution completed.
- `REPLAY_PASS`: file hashes, input binding and recomputed values agree within
  the existing evidence module's fixed tolerances.
- `quality_status`: the original per-method `PASS`, `FAIL` or `INCONCLUSIVE`
  classification under the submitted screening thresholds.
- Process exit code 0 indicates successful execution or replay. It does not
  mean that every filter passed, or that the method is scientifically validated.
- Process exit code 1 indicates invalid input, export failure or verification
  failure. Error details go to stderr; no success record is emitted.

Replay reuses the same numerical implementation. Independent NumPy/SciPy tests
are separate; see the validation record. No physical, general hardware-portability,
real-time, cybersecurity or performance-superiority claim is made.

## Contract and resource scope

The versioned job shape has exactly three fields:

```json
{
  "schema": "x6.edge-reference.job/0.1",
  "job_id": "X6-EDGE-DEMO-0001",
  "parameters": {"signal": "pulse", "samples": 256, "noiseStd": 0.05}
}
```

`job_id` is 1–64 ASCII letters, digits, dots, underscores or hyphens; its first
character must be a letter or digit. `parameters` is a plain JSON object.
Omitted parameters are expanded by `X6SignalLab.defaults()` and exported in full.
Unknown fields are rejected. The authoritative parameter constraints are
`validate()` in [signal-lab-core.js](../../app/signal-lab-core.js); mathematical
definitions are in [SIGNAL_LAB_METHODS.md](../../docs/SIGNAL_LAB_METHODS.md).
This job envelope is a local prototype contract, not the future generic app/device schema.

The job file is limited to 64 KiB, signal lengths to powers of two from 128 to
4096, and an evidence file to 32 MiB. Nonfinite numbers are rejected. Fixed-size
limits bound the supported inputs; there is no enforced CPU/RAM quota or sandbox.
Only the bundled kernel runs. Jobs cannot supply executable code, network URLs,
device commands or arbitrary module names. The process runs with the caller's
ordinary OS permissions. Run only trusted project code.

Verification requires the matching runner and declared source build. Source
updates can intentionally invalidate replay with a different checkout; retain
the publication commit with your records. Hashes detect inconsistency, not
authorship: an attacker able to replace an entire coherent run can create a new
synthetic record. No claim of tamper-proof or authenticated measurements is made.

## Negative control

```bash
node experimental/edge_reference/runner.cjs run experimental/edge_reference/examples/invalid-job.json invalid-run
```

Expected: exit code 1 and no `invalid-run` directory (129 is not a power of two).
