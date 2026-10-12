'use strict';

// Transport only: scientific expectations live in the independent Python oracle.
// The legacy filter is extracted from the unchanged, embedded signal module.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');

const root = path.resolve(__dirname, '../..');
const corePath = path.join(root, 'app/signal-lab-core.js');
const appPath = path.join(root, 'app/index.html');
const digest = data => crypto.createHash('sha256').update(data).digest('hex');

function legacyFilter() {
  const app = fs.readFileSync(appPath, 'utf8');
  const frame = app.match(/<iframe\b[^>]*\bid="signalFrame"[^>]*>/);
  if (!frame) throw new Error('The original signalFrame iframe was not found.');
  const attribute = frame[0].match(/\bsrcdoc="([^"]*)"/);
  if (!attribute) throw new Error('The original signalFrame srcdoc was not found.');
  // Decode exactly one HTML-attribute layer. This is not an HTML renderer.
  const named = {amp: '&', lt: '<', gt: '>', quot: '"', apos: "'"};
  const source = attribute[1].replace(/&(#x[\da-f]+|#\d+|amp|lt|gt|quot|apos);/gi,
    (_, key) => key[0] === '#'
      ? String.fromCodePoint(key[1].toLowerCase() === 'x'
        ? parseInt(key.slice(2), 16) : parseInt(key.slice(1), 10))
      : named[key.toLowerCase()]);
  const start = source.indexOf('function fft(');
  const end = source.indexOf('function smooth(', start);
  if (start < 0 || end <= start) throw new Error('The original FFT/filter block boundaries changed.');
  const block = source.slice(start, end);
  for (const name of ['fft', 'transform', 'filter']) {
    if (!block.includes(`function ${name}(`)) throw new Error(`Missing original ${name} function.`);
  }
  const sandbox = {};
  vm.runInNewContext(`'use strict'; const T = 2 * Math.PI; ${block}; globalThis.legacyFilter = filter;`,
    sandbox, {timeout: 1000, filename: 'unchanged-signalFrame-filter.js'});
  return {filter: sandbox.legacyFilter, sourceHash: digest(block), appHash: digest(app)};
}

function main() {
  const requestText = fs.readFileSync(0, 'utf8');
  if (requestText.length > 8 * 1024 * 1024) throw new Error('Fixture input exceeds the 8 MiB bound.');
  const request = JSON.parse(requestText || '{}');
  const coreBytes = fs.readFileSync(corePath);
  const core = require(corePath);
  const legacy = legacyFilter();
  const result = {
    schema: 'x6-signal-reference-fixture-1',
    node: process.version,
    coreHash: digest(coreBytes),
    originalFilterHash: legacy.sourceHash,
    originalAppHash: legacy.appHash,
    defaults: core.defaults(),
    runs: [],
    evaluations: [],
    legacyFilters: []
  };
  for (const entry of request.runs || []) {
    const run = core.run(entry.params || {});
    const params = {...result.defaults, ...(entry.params || {})};
    // Compatibility comparison uses the exact observed input of this run.
    const original = legacy.filter(run.arrays.observed, params.phaseCenterDeg,
      params.phaseWidthDeg, params.phaseMode);
    result.runs.push({label: entry.label, result: run, originalX6: original.values});
  }
  for (const entry of request.evaluations || []) {
    result.evaluations.push({label: entry.label,
      result: core.evaluate(entry.reference, entry.candidate, entry.sampleRate,
        entry.acceptance || result.defaults.acceptance)});
  }
  for (const entry of request.legacyFilters || []) {
    const original = legacy.filter(entry.values, entry.angle, entry.width, entry.mode);
    result.legacyFilters.push({label: entry.label, values: original.values,
      imaginaryResidual: original.imag});
  }
  // Do not allow JSON to silently turn a nonfinite numeric result into null.
  process.stdout.write(JSON.stringify(result, (key, value) => {
    if (typeof value === 'number' && !Number.isFinite(value)) {
      throw new Error(`Nonfinite fixture output at key ${key}; use an explicit metric status.`);
    }
    return value;
  }));
}

try { main(); }
catch (error) { process.stderr.write(`${error.stack || error}\n`); process.exitCode = 1; }
