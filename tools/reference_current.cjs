'use strict';
// Fixed, local recipe; argv[2] is always the trusted checkout's Signal Lab core.
const core = require(process.argv[2]);
const reference = Array.from({length: 128}, (_, n) => Math.cos(2 * Math.PI * n / 128));
const inputs = {inverted: reference.map(v => -v), identity: reference.slice(), zero: reference.map(() => 0)};
process.stdout.write(JSON.stringify({
  schema: 'x6.reference.current-polarity/1', samples: 128, sampleRate: 128, reference,
  cases: Object.entries(inputs).map(([label, candidate]) => ({
    label, candidate, result: core.evaluate(reference, candidate, 128)
  }))
}) + '\n');
