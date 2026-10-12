'use strict';

const assert = require('node:assert/strict');
const test = require('node:test');
const lab = require('../../app/signal-lab-core.js');
const TAU = 2 * Math.PI;

function close(actual, expected, tolerance = 1e-10) {
  assert.equal(typeof actual, 'number');
  assert.ok(Number.isFinite(actual));
  assert.ok(Math.abs(actual - expected) <= tolerance, `${actual} differs from ${expected} by more than ${tolerance}`);
}

function finiteTree(value) {
  if (typeof value === 'number') assert.ok(Number.isFinite(value), 'No NaN or Infinity may enter evidence.');
  else if (Array.isArray(value)) value.forEach(finiteTree);
  else if (value && typeof value === 'object') Object.values(value).forEach(finiteTree);
}

function sine(n = 512, cycles = 32) {
  return Array.from({length: n}, (_, i) => Math.sin(TAU * cycles * i / n));
}

function shifted(values, lag) {
  return values.map((_, i) => i - lag >= 0 && i - lag < values.length ? values[i - lag] : 0);
}

test('defaults are independent copies and valid; input and acceptance are not mutated', () => {
  const first = lab.defaults(), second = lab.defaults();
  first.acceptance.nrmseMax = 999;
  assert.equal(second.acceptance.nrmseMax, 0.25);
  assert.equal(lab.validate(second).valid, true);
  const input = {seed: 7, acceptance: {nrmseMax: 0.3}};
  const before = JSON.stringify(input);
  lab.run(input);
  assert.equal(JSON.stringify(input), before);
});

test('unknown fields, nonfinite numbers, booleans, invalid grids and aliasing are rejected', () => {
  const invalid = [
    {unknown: 1}, {sampleRate: Infinity}, {sampleRate: true}, {samples: 129},
    {samples: 8192}, {samples: 64}, {seed: -1}, {seed: 4294967296}, {seed: 0.5},
    {gain: NaN}, {gain: true}, {gain: 101}, {noiseStd: -1}, {quantBits: 1},
    {quantBits: 17}, {quantBits: 2.5}, {quantRange: 0}, {quantRange: 1e-320},
    {phaseMode: 'notch'}, {phaseWidthDeg: 361}, {movingAverageWindow: 8},
    {delaySamples: 0.5}, {delaySamples: 65}, {signal: 'sine', frequency: 512},
    {signal: 'multitone', frequency: 205}, {signal: 'chirp', frequency: 0},
    {signal: 'pulse', phaseDeg: 10}, {signal: 'zero', phaseDeg: 90},
    {acceptance: {nrmseMax: true}}, {acceptance: {coherenceMin: 1.1}},
    {acceptance: {unknown: 0}}, {acceptance: null}
  ];
  for (const params of invalid) {
    const validation = lab.validate(params);
    assert.equal(validation.valid, false, JSON.stringify(params));
    assert.equal(validation.parameters, null);
    finiteTree(validation);
    assert.throws(() => lab.run(params), RangeError);
  }
});

test('evaluation rejects sparse arrays, extra properties, malformed lengths and sample values', () => {
  const dense = Array(128).fill(1);
  assert.throws(() => lab.evaluate(new Array(128), dense, 128), RangeError);
  const partial = dense.slice(); delete partial[63];
  assert.throws(() => lab.evaluate(partial, dense, 128), RangeError);
  const extra = dense.slice(); extra.secret = 1;
  assert.throws(() => lab.evaluate(extra, dense, 128), RangeError);
  const symbols = dense.slice(); symbols[Symbol('extra')] = 1;
  assert.throws(() => lab.evaluate(symbols, dense, 128), RangeError);
  for (const bad of [NaN, Infinity, '1', true, 1e13]) {
    const candidate = dense.slice(); candidate[7] = bad;
    assert.throws(() => lab.evaluate(dense, candidate, 128), RangeError);
  }
  assert.throws(() => lab.evaluate(dense, dense.slice(1), 128), RangeError);
  assert.throws(() => lab.evaluate(dense, dense, false), RangeError);
  assert.throws(() => lab.evaluate(dense, dense, 128, {coherenceMin: true}), RangeError);
});

