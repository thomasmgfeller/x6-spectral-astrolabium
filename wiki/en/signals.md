# Understanding signals and filters

A smoother curve is not automatically a better measurement. What matters is whether the important information survives.

[Deutsch](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/signals.md) · [Wiki overview](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/)

Source snapshot: 2026-10-19 · `aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb`

## From a signal to a spectrum

A signal is a sequence of values over time, such as a measured vibration. A spectrum shows which frequency components it contains. Fourier decomposition describes the signal using oscillating building blocks.

Amplitude describes the strength of a component. Phase describes its position within an oscillation cycle. A power spectrum alone therefore does not contain everything needed to reconstruct the original time series.

## Four methods, the same input

| Method | What it does | What to watch for |
| --- | --- | --- |
| Identity | Leaves the input unchanged. | A reference for the unfiltered condition. |
| Moving average | Averages neighbouring samples. | Can weaken short impulses and amplitude. |
| FFT low-pass | Removes components above a cutoff frequency. | May remove useful high frequencies; boundary artefacts are possible. |
| X6 phase filter | Selects Fourier components by their angle. | Is not an ordinary low-pass filter and can remove a clean target signal. |

These comparisons operate on complete stored signals. The centred moving average also uses later samples, so this implementation is not a directly causal real-time filter. A good offline plot does not establish suitability for fast machine control.

## Which numbers help?

| Metric | Plain-language meaning |
| --- | --- |
| RMSE | A typical error on the signal’s scale; usually smaller is better for the same target. |
| NRMSE | Error relative to the specified reference norm; the precise definition matters. |
| PSD | How signal power is distributed across frequencies. |
| Coherence | Frequency-dependent linear agreement; not a reconstruction guarantee by itself. |
| Phase and delay | Whether oscillations line up and whether an output arrives earlier or later. |

A useful counterexample is y = −x: the curve is inverted. Its power spectrum is unchanged, and magnitude-squared coherence can be one. The original signal is still not reconstructed correctly. This is why X6 checks several criteria together.

## Make the experiment informative

- Initially change one parameter at a time.
- Compare every method against the same known reference.
- Check short events and phase alignment as well as noise.
- Keep the seed, settings, raw data and evidence report together.
- Use new tests before transferring a synthetic result to real sensors.

- [Signal Lab](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/signal-lab.html)
- [Metric definitions and limits (German)](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/SIGNAL_LAB_METHODS.md)
- [Polarity-inversion countercheck](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/signal-lab/wolfram-polarity-v0.1/README.md)
