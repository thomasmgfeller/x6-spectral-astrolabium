# CSPP v0.28 - sharper stability bounds from smoothed interval weights

This publication preserves the completed v0.28 development package byte for
byte. Exact global bounds on the actual binomial-smoothed interval weights
replace the coarse maximum-coefficient envelope used in v0.27. A finite
rational calculation plus an analytic monotone tail controls every integer
interval count. Binomial composition extends each certificate to all higher
densities at fixed q.

For theta=21, fixed q=3/(16*pi), rho>=3/pi, T=9/4, prescribed history
duration H=4 and failure probability delta=0.01, the sufficient combined
amplification upper bound for equally bounded active and history errors
falls from about 225.5 million to 82,030, a factor of about 2,749. With exact
history, the active-error bound falls from about 89,858 to 585.

This is a **smaller sufficient upper bound**, not measured error reduction.
The new smaller envelope is not asserted below its specified density floor.
The cancellation retained here is between signed layer contributions inside
each smoothed weight; cancellation between distinct propagation paths
remains open. The theta=21 accuracy exclusion from v0.25 is unchanged.
**METHOD and G1 remain HOLD. No new random clouds were generated.**

The original compact KG error budget is not certified. Long-time stability,
infinite history, correlated-path covariance and global spatial-maximum
control are not established by this result. The c0 comparison is a limit
of the scalar-entry-envelope method, not a physical lower bound on errors.

## Published evidence

- [Report (German PDF)](Geglaettete_Intervallgewichte_Stabilitaetsbudget_v0_28.pdf)
- [Original reproducibility package (ZIP)](CSPP_Geglaettete_Intervallgewichte_v0_28_Pruefpaket.zip)
- [Complete definitions, proofs and quantifiers](cspp_v028/PROOF.md)
- [Exact certificates and rational budget intervals](cspp_v028/results/RESULTS.json)
- [Scientific status](cspp_v028/STATUS.json) and [source provenance](cspp_v028/evidence/SOURCES.json)
- [Publication metadata](PUBLICATION.json)
- [CSPP v0.27](../finite_time_stability_v0_27/README.md)
- [Interactive Causal Stability Lab](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/causal-stability/)

## Reproduce

Python 3.12 and its standard library suffice. No network queries, random
seeds, third-party numerical dependencies or new cloud production:

```sh
python3 -O -B research/cspp/smoothed_weight_stability_v0_28/publication_check.py
python3 -O -B research/cspp/smoothed_weight_stability_v0_28/publication_check.py --replay
```

Publication verification checks all 17 extracted files against the original
ZIP, 16 checksums, both report copies, recorded counts and scientific scope.
The isolated `-I -O -B` replay compares results byte for byte and requires
every package file to remain unchanged. Explicit exceptions keep checks
effective with assertions disabled.

Validation includes six global weight certificates, 1782 integer weights
evaluated three ways, 648 exact binomial compositions, 2442 operator cases
and 2442 frozen-history cases, six negative controls, ten budget rows in
three precisions and five Git-blob/SHA256 source checks. Archived v0.27
intervals are reproduced and explicitly identified common routines are
reused unchanged. Finite graph checks use a rational prefactor 1/7; the
physical project constants are enclosed separately.

Finite checks supplement the written proofs. They are not proof-assistant
verification, external expert review or a scientific priority claim.
The original package's statements that publication was not performed refer
to the development step. They remain unchanged; this wrapper records the
subsequent repository publication.

## Remaining research

Replace the constant entry envelope with interval-volume-dependent path
bounds while retaining the fixed norm, physical time window, failure budget,
prescribed history and detector. Single-chain count identities must not be
mistaken for covariance control of overlapping path pairs. The separate
degree-five accuracy task remains open; publication promotes no gate.
