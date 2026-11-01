const button = document.getElementById('sed-load');
const select = document.getElementById('sed-band');
const status = document.getElementById('sed-status');
const rows = document.getElementById('sed-pairs');
let summary;

function render() {
  const band = select.selectedIndex;
  rows.replaceChildren(...summary.pairs.map(pair => {
    const tr = document.createElement('tr');
    const th = document.createElement('th');
    th.scope = 'row';
    th.textContent = pair.from + ' → ' + pair.to;
    const delay = document.createElement('td');
    delay.textContent = pair.delay_s[band] === null ? 'Offen' : pair.delay_s[band].toFixed(3);
    const spread = document.createElement('td');
    spread.textContent = pair.spread_ms === null ? 'Offen' : pair.spread_ms.toFixed(1);
    tr.append(th,delay,spread);
    return tr;
  }));
  const labels = {OK:'bestimmt', LEFT_EDGE:'über Schwelle am Fensterrand', NO_TRIGGER:'kein Einsatz',
    QUIET_TRIGGER:'Auslösung im Ruhefenster', LOW_CONTRAST:'zu geringer Kontrast', BOUNDARY_OR_FLAT:'Randminimum oder konstantes Signal'};
  const checks = Object.entries(summary.checks).map(([station,bands]) =>
    station+' (Varianzwechsel: '+labels[bands[band].variance]+', Pegelschwelle: '+labels[bands[band].rms]+')');
  document.getElementById('sed-checks').textContent = checks.join(' · ');
}

button.addEventListener('click', async () => {
  button.disabled = true;
  try {
    const result = await fetch(new URL('./sed-data/summary.json',import.meta.url));
    if (!result.ok) throw Error('HTTP '+result.status);
    const data = await result.json();
    if (data.method !== 'x6-sed-pg-variance-v1' || data.bands_hz.length !== 3 || data.pairs.length !== 3 ||
        !data.pairs.every(p => p.delay_s.length === 3 && p.delay_s.every(d=>d===null || Number.isFinite(d)) && (p.spread_ms===null || Number.isFinite(p.spread_ms))))
      throw Error('Unvollständiger Ergebnisdatensatz');
    summary = data;
    select.replaceChildren(...data.bands_hz.map(([low,high]) => new Option(low+'–'+high+' Hz')));
    render();
    status.textContent = '3 Stationen · 3 Frequenzbänder · 120 Abtastwerte pro Sekunde und Station';
    document.getElementById('sed-result').hidden = false;
    button.hidden = true;
  } catch (error) { status.textContent = 'Vergleich nicht verfügbar: '+error.message; }
  finally { button.disabled = false; }
});
select.addEventListener('change',render);
