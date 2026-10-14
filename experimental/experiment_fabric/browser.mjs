import {Coordinator, probabilities} from './core.mjs';
import {makeCampaign, defaultNodes, defaultTruth} from './mechanical.mjs';
const $ = id => document.getElementById(id);
const campaign = makeCampaign(), nodes = defaultNodes(), truth = defaultTruth();
let coordinator, record;
const labels = {'M_K100_C1':'k=100 N/m · c=1 Ns/m','M_K100_C3':'k=100 N/m · c=3 Ns/m',
  'M_K144_C1':'k=144 N/m · c=1 Ns/m','M_K144_C3':'k=144 N/m · c=3 Ns/m','OTHER':'OTHER · begrenztes Abweichungsmodell'};
function models() {
  $('models').replaceChildren();
  campaign.models.forEach((m, i) => {
    const p = probabilities(campaign, coordinator.weights)[i];
    const row = document.createElement('div'); row.className = 'model';
    const label = document.createElement('label'); const name = document.createElement('span'), number = document.createElement('span');
    name.textContent = labels[m.id]; number.textContent = (100 * p).toFixed(2) + ' %'; label.append(name, number);
    const bar = document.createElement('progress'); bar.max = 1; bar.value = p; bar.setAttribute('aria-label', labels[m.id]);
    row.append(label, bar); $('models').append(row);
  });
}
function nodeResult(job) {
  return new Promise((resolve, reject) => {
    const worker = new Worker(new URL('./worker.mjs', import.meta.url), {type:'module'});
    const timer = setTimeout(() => {worker.terminate(); reject(new Error('Worker-Zeitlimit erreicht.'));}, 10000);
    worker.onerror = event => {clearTimeout(timer); worker.terminate(); reject(new Error(event.message));};
    worker.onmessage = event => {
      clearTimeout(timer); worker.terminate();
      event.data.ok ? resolve(event.data.result) : reject(new Error(event.data.error));
    };
    worker.postMessage({campaign, job, truth});
  });
}
async function reset() {
  coordinator = await Coordinator.create(campaign, nodes); record = null;
  $('events').replaceChildren(); $('information').textContent = '—';
  $('status').textContent = 'Bereit. Die Modellgewichte beginnen mit dem registrierten Prior.';
  $('selection').textContent = 'Nächste Auswahl: gemeinsame Information über die Modellidentität, unter Kosten- und Ressourcenbedingungen.';
  $('export').disabled = true; $('run').disabled = false; models();
}
$('run').onclick = async () => {
  $('run').disabled = true; $('reset').disabled = true; $('export').disabled = true;
  try {
    let stop = 'Rundenbudget erreicht.';
    for (let round = 0; round < 6; round++) {
      $('status').textContent = `Runde ${round + 1}: Messpaket auswählen und parallel ausführen …`;
      const selected = await coordinator.issue({budget:2,max_batch:2,cost_weight:0.01});
      if (selected.status !== 'PLANNED') {stop = 'Keine weitere Messung überschreitet im registrierten Modell den Kostenabzug.'; break;}
      await Promise.all(selected.jobs.map(async job => coordinator.accept(await nodeResult(job))));
      const {event} = await coordinator.commit();
      const row = document.createElement('tr');
      const texts = [String(round + 1), ...nodes.map(n => event.jobs.find(j => j.node_id === n.id)?.experiment_id ?? '—'),
        selected.expected_information_bits.toFixed(4) + ' Bit', event.results.map(r => String(r.outcome)).join(' / ')];
      for (const text of texts) {const cell = document.createElement('td'); cell.textContent = text; row.append(cell);}
      $('events').append(row); $('information').textContent = selected.expected_information_bits.toFixed(4) + ' Bit';
      $('selection').textContent = event.jobs.map(j => `${j.node_id}: ${j.experiment_id}`).join(' · '); models();
      if (event.status !== 'UPDATED') {stop = 'Modellsatz unzureichend; Kampagne angehalten.'; break;}
    }
    record = {schema:'x6.fabric.run/0.1.0',evidence_kind:'SYNTHETIC_CONTROL',runtime:navigator.userAgent,
      execution:'TWO_LOCAL_BROWSER_WORKERS_NOT_A_NETWORK_DEPLOYMENT',campaign,nodes,synthetic_truth:truth,
      campaign_sha256:coordinator.campaignHash,events:coordinator.events,
      final_model_probabilities:Object.fromEntries(campaign.models.map((m,i)=>[m.id, probabilities(campaign,coordinator.weights)[i]])),
      conclusion:'RELATIVE_MODEL_WEIGHTS_ONLY_NO_PHYSICAL_ELIMINATION'};
    $('status').textContent = 'Abgeschlossen. ' + stop; $('export').disabled = false;
  } catch (error) {$('status').textContent = 'Angehalten: ' + error.message; record = null;}
  finally {$('reset').disabled = false;}
};
$('reset').onclick = reset;
$('export').onclick = () => {
  const url = URL.createObjectURL(new Blob([JSON.stringify(record,null,2)+'\n'],{type:'application/json'}));
  const a = document.createElement('a'); a.href=url; a.download='x6-fabric-simulation.json'; a.click();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
};
// Read-only convenience for the browser qualification test; no physical adapter.
window.X6FabricDemo = {snapshot:()=>record ? structuredClone(record) : null};
await reset();
