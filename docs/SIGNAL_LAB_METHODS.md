# Signal Validation Lab: methods, numerical evidence, and limits

The Signal Validation Lab evaluates finite, synthetic, real-valued sample arrays
against a known clean reference. It makes an engineering comparison between an
unfiltered observation, a moving average, an FFT low-pass, and the existing X6
Fourier phase filter. A result is conditional on the declared signal, distortion,
filter, and acceptance parameters. It is not a physical experiment or a quantum
coherence measurement.

## Reproduce the independent validation

From the repository root, with Python and Node installed:

```sh
python -m pip install -r tests/signal-lab/requirements.txt
python tests/signal-lab/reference_validation.py
python tests/signal-lab/reference_validation.py --report /tmp/signal-lab-reference-report.json
```

The requirements pin the NumPy and SciPy versions used for this check. The report
records the actual Python, NumPy, SciPy, and Node versions, the core SHA-256, the
application SHA-256, the extracted original filter SHA-256, and the oracle SHA-256.
The optional report contains bounded check summaries rather than sample arrays;
the process exits unsuccessfully if any numerical comparison fails. Running the
command without `--report` does not write a report.

`reference_fixture.cjs` is a transport adapter. It calls the public JavaScript
core and extracts the original `fft`, `transform`, and `filter` functions directly
from `signalFrame.srcdoc` in `app/index.html`. It runs that unchanged filter in a
separate Node VM on the exact observed samples. This verifies compatibility with
the original X6 algorithm without treating the new implementation as its own
reference. It does not execute the application's browser UI.

The scientific oracle is independently implemented in Python using NumPy
convolution/FFT and SciPy `welch`, `csd`, `coherence`, `chirp`, and `correlate`.
It does not translate the JavaScript FFT or Welch implementation. Fixed analytic
cases test sign, scale, undefined values, and identification limits. This is
floating-point numerical validation, not formal proof or interval arithmetic.

## Signal and distortion model

Samples are taken at `t[n] = n / sampleRate` for `n = 0, ..., N-1`. The clean
reference uses zero phase and the selected nominal amplitude. The waveform
families are:

| Family | Clean reference |
| --- | --- |
| Sine | `A sin(2 pi f t)` |
| Multitone | `A / 1.75 * [sin(2 pi f t) + 0.5 sin(2 pi 1.75 f t) + 0.25 sin(2 pi 2.5 f t)]` |
| Linear chirp | `A sin(2 pi [f t + 0.5 (1.5 f / T) t^2])`, with `T = N / sampleRate` |
| Gaussian pulse | `A exp(-0.5 [(t - 0.5 T) / (0.035 T)]^2)` |
| Zero | All samples zero |

The observation is generated in this order:

1. Apply the configured phase offset to the oscillatory waveform.
2. Multiply by the gain.
3. Apply the integer sample delay, filling the exposed boundary with zeros.
4. Add the seeded pseudorandom noise with the configured standard-deviation scale.
5. Apply symmetric hard clipping when the clipping level is positive.
6. Apply signed uniform quantization when the bit count is positive.

The seed makes a run reproducible; it does not turn one realization into a
confidence interval or establish a real sensor's noise distribution. A constant
phase added to every multitone component differs from a time delay, whose phase
change is proportional to frequency. Pulse and zero waveforms have no oscillatory
phase parameter.

For `b` quantizer bits and half-range `R`, the step is `delta = 2 R / 2^b`.
The integer code is `floor(y / delta + 0.5)`, clipped to
`[-2^(b-1), 2^(b-1)-1]`, and the output equals `delta * code`. Thus the upper
endpoint is `R - delta`, the lower endpoint is `-R`, and ties round toward the
positive code. NumPy's ties-to-even rounding is a different operation. Clipping
precedes quantization; rounding can move a sample slightly beyond the preceding
clipping level while respecting the quantizer's own range.

## Compared filters

All four methods receive the same generated observation. Comparisons use their
actual output arrays and the same untouched clean reference.

