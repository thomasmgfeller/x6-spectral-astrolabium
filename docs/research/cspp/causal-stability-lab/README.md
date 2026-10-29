# Causal Stability Lab v0.1

**[Open the public lab](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/causal-stability/)** · [Deutsche Landingpage](https://thomasmgfeller.github.io/x6-spectral-astrolabium/de/#causal-stability) · [Source](../../../../app/causal-stability/)

An interactive instrument for causal-path reinforcement, cancellation, finite
history sensitivity and active error amplification. The German interface runs
locally in the browser without sign-in, dependencies, tracking or a backend.
The DE and EN landing pages provide a prominent launch button and a preview.

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

**METHOD = HOLD; G1 = HOLD.** Density-uniform stability, infinite-past
propagation and the original compact KG detector task remain unresolved.
No new random clouds or fermionic dynamics are generated. The published
fixed-q degree-four mean-screen exclusion is preserved.

Scientific baseline:
[CSPP v0.25 at 13d12544fba9ac8fd54549eacc4a1ec19a2d6b51](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/13d12544fba9ac8fd54549eacc4a1ec19a2d6b51/research/cspp/scalar_candidate_v0_25).
The browser source was transferred from the first Site version, commit
`9803fce22316db16e0f461b6e1c310fbee8376ef`, with public navigation added.
The numerical engine is unchanged.

Original project contributions use Apache-2.0; see the repository's
[licensing scope](../../../../LICENSE_SCOPE.md).
