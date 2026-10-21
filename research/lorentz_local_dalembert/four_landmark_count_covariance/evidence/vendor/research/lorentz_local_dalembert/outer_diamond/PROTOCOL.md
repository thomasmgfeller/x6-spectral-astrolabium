# Nested outer diamonds on fixed inner supports

19 October 2026. Prospective bounded pilot, defined after the retrospective
landmark-availability diagnosis and before the new development/target clouds.
Prior results stay unchanged. This protocol tests the outer-domain intervention,
not a rescue by changing admission or noise thresholds.

## Paired construction

Use flat 2+1 Minkowski diamonds D(T) = {|t| + sqrt(x*x+y*y) < T/2}, with
volume pi*T^3/12. At each density 2048, 8192, 32768 generate a fresh D(1)
cloud by the unchanged sampler. Select and reweight its inner stencil exactly
as in intrinsic_moments. Freeze root, support, temporal probes, weights, tm,
marks and independent event colours. Unavailable stencils remain unavailable.

Add independent homogeneous Poisson processes in D(1.25) minus D(1), then
D(1.5) minus D(1.25). Each shell count is Poisson with mean rho times its
volume; conditional positions are uniform by rejection from the larger
diamond. Position, mark and colour generators use separate SeedSequence
domains, with seed and shell index recorded by the source. The three variants
share the entire inner realization and nested shells. Density never changes.

The original two artificial endpoints are retained as labelled probes if the
fixed stencil uses them. They are excluded from landmark candidates AND from
every interval's interior count and colour count. They are not Poisson events.
No new artificial outer endpoints are inserted. The augmented causal relation
still permits interval queries to the probes. Count bitsets contain only
physical sprinkled events. This distinction matters once old endpoints lie
inside the enlarged region. At T=1 it reproduces the old inference exactly.

All inner-to-inner intervals stay identical by causal convexity of D(1).
Check this for every root/support pair, including half-colour counts, at
each duration. Record the unchanged inner count obstruction to the guard:
any full count below 16 or half count below 4 is sufficient for rejection
regardless of outer size. It does not bypass inference or remove a cloud.

## Inference, diagnostics and evaluation

Reuse intrinsic_moments/intrinsic.py without modifications: at most 40
mark-ranked candidates per side, minimum interval count 8, raw condition <=1000,
guard condition <=100, all used full intervals >=16, both half counts >=4,
half signatures Lorentzian and Gram/feature deviations <=0.25. Calibration,
mass constraints, fields and fallback rules are inherited unchanged.

Only marked order, density, stencil and colours reach inference. Coordinate
access belongs to simulation and subsequent evaluation. Freeze all three
inferences before evaluating fields. Retain raw, guarded, baseline and true-
coordinate oracle responses. The oracle is diagnostic and cannot pass a gate.

Record capped eligible triples, admissible frames, raw calibration adoption,
guard failures, all weights, independent field errors, metric error, affine
drift, signature and coefficient-noise amplification. Also report one uncapped
full-support threshold-eight chain witness or exhaustive absence per side.
This diagnostic does not replace the 40-candidate inference arm. Triples and
frames alone never count as reconstruction improvement.

## Fixed stages and decision

Publish this contract/protocol before six development clouds (two seeds per
density). Freeze and publish the complete computational sources before target
generation. Development can correct implementation defects; any such change
is documented. Neither thresholds, outer durations nor primary arm are selected
from development outcomes. Use 48 new target clouds, 16 per density, with the
exact seeds in contract.json; no replacement or early success stop.

T=1.5 at rho=32768 is the sole primary arm. T=1.25 describes the response to
outer size and cannot be promoted after inspecting results. Require availability
and guarded adoption >=80% of all 16 primary clouds (at least 13). On the same
available clouds, guarded/baseline RMS ratios for independent fields, metric
error and affine drift must each be <=0.75. Report all fallbacks and missing
cases. These are descriptive pilot gates, not confidence or convergence claims.

Each development/target batch is limited to 1800 wall seconds, 2048 MiB peak
RSS and 35000 augmented points per cloud. Reject before allocation if the
point cap is exceeded; no resampling. At T=1.5 expected physical population
is 3.375 times the inner population. A budget stop yields HOLD, not absence
or a completed scientific comparison. Local replay has the same limits.

Software controls: independent scalar causal-relation and direct interval-count
oracles, exclusion of artificial probes even inside enlarged intervals, nested
shell containment, invariant inner/half counts, sampler moment/count checks,
uncapped-witness agreement with brute force on small posets, inherited algebra
and convex-calibration certificates, mark-preserving relabelling and time
reversal on one enlarged cloud per density. Replay every target, comparing
discrete decisions exactly and invariant numerical outputs with frozen
tolerances; coordinate byte hashes are reported separately.

Only a complete, within-budget, verified test passing every primary gate yields
OUTER_DIAMOND_IMPROVEMENT. Otherwise OUTER_DIAMOND_HOLD. Always HOLD_PHASE3:
intrinsic metric qualification, locality, convergence, 3+1, curvature and
external replication remain open. Failure rejects this bounded single-frame
variant, not all larger domains or all intrinsic causal-set geometry.
