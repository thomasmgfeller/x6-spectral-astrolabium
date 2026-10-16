# Repair record: 0.2.0

16 October 2026. This is an intentionally incompatible scientific repair of the four supplied files. The original audit and original files remain historical evidence; previous numerical results are not silently relabelled as corrected results.

| Original problem | Repair and resulting interpretation |
|---|---|
| Relation insertion could omit consequences across both ancestors and descendants | Complete ancestor × descendant update with cycle rejection; exhaustive independent small-order checks |
| Alleged BDG result was primarily N−0.4M | Replaced with the documented 4D interval bracket N−N₀+9N₁−16N₂+8N₃; omitted physical prefactors explicitly stated |
| Arbitrary exponential presented as KR suppression | Removed; the new three-layer ensemble is a reference sampler and makes no suppression claim |
| Spectral asymmetry identically zero | Removed as a diagnostic; causal orientation loss is documented |
| Adjacency width called algebraic connectivity | Retained under its correct name; added the second Laplacian eigenvalue as algebraic connectivity |
| Persistence reduced to sqrt(2M/N) | Renamed adjacency spectral standard deviation and its dependence on N,M made explicit |
| Spectral entropy invited a quantum interpretation | Defined explicitly from H² weights; undefined at M=0; no entanglement claim |
| Browser reported mock values, Gaussian-shaped plots and unconditional validation | Actual generators, interval counts, signed eigenvalue plots, import checks, errors, computed tables and reference tests |
| Global RNG behaviour and insufficient recorded provenance | Local portable PCG32, recorded seeds, matrices, hashes, generator conventions and coordinates |
| Supplied 15-run data could not be reproduced from the stated default convention | Replaced by 240 fresh pilot runs in 30 groups with eight seeded replicates, full raw records and uncertainty summaries |
| Quadratic matter model could be indefinite | Replaced by a distinct classical Gaussian reference Q=m²I+gL, m>0, g≥0; no claim to preserve the old physical model |
| Growth counter could be treated as physical time | Explicit construction parameter; separate assumed two-qubit relational clock with normalized conditioning and stated periodic limitations |
| Order-dependent closure defect could resemble noncommutative physics | Correct fixed-edge insertions commute when jointly acyclic; a separate classical reset example demonstrates why noncommutativity alone is insufficient |
| Thinning could be presented as established RG dynamics | Seeded Bernoulli thinning with induced orders and original indices; no coupling flow or fixed-point claim |
| Broad theoretical validation language | Replaced with bounded implementation evidence and a machine-readable claims register |

## Migration

- JSON schemas change to `RAX-CQG-EXPERIMENT-0.2` and `RAX-CQG-SWEEP-0.2`. Old records are rejected rather than interpreted using different definitions.
- `RAX_CQG_SimulationEngine` remains as an entry point but returns the new schema.
- `BDGAction.compute` now returns the documented interval bracket. Its old numerical meaning and fitted coefficient are removed.
- The old KR proxy and old matter-model API are removed. Use `ClassicalGraphField` only when that explicit classical model is appropriate.
- `CausalSet.R` returns a copy. Use `add_relation`, `from_edges` or `from_matrix` for checked construction.
- Python accepts N≤512; the browser accepts N≤96. Reference checks include empty and singleton orders even though the interactive size control starts at four.
- The exact equations behind inaccessible Gmail image links have not been checked. The new clock is labelled as an independently specified reference, not a recovered version of those equations.

## Verification and remaining limits

See `VALIDATION.json` and `evidence/` for the recorded release run. Independent finite checks are evidence about those implementations and cases. They are not a proof for all inputs, a browser rendering review, a quantum-gravity result or peer review.

Further physical claims require a defined model and their own proofs or evidence. In particular, QSG consistency, covariance of a proposed quantum dynamics, Bell causality, KR suppression, emergence of quantum mechanics, continuum limits and observational predictions remain outside this implementation.
