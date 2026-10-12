# X6 Scientific Evidence & Calibration — isolated v0.1

**Experimental only. No device control, safety approval, quantum claim or performance claim.**

This is a non-invasive precursor to the proposed X6 v4.4 modules. It does **not**
change `app/index.html`, the pinned `app_sha256`, the existing research agent,
or any GitHub Actions workflow. The running 2026-10-16 pilot remains isolated.

Implemented: content-based SHA-256 evidence records; canonical JSON integrity
verification; deterministic Cartesian parameter sweeps; descriptive replicate
statistics (sample SD and SE with independence caveat).

Not implemented: immutable external storage, trusted timestamping, signed
attestations, actual camera/Sagnac adapters, real ECC decoders, automatic
drift compensation, physics-model validation or production authorization.

Run from repository root:

```sh
python -m unittest experimental.evidence_calibration.test_core -v
```

Future modules must use fixture-based and then measured datasets, explicit
uncertainty models, baseline comparisons, negative tests, and independently
reviewed hardware safety boundaries before activation.
