# X6 Scientific Evidence & Calibration — isolated v0.2 remediation

Experimental, software-qualified only. **No physical validation, automatic
hardware operation, calibration certification, GF-651 or quantum advantage.**
This directory does not change the main X6 app, research programs or their
operating window. Only its own isolated CI is changed.

## Reproduce

From repository root, with Python 3.12 or 3.13 and no extra dependencies:

```sh
python -m unittest discover -s experimental/evidence_calibration -t . -v
python -m experimental.evidence_calibration.run_qualification --output evidence-output --protect-research
```

The output path must be new. In an offline module-only snapshot omit
`--protect-research`; the report then explicitly records that the app hash was
NOT checked. No fresh research or data-source runs are invoked by either command.
The qualification command is a reproducible software test run, **not general
computational replay of an archived experiment**.

## Corrected contracts

* Gate flags must be actual booleans; numbers exclude booleans, NaN and infinity.
  `PASS` is lower-is-better screening against caller-supplied flags and limits,
  not authenticated calibration, statistical significance or safety approval.
* Optical files are read once into bounded bytes (16 MiB, 1 million pixels).
  Parsing and SHA-256 consume that same snapshot. Complete, atomically published
  input files remain the producer's responsibility; two frames are not acquired
  simultaneously by this importer.
* Centroids use scaled weights to avoid intermediate overflow. Nonrepresentable
  totals/scaled distances are rejected. Background, saturation and crop can mimic
  motion; `sigma_x/y` are RMS widths in input pixels, not calibrated resolution.
* Evidence records snapshot nested JSON values. Verification checks schema and
  hashes, not truth of submitted results, authenticity, trusted timestamps or
  immutable storage. A caller that edits content AND rehashes it can still pass.
* Descriptive SD/SE has finite-output checks. SE assumes independent replicates;
  systematic error, temporal correlation and metrological uncertainty are open.
* Hamming(7,4) is a classical reference with single-bit correction only. Multi-bit
  errors may miscorrect or have zero syndrome. It is not a GF-651/Golay decoder.

## Recorded optical metadata migration (intentional v0.2 tightening)

In addition to `instrument_id`, `pixel_pitch_um`, `acquired_utc`, `calibration_id`:

```json
{
  "evidence_class": "SYNTHETIC",
  "coordinate_plane": "synthetic_grid",
  "scale_model": "effective_isotropic_um_per_input_pixel"
}
```

`evidence_class` must be `SYNTHETIC` or `RECORDED_UNVERIFIED`. Legacy four-field
metadata returns `UNQUALIFIED_METADATA` rather than being silently treated as
measured evidence. Valid synthetic outputs are `SYNTHETIC_RESULT`; recorded
outputs stay `UNVERIFIED_MEASUREMENT`. A calibration ID alone is never proof.
UTC timestamps require `YYYY-MM-DDTHH:MM:SS[.ffffff]Z` or `+00:00`.

`pixel_pitch_um` now explicitly denotes the **effective isotropic scale per INPUT
pixel in the named coordinate plane**, including resizing, binning and optical
magnification. This is a declared model, not a verified calibration. Anisotropic
or spatially varying calibration is not implemented; do not use this scalar
model for it. Both frames must have the same geometry and preprocessing; this
module checks dimensions but cannot authenticate that acquisition history.

## Regression and evidence

See `REMEDIATION.md` for audit-to-test traceability. CI archives test logs, actual
counts, environment, source snapshots and SHA-256 manifest, including failures.
Actions are fixed to revisions already used in the successful prior CI run;
this is version pinning, not an independent supply-chain audit. Artifact retention
is 30 days, not an immutable long-term research archive.

Still open before measurement release: independently recorded controlled data,
background/dark-frame and saturation qualification, known image scale and its
uncertainty, full uncertainty budget, true experiment replay, and independent
review. No hardware activation is authorized by any status in this directory.
