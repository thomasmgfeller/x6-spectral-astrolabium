// X6 Experiment Fabric 0.1 — finite, binary-outcome reference; simulation only.
export const VERSION = 'x6.experiment-fabric/0.1.0';
export function check(ok, message) { if (!ok) throw new Error(message); }
export function keys(object, required) {
  check(object && Object.getPrototypeOf(object) === Object.prototype &&
    Object.keys(object).length === required.length && required.every(k => Object.hasOwn(object, k)), 'unexpected or missing contract field');
}
export const JOB_KEYS = ['schema','campaign_sha256','job_id','batch_revision','attempt','node_id','specimen_id','experiment_id','replicate_id','deadline_epoch_ms','execution_mode','seed'];
export const RESULT_KEYS = ['schema','observation_id','evidence_kind','quality','outcome','raw','raw_sha256','job_id','campaign_sha256','batch_revision','attempt','node_id','specimen_id','experiment_id','replicate_id'];
const sum = xs => xs.reduce((a, b) => a + b, 0);
const finite = x => typeof x === 'number' && Number.isFinite(x);
const id = x => typeof x === 'string' && /^[A-Za-z0-9][A-Za-z0-9_.:-]{0,95}$/.test(x);
const unique = xs => new Set(xs).size === xs.length;
function freeze(value) { if (value && typeof value === 'object') { Object.values(value).forEach(freeze); Object.freeze(value); } return value; }
export function canonical(value) {
  if (typeof value === 'number') { check(Number.isFinite(value), 'nonfinite number'); return JSON.stringify(value); }
  if (value === null || typeof value === 'string' || typeof value === 'boolean') return JSON.stringify(value);
  if (Array.isArray(value)) return '[' + value.map(canonical).join(',') + ']';
  check(value && Object.getPrototypeOf(value) === Object.prototype, 'plain JSON objects required');
  return '{' + Object.keys(value).sort().map(k => JSON.stringify(k) + ':' + canonical(value[k])).join(',') + '}';
}
export async function digest(value) {
  const bytes = new TextEncoder().encode(canonical(value));
  return [...new Uint8Array(await globalThis.crypto.subtle.digest('SHA-256', bytes))].map(x => x.toString(16).padStart(2, '0')).join('');
}
export function validateCampaign(c) {
  check(c.schema === VERSION && id(c.campaign_id), 'invalid campaign version/id');
  check(c.evidence_kind === 'SYNTHETIC_CONTROL', 'this executor accepts simulations only');
  check(Array.isArray(c.models) && c.models.length >= 2 && c.models.length <= 16, 'model limit');
  check(c.models.every(m => id(m.id)) && unique(c.models.map(m => m.id)), 'model ids');
  check(Array.isArray(c.states) && c.states.length >= 2 && c.states.length <= 64, 'state limit');
  check(c.states.every(s => id(s.id) && c.models.some(m => m.id === s.model_id) && finite(s.prior) && s.prior > 0), 'invalid latent state');
  check(unique(c.states.map(s => s.id)) && c.models.every(m => c.states.some(s => s.model_id === m.id)), 'state/model coverage');
  check(Math.abs(sum(c.states.map(s => s.prior)) - 1) < 1e-12, 'prior must sum to one');
  check(c.dependence === 'INDEPENDENT_GIVEN_PERSISTENT_LATENT_STATE', 'joint dependence model required');
  check(Array.isArray(c.experiments) && c.experiments.length >= 1 && c.experiments.length <= 16, 'experiment limit');
  check(unique(c.experiments.map(e => e.id)), 'duplicate experiment id');
  for (const e of c.experiments) {
    check(id(e.id) && finite(e.cost) && e.cost > 0 && typeof e.capability === 'string', 'invalid experiment');
    check(e.p_one.length === c.states.length && e.p_one.every(p => finite(p) && p >= 0 && p <= 1), 'likelihood probabilities');
  }
  canonical(c);
  return c;
}
export function probabilities(c, weights) {
  check(Array.isArray(weights) && weights.length === c.states.length && weights.every(p => finite(p) && p >= 0), 'invalid posterior');
  check(Math.abs(sum(weights) - 1) < 1e-10, 'posterior must sum to one');
  return c.models.map(m => sum(weights.map((p, i) => c.states[i].model_id === m.id ? p : 0)));
}
export const entropy = weights => -sum(weights.filter(p => p > 0).map(p => p * Math.log2(p)));
function experiment(c, identifier) { const e = c.experiments.find(e => e.id === identifier); check(e, 'unknown experiment'); return e; }
export function condition(c, weights, experimentIds, outcomes) {
  probabilities(c, weights);
  check(experimentIds.length > 0 && experimentIds.length <= 4 && outcomes.length === experimentIds.length, 'batch dimensions');
  check(outcomes.every(y => y === 0 || y === 1), 'binary outcome required');
  const experiments = experimentIds.map(identifier => experiment(c, identifier));
  const unnormalized = weights.map((p, s) => p * experiments.reduce((v, e, i) => v * (outcomes[i] ? e.p_one[s] : 1 - e.p_one[s]), 1));
  const predictive = sum(unnormalized);
  if (predictive === 0) return {status: 'MODEL_SET_INADEQUATE', predictive, posterior: null};
  return {status: 'UPDATED', predictive, posterior: unnormalized.map(p => p / predictive)};
}
export function information(c, weights, experimentIds) {
  const initial = entropy(probabilities(c, weights));
  check(experimentIds.length <= 4, 'batch limit');
  let expected = 0;
  for (let mask = 0; mask < 2 ** experimentIds.length; mask++) {
    const outcomes = experimentIds.map((_, i) => (mask >> i) & 1);
    const result = condition(c, weights, experimentIds, outcomes);
    if (result.predictive > 0) expected += result.predictive * entropy(probabilities(c, result.posterior));
  }
  const gain = initial - expected;
  check(gain >= -1e-10 && gain <= initial + 1e-10, 'invalid information gain');
  return Math.max(0, gain);
}
export function plan(c, weights, nodes, options = {}) {
  validateCampaign(c); probabilities(c, weights);
  const {budget = 2, max_batch = 2, cost_weight = 0.01, min_gain_bits = 1e-9} = options;
  check(finite(budget) && budget > 0 && finite(cost_weight) && cost_weight >= 0 && finite(min_gain_bits) && min_gain_bits >= 0, 'invalid planner budget');
  check(Number.isInteger(max_batch) && max_batch >= 1 && max_batch <= 4 && nodes.length >= 1 && nodes.length <= 4, 'node/batch limit');
  check(unique(nodes.map(n => n.id)) && nodes.every(n => id(n.id) && id(n.specimen_id) && Array.isArray(n.capabilities)), 'invalid node declarations');
  const eligible = nodes.map(n => n.available && n.execution_mode === 'SIMULATION_ONLY' ? c.experiments.filter(e => n.capabilities.includes(e.capability)) : []);
  check(eligible.reduce((p, e) => p * (e.length + 1), 1) <= 100000, 'enumeration budget exceeded');
  const candidates = [];
  function visit(index, assignments, cost, specimens) {
    if (index === nodes.length) {
      if (!assignments.length) return;
      const eig = information(c, weights, assignments.map(a => a.experiment_id));
      candidates.push({assignments: structuredClone(assignments), cost, expected_information_bits: eig, utility: eig - cost_weight * cost});
      return;
    }
    visit(index + 1, assignments, cost, specimens);
    if (assignments.length >= max_batch || specimens.has(nodes[index].specimen_id)) return;
    for (const e of eligible[index]) {
      if (cost + e.cost > budget + 1e-12) continue;
      visit(index + 1, [...assignments, {node_id: nodes[index].id, specimen_id: nodes[index].specimen_id, experiment_id: e.id}],
            cost + e.cost, new Set([...specimens, nodes[index].specimen_id]));
    }
  }
  visit(0, [], 0, new Set());
  candidates.sort((a, b) => {
    const difference = b.utility - a.utility;
    if (Math.abs(difference) > 1e-12) return difference;
    if (a.cost !== b.cost) return a.cost - b.cost;
    const ka = canonical(a.assignments), kb = canonical(b.assignments);
    return ka < kb ? -1 : ka > kb ? 1 : 0;
  });
  const best = candidates[0];
  return best && best.utility > 0 && best.expected_information_bits >= min_gain_bits
    ? {...best, status: 'PLANNED', candidates_evaluated: candidates.length, objective: 'JOINT_MODEL_INFORMATION_MINUS_COST'}
    : {status: 'NO_INFORMATIVE_ADMISSIBLE_BATCH', candidates_evaluated: candidates.length};
}

