# X6 bounded mathematical falsification agent

Version 2, 11 October 2026; operating window repaired 13 October 2026. Lorentzian priority with bounded replication and
adaptive controls. A small search program with explicit
hypotheses, reproducible counterexamples and a compulsory stop time. This is
experimental mathematics infrastructure, not an autonomous theorem prover.

## Operating contract

- Configuration: `agent/math-agent-config.json`.
- Pilot window: 11 October 2026, 10:13:02 Europe/Zurich through **Sunday,
  18 October 2026**. Exclusive cutoff: **19 October 2026, 00:00:00
  Europe/Zurich** (`2026-10-18T22:00:00Z`). The maintainer explicitly
  authorised this extension on 13 October; all three workflows share the cutoff.
- Scheduled attempts: **every six hours**, at 00:23, 06:23, 12:23 and 18:23 UTC,
  only on 11–18 October 2026. The full date guard rejects earlier/expired attempts.
  GitHub may delay or omit scheduled attempts. This is periodic execution,
  not a continuously running process or a delivery guarantee.
- An initial main-branch push of the new source triggers a qualification run.
  Pull requests changing these sources also run a qualification. Manual launches
  and later code-triggered runs are subject to the same guard. Cron becomes
  active only after this workflow is approved and merged to the default branch.
- Stop immediately: set `enabled` to `false`, disable **X6 Bounded Math Agent**
  in Actions and cancel an already running job if necessary. A config change
  cannot be seen by a process that already checked out an older commit.
- Every run has a 5-minute workflow timeout. Admission reserves 6 minutes
  before the end, before installing dependencies. The research process has
  a 90-second budget by default, Unix alarm, per-case checks and subprocess
  timeouts. The configurable ceiling is 120 seconds and 128 cases per track.
- The config reader refuses windows longer than 8 days (192 hours). Changing a future
  window also requires explicitly adapting the cron dates, source pins and
  monitoring/shutdown schedules. Neither extension
  happens automatically. No automatic self-modification or self-extension.
- No overlapping workflow jobs; readonly repository permissions. No LLM,
  paid API, private data, model training or source-data downloads. Standard
  GitHub-hosted runners and artifact storage remain subject to account billing.

## What is implemented

Two Lorentzian tracks run first: exact small-order literature replication and
two finite-diamond sequences against an analytic spectrum. Definitions,
research status, metrics and next steps are in `LORENTZ_RESEARCH.md`.

Three supporting hypotheses are searched with **24 cases per track**, reduced
from version 1's 96 to prioritize Lorentzian work within the unchanged budget.
Their per-track seeds also change with the new position in the run sequence;
compare versions using recorded hashes.
Every six-hour slot has a distinct deterministic seed derived from the fixed
base seed. Within the phase and perturbation searches, half of the candidates
are new, and half mutate a strong previously observed witness. This allocation
is deliberately simple and auditable. Learning does **not** persist between
runs; there is no claim of a self-improving AI or automatic theorem discovery.

The application SHA-256 is pinned. The agent extracts the **unchanged** `fft`,
`transform`, `filter` and `makeGraph` numerical functions from `app/index.html`
and executes them in a Node VM. A changed app hash or unexpected code layout
fails closed. This is numerical-core testing, **not browser E2E**; the existing
data agents separately exercise Chromium. The phase outputs are compared to
a NumPy FFT implementation with absolute tolerance `1e-9`.

### M1: information loss in the signal-to-graph map

Tested hypothesis: the ordered Gaussian weighted path determines its signal,
up to a global sign and additive constant.

The built-in exact witness is `x=(0,1,2)` and `y=(0,1,0)`, with fixed positive
sigma. Both have squared consecutive increments `(1,1)` and therefore identical
weights `exp(-1/sigma^2)` at both edges, before and after the same rounding.
The first increments agree and the second differ, so the two signals are not
related by a global sign plus translation. The actual X6 mapping is checked.

For n labeled samples with all consecutive differences nonzero, fixed sigma,
exact unrounded weights, and a fixed first sample, each edge determines only
the magnitude of the corresponding difference. Every one of the `2^(n-1)`
sign patterns generates a distinct signal with the same ordered graph.
Modulo global sign there are `2^(n-2)` classes. Rounding introduces additional
ambiguity. These counts do not assert uniqueness under a different topology,
different constraints, unknown sigma or spectral-only observations.

This is an elementary consequence of the mapping, **not a novelty claim**.
A future research question is which extra measurements or constraints recover
identifiability, and how much uncertainty remains after those additions.

### M2: finite-graph perturbation certificates

For nonnegative undirected edge weights on the same labeled vertices, let
`delta_ij=w'_ij-w_ij` and `r=max_i sum_j |delta_ij|`. Then

`||L'-L||_2 <= ||L'-L||_infinity <= 2r`,