test('seeded runs replay exactly and nominal Gaussian noise is not renormalized per record', () => {
  const p = {signal: 'zero', samples: 128, sampleRate: 1024, seed: 104729, noiseStd: 0.3};
  const a = lab.run(p), b = lab.run(p), changed = lab.run({...p, seed: 104730});
  assert.deepEqual(a, b);
  assert.notDeepEqual(a.arrays.observed, changed.arrays.observed);
  assert.deepEqual(a.arrays.reference, Array(128).fill(0));
  const average = a.arrays.observed.reduce((s, v) => s + v, 0) / 128;
  const sigma = Math.sqrt(a.arrays.observed.reduce((s, v) => s + (v - average) ** 2, 0) / 128);
  assert.ok(Math.abs(sigma - 0.3) > 1e-6, 'Nominal standard deviation must not imply exact per-record normalization.');
  finiteTree(a);
});

test('identity output is the exact observation, with clean nonzero SNR explicitly infinite', () => {
  const r = lab.run({signal: 'pulse', noiseStd: 0});
  assert.deepEqual(r.arrays.outputs.identity, r.arrays.observed);
  assert.deepEqual(r.arrays.reference, r.arrays.observed);
  assert.equal(r.analysis.identity.metrics.nrmse.value, 0);
  assert.equal(r.analysis.identity.metrics.snr_db.status, 'EXACT_MATCH');
  assert.equal(r.analysis.identity.metrics.snr_db.value, null);
  assert.equal(r.analysis.identity.status, 'PASS');
});

test('analytic inversion: NRMSE 2, PSD error 0, coherence 1, phase error 180 degrees', () => {
  const x = sine(), a = lab.evaluate(x, x.map(v => -v), 512);
  close(a.metrics.nrmse.value, 2, 1e-12);
  close(a.metrics.snr_db.value, -20 * Math.log10(2), 1e-12);
  close(a.metrics.gain_error_pct.value, 0, 1e-12);
  close(a.metrics.spectral_error.value, 0, 1e-12);
  close(a.metrics.coherence_mean.value, 1, 1e-12);
  close(a.metrics.phase_error_deg.value, 180, 1e-10);
  assert.equal(a.status, 'FAIL');
});

test('gain of two has analytic NRMSE 1, RMS gain +100%, PSD L1 error 3', () => {
  const x = sine(), a = lab.evaluate(x, x.map(v => 2 * v), 512);
  close(a.metrics.nrmse.value, 1, 1e-12);
  close(a.metrics.gain_error_pct.value, 100, 1e-12);
  close(a.metrics.spectral_error.value, 3, 1e-12);
  close(a.metrics.coherence_mean.value, 1, 1e-12);
  close(a.metrics.phase_error_deg.value, 0, 1e-12);
});

test('periodic-Hann Welch has analytic bin power, neighboring bins and integrated sine power', () => {
  const a = lab.evaluate(sine(), sine(), 512), s = a.spectrum;
  const bin = s.frequencies.indexOf(32);
  assert.equal(s.estimator.nperseg, 256);
  assert.equal(s.estimator.segments, 3);
  close(s.referencePSD[bin], 1 / 6, 1e-12);
  close(s.referencePSD[bin - 1], 1 / 24, 1e-12);
  close(s.referencePSD[bin + 1], 1 / 24, 1e-12);
  close(s.referencePSD.reduce((sum, p) => sum + p, 0) * 2, 0.5, 1e-12);
});

test('cross-spectrum convention gives +90 degrees from sine reference to cosine candidate', () => {
  const x = sine(), y = Array.from({length: 512}, (_, i) => Math.cos(TAU * 32 * i / 512));
  const a = lab.evaluate(x, y, 512), bin = a.spectrum.frequencies.indexOf(32);
  close(a.spectrum.phaseDeg[bin], 90, 1e-10);
  close(a.spectrum.crossSpectrumReal[bin], 0, 1e-12);
  close(a.spectrum.crossSpectrumImag[bin], 1 / 6, 1e-12);
  close(a.metrics.phase_error_deg.value, 90, 1e-10);
});

