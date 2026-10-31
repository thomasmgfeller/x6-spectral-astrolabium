# Causal Stability Lab v0.1

**[Open the public lab](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/causal-stability/)** · [Deutsche Landingpage](https://thomasmgfeller.github.io/x6-spectral-astrolabium/de/#causal-stability) · [Source](../../../../app/causal-stability/)

An interactive instrument for causal-path reinforcement, cancellation, finite
history sensitivity and active error amplification. The German interface runs
locally in the browser without sign-in, dependencies, tracking or a backend.
The DE and EN landing pages provide a prominent launch button and a preview.

## Follow-up: CSPP v0.28 smoothed-weight stability

[Read the report, full proof and reproducibility package](../../../../research/cspp/smoothed_weight_stability_v0_28/README.md).
Exact global bounds on the binomial-smoothed interval weights replace the
coarse coefficient envelope from v0.27. An analytic tail certificate covers
all interval counts, and binomial composition extends the bound to every
higher density. At fixed q and rho >= 3/pi, the theta=21 combined 99%
finite-time/history upper bound improves by about 2,749. The cancellation
captured here is inside each smoothed weight; cancellation between distinct
propagation paths remains open. This is not measured error reduction, and
the v0.25 accuracy rejection remains unchanged. METHOD and G1 remain HOLD.
The browser engine and its numerical baseline are unchanged.

## Follow-up: CSPP v0.27 finite-time stability

[Read the report, full proof and reproducibility package](../../../../research/cspp/finite_time_stability_v0_27/README.md).
For Poisson causal sets in 1+3 Minkowski space, a uniform entry envelope
`|K_ij| <= kappa/rho` gives density-independent expectation and explicit
failure-probability bounds for a fixed passive probe or deterministic
detector on a fixed finite time window. A separate estimate treats prescribed
finite history. The binomial-smoothed interval family satisfies the entry
envelope at fixed q, rho >= q and nonzero diagonal denominator.
These bounds remain too large to certify the original error budget.
They do not establish long-time stability, infinite-history control or
a spatial global-maximum bound. METHOD and G1 remain HOLD.
The browser engine and its numerical baseline are unchanged.

## Follow-up: CSPP v0.26 stability result

[Read the report, full proof and reproducibility package](../../../../research/cspp/stability_path_v0_26/README.md).
A Minkowski-realizable fan family excludes a deterministic l-infinity bound
over all realizations for any fixed nontrivial interval kernel. The exact
response norm is `1 + M |t(r)|`; every nonsingular v0.25 parameter is covered.
A separate Schur-complement criterion retains signed-path cancellation, with
a synthetic control bounded by 5 at every length. Typical Poisson stability,
the qualified physical propagator and the fixed KG detector remain open.
The current browser models and their published numerical baseline are unchanged.

## First experiment

Choose **Gegenläufige Pfade** and set **Pfad-Asymmetrie** to zero. The passive
probe response vanishes by exact cancellation, while the active error norm can
remain large. Increase the asymmetry to inspect the sensitivity of that
cancellation. No filtering or variance reduction is applied.

## Models and controls

1. **CSPP v0.25:** the published synthetic, totally ordered history-control
   graph, with its fixed q, epsilon, mass and coefficient family. Only theta=21
   and five active nodes reproduce the published finite-control fixture.
2. **Contractive chain:** an analytic family with a uniform inverse-norm bound
   for fixed 0 <= gamma < 1.
3. **Amplifying chain:** identical zero eigenvalues, but inverse norm growing
   linearly or exponentially with graph length.
4. **Opposing paths:** cancellation at one probe, with separate internal error
   amplification and a coefficient-asymmetry control.

Inspect nodes, filter displayed edges, step through the causal calculation,
compare graph lengths, and export the complete experiment as JSON or the
finite length curve as CSV. Display filters never change the calculation.

## Reproduce

From the repository root, with Node.js 24:

```sh
node --test tests/causal-stability/engine.test.mjs
node --check app/causal-stability/app.mjs
node --check app/causal-stability/engine.mjs
```

The nine tests check the original 192-bit certificate's Git blob hash and
values, independent dense inversion, explicit path enumeration, analytic chain
formulas, cancellation, worst-case attainment, relabeling invariance, invalid
graphs and export scope. The existing CSPP certificate is reused in place;
its research bytes are unchanged. GitHub Actions runs these checks and tests
the landing-page-to-lab navigation in a browser.

For a local preview, serve the repository root over HTTP and open
`app/causal-stability/`. Do not open ES modules through a `file:` URL.

## Scientific boundary

Read [MATHEMATICS.md](MATHEMATICS.md) for the finite identities, exact norms
and conditional uniform contraction theorem, and [VALIDATION.md](VALIDATION.md)
for the original instrument checks.

Browser arithmetic is Float64 and does not produce new interval certificates.
Layout distances have no metric meaning. Playback is evaluation order, not
physical time. Graph length is not density. Amplitudes are not independent
variances or quantum probabilities.

**METHOD = HOLD; G1 = HOLD.** The v0.27 follow-up proves a scoped local
density-uniform finite-time bound. Practical error qualification, long-time
stability, infinite-past propagation and the original compact KG detector
task remain unresolved.
No new random clouds or fermionic dynamics are generated. The published
fixed-q degree-four mean-screen exclusion is preserved.

Scientific baseline:
[CSPP v0.25 at 13d12544fba9ac8fd54549eacc4a1ec19a2d6b51](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/13d12544fba9ac8fd54549eacc4a1ec19a2d6b51/research/cspp/scalar_candidate_v0_25).
The browser source was transferred from the first Site version, commit
`9803fce22316db16e0f461b6e1c310fbee8376ef`, with public navigation added.
The numerical engine is unchanged.

Original project contributions use Apache-2.0; see the repository's
[licensing scope](../../../../LICENSE_SCOPE.md).
