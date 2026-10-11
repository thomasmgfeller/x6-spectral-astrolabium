'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const root = path.resolve(__dirname, '../..');
const core = require(path.join(root, 'app/sagnac-core.js'));
const raw = new Uint8Array(fs.readFileSync(path.join(root, 'device/fixtures/synthetic_chsh_capture.bin')));
const results = [];
function test(name, fn) { fn(); results.push({ name, passed: true }); }
function repair(b) { new DataView(b.buffer, b.byteOffset, b.byteLength).setUint32(240, core.crc32(b.subarray(0, 240)), true); return b; }
function reject(b, origin = 'synthetic', seq = '100') { assert.throws(() => core.decode(b, origin, seq)); }
const r = core.decode(raw, 'synthetic', '100');
test('Python reference: all raw counters, sequences and both Hoeffding statistics', () => {
  const script = `import sys,json;sys.path.insert(0,${JSON.stringify(path.join(root, 'device/vendor/sagnac_v0_7'))});from frame_codec import decode_stream;from analyze import analyze;r=decode_stream(sys.stdin.buffer.read(),origin='synthetic',expected_first_sequence=100);print(json.dumps({'records':r['records'],'analysis':analyze(r['records'])}))`;
  const oracle = JSON.parse(execFileSync(process.env.PYTHON || 'python3', ['-c', script], { input: raw }));
  r.records.forEach((v, i) => { assert.deepEqual(v.counters, oracle.records[i].counters); assert.equal(v.transport.sequence, oracle.records[i].transport.sequence); });
  for (const k of ['conditional_coincidences', 'all_trials_fixed_assignment']) {
    for (const p of ['S', 'singlet_T_lower_hoeffding']) assert.ok(Math.abs(r.chsh[k][p] - oracle.analysis[k][p]) < 1e-12);
    assert.equal(r.chsh[k].model_conditional_gate, oracle.analysis[k].model_conditional_gate);
  }
});
test('Every one-bit corruption of a 244-byte frame is rejected (1952 cases)', () => {
  for (let bit = 0; bit < 1952; bit++) { const b = raw.slice(0, 244); b[bit >> 3] ^= 1 << (bit & 7); reject(b); }
});
test('Missing, duplicated, reordered and wrong initial sequences are rejected', () => {
  reject(raw.subarray(244)); reject(Uint8Array.from([...raw.subarray(0, 244), ...raw.subarray(0, 244)]));
  reject(Uint8Array.from([...raw.subarray(244, 488), ...raw.subarray(0, 244)])); reject(raw, 'synthetic', '99');
});
test('Empty, truncated, oversized data and missing provenance are rejected', () => {
  reject(new Uint8Array()); reject(raw.subarray(0, raw.length - 1)); reject(new Uint8Array(244 * 4097)); reject(raw, '');
});
test('Recomputed CRC cannot hide integrity flags or inconsistent counters', () => {
  const flags = raw.slice(0, 244); flags[10] = 4; reject(repair(flags));
  const counts = raw.slice(0, 244); counts[48] ^= 1; reject(repair(counts));
});
test('Version, reserved field and setting are checked independently of CRC', () => {
  for (const [off, value] of [[8, 8], [11, 1], [9, 4]]) { const b = raw.slice(0, 244); b[off] = value; reject(repair(b)); }
});
test('Calibration or bin-width mismatches cannot produce combined CHSH', () => {
  const b = raw.slice(); b[244 + 12] ^= 1; repair(b.subarray(244, 488)); reject(b);
  const differentWidth = raw.slice(), v = new DataView(differentWidth.buffer, 244, 244);
  const start = v.getBigUint64(16, true), stop = v.getBigUint64(24, true);
  v.setBigUint64(24, start + 2n * (stop - start), true);
  v.setBigUint64(32, 2n * v.getBigUint64(32, true), true);
  repair(differentWidth.subarray(244, 488)); reject(differentWidth);
});
test('uint64 counts above 2^53 remain exact; sequence overflow is rejected', () => {
  const b = raw.slice(0, 244), v = new DataView(b.buffer); const n = 2n ** 53n + 17n;
  v.setBigUint64(16, 0n, true); v.setBigUint64(24, n, true); v.setBigUint64(32, 1n, true);
  for (let j = 0; j < 24; j++) v.setBigUint64(48 + 8 * j, [0, 16].includes(j) ? n : 0n, true);
  assert.equal(core.decode(repair(b), 'synthetic', '100').records[0].counters[16], String(n));
  assert.throws(() => core.uint('18446744073709551616'));
  assert.throws(() => core.uint(100));
  const wrap = raw.slice(0, 488);
  new DataView(wrap.buffer).setBigUint64(40, 2n ** 64n - 1n, true);
  new DataView(wrap.buffer).setBigUint64(244 + 40, 0n, true);
  repair(wrap.subarray(0, 244)); repair(wrap.subarray(244, 488));
  reject(wrap, 'synthetic', String(2n ** 64n - 1n));
});
test('Missing settings stay diagnostic; physical and control claims never become PASS', () => {
  const one = core.decode(raw.subarray(0, 244), 'hardware', '100');
  assert.equal(one.chsh.conditional_coincidences, null);
  assert.equal(one.physical_quantum_claim, 'NOT_ASSESSED');
  assert.equal(one.control.actuator_commands, false);
  assert.equal(one.provenance_verification, 'DECLARED_NOT_AUTHENTICATED');
});
console.log(JSON.stringify({ status: 'PASS', tests: results.length, assertions_include_1952_bit_flips: true, results }, null, 2));
