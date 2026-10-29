# CSPP v0.24: method gates after the complete global budget

**Step 3 is complete. METHOD and G1 remain HOLD; no fresh confirmation.**
The next primary research task is an explicitly changed scalar candidate
with deterministic control and stability checks. No new candidate or grid
has been selected in this work.

## Documents and evidence

- [German report (PDF)](Gate_Neubewertung_Globale_Bilanz_v0_24.pdf)
- [Original reproducibility package (ZIP)](CSPP_Gate_Neubewertung_v0_24_Pruefpaket.zip)
- [Full derivation and claim boundaries](cspp_v024/PROOF.md)
- [Prepared next work package](cspp_v024/NEXT_WORK_PACKAGE.md)
- [Protocol](cspp_v024/PROTOCOL.json), [status](cspp_v024/STATUS.json),
  [checks](cspp_v024/results/CHECKS.json), [replay](cspp_v024/REPLAY.json)
- [128-bit decision](cspp_v024/results/DECISION_128.json) and
  [192-bit decision](cspp_v024/results/DECISION_192.json)

## Scientific decision

The near-light-cone enclosure accounts for more than 99.9999% of the
existing certified budget. These are upper proof bounds, not measured
physical errors. Even hypothetical removal of the entire infinite-tail
certificate leaves the unchanged finite bound about 477–549 times above
0.001. This bookkeeping is not a positive lower bound on the actual error.

A new uniform active-count argument gives unconditional L1 bounds under
the ideal Poisson law for the prescribed full KG-history diagnostic:
3.577614 × 10^11 (W0) and 3.936052 × 10^11 (W1), rounded upward, for
the absolute exterior-response difference. It establishes integrability,
not accuracy, covariance prediction, density-uniform stability or sampler
qualification. Exact counterexamples document why L1 cannot supply these
missing conclusions.

The inherited v0.15 Gaussian witness still excludes domain-only repair of
the unchanged fixed cell: its relative mean bias exceeds 0.417028051007
for every real H >= 4. This is a necessary-control failure for that cell,
kernel and domain family, not a rejection of every scalar operator.

All six v0.14 method certificates remain required. The local H1 and
nonlocal PU-H1 candidates remain ineligible for a confirmatory run.
The full KG-history diagnostic is a distinct map and does not silently
replace either frozen candidate. No random calls, new clouds, statistical
rules or physical parameters were introduced.

## Reproduction

From the repository root, with Python 3.12 and python-flint 0.8.0:

```sh
python3 -m pip install python-flint==0.8.0
python3 -B research/cspp/global_gate_reassessment_v0_24/publication_check.py --replay
```

The publication check verifies the original PDF, ZIP, all 58 extracted
package files, 57 manifest hashes and the frozen scientific scope. The
isolated replay reproduces all four numerical result files byte for byte.
It checks 34 source files, 16 global decompositions, 258 inherited H-cover
nodes, 12 independent positive Poisson sums, 60 rational moment identities
and two paired covariance-sign controls. Earlier Gaussian quadratures are
not claimed as newly recomputed. No independent scientific peer review or
proof-assistant verification has been performed.

## Publication record

Research basis: Main after [PR #155](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/155),
commit `0edb8e02aa3dbf5a1b827d7c9aa82385e056e817`.
Both delivered artifacts and all original package files are preserved
byte for byte. Their internal publication status describes the creation
time before this GitHub publication; [PUBLICATION.json](PUBLICATION.json)
records the subsequent publication packaging. Historical source and result
files are unchanged. Date: 29 October 2026.
