# Eigenzeit: all 38 three-support HOLD boxes closed

SPDX-License-Identifier: Apache-2.0

**All 38 HOLD boxes from PR #122 close after four frozen refinement rounds.**
The complete closed parameter cube is covered by 2,367 terminal exclusion
boxes, with no unresolved leaf. All 1,314 previous exclusion records are
preserved unchanged. The calculation evaluates 1,160 new geometric children;
1,053 become terminal leaves and 107 are subdivided further.

For the fixed rational reference in 2+1 Minkowski space, let nodes 15, 17 and 5
move independently in boosted x over `[-0.1,0.1]^3`, keeping boosted time,
transverse y and all other data fixed. Among the inherited admissible
configurations with unchanged selected-node order, the result is:

> Full conditional labelled count/overlap-law TV from the fixed reference
> at most 1/4 implies symmetric physical operator-weight gap at most 1/5.

This is a reference-versus-moved result on this entire closed cube, including
faces, edges and vertices. It does not compare arbitrary pairs of moved
configurations. Other references, other displacement directions, the full
selection-and-graph likelihood and general GFEST stability remain open.
Parameter volume is not probability or a single-sample accuracy guarantee.

## Four complete rounds

Every currently unresolved parent is split into eight closed rational
midpoint octants. The inherited gates and thresholds stay fixed throughout.

| Round | HOLD parents | New children | New exclusions | Remaining HOLD | Remaining cube-volume fraction |
| --- | ---: | ---: | ---: | ---: | ---: |
| Source PR #122 | — | — | — | 38 | 19/2048 |
| 1 | 38 | 304 | 253 | 51 | 51/32768 |
| 2 | 51 | 408 | 354 | 54 | 27/131072 |
| 3 | 54 | 432 | 430 | 2 | 1/1048576 |
| 4 | 2 | 16 | 16 | **0** | **0** |

Counts at different subdivision depths have different granularity. The
remaining exact parameter volume decreases in every round. The final 16
children close by joint physical weight bounds; their largest gap upper
bound is below 0.194169, hence below the unchanged 0.2 threshold.

Of the 38 original boxes, 24 close completely in round 1, another nine in
round 2, four in round 3, and the last source box `357/5` in round 4. The
per-box inventory records every terminal descendant and its decision.

| Terminal exclusion | New leaves replacing the 38 boxes | Entire final cover |
| --- | ---: | ---: |
| Safe source-square projection | 28 | 502 |
| Node-5 count-law strips | 0 | 91 |
| Joint physical weight gap <=1/5 | 888 | 1,177 |
| Marginal Poisson event | 36 | 314 |
| Overlap-dependent difference event | 97 | 279 |
| Uniform order contradiction | 4 | 4 |
| **Total** | **1,053** | **2,367** |

The smallest newly excluding overlap-event TV lower bound is
**0.25045441759222643518 >1/4**. This bound applies to the corresponding
event exclusions, not to the whole cube. Original overlapping observed
counts remain dependent; independence is used only for disjoint Poisson
atoms. Every overlap law covers all common intensities with the inherited
512 closed rational slices and includes the infinite probability tails.

## Evidence and scope

- [Precise theorem and coverage proof](THEOREM.md)
- [Frozen contract](contract.json) and [227 pre-evaluation file hashes](freeze.json)
- [Complete summary](summary.json) and [one closure inventory per original HOLD box](closed_cells.json)
- [Independent audit](audit.json) and [execution record](execution.json)
- [Archive transport hashes](archive_parts.json) and [all deliverable hashes](SHA256SUMS)

The internal freeze preceded evaluation of any new child and included the
runner, contract and inherited scientific inputs. The previous results were
known. This is not external preregistration. The contract allows up to six
complete rounds or 20,000 new geometric cells, with no partial round; the
run stops early because no HOLD remains. No threshold, event ranking, slice
resolution or budget was retuned after seeing the new results.

The complete deterministic replay and independent audit both pass. Across
the four rounds, the audit checks **243,600 exact pairwise ranges**,
**1,384 direct weight enclosures**,
**144 marginal PMFs** and
**133,120 difference PMFs** across
**66,560 exclusive-rate rectangles**. All declared
negative controls pass. [Run](run.log), [replay](replay.log) and
[audit](audit.log) logs preserve the observed outcomes.

The independent audit reconstructs all child coordinates and complete
eight-child covers, preserves every source exclusion, checks exact pairwise
geometry and direct nine-moment solves, compares independent high-precision
PMFs, and rejects deliberately missing children, altered boundaries,
missing event inputs, missing slices and corrupted cache references. Exact
uniform interval/integer certificates carry the claim; center/corner and
decimal PMF checks are diagnostics. Deterministic replay is reproducibility,
not independent personnel review or proof-assistant verification.

## Reproduce

Run from the repository root with Python 3.12 and the inherited dependencies:

```sh
python3 -m pip install -r research/lorentz_local_dalembert/finite_poisson_bounds/requirements.txt
python3 -B research/lorentz_local_dalembert/triple_hold_closure/assemble.py
python3 -B research/lorentz_local_dalembert/triple_hold_closure/thc_run.py --workers 2 --verify
python3 -B research/lorentz_local_dalembert/triple_hold_closure/thc_audit.py --verify
python3 -B research/lorentz_local_dalembert/triple_hold_closure/thc_inventory.py --verify
sha256sum -c research/lorentz_local_dalembert/triple_hold_closure/SHA256SUMS
python3 tests/python/verify_manifest.py
```

Nine transport parts reconstruct four deterministic compressed JSON archives
(29,411,042 bytes in total). Assembly checks each part and the complete
archive before writing. The runner also assembles and verifies its frozen
predecessor inputs. Replay compares every complete round archive and the
final summary exactly. The dedicated CI job repeats these checks.

The [PR #122 subdivision](../triple_subdivision/README.md) is retained as
historical evidence of the previous 38-HOLD state. This module supplies its
closure without rewriting the earlier contract or certificates.