export class Coordinator {
  static async create(campaign, nodes) {
    validateCampaign(campaign);
    const instance = new Coordinator();
    instance.campaign = freeze(structuredClone(campaign));
    instance.nodes = freeze(structuredClone(nodes));
    instance.campaignHash = await digest(campaign);
    instance.weights = campaign.states.map(s => s.prior);
    instance.revision = 0; instance.pending = null; instance.committed = new Set();
    instance.observations = new Set(); instance.events = []; instance.queue = Promise.resolve();
    return instance;
  }
  serial(operation) { const p = this.queue.then(operation); this.queue = p.catch(() => {}); return p; }
  issue(options = {}, now = Date.now(), leaseMs = 30000) {
    return this.serial(async () => {
      check(!this.halted, 'campaign halted: model set inadequate');
      check(!this.pending, 'a batch is already pending');
      check(Number.isSafeInteger(now) && now >= 0 && Number.isSafeInteger(leaseMs) && leaseMs > 0 && leaseMs <= 300000, 'invalid lease');
      const selected = plan(this.campaign, this.weights, this.nodes, options);
      if (selected.status !== 'PLANNED') return selected;
      const jobs = selected.assignments.map((a, i) => ({
        schema: 'x6.fabric.job/0.1.0', campaign_sha256: this.campaignHash,
        job_id: `${this.campaign.campaign_id}.r${this.revision}.j${i}`, batch_revision: this.revision,
        attempt: 1, node_id: a.node_id, specimen_id: a.specimen_id, experiment_id: a.experiment_id,
        replicate_id: `${this.campaign.campaign_id}.r${this.revision}.sample${i}`,
        deadline_epoch_ms: now + leaseMs, execution_mode: 'SIMULATION_ONLY',
        seed: ((this.campaign.simulation_seed ?? 104729) + this.revision * 7919 + i * 65537) >>> 0,
      }));
      this.pending = {selected, jobs, received: new Map()};
      return {...structuredClone(selected), jobs: structuredClone(jobs)};
    });
  }
  retry(jobId, now = Date.now(), leaseMs = 30000) {
    return this.serial(async () => {
      check(this.pending, 'no pending batch');
      const job = this.pending.jobs.find(j => j.job_id === jobId);
      check(job && !this.pending.received.has(jobId), 'job unavailable for retry');
      check(Number.isSafeInteger(now) && now > job.deadline_epoch_ms && Number.isSafeInteger(leaseMs) && leaseMs > 0 && leaseMs <= 300000, 'retry needs expired lease');
      // Same synthetic replicate and seed: retry is not independent evidence.
      job.attempt++; job.deadline_epoch_ms = now + leaseMs;
      return structuredClone(job);
    });
  }
  accept(result, now = Date.now()) {
    return this.serial(async () => {
      keys(result, RESULT_KEYS);
      check(this.pending && result.schema === 'x6.fabric.result/0.1.0', 'no pending batch or wrong result schema');
      check(Number.isSafeInteger(now) && now >= 0, 'invalid receive time');
      const job = this.pending.jobs.find(j => j.job_id === result.job_id);
      check(job, 'unknown job');
      check(!this.committed.has(job.job_id) && !this.pending.received.has(job.job_id), 'duplicate result');
      for (const key of ['campaign_sha256', 'batch_revision', 'attempt', 'node_id', 'specimen_id', 'experiment_id', 'replicate_id'])
        check(result[key] === job[key], 'result binding mismatch: ' + key);
      check(now <= job.deadline_epoch_ms, 'expired result');
      check(result.evidence_kind === 'SYNTHETIC_CONTROL' && result.quality === 'PASS', 'inadmissible evidence');
      check(result.outcome === 0 || result.outcome === 1, 'invalid outcome');
      check(id(result.observation_id) && !this.observations.has(result.observation_id) &&
            ![...this.pending.received.values()].some(r => r.observation_id === result.observation_id), 'duplicate observation');
      check(result.raw && result.raw.replicate_id === job.replicate_id && result.raw.experiment_id === job.experiment_id, 'raw binding mismatch');
      keys(result.raw, ['replicate_id','experiment_id','seed','measured_accelerance','unit','threshold','outcome']);
      check(result.raw.outcome === result.outcome && result.raw.seed === job.seed && finite(result.raw.measured_accelerance), 'raw/outcome mismatch');
      const e = experiment(this.campaign, job.experiment_id);
      check(result.raw.unit === '(m/s^2)/N' && result.raw.threshold === e.threshold &&
            (result.raw.measured_accelerance >= e.threshold ? 1 : 0) === result.outcome, 'threshold encoding mismatch');
      check(await digest(result.raw) === result.raw_sha256, 'raw hash mismatch');
      this.pending.received.set(job.job_id, freeze(structuredClone(result)));
      return {status: 'STORED_NOT_YET_ASSIMILATED', remaining: this.pending.jobs.length - this.pending.received.size};
    });
  }
  commit() {
    return this.serial(async () => {
      check(this.pending && this.pending.received.size === this.pending.jobs.length, 'batch incomplete');
      const batch = this.pending;
      const results = batch.jobs.map(j => batch.received.get(j.job_id));
      const update = condition(this.campaign, this.weights, results.map(r => r.experiment_id), results.map(r => r.outcome));
      const posterior = update.posterior ?? [...this.weights];
      const event = {
        schema: 'x6.fabric.event/0.1.0', campaign_sha256: this.campaignHash, revision: this.revision,
        previous_event_sha256: this.events.at(-1)?.sha256 ?? null,
        plan: batch.selected, jobs: batch.jobs, results, prior: [...this.weights], posterior,
        predictive_probability: update.predictive, status: update.status,
        model_probabilities: Object.fromEntries(this.campaign.models.map((m, i) => [m.id, probabilities(this.campaign, posterior)[i]])),
        physical_claim: 'NONE_SYNTHETIC_CONTROL',
      };
      const entry = {event, sha256: await digest(event)};
      this.events.push(freeze(entry));
      for (const r of results) { this.committed.add(r.job_id); this.observations.add(r.observation_id); }
      this.pending = null;
      if (update.posterior) { this.weights = posterior; this.revision++; }
      else this.halted = true;
      return structuredClone(entry);
    });
  }
}
