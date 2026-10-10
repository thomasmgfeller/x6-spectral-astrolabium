# X6 source agents

These three unattended agents run the actual, unmodified `app/index.html` in
Chromium. They are reproducible software benchmarks on fixed historical data.
They do not discover new measurements or demonstrate better physical performance.
The existing live NOAA workflow is separate.

## Schedule and evidence

Workflow: `.github/workflows/x6-source-agents.yml` (**X6 Source Agents**).
Three independent jobs: `atlas`, `qutech`, `nasa`; a failed job does not cancel
the others. Scheduled on **11, 12 and 13 October 2026 at 06:37 UTC**
(08:37 Europe/Zurich). The authorised trial ends **14 October 2026 at
00:26:52 Europe/Zurich** (`2026-10-13T22:26:52Z`). A date guard before checkout
reserves the complete 25-minute job timeout and skips all agent work outside
the window, including manual launches. Push and pull-request triggers are removed.
An end-of-trial cleanup is scheduled to remove cron; the full-year date guard
also prevents an annual restart if that cleanup is delayed. GitHub may
delay scheduled runs or disable schedules after prolonged public-repository
inactivity. Scheduling is not a real-time service guarantee.

Each job has a 25-minute timeout. Original selected files, input transforms,
browser evidence, exact Python checks, errors, dependency versions, source-code
hashes and an artifact SHA-256 manifest are uploaded for **14 days**. Names:
`x6-atlas-agent-RUN-ATTEMPT`, `x6-qutech-agent-RUN-ATTEMPT`, and
`x6-nasa-agent-RUN-ATTEMPT`. Full NASA/Zenodo archives are never uploaded.
The small NASA cache is about 2.1 MB; it is validated against fixed file hashes
on every use. Public data only; no account credentials or LLM API are required.
The browser is restricted to its local application server.

## Graph Atlas

