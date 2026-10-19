# Glossary: terms without detours

These definitions are starting points. Calculations always use the precise definition in the relevant module.

[Deutsch](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/glossary.md) · [Wiki overview](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/)

Source snapshot: 2026-10-19 · `c58cc26adb2b4a646e3940e417351040b5dc9ff0`

## Key terms

| Term | Meaning |
| --- | --- |
| Signal | A sequence of values, usually over time. |
| Spectrum | A representation of frequency components or, for a matrix, its eigenvalues. Context matters. |
| Fourier transform / FFT | Decomposition into oscillating components; FFT is a fast method of calculating it. |
| Phase | The position of an oscillating component within its cycle. |
| Noise | Additional fluctuations; which components are unwanted depends on the task. |
| Graph | Nodes and their connections. |
| Laplacian matrix | A matrix built from node degrees and connections; a precisely defined graph operator here. |
| Eigenvalue / spectral gap | A characteristic value of an operator / a separation between specified eigenvalues. The intended gap must be defined. |
| Causal order / poset | A set with a directed, transitive ordering; not every pair must be comparable. |
| Hasse diagram | A drawing of the immediate relations of a finite order. |
| Isomorphism | Identical structure after a one-to-one renaming of nodes. |
| Invariant / fingerprint | A feature unchanged by the allowed relabelling; it need not uniquely identify a structure. |
| Interval count K | In the proper-time experiment: the number of events strictly between two marked events. |
| Height H | The length of a longest chain; counted in nodes here. |
| Relation density | The fraction of comparable pairs under the specified counting convention. |
| Minkowski model | A flat relativistic spacetime model, without curvature. |
| 1+1 dimensions | One time dimension and one spatial dimension. |
| Proper time | A measure of time along a timelike connection; relative to an outer scale in this experiment. |
| Seed | A starting specification for a reproducible random sequence. |
| Baseline | A specified comparison method. |
| Control / counterexample | A test case for a particular error risk / a case refuting a general claim. |
| Holdout | Data not used to fit or select a method. |
| Bootstrap | Repeated sampling from existing data to estimate a particular uncertainty. |
| RMSE | Root mean square error. |
| Commit | A precisely identified version of a Git project. |
| Pull request / PR | A proposal to incorporate changes into another development branch. |
| CI | Automatically executed integration and checking workflows. |
| Replay / replication | Recomputing a result / repeating a finding; scope and independence must be stated. |
| Provenance / hash | Documented origin / a checksum of bytes. |
| Continuum limit | A mathematically controlled passage from discrete objects to a continuous limiting model. |

## One word can have several meanings

A graph spectrum is not the same as the frequency spectrum of a measured vibration. Likewise, a spectral gap is not automatically a physical energy gap. Always check which operator, unit and model are involved.

- [Mathematical contract](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/SCIENTIFIC_SCOPE.md)
- [Signal Lab methods](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/SIGNAL_LAB_METHODS.md)
