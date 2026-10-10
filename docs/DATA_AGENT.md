# X6 public-data test agent

This agent downloads public observations, drives the **actual, unmodified X6
browser application**, and checks its exported rational graph certificate with
a separate Python implementation. It does not train an AI, modify the app,
approve a release, or claim a physical discovery.

## Schedule and destination

- GitHub workflow: **X6 Data Agent**.
- Limited trial: **11–13 October 2026**, at **06:17 UTC** (08:17 Europe/Zurich).
- Authorised window ends **14 October 2026, 00:26:52 Europe/Zurich**
  (`2026-10-13T22:26:52Z`). A first-step date guard checks the full year and
  reserves the 15-minute job timeout. Outside the window even manual workflow
  runs skip installation, downloads, tests and uploads, with a STOPPED summary.
- Push and pull-request triggers have been removed. A scheduled end-of-trial
  cleanup will remove the cron trigger; the date guard also prevents an annual
  restart if cleanup is delayed. Existing evidence keeps its normal retention.
- Standard `ubuntu-24.04` runner; maximum 15 minutes; no overlapping runs per ref.
- Data and reports are uploaded as an **Actions artifact**, retained **30 days**.
  Open the workflow run under **Actions**, then its **Artifacts** section.
- The agent has read-only repository permission. It does not commit daily raw
  data into the source history, send messages, change settings or use paid LLM APIs.
- Scheduled GitHub runs may be delayed. Public-repository schedules may be
  disabled after 60 days of repository inactivity. This is periodic testing,
  not an uninterrupted measurement archive or guaranteed real-time service.

## Data and modelling contract

Source: NOAA / NWS Space Weather Prediction Center, GOES X-Ray Sensor.

<https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json>

The 0.1–0.8 nm `flux` channel is selected. Only finite positive observations with
`electron_contaminaton == false` (the operational API spelling) are used.
Missing/positive contamination flags are rejected. One latest contiguous
128-minute window from a single satellite is selected; gaps are not filled.
The selected end must be at most two hours old and no more than five minutes
in the future. If no suitable window exists, the data run **fails visibly**.
This quality gate is not a complete scientific calibration of the sensor.

For numerical conditioning the input is **zscore(log10(flux in W/m²))**. Raw
bytes, selected observations, mean, population standard deviation and timestamps
are retained. NOAA is credited; transformed data/results are not NOAA products
and imply no endorsement. The original observations are solar X-ray data,
not quantum-computer measurements.

The app imports the 128 normalized values as CSV and runs its existing signal
analysis with seed 104729 and 20 Monte Carlo draws. Its own tests and numerical
finite/reality gates must pass. SNR and Monte Carlo threshold outcomes are
recorded but **are not agent success criteria**: imported SNR uses a smoothed
proxy and cannot establish denoising performance against unknown truth.

The app's actual raw-signal handoff selects every sixth sample (22 samples),
then builds its declared weighted path graph. Sigma is explicitly chosen as
`max(1, largest adjacent captured-sample difference)` and weights are rounded
to six decimals. These choices prevent zero rounded weights in this bounded
test; they are modelling choices, not inferred physical interactions.

The agent checks:

1. Four analytic browser controls, including too-high and equality rejection.
2. Signal import fidelity and the app's signal self-tests.
3. The actual browser subsampling, graph mapping and downloaded export.
4. The exported strict lower bound with Python rational Schur complements.
5. The exact upper Rayleigh witness and every recorded bisection decision.

The Python checker is a separate implementation, but remains part of the same
project. This is **not independent peer review**, formal verification of every
program path, or physical validation. Certificates cover the rounded rational
graph only. Browser exports are preserved without rewriting their historical
external-verification labels; the Python result is a separate evidence file.

## Reproduce one iteration

```bash
python -m pip install -r agent/requirements.txt
python -m playwright install --with-deps chromium --only-shell
python -m unittest tests/python/test_data_agent.py -v
python agent/run_agent.py --output agent-output
```

The output directory must be new/empty. To explicitly replay a saved source:

```bash
python agent/run_agent.py --replay saved/noaa_raw.json --output replay-output
```

Replay bypasses freshness only and is labelled **REPLAY**, never LIVE.
`X6_CHROMIUM_PATH` optionally selects an already installed browser; its actual
version is recorded. App and agent SHA-256 digests, Git commit, Python,
Playwright and Chromium versions are captured in `report.json`.

## Evidence and failures

The artifact contains `noaa_raw.json`, `selected_samples.json`, `signal.csv`,
`signal_evidence.json`, `sample_handoff.json`, `browser_certificate.json`,
`python_certificate_check.json`, `browser_controls.json`, `browser_run.json`,
`report.json`, `summary.md`, and `SHA256.json` where the corresponding stage ran.
Failure artifacts can have fewer files. **Missing/NOT_EXECUTED is never PASS.**
Exit status is nonzero when data or browser/certificate validation fails.
Downloads are limited to 2 MB, two attempts and 25 seconds per request.
Browser network requests outside its local app origin are blocked.

## Costs and storage

GitHub currently provides standard hosted-runner minutes free for public
repositories. Artifact storage has a separate shared allowance. This bounded
daily job with 30-day retention should use only a small part of that allowance;
it cannot guarantee the account's total bill when other jobs use storage.
No paid runners or API subscriptions are configured.

References:
- <https://docs.github.com/en/billing/concepts/product-billing/github-actions>
- <https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows>
- <https://docs.github.com/en/actions/how-tos/manage-workflow-runs/remove-workflow-artifacts>
