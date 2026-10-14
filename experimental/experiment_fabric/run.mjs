import {readFile, mkdir, writeFile} from 'node:fs/promises';
import {resolve, join, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {Worker} from 'node:worker_threads';
import {Coordinator, digest, check, condition, probabilities} from './core.mjs';
import {makeCampaign, defaultNodes, defaultTruth, simulate} from './mechanical.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
function numericallyEqual(a, b) {
  if (typeof a === 'number' && typeof b === 'number')
    return Number.isFinite(a) && Number.isFinite(b) &&
      ((Number.isInteger(a) && Number.isInteger(b)) ? a === b : Math.abs(a-b) <= 1e-12 * (1 + Math.max(Math.abs(a),Math.abs(b))));
  if (a === null || b === null || typeof a !== 'object' || typeof b !== 'object') return a === b;
  if (Array.isArray(a) !== Array.isArray(b)) return false;
  const ak=Object.keys(a).sort(),bk=Object.keys(b).sort();
  return JSON.stringify(ak)===JSON.stringify(bk) && ak.every(k=>numericallyEqual(a[k],b[k]));
}
export function workerResult(campaign, job, truth) {
  return new Promise((resolveResult, reject) => {
    const worker = new Worker(new URL('./worker.mjs', import.meta.url));
    const timer = setTimeout(() => { worker.terminate(); reject(new Error('simulation worker timeout')); }, 10000);
    worker.once('error', error => { clearTimeout(timer); worker.terminate(); reject(error); });
    worker.once('message', message => {
      clearTimeout(timer); worker.terminate();
      message.ok ? resolveResult(message.result) : reject(new Error(message.error));
    });
    worker.postMessage({campaign, job, truth});
  });
}
export async function run(rounds = 6) {
  const campaign = makeCampaign(), nodes = defaultNodes(), truth = defaultTruth();
  const coordinator = await Coordinator.create(campaign, nodes);
  const history = [];
  for (let round = 0; round < rounds; round++) {
    const selected = await coordinator.issue({budget: 2, max_batch: 2, cost_weight: 0.01});
    if (selected.status !== 'PLANNED') break;
    // Concurrent worker threads are local stand-ins for two network nodes.
    await Promise.all(selected.jobs.map(async job => coordinator.accept(await workerResult(campaign, job, truth))));
    const entry = await coordinator.commit();
    history.push(entry);
    if (entry.event.status !== 'UPDATED') break;
  }
  return {schema: 'x6.fabric.run/0.1.0', evidence_kind: 'SYNTHETIC_CONTROL', runtime: process.version,
    execution: 'TWO_LOCAL_WORKER_THREADS_NOT_A_NETWORK_DEPLOYMENT', campaign, nodes,
    synthetic_truth: truth, campaign_sha256: await digest(campaign), events: history,
    final_model_probabilities: Object.fromEntries(campaign.models.map((m, i) => [m.id, probabilities(campaign, coordinator.weights)[i]])),
    conclusion: 'RELATIVE_MODEL_WEIGHTS_ONLY_NO_PHYSICAL_ELIMINATION'};
}
export async function verify(record) {
  check(record.evidence_kind === 'SYNTHETIC_CONTROL' && record.campaign_sha256 === await digest(record.campaign), 'run/campaign binding');
  const coordinator = await Coordinator.create(record.campaign, record.nodes);
  let previousHash = null;
  for (const entry of record.events) {
    const e = entry.event;
    check(entry.sha256 === await digest(e) && e.previous_event_sha256 === previousHash, 'event chain mismatch');
    check(e.campaign_sha256 === record.campaign_sha256 && e.revision === coordinator.revision, 'revision mismatch');
    // Recreate the plan under the same lease creation time. Lease durations are fixed by this runner.
    const selected = await coordinator.issue({budget: 2, max_batch: 2, cost_weight: 0.01}, e.jobs[0].deadline_epoch_ms - 30000);
    check(await digest(selected.jobs) === await digest(e.jobs) && numericallyEqual(coordinator.pending.selected,e.plan), 'plan/job replay mismatch');
    for (let i = 0; i < e.jobs.length; i++) {
      const actual = await simulate(record.campaign, e.jobs[i], record.synthetic_truth);
      const expected = structuredClone(e.results[i]);
      delete actual.raw_sha256; delete expected.raw_sha256;
      check(numericallyEqual(actual,expected), 'simulation replay mismatch');
      await coordinator.accept(e.results[i], e.jobs[i].deadline_epoch_ms - 1);
    }
    const replay = await coordinator.commit();
    check(numericallyEqual(replay.event,e), 'posterior/event replay mismatch');
    // Preserve the checked original hash chain; computed floats use a fixed replay tolerance.
    coordinator.events[coordinator.events.length-1] = structuredClone(entry);
    previousHash = entry.sha256;
  }
  const final = Object.fromEntries(record.campaign.models.map((m, i) => [m.id, probabilities(record.campaign, coordinator.weights)[i]]));
  check(numericallyEqual(final,record.final_model_probabilities), 'final posterior mismatch');
  return {status: 'REPLAY_PASS', batches: record.events.length, physical_evidence: false};
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const [command, destination] = process.argv.slice(2);
    check(destination, 'usage: node run.mjs run NEW_DIRECTORY | verify run.json');
    if (command === 'run') {
      const record = await run();
      const output = resolve(destination);
      await mkdir(output); // Refuse overwriting an existing result directory.
      await writeFile(join(output, 'run.json'), JSON.stringify(record, null, 2) + '\n');
      console.log(JSON.stringify({output, batches: record.events.length, posterior: record.final_model_probabilities, evidence_kind: record.evidence_kind}, null, 2));
    } else if (command === 'verify') console.log(JSON.stringify(await verify(JSON.parse(await readFile(destination, 'utf8'))), null, 2));
    else throw new Error('unknown command');
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
