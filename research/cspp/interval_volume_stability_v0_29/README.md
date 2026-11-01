# CSPP v0.29 - interval-volume bounds for causal propagation

This publication preserves the completed v0.29 development package byte for
byte. The positive path majorant now uses the Poisson mean of the absolute
smoothed interval weight, retaining its dependence on causal interval volume.
Binomial thinning covers every higher density at fixed q. A single-chain
Mecke calculation handles inserted points and the disjoint adjacent open
intervals explicitly; a positive Volterra bound includes prescribed history.

For theta=21, q=3/(16*pi), rho>=3/pi, T=9/4, H=4, delta=0.01 and a fixed
normalized detector Q=1, the sufficient combined amplification upper bound
falls from about 82,031 to **at most 34,820**. The certified improvement is
at least a factor of 2.35. With exact history, the active-error upper bound
falls from about 584.887 to at most 321.952.

**Complete causal intervals are required**, including every interval used
for a passive probe. Causal diamonds such as the project domain Omega5
satisfy this additional condition. Arbitrarily clipped intervals retain
the v0.28 constant-envelope bound. The numerical comparison concerns the
common domain class and unchanged physical and history budgets.

These are smaller **sufficient upper bounds**, not measured error reductions.
Lower endpoints enclose the mathematical majorant, not actual response or
error lower bounds. Different paths may overlap: their covariance and signed
cancellation remain open. The theta=21 accuracy exclusion from v0.25 is
unchanged. **METHOD and G1 remain HOLD. No new random clouds were generated.**

## Published evidence

- [Report (German PDF)](Intervallvolumen_Pfadstabilitaet_v0_29.pdf)
- [Original reproducibility package (ZIP)](CSPP_Intervallvolumen_Pfadstabilitaet_v0_29_Pruefpaket.zip)
- [Full definitions, proofs and quantifiers](cspp_v029/PROOF.md)
- [Certified bounds and validation results](cspp_v029/results/RESULTS.json)
- [Scientific status](cspp_v029/STATUS.json) and [source provenance](cspp_v029/evidence/SOURCES.json)
- [Development replay receipt](cspp_v029/REPLAY.json) and [publication metadata](PUBLICATION.json)
- [CSPP v0.28](../smoothed_weight_stability_v0_28/README.md)
- [Interactive Causal Stability Lab](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/causal-stability/)

## Reproduce

Python 3.12 and its standard library suffice. The mathematical replay uses
only integers and rational numbers, including outward rounding and bounds
on infinite tails. No network access or random ensemble is needed:

```sh
python3 -O -B research/cspp/interval_volume_stability_v0_29/publication_check.py
python3 -O -B research/cspp/interval_volume_stability_v0_29/publication_check.py --replay
```

The full replay takes several minutes. Publication verification compares all
18 extracted files with the original ZIP, checks 17 checksums, both report
copies, headline rounding, counts and scientific scope. An isolated
`-I -O -B` replay requires byte-identical results and unchanged package files.
Explicit exceptions keep validation active with assertions disabled.

The package includes 407 finite orders and 2164 chains (457 with multiple
edges), 200 exact conditional binomial/Jensen checks, ten independent rational
Poisson evaluations, two analytic v0.28 regressions, 202 radial-shell/cone
checks, eight negative controls and six Git-blob/SHA256 source checks.
Two space/time meshes and two integer precisions give six certified runs;
each run provides an enclosure independently of an observed convergence trend.

The original package's statements that GitHub publication had not occurred
describe the development step. They are preserved verbatim; this wrapper
documents the subsequent repository publication. Finite checks are not
proof-assistant verification, external expert review or a priority claim.

## Remaining research

Derive a two-path Mecke/Poisson formula including overlap volumes, shared
vertices and deterministic insertion counts before claiming second-moment
control or signed cancellation. The original KG error budget, long-time
stability, infinite history, a growing global spatial maximum and the
separate degree-five accuracy task remain open. Publication promotes no gate.
