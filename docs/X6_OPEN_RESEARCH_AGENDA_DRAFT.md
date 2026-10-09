# X6 Spectral Astrolabium: Verified Finite-Graph Spectral Methods and an Open Research Agenda

**Status:** Working paper / research-program orientation, version 0.1 (2026-10-09).
**Software:** X6 v4.2 RC; community audit kit v4.3.
**Attribution:** Maintainer-led, AI-assisted development; formal author list and citation metadata pending confirmation.
**License:** Not yet granted. Apache-2.0 intended for code, subject to provenance review.
**Scope:** Mathematical research questions and reproducibility; not a claim of experimentally validated fundamental physics.

## Abstract

X6 provides an experimental browser interface for signal exploration, a
model-dependent map from samples to finite weighted graphs, and exact
rational certificates for strict lower bounds on spectral gaps of finite
undirected graph Laplacians. The accompanying Python, Julia and Chromium
tests exercise selected reference cases and application behavior.
This paper identifies research directions that can be falsified using
explicit hypotheses, independent implementations, reproducible datasets
and acceptance criteria. We distinguish exact finite-dimensional
certificates from numerical approximations, modeling assumptions and
unproved continuum or physical interpretations.

## 1. Established mathematical baseline

Let `G=(V,E,w)` be a finite connected undirected graph with `n>=2`
and strictly positive rational edge weights. Its combinatorial Laplacian
`L=D-W` is real symmetric with eigenvalues
`0=lambda_1 < lambda_2 <= ... <= lambda_n`.
Let `J=11^T` and define, for rational `b`,

`M(b)=L + ((b+1)/n) J - b I.`

On the constant vector, `M(b)` has eigenvalue `1`; on the orthogonal
complement its eigenvalues are `lambda_i-b` for `i>=2`.
Consequently

`M(b) positive definite  <=>  b < lambda_2(L).`

Positive definiteness can be certified using exact rational
`LDL^T`/Schur-complement arithmetic, provided matrix symmetry and
input assumptions are checked. For any nonzero `x` orthogonal to
`1`, the Rayleigh quotient `x^T L x / x^T x` is an upper bound on
`lambda_2`. Choosing `x=e_i-e_j` gives
`(d_i+d_j+2w_ij)/2` (with `w_ij=0` if no edge).

This certificate applies to the *specified rational graph*, not to
unrounded real-valued signals. A disconnected graph has `lambda_2=0`;
component-wise positive gaps are not a positive global gap.

## 2. Evidence and limits

- GitHub Actions run 37992910863: Python, Julia and Chromium jobs all
  completed successfully for the tested commit.
- Python: rational reference fixtures and manifest/static tests.
- Julia: four floating-point spectral reference fixtures, not exact proofs.
- Chromium: local qualification smoke test, not complete functionality.
- The browser's `allPassed` report is not independent physical or
  mathematical certification.
- A future release requires explicit versioned evidence and a clear
  distinction between PASS, FAIL, NOT_EXECUTED and PENDING.
- Rights/provenance and security review remain open.

## 3. Research questions and falsifiable protocols

### RQ1 — Certified spectral enclosures under quantization

**Question.** Given real or interval-valued input weights and a rational
rounded graph, can one compute a *rigorous enclosure* for the unrounded
graph's `lambda_2` using explicit rounding-error bounds?

**Hypothesis to test.** If `L` and `Lhat` are symmetric Laplacians on
the same labeled vertices, Weyl's inequality yields
`|lambda_2(L)-lambda_2(Lhat)| <= ||L-Lhat||_2`.
If edgewise uncertainty is bounded, construct an explicit, auditable
operator-norm bound `epsilon` and combine it with rational certificates
for `Lhat`.

**Falsification / acceptance.** Generate graphs with exact rational
perturbations and independent high-precision eigenvalue references;
reject any proposed enclosure violated by a sample. Include zero
weights, near-disconnection, ties and extreme scales. A theorem-level
claim requires proof of the uncertainty bound, not only simulations.

### RQ2 — Certified gap stability under graph edits

**Question.** How do edge additions/removals and bounded weight changes
affect strict rational lower bounds and connectedness?

**Protocol.** Construct controlled edge perturbations and compute
`L'=L+Delta L`; certify lower bounds and compare with independent
spectral calculations. Test whether proposed perturbation budgets
guarantee preserved connectivity and a positive gap.

**Failure criteria.** A predicted positive global gap on a disconnected
perturbed graph, or a violated bound, rejects the claim.

### RQ3 — Numerical-to-exact certificate pipelines

