# Legacy selection replay portability

SPDX-License-Identifier: Apache-2.0

PR #89 job 119836947315 failed at byte equality of a regenerated legacy
selection, after the summary comparison and controls passed. This assertion
includes two floating eigensolver/SVD condition diagnostics. Local replays
of configurations 0 and 31 agree numerically with the archived diagnostics;
the failing runner did not print their values. The revised check logs any
diagnostic difference and permits only 1e-12 absolute/relative differences
in `landmark_condition` and `design_condition`. All remaining selection
payload, including scale, selected node IDs, counts, order, status and funnel,
remains byte-exact after the existing JSON normalization. A change of choice
or decision therefore still fails. Nonfinite diagnostics fail.

Negative controls reject changed status, count, scale (even 1e-14), and a
1e-8 diagnostic perturbation. Archived evidence and frozen experiment code
are unchanged. This is a post-freeze verification change, not a new run or
a scientific gate adjustment. The remote replay must pass before merging.

Failure: https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/39782468556/job/119836947315