test('Gaussian positive and negative zero-padded delays retain sign and unaligned fidelity error', () => {
  const x = lab.run({signal: 'pulse', samples: 512, sampleRate: 512, noiseStd: 0}).arrays.reference;
  for (const lag of [-7, 7]) {
    const a = lab.evaluate(x, shifted(x, lag), 512);
    assert.equal(a.metrics.delay_samples.status, 'DEFINED');
    assert.equal(a.metrics.delay_samples.value, lag);
    assert.ok(a.metrics.nrmse.value > 0.1);
    assert.equal(a.gates.find(g => g.id === 'delay_samples').status, 'FAIL');
  }
  const boundary = lab.evaluate(x, shifted(x, 64), 512);
  assert.equal(boundary.metrics.delay_samples.status, 'AMBIGUOUS');
  assert.equal(boundary.metrics.delay_samples.value, null);
});

test('periodic aliases produce ambiguous delay, even for exact matching records', () => {
  const x = sine(), a = lab.evaluate(x, x, 512);
  assert.equal(a.metrics.delay_samples.status, 'AMBIGUOUS');
  assert.equal(a.metrics.delay_samples.value, null);
  assert.equal(a.delay.bestLagSamples, 0, 'Numerically tied periodic peaks use the deterministic smallest-absolute-lag representative.');
  assert.ok(a.delay.competingLags.length > 0);
  assert.equal(a.status, 'INCONCLUSIVE');
});

test('zero and arbitrary decimal DC do not invent normalized spectral or delay success', () => {
  for (const c of [0, 0.1, -0.3, 2]) {
    const x = Array(128).fill(c), a = lab.evaluate(x, x, 128);
    assert.equal(a.metrics.rmse.value, 0);
    assert.equal(a.metrics.spectral_error.value, null);
    assert.equal(a.metrics.coherence_mean.value, null);
    assert.equal(a.metrics.phase_error_deg.value, null);
    assert.equal(a.metrics.delay_samples.value, null);
    assert.equal(a.status, 'INCONCLUSIVE');
    assert.ok(a.spectrum.referencePSD.every(p => p === 0));
    assert.ok(a.spectrum.coherence.every(p => p === null));
    if (c === 0) assert.equal(a.metrics.nrmse.value, null);
    finiteTree(a);
  }
});

test('DC mismatch is rejected by raw metrics despite detrended spectral absence', () => {
  const a = lab.evaluate(Array(128).fill(1), Array(128).fill(2), 128);
  close(a.metrics.nrmse.value, 1, 1e-12);
  close(a.metrics.gain_error_pct.value, 100, 1e-12);
  assert.equal(a.metrics.spectral_error.status, 'UNDEFINED');
  assert.equal(a.status, 'FAIL');
});

test('tiny nonzero norms do not underflow into an exact-match SNR claim', () => {
  const x = Array(128).fill(1e-250), y = x.map(v => 2 * v);
  const a = lab.evaluate(x, y, 128);
  close(a.metrics.nrmse.value, 1, 1e-12);
  close(a.metrics.snr_db.value, 0, 1e-10);
  assert.equal(a.metrics.snr_db.status, 'DEFINED');
  assert.equal(a.metrics.spectral_error.status, 'UNDEFINED');
  finiteTree(a);
});

test('zero candidate has undefined coherence and phase, and an explicit fidelity failure', () => {
  const x = sine(), a = lab.evaluate(x, x.map(() => 0), 512);
  close(a.metrics.nrmse.value, 1, 1e-12);
  close(a.metrics.gain_error_pct.value, -100, 1e-12);
  assert.equal(a.metrics.coherence_mean.value, null);
  assert.equal(a.metrics.phase_error_deg.value, null);
  assert.equal(a.status, 'FAIL');
});

