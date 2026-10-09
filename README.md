# X6 Spectral Astrolabium

**Public Research Preview — independent validation requested. NOT a scientifically certified stable release.**

This repository publishes the actual **X6 v4.2 RC** browser application, alongside the **v4.3 community audit kit**. The application combines experimental signal/Fourier analysis, a model-dependent signal-to-graph mapping, and exact rational lower bounds for finite weighted undirected graph Laplacians.

## Run

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

## Help wanted

We invite independent Julia reproductions, exact certificate audits, browser/translation/accessibility tests, security reviews and counterexamples. Use the GitHub issue forms and [community guide](docs/COMMUNITY_VALIDATION.md). Report PASS, FAIL and NOT_EXECUTED distinctly.

## License status

**License selection pending.** Public visibility is not permission to reuse or redistribute. Maintainer must review [license options](docs/LICENSE_OPTIONS.md), copyright ownership and bundled dependencies before adding a real `LICENSE` file. Code contributions should wait until contribution terms are confirmed; audit reports and issues are welcome.

See [provenance](docs/PROVENANCE.md), [release checklist](docs/RELEASE_CHECKLIST.md), and draft [citation metadata](CITATION.cff).
