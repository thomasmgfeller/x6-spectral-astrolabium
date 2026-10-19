# Joint support/count/frame feasibility succeeds at the highest tested density

**JOINT_FEASIBILITY_SUPPORTED in the declared finite 2+1 pilot.**
**HOLD_PHASE3 remains in force.** No differential operator was calibrated or
qualified in this study.

All 48 fresh target clouds completed after the public computational freeze
`8717861f6c2f13371e8bb5a5deaf5597be9d5688`. The three densities have sixteen
clouds each. The outer duration is fixed at 1.5. The original root and marked
chain remain fixed, while both temporal and other support points are adaptive.
The initial protocol and all subsequent development revisions are retained.

## Result on the full denominator

| Density rho | Temporal supports meet counts at some scale | A count-qualified landmark triple | A frame meets signature/condition | A frame also meets half-Gram checks | Joint support selected | Also passes hidden recolouring |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2,048 | 2/16 | 0/16 | 0/16 | 0/16 | 0/16 | 0/16 |
| 8,192 | 16/16 | 16/16 | 7/16 | 3/16 | 1/16 | 1/16 |
| 32,768 | 16/16 | 16/16 | 16/16 | 16/16 | 16/16 | 16/16 |

The predeclared primary requirement was at least 13/16 jointly passing
high-density clouds. The old fixed-support/frame rule passes its guard in
0/16 clouds at every density on these same new realizations. This is a
paired feasibility comparison, not a derivative-accuracy comparison.

Every selected support passes all required full and half interval counts,
the frame condition/signature and both Gram/feature stability checks. Its
linear/quadratic design has numerical rank nine and condition at most 1,000.
The second binary colouring is generated only after selection and cannot
change the selected frame, support or scale. Its checks pass for all seventeen
selected target witnesses. It reuses the physical cloud and is therefore an
auxiliary-thinning audit, not independent physical data or a confidence bound.

## What changed and what did not

The unchanged guards require full interval counts >=16, both half-counts >=4,
frame condition <=100, and normalized Gram/feature discrepancies <=0.25.
Thus the earlier count-eight eligibility rule is also satisfied. No acceptance
threshold was relaxed. An additional per-point feature check and quadratic
design check make the construction more restrictive.

The new search jointly adapts:

- temporal points on the original chain, using count >=2k;
- other inner support points in k <= N(root,b) <2k, k in {16,32,64};
- a single frame whose landmark triple may mix past and future events.

All seventeen retained frames are mixed. This does not establish that mixed
landmarks alone fix the old supports. The combined intervention changes
temporal supports, other supports and the frame search. In the searched
high-density pools there are also five stable all-past triples, though none
is retained. No factorial attribution or exhaustive global search is claimed.

## Conditioning and resolution cost

For the sixteen primary-density witnesses:

| Quantity | Minimum | Median | Maximum |
| --- | ---: | ---: | ---: |
| Frame condition | 17.529 | 20.701 | 24.757 |
| Quadratic-design condition | 22.504 | 47.461 | 106.967 |
| Number of support events | 15 | 22 | 32 |
| Coordinate-only relative Lorentz Gram error | 0.0331 | 0.0631 | 0.1114 |

Every retained witness uses k=16. Its lower count-shell scale
tau_k=(k/(rho*pi/12))^(1/3) is 1.114112 times the old tau_m at the primary
density, and 1.392640 times tau_m for the single middle-density success.
This factor describes the lower count-shell scale only. Actual support extent
and the temporal points change separately; it is not a claim that total
operator resolution degrades by exactly 11.4 percent. Each cloud retains
coordinate-only support-extent diagnostics.

The Lorentz Gram errors compare reconstructed pairwise inner products with
the simulator geometry after all intrinsic selection and audit steps. They
are descriptive diagnostics, not the previous product-identity metric RMS
and not a new metric-accuracy acceptance gate.

## Reproduction and limits

Target execution: **309.875 seconds**, **1,353.414 MiB** peak RSS; limits are
1,800 seconds, 2,048 MiB and 35,000 augmented points. Direct matrix-based
oracles check **3,340 witness intervals** across both colourings. Inherited
sampler/count controls, threshold rejections, an exhaustive small-chain
mixed-triple oracle and marked inference-transport controls also pass.
The complete local repetition passes for all 48 clouds, with exact discrete
decisions and 48/48 matching coordinate hashes: **311.253 seconds**,
**1,351.176 MiB** peak RSS. See [VERIFICATION.json](VERIFICATION.json).

Full source bindings, seeds and raw records are in
[execution.json](results/execution.json); the machine-readable decision is
[summary.json](results/summary.json). Reproduction instructions are in
[README.md](README.md). Local execution and CI are internal project checks,
not person-level external validation.

The success is limited to known-density flat 2+1 Minkowski at the tested
high density, marked finite windows and bounded candidate pools. Sixteen
successes are not a guarantee of the same population rate. Search failures
at lower densities are not impossibility theorems. Selection using counts
and colours changes sampling distributions; no coverage claim follows.

## Next scientific gate

For these new supports, first test whether sign-constrained moment weights
exist with acceptable coefficient mass and noise amplification. Numerical
rank nine alone does not answer that question. Freeze any proposed operator
and evaluate it on independent fields and fresh clouds at the declared
resolution. Retain failures in the denominator. Only a subsequent successful
flat-operator study could support reconsidering phase 3. Locality, convergence,
3+1 and curvature remain open, and the earlier BD-C2 NO_GO remains unchanged.
