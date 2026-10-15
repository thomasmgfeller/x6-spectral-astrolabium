# A clear route into the research

Choose a practical starting point, understand the evidence classes, and find the exact sources behind a result.

## 1. Understand the project

A signal is a sequence of measurements, such as vibration over time. A graph describes elements and their connections. A causal order describes which events precede others. X6 explores methods for analysing these mathematical objects and checking their results.

A spectrum is a collection of values derived from a matrix. Different structures can share a spectrum; the project includes explicit counterexamples. A pattern in an image alone is not evidence for prime numbers or a new physical mechanism.

The current priority is Lorentzian spectral geometry. Signal processing, RAX, photonics and industrial data studies have their own scopes and acceptance gates. There is no claim of a completed quantum computer or a proven quantum-gravity theory.

- [Lorentz: exact finite causal-order references](https://thomasmgfeller.github.io/x6-spectral-astrolabium/modules/lorentz-n6-residuals.html)
- [X6-QE: structures with the same spectrum](https://thomasmgfeller.github.io/x6-spectral-astrolabium/modules/x6-qe.html)
- [Browse every registered research module](https://thomasmgfeller.github.io/x6-spectral-astrolabium/modules/index.html)

## 2. Try a browser experiment

Open Signal Validation Lab. Start with a synthetic example whose clean signal is known. Compare the original signal, a noisy version and the reference-filter outputs. Inspect reconstruction errors as well as spectral summaries.

Explore the documented counterexamples, including polarity inversion: a signal and its negative can share a power spectrum. Similar-looking spectral summaries do not establish faithful signal recovery.

Export the experiment evidence and use the documented import/replay workflow to check the calculation. A successful replay shows computational consistency within that workflow; it does not prove data authenticity or physical device performance.

- [Open Signal Validation Lab (DE / EN / FR)](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/signal-lab.html)
- [Read the Signal Lab scope and expected results](https://thomasmgfeller.github.io/x6-spectral-astrolabium/modules/signal-lab.html)
- [Open the original Astrolabium application](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/index.html)
- [Install and run the local workflow](https://thomasmgfeller.github.io/x6-spectral-astrolabium/modules/integration.html)

## 3. Reproduce a reference calculation

For the common offline reference suite, install Git, Python 3.12 and Node.js 24 first. Cloning requires network access; the reference computation itself needs no package download or new Wolfram call. Use a fresh output directory.

The commands below reproduce the current main checkout. For a versioned result, use the reference-edition page and its pinned source commit or immutable release package. Record the commit and runtime versions in any report.

Expected status: PASS_OFFLINE_REFERENCE_REPLAY. Read the individual report scopes and rejection controls. Reproducing a negative or inconclusive scientific result can be the correct software outcome.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6
cd x6
python3 -S -B x6.py reference qualify --output /tmp/x6-reference-evidence
```

- [Pinned reference edition and external reproduction instructions](https://thomasmgfeller.github.io/x6-spectral-astrolabium/modules/reference-edition.html)
- [Offline suite: prerequisites, evidence and next acceptance gate](https://thomasmgfeller.github.io/x6-spectral-astrolabium/modules/offline-reference.html)
- [Full offline-suite documentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/OFFLINE_REFERENCE.md)
- [Report a reproducible result or counterexample](https://github.com/thomasmgfeller/x6-spectral-astrolabium/issues/new/choose)

## 4. Interpret status and evidence

MAIN means the registered source is available in the main branch. BRANCH_ONLY means the documented research source requires the named branch and pinned commit. These are source-location labels, not quality ratings.

SOFTWARE means a bounded executable checking path is documented. CONCEPT and DOSSIER describe plans or documents without a standalone executable whole. A photonics module can be SOFTWARE because its digital reference is testable while the physical device remains unqualified.

An exact finite computation concerns its specified finite objects. A numerical simulation concerns its model and assumptions. Archived laboratory data are measurements from their original acquisition context. None of these automatically establish a new physical measurement, industrial superiority or independent external review.

PASS, FAIL, NOT_RUN, NOT_READY and INCONCLUSIVE have different meanings. Read the stated claim, the evidence report and the next acceptance gate together. Each evidence report retains its own checked revision; a newer source pin does not retroactively qualify changed code.

- [Read all module scopes](https://thomasmgfeller.github.io/x6-spectral-astrolabium/modules/index.html)
- [Machine-readable source of truth](https://thomasmgfeller.github.io/x6-spectral-astrolabium/MODULE_REGISTRY.json)

## 5. Cite, reuse and contribute

Cite the precise release or commit you used, and cite external datasets separately. CITATION.cff describes the selected finite reference edition; it is not a certification of every module.

Original project contributions use Apache-2.0. Separately licensed components and datasets keep their own conditions. Included Paderborn data retain CC BY-NC 4.0; the portal does not grant commercial rights to those data.

Useful contributions include independent reproductions, counterexamples, accessibility improvements and clearer documentation. The optional llms.txt and JSON index help navigation; they do not guarantee indexing, ranking or inclusion in an AI answer.

- [Citation metadata](https://thomasmgfeller.github.io/x6-spectral-astrolabium/CITATION.cff)
- [License scope and third-party terms](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/LICENSE_SCOPE.md)
- [Contribution guide](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/CONTRIBUTING.md)
- [Optional navigation for AI tools](https://thomasmgfeller.github.io/x6-spectral-astrolabium/llms.txt)
- [Documentation sitemap](https://thomasmgfeller.github.io/x6-spectral-astrolabium/sitemap.xml)
