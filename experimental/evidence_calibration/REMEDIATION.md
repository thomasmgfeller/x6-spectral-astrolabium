# Audit remediation — 2026-10-12

Baseline: dccddf868a29fa59c7f320f81c7112b8ec959073.
Scope: isolated evidence/calibration modules and their own CI only.

| Finding | Correction | Regression |
|---|---|---|
| A01/A02 false strings or truthy non-bools authorize | Exact bool contract; reject invalid | test_A01, test_A02, all_invalid_gate_flag_types |
| A03 NaN threshold reported as no signal | Finite nonnegative threshold contract | test_A03, threshold_invalid_values |
| A04 intermediate overflow with OK | Scaled weights; finite outputs or rejection | test_A04, representable_large_centroid_and_total_overflow |
| A05 invalid timestamp accepted | Strict UTC syntax and actual date parsing | test_A05, dates_types_and_explicit_utc |
| A06 bool treated as pixel length | Exact numeric type contract | test_A06, no_inferred_scale_or_class |
| A07 data/hash race | One bounded read per input, same bytes hashed and parsed | test_A07, snapshot_read_bound |
| A08 mutable evidence inputs | Deep finite JSON snapshot | test_A08, sweep_callback_cannot_mutate_archived_parameters |
| A09 invalid metadata containers | Nonempty typed identifiers | test_A09 |
| A10 checksum without schema | Required schema, types and digest format checked | test_A10, record_rejects_bad_schema_even_rehashed |

The audit's A07 injection has been moved from the removed double-read loader
path to the new byte-snapshot seam. It asserts two reads, actual mutation of the
sample file after reading, 1-pixel output and the ORIGINAL bytes' hash. This
preserves and strengthens the criterion; the old test hook would no longer
exercise the changed path.

The original optical CSV fixture is explicitly labeled SYNTHETIC, adds the
required image-plane/scale semantics and expects SYNTHETIC_RESULT. Original
arithmetic and corrupt-CSV assertions are retained. The old test named
`integrity_and_replay` is renamed `integrity_and_repeatability`: it never ran a
full experiment replay. No full replay implementation is claimed in this patch.

The independent parity-equation, nearest-neighbor and rational-arithmetic checks
from the audit are retained with the SAME 1e-12 absolute tolerance and seed 104729:
128 received words, 2,048 codeword/error-mask pairs, 1,000 small synthetic frames,
and 1,000 replicate series. These are finite/synthetic tests, not error rates on
real experiments or physical measurement uncertainty. The 0.75-pixel uniform
background counterexample remains an expected method limitation, not a removed
failure or alleged new physics result.

Run counts and outcomes belong in the generated report.json, not an unsupported
static success badge. All ten A01-A10 checks must pass, all existing cases must
run, and the pinned app check must pass on CI before merge. This is software
acceptance only; physical measurement release remains blocked.
