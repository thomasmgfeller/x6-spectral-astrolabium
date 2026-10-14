#!/usr/bin/env node
/* Copyright 2026 Thomas Gfeller. SPDX-License-Identifier: Apache-2.0 */
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const core = require('../../app/signal-lab-core.js');
const evidence = require('../../app/signal-lab-evidence.js');
const root = path.resolve(__dirname, '../..');
const VERSION = '0.1.0';
const FILES = ['input.json', 'evidence.json'];
const SOURCES = ['experimental/edge_reference/runner.cjs', 'app/signal-lab-core.js',
  'app/signal-lab-evidence.js', 'app/signal-lab-build.js'];
const digest = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const encode = value => evidence.canonical(value) + '\n';

function read(filename, limit) {
  const info = fs.lstatSync(filename);
  if (!info.isFile() || info.isSymbolicLink() || info.size > limit) {
    throw new Error('Expected a regular file within its size limit: ' + path.basename(filename));
  }
  const bytes = fs.readFileSync(filename);
  if (bytes.length > limit) throw new Error('Input exceeds size limit');
  return bytes;
}

function keys(value, expected, label) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('Invalid ' + label);
  assert.deepEqual(Object.keys(value).sort(), expected.slice().sort(), 'Unexpected ' + label + ' fields');
}

function jobFrom(bytes) {
  const job = JSON.parse(bytes.toString('utf8'));
  keys(job, ['schema', 'job_id', 'parameters'], 'job');
  if (job.schema !== 'x6.edge-reference.job/0.1' || typeof job.job_id !== 'string' ||
      !/^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$/.test(job.job_id)) throw new Error('Unsupported job schema or ID');
  const checked = core.validate(job.parameters);
  if (!checked.valid) throw new Error('Invalid parameters: ' + JSON.stringify(checked.errors));
  // Apply the same finite-JSON restrictions as evidence export.
  evidence.canonical(job);
  return {job, parameters: checked.parameters};
}

function sources() {
  return Object.fromEntries(SOURCES.map(name => [name, digest(read(path.join(root, name), 2 * 1024 * 1024))]));
}

async function run(input, directory) {
  const bytes = read(input, 65536);
  const {job, parameters} = jobFrom(bytes);
  const started = new Date().toISOString();
  const sourceHashes = sources();
  const result = core.run(parameters);
  const doc = await evidence.create(result);
  const replay = await evidence.verifyAndReplay(doc);
  const exported = Buffer.from(encode(doc));
  const record = {
    schema: 'x6.edge-reference.run/0.1', runner_version: VERSION, job_id: job.job_id,
    execution_status: 'EXECUTED', validation_status: 'REPLAY_PASS',
    evidence_class: 'SYNTHETIC_RESULT', started_utc: started, finished_utc: new Date().toISOString(),
    environment: {node: process.version, v8: process.versions.v8, platform: process.platform, arch: process.arch},
    files: {'input.json': digest(bytes), 'evidence.json': digest(exported)},
    sources: sourceHashes, verification: replay.verification,
    quality_status: Object.fromEntries(Object.entries(result.analysis).map(([name, value]) => [name, value.status]))
  };
  // Directory creation is exclusive. run.json is written last as the completion record.
  fs.mkdirSync(directory, {recursive: false});
  fs.writeFileSync(path.join(directory, 'input.json'), bytes, {flag: 'wx'});
  fs.writeFileSync(path.join(directory, 'evidence.json'), exported, {flag: 'wx'});
  fs.writeFileSync(path.join(directory, 'run.json'), encode(record), {flag: 'wx'});
  return {execution: record.execution_status, validation: record.validation_status,
    quality_status: record.quality_status, directory: path.resolve(directory)};
}

async function verify(directory) {
  const record = JSON.parse(read(path.join(directory, 'run.json'), 65536));
  keys(record, ['schema', 'runner_version', 'job_id', 'execution_status', 'validation_status',
    'evidence_class', 'started_utc', 'finished_utc', 'environment', 'files', 'sources',
    'verification', 'quality_status'], 'run record');
  if (record.schema !== 'x6.edge-reference.run/0.1' || record.runner_version !== VERSION ||
      record.execution_status !== 'EXECUTED' || record.validation_status !== 'REPLAY_PASS' ||
      record.evidence_class !== 'SYNTHETIC_RESULT') throw new Error('Unsupported run record');
  keys(record.files, FILES, 'file inventory');
  assert.deepEqual(record.sources, sources(), 'Runner/source revision mismatch');
  const inputs = {};
  for (const name of FILES) {
    inputs[name] = read(path.join(directory, name), name === 'input.json' ? 65536 : evidence.MAX_BYTES);
    if (digest(inputs[name]) !== record.files[name]) throw new Error('File SHA-256 mismatch: ' + name);
  }
  const {job, parameters} = jobFrom(inputs['input.json']);
  if (job.job_id !== record.job_id) throw new Error('Job ID mismatch');
  const replay = await evidence.verifyAndReplay(inputs['evidence.json'].toString('utf8'));
  assert.deepEqual(replay.result.parameters, parameters, 'Job parameters disagree with evidence');
  assert.deepEqual(replay.verification, record.verification, 'Reported verification mismatch');
  const quality = Object.fromEntries(Object.entries(replay.result.analysis).map(([name, value]) => [name, value.status]));
  assert.deepEqual(record.quality_status, quality, 'Reported quality status mismatch');
  return {validation: 'REPLAY_PASS', quality_status: quality,
    scope: 'File integrity, job binding and same-engine numerical replay only',
    authenticity: 'NOT_ASSESSED', runtime_metadata: 'RECORDED_NOT_AUTHENTICATED',
    independent_validation: 'NOT_PERFORMED_BY_REPLAY', physical_validation: 'NOT_PERFORMED'};
}

async function main(args) {
  if (args.length === 3 && args[0] === 'run') return run(args[1], args[2]);
  if (args.length === 2 && args[0] === 'verify') return verify(args[1]);
  throw new Error('Usage: node experimental/edge_reference/runner.cjs run JOB.json NEW_DIRECTORY | verify DIRECTORY');
}
if (require.main === module) main(process.argv.slice(2)).then(result => {
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
}).catch(error => {
  process.stderr.write(JSON.stringify({status: 'ERROR', error: error.message}) + '\n');
  process.exitCode = 1;
});
module.exports = {run, verify, jobFrom};
