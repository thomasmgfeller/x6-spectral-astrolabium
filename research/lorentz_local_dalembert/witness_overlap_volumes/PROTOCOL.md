# Fixed witness-overlap audit

SPDX-License-Identifier: Apache-2.0

Check both exact PR88 coordinate witnesses on all 74 selected interval means
and all 2701 unordered interval pairs (intersection plus two exclusive parts).
Keep PR90 c=12 marginal and c=20 overlap confidence bands unchanged. Simplify
intersections by exact causal dominance. Empty intersections and single
Alexandrov diamonds use rational/analytic volume enclosures; all other cases
use randomized cell integration, explicitly probabilistic rather than a
deterministic quadrature guarantee. No geometry is re-fitted or selected.

Use exact rational Lorentz boost (gamma=17/8, sinh=15/8), grid unit 2^-16,
and the spatial ellipse bounding box of the containing diamond I(3,0).
Uniform independent grid-cell draws are the mathematical integration model;
the reproducible implementation uses the declared PCG64 seeds and chunk size.
Classify whole cells inward/outward using checked int64 interval arithmetic.
Count intersections and exclusive parts directly, not by subtracting uncertain
numerical integrals. Apply the proved binomial MGF/Poisson-Chernoff envelope
with c=24 to each inner/outer count. Include every possible refinement stage
and analytic marginal control in the numerical union budget.

Fixed stages: 2^20, 2^22, 2^24 cells per geometry. Stop when all unknown
constraints are classified or one excludes the witness. An analytic-control
failure returns integration HOLD. Remaining overlap at the final budget is
UNRESOLVED, never a silent PASS. Preserve all original scientific HOLDs.
Freeze code/input hashes before evaluation of these known posthoc witnesses.
No statistical indistinguishability or minimax-risk inference from compatibility.