test('declared pairwise dynamic range excludes negligible residuals without inventing decoherence', () => {
  const x = lab.run({signal: 'pulse', samples: 512, sampleRate: 512, noiseStd: 0}).arrays.reference;
  const tiny = x.map(v => v * 1e-14);
  for (const pair of [[x, tiny], [tiny, x]]) {
    const a = lab.evaluate(pair[0], pair[1], 512);
    assert.equal(a.metrics.coherence_mean.status, 'UNDEFINED');
    assert.equal(a.metrics.phase_error_deg.status, 'UNDEFINED');
    assert.equal(a.metrics.delay_samples.status, 'UNDEFINED');
    assert.ok(a.spectrum.coherence.every(v => v === null));
    assert.ok(a.spectrum.phaseDeg.every(v => v === null));
    assert.ok(a.delay.correlationByLag.every(v => v.correlation === null));
    assert.ok(a.spectrum.referencePSD.some(v => v > 0));
    assert.ok(a.spectrum.outputPSD.some(v => v > 0));
    assert.equal(a.metrics.nrmse.status, 'DEFINED');
    assert.equal(a.metrics.gain_error_pct.status, 'DEFINED');
    assert.equal(a.metrics.spectral_error.status, 'DEFINED');
    finiteTree(a);
  }
  const eligible = lab.evaluate(x, x.map(v => v * 1e-8), 512);
  close(eligible.metrics.coherence_mean.value, 1, 1e-12);
  close(eligible.metrics.phase_error_deg.value, 0, 1e-8);
  assert.equal(eligible.metrics.coherence_mean.status, 'DEFINED');
  assert.equal(eligible.metrics.delay_samples.status, 'DEFINED');
  assert.equal(eligible.metrics.delay_samples.value, 0);
  assert.equal(eligible.status, 'FAIL', 'Coherence eligibility does not mean acceptable amplitude fidelity.');
});

test('common tiny scaling preserves normalized coherence and delay while raw PSD stays tiny', () => {
  const x = lab.run({signal: 'pulse', samples: 512, sampleRate: 512, noiseStd: 0}).arrays.reference;
  const normal = lab.evaluate(x, shifted(x, 7), 512);
  const a = lab.evaluate(x.map(v => v * 1e-100), shifted(x, 7).map(v => v * 1e-100), 512);
  close(a.metrics.coherence_mean.value, normal.metrics.coherence_mean.value, 1e-10);
  close(a.metrics.phase_error_deg.value, normal.metrics.phase_error_deg.value, 1e-8);
  close(a.metrics.nrmse.value, normal.metrics.nrmse.value, 1e-12);
  assert.equal(a.metrics.delay_samples.status, 'DEFINED');
  assert.equal(a.metrics.delay_samples.value, 7);
  const ratio = Math.max(...a.spectrum.referencePSD) / Math.max(...normal.spectrum.referencePSD);
  close(ratio, 1e-200, 1e-212);
  finiteTree(a);
});

test('X6 clean-removal roundoff remains in raw arrays but cannot create phase/coherence/delay claims', () => {
  const suite = lab.runCounterexamples();
  const c = suite.cases.find(c => c.id === 'x6_clean_signal_removal');
  const a = c.result.analysis.identity;
  assert.ok(c.result.arrays.observed.some(v => v !== 0), 'Do not replace the faithful FFT residual with invented zeros.');
  assert.ok(a.spectrum.outputPSD.some(v => v > 0), 'Raw PSD remains an unmodified computed array.');
  assert.ok(a.spectrum.numericalGuard.peakPowerRatio < 1e-24);
  assert.ok(a.delay.numericalGuard.centeredNormRatio < 1e-12);
  assert.ok(a.spectrum.phaseDeg.every(v => v === null));
  assert.ok(a.spectrum.coherence.every(v => v === null));
  assert.ok(a.delay.correlationByLag.every(v => v.correlation === null));
  assert.equal(a.metrics.coherence_mean.status, 'UNDEFINED');
  assert.equal(a.metrics.phase_error_deg.status, 'UNDEFINED');
  assert.equal(a.metrics.delay_samples.status, 'UNDEFINED');
  close(a.metrics.nrmse.value, 1, 1e-10);
  assert.equal(a.status, 'FAIL');
});

test('moving average renormalizes finite edges rather than zero-padding the denominator', () => {
  const r = lab.run({signal: 'pulse', samples: 128, sampleRate: 128, noiseStd: 0, movingAverageWindow: 9, cutoffHz: 32});
  const x = r.arrays.observed, y = r.arrays.outputs.moving_average;
  close(y[0], x.slice(0, 5).reduce((sum, v) => sum + v, 0) / 5, 1e-15);
  close(y[127], x.slice(123).reduce((sum, v) => sum + v, 0) / 5, 1e-15);
  close(y[64], x.slice(60, 69).reduce((sum, v) => sum + v, 0) / 9, 1e-15);
});

