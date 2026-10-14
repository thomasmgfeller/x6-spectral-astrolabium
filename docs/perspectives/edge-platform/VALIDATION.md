# X6 Edge Reference 0.1.0 — validation record

Publication date: 14 October 2026. **Experimental local software evidence.**
Base repository commit: `9c8ef27f73bcd5f11157a4cdd15c4e5a07f737cc`.
Tests below were executed on the publication working tree. Source digests are
recorded in `EDGE_REFERENCE_SOURCE_MANIFEST.json` and the attached reports;
the containing Git commit identifies the published snapshot.

## Executed checks

| Check | Observed result | Scope |
| --- | --- | --- |
| New local adapter tests | 11/11 PASS | CLI, replay, input limits, negative controls, no overwrite, input/result binding, forged numerical results, missing completion record |
| Existing Signal Lab core tests | 25/25 PASS | Numerical and synthetic adversarial fixtures |
| Existing Signal Lab evidence tests | 25/25 PASS | Hashing, replay, source declarations, fixed tolerances and tampered records |
| Independent NumPy/SciPy validation | 198/198 PASS | 16 run fixtures and 23 evaluation fixtures; arrays, filters and metrics within declared tolerances |
| Protected-source provenance tests | 16/16 PASS | Fixed baseline and rejection of unauthorised path/hash substitutions |
| Static application preflight | 15/15 PASS | HTML structure; no browser execution |
| License-only application diff | PASS | Exactly six notice substitutions; numerical core/evidence bytes unchanged |
| Repository inventory and Signal Lab build | PASS_WITH_EXCLUSIONS / PASS | Existing historical exclusions remain explicit; current tracked inventory verified |
| Documented example and second-process replay | EXECUTED / REPLAY_PASS | Complete local synthetic run; per-method quality is reported separately |

Detailed [independent reference report](evidence/independent-reference.json),
[evidence test report](evidence/evidence-tests.json), and
[local execution summary](evidence/local-validation.json) accompany this record.

Environment: Linux x86-64; Node.js 24.19.0; Python 3.12.14;
NumPy 2.3.5; SciPy 1.17.0. The local versions are recorded as observed, not
silently treated as the pinned reference environment. See the repository
requirements files for reproducing the independent test environment.
The GitHub workflow targets Node.js 22; its result must be read on the actual
publication commit and is not implied by these local results.

## Interpretation of the example

For the fixed synthetic pulse job, identity, moving average and FFT low-pass
passed the submitted screening gates; **X6 phase selection failed**. This is
retained in the exported record. `REPLAY_PASS` describes reproducibility and
integrity, not superiority of the X6 filter. One fixture is not an efficacy study.

## Reproduction

From the repository root:

```bash
node --test experimental/edge_reference/test_runner.cjs
node tests/signal-lab/test_core.cjs
node tests/signal-lab/test_evidence.cjs
python3 tests/signal-lab/reference_validation.py --report reference.local.json
python3 -m unittest discover -s tests/signal-lab -p test_provenance.py -v
python3 tests/python/static_ui_preflight.py
python3 tests/python/verify_manifest.py
python3 tools/build_signal_lab.py --check
```

The independent Python command requires NumPy and SciPy. The runtime adapter
uses no third-party npm dependencies. See its README for execution and replay.

## Not executed or established by this publication

Browser end-to-end tests, ARM64 execution, physical sensor tests, comparative
integration-cost measurements, production security assessment, hard real-time
qualification and Post-Quanten cryptographic profiles are not established here.
No external maker installation or multi-application platform transfer has been
demonstrated. Same-engine replay is not independent numerical validation;
the separate NumPy/SciPy tests cover only their declared finite fixtures.

The original protected research baseline and historical evidence remain intact.
See [license amendment details](NOTICE_UPDATE.md) for the exact approved source
pin changes. No scheduled research-agent run was started for this publication.