| Method | Definition and boundary convention |
| --- | --- |
| Identity | Return the observation unchanged. |
| Moving average | Centered odd-width mean; truncate and renormalize the averaging window at both boundaries. |
| FFT low-pass | Transform the complete record; set bins above `cutoffHz` to zero, retain DC and bins at the cutoff, and invert. |
| X6 phase | Original conjugate-pair-preserving Fourier phase selection; the phase of the positive-frequency coefficient determines whether to retain the pair. DC and Nyquist are handled as real coefficients. |

The centered moving average uses future samples and is an offline baseline.
The FFT low-pass uses the finite record's periodic extension; it is not a causal
streaming implementation. Their boundary behavior can affect raw fidelity.
The X6 filter selects phases, not frequency bands. It depends on the time origin
and need not preserve an arbitrary waveform or improve its signal-to-error ratio.
Pass and stop outputs should sum to the original observation, within roundoff,
when evaluated on the same samples and selection settings.

## Time-domain errors

Let `x` denote the known reference, `y` the candidate output, and
`e = y - x`. The primary comparisons use the original sample alignment. The lab
does not remove a fitted gain, offset, or delay before computing them.

| Metric | Definition |
| --- | --- |
| RMSE | `sqrt(mean(e^2))`, in the input's amplitude units |
| NRMSE | `sqrt(sum(e^2) / sum(x^2))`, dimensionless |
| RMS gain error | `100 * [sqrt(sum(y^2) / sum(x^2)) - 1]`, percent |
| Signal-to-error ratio | `10 log10(sum(x^2) / sum(e^2))`, dB |

The RMS gain error includes DC and does not recover polarity. It is not a fitted
transfer-function gain. For nonzero reference energy and exact equality, the
signal-to-error ratio has an infinite mathematical limit; its JSON value is
`null` with status `EXACT_MATCH`. For a zero-energy reference, normalized errors,
gain error, and the ratio are `UNDEFINED`, including the all-zero pair. RMSE itself
remains defined. Numeric `null` always has an explanatory status and reason.
The implementation evaluates these formulas using scaled vector norms, and
computes the logarithmic ratio as a difference of logarithms. This preserves
small but representable nonzero errors that a direct sum of squared samples
could underflow to zero. The independent oracle uses SciPy's vector norm.

## Welch power, cross phase, and coherence

The reference and output spectra use identical, explicit settings:

- Segment length `L = min(256, N / 2)` for the supported even sample counts.
- Periodic Hann window `w[n] = 0.5 - 0.5 cos(2 pi n / L)`.
- Half-segment overlap, FFT length `L`, and no additional zero padding.
- Remove the mean separately from each segment before windowing.
- Arithmetic mean of segment periodograms.
- One-sided density normalization by `sampleRate * sum(w^2)`; double positive
  interior bins, while retaining the undoubled DC and Nyquist bins.

These choices are passed explicitly to SciPy, including an explicit window
array, rather than relying on defaults that may vary with a library release.
SciPy's documentation specifies these estimator parameters and density scaling
([Welch documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html)).
PSD units are amplitude squared per Hz; they become V squared per Hz only when
the input has a justified calibration in volts.

The cross spectrum is `Pxy = mean(conj(X) * Y)` with the same normalization.
Cross phase is `arg(Pxy)` in degrees, wrapped to a full turn around zero. This
matches the [SciPy CSD convention](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.csd.html).
Consequently, a positive output delay contributes a negative phase slope with
frequency. Phase advance and time delay are distinct controls.

Magnitude-squared coherence is `abs(Pxy)^2 / (Pxx * Pyy)`, following the
[SciPy coherence definition](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.coherence.html).
It describes linear frequency-domain association under the estimator assumptions.
It is neither quantum coherence nor a fidelity measure. In particular, `y = -x`
has identical PSD and coherence one while its NRMSE is two. The regression suite
requires that this case fail the fidelity criteria.

The relative spectral error is `sum(abs(Pyy - Pxx)) / sum(Pxx)`. The common bin
spacing cancels. This is an L1 error of estimated power density, not a phase
metric. Segment-mean subtraction makes PSD insensitive to a constant offset;
the raw RMSE/NRMSE therefore remain necessary. The validation includes a DC-offset
case that must fail despite its matching detrended spectrum.

