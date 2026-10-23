# Eigenzeit: all 60 frozen paired directions excluded continuously

**The last 38 HOLD cells are now excluded. All 60 frozen signed paired rays
are covered continuously for step magnitudes [0,0.1], with no unresolved cell.**
The new certificates preserve the dependence of overlapping observed counts.
They close signed ray 3 (nodes 15/5, boosted y) and signed ray 44 (nodes 15/17,
negative boosted x), adding two complete-ray exclusions to PR114's 58.

On these 30 one-dimensional lines from the fixed reference, no point
simultaneously preserves the selected-node order, has symmetric operator-weight
gap >20%, and has full conditional labelled count/overlap-law TV <=0.25.
This bounded family exclusion does not establish general operator stability.

## New result

| Signed ray | Previously unresolved step magnitude | Cells | Uniform full-law TV lower bound |
|---:|---|---:|---:|
| 3 | [327/5120, 93/1280] | 31 | 0.54818812388209538992 |
| 44 | [5/128, 107/2560] | 7 | 0.28571661749849482568 |

These lower bounds concern the newly excluded cells, not the full motion
domain or h=0. The complete cover also uses inherited order and weight-gap
exclusions where a statistical separation need not hold.

The single frozen pass evaluated 38 anchor events; the first proposed anchor
succeeded for every cell, so none needed the permitted second attempt. Four
reference-law enclosures were reused. Every law enclosure covers its entire
unknown common-intensity range with 64 closed rational slices. No displacement
subdivision, slice refinement, extra anchors or threshold retuning followed
evaluation. The complete inherited and new cover contains 3,375 terminal cells
on 30 lines, representing all 60 signed rays.

For line 3 the successful statistic is

    D=N(I(3,15))-N(I(3,5)),  D<=k,  k in {39,40}.

For line 45's negative half (signed ray 44), it is

    D=N(I(15,1))-N(I(17,1)),  D<=k,  k in {201,202}.

Each cell uses one fixed integer threshold, selected before its event
probability is evaluated by the frozen geometric proposal rule. The exact
cell/threshold assignments are archived in `certificates.json.gz`.

## Why overlap cancellation works here

For two overlapping intervals A,B, the observed difference satisfies

    N(A)-N(B) = N(A minus B)-N(B minus A).

Only the two exclusive Poisson atoms are independent. Their means are a-c
and b-c, where c is the common intensity. Although the shared count cancels,
the difference law still depends on c; replacing c by a midpoint or treating
the original counts as independent would be unjustified.

The inherited virtual-tip geometry bounds c from below, and the smaller
interval intensity bounds it from above. Within every overlap slice, a
rectangle encloses both exclusive means. Monotonicity in these two independent
means gives exact event bounds. Taking the minimum lower and maximum upper
bounds over ALL slices yields a uniform bound without assuming monotonicity
in c. A reference/moved event-probability separation lower-bounds the full
observed law's TV. See [THEOREM.md](THEOREM.md).

Geometry and probability certificates use exact fractions, directed 80-digit
integer PMF recurrences, and explicit infinite-tail bounds. Budget failures
would retain [0,1] and HOLD; none occurred in this pass. The probability proof
uses whole-cell enclosures, not sampled displacement values.

## Reproduction and independent validation

From the repository root with Python 3.12 and the existing
`finite_poisson_bounds/requirements.txt` dependencies:

```sh
python3 -B research/lorentz_local_dalembert/overlap_tails/ot_run.py --verify
python3 -B research/lorentz_local_dalembert/overlap_tails/ot_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/overlap_tails/SHA256SUMS
python3 tests/python/verify_manifest.py
```

`audit.json` reports PASS: 5,376 independent 110-digit direct PMF checks of
every distinct probability endpoint, 2,688 exclusive-rate rectangle checks,
40 virtual-subset checks, 240 direct reconstructed-geometry checks and complete
reconstruction of all 30 line covers. Controls reject missing overlap slices and missing parameter cells;
small-mean factorial-series and zero-rate cases test the probability engine;
an identical-interval example rejects independence of overlapping counts and
a midpoint-only overlap substitution. A forced rate-budget failure must HOLD.
Decimal evaluations are implementation checks; the rigorous certificates come
from directed arithmetic and proved inequalities.

The scientific contract, algorithm, proof and input evidence were internally
hashed before the first new event evaluation. Prior PR114 results and
geometry-only statistics were known; this was not external preregistration.
Source parent PR114 is `e65bfac83e51f0b8e0ce60d480bf5d6dc23fbf69`, tree
`34a1531af84dda67a8592be0784c5be9555a1517`. All five parent workflow runs passed.
Predecessor evidence files remain unchanged. A dedicated CI job replays this
package and its audit.

## What remains open

The result covers only the declared velocity ratios, axes, parameter range
and fixed reference. It does not cover arbitrary two-support displacement
ratios or directions, three-or-more-support motions, other references, the
full A-selection/B-graph likelihood, or physical continuum accuracy.

The next bounded extension is a two-parameter paired domain allowing the two
support displacements to vary independently, beginning with nodes 15/17 in
boosted x. The current difference-law construction can be applied to exact
rectangle bounds there, but a new contract must freeze that domain, geometric
and operator bounds, resolution budget and stopping rules before evaluation.
No outcome for that larger domain is claimed here.
