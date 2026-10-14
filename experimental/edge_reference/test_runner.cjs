/* Copyright 2026 Thomas Gfeller. SPDX-License-Identifier: Apache-2.0 */
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const {spawnSync} = require('node:child_process');
const runner = require('./runner.cjs');
const evidence = require('../../app/signal-lab-evidence.js');
const baseJob = JSON.parse(fs.readFileSync(path.join(__dirname, 'examples/synthetic-signal.json')));
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');

async function fixture(t, job = baseJob) {
  const parent = fs.mkdtempSync(path.join(os.tmpdir(), 'x6-edge-'));
  t.after(() => fs.rmSync(parent, {recursive: true, force: true}));
  const input = path.join(parent, 'job.json'), out = path.join(parent, 'result');
  fs.writeFileSync(input, JSON.stringify(job));
  await runner.run(input, out);
  return {parent, input, out};
}
function mutate(out, name, fn, rehash = false) {
  const file = path.join(out, name), data = JSON.parse(fs.readFileSync(file));
  fn(data); fs.writeFileSync(file, JSON.stringify(data));
  if (rehash) {
    const recordPath = path.join(out, 'run.json'), record = JSON.parse(fs.readFileSync(recordPath));
    record.files[name] = hash(fs.readFileSync(file));
    fs.writeFileSync(recordPath, JSON.stringify(record));
  }
}

test('CLI runs from another cwd and verifies its complete exported directory', async t => {
  const {parent, input} = await fixture(t);
  const out = path.join(parent, 'cli');
  const script = path.join(__dirname, 'runner.cjs');
  for (const args of [['run', input, out], ['verify', out]]) {
    const result = spawnSync(process.execPath, [script, ...args], {cwd: parent, encoding: 'utf8', timeout: 20000});
    assert.equal(result.status, 0, result.stderr);
    assert.equal(JSON.parse(result.stdout).validation, 'REPLAY_PASS');
  }
});
test('invalid job and unknown fields are rejected before output creation', async t => {
  const {parent} = await fixture(t);
  for (const [i, job] of [{...baseJob, parameters: {samples: 129}}, {...baseJob, extra: true},
    {...baseJob, schema: 'future'}, {...baseJob, parameters: {seed: NaN}}, {...baseJob, parameters: {samples: 8192}}].entries()) {
    const input = path.join(parent, 'bad.json'), out = path.join(parent, 'bad-' + i);
    fs.writeFileSync(input, JSON.stringify(job));
    await assert.rejects(runner.run(input, out)); assert.equal(fs.existsSync(out), false);
  }
});
test('oversized input is rejected', async t => {
  const {parent} = await fixture(t), file = path.join(parent, 'large.json');
  fs.writeFileSync(file, ' '.repeat(65537));
  await assert.rejects(runner.run(file, path.join(parent, 'large')), /size limit/);
});
test('existing output cannot be overwritten', async t => {
  const {input, out} = await fixture(t), before = fs.readFileSync(path.join(out, 'run.json'));
  await assert.rejects(runner.run(input, out), /EEXIST/);
  assert.deepEqual(fs.readFileSync(path.join(out, 'run.json')), before);
});
test('changed evidence bytes are detected', async t => {
  const {out} = await fixture(t);
  mutate(out, 'evidence.json', d => {d.payload.result.arrays.observed[0] += 1;});
  await assert.rejects(runner.verify(out), /SHA-256 mismatch/);
});
test('rehashing a forged numerical result cannot bypass computational replay', async t => {
  const {out} = await fixture(t);
  mutate(out, 'evidence.json', d => {
    d.payload.result.arrays.outputs.identity[0] += 1;
    d.integrity.sha256 = hash(evidence.canonical(d.payload));
  }, true);
  await assert.rejects(runner.verify(out), /Replay numerical mismatch/);
});
test('rehashing a changed job cannot detach it from the evidence', async t => {
  const {out} = await fixture(t);
  mutate(out, 'input.json', d => {d.parameters.seed += 1;}, true);
  await assert.rejects(runner.verify(out), /parameters disagree/);
});
test('source revision mismatch is rejected', async t => {
  const {out} = await fixture(t);
  mutate(out, 'run.json', d => {d.sources['experimental/edge_reference/runner.cjs'] = '0'.repeat(64);});
  await assert.rejects(runner.verify(out), /source revision mismatch/);
});
test('inventory cannot introduce an arbitrary file path', async t => {
  const {out} = await fixture(t);
  mutate(out, 'run.json', d => {d.files['../outside'] = '0'.repeat(64);});
  await assert.rejects(runner.verify(out), /file inventory/);
});
test('quality FAIL or INCONCLUSIVE is not rewritten as scientific PASS', async t => {
  const {out} = await fixture(t, {...baseJob, parameters: {signal: 'zero', samples: 128, noiseStd: 0}});
  const report = await runner.verify(out);
  assert.equal(report.validation, 'REPLAY_PASS');
  assert.equal(report.quality_status.identity, 'INCONCLUSIVE');
  assert.equal(report.physical_validation, 'NOT_PERFORMED');
  mutate(out, 'run.json', d => {d.quality_status.identity = 'PASS';});
  await assert.rejects(runner.verify(out), /quality status mismatch/);
});
test('missing completion record is not accepted', async t => {
  const {out} = await fixture(t);
  fs.unlinkSync(path.join(out, 'run.json'));
  await assert.rejects(runner.verify(out), /ENOENT/);
});
