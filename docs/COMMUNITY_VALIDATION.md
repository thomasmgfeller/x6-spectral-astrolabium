# Community validation protocol

1. Pin the commit and record SHA-256 of `app/index.html`.
2. Run `python tests/python/independent_audit.py`; introduce deliberate false bounds.
3. Run `julia --version` and `julia tests/julia/reference.jl`; record BLAS and tolerance. Numerical matches are not proofs.
4. Install Playwright and run `python tests/browser/browser_test.py`; manually test Chromium, Firefox, WebKit, DE/EN/FR, keyboard and export.
5. Rebuild exported graph Laplacians independently; ignore any claimed PASS flag and verify exact matrix positivity.
6. Optional Wolfram: independently compute exact eigenvalues or principal minors; attach actual kernel output.
7. File reproducible issues with input, commands, environment, expected/actual, evidence and PASS/FAIL/NOT_EXECUTED.

Stable release requires explicit maintainer approval after independent audits and resolution of blocking failures.
