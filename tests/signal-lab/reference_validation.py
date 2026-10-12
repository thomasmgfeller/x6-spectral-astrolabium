#!/usr/bin/env python3
"""Independent, deterministic numerical oracle for the Signal Validation Lab.

Uses NumPy FFT/convolution and SciPy Welch/CSD/coherence/correlation. It does not
translate the JavaScript FFT or spectral estimator. The Node fixture transports
public-API results and separately runs the filter extracted from the original
application. Optional reports contain checks and hashes, not sample arrays.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import warnings

import numpy as np
import scipy
from scipy import linalg, signal

ROOT = Path(__file__).resolve().parents[2]
METHODS = ("identity", "moving_average", "fft_lowpass", "x6_phase")
ARRAY_RTOL = 2e-10
ARRAY_ATOL = 2e-12
PSD_RTOL = 2e-9
PSD_ATOL = 2e-12
SCALAR_RTOL = 2e-9
SCALAR_ATOL = 2e-11
PHASE_ATOL_DEG = 2e-6
COHERENCE_ATOL = 2e-8
INDIVIDUAL_PSD_RATIO = 1e-12
PAIRWISE_PSD_RATIO = 1e-24
CENTERED_NORM_RATIO = 1e-12


class Validation:
    def __init__(self) -> None:
        self.checks: list[dict] = []

    def check(self, name, callback) -> None:
        try:
            detail = callback()
            self.checks.append({"name": name, "status": "PASS", **(detail or {})})
        except Exception as exc:  # Collect independent failures, then exit nonzero.
            self.checks.append({"name": name, "status": "FAIL",
                                "error": f"{type(exc).__name__}: {exc}"[:1800]})


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def close(actual, expected, *, rtol=SCALAR_RTOL, atol=SCALAR_ATOL):
    actual, expected = np.asarray(actual, dtype=float), np.asarray(expected, dtype=float)
    require(actual.shape == expected.shape, f"Shape mismatch: {actual.shape} vs {expected.shape}")
    require(np.isfinite(actual).all(), "Unexpected nonfinite numerical output")
    np.testing.assert_allclose(actual, expected, rtol=rtol, atol=atol)
    return float(np.max(np.abs(actual - expected), initial=0.0))


def array_close(actual, expected):
    return close(actual, expected, rtol=ARRAY_RTOL, atol=ARRAY_ATOL)


def stable_norm(values):
    """SciPy's BLAS-backed vector norm preserves small, nonzero magnitudes."""
    return float(linalg.norm(np.asarray(values, dtype=float)))


def centered_values(values):
    # Translation before SciPy detrending preserves decimal constants exactly;
    # Pearson correlation is unchanged by either translation.
    shifted = np.asarray(values, dtype=float) - values[0]
    return signal.detrend(shifted, type="constant")


def centered_norm_ratio(reference, output):
    norms = (stable_norm(centered_values(reference)), stable_norm(centered_values(output)))
    return min(norms) / max(norms) if max(norms) else None


def powered_bin_mask(pxx, pyy):
    xpeak, ypeak = np.max(pxx, initial=0), np.max(pyy, initial=0)
    pair_floor = max(xpeak, ypeak) * PAIRWISE_PSD_RATIO
    return ((pxx > xpeak * INDIVIDUAL_PSD_RATIO)
            & (pyy > ypeak * INDIVIDUAL_PSD_RATIO)
            & (pxx > pair_floor) & (pyy > pair_floor))


def metric(analysis, name, *, defined=True):
    item = analysis["metrics"][name]
    for field in ("value", "status", "reason", "unit"):
        require(field in item, f"Metric {name} omits {field}")
    if defined:
        require(item["status"] == "DEFINED", f"{name}: expected DEFINED, got {item}")
        require(item["value"] is not None, f"{name}: DEFINED without a value")
    return item


def shift_zero(values, lag):
    n = len(values)
    out = np.zeros(n)
    if lag >= 0:
        out[lag:] = values[:n - lag]
    else:
        out[:n + lag] = values[-lag:]
    return out


def waveform(params, phase_deg=0.0):
    n, fs = params["samples"], params["sampleRate"]
    t = np.arange(n, dtype=float) / fs
    phase = np.deg2rad(phase_deg)
    freq, amplitude = params["frequency"], params["amplitude"]
    kind = params["signal"]
    if kind == "sine":
        values = amplitude * np.sin(2 * np.pi * freq * t + phase)
    elif kind == "multitone":
        values = amplitude / 1.75 * sum(weight * np.sin(2 * np.pi * factor * freq * t + phase)
                                         for weight, factor in ((1, 1), (.5, 1.75), (.25, 2.5)))
    elif kind == "chirp":
        duration = n / fs
        values = amplitude * signal.chirp(t, f0=freq, t1=duration, f1=2.5 * freq,
                                           method="linear", phi=phase_deg - 90)
    elif kind == "pulse":
        duration = n / fs
        values = amplitude * np.exp(-.5 * ((t - .5 * duration) / (.035 * duration)) ** 2)
    elif kind == "zero":
        values = np.zeros(n)
    else:
        raise AssertionError(f"Unknown waveform contract: {kind}")
    return t, values


