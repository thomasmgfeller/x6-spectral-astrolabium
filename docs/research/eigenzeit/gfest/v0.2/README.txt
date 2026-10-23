Eigenzeit / GFEST 0.2 - 23 October 2026

Read GFEST_Stabilitaet_v0_2.pdf for hypotheses, proofs, results and limits.
This is a separate supplement; GFEST 0.1 remains unchanged.

Reproduce from this directory:
  python -m pip install -r requirements.txt
  python verify_stability.py

Main result: under the declared complete labelled Poisson-landmark model,
all configuration pairs whose full laws are each within TV 1e-5 of the
archived reference have symmetric operator-weight gap below 0.07.
This is LOCAL and conditional on the model. It is NOT the original claim
at pairwise TV 1/4 and not a 7% statistical reconstruction guarantee.

All radius-grid outcomes, including HOLD, are in validation.json.
Rational certificate quantities carry the local result; printed decimals
and the finite high-precision Poisson checks are diagnostics.
run.log contains the execution summary. source_snapshot.json preserves
the fetched source data and PR122 scope. SHA256SUMS inventories the package.

No new clouds, no optimizer, no new classification of PR122's 38 HOLD cells,
no independent peer review or formal proof-assistant verification.
No changes were published to GitHub by this work step.