**Question.** Can approximate eigenvalue estimates from Julia/Wolfram
be converted into small, machine-checkable rational gap certificates
without relying on floating-point trust?

**Protocol.** Use numerics only to propose rational candidates `b`;
verify `M(b)>0` independently using exact arithmetic. Record bit
complexity, memory, proof size and verification time as graph size grows.

**Acceptance.** Every published lower-bound claim has a portable
certificate checked by a second implementation; timeouts are
NOT_EXECUTED, never PASS.

### RQ4 — Identifiability of signal-to-graph mappings

**Question.** Which conclusions about the original signal remain
invariant under sampling, normalization, kernel width, topology choice
and rounding in the map from signals to weighted graphs?

**Protocol.** Define the mapping mathematically; test families of
distinct signals producing identical graphs and families of nearby
signals producing significantly different gaps. Report sensitivity
curves and counterexamples.

**Failure criteria.** A claimed signal invariant that changes under a
declared admissible transformation is falsified. A graph property
alone must not be described as a physical property of the signal.

### RQ5 — Scaling and continuum limits

**Question.** Under which precisely stated sampling and geometry
assumptions do appropriately rescaled discrete operators converge to
a chosen continuum operator, and do spectral gaps converge?

**Protocol.** Fix the continuum domain, boundary conditions, graph
construction, normalization and sampling distribution. Establish
operator or form convergence assumptions separately from Monte Carlo
evidence. Test convergence rates across independent seeds and mesh
densities, with finite-size confidence intervals.

**Failure criteria.** Lack of stabilization, inconsistent scaling or
counterexamples to compactness assumptions blocks any continuum claim.

### RQ6 — Directed and causal structures (separate research track)

**Question.** Can causal-order data be associated with mathematically
well-defined operators whose spectra carry stable geometric
information, without misusing undirected graph-Laplacian certificates?

**Protocol.** Start with explicit finite posets/causal sets, operator
definitions, invariance tests and small exact counterexamples. Develop
a Lorentzian convergence notion and prove any relationship to
continuum geometry separately. Do not apply the symmetric
`M(b)` criterion to nonsymmetric directed operators without new
hypotheses and proof.

**Failure criteria.** Violated causal invariance, operator ambiguity
or unjustified identification with Lorentzian geometry rejects the
proposed interpretation.

### RQ7 — Reproducible and adversarial verification

**Question.** What is the smallest independent verification stack
capable of detecting incorrect certificates, malformed input,
inconsistent exports and misleading success states?

**Protocol.** Differential testing across Python, Julia and browser;
property-based and mutation tests; malformed JSON and certificate
tampering; browser engines, accessibility and translation audits.
Record versioned inputs, SHA-256 hashes, stdout/stderr and failures.

**Acceptance.** Intentional mutations are detected, expected failures
remain failures, and a missing backend never appears as PASS.

## 4. Proposed research-program work packages

| Package | Deliverable | Exit gate |
| --- | --- | --- |
| WP1: Exact certificates | Standalone rational verifier + corpus | All reference and adversarial certificates checked independently |
| WP2: Perturbation and rounding | Proved interval bounds + benchmarks | No enclosure violations; mathematical assumptions published |
| WP3: Mapping identifiability | Sensitivity atlas and counterexamples | Reproducible negative and positive cases |
| WP4: Continuum scaling | Convergence study with stated assumptions | Scaling and uncertainty documented; no unsupported limit theorem |
| WP5: Causal extension | Separate finite-poset operator specification | Small exact tests and clearly stated open proofs |
| WP6: Open verification | CI, evidence archive, reproducibility guide | External reproducer can rerun and inspect all gates |

## 5. Publication and governance

Release X6 as a clearly labeled **Public Research Preview** with
documented limitations. The public repository can permit reading and
running for inspection where legally permitted, but public visibility
does not itself grant redistribution/modification rights. The intended
Apache-2.0 license remains on hold pending rights clearance.
Do not describe the preview as scientifically certified or as a
stable physics result. Keep separate records for mathematical proofs,
numerical simulations, software tests and physical evidence.

## 6. Open questions for collaborators

Independent researchers are invited to submit counterexamples,
alternative exact verifiers, independent Julia/Wolfram results,
perturbation bounds, rigorous continuum hypotheses and negative
results. Every proposed claim should identify assumptions, a
falsification protocol and a reproducible artifact.

## References to add before formal paper submission

A formal manuscript must include verified citations to the relevant
spectral graph theory, matrix perturbation theory, exact arithmetic,
graph-to-manifold convergence and causal-set literature. This working
draft intentionally avoids invented bibliographic details.
