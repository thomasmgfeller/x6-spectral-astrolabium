# CSPP v0.27 - density-uniform local stability on finite time windows

This publication preserves the completed v0.27 development package byte for
byte. For a Poisson causal set in 1+3 Minkowski space and a measurable causal
transfer satisfying `|K_ij| <= kappa/rho`, causal-chain counting gives

```
E G_x <= F(T) = sum_{k>=0} (8*pi*kappa)^k T^(4*k)/(4*k)!
             = [cosh(omega*T)+cos(omega*T)]/2,
P(G_x > 1+[F(T)-1]/delta) <= delta,  omega=(8*pi*kappa)^(1/4).
```

The statement concerns a fixed passive probe or a fixed deterministic
detector measure on a fixed finite physical time window. It is uniform in
density at fixed q and in spatial domain enlargement for that observation.
It is a per-density probability bound, not a joint event over infinitely
many refinements. Binomial-smoothed interval kernels satisfy the envelope
when their coefficients and q are fixed, rho >= q and the diagonal
denominator is nonzero.

A separate bound handles prescribed finite history without propagating its
values again. For the previous theta=21 example and equal bounded input
errors, this improves the conservative combined 99% bound by about 838.
The constants remain too large to certify the original error budget.
Large upper bounds do not establish actual instability. The v0.25 accuracy
exclusion remains unchanged.

This is **not** a long-time stability theorem, an infinite-history bound,
a covariance result or a qualified compact KG error certificate. A separate
argument excludes a uniform global spatial maximum over arbitrarily many
separated probes for the stated nontrivial interval-kernel class. Robust
signed-path cancellation for a physically qualified family remains open.
**METHOD and G1 remain HOLD. No new random clouds were generated.**

## Published evidence

- [Report (German PDF)](Dichteuniforme_Finite_Zeit_Stabilitaet_v0_27.pdf)
- [Original reproducibility package (ZIP)](CSPP_Dichteuniforme_Finite_Zeit_v0_27_Pruefpaket.zip)
- [Complete definitions, proofs and quantifiers](cspp_v027/PROOF.md)
- [Exact finite checks and rational bounds](cspp_v027/results/RESULTS.json)
- [Scientific status](cspp_v027/STATUS.json) and [source provenance](cspp_v027/evidence/SOURCES.json)
- [Publication metadata](PUBLICATION.json)
- [CSPP v0.26](../stability_path_v0_26/README.md)
- [Interactive Causal Stability Lab](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/causal-stability/)

## Reproduce

Python 3.12 and its standard library suffice. No numerical dependencies,
network queries, random seeds or Monte Carlo production are required:

```sh
python3 -O -B research/cspp/finite_time_stability_v0_27/publication_check.py
python3 -O -B research/cspp/finite_time_stability_v0_27/publication_check.py --replay
```

Publication verification checks all 15 extracted files against the original
ZIP, 14 checksums, both report copies, recorded counts and scientific scope.
The isolated `-I -O -B` replay compares results byte for byte and requires
all published evidence to remain unchanged. Checks use explicit exceptions
and remain effective with assertions disabled.

The replay covers all 407 naturally numbered partial orders on 1 to 5
points, 3256 operator cases plus 3256 frozen-history cases, independent
dense inversion, forward recursion and chain enumeration, 72 exact integral
identities, six negative controls, three-precision rational enclosures and
three Git-blob/SHA256 source checks. The finite algebra cases use a rational
prefactor 1/7; the actual project constants are enclosed separately.
Finite checks supplement the written proofs; they are not proof-assistant
verification or independent expert review. No priority claim is made.

The original proof, README and status describe publication as not performed
in the development step. Those historical statements are preserved;
this wrapper records the later repository publication.

## Remaining research

Replace the coarse coefficient envelope with controlled interval and signed
path bounds while retaining the same norm, fixed time window, failure
budget, prescribed history and detector. Correlated path pairs require
their own treatment. The separate degree-five accuracy task remains open;
publication does not promote any scientific gate.
