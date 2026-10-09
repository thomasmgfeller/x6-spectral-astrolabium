# X6 Spectral Astrolabium

**Public Research Preview — independent validation requested. NOT a scientifically certified stable release.**

This repository publishes the actual **X6 v4.2 RC** browser application, alongside the **v4.3 community audit kit**. The application combines experimental signal/Fourier analysis, a model-dependent signal-to-graph mapping, and exact rational lower bounds for finite weighted undirected graph Laplacians.

## Run

**Experimental software.** Do not enter confidential data; this is not a production-hardened service. The browser's local qualification is not independent scientific certification.

Open `app/index.html` in a browser, or run `python -m http.server 8000` and visit `http://localhost:8000/app/`.

## Reproduce

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

## Open research agenda

See the [X6 Working Paper v0.3](docs/X6_OPEN_RESEARCH_AGENDA_DRAFT.md) for falsifiable research questions and proposed industrial pilots in signal denoising, quantum readout analysis, and cryptographic graph verification. These are proposals, not validated product performance or physical claims.

## Help wanted

We invite independent Julia reproductions, exact certificate audits, browser/translation/accessibility tests, security reviews and counterexamples. Use the GitHub issue forms and [community guide](docs/COMMUNITY_VALIDATION.md). Report PASS, FAIL and NOT_EXECUTED distinctly.

## License status

**Apache-2.0 is intended but NOT yet granted.** Rights and provenance clearance is still in progress; no `LICENSE` file has been added. Public visibility does not itself grant permission to copy, modify, or redistribute code. Inspect the project online and submit audit findings or issues; do not assume open-source reuse rights. See [rights clearance](docs/APACHE_2_0_RIGHTS_CLEARANCE.md) and [dependency audit](docs/M1_20_DEPENDENCY_LICENSE_AUDIT.md).

See [provenance](docs/PROVENANCE.md), [release checklist](docs/RELEASE_CHECKLIST.md), and draft [citation metadata](CITATION.cff).
