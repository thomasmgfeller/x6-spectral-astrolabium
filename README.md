# X6 Spectral Astrolabium

**Public Research Preview — independent validation requested. NOT a scientifically certified stable release.**

This repository publishes the actual **X6 v4.2 RC** browser application, alongside the **v4.3 community audit kit**. The application combines experimental signal/Fourier analysis, a model-dependent signal-to-graph mapping, and exact rational lower bounds for finite weighted undirected graph Laplacians.

## Run

**Experimental software.** Do not enter confidential data; this is not a production-hardened service. The browser's local qualification is not independent scientific certification.

Open `app/index.html` in a browser, or run `python -m http.server 8000` and visit `http://localhost:8000/app/`.

## Signal Validation Lab

Open the [Signal Validation Lab](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/signal-lab.html)
or `app/signal-lab.html` locally. This isolated DE/EN/FR extension compares known
synthetic signals with identity, centered moving average, periodic FFT low-pass
and the original X6 phase-selection method. Noise, gain, phase, signed delay,
clipping and quantization are explicit, seeded and reproducible. The comparison
uses actual time-series errors, Welch spectra, cross-phase and coherence with
declared acceptance limits and explicit undefined/ambiguous results.

Eight adversarial cases expose false quality judgments, including polarity
inversion with unchanged PSD/coherence, periodic delay ambiguity and removal of
a clean signal by the X6 phase filter. JSON exports preserve all input/output
arrays, parameters, results, source hashes and optional counterexamples; import
checks the digest and actually recomputes the experiment. CSV exports contain
every sample from all four methods.

The app runs without external frontend dependencies or a backend. The existing
Astrolabium app, scheduled agents and their pinned research sources are unchanged.
The lab's own **X6 Signal Lab** CI checks numerical reference results and browser
behavior; it does not activate research agents or hardware.

Read [usage, exports and qualification](docs/SIGNAL_VALIDATION_LAB.md) and
[mathematical definitions and limitations](docs/SIGNAL_LAB_METHODS.md).
These are synthetic software experiments, not measured device performance or
physical/quantum qualification. A hash or a successful replay is not authenticity.

## Astrolabium Control and Validation Module — concept 0.1

[ACVM concept and evidence status](docs/acvm/README.md) describes a proposed
control and validation module for reproducible experiment sequences, FPGA
execution, independent acquisition and explicit acceptance criteria.
The German concept is available as readable Markdown and as the original Word
document. **Concept only: implementation and hardware qualification are pending.**
Its ten proposed checks are NOT RUN; publication does not establish working
device control, validated photonics or a quantum processor.

[ACVM Experiment Records — concept 0.1](docs/acvm/experiment-records/README.md)
specifies the proposed Run Archive data model, provenance and acceptance plan.
Its fourteen Records checks are NOT_RUN; implementation and adapter qualification
remain pending. The German Markdown and unchanged Word concept are included.

## Experimental Sagnac integration preview 0.1

This experimental extension adds tab **07 · Sagnac**: validated SGNCv007 binary
capture import, an explicitly synthetic example, and a loopback-only Linux
UART receiver. Start `python3 device/sagnac_bridge.py` and open its URL.
All quantum/physical claims remain NOT_ASSESSED. Optical control is unavailable;
no command path or qualified actuators are implemented. Physical hardware
qualification remains open. No scheduled research agent is activated or modified.

The **X6 Validation** workflow checks the decoder, local bridge, Chromium UI,
mobile viewport and existing scientific modules. Consult the checks on the
specific commit; software success does not establish physical validity.

Read [Sagnac integration and test scope](docs/SAGNAC_INTEGRATION.md).

## Photonic two-qubit experiment — design preview

[Complete experimental design and supporting materials](experiments/photonic-two-qubit/README.md): Sagnac source concept, v0.7 RTL/host reference, fabrication CAD and corrected Jig manual, detector-development archives, source literature and staged laboratory protocol. The **Photonic Reference** workflow checks software and mechanical models. No physical measurements, demonstrated entanglement, quantum processor or hardware qualification are claimed.

