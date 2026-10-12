'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const core = require('../../app/signal-lab-core.js');
const evidence = require('../../app/signal-lab-evidence.js');
const build = require('../../app/signal-lab-build.js');
const results = [];
const clone = x => JSON.parse(JSON.stringify(x));
const hash = x => crypto.createHash('sha256').update(evidence.canonical(x)).digest('hex');
async function test(name, fn) {
  try { await fn(); results.push({ name, passed: true }); }
  catch (error) { results.push({ name, passed: false, error: error.stack }); }
}
async function rejectChanged(original, fn, pattern = /./) {
  const edited = clone(original);
  fn(edited.payload);
  edited.integrity.sha256 = hash(edited.payload);
  await assert.rejects(evidence.verifyAndReplay(edited), pattern);
}

(async () => {
  const params = { ...core.defaults(), samples: 256, noiseStd: 0.1 };
  const run = core.run(params);
  const original = await evidence.create(run);
  await test('SHA-256 abc published test vector', async () => {
    assert.equal(await evidence.sha256('abc'), 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad');
  });
  await test('canonical JSON ignores object insertion order, preserves arrays', () => {
    assert.equal(evidence.canonical({ z: 2, a: [3, 1] }), evidence.canonical({ a: [3, 1], z: 2 }));
    assert.notEqual(evidence.canonical([3, 1]), evidence.canonical([1, 3]));
  });
  await test('every declared runtime source hash matches bytes', () => {
    for (const [name, expected] of Object.entries(build.files)) {
      const bytes = fs.readFileSync(path.resolve(__dirname, '../..', name));
      assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'), expected, name);
    }
    assert.equal(hash(build.files), build.bundle_sha256);
  });
  await test('complete evidence survives JSON export and computational replay', async () => {
    const replay = await evidence.verifyAndReplay(JSON.stringify(original));
    assert.equal(replay.verification.passed, true);
    assert.equal(replay.verification.authenticity, 'NOT_ASSESSED');
    assert.deepEqual(replay.result, run);
    assert.equal(replay.suite, null);
  });
  await test('changed bytes fail SHA-256 before replay', async () => {
    const edited = clone(original);
    edited.payload.result.arrays.observed[7] += 0.5;
    await assert.rejects(evidence.verifyAndReplay(edited), /SHA-256 mismatch/);
  });
  await test('rehashing a forged output still fails computational replay', async () => {
    await rejectChanged(original, p => { p.result.arrays.outputs.identity[7] += 0.5; }, /Replay numerical mismatch/);
  });
  await test('rehashing a forged reference still fails computational replay', async () => {
    await rejectChanged(original, p => { p.result.arrays.reference[7] += 0.5; }, /Replay numerical mismatch/);
  });
  await test('rehashing a forged reported metric still fails replay', async () => {
    await rejectChanged(original, p => { p.result.analysis.identity.metrics.nrmse.value = 0; }, /Replay numerical mismatch/);
  });
  await test('changed seed cannot retain old arrays', async () => {
    await rejectChanged(original, p => { p.result.parameters.seed += 1; }, /Replay/);
  });
  await test('null and zero have different metric meanings', async () => {
    const zero = await evidence.create(core.run({ ...core.defaults(), samples: 256, signal: 'zero', noiseStd: 0 }));
    await rejectChanged(zero, p => { p.result.analysis.identity.metrics.nrmse.value = 0; }, /Replay/);
  });
  await test('changed result lengths are rejected', async () => {
    await rejectChanged(original, p => { p.result.arrays.reference.pop(); }, /Replay fields mismatch/);
  });
  await test('evidence cannot widen its own replay tolerance', async () => {
    await rejectChanged(original, p => { p.replay.absolute_tolerance = 1e20; }, /tolerance policy/);
    await rejectChanged(original, p => { p.replay.phase_tolerance_degrees = 180; }, /tolerance policy/);
  });
  await test('weak-bin phase roundoff has a separate fixed degree tolerance', async () => {
    const edited = clone(original);
    const values = edited.payload.result.analysis.identity.spectrum.phaseDeg;
    const index = values.findIndex(value => value !== null && Math.abs(value) < 170);
    assert.ok(index >= 0); values[index] += 5e-7;
    edited.integrity.sha256 = hash(edited.payload);
    assert.equal((await evidence.verifyAndReplay(edited)).verification.passed, true);
    values[index] += 0.001; edited.integrity.sha256 = hash(edited.payload);
    await assert.rejects(evidence.verifyAndReplay(edited), /Replay numerical mismatch/);
  });
  await test('wrapped phase representation remains within its declared range', async () => {
    await rejectChanged(original, p => {
      const values = p.result.analysis.identity.spectrum.phaseDeg;
      const index = values.findIndex(value => value !== null); values[index] += 720;
    }, /outside wrapped range/);
  });
  await test('synthetic evidence cannot be relabeled recorded or measured', async () => {
    await rejectChanged(original, p => { p.evidence_class = 'MEASURED_RESULT'; }, /evidence class/);
  });
  await test('unsupported engine versions fail explicitly', async () => {
    await rejectChanged(original, p => { p.engine_version = '999.0.0'; }, /engine version/);
  });
  await test('source revision drift cannot be silently replayed', async () => {
    await rejectChanged(original, p => { p.source.bundle_sha256 = '1'.repeat(64); }, /Source revision mismatch/);
  });
  await test('removing the limitations cannot yield verified evidence', async () => {
    await rejectChanged(original, p => { p.limitations = []; }, /limitations/);
  });
  await test('invalid declared timestamp rejected even with matching digest', async () => {
    await rejectChanged(original, p => { p.created_utc = '2026-02-30T12:00:00.000Z'; }, /timestamp/);
  });
  await test('unknown envelope fields do not disappear silently', async () => {
    await assert.rejects(evidence.verifyAndReplay({ ...original, certified: true }), /envelope fields/);
  });
  await test('snapshot precedes asynchronous hashing and caller mutation', async () => {
    const mutable = clone(run);
    const pending = evidence.create(mutable);
    mutable.arrays.observed[0] = 999;
    mutable.parameters.seed = 0;
    const fixed = await pending;
    assert.deepEqual(fixed.payload.result, run);
    await evidence.verifyAndReplay(fixed);
  });
  await test('forged completed runs cannot be exported as fresh evidence', async () => {
    const forged = clone(run);
    forged.arrays.outputs.x6_phase[3] = 999;
    await assert.rejects(evidence.create(forged), /Replay/);
  });
  await test('non-finite, undefined, sparse and cyclic values are rejected', () => {
    for (const value of [NaN, Infinity, -Infinity, undefined, [undefined], new Date(), [1, , 2]]) {
      assert.throws(() => evidence.canonical(value));
    }
    const cyclic = {}; cyclic.self = cyclic;
    assert.throws(() => evidence.canonical(cyclic), /cycle/);
    assert.throws(() => evidence.canonical(JSON.parse('{"__proto__":{"value":1}}')), /Reserved/);
  });
  await test('CSV contains every actual sample and all four actual method arrays', () => {
    const lines = evidence.toCSV(run).trim().split('\n');
    assert.equal(lines[0], 'index,time_s,reference,observed,identity,moving_average,fft_lowpass,x6_phase');
    assert.equal(lines.length, run.parameters.samples + 1);
    for (let i = 0; i < run.parameters.samples; i++) {
      const cells = lines[i + 1].split(',').map(Number);
      assert.deepEqual(cells, [i, run.arrays.time[i], run.arrays.reference[i], run.arrays.observed[i],
        ...['identity', 'moving_average', 'fft_lowpass', 'x6_phase'].map(m => run.arrays.outputs[m][i])]);
    }
  });
  await test('full counterexample evidence preserves every case and replays', async () => {
    const suite = core.runCounterexamples();
    assert.equal(suite.passed, true);
    const exported = await evidence.create(run, suite);
    const replay = await evidence.verifyAndReplay(exported);
    assert.deepEqual(replay.suite, suite);
    assert.ok(JSON.stringify(exported).length < evidence.MAX_BYTES);
    const inverse = exported.payload.counterexamples.cases.find(c => c.id === 'polarity_inversion');
    const phases = inverse.result.analysis.identity.spectrum.phaseDeg;
    const index = phases.findIndex(value => value !== null && Math.abs(Math.abs(value) - 180) < 1e-10);
    assert.ok(index >= 0); phases[index] *= -1;
    exported.integrity.sha256 = hash(exported.payload);
    assert.equal((await evidence.verifyAndReplay(exported)).verification.passed, true);
  });
  const report = { schema: 'x6.signal-lab.evidence-tests/1', status: results.every(x => x.passed) ? 'PASS' : 'FAIL',
    total: results.length, passed: results.filter(x => x.passed).length, cases: results };
  process.stdout.write(JSON.stringify(report, null, 2) + '\n');
  if (report.status !== 'PASS') process.exitCode = 1;
})().catch(error => { process.stderr.write(error.stack + '\n'); process.exitCode = 1; });
