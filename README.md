# X6 Spectral Astrolabium

**Public Research Preview — independent validation requested. NOT a scientifically certified stable release.**

This repository publishes the actual **X6 v4.2 RC** browser application, alongside the **v4.3 community audit kit**. The application combines experimental signal/Fourier analysis, a model-dependent signal-to-graph mapping, and exact rational lower bounds for finite weighted undirected graph Laplacians.

## Lorentz: die vier n=6-Restpaare

Die [gezielte Restpaaranalyse](research/lorentz_n6_residuals/README.md) trennt alle vier
Paare mit gerichteten Gradpaaren und einer einfachen Zukunftszählung. Exakte
Wolfram-Gegenrechnung, Offline-Replay und Gegenbeispiele bei n=7/n=8 sind enthalten.
Die nächste Hypothese betrifft beide gerichteten Zählgrößen bei n≤7;
n=7 mit Höhe ≥3 bleibt offen. Die gemeinsame Referenzsuite umfasst jetzt neun Berichte.

## Start here: actual module and evidence status

The [central module register](docs/MODULE_REGISTRY.md) lists **33 modules** with
their authoritative branch and commit, prerequisites, executable entry point,
expected result, available evidence and next acceptance gate. Its
[machine-readable source](MODULE_REGISTRY.json) is a dated snapshot, not a live
qualification badge. Concepts without an executable package are marked explicitly.

The integrated CLI, Signal Lab, Edge reference, Sagnac import, ACVM C1/0.2 and
published RAX/Wolfram packages are in **main**. The n=6 atlas generator, Industrial V1
assessor, fingerprints, Experiment Fabric, Neutral Discovery, NQK dossier and
Photonic Link still have separate research sources; use their pinned checkout
instructions in the register. A historical branch tip is not proof that its
features are absent from main.

## Run

**Experimental software.** Do not enter confidential data; this is not a production-hardened service. The browser's local qualification is not independent scientific certification.

Use the [unified local workflow](docs/INTEGRATION.md) from a checkout of **main**
(Python 3.12, Git and Node.js 22 or newer):

```sh
python3 x6.py setup --profile research
python3 x6.py doctor --profile research
python3 x6.py serve
```

