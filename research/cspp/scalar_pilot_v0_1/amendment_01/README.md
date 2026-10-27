# Amendment 01: unbiased outer-shell selection

During review of the first development run on 2026-10-27, before publication,
the optional outer-shell sampler was found to truncate a **time-sorted**
rejection-sampling batch. Selecting the first accepted points from this sorted
batch biases the shell toward early times. The inner Poisson sprinklings are
unaffected because their entire point sample is retained.

Correction: randomly permute each proposed batch before rejection and truncation.
The accepted sequence is then exchangeable, giving the required iid uniform
shell positions conditional on the independently drawn Poisson count.
The same seed identities and all physical parameters, run counts, error definitions
and thresholds are retained. This is a development-code correction after seeing
the first results, **not a new pre-registered confirmatory experiment**.

`original_scalar.py` and `original_FREEZE.json` preserve the affected source and
initial source lock. `original_RUNS.json` preserves all original run/cloud/count
hashes. `UNCHANGED_PRIMARY_HASHES.json` records the original primary numerical
arrays. The corrected pilot is rerun in full, and the publication audit requires
byte-identical primary operator, propagation, residual and reference-probe arrays.
Only the optional outer-cloud coordinates and their paired boundary diagnostics
are superseded. The initial outer results must not be interpreted scientifically.

The final `../FREEZE.json` locks the corrected development implementation.
The earlier E4 confirmation contract remains DRAFT / NOT_FROZEN.