because each absolute row sum is at most
`|sum_j delta_ij|+sum_j |delta_ij| <= 2 sum_j |delta_ij|`.
The first inequality follows from symmetry and the usual induced-norm bound.
The symmetric eigenvalue perturbation bound therefore implies

`|lambda_2(L')-lambda_2(L)| <= 2r`.

If `b<lambda_2(L)` is certified, `b-2r<lambda_2(L')` follows. The agent
independently tests those transferred bounds by exact rational Schur
complements on small connected weighted paths. NumPy is used for search
ranking only; its eigenvalues do not establish exact counterexamples.

The deliberately stronger factor-one hypothesis is refuted already with
two vertices: increasing the single edge weight from `1` to `11/10` changes
the nonzero eigenvalue from `2` to `11/5`, a change of `1/5=2r`.
The general bound is therefore sharp without extra restrictions. The agent
records exact rational enclosures that independently certify the violation.

This is a standard perturbation argument and a calibration target, not a new
theorem. Search is currently limited to paths of 2–8 vertices, denominator
100, bounded mutations and ten rational bisection steps per enclosure.
Broader graphs, interval propagation from sensor uncertainty, floating-point
exp rounding guarantees and sharper conditional bounds remain future work.

### M3: time-shift sensitivity of the actual Fourier phase filter

Tested hypothesis: with angle and width fixed, filtering commutes with every
circular shift of the input. The reported defect is

`||F(T_s x)-T_s F(x)||_2 / ||x||_2`.

The calibration signal is `(1,0,-1,0)` repeated eight times, angle 0 degrees,
width 45 degrees, pass mode. Its nonzero positive Fourier component has phase
zero and is retained. A one-sample circular shift changes that phase to
`-pi/2`; the component is rejected. The normalized defect is one in exact
arithmetic. Node and NumPy provide numerical realizations of this analytic
example. Additional single-tone cases vary frequency, phase, angle, width and
shift. They do not constitute a denoising benchmark or a physical experiment.

This is a direct consequence of the DFT shift theorem, not newly discovered
mathematics. It suggests research on justified alignment rules or equivariant
alternatives. An angle change applied to all frequencies is generally not the
same as undoing a time shift, since the phase shift depends on frequency.

## Results and epistemic status

- `PASS`: all configured research tracks executed and their numerical/exact
  checks passed. It does **not** mean their hypotheses are true.
- `FALSIFIED_EXACT_WITNESS`: an exact counterexample to the stated hypothesis.
- `NUMERICAL_COUNTEREXAMPLE`: floating-point evidence; inspect the analytic
  control separately. No exact proof status is assigned from floating point.
- `SURVIVED_FINITE_SEARCH`: no counterexample in this bounded search; no proof.
- `LITERATURE_REPLICATION_EXACT_SMALL_ORDERS`: exact n=3..5 published counts match.
- `FINITE_SIZE_NUMERICAL_COMPARISON`: sequences checked against the known 1+1
  diamond spectrum; no asymptotic or physical claim.
- `FAIL`: execution or cross-check failure; inspect the report.
- `INCOMPLETE`: budget exhausted; completed tracks remain available, not a PASS.
- `STOPPED`: no research execution was admitted.
- A setup failure with no report is `NOT_EXECUTED`, not a successful run.

Each artifact includes the complete searched cases, actual core outputs,
exact witness inputs, parameters, run seed, runtime versions, source digests,
git commit, per-track status, report and SHA-256 manifest. Adaptive cases are
selection-biased: no population success rate, p-value or model-performance
claim may be inferred from them. Literature novelty and general proofs require
separate expert review. Nothing here validates quantum gravity, readout
fidelity, fault detection or physical interaction graphs.

Results are Actions artifacts `x6-math-agent-RUN-ATTEMPT`, retained **30 days**.
Archive selected runs deliberately for longer-term reuse. The main app and
the four existing data-agent configurations are unchanged.

## Local commands

Requires Node 24 and Python 3.12 (Linux for the Unix deadline alarm).

```bash
python -m pip install -r agent/math-requirements.txt
python -m unittest tests/python/test_math_agent.py tests/python/test_lorentz_spectral.py -v
python agent/run_math_agent.py --guard
python agent/run_math_agent.py --output /tmp/x6-math-new
python agent/run_math_agent.py --replay-slot 0 --output /tmp/x6-math-replay
```

`--replay-slot` reuses the report's `seed_slot`, labels the run REPLAY and never
bypasses the admission window. Cross-platform floating-point results may differ
within tolerances; exact rational witnesses should agree.

The output directory must not exist. After expiry, an explicitly re-authorized
configuration is required for any new search; changing the random seed does
not bypass the window. Saved witnesses can be checked offline directly without
starting the scheduled search. A scheduled ChatGPT review reads evidence and
literature; it does not modify hypotheses, code, scope or operating limits.