Source: [NetworkX Graph Atlas](https://networkx.org/documentation/stable/reference/generated/networkx.generators.atlas.graph_atlas_g.html),
bundled in pinned NetworkX 3.4.2; underlying reference: Read and Wilson,
*An Atlas of Graphs* (1998). NetworkX is distributed under BSD-3-Clause.

- All **1,253** unweighted simple graphs on zero to seven vertices are visited.
- **995** connected graphs with at least two vertices: actual browser rational
  lower-bound search and Rayleigh upper witness, checked again using Python
  `fractions.Fraction` for every search decision.
- **258** remaining inputs: global positive-gap certificates must be explicitly
  rejected. Isolated vertices are retained as vertex declarations. Empty and
  singleton inputs have their own expected rejection reasons.
- For all nonempty graphs, browser component count is compared to NetworkX;
  browser numerical eigenvalues are compared to NumPy `eigvalsh` with absolute
  tolerance `1e-9`. Numerical agreement is not interval arithmetic or a proof.

Inputs are saved in `atlas_inputs.json`; each browser result and independent
check is saved in `atlas_results.jsonl`. Passing this finite catalogue is not
a correctness theorem for every weighted graph or larger graph.

## QuTech / mobile spin qubits

Source: Krzywda, Matsumoto, De Smet et al. (2026), *Coherence Protection for
Mobile Spin Qubits in Silicon*, [Zenodo DOI 10.5281/zenodo.18470200](https://doi.org/10.5281/zenodo.18470200),
version 1, CC-BY-4.0. No author or institution endorsement is implied.

Selected original member: `data/ds_1730672289460108893.hdf5` (4,815,464 bytes).
SHA-256: `7c42a454d7704cbea3291f59d6f671f6214dfafcf14315c016f512c37428b84c`.
The agent retrieves the ZIP directory and this member by HTTPS byte ranges,
about **3.22 MB per run**, rather than fetching the 1.16 GB archive. Local ZIP
header, member size, CRC and pinned member SHA-256 must match. The full archive
MD5 is not claimed to be verified by partial downloads.

The inspected `_m0` dataset has shape `(200 wait settings, 1000 repetitions)`
and units mV. Fixed rows **0, 99, 199**, first **512 repetitions** each, are
processed separately. The wait axis and repetition axis are explicitly checked;
dimensions are never flattened together. Original values, wait time in ns,
repetition indices, source timestamp and z-score parameters are retained.

These are repeated voltage readouts, not 512 consecutive time samples of a
calibrated waveform. Frequency axes therefore have units per repetition, not Hz.
There are no trusted qubit-state labels or clean signals in this benchmark.
It does not estimate readout fidelity, prove a coherence improvement or reproduce
the entire publication. Missing data or a changed schema fail the job.

## NASA / IMS bearings

Source: J. Lee, H. Qiu, G. Yu, J. Lin and Rexnord Technical Services (2007),
IMS, University of Cincinnati, distributed by the [NASA PCoE repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/).
The source README identifies the supported test setup and channels. Credit the
original researchers and NASA repository when reusing data. Third-party source
data are not relicensed by this repository; no affiliation is implied.

Official archive:
`https://phm-datasets.s3.amazonaws.com/NASA/4.+Bearings.zip`.
Archive SHA-256:
`21001ac266c465f5d345ec42d7b508c6a6328487fd9d4d7774422dd5ea10ad83`.

On a cache miss, download up to **1.1 GB**, check the full archive hash, unpack
only test 2 and its README, retain three named original files plus that README,
and discard temporary archives. Cache hits validate every retained file hash;
a 64-byte request also checks current archive availability, size and ETag.
Cache eviction requires another bootstrap. Each download has two attempts,
a socket timeout, byte cap and overall deadline.

The three chronological anchors are:

| Original record | Position in the 984-record test |
|---|---|
| `2004.02.12.10.32.39` | first |
| `2004.02.15.20.32.39` | middle, index 492 |
| `2004.02.19.06.22.39` | final |

Each file must contain exactly 20,480 rows and four finite measurement channels.
The agent sends the first **1,024 contiguous samples of channel 1** to X6, with
the documented 20 kHz sampling rate recorded separately. That window is 51.2 ms
long; no decimation or interpolation is applied before the signal import.
Full-record RMS, population standard deviation and maximum absolute amplitude
are observations only. Original amplitudes are preserved before z-scoring.

Chronological position does not supply a per-record health label. In particular,
the final record has a much smaller amplitude than the earlier selected records;
we do not infer recovery or a specific physical cause from that observation.
These checks are not an early-warning classifier or a validation of fault detection.

## Shared signal checks and interpretation

For each of the six experimental windows, the agent imports a CSV into the real
X6 signal panel (seed 104729, 20 Monte Carlo draws), verifies unchanged imported
samples, runs 15 browser self-tests, and checks finite output and conjugate
symmetry. Four analytic graph controls include too-high and equality rejection.
SNR/Monte Carlo thresholds remain observations, not pass criteria.

The existing app maps a stride-selected subset of at most 24 samples to a weighted
path. The sigma rule is `max(1, largest adjacent selected-sample difference)`;
weights are rounded to six decimals. Every exported rational lower/upper bound
and search decision is independently recomputed by a separate Python implementation.
This is a same-project cross-check, not external peer review. A path derived this
way is a model of the selected data, not a measured physical interaction graph.

`PASS` means all specified source, software and mathematical gates executed and
passed. Missing source, unexpected format, checksum mismatch, browser failure or
failed certificate yields a nonzero exit and `FAIL` evidence. Setup failure is
reported as `NOT_EXECUTED`; it cannot produce a successful data report.

## Local execution

Requires Python 3.12 and libarchive (available on the selected Ubuntu runner).

```bash
python -m pip install -r agent/source-requirements.txt
python -m playwright install chromium --only-shell
python -m unittest tests/python/test_data_agent.py tests/python/test_source_agents.py -v
python agent/run_sources.py --source atlas --output /tmp/x6-atlas-new
python agent/run_sources.py --source qutech --output /tmp/x6-qutech-new
python agent/run_sources.py --source nasa --output /tmp/x6-nasa-new --cache-dir /tmp/x6-source-cache
```

Output directories must be new/empty. To disable these three jobs, disable the
**X6 Source Agents** workflow; this does not disable the original NOAA agent.
