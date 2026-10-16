# Causal orders and spacetime questions

This research asks what structure is carried by relationships before a spatial drawing is assumed.

[Deutsch](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/causal-orders.md) · [Wiki overview](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/)

Source snapshot: 2026-10-16 · `08c64744caa584c940b45a8825d0b099ae0c92fb`

## Events and their ordering

A causal order describes which events can precede which others. Imagine three tasks: A must happen before B, and B before C. Then A must also precede C. This implication is called transitivity.

Some pairs have no specified ordering. In a causal spacetime interpretation they may be spatially separated. An arbitrary generated network does not automatically justify that physical interpretation.

A Hasse diagram draws only the immediate relationships. The full relation matrix also contains the relationships implied by transitivity. An attractive arrangement of dots on a screen is not a measured geometry.

## Why a spectrum is not the whole story

Renumbering the nodes can make a drawing look different while leaving its structure unchanged. Isomorphism here means there is a one-to-one node correspondence preserving every directed relationship. That correspondence need not be the only possible one.

A fingerprint summarises a structure using a few numbers or frequency counts. Different structures can share the same fingerprint, just as different people can have the same height.

| Project abbreviation | What it represents |
| --- | --- |
| H7 | A specifically defined combination of spectra and counts; not a unique identifier. |
| N1 | Local neighbourhood profiles. |
| Q1 | Spectra of targeted one-point extensions. |
| R2 | Iterative refinement of features of ordered node pairs. |
| P123 | Histograms of common predecessors and successors for sets of one, two and three nodes. |

Published counterexamples expose limits of these summaries. The full directed relation and exact isomorphism checking remain the comparison reference.

## What do fairer controls achieve?

Two generators are easy to distinguish if one produces much denser or taller orders. Comparison pairs were therefore selected with the same node count N, relation count R and height H. Here height is the length of a longest chain, counted in nodes.

In the published primary comparison at N=64, P123 showed no demonstrated incremental benefit: the baseline reached 54.30%, while the combination reached 50.39%. Four of nine comparison cells lacked enough matching pairs and received no performance assessment. This limits a tested method; it does not prove that learning geometry is generally impossible.

- [Matched-control study and original data](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_matched_controls/README.md)
- [Counterexamples and reconstruction limits](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_relational_boundary/README.md)

## A concrete next question: proper time

Proper time describes time along a timelike connection. In the specified flat 1+1-dimensional model, the target is its ratio to a known outer time scale. This is a statistical estimation task between two marked events.

The reference counts points in the open interval between the marks. In this model that motivates the estimate sqrt(K/(N−2)). The scale and dimension are given. The same finite order can admit several different geometric embeddings.

The published reference state covered here contains the target definition and contract from PR #42. The subsequent numerical run is documented separately; this wiki edition does not present it as already published in full or physically validated.

- [Proper time: definition, example and contract](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time/README.md)
- [Open Causal-Set Lab](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/rax-cqg-lab.html)
- [Limits of the browser model](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/research/rax/cqg-benchmark-v0.2.0/README.md)
