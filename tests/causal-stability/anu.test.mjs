import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {makeModel} from '../../app/causal-stability/engine.mjs';
import {replayBlock} from '../../app/causal-stability/anu-control.mjs';

// Deliberately synthetic values used only in offline tests.
function fixture(bytes) {
  return {schema: 'x6.anu-qrng/1', type: 'uint8', length: 1024,
    source: 'https://api.quantumnumbers.anu.edu.au/?length=1024&type=uint8',
    provider: 'Australian National University', usage_terms: 'https://quantumnumbers.anu.edu.au/faq',
    retrieved_at: '2026-11-01T00:00:00+00:00', data_hex: Buffer.from(bytes).toString('hex'),
    sha256: createHash('sha256').update(Buffer.from(bytes)).digest('hex')};
}

test('each sign pattern matches the independent forward graph solution', async () => {
  const model = makeModel({preset: 'cspp', n: 5, theta: 21});
  for (let pattern = 0; pattern < 8; ++pattern) {
    const values = {};
    for (const node of model.nodes) {
      values[node.id] = node.role === 'history' ? (pattern & (1 << Number(node.id[1])) ? 1 : -1) :
        model.edges.filter(e => e.to === node.id).reduce((s, e) => s + values[e.from] * e.weight, 0);
    }
    const {rms} = await replayBlock(fixture(Array(1024).fill(pattern)));
    assert.ok(Math.abs(rms - Math.abs(values.d)) < 1e-12);
  }
});

test('balanced enumeration gives the model population RMS', async () => {
  const {rms, expectedRms, trials} = await replayBlock(fixture(Array.from({length: 1024}, (_, i) => i % 256)));
  assert.ok(expectedRms > 0 && Math.abs(rms - expectedRms) < 1e-12);
  assert.equal(trials, 1024);
});

test('modified bytes, missing data or wrong source cannot be replayed', async () => {
  const r = fixture(Array(1024).fill(0));
  for (const delta of [{data_hex: '0'}, {data_hex: '01'.repeat(1024)}, {source: 'other'}, {sha256: ''}]) {
    await assert.rejects(replayBlock({...r, ...delta}));
  }
});