### Powered bins and phase identifiability

Individual coherence and phase values require all four strict inequalities:

```text
Pxx[k] > 1e-12 * peak(Pxx)
Pyy[k] > 1e-12 * peak(Pyy)
Pxx[k] > 1e-24 * max(peak(Pxx), peak(Pyy))
Pyy[k] > 1e-24 * max(peak(Pxx), peak(Pyy))
```

The first two rules reject weak bins within each spectrum. The latter two are
a declared diagnostic dynamic-range limit between the two signals. They prevent
normalizing a nearly removed component's residual floating-point error into an
apparently precise coherence or phase result. The configured ratio, actual
pairwise peak, resulting minimum power, and actual peak-power ratio are retained
in `spectrum.numericalGuard`. Undefined bins carry `null`; zero power is not
assigned coherence one or phase zero. Cross phase also requires a nonzero cross
spectrum.

This is a software eligibility policy, not a measured noise floor, confidence
bound, or evidence of decoherence. A mathematically coherent signal attenuated
below the relative range can therefore have an undefined lab diagnostic. Its
raw waveform, PSD, cross spectrum, and reconstruction errors remain available
and unchanged. Multiplying both signals by the same positive factor preserves
this relative rule while their powers remain numerically representable. A small
absolute amplitude alone is not grounds for rejecting the diagnostic.

For eligible bins, coherence is evaluated equivalently as
`[hypot(Re(Pxy), Im(Pxy)) / (sqrt(Pxx) * sqrt(Pyy))]^2`, bounded to `[0, 1]` for
roundoff. This avoids prematurely underflowing the product `Pxx * Pyy` for two
equally small signals. In the independent oracle, SciPy coherence is computed
on independently, positively rescaled copies of the input arrays; this
mathematically preserves coherence. Raw SciPy PSD and CSD are still computed and
compared in the original scale. Neither procedure is a universal guarantee
outside representable floating-point ranges.

Aggregate coherence uses positive-frequency reference bins at or above `0.001`
of the reference PSD peak, weighted by reference PSD. Aggregate phase error is
the weighted RMS wrapped phase, relative to expected phase zero, among those
bins whose coherence reaches `phaseCoherenceMin` (default `0.8`). Missing active
weight yields `PARTIAL`; no usable bins yields `UNDEFINED`. A selected subset
cannot silently stand for complete phase preservation.

The phase error does not subtract the estimated delay. Sparse spectra, leakage,
nonstationarity, short records, and poor coherence limit interpretation. Welch
segment averaging avoids the identically-one coherence of a single raw
periodogram, but these finite records do not provide automatic confidence bands.

## Delay estimate and ambiguity

For integer lag `l`, correlate the overlapping samples `x[i]` and `y[i+l]`,
subtracting their separate overlap means and normalizing by their overlap
standard deviations. Search `|l| <= min(64, N / 4)`, which keeps at least 75% of
the samples. Positive lag means that the output is delayed. Maximize absolute
correlation so that a polarity inversion does not falsely become half a period
of delay.

Before searching, the smaller centered full-record norm divided by the larger
must strictly exceed `1e-12`. The same relative-norm requirement applies to each
lag's overlapping pair. Zero variance or an insufficient norm ratio makes that
correlation unavailable; if the full-record ratio is insufficient, all lag
correlations are `null`. The actual ratio and declared limit are retained in
`delay.numericalGuard`. As with the PSD rule, this is a diagnostic eligibility
limit, including a deliberate limit on very strong genuine attenuation. The
calculation normalizes each centered sample by its own overlap norm before
forming the dot product, so a common small scale does not itself prevent a
delay estimate.

The estimate is also `UNDEFINED` when maximum absolute correlation is below
`0.2`. It is `AMBIGUOUS` when a competing local maximum more than one sample
away lies within `0.01` of the best absolute correlation, or when the best lag
lies at a search boundary. These are declared engineering identification rules,
not statistical confidence intervals. A pure periodic signal may have several
equally plausible lags even when it exactly matches its reference. Delay
diagnostics retain candidate information, while the identifiable metric value
is `null` for an ambiguous result.

