# Certified closure of the three-support parameter cube

SPDX-License-Identifier: Apache-2.0

## Precise statement

Let theta(0) be the frozen rational reference inherited from PR #122, in 2+1
Minkowski space, at the declared density and physical scale. Let theta(s),
s = (u,v,w) in [-1/10,1/10]^3, move only nodes 15,17,5 in boosted x;
boosted time and the transverse coordinate, the other 18 selected nodes,
the root, landmarks and observation protocol stay fixed. Keep the inherited
unchanged-order and admissibility conditions. Let P_s be the conditional law
of the 90 labelled observed counts, including their overlap dependence, and
let W_s contain all 17 physical minimum-norm quadratic-moment weights.

Define g(s) = 2 ||W_s-W_0||_2 / (||W_s||_2 + ||W_0||_2).
If the complete closed cube cover has no HOLD leaf, and every terminal leaf
passes one of the verified uniform exclusion gates below, then

    for every admissible s with unchanged selected-node order:
        TV(P_s, P_0) <= 1/4  implies  g(s) <= 1/5.

The premises are certified in this execution: `summary.json` records 2,367
terminal exclusions and zero HOLD leaves; `audit.json` reports PASS on the
complete closed cover and all four refinement rounds. Deterministic replay
reproduces all four archives and the summary exactly. Thus the implication
above holds throughout the declared domain under its stated conditions.
The comparison is to ONE fixed reference. No arbitrary-pair theorem, general
GFEST result, other references/directions, full selection-and-graph likelihood,
statistical single-sample accuracy or continuum statement follows.

## Uniform exclusion gates

1. A safe source-square projection or node-5 strip supplies a count-event
   separation strictly greater than 1/4, or an order contradiction, throughout
   the subregion. Its witness uses only moving nodes included in that earlier
   law and fixed anchors. Old two-support operator-gap bounds are not extended
   away from the plane where they were proved.
2. A whole-box causal-sign contradiction rules out unchanged order.
3. Exact rational interval geometry and the joint rank-at-most-six moment
   update give a physical operator-gap upper bound at most 1/5 everywhere
   in the box. All three changing columns, mixed terms and the root weight
   are included. Failure to certify invertibility remains HOLD.
4. A labelled marginal Poisson event gives a uniform full-law TV lower bound
   strictly greater than 1/4.
5. A common-anchor difference event gives the same strict lower bound. For
   overlapping intervals A,B, N(A)-N(B)=U-V for independent Poisson counts on
   the two disjoint exclusive atoms. Independence is not assumed for the
   original observed counts. All possible common intensities are covered by
   512 closed rational slices. Opposite monotone corners bound each exclusive
   rate rectangle; directed integer sums include the infinite Poisson tails.

The exact geometry polynomial, joint moment identity, Neumann enclosure,
physical normalization and probability arguments are those proved in
[the three-support derivation](../triple_cube/THEOREM.md) and
[the preceding subdivision](../triple_subdivision/THEOREM.md).
The unchanged gates are applied on smaller boxes. Thresholds remain 1/5 and
1/4. Bounds are rounded outwards. A gap upper bound above 1/5 or a TV lower
bound below 1/4 is never treated as a counterexample.

## Closed coverage, not sampling

Start with the 1,352 verified terminal boxes of PR #122. Exactly 38 are HOLD;
the other 1,314 exclusion records remain unchanged. In each round replace
EVERY currently unresolved closed box by its eight rational midpoint octants.
These cover their parent exactly, have disjoint interiors, and include all
faces, edges and vertices. No parent is silently dropped. The audit constructs
all coordinates independently from the original 8-by-8-by-8 grid and path.
An equal volume sum alone would not establish coverage; the full replacement
tree, exact endpoints and all eight children are checked.

Inductively the terminal boxes cover the entire closed cube. If every leaf
excludes the conjunction of unchanged order, admissibility, g>1/5 and
TV<=1/4, that conjunction is impossible anywhere in the cube. Restricting to
unchanged-order admissible configurations gives the stated implication.
The non-strict weight conclusion and strict probability exclusions are
essential. Parameter volume is not probability.

## Budget and provenance

The internal contract freezes at most six complete refinement rounds and
20,000 new geometric boxes. A round is started only if all its children fit
the budget; every unresolved box is retained on stopping. Each remaining
geometric failure receives at most two deterministically ranked marginal
events, then one highest-ranked overlap event if still unresolved. No event,
threshold, overlap resolution or budget is retuned after seeing results.

The contract, classification runner and predecessor inputs were hashed before
new child evaluations. The source results were known; this is not external
preregistration. The audit was adapted afterwards, as explicitly declared in
the contract. It checks independently reconstructed exact geometric ranges,
direct nine-moment solves, high-precision marginal/difference PMFs, complete
covers, cache identities and deliberate missing/corrupted inputs. Uniform
interval/integer certificates carry the claim; center/corner solves and
high-precision decimal PMFs are diagnostics. Computational replay is not
independent personnel review or proof-assistant verification.
