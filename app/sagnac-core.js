/* X6 Sagnac integration 0.1: raw counts, explicit provenance, no actuator control. */
(function (root) {
  'use strict';
  const FRAME_BYTES = 244, U64 = 1n << 64n;
  function need(ok, message) { if (!ok) throw new Error(message); }
  function uint(value) {
    need(typeof value === 'string' && /^[0-9]+$/.test(value), 'Unsigned decimal string required');
    const n = BigInt(value); need(n < U64, 'uint64 overflow'); return n;
  }
  function crc32(bytes) {
    let c = 0xffffffff;
    for (const b of bytes) { c ^= b; for (let i = 0; i < 8; i++) c = (c >>> 1) ^ ((c & 1) ? 0xedb88320 : 0); }
    return (c ^ 0xffffffff) >>> 0;
  }
  function correlation(pos, neg) {
    const n = pos + neg;
    return { n: String(n), positive: String(pos), negative: String(neg),
      E: n ? Number(pos - neg) / Number(n) : null };
  }
  function validateRecord(r) {
    const c = r.counters.map(uint), cfg = r.configuration;
    need(r.flags === 0, 'Acquisition integrity flag: ' + r.flags);
    const start = uint(cfg.start_ps), stop = uint(cfg.stop_ps), width = uint(cfg.window_ps);
    need(width > 0n && stop > start && (stop - start) % width === 0n, 'Invalid time-window configuration');
    const n = (stop - start) / width;
    need(c[16] === n && c.slice(0, 16).reduce((a, b) => a + b, 0n) === n, 'Trial accounting mismatch');
    const presence = [0n, 0n, 0n, 0n]; let multi = 0n, allPos = 0n;
    for (let m = 0; m < 16; m++) {
      for (let ch = 0; ch < 4; ch++) if (m & (1 << ch)) presence[ch] += c[m];
      if ((m & 3) === 3 || ((m >> 2) & 3) === 3) multi += c[m];
      if (((m & 3) === 2) === (((m >> 2) & 3) === 2)) allPos += c[m];
    }
    need(presence.every((v, i) => c[18 + i] >= v), 'Click accounting mismatch');
    const extras = c.slice(18, 22).reduce((a, b) => a + b, 0n) - presence.reduce((a, b) => a + b, 0n);
    need(c[22] === extras && c[17] <= n && c[17] <= extras && ((c[17] === 0n) === (extras === 0n)), 'Repeat accounting mismatch');
    need(c[23] === multi, 'Multiport accounting mismatch');
    const seconds = Number(stop - start) / 1e12;
    return { setting_index: r.setting_index, sequence: r.transport.sequence, calibration_id: r.calibration_id,
      duration_seconds: seconds, trials: String(n), clicks: c.slice(18, 22).map(String),
      observed_clicks_per_second: c.slice(18, 22).map(v => Number(v) / seconds),
      repeat_trials: String(c[17]), multiport_trials: String(c[23]),
      conditional_coincidences: correlation(c[5] + c[10], c[9] + c[6]),
      all_trials_fixed_assignment: correlation(allPos, n - allPos) };
  }
  function combine(values, alpha) {
    if (values.some(v => v.E === null)) return { status: 'INSUFFICIENT_DATA', S: null, model_conditional_gate: false };
    const S = values.reduce((a, v, i) => a + (i === 3 ? -1 : 1) * v.E, 0);
    const lower = -S - values.reduce((a, v) => a + Math.sqrt(2 * Math.log(4 / alpha) / Number(v.n)), 0);
    return { status: 'MODEL_CONDITIONAL_DIAGNOSTIC', S, singlet_T: -S,
      singlet_T_lower_hoeffding: lower, hoeffding_alpha: alpha, model_conditional_gate: lower > 2 };
  }
  function decode(bytes, origin, firstSequence, alpha = 0.0027) {
    need(bytes instanceof Uint8Array, 'Binary capture required');
    need(['synthetic', 'hardware'].includes(origin), 'Explicit data origin required');
    const first = uint(firstSequence);
    need(Number.isFinite(alpha) && alpha > 0 && alpha < 1, 'Invalid alpha');
    need(bytes.length > 0 && bytes.length % FRAME_BYTES === 0 && bytes.length <= FRAME_BYTES * 4096, 'Empty, truncated or oversized capture');
    const records = [], summaries = [];
    for (let offset = 0, i = 0; offset < bytes.length; offset += FRAME_BYTES, i++) {
      const b = bytes.subarray(offset, offset + FRAME_BYTES), v = new DataView(b.buffer, b.byteOffset, b.byteLength);
      need(crc32(b.subarray(0, 240)) === v.getUint32(240, true), 'CRC32 mismatch in frame ' + i);
      need(String.fromCharCode(...b.subarray(0, 8)) === 'SGNCv007' && b[8] === 7 && b[11] === 0, 'Unsupported frame version or reserved field');
      need(b[9] < 4, 'Invalid measurement setting');
      const seq = v.getBigUint64(40, true);
      need(first + BigInt(i) < U64 && seq === first + BigInt(i), 'Missing, repeated or reordered frame');
      const r = { format: 'sagnac.fixed_bins.v0.6', origin, complete: true,
        setting_index: b[9], flags: b[10], calibration_id: String(v.getUint32(12, true)),
        configuration: { start_ps: String(v.getBigUint64(16, true)), stop_ps: String(v.getBigUint64(24, true)), window_ps: String(v.getBigUint64(32, true)) },
        counters: Array.from({ length: 24 }, (_, j) => String(v.getBigUint64(48 + j * 8, true))),
        transport: { format: 'SGNCv007', sequence: String(seq), crc32: v.getUint32(240, true).toString(16).padStart(8, '0') } };
      summaries.push(validateRecord(r)); records.push(r);
    }
    let chsh = { status: 'REQUIRES_EXACTLY_FOUR_DISTINCT_SETTINGS', conditional_coincidences: null, all_trials_fixed_assignment: null };
    if (records.length === 4 && new Set(records.map(r => r.setting_index)).size === 4) {
      need(new Set(records.map(r => r.calibration_id + '/' + r.configuration.window_ps)).size === 1, 'Incompatible calibration IDs or window widths');
      const sorted = summaries.slice().sort((a, b) => a.setting_index - b.setting_index);
      chsh = { status: 'MODEL_CONDITIONAL_DIAGNOSTIC',
        conditional_coincidences: combine(sorted.map(r => r.conditional_coincidences), alpha),
        all_trials_fixed_assignment: combine(sorted.map(r => r.all_trials_fixed_assignment), alpha) };
    }
    return { schema: 'x6.sagnac.evidence/1', version: '0.1', origin,
      provenance_verification: 'DECLARED_NOT_AUTHENTICATED', integrity: 'VALIDATED_TRANSPORT_AND_COUNTERS',
      calibration_status: 'ID_PRESENT_PHYSICAL_CALIBRATION_NOT_VERIFIED', physical_quantum_claim: 'NOT_ASSESSED',
      control: { status: 'UNAVAILABLE', actuator_commands: false, reason: 'SGNCv007 is a snapshot output; no command or actuator protocol is implemented.' },
      records, summaries, chsh,
      assumptions: ['Correct detector and analyzer calibration is not established.',
        'Hoeffding bounds require iid trials within each setting; drift and dead time are not included.',
        'Conditional coincidences require representative detection (fair sampling).',
        'Setting independence, stationarity and Bell-test loopholes are not established.',
        'Rates are observed clicks per run duration, not photon-pair generation rates.',
        'Snapshot data cannot reconstruct per-photon arrival times or within-run drift.'],
      processing: { background_subtraction: false, efficiency_compensation: false, outcome_filtering: false } };
  }
  const api = Object.freeze({ FRAME_BYTES, crc32, decode, uint });
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.X6Sagnac = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
