# Joint support, count and frame feasibility

19 October 2026. Revision 2 after six development clouds, before any target
cloud. Revision 1 is public at 8647afdc5177600251faf2cc08e3674568d6b5ee.
Implementation will be frozen publicly again before fresh targets.
Parent: outer-diamond HOLD. Development history is retained separately.

## Question and intervention

Can one intrinsic construction simultaneously supply sufficiently populated
root/support and landmark intervals, a stable Lorentz frame, and a nondegenerate
quadratic design? Pure outer expansion has already failed for the fixed old
supports. This study changes supports explicitly and reports the associated
change of resolution. It does not recalibrate or qualify a differential operator.

Generate the unchanged unit inner diamond, including its two labelled probes,
and independent physical Poisson shells to outer duration 1.5 using the previous
sampler. Root and its marked longest chain remain those of the original inner
problem. The two temporal supports are now also adaptive: at each count scale,
choose the nearest chain point on each side with count >=2k and both half-counts
>=4. Both points must be physical inner events. Probes are never counted as events.
The old support and frame rule are a paired diagnostic reference.

All selection receives only the relation, independent marks, known density,
inner membership, the fixed root/chain and selection colours.
Simulator coordinates are unavailable to the inference module.

## Fixed bounded joint search

1. For each count scale k=16,32,64, candidates are physical inner events
   causally related to the root with k <= N(root,b) < 2k, excluding the two
   selected temporal points. Root intervals must already meet full-count >=16 and
   both selection-colour half-counts >=4. Keep the first 64 by independent
   mark in each time direction. The scale is tau_k=(k/(rho*pi/12))^(1/3).
2. Frame candidates are in the common past or common future of the root and
   both temporal points. All these intervals must meet the unchanged count
   guards. Keep 256 per side by mark. Enumerate every three-element causal
   chain in these finite pools whose mutual intervals meet the same guards.
   Enumerate through eligible middle vertices, not all unordered triples.
   Gram construction and normalization use the unchanged intrinsic formula.
   Require Lorentz signature, condition <=100, and both half-Gram signatures
   and normalized errors <=0.25. Sort surviving frames by condition then
   marks. Test at most 128 frames for each support scale.
3. For each tested frame require all landmark/support intervals to pass the
   count guards. Features are the unchanged intrinsic landmark features.
   The difference between the temporal features defines a timelike observer
   axis; temporal features must straddle the root in this axis. A shell
   candidate must have transverse radius <= (2/3)*tau(root,b) in this frame.
   Require each point's relative half-feature error <=0.25 (a conservative
   construction filter in addition to the unchanged aggregate guard).
   Keep at most 16 by mark per side and require at least four per side.
4. Combine these events with the two selected temporal points. Recheck EVERY
   interval and every inherited aggregate guard on the complete support.
   Require rank nine in the linear/quadratic design, relative SVD threshold
   1e-10, and design condition <=1000. This additional feasibility requirement
   prevents a merely numerous but degenerate support from counting as success.
5. Select the first jointly passing frame at the smallest passing count scale.
   Keep its selection immutable. Only then reveal a second independent binary
   recolouring and recheck the complete unchanged guard. No retries, support
   changes or scale changes are permitted after this check.

The second colouring checks sensitivity to auxiliary thinning; it is not an
independent physical cloud, a confidence interval, or proof of stability under
arbitrary perturbations. Count-based selection is itself adaptive and needs
separate analysis before any subsequent statistical coverage claim.

## Reporting and decision

Revision rationale: the initial six development clouds selected no support.
At low density the fixed temporal points failed the count guard; at high
density the 64-per-side frame pools supplied only three and zero count-qualified
triples. Revision 2 adapts the temporal supports as part of the joint task and
raises the bounded frame pool. It neither changes any acceptance threshold
nor converts these development observations into confirmation evidence.

Three densities, two development seeds and sixteen fresh target seeds each;
the exact constants and budgets are in contract.json. Full denominator includes
short chains, insufficient supports and exhausted frame searches. Keep funnel
counts, search truncation counts, selected witnesses, rejected-stage reasons,
all required interval counts and both colour audits. Report selected tau_k
relative to the old tau_m, support sizes and conditioning. Coordinate-only
diagnostics after selection report actual support extent and Lorentz Gram
error; they cannot select a frame or override the decision.

Primary descriptive target: at least 13/16 high-density clouds pass jointly
and also pass the held-out recolouring. This pilot fraction is not a lower
confidence bound on population success. Low/middle densities remain visible.
An exhausted capped search is not an exhaustive no-go theorem. No claim that
the chosen frame/support is unique, optimal, or yields accurate derivatives.
HOLD_PHASE3 and the earlier BD-C2 NO_GO remain in force under every outcome.

## Controls and source binding

Check direct scalar interval counts with probe exclusion, all intervals in
each retained witness, count-threshold boundary cases, signature/condition and
rank rejection, marked relabelling and time reversal on development examples,
and invariance to changes of the hidden audit colours before the audit step.
Use fixed-budget full replay with exact discrete decisions and fixed numeric
tolerances. Coordinate-byte hashes are recorded separately from relation and
decision equality, following the previous portability policy. Record all
development revisions; freeze code and protocol before target generation.
