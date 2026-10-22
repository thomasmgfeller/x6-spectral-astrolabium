# Joint membership atoms: validated bound and resolution audit

SPDX-License-Identifier: Apache-2.0

**Result: HOLD_VOLUME_RESOLUTION.** The full-law atom bound is implemented and
validated, but does not improve the TV certificate for the unchanged PR95 pair
within the fixed integration budget. This is a useful numerical limitation,
not evidence of statistical distinguishability or stability.

| Check | Result |
|---|---|
| Exact toy atom certificate | TV <=0.070711784 versus coupling <=0.632120559 |
| Actual pair, partitions | 16³, 32³, 64³; 299,008 cells per geometry total |
| Final certified nonzero labels | 48 per geometry; others are not assumed absent |
| Unresolved mean upper bound | 11,771.54685595 per geometry |
| Ideal equal residual allowance at zero known distance | 0.015625 per geometry |
| Actual-pair atom TV upper bound | 1; no improvement |
| Retained earlier coupling TV upper bound | 0.24999999774322784776 |

The method partitions by all 90 membership bits, preserving arbitrary count
and overlap dependence. Unknown labels remain in a rigorous residual-mass
bound. The audit includes an exact three-bit counterexample to identifying
the law from first/second moments, 1,719 exact point-membership checks,
monotone lower volumes, a boundary-crossing control and invalid-input checks.

- [Derivation, source and scope](THEORY.md)
- [Contract](contract.json), [results](summary.json), [audit](audit.json)
- [Complete integer volume records](partitions.json.gz)

Reproduce from repository root:

```sh
python3 -B research/lorentz_local_dalembert/joint_atoms/ja_run.py --verify
python3 -B research/lorentz_local_dalembert/joint_atoms/ja_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/joint_atoms/SHA256SUMS
python3 tests/python/verify_manifest.py
```

Next: validated paired atom-intensity DIFFERENCES with shared uncertainty,
before more geometry optimization. Do not extrapolate the toy improvement to
the real pair or delete unseen labels. No global stability or physical claim;
all scientific HOLDs remain.