## Reproduce existing scientific modules

```bash
python tests/python/independent_audit.py
julia tests/julia/reference.jl
python -m pip install -r requirements-test.txt
python -m playwright install chromium
python tests/browser/browser_test.py
```

Python tests exact rational bounds; Julia tests numerical eigenvalues (not a formal proof); browser automation tests the existing qualification gate (not all UI functionality). CI results must be interpreted within these scopes.

## Mathematical scope

For a connected graph Laplacian L, n vertices, and J the all-ones matrix:

`M(b) = L + ((b+1)/n) J - b I` is positive definite exactly when `lambda_2(L) > b`.

This certifies the **rounded rational graph**, not unrounded signal values or a quantum-gravity theory. Disconnected graphs require special treatment. Read [scientific scope](docs/SCIENTIFIC_SCOPE.md).

## Automated public-data checks

**Current run window: 11–13 October 2026.** All four agents stop by
14 October 2026, 00:26:52 Europe/Zurich. Their workflows enforce the cutoff
before any data work; automatic runs on code changes are disabled. Existing
results keep the retention periods below.

The [X6 Data Agent](docs/DATA_AGENT.md) downloads public NOAA GOES X-ray observations, drives the actual browser app, and separately checks its exported rational graph certificate in Python. The bounded daily workflow uploads inputs and evidence as Actions artifacts for 30 days. PASS means the named software checks passed; it does not establish denoising performance or physical validity.

Three additional [source agents](docs/SOURCE_AGENTS.md) check the complete NetworkX Graph Atlas and fixed experimental subsets from QuTech and NASA/IMS. They run daily as separate jobs, preserve original inputs and failure evidence for 14 days, and label archival measurements explicitly. They do not claim fresh quantum measurements, improved coherence or bearing-failure prediction.

## Open research agenda

**Current priority: Lorentzian spectral geometry.** The
[bounded research agent](docs/MATH_AGENT.md) reproduces exact small-causal-order
classification and compares independent 1+1-dimensional diamond samples with
the known causal-propagator spectrum. Signal/graph controls continue alongside.
See [definitions, literature and next research gates](docs/LORENTZ_RESEARCH.md).
Runs are attempted every six hours during the same pilot window, with a
90-second research budget and mandatory cutoff at 14 October 2026,
00:26:52 Europe/Zurich. These are replication/calibration results; no new
theorem, general continuum limit or physical validation is claimed.

See the [X6 Working Paper v0.3](docs/X6_OPEN_RESEARCH_AGENDA_DRAFT.md) for falsifiable research questions and proposed industrial pilots in signal denoising, quantum readout analysis, and cryptographic graph verification. These are proposals, not validated product performance or physical claims.

## Help wanted

We invite independent Julia reproductions, exact certificate audits, browser/translation/accessibility tests, security reviews and counterexamples. Use the GitHub issue forms and [community guide](docs/COMMUNITY_VALIDATION.md). Report PASS, FAIL and NOT_EXECUTED distinctly.

## License status

**Apache License 2.0 — granted by the maintainer on 13 October 2026.**
Original project code, documentation, reports and original data are licensed
under [Apache-2.0](LICENSE), subject to the [licensing scope](LICENSE_SCOPE.md).
Copyright 2026 Thomas Gfeller. See [NOTICE](NOTICE).

Separately licensed components, including MIT Sagnac/photonic reference
packages, retain their own licenses. External datasets and third-party works
are not relicensed. This licensing decision is not scientific certification
or a completed independent rights audit. See the
[dated activation record](docs/LICENSE_ACTIVATION_2026-10-13.md).

See [provenance](docs/PROVENANCE.md), [release checklist](docs/RELEASE_CHECKLIST.md), and draft [citation metadata](CITATION.cff).