def noiseless_pipeline(params):
    _, transformed = waveform(params, params["phaseDeg"])
    values = shift_zero(params["gain"] * transformed, params["delaySamples"])
    if params["clipLevel"]:
        values = np.clip(values, -params["clipLevel"], params["clipLevel"])
    if params["quantBits"]:
        levels = 2 ** params["quantBits"]
        step = 2 * params["quantRange"] / levels
        # Nearest quantizer with the documented tie-to-positive rule. np.round
        # uses ties-to-even and would be a different quantizer.
        codes = np.floor(values / step + .5)
        values = np.clip(codes, -levels // 2, levels // 2 - 1) * step
    return values


def welch_reference(reference, output, fs):
    nperseg = min(256, len(reference) // 2)
    window = signal.windows.hann(nperseg, sym=False)
    kwargs = dict(fs=fs, window=window, nperseg=nperseg,
                  noverlap=nperseg // 2, nfft=nperseg, detrend="constant")
    f, pxx = signal.welch(reference, **kwargs, return_onesided=True,
                          scaling="density", average="mean")
    _, pyy = signal.welch(output, **kwargs, return_onesided=True,
                          scaling="density", average="mean")
    _, pxy = signal.csd(reference, output, **kwargs, return_onesided=True,
                        scaling="density", average="mean")
    # Positive independent rescaling leaves mathematical coherence unchanged.
    # scipy.signal.coherence otherwise forms Pxx*Pyy and can underflow for two
    # equally tiny, perfectly usable inputs. Raw PSD and CSD stay unscaled above.
    xscale, yscale = np.max(np.abs(reference)), np.max(np.abs(output))
    normalized_x = reference / xscale if xscale else reference
    normalized_y = output / yscale if yscale else output
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        _, coh = signal.coherence(normalized_x, normalized_y, **kwargs)
    return dict(f=f, pxx=pxx, pyy=pyy, pxy=pxy, coherence=coh,
                phase=np.angle(pxy, deg=True), nperseg=nperseg)


def delay_reference(reference, output):
    """Overlap Pearson correlation, using SciPy correlation and prefix sums.

    This oracle computes all dot products independently with SciPy's FFT path,
    rather than copying the core's per-lag, per-sample implementation.
    """
    n = len(reference)
    bound = min(64, n // 4)
    lags = np.arange(-bound, bound + 1)
    norm_ratio = centered_norm_ratio(reference, output)
    if norm_ratio is None or norm_ratio <= CENTERED_NORM_RATIO:
        return lags, np.full(len(lags), np.nan)
    # Correlation is invariant to independent positive rescaling and constant
    # offsets. Apply both before SciPy FFT correlation/prefix moments to avoid
    # multiplying tiny norms or subtracting a large DC term from small variance.
    reference, output = centered_values(reference), centered_values(output)
    xscale, yscale = np.max(np.abs(reference)), np.max(np.abs(output))
    reference, output = reference / xscale, output / yscale
    dots = signal.correlate(output, reference, mode="full", method="fft")[n - 1 + lags]
    x0, x1 = np.maximum(0, -lags), np.minimum(n, n - lags)
    y0, y1 = np.maximum(0, lags), np.minimum(n, n + lags)
    count = n - np.abs(lags)
    prefix = lambda a: np.r_[0., np.cumsum(a)]
    px, py, px2, py2 = map(prefix, (reference, output, reference ** 2, output ** 2))
    sx, sy = px[x1] - px[x0], py[y1] - py[y0]
    vx, vy = px2[x1] - px2[x0] - sx * sx / count, py2[y1] - py2[y0] - sy * sy / count
    covariance = dots - sx * sy / count
    with np.errstate(divide="ignore", invalid="ignore"):
        correlation = covariance / np.sqrt(np.maximum(0, vx) * np.maximum(0, vy))
    # Recover the original relative norm scale only for the declared eligibility
    # decision. These overlap energies come from independent prefix moments.
    overlap_x, overlap_y = np.sqrt(np.maximum(0, vx)) * xscale, np.sqrt(np.maximum(0, vy)) * yscale
    with np.errstate(divide="ignore", invalid="ignore"):
        overlap_ratio = np.minimum(overlap_x, overlap_y) / np.maximum(overlap_x, overlap_y)
    correlation[~(overlap_ratio > CENTERED_NORM_RATIO)] = np.nan
    return lags, correlation


def compare_spectrum(analysis, reference, output, fs):
    oracle = welch_reference(reference, output, fs)
    actual = analysis["spectrum"]
    close(actual["frequencies"], oracle["f"], atol=1e-12)
    pxx_error = close(actual["referencePSD"], oracle["pxx"], rtol=PSD_RTOL, atol=PSD_ATOL)
    pyy_error = close(actual["outputPSD"], oracle["pyy"], rtol=PSD_RTOL, atol=PSD_ATOL)
    cross_real_error = close(actual["crossSpectrumReal"], oracle["pxy"].real, rtol=PSD_RTOL, atol=PSD_ATOL)
    cross_imag_error = close(actual["crossSpectrumImag"], oracle["pxy"].imag, rtol=PSD_RTOL, atol=PSD_ATOL)
    xpeak, ypeak = oracle["pxx"].max(initial=0), oracle["pyy"].max(initial=0)
    # The ordinary absolute tolerance alone would let an all-zero implementation
    # pass tiny fixtures. Also compare each spectrum in its own power scale;
    # CSD's scale is sqrt(peak Pxx)*sqrt(peak Pyy), shared by real/imaginary parts.
    scaled_errors = []
    for key, expected, scale, usable in (
            ("referencePSD", oracle["pxx"], xpeak, np.ptp(reference) > 0),
            ("outputPSD", oracle["pyy"], ypeak, np.ptp(output) > 0),
            ("crossSpectrumReal", oracle["pxy"].real, np.sqrt(xpeak) * np.sqrt(ypeak),
             np.ptp(reference) > 0 and np.ptp(output) > 0),
            ("crossSpectrumImag", oracle["pxy"].imag, np.sqrt(xpeak) * np.sqrt(ypeak),
             np.ptp(reference) > 0 and np.ptp(output) > 0)):
        if usable and scale > 0:
            scaled_errors.append(close(np.asarray(actual[key]) / scale, expected / scale,
                                       rtol=PSD_RTOL, atol=PSD_ATOL))
    actual_x, actual_y = np.asarray(actual["referencePSD"]), np.asarray(actual["outputPSD"])
    actual_eligible = powered_bin_mask(actual_x, actual_y)
    for k in np.flatnonzero(~actual_eligible):
        require(actual["coherence"][k] is None and actual["phaseDeg"][k] is None,
                f"Bin {k} violates the declared PSD eligibility rule")
    guard = actual["numericalGuard"]
    require(guard["pairwisePeakFloorRatio"] == PAIRWISE_PSD_RATIO,
            "Pairwise PSD guard must be explicit and fixed")
    pair_peak = max(float(actual_x.max()), float(actual_y.max()))
    close(guard["pairwisePeakPower"], pair_peak, rtol=1e-14, atol=0)
    close(guard["minimumPSD"], pair_peak * PAIRWISE_PSD_RATIO, rtol=1e-14, atol=0)
    if pair_peak:
        close(guard["peakPowerRatio"], min(float(actual_x.max()), float(actual_y.max())) / pair_peak,
              rtol=1e-14, atol=0)
    else:
        require(guard["peakPowerRatio"] is None, "Zero pair has no power ratio")
    # Cross phase and normalized coherence are ill-conditioned at numerical
    # zero power. Compare every comfortably energetic bin, including DC/Nyquist
    # where a defined result is present, and separately enforce nulls at zero.
    reliable = ((oracle["pxx"] > xpeak * 1e-8) & (oracle["pyy"] > ypeak * 1e-8)
                & powered_bin_mask(oracle["pxx"], oracle["pyy"]))
    if np.ptp(reference) == 0 or np.ptp(output) == 0:
        # Decimal constants such as 0.1 can leave sub-roundoff PSD after SciPy's
        # segment mean subtraction. They have no AC signal or identifiable phase.
        reliable[:] = False
        require(all(v is None for v in actual["coherence"]), "Constant signal acquired spurious coherence")
        require(all(v is None for v in actual["phaseDeg"]), "Constant signal acquired spurious phase")
    indexes = np.flatnonzero(reliable)
    if len(indexes):
        require(all(actual["coherence"][i] is not None for i in indexes),
                "A substantial-power bin has undefined coherence")
        require(all(actual["phaseDeg"][i] is not None for i in indexes),
                "A substantial-power bin has undefined phase")
        close([actual["coherence"][i] for i in indexes], oracle["coherence"][indexes],
              rtol=2e-8, atol=COHERENCE_ATOL)
        # Angles are compared modulo 360 degrees; -180 and +180 are equivalent.
        error = (np.asarray([actual["phaseDeg"][i] for i in indexes])
                 - oracle["phase"][indexes] + 180) % 360 - 180
        close(error, np.zeros(len(indexes)), rtol=0, atol=PHASE_ATOL_DEG)
    require(all(v is None or -1e-12 <= v <= 1 + 1e-12 for v in actual["coherence"]),
            "Magnitude-squared coherence outside [0,1]")
    return {"reference_psd_max_abs_error": pxx_error,
            "output_psd_max_abs_error": pyy_error,
            "cross_real_max_abs_error": cross_real_error,
            "cross_imag_max_abs_error": cross_imag_error,
            "scaled_spectral_max_abs_error": max(scaled_errors, default=0),
            "cross_bins_compared": len(indexes)}


def compare_metrics(analysis, reference, output, fs, acceptance):
    error_norm = stable_norm(output - reference)
    reference_norm, output_norm = stable_norm(reference), stable_norm(output)
    expected_rmse = error_norm / np.sqrt(len(reference))
    close(metric(analysis, "rmse")["value"], expected_rmse)
    if expected_rmse:
        close(metric(analysis, "rmse")["value"] / expected_rmse, 1.)
    else:
        require(metric(analysis, "rmse")["value"] == 0, "Exactly zero error must have RMSE zero")
    if reference_norm > 0:
        close(metric(analysis, "nrmse")["value"], error_norm / reference_norm)
        expected_gain = 100 * (output_norm / reference_norm - 1)
        close(metric(analysis, "gain_error_pct")["value"], expected_gain)
        if error_norm > 0:
            close(metric(analysis, "snr_db")["value"], 20 * (np.log10(reference_norm) - np.log10(error_norm)))
        else:
            exact = metric(analysis, "snr_db", defined=False)
            require(exact["value"] is None and exact["status"] == "EXACT_MATCH",
                    f"Infinite SNR limit must be explicit, got {exact}")
    else:
        for name in ("nrmse", "gain_error_pct", "snr_db"):
            item = metric(analysis, name, defined=False)
            require(item["value"] is None and item["status"] == "UNDEFINED",
                    f"Zero reference: {name} must be UNDEFINED")

    sp = welch_reference(reference, output, fs)
    total = sp["pxx"].sum()
    if np.ptp(reference) == 0:
        for name in ("spectral_error", "coherence_mean", "phase_error_deg"):
            item = metric(analysis, name, defined=False)
            require(item["value"] is None and item["status"] == "UNDEFINED",
                    f"Constant detrended reference: {name} must be UNDEFINED")
    elif total > 0:
        expected = np.abs(sp["pyy"] - sp["pxx"]).sum() / total
        close(metric(analysis, "spectral_error")["value"], expected)
        active = (sp["f"] > 0) & (sp["pxx"] >= .001 * sp["pxx"].max())
        valid = powered_bin_mask(sp["pxx"], sp["pyy"])
        if np.ptp(output) == 0:
            valid[:] = False
        eligible_coh = active & valid
        coherence_item = metric(analysis, "coherence_mean", defined=False)
        if eligible_coh.any():
            expected = np.average(np.clip(sp["coherence"][eligible_coh], 0, 1),
                                  weights=sp["pxx"][eligible_coh])
            close(coherence_item["value"], expected, atol=COHERENCE_ATOL)
        else:
            require(coherence_item["value"] is None and coherence_item["status"] == "UNDEFINED",
                    "No eligible powered bins: coherence must be UNDEFINED")
        eligible_phase = eligible_coh & (sp["coherence"] >= acceptance["phaseCoherenceMin"])
        phase_item = metric(analysis, "phase_error_deg", defined=False)
        if eligible_phase.any():
            expected = np.sqrt(np.average(sp["phase"][eligible_phase] ** 2,
                                           weights=sp["pxx"][eligible_phase]))
            close(phase_item["value"], expected, atol=PHASE_ATOL_DEG)
        else:
            require(phase_item["value"] is None and phase_item["status"] == "UNDEFINED",
                    "No coherent powered bins: aggregate phase must be UNDEFINED")
    ratio = centered_norm_ratio(reference, output)
    guard = analysis["delay"]["numericalGuard"]
    require(guard["minimumCenteredNormRatio"] == CENTERED_NORM_RATIO,
            "Delay centered-norm guard must be explicit and fixed")
    if ratio is not None:
        close(guard["centeredNormRatio"], ratio, rtol=SCALAR_RTOL, atol=0)
    else:
        require(guard["centeredNormRatio"] is None, "Two constant arrays have no centered-norm ratio")
    if ratio is None or ratio <= CENTERED_NORM_RATIO:
        item = metric(analysis, "delay_samples", defined=False)
        require(item["value"] is None and item["status"] == "UNDEFINED",
                "Delay below centered-norm eligibility floor must be UNDEFINED")
        require(all(item["correlation"] is None for item in analysis["delay"]["correlationByLag"]),
                "Globally ineligible delay must not expose unstable normalized correlations")
    return None


def build_cases():
    runs = [
        {"label": "default", "params": {}},
        {"label": "default_repeat", "params": {}},
        {"label": "different_seed", "params": {"seed": 104730}},
        {"label": "multitone_clean", "params": {"noiseStd": 0}},
        {"label": "sine_phase_removed", "params": {"signal": "sine", "frequency": 32,
          "phaseCenterDeg": 0, "phaseWidthDeg": 45, "phaseMode": "pass", "noiseStd": 0}},
        {"label": "sine_gain_phase_delay", "params": {"signal": "sine", "frequency": 29,
          "gain": 1.2, "phaseDeg": 35, "delaySamples": 7, "noiseStd": 0}},
        {"label": "sine_advance", "params": {"signal": "sine", "frequency": 23,
          "amplitude": .8, "phaseDeg": -20, "delaySamples": -5, "noiseStd": 0}},
        {"label": "chirp", "params": {"signal": "chirp", "samples": 512,
          "sampleRate": 512, "frequency": 24, "amplitude": .7, "noiseStd": 0}},
        {"label": "pulse", "params": {"signal": "pulse", "samples": 512,
          "sampleRate": 512, "frequency": 24, "amplitude": .9, "noiseStd": 0}},
        {"label": "zero", "params": {"signal": "zero", "samples": 256, "noiseStd": 0}},
        {"label": "hard_clip", "params": {"signal": "sine", "gain": 1.4,
          "phaseDeg": 17, "clipLevel": .4, "noiseStd": 0}},
        {"label": "quantize_saturate", "params": {"signal": "multitone", "gain": 1.8,
          "quantBits": 4, "quantRange": 1, "noiseStd": 0}},
        {"label": "clip_then_quantize", "params": {"signal": "sine", "gain": 1.8,
          "clipLevel": .73, "quantBits": 4, "quantRange": 1, "noiseStd": 0}},
        {"label": "lowpass_nyquist", "params": {"cutoffHz": 512}},
        {"label": "phase_stop", "params": {"phaseMode": "stop"}},
        {"label": "short128", "params": {"samples": 128, "sampleRate": 256,
          "frequency": 16, "cutoffHz": 64, "movingAverageWindow": 5}},
    ]
    rng = np.random.default_rng(20261012)
    n, fs = 1024, 1024
    t = np.arange(n) / fs
    broadband = rng.standard_normal(n)
    tone = np.sin(2 * np.pi * 32 * t)
    pulse = np.exp(-.5 * ((np.arange(n) - n / 2) / 24) ** 2)
    evaluations = []

    def add(label, reference, candidate, sample_rate=fs):
        evaluations.append(dict(label=label, reference=np.asarray(reference).tolist(),
                                candidate=np.asarray(candidate).tolist(), sampleRate=sample_rate))

    add("identity_broadband", broadband, broadband.copy())
    add("inverted_broadband", broadband, -broadband)
    add("gain20pct", broadband, 1.2 * broadband)
    add("phase_plus30", tone, np.sin(2 * np.pi * 32 * t + np.pi / 6))
    add("phase_minus30", tone, np.sin(2 * np.pi * 32 * t - np.pi / 6))
    add("delay_plus7", broadband, shift_zero(broadband, 7))
    add("delay_minus7", broadband, shift_zero(broadband, -7))
    add("pulse_delay_plus7", pulse, shift_zero(pulse, 7))
    add("periodic_ambiguity", tone, tone.copy())
    add("all_zero", np.zeros(n), np.zeros(n))
    add("zero_reference_noise", np.zeros(n), broadband)
    add("constant", np.ones(n), np.ones(n))
    add("constant_decimal", np.full(n, .1), np.full(n, .1))
    add("dc_offset", broadband, broadband + .3)
    add("decorrelated", broadband, rng.standard_normal(n))
    add("small_n128", broadband[:128], .9 * broadband[:128] + .03 * rng.standard_normal(128), 512)
    add("attenuated_above_floor_1e8", broadband, 1e-8 * broadband)
    add("attenuated_above_floor_1e11", broadband, 1e-11 * broadband)
    add("attenuated_below_floor_1e13", broadband, 1e-13 * broadband)
    add("amplified_above_contrast_limit", 1e-13 * broadband, broadband)
    add("balanced_tiny_identity", 1e-100 * broadband, 1e-100 * broadband)
    add("balanced_tiny_gain20pct", 1e-100 * broadband, 1.2e-100 * broadband)
    add("balanced_tiny_delay_plus7", 1e-100 * broadband, 1e-100 * shift_zero(broadband, 7))
    return runs, evaluations


def execute_fixture(runs, evaluations, node):
    request = json.dumps({"runs": runs, "evaluations": evaluations}, allow_nan=False)
    process = subprocess.run([node, str(Path(__file__).with_name("reference_fixture.cjs"))],
                             input=request, text=True, capture_output=True, timeout=60, cwd=ROOT)
    require(process.returncode == 0, f"Node fixture failed:\n{process.stderr[:4000]}")
    require(len(process.stdout) <= 32 * 1024 * 1024, "Fixture output exceeds the 32 MiB bound")
    return json.loads(process.stdout, parse_constant=lambda s: (_ for _ in ()).throw(
        ValueError(f"Nonstandard JSON number {s}")))


def get_analysis(run, name):
    return run["analysis"][name]


def run_validation(args):
    validation = Validation()
    run_specs, eval_specs = build_cases()
    payload = execute_fixture(run_specs, eval_specs, args.node)
    defaults = payload["defaults"]
    run_by_label = {entry["label"]: entry for entry in payload["runs"]}
    eval_by_label = {entry["label"]: entry["result"] for entry in payload["evaluations"]}
    for spec in run_specs:
        label = spec["label"]
        entry = run_by_label[label]
        result = entry["result"]
        params = {**defaults, **spec["params"]}
        arrays = result["arrays"]
        ref = np.asarray(arrays["reference"])
        obs = np.asarray(arrays["observed"])
        outputs = arrays["outputs"]

        def check_arrays(params=params, arrays=arrays, outputs=outputs, entry=entry, ref=ref, obs=obs):
            t, expected_ref = waveform(params)
            array_close(arrays["time"], t)
            array_close(ref, expected_ref)
            require(set(outputs) == set(METHODS), f"Unexpected method set: {list(outputs)}")
            if params["noiseStd"] == 0:
                array_close(obs, noiseless_pipeline(params))
            array_close(outputs["identity"], obs)
            window = np.ones(params["movingAverageWindow"])
            expected_moving = np.convolve(obs, window, mode="same") / np.convolve(np.ones(len(obs)), window, mode="same")
            array_close(outputs["moving_average"], expected_moving)
            coefficients = np.fft.rfft(obs)
            coefficients[np.fft.rfftfreq(len(obs), d=1 / params["sampleRate"]) > params["cutoffHz"]] = 0
            array_close(outputs["fft_lowpass"], np.fft.irfft(coefficients, n=len(obs)))
            max_error = array_close(outputs["x6_phase"], entry["originalX6"])
            return {"samples": len(ref), "original_x6_max_abs_error": max_error}

        validation.check(f"run/{label}/waveform_pipeline_baselines_original_x6", check_arrays)
        for method_name in METHODS:
            output = np.asarray(outputs[method_name])
            analysis = get_analysis(result, method_name)
            validation.check(f"run/{label}/{method_name}/scipy_spectrum",
                             lambda a=analysis, r=ref, y=output, p=params:
                             compare_spectrum(a, r, y, p["sampleRate"]))
            validation.check(f"run/{label}/{method_name}/metrics",
                             lambda a=analysis, r=ref, y=output, p=params:
                             compare_metrics(a, r, y, p["sampleRate"], p["acceptance"]))

    def deterministic():
        first = run_by_label["default"]["result"]
        repeat = run_by_label["default_repeat"]["result"]
        require(first == repeat, "Identical parameter/seed runs are not exactly deterministic")
        changed = run_by_label["different_seed"]["result"]
        require(first["arrays"]["observed"] != changed["arrays"]["observed"], "Changing seed leaves noisy samples unchanged")
        # Resetting the seed changes noise only; the known clean reference stays fixed.
        require(first["arrays"]["reference"] == changed["arrays"]["reference"], "Seed changed the clean reference")
        array_close(np.asarray(first["arrays"]["outputs"]["x6_phase"])
                    + np.asarray(run_by_label["phase_stop"]["result"]["arrays"]["outputs"]["x6_phase"]),
                    first["arrays"]["observed"])
        array_close(run_by_label["lowpass_nyquist"]["result"]["arrays"]["outputs"]["fft_lowpass"],
                    first["arrays"]["observed"])
    validation.check("reproducibility_seed_and_complementary_filters", deterministic)

    for spec in eval_specs:
        label = spec["label"]
        reference, output = np.asarray(spec["reference"]), np.asarray(spec["candidate"])
        analysis = eval_by_label[label]
        validation.check(f"evaluate/{label}/scipy_spectrum",
                         lambda a=analysis, r=reference, y=output, f=spec["sampleRate"]:
                         compare_spectrum(a, r, y, f))
        validation.check(f"evaluate/{label}/metrics",
                         lambda a=analysis, r=reference, y=output, f=spec["sampleRate"]:
                         compare_metrics(a, r, y, f, defaults["acceptance"]))

    def inversion_guard():
        analysis = eval_by_label["inverted_broadband"]
        close(metric(analysis, "nrmse")["value"], 2.)
        close(metric(analysis, "spectral_error")["value"], 0.)
        close(metric(analysis, "coherence_mean")["value"], 1.)
        close(metric(analysis, "phase_error_deg")["value"], 180., atol=PHASE_ATOL_DEG)
        require(analysis["status"] == "FAIL", "Perfect PSD/coherence must not pass a polarity-inverted signal")
    validation.check("analytic/inversion_psd_coherence_trap", inversion_guard)

    def phase_signs():
        center = 32 / (1024 / 256)
        for label, expected in (("phase_plus30", 30.), ("phase_minus30", -30.)):
            analysis = eval_by_label[label]
            close(analysis["spectrum"]["phaseDeg"][int(center)], expected, atol=PHASE_ATOL_DEG)
            close(metric(analysis, "phase_error_deg")["value"], 30., atol=PHASE_ATOL_DEG)
            close(metric(analysis, "nrmse")["value"], 2 * np.sin(np.pi / 12))
            require(analysis["status"] == "FAIL", "Phase-distorted sine must fail default fidelity criteria")
    validation.check("analytic/csd_phase_sign_and_absolute_phase_error", phase_signs)

    def delays():
        for label, expected in (("delay_plus7", 7), ("delay_minus7", -7), ("pulse_delay_plus7", 7)):
            analysis = eval_by_label[label]
            spec = next(item for item in eval_specs if item["label"] == label)
            lags, corr = delay_reference(np.asarray(spec["reference"]), np.asarray(spec["candidate"]))
            require(lags[np.nanargmax(np.abs(corr))] == expected, "Independent SciPy lag oracle disagrees with injected delay")
            close(metric(analysis, "delay_samples")["value"], expected)
        ambiguous = metric(eval_by_label["periodic_ambiguity"], "delay_samples", defined=False)
        require(ambiguous["status"] == "AMBIGUOUS" and ambiguous["value"] is None,
                "A periodic waveform must not receive a unique delay estimate")
        require(eval_by_label["periodic_ambiguity"]["status"] == "INCONCLUSIVE",
                "A gate with an ambiguous required delay must be inconclusive")
        require(eval_by_label["periodic_ambiguity"]["delay"]["bestLagSamples"] == 0,
                "Numerically tied periodic peaks must display the smallest absolute lag")
    validation.check("analytic/signed_delay_and_periodic_ambiguity", delays)

    def undefined_and_dc():
        for label in ("all_zero", "zero_reference_noise", "constant", "constant_decimal"):
            analysis = eval_by_label[label]
            delay = metric(analysis, "delay_samples", defined=False)
            require(delay["value"] is None and delay["status"] == "UNDEFINED",
                    "A constant reference has no identifiable correlation delay")
            require(analysis["status"] != "PASS", f"Undefined required evidence produced PASS for {label}")
        analysis = eval_by_label["dc_offset"]
        close(metric(analysis, "rmse")["value"], .3)
        close(metric(analysis, "spectral_error")["value"], 0.)
        close(metric(analysis, "coherence_mean")["value"], 1.)
        require(analysis["status"] == "FAIL", "A DC bias above NRMSE tolerance must not pass on detrended PSD alone")
    validation.check("analytic/undefined_zero_constant_and_dc_guard", undefined_and_dc)

    def eligible_attenuation():
        for label, gain in (("attenuated_above_floor_1e8", 1e-8),
                            ("attenuated_above_floor_1e11", 1e-11)):
            analysis = eval_by_label[label]
            close(metric(analysis, "coherence_mean")["value"], 1., atol=COHERENCE_ATOL)
            close(metric(analysis, "phase_error_deg")["value"], 0., atol=PHASE_ATOL_DEG)
            close(metric(analysis, "delay_samples")["value"], 0.)
            close(metric(analysis, "nrmse")["value"], 1. - gain)
            close(analysis["spectrum"]["numericalGuard"]["peakPowerRatio"] / gain ** 2, 1.)
            require(analysis["status"] == "FAIL", "Coherent severe attenuation still fails raw fidelity")
    validation.check("analytic/true_attenuation_above_diagnostic_floor_keeps_coherence", eligible_attenuation)

    def below_diagnostic_floor():
        for label in ("attenuated_below_floor_1e13", "amplified_above_contrast_limit"):
            analysis = eval_by_label[label]
            spec = next(item for item in eval_specs if item["label"] == label)
            sp = welch_reference(np.asarray(spec["reference"]), np.asarray(spec["candidate"]), spec["sampleRate"])
            # The oracle remains mathematically coherent: null is the lab's
            # declared relative-range eligibility, not a measurement of zero.
            close(sp["coherence"], np.ones(len(sp["f"])), atol=COHERENCE_ATOL)
            require(all(v is None for v in analysis["spectrum"]["coherence"]),
                    "Below-range spectrum must not claim normalized coherence")
            require(all(v is None for v in analysis["spectrum"]["phaseDeg"]),
                    "Below-range spectrum must not claim a cross phase")
            for name in ("coherence_mean", "phase_error_deg", "delay_samples"):
                item = metric(analysis, name, defined=False)
                require(item["status"] == "UNDEFINED" and item["value"] is None,
                        f"Below-range {name} must be explicitly UNDEFINED")
            require(np.max(analysis["spectrum"]["referencePSD"]) > 0
                    and np.max(analysis["spectrum"]["outputPSD"]) > 0,
                    "Eligibility guard must preserve nonzero raw powers")
        removed = run_by_label["sine_phase_removed"]["result"]
        analysis = removed["analysis"]["x6_phase"]
        require(np.max(np.abs(removed["arrays"]["outputs"]["x6_phase"])) < 1e-12,
                "X6 clean-sine fixture did not remove the principal component")
        require(np.max(analysis["spectrum"]["outputPSD"]) > 0,
                "X6 roundoff residual must remain visible in the raw PSD")
        for name in ("coherence_mean", "phase_error_deg", "delay_samples"):
            item = metric(analysis, name, defined=False)
            require(item["status"] == "UNDEFINED" and item["value"] is None,
                    "Near-annihilated X6 residual must not produce normalized diagnostics")
    validation.check("analytic/contrast_guard_is_symmetric_and_preserves_raw_residuals", below_diagnostic_floor)

    def balanced_tiny_controls():
        for tiny_label, ordinary_label, expected_delay in (
                ("balanced_tiny_identity", "identity_broadband", 0),
                ("balanced_tiny_gain20pct", "gain20pct", 0),
                ("balanced_tiny_delay_plus7", "delay_plus7", 7)):
            tiny, ordinary = eval_by_label[tiny_label], eval_by_label[ordinary_label]
            require(tiny["status"] == ordinary["status"], "Common small scale changed gate outcome")
            for name in ("nrmse", "gain_error_pct", "spectral_error", "coherence_mean", "phase_error_deg"):
                tiny_metric, ordinary_metric = metric(tiny, name, defined=False), metric(ordinary, name, defined=False)
                require(tiny_metric["status"] == ordinary_metric["status"],
                        f"Common tiny scaling changed {name} eligibility")
                close(tiny_metric["value"], ordinary_metric["value"],
                      atol=PHASE_ATOL_DEG if name == "phase_error_deg" else COHERENCE_ATOL)
            close(metric(tiny, "delay_samples")["value"], expected_delay)
            spec = next(item for item in eval_specs if item["label"] == tiny_label)
            lags, corr = delay_reference(np.asarray(spec["reference"]), np.asarray(spec["candidate"]))
            require(lags[np.nanargmax(np.abs(corr))] == expected_delay,
                    "Independent normalized SciPy correlation missed the tiny-signal lag")
            actual_corr = np.asarray([p["correlation"] for p in tiny["delay"]["correlationByLag"]])
            close(actual_corr, corr, rtol=SCALAR_RTOL, atol=SCALAR_ATOL)
            require(np.max(tiny["spectrum"]["referencePSD"]) > 0,
                    "Balanced tiny signal must retain representable PSD")
    validation.check("analytic/balanced_tiny_scale_preserves_normalized_diagnostics", balanced_tiny_controls)

    report = {
        "schema": "x6-signal-independent-validation-1",
        "status": "PASS" if all(c["status"] == "PASS" for c in validation.checks) else "FAIL",
        "scope": "Numerical software validation against NumPy/SciPy and unchanged original X6 filter; synthetic fixtures only",
        "versions": {"python": sys.version.split()[0], "numpy": np.__version__, "scipy": scipy.__version__, "node": payload["node"]},
        "hashes": {"core_sha256": payload["coreHash"], "original_filter_sha256": payload["originalFilterHash"],
                   "application_sha256": payload["originalAppHash"],
                   "oracle_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   "fixture_sha256": hashlib.sha256(Path(__file__).with_name("reference_fixture.cjs").read_bytes()).hexdigest(),
                   "requirements_sha256": hashlib.sha256(Path(__file__).with_name("requirements.txt").read_bytes()).hexdigest()},
        "tolerances": {"array_rtol": ARRAY_RTOL, "array_atol": ARRAY_ATOL,
                       "psd_rtol": PSD_RTOL, "psd_atol": PSD_ATOL,
                       "metric_rtol": SCALAR_RTOL, "metric_atol": SCALAR_ATOL,
                       "phase_atol_degrees": PHASE_ATOL_DEG, "coherence_atol": COHERENCE_ATOL},
        "diagnostic_eligibility": {"individual_psd_peak_ratio": INDIVIDUAL_PSD_RATIO,
                                   "pairwise_psd_peak_ratio": PAIRWISE_PSD_RATIO,
                                   "centered_norm_ratio": CENTERED_NORM_RATIO,
                                   "comparison": "strictly greater than; declared software policy, not a physical noise floor"},
        "run_fixtures": len(run_specs), "evaluation_fixtures": len(eval_specs),
        "passed": sum(c["status"] == "PASS" for c in validation.checks),
        "total": len(validation.checks), "checks": validation.checks,
        "limitations": ["No physical measurement or quantum inference", "Floating-point comparisons, not formal interval certification",
                        "No statistical coverage claim from the fixed seeds", "This command does not execute browser UI tests"]}
    if args.report:
        destination = Path(args.report)
        destination.parent.mkdir(parents=True, exist_ok=True)
        serialized = json.dumps(report, indent=2, allow_nan=False) + "\n"
        require(len(serialized.encode()) <= 256 * 1024, "Report exceeds 256 KiB bound")
        destination.write_text(serialized)
    summary = {key: report[key] for key in ("status", "versions", "passed", "total", "run_fixtures", "evaluation_fixtures")}
    summary["failures"] = [c for c in validation.checks if c["status"] == "FAIL"]
    print(json.dumps(summary, indent=2, allow_nan=False))
    return 0 if report["status"] == "PASS" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", help="Optional compact JSON report destination; no report is written by default")
    parser.add_argument("--node", default=os.environ.get("NODE", "node"), help="Node executable (default: NODE or node)")
    args = parser.parse_args()
    try:
        return run_validation(args)
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": f"{type(exc).__name__}: {exc}"[:4000]}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
