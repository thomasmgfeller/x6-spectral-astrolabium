/* Signal Validation Lab: deterministic synthetic comparisons, not physical qualification. */
(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.X6SignalLab = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  const VERSION = '1.0.0';
  const TAU = 2 * Math.PI;
  const METHODS = ['identity', 'moving_average', 'fft_lowpass', 'x6_phase'];
  const SIGNALS = ['sine', 'multitone', 'chirp', 'pulse', 'zero'];
  const ACTIVE_PSD_RATIO = 1e-3;
  const NUMERICAL_PSD_RATIO = 1e-12;
  const PAIRWISE_PSD_RATIO = 1e-24;
  const CENTERED_NORM_RATIO = 1e-12;
  const DELAY_COMPETITOR_MARGIN = 0.01;
  const DELAY_TIE_TOLERANCE = 1e-12;
  const ACCEPTANCE = Object.freeze({
    nrmseMax: 0.25, gainErrorPctMax: 10, phaseErrorDegMax: 10,
    delaySamplesMax: 1, spectralErrorMax: 0.2,
    coherenceMin: 0.9, phaseCoherenceMin: 0.8
  });

  function defaults() {
    return {
      signal: 'multitone', samples: 1024, sampleRate: 1024, frequency: 32,
      amplitude: 1, seed: 104729, gain: 1, phaseDeg: 0, delaySamples: 0,
      noiseStd: 0.15, clipLevel: 0, quantBits: 0, quantRange: 2,
      movingAverageWindow: 9, cutoffHz: 128,
      phaseCenterDeg: 0, phaseWidthDeg: 45, phaseMode: 'pass',
      acceptance: Object.assign({}, ACCEPTANCE)
    };
  }

  function plainObject(value) {
    return value !== null && typeof value === 'object' && !Array.isArray(value) &&
      (Object.getPrototypeOf(value) === Object.prototype || Object.getPrototypeOf(value) === null);
  }

  function acceptanceValues(input, errors) {
    const result = Object.assign({}, ACCEPTANCE);
    if (input === undefined) return result;
    if (!plainObject(input)) {
      errors.push({field: 'acceptance', message: 'Acceptance must be a plain object.'});
      return result;
    }
    Object.keys(input).forEach(function (key) {
      if (!Object.prototype.hasOwnProperty.call(ACCEPTANCE, key)) {
        errors.push({field: 'acceptance.' + key, message: 'Unknown acceptance key.'});
        return;
      }
      const value = input[key];
      const upper = key === 'phaseErrorDegMax' ? 180 :
        (key === 'coherenceMin' || key === 'phaseCoherenceMin') ? 1 :
        key === 'delaySamplesMax' ? 4096 : 1e6;
      if (typeof value !== 'number' || !Number.isFinite(value) || value < 0 || value > upper) {
        errors.push({field: 'acceptance.' + key, message: 'Expected a finite number in [0, ' + upper + '].'});
      } else result[key] = value;
    });
    return result;
  }

  function validate(input) {
    const errors = [];
    const base = defaults();
    if (input === undefined) input = {};
    if (!plainObject(input)) {
      return {valid: false, errors: [{field: 'parameters', message: 'Parameters must be a plain object.'}], parameters: null};
    }
    const params = Object.assign({}, base);
    Object.keys(input).forEach(function (key) {
      if (!Object.prototype.hasOwnProperty.call(base, key)) {
        errors.push({field: key, message: 'Unknown parameter.'});
      } else if (key !== 'acceptance') params[key] = input[key];
    });
    params.acceptance = acceptanceValues(input.acceptance, errors);
    function finiteRange(key, lower, upper, integer) {
      const v = params[key];
      if (typeof v !== 'number' || !Number.isFinite(v) || v < lower || v > upper || (integer && !Number.isInteger(v))) {
        errors.push({field: key, message: 'Expected ' + (integer ? 'an integer' : 'a finite number') + ' in [' + lower + ', ' + upper + '].'});
        return false;
      }
      return true;
    }
    if (!SIGNALS.includes(params.signal)) errors.push({field: 'signal', message: 'Unknown waveform.'});
    const validN = finiteRange('samples', 128, 4096, true) && !(params.samples & (params.samples - 1));
    if (Number.isInteger(params.samples) && params.samples >= 128 && params.samples <= 4096 && !validN) {
      errors.push({field: 'samples', message: 'Samples must be a power of two.'});
    }
    const validFs = finiteRange('sampleRate', 0.001, 1e7);
    const validF = finiteRange('frequency', 0, 1e7);
    finiteRange('amplitude', 0, 1e6);
    finiteRange('seed', 0, 4294967295, true);
    finiteRange('gain', -100, 100);
    finiteRange('phaseDeg', -180, 180);
    finiteRange('noiseStd', 0, 1e6);
    finiteRange('clipLevel', 0, 1e9);
    finiteRange('quantBits', 0, 16, true);
    if (params.quantBits === 1) errors.push({field: 'quantBits', message: 'Use zero (off) or 2–16 bits.'});
    finiteRange('quantRange', 1e-12, 1e9);
    const delayBound = validN ? Math.min(64, params.samples / 4) : 64;
    finiteRange('delaySamples', -delayBound, delayBound, true);
    if (finiteRange('movingAverageWindow', 1, validN ? params.samples - 1 : 4095, true) && params.movingAverageWindow % 2 !== 1) {
      errors.push({field: 'movingAverageWindow', message: 'Centered moving-average window must be odd.'});
    }
    finiteRange('cutoffHz', 0, validFs ? params.sampleRate / 2 : 5e6);
    finiteRange('phaseCenterDeg', -180, 180);
    finiteRange('phaseWidthDeg', 0, 360);
    if (!['pass', 'stop'].includes(params.phaseMode)) errors.push({field: 'phaseMode', message: 'Expected pass or stop.'});
    if (validFs && validF && ['sine', 'multitone', 'chirp'].includes(params.signal)) {
      const multiplier = params.signal === 'sine' ? 1 : 2.5;
      if (!(params.frequency > 0 && multiplier * params.frequency < params.sampleRate / 2)) {
        errors.push({field: 'frequency', message: 'All modeled frequencies must be positive and strictly below Nyquist (maximum ' + multiplier + ' × frequency).'});
      }
    }
    if (['pulse', 'zero'].includes(params.signal) && params.phaseDeg !== 0) {
      errors.push({field: 'phaseDeg', message: 'Phase offset is only defined for the oscillatory waveforms; use zero for pulse/zero.'});
    }
    return {valid: errors.length === 0, errors: errors, parameters: errors.length ? null : params};
  }

  function requireParameters(input) {
    const checked = validate(input);
    if (!checked.valid) throw new RangeError(checked.errors.map(function (e) { return e.field + ': ' + e.message; }).join(' '));
    return checked.parameters;
  }

  function mean(values) {
    const anchor = values[0];
    let sum = 0;
    for (let i = 0; i < values.length; i++) sum += values[i] - anchor;
    return anchor + sum / values.length;
  }

  function sumSquares(values) {
    let result = 0;
    for (let i = 0; i < values.length; i++) result += values[i] * values[i];
    return result;
  }

  // Original X6 radix-2 transform and phase-selection arithmetic are retained.
  function fft(re, im, inv = false) {
    let n = re.length;
    if (n < 2 || (n & (n - 1))) throw Error('FFT length must be a power of two');
    for (let i = 1, j = 0; i < n; i++) {
      let b = n >> 1;
      for (; j & b; b >>= 1) j ^= b;
      j ^= b;
      if (i < j) { [re[i], re[j]] = [re[j], re[i]]; [im[i], im[j]] = [im[j], im[i]]; }
    }
    for (let len = 2; len <= n; len *= 2) {
      let a = (inv ? 1 : -1) * TAU / len, wr = Math.cos(a), wi = Math.sin(a);
      for (let k = 0; k < n; k += len) {
        let cr = 1, ci = 0;
        for (let j = 0; j < len / 2; j++) {
          let u = k + j, v = u + len / 2, tr = cr * re[v] - ci * im[v], ti = cr * im[v] + ci * re[v];
          re[v] = re[u] - tr; im[v] = im[u] - ti; re[u] += tr; im[u] += ti;
          [cr, ci] = [cr * wr - ci * wi, cr * wi + ci * wr];
        }
      }
    }
    if (inv) for (let i = 0; i < n; i++) { re[i] /= n; im[i] /= n; }
    return {re: re, im: im};
  }

  function transform(values) { return fft(values.slice(), Array(values.length).fill(0)); }

  function x6Phase(values, angle, width, mode) {
    let {re, im} = transform(values), n = values.length;
    let c = angle * Math.PI / 180, h = width * Math.PI / 360;
    const distance = p => Math.abs(Math.atan2(Math.sin(p - c), Math.cos(p - c)));
    for (let k = 1; k < n / 2; k++) {
      let inside = distance(Math.atan2(im[k], re[k])) <= h;
      let keep = mode === 'pass' ? inside : !inside;
      if (!keep) re[k] = im[k] = re[n - k] = im[n - k] = 0;
    }
    for (let k of [0, n / 2]) {
      let inside = distance(re[k] < 0 ? Math.PI : 0) <= h;
      let keep = mode === 'pass' ? inside : !inside;
      if (!keep) re[k] = im[k] = 0;
    }
    return fft(re, im, true).re;
  }

  function movingAverage(values, window) {
    const half = (window - 1) / 2;
    return values.map(function (_, i) {
      let sum = 0;
      const start = Math.max(0, i - half), end = Math.min(values.length, i + half + 1);
      for (let j = start; j < end; j++) sum += values[j];
      return sum / (end - start);
    });
  }

  function fftLowpass(values, fs, cutoff) {
    const z = transform(values), n = values.length;
    for (let k = 0; k < n; k++) {
      if (Math.min(k, n - k) * fs / n > cutoff) z.re[k] = z.im[k] = 0;
    }
    return fft(z.re, z.im, true).re;
  }

  function seededUniform(seed) {
    let state = seed >>> 0;
    return function () { state = (Math.imul(state, 1664525) + 1013904223) >>> 0; return state / 4294967296; };
  }

  function gaussian(random) {
    return Math.sqrt(-2 * Math.log(Math.max(random(), 1e-12))) * Math.cos(TAU * random());
  }

  function waveform(params, phaseDeg) {
    const duration = params.samples / params.sampleRate;
    const phase = phaseDeg * Math.PI / 180;
    return Array.from({length: params.samples}, function (_, i) {
      const t = i / params.sampleRate, f = params.frequency, a = params.amplitude;
      if (params.signal === 'zero') return 0;
      if (params.signal === 'pulse') return a * Math.exp(-0.5 * ((t - duration / 2) / (0.035 * duration)) ** 2);
      if (params.signal === 'chirp') return a * Math.sin(TAU * (f * t + 0.5 * (1.5 * f / duration) * t * t) + phase);
      if (params.signal === 'multitone') return a / 1.75 * (Math.sin(TAU * f * t + phase) + 0.5 * Math.sin(TAU * 1.75 * f * t + phase) + 0.25 * Math.sin(TAU * 2.5 * f * t + phase));
      return a * Math.sin(TAU * f * t + phase);
    });
  }

  function shiftZeroPadded(values, lag) {
    return values.map(function (_, i) { const j = i - lag; return j >= 0 && j < values.length ? values[j] : 0; });
  }

  function distort(params) {
    const shifted = shiftZeroPadded(waveform(params, params.phaseDeg).map(v => params.gain * v), params.delaySamples);
    const random = seededUniform(params.seed);
    const halfCodes = params.quantBits ? 2 ** (params.quantBits - 1) : 0;
    const step = params.quantBits ? 2 * params.quantRange / (2 ** params.quantBits) : 0;
    return shifted.map(function (value) {
      let out = value + params.noiseStd * gaussian(random);
      if (params.clipLevel > 0) out = Math.max(-params.clipLevel, Math.min(params.clipLevel, out));
      if (params.quantBits) out = Math.max(-halfCodes, Math.min(halfCodes - 1, Math.floor(out / step + 0.5))) * step;
      return out;
    });
  }

  function metric(value, status, reason, unit) {
    if (value !== null && !Number.isFinite(value)) return {value: null, status: 'UNDEFINED', reason: 'Numerical range exhausted: ' + reason, unit: unit};
    return {value: value, status: status, reason: reason, unit: unit};
  }

  function welch(reference, candidate, fs) {
    const nperseg = Math.min(256, reference.length / 2), step = nperseg / 2;
    const bins = nperseg / 2 + 1;
    const window = Array.from({length: nperseg}, (_, i) => 0.5 - 0.5 * Math.cos(TAU * i / nperseg));
    const normalization = fs * sumSquares(window);
    const referencePSD = Array(bins).fill(0), outputPSD = Array(bins).fill(0);
    const crossRe = Array(bins).fill(0), crossIm = Array(bins).fill(0);
    let segments = 0;
    for (let start = 0; start + nperseg <= reference.length; start += step) {
      const x = reference.slice(start, start + nperseg), y = candidate.slice(start, start + nperseg);
      const mx = mean(x), my = mean(y);
      for (let i = 0; i < nperseg; i++) { x[i] = (x[i] - mx) * window[i]; y[i] = (y[i] - my) * window[i]; }
      const X = transform(x), Y = transform(y);
      for (let k = 0; k < bins; k++) {
        const factor = (k === 0 || k === nperseg / 2 ? 1 : 2) / normalization;
        referencePSD[k] += (X.re[k] ** 2 + X.im[k] ** 2) * factor;
        outputPSD[k] += (Y.re[k] ** 2 + Y.im[k] ** 2) * factor;
        crossRe[k] += (X.re[k] * Y.re[k] + X.im[k] * Y.im[k]) * factor;
        crossIm[k] += (X.re[k] * Y.im[k] - X.im[k] * Y.re[k]) * factor;
      }
      segments++;
    }
    for (let k = 0; k < bins; k++) { referencePSD[k] /= segments; outputPSD[k] /= segments; crossRe[k] /= segments; crossIm[k] /= segments; }
    const maxX = Math.max(...referencePSD), maxY = Math.max(...outputPSD);
    const pairPeak = Math.max(maxX, maxY), pairFloor = pairPeak * PAIRWISE_PSD_RATIO;
    const coherence = Array(bins).fill(null), phaseDeg = Array(bins).fill(null);
    for (let k = 0; k < bins; k++) {
      const denominator = Math.sqrt(referencePSD[k]) * Math.sqrt(outputPSD[k]);
      if (referencePSD[k] > maxX * NUMERICAL_PSD_RATIO && outputPSD[k] > maxY * NUMERICAL_PSD_RATIO && referencePSD[k] > pairFloor && outputPSD[k] > pairFloor && denominator > 0) {
        const crossMagnitude = Math.hypot(crossRe[k], crossIm[k]);
        const value = (crossMagnitude / denominator) ** 2;
        if (Number.isFinite(value)) coherence[k] = Math.max(0, Math.min(1, value));
        if (crossMagnitude > 0) phaseDeg[k] = Math.atan2(crossIm[k], crossRe[k]) * 180 / Math.PI;
      }
    }
    const activeReferenceBins = [];
    for (let k = 1; k < bins; k++) if (maxX > 0 && referencePSD[k] >= maxX * ACTIVE_PSD_RATIO) activeReferenceBins.push(k);
    return {
      frequencies: Array.from({length: bins}, (_, k) => k * fs / nperseg),
      referencePSD: referencePSD, outputPSD: outputPSD, coherence: coherence, phaseDeg: phaseDeg,
      crossSpectrumReal: crossRe, crossSpectrumImag: crossIm,
      activeReferenceBins: activeReferenceBins,
      numericalGuard: {pairwisePeakFloorRatio: PAIRWISE_PSD_RATIO, pairwisePeakPower: pairPeak, minimumPSD: pairFloor, peakPowerRatio: pairPeak > 0 ? Math.min(maxX, maxY) / pairPeak : null},
      estimator: {method: 'Welch', nperseg: nperseg, overlap: step, segments: segments, window: 'periodic Hann', detrend: 'constant per segment', scaling: 'one-sided density', densityDenominator: normalization}
    };
  }

  function delayEstimate(reference, candidate) {
    const n = reference.length, bound = Math.min(64, n / 4), correlations = [];
    const globalMeanX = mean(reference), globalMeanY = mean(candidate);
    const globalNormX = Math.hypot(...reference.map(v => v - globalMeanX));
    const globalNormY = Math.hypot(...candidate.map(v => v - globalMeanY));
    const maximumNorm = Math.max(globalNormX, globalNormY);
    const normRatio = maximumNorm > 0 ? Math.min(globalNormX, globalNormY) / maximumNorm : null;
    const numericalGuard = {centeredNormRatio: normRatio, minimumCenteredNormRatio: CENTERED_NORM_RATIO};
    if (!(normRatio > CENTERED_NORM_RATIO)) {
      for (let lag = -bound; lag <= bound; lag++) correlations.push({lag: lag, correlation: null});
      return {value: null, status: 'UNDEFINED', reason: 'Centered energy is zero or the signal-pair centered-norm ratio does not exceed the declared 1e-12 diagnostic range limit. Delay is not evaluated on a negligible residual; this is not a physical decoherence claim.', searchMaxLagSamples: bound, bestLagSamples: null, maxAbsCorrelation: null, competingLags: [], correlationByLag: correlations, numericalGuard: numericalGuard};
    }
    for (let lag = -bound; lag <= bound; lag++) {
      const start = Math.max(0, -lag), end = Math.min(n, n - lag), count = end - start;
      const anchorX = reference[start], anchorY = candidate[start + lag];
      let mx = 0, my = 0;
      for (let i = start; i < end; i++) { mx += reference[i] - anchorX; my += candidate[i + lag] - anchorY; }
      mx = anchorX + mx / count; my = anchorY + my / count;
      const centeredX = [], centeredY = [];
      for (let i = start; i < end; i++) {
        centeredX.push(reference[i] - mx); centeredY.push(candidate[i + lag] - my);
      }
      const normX = Math.hypot(...centeredX), normY = Math.hypot(...centeredY);
      const overlapRatio = Math.max(normX, normY) > 0 ? Math.min(normX, normY) / Math.max(normX, normY) : 0;
      let correlation = null;
      if (overlapRatio > CENTERED_NORM_RATIO) {
        let dot = 0;
        for (let i = 0; i < count; i++) dot += (centeredX[i] / normX) * (centeredY[i] / normY);
        correlation = Math.max(-1, Math.min(1, dot));
      }
      correlations.push({lag: lag, correlation: Number.isFinite(correlation) ? correlation : null});
    }
    const defined = correlations.filter(c => c.correlation !== null);
    if (!defined.length) return {value: null, status: 'UNDEFINED', reason: 'Delay requires nonzero centered overlap energy and a centered-norm ratio above the declared 1e-12 diagnostic range limit.', searchMaxLagSamples: bound, bestLagSamples: null, maxAbsCorrelation: null, competingLags: [], correlationByLag: correlations, numericalGuard: numericalGuard};
    const score = Math.max(...defined.map(item => Math.abs(item.correlation)));
    const numericalTies = defined.filter(item => Math.abs(item.correlation) >= score - DELAY_TIE_TOLERANCE);
    numericalTies.sort(function (a, b) { return Math.abs(a.lag) - Math.abs(b.lag) || a.lag - b.lag; });
    const best = numericalTies[0], competitors = [];
    for (let i = 0; i < correlations.length; i++) {
      const item = correlations[i];
      if (item.correlation === null || Math.abs(item.lag - best.lag) <= 1) continue;
      const value = Math.abs(item.correlation);
      const left = i > 0 && correlations[i - 1].correlation !== null ? Math.abs(correlations[i - 1].correlation) : -1;
      const right = i + 1 < correlations.length && correlations[i + 1].correlation !== null ? Math.abs(correlations[i + 1].correlation) : -1;
      if (value >= left - 1e-12 && value >= right - 1e-12 && value >= score - DELAY_COMPETITOR_MARGIN) competitors.push(item.lag);
    }
    let status = 'DEFINED', reason = 'Unique dominant absolute overlap-correlation peak inside the bounded search; positive means candidate delayed.';
    if (score < 0.2) { status = 'UNDEFINED'; reason = 'Maximum absolute overlap correlation is below the declared 0.2 identifiability threshold.'; }
    else if (Math.abs(best.lag) === bound) { status = 'AMBIGUOUS'; reason = 'Best peak is at the search boundary; delay outside the search cannot be excluded.'; }
    else if (competitors.length) { status = 'AMBIGUOUS'; reason = 'Competing separated correlation peaks lie within 0.01 of the maximum; periodic or ambiguous delay.'; }
    return {value: status === 'DEFINED' ? best.lag : null, status: status, reason: reason, searchMaxLagSamples: bound, bestLagSamples: best.lag, maxAbsCorrelation: score, competingLags: competitors, correlationByLag: correlations, numericalGuard: numericalGuard};
  }

  function validateSeries(reference, candidate, sampleRate) {
    if (!Array.isArray(reference) || !Array.isArray(candidate) || reference.length !== candidate.length || reference.length < 128 || reference.length > 4096 || (reference.length & (reference.length - 1))) {
      throw new RangeError('Evaluation requires two equally long ordinary arrays, power-of-two length 128–4096.');
    }
    if (typeof sampleRate !== 'number' || !Number.isFinite(sampleRate) || sampleRate < 0.001 || sampleRate > 1e7) throw new RangeError('sampleRate must be a finite number in [0.001, 1e7].');
    for (const values of [reference, candidate]) {
      if (Reflect.ownKeys(values).length !== values.length + 1) throw new RangeError('Signal arrays must be dense and have no extra properties.');
      for (let i = 0; i < values.length; i++) {
        if (!Object.prototype.hasOwnProperty.call(values, i) || typeof values[i] !== 'number' || !Number.isFinite(values[i]) || Math.abs(values[i]) > 1e12) throw new RangeError('Signal samples must be present finite numbers with magnitude at most 1e12.');
      }
    }
  }

  function evaluate(reference, candidate, sampleRate, acceptanceInput) {
    validateSeries(reference, candidate, sampleRate);
    const errors = [], acceptance = acceptanceValues(acceptanceInput, errors);
    if (errors.length) throw new RangeError(errors.map(e => e.field + ': ' + e.message).join(' '));
    // hypot uses scaled accumulation, keeping tiny but nonzero time-domain norms usable.
    const referenceNorm = Math.hypot(...reference), outputNorm = Math.hypot(...candidate);
    const errorNorm = Math.hypot(...candidate.map((value, i) => value - reference[i]));
    const metrics = {};
    metrics.rmse = metric(errorNorm / Math.sqrt(reference.length), 'DEFINED', 'Root mean squared sample error against the known reference; no alignment or rescaling.', 'amplitude');
    metrics.nrmse = referenceNorm > 0 ? metric(errorNorm / referenceNorm, 'DEFINED', 'RMS error divided by raw reference RMS; no alignment or rescaling.', 'ratio') : metric(null, 'UNDEFINED', 'Reference has zero representable norm; normalized error has no denominator.', 'ratio');
    metrics.gain_error_pct = referenceNorm > 0 ? metric(100 * (outputNorm / referenceNorm - 1), 'DEFINED', 'Signed raw RMS amplitude-ratio error; this does not detect polarity inversion.', '%') : metric(null, 'UNDEFINED', 'Reference has zero representable RMS; gain ratio is undefined.', '%');
    if (referenceNorm <= 0) metrics.snr_db = metric(null, 'UNDEFINED', 'Reference energy is zero; reconstruction SNR is undefined (including zero versus zero).', 'dB');
    else if (errorNorm === 0) metrics.snr_db = metric(null, 'EXACT_MATCH', 'Exactly zero sample error with nonzero reference: mathematical SNR is +infinity; represented as null with this explicit status.', 'dB');
    else metrics.snr_db = metric(20 * (Math.log10(referenceNorm) - Math.log10(errorNorm)), 'DEFINED', '10 log10(sum reference² / sum reconstruction-error²), evaluated with scaled norms and logarithms; known synthetic reference, not a measurement of physical noise power.', 'dB');

    const spectrum = welch(reference, candidate, sampleRate);
    const spectralReferencePower = spectrum.referencePSD.reduce((a, b) => a + b, 0);
    let spectralDifference = 0;
    for (let k = 0; k < spectrum.referencePSD.length; k++) spectralDifference += Math.abs(spectrum.outputPSD[k] - spectrum.referencePSD[k]);
    metrics.spectral_error = spectralReferencePower > 0 ? metric(spectralDifference / spectralReferencePower, 'DEFINED', 'L1 difference of detrended Welch PSDs divided by reference PSD integral; phase and DC errors can be invisible.', 'ratio') : metric(null, 'UNDEFINED', 'Detrended reference spectrum has zero representable energy (e.g. DC/zero); relative spectral error is undefined.', 'ratio');
    let allWeight = 0, coherenceWeight = 0, phaseWeight = 0, coherenceSum = 0, phaseSquare = 0;
    const phaseEligibleBins = [];
    spectrum.activeReferenceBins.forEach(function (k) {
      const weight = spectrum.referencePSD[k]; allWeight += weight;
      if (spectrum.coherence[k] !== null) { coherenceWeight += weight; coherenceSum += weight * spectrum.coherence[k]; }
      if (spectrum.coherence[k] !== null && spectrum.coherence[k] >= acceptance.phaseCoherenceMin && spectrum.phaseDeg[k] !== null) {
        phaseWeight += weight; phaseSquare += weight * spectrum.phaseDeg[k] ** 2; phaseEligibleBins.push(k);
      }
    });
    const coherenceCoverage = allWeight > 0 ? coherenceWeight / allWeight : null;
    const phaseCoverage = allWeight > 0 ? phaseWeight / allWeight : null;
    metrics.coherence_mean = coherenceWeight > 0 ? metric(coherenceSum / coherenceWeight, coherenceCoverage >= 1 - 1e-12 ? 'DEFINED' : 'PARTIAL', 'Reference-PSD-weighted coherence on non-DC bins at least 0.001 of peak reference PSD; defined reference-weight coverage is recorded in spectrum.coherenceCoverage. Coherence alone cannot identify gain or phase correctness.', 'ratio') : metric(null, 'UNDEFINED', 'No reference-active bins with nonzero-energy coherence inside the declared diagnostic dynamic range. This is an evaluation limit, not evidence of physical decoherence.', 'ratio');
    metrics.phase_error_deg = phaseWeight > 0 ? metric(Math.sqrt(phaseSquare / phaseWeight), phaseCoverage >= 1 - 1e-12 ? 'DEFINED' : 'PARTIAL', 'Reference-PSD-weighted RMS wrapped cross-phase relative to zero; only coherence >= ' + acceptance.phaseCoherenceMin + '; eligible reference-weight coverage is recorded in spectrum.phaseCoverage. No delay compensation.', 'deg') : metric(null, 'UNDEFINED', 'No reference-active bins inside the declared diagnostic dynamic range with sufficient coherence and a defined cross-phase.', 'deg');
    spectrum.phaseEligibleBins = phaseEligibleBins;
    spectrum.coherenceCoverage = coherenceCoverage;
    spectrum.phaseCoverage = phaseCoverage;
    const delay = delayEstimate(reference, candidate);
    metrics.delay_samples = metric(delay.value, delay.status, delay.reason, 'samples');

    const specifications = [
      ['nrmse', acceptance.nrmseMax, false, false],
      ['gain_error_pct', acceptance.gainErrorPctMax, true, false],
      ['phase_error_deg', acceptance.phaseErrorDegMax, false, false],
      ['delay_samples', acceptance.delaySamplesMax, true, false],
      ['spectral_error', acceptance.spectralErrorMax, false, false],
      ['coherence_mean', acceptance.coherenceMin, false, true]
    ];
    const gates = specifications.map(function (specification) {
      const id = specification[0], limit = specification[1], m = metrics[id];
      if (m.status !== 'DEFINED' || m.value === null) return {id: id, value: m.value, limit: limit, status: 'UNDEFINED', reason: 'Screening cannot pass an unavailable, partial, or ambiguous metric. ' + m.reason};
      const comparison = specification[2] ? Math.abs(m.value) : m.value;
      const pass = specification[3] ? comparison >= limit : comparison <= limit;
      return {id: id, value: m.value, limit: limit, status: pass ? 'PASS' : 'FAIL', reason: 'Declared exploratory screening: ' + (specification[2] ? 'absolute value ' : 'value ') + (specification[3] ? '>= ' : '<= ') + limit + '; no physical qualification.'};
    });
    const status = gates.some(g => g.status === 'FAIL') ? 'FAIL' : gates.some(g => g.status !== 'PASS') ? 'INCONCLUSIVE' : 'PASS';
    return {metrics: metrics, spectrum: spectrum, delay: delay, gates: gates, status: status, acceptance: acceptance, evidenceClass: 'SYNTHETIC_RESULT'};
  }

  function methodology(params) {
    return {
      scope: 'Known-truth synthetic signal comparison. Declared screening limits are not physical qualification, measured device performance, or proof of a quantum model.',
      sampling: 't[i]=i/sampleRate; record duration=samples/sampleRate. No automatic time alignment, amplitude fit, or reference smoothing.',
      signals: {sine: 'A sin(2π f t)', multitone: 'A/1.75 [sin(2π f t)+0.5 sin(2π·1.75 f t)+0.25 sin(2π·2.5 f t)]', chirp: 'A sin(2π[f t + 0.5(1.5 f/T)t²]), T=N/fs', pulse: 'A exp(-0.5[(t-T/2)/(0.035T)]²)', zero: '0'},
      impairments: 'Oscillatory phase offset (same offset per tone), gain, signed integer zero-padded delay, Gaussian white noise, hard clipping, signed quantization, in that order.',
      noise: {generator: 'uint32 LCG: s=(1664525*s+1013904223) mod 2^32; u=s/2^32', gaussian: 'sqrt(-2 ln(max(u1,1e-12))) cos(2πu2); two draws per sample; no spare caching', interpretation: 'noiseStd is nominal distribution standard deviation, not a per-record renormalization. The tiny uniform cutoff is explicit.'},
      quantization: 'delta=2*quantRange/2^bits; code=floor(value/delta+0.5), clamped to [-2^(bits-1),2^(bits-1)-1]; output=code*delta. Round ties toward +infinity. Zero bits disables quantization.',
      baselines: {identity: 'Unchanged observed samples.', moving_average: 'Centered odd-window local mean; available samples renormalize the edges. Noncausal offline comparison.', fft_lowpass: 'Periodic record FFT; retain |frequency| <= cutoffHz, including DC. Ideal brick-wall offline comparison; wrap-around and ringing are possible.', x6_phase: 'Original X6 positive-frequency phase selection, conjugate pairs retained/removed together, DC/Nyquist selected by real sign. This is phase selection, not a frequency low-pass, and is not generally time-shift invariant.'},
      welch: {nperseg: Math.min(256, params.samples / 2), overlap: Math.min(256, params.samples / 2) / 2, window: 'periodic Hann', detrend: 'constant per segment before window', scaling: 'one-sided density, denominator fs*sum(window²), interior bins doubled', crossSpectrum: 'conj(reference FFT)*candidate FFT, positive delay gives negative cross-phase', caveat: 'Finite-record descriptive estimator, no coherence significance interval. Constant detrending hides DC differences; raw time-domain metrics retain them.'},
      spectralEligibility: {activeReferencePeakRatio: ACTIVE_PSD_RATIO, numericalPowerPeakRatio: NUMERICAL_PSD_RATIO, pairwisePowerPeakRatio: PAIRWISE_PSD_RATIO, phaseMinimumCoherence: params.acceptance.phaseCoherenceMin, pairwiseRule: 'Both bin PSDs must strictly exceed 1e-24 times the larger signal PSD peak, in addition to their individual relative floors. This declared diagnostic dynamic-range limit suppresses unreliable residual normalization; mathematically coherent strong attenuation may still be unqualified. It is not a physical noise floor or a decoherence measurement. Raw PSD/CSD arrays are retained.', missingCoverage: 'partial/undefined metrics cannot pass their gates'},
      delay: {searchMaxLagSamples: Math.min(64, params.samples / 4), convention: 'positive means candidate delayed', estimator: 'maximum absolute Pearson correlation on mean-centered overlaps x[i], y[i+lag]; at least 75% record overlap; normalized vectors avoid product underflow', minimumCenteredNormRatio: CENTERED_NORM_RATIO, dynamicRange: 'Global and overlap min(centered norms)/max(centered norms) must strictly exceed 1e-12. This is a declared diagnostic eligibility limit, not a physical noise threshold. Common small rescaling is allowed.', numericTieTolerance: DELAY_TIE_TOLERANCE, tieRule: 'Compute the global maximum score, retain lags with absolute correlation >= maximum minus 1e-12, then choose the smallest absolute lag and finally the smallest signed lag. This deterministic representative does not resolve periodic ambiguity.', ambiguity: 'boundary peak, or separated local maximum within 0.01 of best absolute correlation; best <0.2 undefined', compensation: 'None: delay estimate does not align any other metric.'},
      referenceStatus: 'Analytic software reference; not externally measured ground truth.',
      units: 'Amplitude is arbitrary; PSD amplitude²/Hz; frequency Hz; signed delay samples; phase degrees.',
      reproducibility: 'No timestamps, network calls, global random source, or unrecorded parameter changes. Floating-point replay requires declared tolerances; hashes are not authenticity evidence.'
    };
  }

  function run(input) {
    const params = requireParameters(input);
    const reference = waveform(params, 0), observed = distort(params);
    const outputs = {
      identity: observed.slice(),
      moving_average: movingAverage(observed, params.movingAverageWindow),
      fft_lowpass: fftLowpass(observed, params.sampleRate, params.cutoffHz),
      x6_phase: x6Phase(observed, params.phaseCenterDeg, params.phaseWidthDeg, params.phaseMode)
    };
    const analysis = {};
    METHODS.forEach(function (method) { analysis[method] = evaluate(reference, outputs[method], params.sampleRate, params.acceptance); });
    return {
      version: VERSION, parameters: params,
      source: {type: 'synthetic', reference: 'known analytic waveform at zero impairment', generator: 'X6SignalLab ' + VERSION, measuredData: false, seed: params.seed},
      arrays: {time: Array.from({length: params.samples}, (_, i) => i / params.sampleRate), reference: reference, observed: observed, outputs: outputs},
      analysis: analysis, methodology: methodology(params), evidenceClass: 'SYNTHETIC_RESULT'
    };
  }

  function runCounterexamples() {
    const cases = [];
    function append(id, description, reference, candidate, expected, checksFn, extra) {
      const params = requireParameters(Object.assign({signal: 'sine', samples: reference.length, sampleRate: 512, frequency: 32, noiseStd: 0}, extra || {}));
      const analysis = evaluate(reference, candidate, params.sampleRate, params.acceptance);
      const checks = checksFn(analysis);
      const result = {
        version: VERSION, parameters: params,
        source: {type: 'synthetic counterexample', generator: 'X6SignalLab ' + VERSION, measuredData: false, construction: description, replay: 'runCounterexamples() selects the fixed construction recipe by case ID. These case parameters describe sampling/screening and do not by themselves regenerate the supplied candidate via run(parameters).'},
        arrays: {time: reference.map((_, i) => i / params.sampleRate), reference: reference.slice(), observed: candidate.slice(), outputs: {identity: candidate.slice()}},
        analysis: {identity: analysis}, methodology: methodology(params), evidenceClass: 'SYNTHETIC_RESULT'
      };
      cases.push({id: id, description: description, result: result, expected: expected, checks: checks, passed: checks.every(c => c.passed)});
    }
    const tone = Array.from({length: 512}, (_, i) => Math.sin(TAU * 32 * i / 512));
    const close = (x, y, tolerance) => x !== null && Math.abs(x - y) <= tolerance;
    const check = (id, passed, reason) => ({id: id, passed: Boolean(passed), reason: reason});
    append('polarity_inversion', 'Candidate y=-x for a coherent bin-centered sinusoid.', tone, tone.map(v => -v), 'PSD and coherence agree while time error and 180-degree phase error reject the signal.', function (a) {
      return [check('nrmse_two', close(a.metrics.nrmse.value, 2, 1e-12), 'Analytically NRMSE(-x,x)=2.'), check('psd_false_pass', close(a.metrics.spectral_error.value, 0, 1e-12), 'PSD is invariant under polarity reversal.'), check('coherence_false_pass', close(a.metrics.coherence_mean.value, 1, 1e-12), 'Magnitude-squared coherence is invariant under nonzero constant sign change.'), check('phase_180', close(a.metrics.phase_error_deg.value, 180, 1e-9), 'Cross-phase reveals polarity reversal.'), check('screen_rejects', a.status === 'FAIL', 'A favorable PSD/coherence result cannot override failed fidelity gates.')];
    }, {gain: -1});
    const pulseParams = requireParameters({signal: 'pulse', samples: 512, sampleRate: 512, frequency: 32, noiseStd: 0});
    const pulse = waveform(pulseParams, 0);
    append('positive_delay', 'Gaussian pulse shifted by +7 samples, with zero padding.', pulse, shiftZeroPadded(pulse, 7), 'Signed delay +7 is recovered without aligning the fidelity metrics.', function (a) {
      return [check('delay_plus_seven', a.metrics.delay_samples.status === 'DEFINED' && a.metrics.delay_samples.value === 7, 'Positive means candidate delayed.'), check('unaligned_error', a.metrics.nrmse.value > 0, 'Time-domain fidelity is computed before alignment.'), check('delay_gate_fails', a.gates.find(g => g.id === 'delay_samples').status === 'FAIL', 'Seven samples exceeds the default declared screening limit.')];
    }, {signal: 'pulse', delaySamples: 7});
    append('negative_delay', 'Gaussian pulse shifted by -7 samples, with zero padding.', pulse, shiftZeroPadded(pulse, -7), 'Signed delay -7 is recovered, rather than an absolute or circular delay.', function (a) {
      return [check('delay_minus_seven', a.metrics.delay_samples.status === 'DEFINED' && a.metrics.delay_samples.value === -7, 'Negative means candidate advanced.'), check('unaligned_error', a.metrics.nrmse.value > 0, 'Advancement is retained in the time-domain error.')];
    }, {signal: 'pulse', delaySamples: -7});
    append('clipping', 'Sinusoid hard-clipped to ±0.25 amplitude.', tone, tone.map(v => Math.max(-0.25, Math.min(0.25, v))), 'Clipping changes waveform energy and creates spectral distortion; deterministic dependence does not imply correctness.', function (a) {
      return [check('fidelity_rejects', a.metrics.nrmse.value > 0.5, 'Severe clipping has substantial sample error.'), check('spectral_distortion', a.metrics.spectral_error.value > 0.5, 'Reference and clipped PSDs differ.'), check('screen_rejects', a.status === 'FAIL', 'Clipping is not accepted because selected bins remain coherent.')];
    }, {clipLevel: 0.25});
    append('zero_signal', 'Both reference and candidate are identically zero.', Array(512).fill(0), Array(512).fill(0), 'Zero absolute error is defined; normalized, phase, coherence and delay claims remain undefined.', function (a) {
      return [check('rmse_zero', a.metrics.rmse.value === 0, 'Absolute error exists without a nonzero reference.'), check('nrmse_undefined', a.metrics.nrmse.value === null && a.metrics.nrmse.status === 'UNDEFINED', 'Zero denominator is not converted to a favorable ratio.'), check('spectral_undefined', a.metrics.coherence_mean.value === null && a.metrics.phase_error_deg.value === null, 'No AC content means no defined coherence or phase.'), check('screen_inconclusive', a.status === 'INCONCLUSIVE', 'Undefined gates cannot produce PASS.')];
    }, {signal: 'zero'});
    append('dc_only', 'Reference is constant 1 and candidate constant 2.', Array(512).fill(1), Array(512).fill(2), 'Welch constant detrending removes both DC levels; raw NRMSE and RMS gain must still reject.', function (a) {
      return [check('raw_nrmse_one', close(a.metrics.nrmse.value, 1, 1e-12), 'Raw reference is not centered for fidelity.'), check('gain_100_percent', close(a.metrics.gain_error_pct.value, 100, 1e-12), 'DC amplitude difference remains visible.'), check('detrended_spectrum_undefined', a.metrics.spectral_error.value === null && a.metrics.coherence_mean.value === null, 'No invented zero-error spectral ratio.'), check('screen_rejects', a.status === 'FAIL', 'Time-domain errors remain decisive.')];
    });
    append('periodic_delay_ambiguity', 'Bin-centered sinusoid compared to itself with many equally good periodic lag aliases.', tone, tone.slice(), 'Exact sample agreement does not make the physical lag identifiable from a periodic record.', function (a) {
      return [check('exact_snr_status', a.metrics.snr_db.status === 'EXACT_MATCH' && a.metrics.snr_db.value === null, 'Infinite exact-match SNR has an explicit JSON-safe status.'), check('delay_ambiguous', a.metrics.delay_samples.status === 'AMBIGUOUS' && a.metrics.delay_samples.value === null, 'Competing periodic peaks are reported.'), check('not_vacuous_pass', a.status === 'INCONCLUSIVE', 'Ambiguous delay gate cannot pass.')];
    });
    const removed = x6Phase(tone, 0, 45, 'pass');
    append('x6_clean_signal_removal', 'Original X6 pass filter, center 0°, width 45°, applied to a clean sine whose positive-frequency phase is -90°.', tone, removed, 'The faithful phase filter can remove a clean signal; there is no assumed denoising benefit.', function (a) {
      return [check('clean_signal_removed', close(a.metrics.nrmse.value, 1, 1e-10), 'A zero-like output loses the reference waveform.'), check('rms_removed', a.metrics.gain_error_pct.value < -99.999999, 'Nearly all signal RMS is removed.'), check('screen_rejects', a.status === 'FAIL', 'Failure is displayed instead of being recast as improvement.')];
    });
    const totalChecks = cases.reduce((sum, c) => sum + c.checks.length, 0);
    return {version: VERSION, cases: cases, totalCases: cases.length, totalChecks: totalChecks, passedChecks: cases.reduce((sum, c) => sum + c.checks.filter(check => check.passed).length, 0), passed: cases.every(c => c.passed), evidenceClass: 'SYNTHETIC_RESULT'};
  }

  return Object.freeze({VERSION: VERSION, defaults: defaults, validate: validate, run: run, evaluate: evaluate, runCounterexamples: runCounterexamples});
});
