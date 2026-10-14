"""Explicit complex-signal conventions. Small, dependency-free reference tools.
SPDX-License-Identifier: Apache-2.0
"""
import cmath
import math
import random


def finite(value, name='value', low=-math.inf, high=math.inf):
    if type(value) not in (int, float) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f'{name}: invalid finite number/range')
    return value


def samples(values):
    if not values or any(not math.isfinite(z.real) or not math.isfinite(z.imag) for z in values):
        raise ValueError('Empty or nonfinite signal')
    return values


def phase_error(measured, reference, floor=1e-12):
    finite(floor, 'amplitude floor', 0)
    if len(measured) != len(reference):
        raise ValueError('Length mismatch')
    samples(measured); samples(reference)
    return [None if abs(m) <= floor or abs(r) <= floor else
            math.atan2((m*r.conjugate()).imag, (m*r.conjugate()).real)
            for m, r in zip(measured, reference)]


def relative_rms(measured, reference):
    if len(measured) != len(reference):
        raise ValueError('Length mismatch')
    samples(measured); samples(reference)
    power = sum(abs(z)**2 for z in reference)
    return None if power == 0 else math.sqrt(sum(abs(a-b)**2 for a, b in zip(measured, reference))/power)


def align_integer_delay(measured, reference, max_lag):
    """Positive lag means measured signal is delayed. Same central support for all lags.

    No circular wrap, no phase/gain fitting. Raw error always retained.
    This operation must be allowed by the frozen experiment contract.
    """
    if type(max_lag) is not int or max_lag < 0 or len(reference) <= 2*max_lag:
        raise ValueError('Invalid lag/support')
    if len(measured) != len(reference):
        raise ValueError('Length mismatch')
    raw = relative_rms(measured, reference)
    indices = range(max_lag, len(reference)-max_lag)
    ref = [reference[i] for i in indices]
    candidates = [(relative_rms([measured[i+lag] for i in indices], ref), lag)
                  for lag in range(-max_lag, max_lag+1)]
    if any(error is None for error, _ in candidates):
        raise ValueError('Alignment undefined for zero reference')
    error, lag = min(candidates)
    return {'raw_relative_rms': raw, 'aligned_relative_rms': error,
            'delay_samples': lag, 'support': [max_lag, len(reference)-max_lag],
            'corrections': ['integer_delay_only']}


def spectrum(values, sample_rate_hz):
    """Two-sided rectangular-window DFT. Density units |signal|²/Hz.

    O(N²) oracle for at most 1024 samples; no real-FFT or one-sided doubling.
    """
    samples(values); finite(sample_rate_hz, 'sample rate', 1e-12)
    n = len(values)
    if n > 1024:
        raise ValueError('Reference DFT is limited to 1024 samples')
    transformed = [sum(z*cmath.exp(-2j*math.pi*k*i/n) for i, z in enumerate(values))
                   for k in range(n)]
    return {'frequency_hz': [(k if k < (n+1)//2 else k-n)*sample_rate_hz/n for k in range(n)],
            'density': [abs(z)**2/(sample_rate_hz*n) for z in transformed],
            'bin_width_hz': sample_rate_hz/n, 'window': 'rectangular', 'sidedness': 'two'}


def time_signal(function, count, period_s, offset_s=0, drift_ppm=0, jitter_s=0, seed=0):
    if type(count) is not int or not 1 <= count <= 100000:
        raise ValueError('Invalid sample count')
    finite(period_s, 'period', 1e-12)
    finite(offset_s); finite(drift_ppm, 'drift', -1000, 1000)
    finite(jitter_s, 'jitter', 0, period_s/4)
    rng = random.Random(seed)
    times = [offset_s+i*period_s*(1+drift_ppm*1e-6)+rng.uniform(-jitter_s, jitter_s)
             for i in range(count)]
    if any(b <= a for a, b in zip(times, times[1:])):
        raise ValueError('Nonmonotonic sampling time')
    return times, [function(t) for t in times]
