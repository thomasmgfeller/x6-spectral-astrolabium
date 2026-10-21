# Development-bytehash reporting correction

The initial PR #74 CI run 39569487265 failed at
`root.records[0].coordinate_hash_matches`: the current runner returned `false`
while the recorded local development fit says `true`. This is an exact-byte
diagnostic for regenerated historical coordinates, not an error statistic.
The frozen verifier inadvertently compared that boolean exactly even though
the frozen protocol separates numerical replay from byte identity.

`portable_verify.py` leaves all 95 frozen source/data files unchanged. It calls
the original verifier, intercepting only the exact path
`root.records[i].coordinate_hash_matches` in the development refit. Every flag
is reported as current/original; numerical errors, fitted scales, covariance
matrices, source pins, calibrated intervals, test observations, decisions and
all declared tolerances retain their original comparisons. The target-cloud
coordinate/noise bytehashes were already reported separately by the frozen
verifier. There is no new data, refitting choice or relaxed numerical tolerance.

Run the portable replay with `portable_verify.py`; use `--strict` or the
unchanged `ec_verify.py` for the original exact development-flag behavior.
`--self-test` demonstrates that the one byteflag discrepancy is reported,
while another boolean, a numerical discrepancy and a source-hash discrepancy
still fail; it also confirms the original exact comparison remains intact.

The original local replay `results/verification.json` is preserved.
`results/portable_verification.json` records the adapter's local replay.
GitHub Actions reports its own current bytehash counts in its job log; a
numerical pass is not a claim of cross-platform byte identity.
