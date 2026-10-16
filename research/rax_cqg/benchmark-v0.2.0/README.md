# RAX-CQG Causal-Set Benchmark

Version 0.2.0 · 16 October 2026

A reproducible finite-order benchmark and an offline laboratory. This release repairs the supplied experimental code and separates implemented mathematics from physical hypotheses. It is **not a validated theory of quantum gravity**, a derivation of quantum mechanics, or evidence for emergent spacetime.

The useful research contribution is a checkable implementation: explicit ensembles, exact small-order reference cases, independently checked diagnostics, portable random-number conventions, raw matrices, and reproducible pilot data. Scientific novelty has not been established.

## Start here

Open `rax_cqg_lab.html` in a modern browser. It contains its JavaScript and styles and needs no server, CDN or installation. BigInt and SVG support are required. Matrix hashing uses Web Crypto where available; importing a record with a hash requires that API. The lab supports generation, real spectra, interval counts, induced-order thinning, JSON import/export, and a separate finite-clock reference.

For the Python tools and complete checks, use Python 3.12 and Node.js 24:

```sh
python -m venv .venv
# Activate the environment using the command appropriate to your shell.
python -m pip install -r requirements.txt
python rax_cqg_twin.py --model minkowski_4d --size 30 --seed 42 --output experiment.json
python rax_cqg_matter_astrolab.py
python rax_cqg_reference_models.py
python validate.py
```

The core and reference models require NumPy. SciPy is used for statistical summaries and independent checks. Node runs the JavaScript parity and UI logic checks; no npm packages are required.

After changing the web sources:

```sh
python build_web.py
python validate.py
```

To intentionally regenerate the pilot data after a generator change:

```sh
python run_sweep.py
python validate.py
```

`validate.py` checks the stored sweep against its source hashes and regenerates its matrices from the recorded seeds. It does not silently regenerate the stored data. A generator change requires an explicit data update and review.

## Contents

| File | Role |
|---|---|
| `rax_cqg_twin.py` | Strict partial orders, six generators, interval counts, graph spectra, thinning, JSON records |
| `rax_cqg_matter_astrolab.py` | Positive classical Gaussian graph-field reference |
| `rax_cqg_reference_models.py` | Assumed two-qubit clock and classical move examples |
| `rax_cqg_lab.html` | Standalone offline lab, built from `web/` |
| `rax_cqg_sweep_results.json` | 240 newly computed pilot runs with raw relations and provenance |
| `MODEL_CONTRACT.md` | Mathematical definitions, assumptions and interpretation limits |
| `CHANGELOG.md` | Defect-by-defect repair record and incompatible changes |
| `CLAIMS.json` | Machine-readable evidence boundaries |
| `VALIDATION.json`, `evidence/` | Results and logs of the bounded release checks |
| `tests/`, `validate.py` | Reproducible verification code |

## What is checked

The recorded release run passed 28 Python test methods, including exhaustive independent reachability and interval checks on all 1,024 upper-triangular DAGs on five fixed labels (357 distinct transitive orders). It also passed 28 Python/JavaScript parity cases and 16 UI logic checks. Every one of the 240 pilot runs was replayed; all 30 group means and confidence intervals were checked.

Matrix parity is exact in the tested cases. Floating-point diagnostics use absolute and relative tolerances of `1e-9`. The browser implements a symmetric Jacobi eigensolver; Python uses NumPy's symmetric eigensolver. Continuous-coordinate generation near a floating-point light cone is not guaranteed to be bit-identical on every platform or seed. Exported matrices are therefore retained as the authoritative computational record.

**Visual testing in an actual browser has not been performed in this environment.** The UI checks execute the actual built scripts in Node with a minimal DOM; they cover application logic, not layout, browser compatibility, accessibility or downloadable-file behaviour. No hardware experiment, continuum-limit study or external peer review is represented by these checks.

## Pilot study

The fixed study grid is `N = 8, 16, 24, 32, 48`, with eight seeded replicates of each of six configurations: percolation at `p = 0.15, 0.25, 0.35`, adjacent-layer sampling at `p = 0.5`, and fixed-N uniform volume samples in 2D and 4D Minkowski diamonds. The grid is encoded in `run_sweep.py`; this is an exploratory pilot, not an externally preregistered study.

Student-t intervals describe the approximate sampling uncertainty of the group mean under these generators. They do not include systematic errors, guarantee independence of pseudorandom streams, or account for multiple comparisons. With only eight replicates, they should not support strong inference. Undefined quantities remain null and their counts are reported. Ensembles differ in density; raw differences alone do not show sensitivity to geometry beyond graph density or size.

## Publication status and next scientific question

This package is suitable to submit for public scrutiny as a **research software prototype with finite reference tests**. GitHub publication itself is not peer review. The package has not been uploaded to GitHub as part of this repair.

A useful next investigation is whether any specified observable distinguishes these ensembles after matching or controlling for size and ordering fraction. That would require a prespecified observable, density-matched controls, adequate replicate counts, effect sizes with uncertainty, and independent confirmation. The present pilot does not answer that question.

The growth index is a construction/counting parameter. No mapping to a measured clock time is implemented. The finite quantum clock assumes quantum mechanics and is not coupled to the causal-set generator. No noncommutative QSG dynamics, Bell-causality solution, KR suppression, Hauptvermutung proof, gravitational field equation or continuum limit is claimed.

See `MODEL_CONTRACT.md` for primary references and `CHANGELOG.md` before migrating old code. Released under Apache-2.0; see `LICENSE` and `THIRD_PARTY_NOTICES.txt`.
