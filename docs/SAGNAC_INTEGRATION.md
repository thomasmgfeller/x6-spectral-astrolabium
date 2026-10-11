# X6 Sagnac integration 0.1 — experimental research preview

Base: X6 public research preview, commit
`e1c701c85a326917c6224d5977311fdba25a3a98` (X6 v4.2 RC).
The added module has its own version 0.1. Existing scientific modules and
scheduled research workflows are unchanged. The public preview is intended
for technical inspection; physical device qualification remains open.

## What is implemented

- New **07 · Sagnac** tab, DE/EN/FR, with responsive layout. Browser and
  mobile-viewport checks run in the X6 Validation workflow; inspect the
  result for the exact commit. No physical phone qualification is claimed.
- Offline synthetic example and binary `.bin` import, SGNCv007 only.
- Exact uint64 decoding using JavaScript BigInt. Decimal strings are retained
  for all counts and times; derived ratios use floating-point arithmetic.
- CRC32, version, reserved field, sequence continuity, acquisition flags and
  trial/click/repeat/multiport accounting checks. Invalid input clears previous
  displayed results and blocks export. No silent frame repair or resync.
- Separate conditional and all-trial CHSH statistics for exactly four distinct
  settings with matching calibration ID and window width. The alpha=0.0027
  Hoeffding calculation is compared to the original Python implementation.
- SHA-256-bound evidence export including the unmodified binary input, source
  declaration, sequences, calibration IDs and assumptions. Hashes and CRC are
  NOT authentication or physical validation.
- Loopback-only Python standard-library bridge: immutable file replay or an
  explicitly selected Linux serial device. Finite capture only, not continuous
  acquisition. Raw bytes are saved incrementally, including timeout/cancellation.

## Quick start — no hardware required

From the repository root:

```bash
python3 device/sagnac_bridge.py
```

Open `http://127.0.0.1:8766/app/`, select **07 · Sagnac**, then read the local
bridge or load the synthetic example. The bridge defaults to the labelled
synthetic fixture. It does not probe or open a physical device by default.

Alternatively open `app/index.html` directly. Keep `sagnac-core.js` and
`sagnac-ui.js` beside it. File replay and the embedded example work offline;
the local-service button requires the bridge's HTTP address.

## Existing captured data

Only binary snapshot frames are accepted by this new module. The JSON output
of other tools is not silently trusted as CRC-verified input.

```bash
python3 device/sagnac_bridge.py --capture capture.bin --origin hardware --first-sequence 100
```

The origin and first sequence must match the actual acquisition protocol.
`hardware` is an operator declaration, not proof that data came from photons.
Use `synthetic` for electrical/software tests. The file is read once when the
bridge starts; browser polling is a status refresh, not a new measurement.

## Linux UART — prepared, not physically qualified

After the board, voltage levels, sender and serial port are separately verified:

```bash
python3 device/sagnac_bridge.py --device /dev/serial/by-id/YOUR_VERIFIED_ADAPTER --origin hardware --first-sequence 100 --frames 4 --baud 1000000 --timeout 120 --raw new_capture.bin
```

Replace the path. The target raw file must not already exist. The bridge does
not start the FPGA, configure GPIO, reset the board or move optics. v0.7 sends
one frame per run/reset; assembling four settings still requires the external
acquisition procedure. On timeout, partial input remains saved and is invalid.
Ctrl-C stops the receiver; already received bytes remain in the raw file.
Re-run explicitly for another capture. UART transport carries snapshots, not
per-photon raw time tags. Electrical compatibility remains untested here.

## Why control remains unavailable

SGNCv007 defines a snapshot output only. No actuator protocol, physically
calibrated waveplate mapping, settling-time model or confirmed board pinout
exists in this integration. Consequently the UI has no working actuator
button and the server rejects POST requests. This is an implemented data
adapter and receiver, not a completed quantum controller.

Future control needs an independently versioned command protocol with
acknowledgements and measured positions, verified actuators, bounded settings,
calibration validity, stop/timeout behaviour and a fixed evaluation protocol.
Calibration data and acceptance data must be separate. Optimize a declared
instrument objective; never select Bell-test data to maximize a result.
Slow calibration belongs on the Pi; any fast photon feed-forward needs separate
timing-qualified hardware. No simulator control is presented as physical control.

## Scientific limits

`physical_quantum_claim` remains `NOT_ASSESSED` for every source. A calibration
ID does not verify the calibration. CHSH uses a predeclared singlet sign;
conditional coincidences require fair sampling; bounds assume iid trials,
stationarity between measurement blocks and correct measurement definitions.
No loophole-free Bell claim is made. Optical angles are measurement axes, not
uncalibrated waveplate motor angles. No background subtraction, efficiency
compensation, click filtering or Fourier filtering is applied to counts.

Observed click rates refer to the acquisition durations recorded in the
frames. They are not photon-pair generation rates. The table shows the first
100 records of a larger capture; all records remain in the evidence. Captures
other than exactly four distinct settings do not produce combined CHSH.
Snapshots alone do not contain enough information to diagnose timing jitter,
afterpulsing or within-run drift. Tomography v0.8 remains a separate option;
its nine settings are not encoded by the current two-bit setting ID.

## Provenance and rights

The original X6 license status is unchanged: Apache-2.0 intended, not granted.
No new blanket license or publication permission is inferred. This addition
was created with AI assistance for the repository owner, initially for private
review and subsequently authorized for an experimental public preview.
The existing X6 rights/provenance documents retain their status.

`device/vendor/sagnac_v0_7/{analyze.py,frame_codec.py,capture_serial.py,LICENSE}`
are unchanged files from `Sagnac_v0_7_UART_Host_und_Hardwareplan.zip`, created
in this project's earlier work. Their MIT notice is retained. The receiver's
termios setup is adapted from that MIT source. Fixtures are the existing
synthetic test vectors, not lab data. No external datasets or images added.

## Verification

```bash
node tests/sagnac/test_core.cjs
python3 -m unittest discover -s tests/sagnac -p 'test_*.py' -v
# Install the pinned browser test dependency in a local development directory:
npm install --prefix .venv/sagnac-browser --no-save --no-package-lock playwright@1.62.1
node .venv/sagnac-browser/node_modules/playwright/cli.js install chromium
export NODE_PATH="$PWD/.venv/sagnac-browser/node_modules"
node tests/sagnac/browser_test.cjs
```

The historical private-build checks are retained unchanged in
`evidence/sagnac_integration_validation.json`; they are not a claim about a
later commit. For the public preview, use the X6 Validation checks and its
`x6-sagnac-evidence` artifact attached to the specific commit. CI runs only on
relevant pull requests or manual dispatch, with a 10-minute Sagnac job limit
and seven-day evidence retention; it does not schedule hardware acquisition.
Browser screenshots used during development are internal QA, not experimental
evidence. Physical UART, detector, optical and actuator tests remain NOT_EXECUTED.
