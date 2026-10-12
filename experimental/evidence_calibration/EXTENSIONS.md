# X6 v4.4 experimental extensions (not activated)

Three standard-library modules: optical frame centroid/width/drift, Hamming(7,4)
single-bit-error reference, and fail-closed scientific comparison gate.

Run from repository root:
```
python -m unittest experimental.evidence_calibration.test_core experimental.evidence_calibration.test_extensions -v
```

Scope: fixtures and deterministic software only. No actual Sagnac, CMOS,
quantum-state tomography, GF-651 hardware, laser control, cryptographic
attestation, or physical safety certification. Hamming(7,4) can miscorrect
multi-bit errors; it is NOT a BCH/RS/LDPC or Golay implementation.
Thresholding and centroid tracking are classical optics/image processing.

Do not integrate with `app/index.html` or alter the pinned research
agent app hash during the authorized pilot ending 2026-10-16 Europe/Zurich.
Before adoption: CI execution, recorded real-data baselines, negative tests,
uncertainty budgets, and independent review are required.
