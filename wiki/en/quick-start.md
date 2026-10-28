# Quick start: your first experiment

Start in the browser. Local installation is a separate, optional route for reproducible computational runs.

[Deutsch](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/quick-start.md) · [Wiki overview](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/)

Source snapshot: 2026-10-28 · `0ea645c9381979a55bc943f5f5ce1dcc4d39b6ca`

## Five minutes in the Signal Lab

1. Open the Signal Validation Lab and select English if needed.
2. Keep the defaults and run the test.
3. Compare identity, moving average, FFT low-pass and X6 phase filter. They all receive the same input.
4. Look at the reference and output together, then read the error value and individual criteria.
5. Change only the noise level and run again. This makes the effect of that change easier to identify.
6. Run the counterexample checks. A passing counterexample means the expected fault was detected.
7. Export the JSON evidence report. Import it again using the report replay option and recompute it.

Not every result needs to show PASS. A correctly executed experiment may demonstrate that a filter makes the signal worse. JSON preserves the full evidence report; CSV contains time series for further analysis.

- [Open Signal Validation Lab](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/signal-lab.html)
- [Detailed operation guide (German)](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/SIGNAL_VALIDATION_LAB.md)

## Run locally

The documented local qualification uses Linux/POSIX on x86-64, Python 3.12, Git and Node.js 22 or later. That report does not automatically cover other platforms. Run these commands in a new project directory.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-wiki-start
cd x6-wiki-start
python3 x6.py setup --profile research
python3 x6.py doctor --profile research
python3 x6.py serve
```

Open the local address printed by the command. Press Ctrl+C to stop the server. If the port is busy, use python3 x6.py serve --port 8001. For an exact reproduction, check out the source commit stated in the relevant module report; main continues to change.

- [Installation and integration guide (German)](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/INTEGRATION.md)

## Run and verify an experiment

```sh
python3 x6.py run signal --output runs/wiki-signal-001
python3 x6.py verify runs/wiki-signal-001
python3 x6.py export runs/wiki-signal-001 --output exports/wiki-signal-001.zip
python3 x6.py verify exports/wiki-signal-001.zip
```

Use a new output name for the next run. verify checks more than file hashes: it recomputes the prescribed results. A successful export does not change the scientific verdict on the filter.

Getting started requires neither a new Wolfram query nor laboratory equipment. The separately documented offline reference suite uses Python 3.12 and Node.js 24.

- [Offline reference suite](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/OFFLINE_REFERENCE.md)
