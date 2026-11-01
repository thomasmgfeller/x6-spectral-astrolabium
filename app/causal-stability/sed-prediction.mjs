const button = document.getElementById('sed-trial-load');
const status = document.getElementById('sed-trial-status');

button.addEventListener('click', async () => {
  button.disabled = true;
  try {
    const url = new URL('../../research/sed_filter_prediction/v1/results.json', import.meta.url);
    const response = await fetch(url);
    if (!response.ok) throw Error('HTTP ' + response.status);
    const {result} = await response.json();
    const rows = [];
    for (const [key,name] of [['x6','X6-Suchfenster'],['snr','Signal/Rauschen']]) {
      const c = result.counts[key];
      const nums = [result.released_each,c.WITHIN,c.EXCEEDED,c.INDETERMINATE];
      if (!nums.every(n => Number.isInteger(n) && n >= 0) || nums[0] !== nums[1]+nums[2]+nums[3])
        throw Error('Unvollständige Entscheidungstabelle');
      const tr = document.createElement('tr');
      const th = document.createElement('th');
      th.scope = 'row';
      th.textContent = name;
      tr.append(th);
      for (const n of nums) {
        const td = document.createElement('td');
        td.textContent = String(n);
        tr.append(td);
      }
      rows.push(tr);
    }
    if (!['ADVANTAGE_SUPPORTED','ADVANTAGE_NOT_DEMONSTRATED'].includes(result.decision))
      throw Error('Unbekannte Entscheidung');
    document.getElementById('sed-trial-counts').replaceChildren(...rows);
    status.textContent = result.decision === 'ADVANTAGE_SUPPORTED'
      ? 'Das vorab festgelegte Kriterium für einen X6-Vorteil ist in diesem Archivtest erfüllt.'
      : 'Ein Vorteil der X6-Regel ist in diesem Archivtest nicht nachgewiesen.';
    document.getElementById('sed-trial-paired').textContent =
      `Dasselbe Paar gewählt: ${result.same_pair} von ${result.released_each}. Nur X6 besteht: ${result.x6_only_success}. Nur Signal/Rauschen besteht: ${result.snr_only_success}. Einseitiger exakter Vorzeichentest: p = ${result.p_one_sided.toLocaleString('de-CH',{maximumSignificantDigits:4})}. Unbestimmte Kontrollen zählen als Fehlfreigaben.`;
    document.getElementById('sed-trial-result').hidden = false;
    button.hidden = true;
  } catch (error) { status.textContent = 'Versuchsbericht nicht verfügbar: ' + error.message; }
  finally { button.disabled = false; }
});
