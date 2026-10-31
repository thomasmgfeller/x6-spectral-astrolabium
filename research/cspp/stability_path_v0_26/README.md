# CSPP v0.26 - universal stability limit and signed-path criterion

This publication preserves the completed v0.26 development package byte for
byte. A concrete family of finite causal sets proves that no deterministic
l-infinity response bound can cover **all realizations** for any fixed,
nontrivial, realization-independent interval kernel with a nonzero
normalization denominator. The exact response norm is `1 + M |t(r)|`,
where r is the first nonzero interval weight and M counts incomparable
predecessors. The construction is Minkowski-realizable and has positive
Poisson probability in a suitable fixed bounded region at every fixed
positive density. Every nonsingular v0.25 parameter is covered, including
the exceptional zero-first-layer case.

This excludes the strongest all-realization maximum-norm requirement. It
does **not** establish typical Poisson instability, infinite variance,
physical time growth or failure of the specified compact KG detector.
Every individual finite realization still has a finite response. No
scientific priority claim or independent expert review is asserted.

A separate sufficient Schur-complement criterion sums signed internal paths
before taking norms. An exactly solvable synthetic family remains bounded
by 5 at every length despite an original row norm of 3. Its stability
threshold is `|AB+C| < 1`; it is not a qualified GCB or physical operator.
**METHOD and G1 remain HOLD. No new random clouds were generated.**

## Published evidence

- [Report (German PDF)](Stabilitaet_Pfadkriterium_v0_26.pdf)
- [Original reproducibility package (ZIP)](CSPP_Stabilitaet_Pfadkriterium_v0_26_Pruefpaket.zip)
- [Complete definitions and proofs](cspp_v026/PROOF.md)
- [Exact finite checks and rational constants](cspp_v026/results/RESULTS.json)
- [Scientific status](cspp_v026/STATUS.json) and [source provenance](cspp_v026/evidence/SOURCES.json)
- [Publication metadata](PUBLICATION.json)
- [Interactive Causal Stability Lab](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/causal-stability/)

## Reproduce

Python 3.12 and its standard library suffice; no numerical dependencies,
network queries or Monte Carlo runs are required:

```sh
python3 -O -B research/cspp/stability_path_v0_26/publication_check.py
python3 -B research/cspp/stability_path_v0_26/publication_check.py --replay
```

The first command checks 15 extracted files against the original ZIP,
14 package checksums, both report copies and the scientific status. It uses
explicit exceptions and remains effective with Python assertions disabled.
The second command runs the original assertions in a fresh isolated
interpreter (`-I -B`, without `-O`) on a temporary copy, comparing results
byte for byte and verifying that no package bytes changed.

The replay covers 144 rational fan cases, 30 rational cell cases, four
negative controls, three overlapping rational alpha enclosures and three
Git-blob/SHA256 source checks. Dense Gauss-Jordan inversion and causal forward
recursion are compared. Finite checks supplement the written analytic
proofs; they are not proof-assistant verification of the universal theorem.

The original PDF, proof and status say publication was not performed in the
development step. Those historical statements are deliberately preserved;
this directory and `PUBLICATION.json` record the later repository publication.

## Remaining research

A positive stability result for a physically qualified GCB family remains
open. The next task must fix the norm, physical time window and quantifiers:
a geometrically restricted class or a high-probability bound with an explicit
failure probability. History and detector couplings need their own uniform
control. The degree-five accuracy work package from v0.25 remains separate
and unperformed; publication does not promote any scientific gate.