test('FFT low-pass agrees with a direct periodic Fourier-series reconstruction', () => {
  const r = lab.run({signal: 'pulse', samples: 128, sampleRate: 128, noiseStd: 0, cutoffHz: 8});
  const x = r.arrays.observed, n = x.length, expected = Array(n).fill(0);
  // Independent O(N^2) Fourier definition; no FFT algorithm or core internals reused.
  for (let k = -8; k <= 8; k++) {
    let re = 0, im = 0;
    for (let j = 0; j < n; j++) { re += x[j] * Math.cos(TAU * k * j / n); im -= x[j] * Math.sin(TAU * k * j / n); }
    for (let j = 0; j < n; j++) expected[j] += (re * Math.cos(TAU * k * j / n) - im * Math.sin(TAU * k * j / n)) / n;
  }
  r.arrays.outputs.fft_lowpass.forEach((v, i) => close(v, expected[i], 2e-12));
});

test('X6 full-width pass preserves observations and pass/stop remain complementary', () => {
  const p = {samples: 128, seed: 42, phaseCenterDeg: 17, phaseWidthDeg: 43};
  const pass = lab.run({...p, phaseMode: 'pass'}), stop = lab.run({...p, phaseMode: 'stop'});
  pass.arrays.observed.forEach((v, i) => close(pass.arrays.outputs.x6_phase[i] + stop.arrays.outputs.x6_phase[i], v, 1e-12));
  const full = lab.run({...p, phaseWidthDeg: 360});
  full.arrays.observed.forEach((v, i) => close(full.arrays.outputs.x6_phase[i], v, 1e-12));
});

test('faithful X6 phase selection removes clean sine at center zero and preserves it at minus ninety', () => {
  const p = {signal: 'sine', samples: 512, sampleRate: 512, frequency: 32, noiseStd: 0, phaseWidthDeg: 45};
  const removed = lab.run({...p, phaseCenterDeg: 0}), kept = lab.run({...p, phaseCenterDeg: -90});
  close(removed.analysis.x6_phase.metrics.nrmse.value, 1, 1e-10);
  close(kept.analysis.x6_phase.metrics.nrmse.value, 0, 1e-12);
  assert.equal(removed.analysis.x6_phase.status, 'FAIL');
});

test('signed quantizer clips to its declared asymmetric code endpoints and keeps zero exact', () => {
  const r = lab.run({signal: 'sine', samples: 128, sampleRate: 128, frequency: 8, amplitude: 3, noiseStd: 0, quantBits: 3, quantRange: 1, cutoffHz: 32});
  assert.equal(Math.min(...r.arrays.observed), -1);
  assert.equal(Math.max(...r.arrays.observed), 0.75);
  assert.ok(r.arrays.observed.every(v => Number.isInteger(v / 0.25)));
  const z = lab.run({signal: 'zero', samples: 128, noiseStd: 0, quantBits: 2, quantRange: 1});
  assert.ok(z.arrays.observed.every(v => v === 0));
});

test('all eight counterexamples contain full arrays and 27 independently evaluated checks pass', () => {
  const suite = lab.runCounterexamples();
  assert.equal(suite.totalCases, 8);
  assert.equal(suite.totalChecks, 27);
  assert.equal(suite.passedChecks, 27);
  assert.equal(suite.passed, true);
  for (const c of suite.cases) {
    assert.equal(c.result.arrays.reference.length, 512);
    assert.equal(c.result.arrays.observed.length, 512);
    assert.equal(c.result.arrays.time.length, 512);
    assert.deepEqual(c.result.arrays.observed, c.result.arrays.outputs.identity);
    assert.ok(c.result.source.replay.includes('runCounterexamples'));
  }
  assert.deepEqual(suite, lab.runCounterexamples());
  finiteTree(suite);
  assert.ok(JSON.stringify(suite).length < 1e6);
});

test('practical maximum input ranges remain finite and Welch always has multiple segments', () => {
  const r = lab.run({signal: 'multitone', samples: 4096, sampleRate: 1e7, frequency: 1e5, amplitude: 1e6, gain: 100, noiseStd: 1e6, clipLevel: 1e9, quantBits: 16, quantRange: 1e9, cutoffHz: 5e6});
  finiteTree(r);
  for (const a of Object.values(r.analysis)) assert.equal(a.spectrum.estimator.segments, 31);
  const small = lab.run({samples: 128});
  for (const a of Object.values(small.analysis)) assert.equal(a.spectrum.estimator.segments, 3);
});
