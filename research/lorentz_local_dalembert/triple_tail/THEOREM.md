# Uniform event exclusions for the inherited three-support boxes

SPDX-License-Identifier: Apache-2.0

This bounded extension retains the experiment, admissibility conditions,
physical operator, 960 terminal boxes and all exclusions of `../triple_cube`.
The reference is fixed in 2+1 Minkowski space. Nodes 15, 17 and 5 move
independently along boosted x over [-1/10,1/10]^3; the other 18 selected nodes
are fixed. There is no new geometric or operator refinement in this pass.

The strong target is the conjunction of unchanged selected-node order,
inherited admissibility, symmetric physical weight gap >1/5 and full
conditional labelled count/overlap-law total variation <=1/4. This is not
the full A-selection/B-graph likelihood. The completed w=0 square theorem
remains valid; HOLD boxes may contain already excluded points.

## Fixed selection and stopping rule

The source contains 421 HOLD boxes. Remove the 23 which already received a
new marginal or overlap attempt. Process all remaining 398 in numeric
octree-path order. Each receives the first at most two inherited marginal
candidates, ranked by exact separated-mean score, stopping at its first
TV lower bound >1/4. Every remaining input receives exactly one highest-ranked
pair/common-anchor difference event with 64 overlap slices. The overlap
budget is 398, so no remaining input is truncated. No event retuning,
alternative pair search after failure, box splitting or budget extension is
allowed. Precondition and probability-budget failures remain HOLD.

The contract and scientific implementation are internally frozen before new
event evaluation, after source outcomes are known. This is not external
preregistration. A cache hit reuses a certificate and is not an independent
replication. A skipped mean-separation precondition is an attempt, not an
enclosed probability event.

## Marginal and dependent-count certificates

For an observed interval A, exact geometry encloses its Poisson mean on the
whole parameter box. Poisson CDFs at a fixed integer threshold decrease
monotonically with their means. Directed integer normalization and explicit
infinite-tail bounds therefore enclose the event probability throughout the
box. Disjoint reference and moved probability intervals yield a uniform TV
lower bound by the definition of total variation and projection onto that
labelled count. All other labelled counts remain in the full experiment.

For two observed intervals A,B with a common fixed anchor, decompose
N(A)=C+U and N(B)=C+V into independent Poisson counts on the three disjoint
atoms. Then N(A)-N(B)=U-V. The original overlapping counts are dependent;
only the disjoint atoms are independent. For mean rectangles
a in [aL,aU], b in [bL,bU] and common intensity c in [cL,min(aU,bU)],
partition the entire closed common-intensity range into 64 closed slices
[l,u]. On each slice, the exclusive means lie in

    a-c in [max(0,aL-u), aU-l],
    b-c in [max(0,bL-u), bU-l].

These rectangles may include unattainable combinations, which only enlarges
the bound. The common-intensity lower bound comes from the uniform virtual
tip construction proved in `../triple_cube/THEOREM.md`. Mixed relative-motion
terms are retained. Monotonicity of P(U-V<=k) in the two exclusive means
reduces each rectangle to opposite corners. Directed Poisson sums include
their infinite tails. Take the minimum of lower bounds and maximum of upper
bounds across every slice. Budget failures return [0,1] and cannot exclude.

For reference and moved event intervals [pL,pU], [qL,qU],

    TV(full reference law, full moved law)
        >= max(0, pL-qU, qL-pU).

If this bound exceeds 1/4, the box cannot satisfy the strong target. The
shared law cache includes pair, anchor, integer threshold and the complete
geometry/statistics record. Both reference and moved law lookups are checked
against their intended input; using a law from another box is rejected.

## Coverage and scope

Each new record replaces only an inherited HOLD with exactly the same closed
box. The octree partition, all 539 inherited exclusions and 23 previously
tested HOLD records are unchanged. Thus the source closed cube cover and
all boundary coverage are retained. Sum exact rational volumes; shared
boundaries have zero volume. Volume fractions are not probabilities.

The independent audit reconstructs the source octree and stage replacements,
checks geometry by fixed boosted time minus squared spatial separation,
validates the uniform virtual subset and complete overlap slices, and
compares certified PMFs with separate 100/110-digit direct sums. It includes
wrong-cache, missing-input, missing-slice, small-mean, zero-rate and dependence
controls. Decimal and point checks are diagnostics; exact uniform interval
and integer certificates carry the mathematical exclusions. Full replay is
an additional reproducibility check, not independent evidence.

No failed exclusion proves a counterexample. An operator gap upper bound
above 1/5 does not prove the actual gap exceeds 1/5. No conclusion about all
multi-support motions, other references, continuum accuracy or general
stability follows from this bounded pass.
