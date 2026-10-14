import {VERSION, check, digest, validateCampaign, keys, JOB_KEYS} from './core.mjs';

export function accelerance(model, omega) {
  return omega * omega / Math.hypot(model.stiffness_n_m - model.mass_kg * omega * omega, model.damping_ns_m * omega);
}
const logistic = x => x >= 0 ? 1 / (1 + Math.exp(-x)) : Math.exp(x) / (1 + Math.exp(x));
export function makeCampaign() {
  const models = [
    {id: 'M_K100_C1', mass_kg: 1, stiffness_n_m: 100, damping_ns_m: 1},
    {id: 'M_K100_C3', mass_kg: 1, stiffness_n_m: 100, damping_ns_m: 3},
    {id: 'M_K144_C1', mass_kg: 1, stiffness_n_m: 144, damping_ns_m: 1},
    {id: 'M_K144_C3', mass_kg: 1, stiffness_n_m: 144, damping_ns_m: 3},
    {id: 'OTHER', description: 'Independent fair binary outcomes: a limited discrepancy sentinel, not all unknown physics.'},
  ];
  const states = models.flatMap(model => model.id === 'OTHER'
    ? [{id: 'OTHER', model_id: 'OTHER', prior: 0.1, gain: 1}]
    : [0.92, 1, 1.08].map((gain, i) => ({id: `${model.id}.g${i}`, model_id: model.id, prior: 0.075, gain})));
  const experiments = [];
  for (const omega of [7, 9, 10, 11, 12, 14]) {
    const predicted = models.slice(0, 4).map(m => accelerance(m, omega)).sort((a, b) => a - b);
    for (const [name, threshold] of [['low', (predicted[0] + predicted[1]) / 2], ['high', (predicted[2] + predicted[3]) / 2]]) {
      const noiseScale = 0.3;
      experiments.push({id: `omega${omega}.${name}`, capability: 'OSCILLATOR_SIM', cost: 1,
        omega_rad_s: omega, force_n: 0.01, threshold, noise_scale: noiseScale,
        observable: 'noisy accelerance estimate >= threshold', unit: '(m/s^2)/N',
        p_one: states.map(state => state.model_id === 'OTHER' ? 0.5 : logistic((state.gain * accelerance(models.find(m => m.id === state.model_id), omega) - threshold) / noiseScale)),
      });
    }
  }
  return validateCampaign({schema: VERSION, campaign_id: 'X6-MECHANICAL-CONTROL-001', evidence_kind: 'SYNTHETIC_CONTROL', simulation_seed: 104729,
    dependence: 'INDEPENDENT_GIVEN_PERSISTENT_LATENT_STATE',
    description: 'Four point hypotheses in one linear oscillator family, plus a limited discrepancy model. Not four validated physical theories.',
    observation_model: 'm*x_ddot+c*x_dot+k*x=F; scalar accelerance magnitude plus logistic noise, thresholded to one bit; no time-domain sensor/DAQ simulation.',
    nuisance_model: 'One persistent shared multiplicative calibration gain for the entire campaign. Independent observation noise conditional on model and gain.',
    specimen_model: 'Identical simulated replicas share the same parameters and gain; real replica variation is not modelled.',
    models, states, experiments});
}
export const defaultNodes = () => [
  {id: 'node-A', specimen_id: 'replica-A', available: true, execution_mode: 'SIMULATION_ONLY', capabilities: ['OSCILLATOR_SIM']},
  {id: 'node-B', specimen_id: 'replica-B', available: true, execution_mode: 'SIMULATION_ONLY', capabilities: ['OSCILLATOR_SIM']},
];
export const defaultTruth = () => ({mass_kg: 1, stiffness_n_m: 144, damping_ns_m: 3, gain: 1.08});
function uniform(seed) {
  let t = (seed + 0x6D2B79F5) >>> 0;
  t = Math.imul(t ^ t >>> 15, t | 1);
  t ^= t + Math.imul(t ^ t >>> 7, t | 61);
  return (((t ^ t >>> 14) >>> 0) + 0.5) / 4294967296;
}
export async function simulate(campaign, job, truth) {
  keys(job, JOB_KEYS);
  validateCampaign(campaign);
  check(job.schema === 'x6.fabric.job/0.1.0' && job.execution_mode === 'SIMULATION_ONLY', 'physical execution refused');
  check(await digest(campaign) === job.campaign_sha256, 'campaign binding mismatch');
  check(Object.values(truth).every(v => typeof v === 'number' && Number.isFinite(v) && v > 0), 'invalid synthetic truth');
  check(Number.isSafeInteger(job.seed) && job.seed >= 0 && job.seed <= 4294967295, 'invalid seed');
  const e = campaign.experiments.find(e => e.id === job.experiment_id);
  check(e, 'unknown experiment');
  const u = uniform(job.seed);
  const measured = truth.gain * accelerance(truth, e.omega_rad_s) + e.noise_scale * Math.log(u / (1 - u));
  const outcome = measured >= e.threshold ? 1 : 0;
  const raw = {replicate_id: job.replicate_id, experiment_id: job.experiment_id, seed: job.seed,
    measured_accelerance: measured, unit: '(m/s^2)/N', threshold: e.threshold, outcome};
  const result = {schema: 'x6.fabric.result/0.1.0', observation_id: job.replicate_id + '.observation',
    evidence_kind: 'SYNTHETIC_CONTROL', quality: 'PASS', outcome, raw, raw_sha256: await digest(raw)};
  for (const key of ['job_id', 'campaign_sha256', 'batch_revision', 'attempt', 'node_id', 'specimen_id', 'experiment_id', 'replicate_id']) result[key] = job[key];
  return result;
}