Open the reported loopback URL for Astrolabium and Signal Validation Lab.
The same entry point runs `signal`, `spectral` and `rax`, verifies directories
or exported ZIPs, and imports native Signal Lab JSON without losing its format.
The [documented fresh-checkout procedure](docs/INTEGRATION.md#6-abnahme-aus-einem-frischen-checkout-wiederholen)
checks installation, execution, export and replay. Directly opening
`app/index.html` remains available for the existing browser-only application.

## Offline reference suite

From a fresh checkout with **Python 3.12 and Node.js 24** already available:

```sh
python3 -S -B x6.py reference qualify --output /tmp/x6-reference-evidence
```

The [common offline reference suite](docs/OFFLINE_REFERENCE.md) recomputes the
stored Wolfram packages, five rational graph cases and the n=6 causal-order atlas,
and checks the current Signal Lab core against the stored polarity reference.
No setup, package download or new Wolfram call is needed. Expected:
`PASS_OFFLINE_REFERENCE_REPLAY`, nine reports, 26 rejected bundle/domain controls plus 17 Lorentz-specific controls.
Relevant changes run the fresh-checkout acceptance in CI with networking disabled.

## X6 Edge Reference — experimental development perspective

[Concept, roadmap and evidence status](docs/perspectives/edge-platform/README.md)
introduce X6 as one reference application for a proposed generic Edge Application
Platform. The [local Node.js adapter](experimental/edge_reference/README.md)
executes a bounded synthetic signal job, exports its evidence and verifies it by
computational replay. The existing Signal Lab kernel is reused unchanged.

The executable baseline is already in **main**. The historical
[`research/x6-edge-reference`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/research/x6-edge-reference)
branch is retained for provenance; use the register's main pin to reproduce it.
This is an experimental software baseline: hardware adapters, a generic scheduler,
cross-architecture qualification, measured savings and security profiles remain
open. Read the [executed checks](docs/perspectives/edge-platform/VALIDATION.md).

## Signal Validation Lab

[Executed Wolfram zero-failure/dependence countercheck](docs/signal-lab/wolfram-zero-failures-v0.1/README.md)
compares twenty independent trials with twenty copies of one trial. Twelve Wolfram
checks and seven Python comparisons verify exact confidence bounds and an explicit
coverage counterexample. This constructed model test does not audit project datasets.

[Executed Wolfram polarity-inversion countercheck](docs/signal-lab/wolfram-polarity-v0.1/README.md)
provides the unchanged reproduction package, four symbolic identities and twelve
numerical checks. X6 correctly rejects the inverted signal despite unchanged PSD
and unit magnitude-squared coherence. The documented scope is synthetic computation.

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

## Astrolabium Control and Validation Module — reference 0.2

[ACVM concept and evidence status](docs/acvm/README.md) describes a proposed
control and validation module for reproducible experiment sequences, FPGA
execution, independent acquisition and explicit acceptance criteria.
The German concept is available as readable Markdown and as the original Word
document. The original 0.1 concept is retained as a historical specification.
Current implementation and evidence are tracked in the following separate modules;
publication does not establish validated photonics or a quantum processor.

[ACVM 0.2 — optical/reference workflow](docs/acvm/optical-v0.2/README.md)
adds a complex-signal reference core, full-byte archives, ELL14 motor and legacy
PM100D adapters, calibrated QHQ phase mapping and bounded slow power feedback.
Run `python3 x6.py acvm qualify --output runs/acvm-v02`.
V01–V08 are exercised in software; V09/V10 and physical closed-loop/feed-forward
remain unperformed. Component choices and concrete laboratory acceptance steps
are documented; hardware adapters are not yet device-qualified.

[Crystal, Sagnac loop and oven specification 0.1](docs/acvm/sagnac-components-v0.1/README.md)
publishes the approved ten-page engineering document. It defines the type-II
ppKTP procurement profile, a shared triangular loop with 22.5° mirror incidence,
temperature requirements and twelve unperformed acceptance checks.
Supplier confirmation, fabrication approval and physical validation remain open.

[ACVM C1 — executable single-channel reference](docs/acvm/control-channel-v0.1/README.md)
adds a bounded host-to-device command protocol, sequence compiler, portable C++
sequencer, Pico/MCP4921 target source and independent software tests.
Run `python3 x6.py control qualify --output runs/c1-qualification`.
The native core and virtual serial path are tested; the Pico target build,
electrical measurements and optical actuation remain unperformed. This limited
implementation does not complete the full ACVM concept validation programme.

[ACVM Experiment Records — concept 0.1](docs/acvm/experiment-records/README.md)
specifies the proposed Run Archive data model, provenance and acceptance plan.
Its fourteen Records checks are NOT_RUN; implementation and adapter qualification
remain pending. The German Markdown and unchanged Word concept are included.

[ACVM Electrical & Thermal Test Fixture — concept 0.1](docs/acvm/electrical-thermal-fixture/README.md)
adds a proposed electrical/thermal bench fixture, its original Word concept,
two separate illustrative design images and the complete download package.
ETF-T01–ETF-T14 remain NOT_RUN. The separate Astrolabium QD-01 chip image is a
provisional research concept, not a fabricated device or demonstrated qubit.

## Experimental Sagnac integration preview 0.1

This experimental extension adds tab **07 · Sagnac**: validated SGNCv007 binary
capture import, an explicitly synthetic example, and a loopback-only Linux
UART receiver. Start `python3 device/sagnac_bridge.py` and open its URL.
All quantum/physical claims remain NOT_ASSESSED. This acquisition/import module
does not issue optical commands. Separate ACVM C1/0.2 command paths and adapter
tests are available above; their physical actuator qualification remains open.
Physical hardware
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

[Executed Wolfram causal-order countercheck](docs/research/causal-order/wolfram-countercheck-v0.1/README.md)
provides an exact three-event example with equal spectra of S, A and their
commutator but no order-preserving isomorphism. Sixteen Wolfram assertions and an
independent integer-polynomial Python calculation verify this finite limitation
of the selected spectral fingerprint. No continuum or physical validation is claimed.

For a connected graph Laplacian L, n vertices, and J the all-ones matrix:

`M(b) = L + ((b+1)/n) J - b I` is positive definite exactly when `lambda_2(L) > b`.

This certifies the **rounded rational graph**, not unrounded signal values or a quantum-gravity theory. Disconnected graphs require special treatment. Read [scientific scope](docs/SCIENTIFIC_SCOPE.md).

## Automated public-data checks

**Current run window: 11–18 October 2026, including Sunday.** The exclusive
cutoff is **19 October 2026, 00:00:00 Europe/Zurich**
(`2026-10-18T22:00:00Z`). Four data jobs in two workflows and the bounded math
agent share this cutoff. Data/source workflows have no code-change triggers;
the math workflow also has guarded source-change qualification triggers.
Admission reserves the documented job budgets. A schedule is not evidence of
execution; the [register](docs/MODULE_REGISTRY.md#agentenfenster) links observed
runs and the authoritative configuration. Existing results keep the retention
periods below.

The [X6 Data Agent](docs/DATA_AGENT.md) downloads public NOAA GOES X-ray observations, drives the actual browser app, and separately checks its exported rational graph certificate in Python. The bounded daily workflow uploads inputs and evidence as Actions artifacts for 30 days. PASS means the named software checks passed; it does not establish denoising performance or physical validity.

Three additional [source agents](docs/SOURCE_AGENTS.md) check the complete NetworkX Graph Atlas and fixed experimental subsets from QuTech and NASA/IMS. They run daily as separate jobs, preserve original inputs and failure evidence for 14 days, and label archival measurements explicitly. They do not claim fresh quantum measurements, improved coherence or bearing-failure prediction.

## RAX — relational research programme v0.1

[Programme, work packages and evidence status](docs/research/rax/README.md)
introduce a staged investigation of predictive reductions, competing generators,
possible geometric representations and independent falsification tests.
The approved 14-page German research programme is available as a Word document.

**Executed synthetic control:** The [RAX-U1 countercheck v0.1](docs/research/rax/countercheck-v0.1/README.md)
publishes the approved four-page report and a complete reproducibility archive.
All 160 matrices and 3.2 million transitions were rechecked; the 40 decisions
remain 8 supported, 16 rejected and 16 inconclusive. The archive-loss incident
remains unresolved, and full acquisition qualification is not claimed.
This is internal, post-hoc checking, not external review or new physical evidence.
**Measurement-plan benchmark:** [RAX-B1 v0.1](docs/research/rax/benchmark-v0.1/README.md)
compares adaptive, optimized fixed and random plans at equal measurement budgets
with separate heldout data. All 67,584 test runs were independently replayed in
code. Adaptive plans have lower observed mean Brier scores; all eight prespecified
simultaneous superiority decisions remain inconclusive. The approved ten-page
report and complete raw-data/source archive are available. This is a finite
synthetic control, without external review or physical validation.

**Methods review:** [RAX-M1 v0.1](docs/research/rax/method-review-v0.1/README.md)
reproduces two validation defects: acceptance of a negative-index duplicate row
and an ineffective holdout-isolation unit test. It also documents callback-access
and freeze-attestation limits, with exact dependence and selection counterexamples.
The original data pass stricter coverage checks and full replay; all eight B1
primary conclusions remain inconclusive. The seven-page report, executable
examples and supplemental guards are published with the complete evidence package.
This is internal post-hoc review, without independent personnel or physical evidence.

**Exact Wolfram cross-check:** [RAX-W1 v0.1](docs/research/rax/wolfram-check-v0.1/README.md)
reconstructs 44 selected U1 matrices in Wolfram Language and matches their exact
hashes and properties against the published results and both historical Python
implementations. Ten valid reductions and 34 intended violations are identified;
symbolic conditions and explicit counterexamples are included. The approved
four-page report, all tool responses and complete offline verification package
are available. This is internal post-hoc checking with another computation
engine, without external personnel review or physical validation.

Open discovery (RAX-U2), geometry and singularity investigations remain planned.
Lorentzian and other structures remain competing candidates under the same rules.

## Open research agenda

**Current priority: Lorentzian spectral geometry.** The
[bounded research agent](docs/MATH_AGENT.md) reproduces exact small-causal-order
classification and compares independent 1+1-dimensional diamond samples with
the known causal-propagator spectrum. Signal/graph controls continue alongside.
See [definitions, literature and next research gates](docs/LORENTZ_RESEARCH.md).
Runs are attempted every six hours during the same pilot window, with a
90-second research budget and mandatory exclusive cutoff at **19 October 2026,
00:00:00 Europe/Zurich**. The separate n=6 atlas and later research modules are
located in the [module register](docs/MODULE_REGISTRY.md).
These are replication/calibration results; no new
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


