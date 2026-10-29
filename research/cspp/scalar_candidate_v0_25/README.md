# CSPP v0.25 — scalar candidate and two-scale exclusion

This publication preserves the completed v0.25 development package byte for byte. The normalized five-layer candidate at theta = 21 passes the original Gaussian L = 2 mean screen (relative bias 0.152525%) but fails the added L = 4 development control (84.648939%). At fixed q = 3/(16*pi), the entire normalized polynomial degree-at-most-four family fails the joint 10% mean screen for every real theta: its minimax relative bias is 28.473298%.

The exclusion concerns only these two Gaussian scales, the full-past mean, the stated normalization and fixed q. It does not exclude other q values, higher-degree kernels, different boundary constructions or scalar operators generally. L = 4 was added after exploratory calculations and is not preregistered independent validation. **METHOD and G1 remain HOLD.** No new random clouds or confirmation design were produced.

## Published evidence

- [Report (PDF)](Skalarer_Kandidat_Zweiskalenpruefung_v0_25.pdf)
- [Original reproducibility package (ZIP)](CSPP_Skalarer_Kandidat_v0_25_Pruefpaket.zip)
- [Derivation and scope](cspp_v025/PROOF.md), [protocol](cspp_v025/PROTOCOL.json) and [status](cspp_v025/STATUS.json)
- [128-bit certificate](cspp_v025/results/CERTIFICATE_128.json), [192-bit certificate](cspp_v025/results/CERTIFICATE_192.json), [independent checks](cspp_v025/results/CHECKS.json) and [recorded replay](cspp_v025/results/REPLAY.json)
- [Next work package](cspp_v025/NEXT_WORK_PACKAGE.md)
- [Publication metadata](PUBLICATION.json)

Algebraic infrared normalization, retarded structure and uniqueness of the finite history problem pass their stated checks. Density-uniform and infinite-past spectral stability are not certified. Compact-detector production and the full spectral search are explicitly `NOT_RUN_EARLY_ABORT`, following failure of the necessary development screen. A successful reproduction validates the published calculations and status bookkeeping; it does not turn the rejected candidate into a physical success or certify the open method gates.

## Reproduce

From the repository root, use Python **3.12.14** (the recorded version participates in certificate bytes):

```sh
python3 -m pip install python-flint==0.8.0 scipy==1.17.0 numpy==2.3.5
python3 -O -B research/cspp/scalar_candidate_v0_25/publication_check.py
python3 -B research/cspp/scalar_candidate_v0_25/publication_check.py --replay
```

The first command checks all 29 extracted files against the original ZIP, the 28 SHA-256 entries, both report copies, the recorded scope and the retained HOLD decisions. The replay copies the package to a temporary directory, reproduces both certificates byte for byte and runs the original verification suite without modifying published evidence. CI also checks that the publication subtree remains unchanged.

The original report and package describe publication as not performed in that development step. Those historical statements are preserved deliberately; this directory and `PUBLICATION.json` record the subsequent GitHub publication. Input evidence remains pinned to commit `4c755221b76364c02beca5e7a40c0f8d50931375` and the earlier source snapshots identified inside the package.
