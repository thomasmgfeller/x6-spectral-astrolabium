/* X6 Signal Validation Lab: finite JSON snapshots, SHA-256 and computational replay.
 * A digest detects changes to a snapshot; it is not a signature or a truth claim.
 */
(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) {
    module.exports = factory(require('./signal-lab-core.js'), () => require('./signal-lab-build.js'));
  } else {
    root.X6SignalLabEvidence = factory(root.X6SignalLab, () => root.X6SignalLabBuild);
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function (core, build) {
  'use strict';
  const SCHEMA = 'x6.signal-lab.evidence/1';
  const CANONICAL = 'X6 finite JSON v1: sorted object keys; JSON number serialization';
  const ABS_TOL = 5e-12;
  const REL_TOL = 5e-10;
  const PHASE_TOL_DEG = 2e-6;
  const MAX_BYTES = 32 * 1024 * 1024;
  const MAX_NODES = 1500000;
  const LIMITATIONS = Object.freeze([
    'SYNTHETIC_RESULT: generated numerical experiments, not recorded measurement evidence.',
    'Screening limits are declared by the user; passing them is not calibration or certification.',
    'SHA-256 and a declared build identify content, not its author, truth, acquisition time or authenticity.',
    'Replay checks this engine and declared numerical tolerances, not an independent implementation.',
    'Independent NumPy/SciPy and original-X6 comparisons are separate repository tests.',
    'Source hashes come from the build manifest; this browser does not authenticate the running source.',
    'No physical, quantum, hardware-safety or cryptographic qualification is performed.'
  ]);

  function canonical(value) {
    let nodes = 0;
    const seen = new Set();
    function encode(v, depth) {
      if (++nodes > MAX_NODES || depth > 32) throw new Error('Evidence exceeds structural limits');
      if (v === null) return 'null';
      if (typeof v === 'number') {
        if (!Number.isFinite(v)) throw new Error('Evidence contains a non-finite number');
        return JSON.stringify(v);
      }
      if (typeof v === 'string') {
        if (v.length > 200000) throw new Error('Evidence string exceeds limit');
        return JSON.stringify(v);
      }
      if (typeof v === 'boolean') return v ? 'true' : 'false';
      if (typeof v !== 'object') throw new Error('Evidence must contain only finite JSON values');
      if (seen.has(v)) throw new Error('Evidence contains a cycle');
      seen.add(v);
      let result;
      if (Array.isArray(v)) {
        if (v.length > 100000) throw new Error('Evidence array exceeds limit');
        const items = [];
        for (let i = 0; i < v.length; i++) {
          if (!Object.prototype.hasOwnProperty.call(v, i)) throw new Error('Sparse arrays are not evidence');
          items.push(encode(v[i], depth + 1));
        }
        if (Object.keys(v).length !== v.length) throw new Error('Array properties are not evidence');
        result = '[' + items.join(',') + ']';
      } else {
        const proto = Object.getPrototypeOf(v);
        if (proto !== Object.prototype && proto !== null) throw new Error('Evidence objects must be plain JSON');
        const keys = Object.keys(v).sort();
        if (keys.some(k => k === '__proto__' || k === 'constructor' || k === 'prototype')) {
          throw new Error('Reserved evidence key');
        }
        result = '{' + keys.map(k => JSON.stringify(k) + ':' + encode(v[k], depth + 1)).join(',') + '}';
      }
      seen.delete(v);
      return result;
    }
    const result = encode(value, 0);
    if (new TextEncoder().encode(result).length > MAX_BYTES) throw new Error('Evidence exceeds 32 MiB');
    return result;
  }

  function snapshot(value) { return JSON.parse(canonical(value)); }

  async function sha256(text) {
    if (typeof text !== 'string') throw new Error('SHA-256 input must be text');
    if (globalThis.crypto && globalThis.crypto.subtle) {
      const bytes = new TextEncoder().encode(text);
      const digest = await globalThis.crypto.subtle.digest('SHA-256', bytes);
      return Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, '0')).join('');
    }
    if (typeof require === 'function') return require('node:crypto').createHash('sha256').update(text, 'utf8').digest('hex');
    throw new Error('SHA-256 requires a secure browser context (HTTPS, localhost or a supported local file)');
  }

  function exactKeys(object, keys, name) {
    if (!object || typeof object !== 'object' || Array.isArray(object) ||
        Object.keys(object).sort().join('|') !== keys.slice().sort().join('|')) {
      throw new Error('Invalid ' + name + ' fields');
    }
  }

  function compare(actual, expected, path, phaseMagnitude = false) {
    if (typeof actual !== typeof expected) throw new Error('Replay type mismatch at ' + path);
    if (typeof expected === 'number') {
      const circular = /\.spectrum\.phaseDeg\.\d+$/.test(path);
      const phase = circular || phaseMagnitude || /\.metrics\.phase_error_deg\.value$/.test(path);
      if (circular && Math.abs(actual) > 180 + PHASE_TOL_DEG) throw new Error('Replay phase outside wrapped range at ' + path);
      const delta = circular ? Math.abs(((actual - expected + 180) % 360 + 360) % 360 - 180) : Math.abs(actual - expected);
      const tolerance = phase ? PHASE_TOL_DEG : ABS_TOL + REL_TOL * Math.abs(expected);
      if (!Number.isFinite(actual) || delta > tolerance) {
        throw new Error('Replay numerical mismatch at ' + path);
      }
      return;
    }
    if (expected === null || typeof expected !== 'object') {
      if (actual !== expected) throw new Error('Replay mismatch at ' + path);
      return;
    }
    if (actual === null || Array.isArray(actual) !== Array.isArray(expected)) throw new Error('Replay shape mismatch at ' + path);
    const keys = Object.keys(expected);
    if (keys.length !== Object.keys(actual).length || keys.some(k => !Object.prototype.hasOwnProperty.call(actual, k))) {
      throw new Error('Replay fields mismatch at ' + path);
    }
    for (const key of keys) compare(actual[key], expected[key], path + '.' + key, key === 'value' && expected.id === 'phase_error_deg');
  }

  function sourceSnapshot(source) {
    const candidate = source || build();
    if (!candidate || candidate.schema !== 'x6.signal-lab.build/1' || candidate.version !== core.VERSION ||
        !/^[0-9a-f]{64}$/.test(candidate.bundle_sha256 || '') || !candidate.files ||
        !/^[0-9a-f]{40}$/.test(candidate.base_commit || '') ||
        !/^[0-9a-f]{64}$/.test(candidate.protected_app_sha256 || '')) {
      throw new Error('Missing or incompatible source build manifest');
    }
    for (const name of ['app/signal-lab-core.js', 'app/signal-lab-evidence.js', 'app/signal-lab-ui.js',
      'app/signal-lab.html', 'app/signal-lab.css']) {
      if (!/^[0-9a-f]{64}$/.test(candidate.files[name] || '')) throw new Error('Incomplete source build manifest');
    }
    return snapshot(candidate);
  }

  function reconstruct(result, suite) {
    if (!result || !result.parameters || result.evidenceClass !== 'SYNTHETIC_RESULT') throw new Error('Invalid synthetic run');
    const fresh = core.run(result.parameters);
    // Parameters are exact claims, unlike floating-point derived values.
    if (canonical(result.parameters) !== canonical(fresh.parameters)) throw new Error('Parameters are not canonical');
    compare(result, fresh, 'result');
    let freshSuite = null;
    if (suite !== null) {
      freshSuite = core.runCounterexamples();
      compare(suite, freshSuite, 'counterexamples');
    }
    return { result: fresh, suite: freshSuite };
  }

  async function create(result, suite = null, source) {
    // Snapshot before any async boundary, including source metadata and all input arrays.
    const fixed = snapshot(result);
    const fixedSuite = snapshot(suite);
    const fixedSource = sourceSnapshot(source);
    reconstruct(fixed, fixedSuite);
    const payload = {
      schema: SCHEMA,
      created_utc: new Date().toISOString(),
      engine_version: core.VERSION,
      evidence_class: 'SYNTHETIC_RESULT',
      source: fixedSource,
      result: fixed,
      counterexamples: fixedSuite,
      replay: { algorithm: 'regenerate parameters and recompute all arrays and diagnostics', absolute_tolerance: ABS_TOL, relative_tolerance: REL_TOL,
        phase_tolerance_degrees: PHASE_TOL_DEG, phase_distance: 'circular for wrapped spectrum phase; absolute for RMS phase metrics and gates' },
      limitations: LIMITATIONS.slice()
    };
    return { payload, integrity: { algorithm: 'SHA-256', canonicalization: CANONICAL, sha256: await sha256(canonical(payload)) } };
  }

  async function verifyAndReplay(input) {
    let doc;
    if (typeof input === 'string') {
      if (new TextEncoder().encode(input).length > MAX_BYTES) throw new Error('Evidence exceeds 32 MiB');
      doc = JSON.parse(input);
    } else doc = input;
    doc = snapshot(doc);
    exactKeys(doc, ['payload', 'integrity'], 'evidence envelope');
    exactKeys(doc.integrity, ['algorithm', 'canonicalization', 'sha256'], 'integrity');
    if (doc.integrity.algorithm !== 'SHA-256' || doc.integrity.canonicalization !== CANONICAL ||
        !/^[0-9a-f]{64}$/.test(doc.integrity.sha256)) throw new Error('Unsupported evidence integrity contract');
    if (await sha256(canonical(doc.payload)) !== doc.integrity.sha256) throw new Error('Evidence SHA-256 mismatch');
    const p = doc.payload;
    exactKeys(p, ['schema', 'created_utc', 'engine_version', 'evidence_class', 'source', 'result', 'counterexamples', 'replay', 'limitations'], 'payload');
    if (p.schema !== SCHEMA || p.engine_version !== core.VERSION || p.evidence_class !== 'SYNTHETIC_RESULT') {
      throw new Error('Unsupported schema, engine version or evidence class');
    }
    if (typeof p.created_utc !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(p.created_utc) ||
        !Number.isFinite(Date.parse(p.created_utc)) || new Date(p.created_utc).toISOString() !== p.created_utc) {
      throw new Error('Invalid declared UTC timestamp');
    }
    exactKeys(p.replay, ['algorithm', 'absolute_tolerance', 'relative_tolerance', 'phase_tolerance_degrees', 'phase_distance'], 'replay policy');
    if (p.replay.absolute_tolerance !== ABS_TOL || p.replay.relative_tolerance !== REL_TOL ||
        p.replay.algorithm !== 'regenerate parameters and recompute all arrays and diagnostics' ||
        p.replay.phase_tolerance_degrees !== PHASE_TOL_DEG ||
        p.replay.phase_distance !== 'circular for wrapped spectrum phase; absolute for RMS phase metrics and gates') {
      throw new Error('Replay tolerance policy cannot be changed');
    }
    if (canonical(p.limitations) !== canonical(LIMITATIONS)) throw new Error('Evidence limitations were changed');
    const source = sourceSnapshot(p.source);
    const local = sourceSnapshot();
    if (canonical(source) !== canonical(local)) throw new Error('Source revision mismatch: replay with the matching archived build');
    const fresh = reconstruct(p.result, p.counterexamples);
    return {
      result: fresh.result,
      suite: fresh.suite,
      verification: {
        passed: true,
        sha256: doc.integrity.sha256,
        hash: 'MATCH',
        replay: 'MATCH_WITHIN_DECLARED_TOLERANCE',
        source: 'MATCHING_DECLARED_BUILD',
        authenticity: 'NOT_ASSESSED',
        independent_validation: 'NOT_PERFORMED_BY_REPLAY',
        declared_created_utc: p.created_utc
      }
    };
  }

  function toCSV(result) {
    const r = snapshot(result);
    reconstruct(r, null);
    const { time, reference, observed, outputs } = r.arrays;
    const methods = ['identity', 'moving_average', 'fft_lowpass', 'x6_phase'];
    const header = ['index', 'time_s', 'reference', 'observed', ...methods];
    const rows = reference.map((value, i) => [i, time[i], value, observed[i], ...methods.map(m => outputs[m][i])].join(','));
    return header.join(',') + '\n' + rows.join('\n') + '\n';
  }

  return Object.freeze({ SCHEMA, MAX_BYTES, canonical, sha256, create, verifyAndReplay, toCSV });
});
