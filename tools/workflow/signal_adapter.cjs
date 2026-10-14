/* Copyright 2026 Thomas Gfeller. SPDX-License-Identifier: Apache-2.0 */
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const runner = require('../../experimental/edge_reference/runner.cjs');
const evidence = require('../../app/signal-lab-evidence.js');

async function main(args) {
  const [command, directory, input] = args;
  if (['run', 'import'].includes(command) && args.length === 3) {
    if (command === 'run') {
      await runner.run(input, directory);
    } else {
      const info = fs.lstatSync(input);
      if (!info.isFile() || info.isSymbolicLink() || info.size > evidence.MAX_BYTES) throw new Error('Invalid or oversized evidence input');
      const bytes = fs.readFileSync(input);
      if (bytes.length > evidence.MAX_BYTES) throw new Error('Evidence exceeds size limit');
      const replay = await evidence.verifyAndReplay(bytes.toString('utf8'));
      const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'x6-import-'));
      try {
        const job = path.join(temporary, 'job.json');
        fs.writeFileSync(job, evidence.canonical({schema: 'x6.edge-reference.job/0.1', job_id: 'X6-IMPORTED-SIGNAL', parameters: replay.result.parameters}) + '\n');
        await runner.run(job, directory);
        // Preserve the validated native export byte for byte, including counterexamples.
        fs.writeFileSync(path.join(directory, 'evidence.json'), bytes);
        const recordPath = path.join(directory, 'run.json');
        const record = JSON.parse(fs.readFileSync(recordPath, 'utf8'));
        record.files['evidence.json'] = crypto.createHash('sha256').update(bytes).digest('hex');
        record.verification = replay.verification;
        fs.writeFileSync(recordPath, evidence.canonical(record) + '\n');
      } finally { fs.rmSync(temporary, {recursive: true, force: true}); }
    }
    const replay = await evidence.verifyAndReplay(fs.readFileSync(path.join(directory, 'evidence.json'), 'utf8'));
    fs.writeFileSync(path.join(directory, 'samples.csv'), evidence.toCSV(replay.result), {flag: 'wx'});
  } else if (command !== 'verify' || args.length !== 2) {
    throw new Error('Usage: signal_adapter.cjs run DIRECTORY JOB | import DIRECTORY EVIDENCE | verify DIRECTORY');
  }
  const result = await runner.verify(directory);
  const replay = await evidence.verifyAndReplay(fs.readFileSync(path.join(directory, 'evidence.json'), 'utf8'));
  assert.equal(fs.readFileSync(path.join(directory, 'samples.csv'), 'utf8'), evidence.toCSV(replay.result), 'CSV differs from replay');
  process.stdout.write(JSON.stringify(result) + '\n');
}
main(process.argv.slice(2)).catch(error => {
  process.stderr.write(JSON.stringify({status: 'ERROR', error: error.message}) + '\n');
  process.exitCode = 1;
});