For displaying a best candidate, peaks within `1e-12` of the largest absolute
correlation are treated as a numerical tie: choose the smallest absolute lag,
then the smaller signed lag. This stabilizes a periodic signal's diagnostic
candidate across floating-point implementations. It does not remove competing
peaks, widen the `0.01` ambiguity margin, or turn an ambiguous delay into an
identified one. The complete raw correlation array and maximum score remain
available.

The independent oracle uses `scipy.signal.correlate` for all dot products and
prefix-sum overlap moments for Pearson normalization. It first removes a
constant offset and positively rescales each input, both invariances of Pearson
correlation, to avoid underflow in the independent computation. Eligibility
still uses the signals' original relative norm scale. Injected positive and
negative delays verify the sign convention separately from phase. Periodic and
constant cases verify that missing identification cannot become a passing gate.

## Acceptance interpretation

Default tolerances are NRMSE at most `0.25`, absolute RMS gain error at most
`10%`, phase error at most `10 degrees`, absolute identifiable delay at most
`1 sample`, relative spectral error at most `0.2`, and aggregate coherence at
least `0.9`. These are editable engineering criteria for the selected task, not
universal limits, p-values, or evidence of quantum behavior. They must be kept
with the result so that changing a criterion is visible.

Metric statuses distinguish `DEFINED`, `EXACT_MATCH`, `UNDEFINED`, `PARTIAL`, and
`AMBIGUOUS`. The analysis distinguishes `PASS`, `FAIL`, and `INCONCLUSIVE`.
An unavailable required metric cannot be converted to a passing measurement.
Several metrics share the same samples and are correlated; their agreement is
not a set of independent statistical confirmations. There is no automatic
claim that any candidate filter is better than the identity baseline.

## Scope of the independent tests

The fixed suite covers clean and noisy multitone signals, sine gain/phase/delay,
a chirp, a Gaussian pulse, zero input, hard clipping, quantizer saturation,
clipping-before-quantization order, short Welch records, the Nyquist cutoff,
seed reproducibility, and complementary X6 pass/stop filters. Direct evaluation
fixtures additionally test polarity inversion, positive/negative phase and delay,
periodic ambiguity, constant input, DC offset, and independent noise arrays.
Dynamic-range controls include genuine attenuation by `1e-8` and `1e-11`, which
retains usable coherence and delay on the broadband fixtures; a contrast of
`1e-13` in either direction, which must leave normalized diagnostics undefined;
and a common `1e-100` amplitude factor, which must preserve normalized results
for identity, gain change, and a seven-sample delay. A clean sine rejected by
the X6 phase filter must retain its raw roundoff residual while withholding
normalized phase, coherence, and delay claims.

Array checks use `rtol = 2e-10`, `atol = 2e-12`; PSD checks use `rtol = 2e-9`,
`atol = 2e-12`; ordinary scalar comparisons use `rtol = 2e-9`, `atol = 2e-11`.
Cross-phase tolerance is `2e-6 degrees` and coherence absolute tolerance is
`2e-8` on comfortably powered bins. Near-zero spectral bins are deliberately
not treated as precise phase measurements. An additional spectral comparison
divides each PSD by its own oracle peak, and each CSD component by
`sqrt(peak(Pxx)) * sqrt(peak(Pyy))`, applying the same spectral tolerances there.
This makes the tiny-signal checks substantive: substituting zero arrays cannot
pass merely because the ordinary absolute tolerance exceeds their power.
Nonzero RMSE is also checked relative to its independent value. These bounds
accommodate double-precision FFT roundoff on the fixed fixtures; they do not
certify arbitrary magnitude ranges or every possible parameter combination.

Passing the oracle demonstrates consistency on the tested arrays and declared
definitions. It does not replace browser tests, validate an external device,
provide an empirical noise model, or establish a physical mechanism. Synthetic
sample time is a simulation coordinate; the implementation does not control
experimental hardware.
