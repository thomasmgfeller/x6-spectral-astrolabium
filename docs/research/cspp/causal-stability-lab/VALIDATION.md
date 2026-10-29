# Validation — 2026-10-29

- `npm test`: 9 tests passed. The original 192-bit certificate is verified by
  its Git blob hash. The CSPP finite-control diagnostics reproduce its values
  within the stated Float64 comparison tolerances.
- Independent dense inversion, explicit path enumeration, analytic chain
  formulas, exact cancellation, worst-case attainment, relabeling invariance,
  invalid-graph rejection, and export scope are covered by the test suite.
- `node --check dist/app.mjs` and `node --check dist/engine.mjs`: passed.
- Desktop browser: all four presets, node-count extremes, exact path
  cancellation, node selection, edge filters, perturbation pattern, playback,
  stepping, and logarithmic/linear display were exercised.
- A 390 × 844 iframe viewport (375 CSS pixels of content after scrollbar)
  was inspected visually. Document width equalled available content width;
  the causal graph has its own horizontal scroll container.
- Both export controls produced downloadable files. The JSON contains the
  graph, parameters, provenance, finite diagnostics, and HOLD statuses.
  The CSV contains 22 data rows for N = 3 through 24, plus its header.
- Small nonzero values use scientific notation when fixed decimal rounding
  would hide them.

These checks validate this finite-model instrument. They do not certify
density-uniform stability, an infinite-past propagator, or the original
compact KG detector task. No new random clouds were generated.
