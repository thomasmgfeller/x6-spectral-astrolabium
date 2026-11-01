const get = id => document.getElementById(id);
const load = get('hanford-load');
const select = get('hanford-select');
const status = get('hanford-status');
const root = new URL('./hanford-data/', import.meta.url);
const NS = 'http://www.w3.org/2000/svg';
let entries;

async function read(url) {
  const response = await fetch(url, {cache: 'no-cache'});
  if (!response.ok) throw Error(`HTTP ${response.status}`);
  return response;
}

function element(name, attrs, label) {
  const node = document.createElementNS(NS, name);
  for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
  if (label !== undefined) node.textContent = label;
  return node;
}

function plot(record) {
  const svg = get('hanford-plot');
  const y = record.strain, width = 600, left = 94;
  const scale = Math.max(...y.map(Math.abs)) || 1;
  const paths = [];
  for (let x = 0; x < width; x++) {
    const bin = y.slice(Math.floor(x*y.length/width), Math.floor((x+1)*y.length/width));
    paths.push(`M${left+x} ${77-60*Math.max(...bin)/scale}V${77-60*Math.min(...bin)/scale}`);
  }
  const target = left + (Number(record.catalog.gps) - record.window_gps_start) * width / 4;
  svg.replaceChildren(element('line',{x1:left,x2:left+width,y1:77,y2:77,stroke:'#61778f'}),
    element('path',{d:paths.join(' '),stroke:'#66e5da',fill:'none'}),
    element('line',{x1:target,x2:target,y1:11,y2:138,stroke:'#efbd71','stroke-dasharray':'4 3'}));
  for (const [x,py,text] of [[1,18,'Strain'],[1,36,scale.toExponential(2)],[1,80,'0'],
    [1,138,'−'+scale.toExponential(2)],[left,161,'0 s'],[left+width/2,161,'2 s'],
    [left+width-16,161,'4 s']]) {
    svg.append(element('text',{x,y:py,fill:'#b6c5d6','font-size':13},text));
  }
}

async function show() {
  const entry = entries[select.selectedIndex];
  select.disabled = true;
  get('hanford-result').hidden = true;
  status.textContent = 'Lade und prüfe das Messfenster …';
  try {
    const url = new URL(entry.file, root);
    const bytes = await (await read(url)).arrayBuffer();
    const digest = await crypto.subtle.digest('SHA-256', bytes);
    const hash = Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2,'0')).join('');
    if (hash !== entry.sha256) throw Error('Dateiprüfsumme stimmt nicht überein');
    const rec = JSON.parse(new TextDecoder().decode(bytes));
    if (rec.detector !== 'H1' || rec.catalog.gps !== entry.gps || rec.strain.length !== 16384)
      throw Error('Unerwartetes Messformat');
    plot(rec);
    get('hanford-metrics').textContent = `Eigene 235-Hz-Spitzenamplitude: ${rec.analysis.peak_amplitude_strain.toExponential(3)} Strain · Katalog-SNR: ${rec.catalog.snr_recovered_catalog.toFixed(2)} · ${rec.sample_count.toLocaleString('de-CH')} Messwerte bei 4096 Hz`;
    get('hanford-download').href = url;
    get('hanford-download').download = entry.file;
    get('hanford-result').hidden = false;
    status.textContent = `GPS ${entry.gps} · Dateihash geprüft · DATA und BURST_CAT1 im Fenster · HW_BURST zur Zielsekunde`;
  } catch (error) {
    status.textContent = `Messfenster nicht verfügbar: ${error.message}`;
    load.hidden = false;
  } finally { select.disabled = false; }
}

load.addEventListener('click', async () => {
  load.disabled = true;
  try {
    const index = await (await read(new URL('index.json',root))).json();
    if (index.schema !== 'x6-hanford-s6-v1' || !index.records.length ||
        !index.records.every(e => /^\d{9}\.\d{2}$/.test(e.gps) && e.file === 'H1-'+e.gps+'.json'))
      throw Error('Ungültiges Messarchiv');
    entries = index.records;
    select.replaceChildren(...entries.map(e => new Option(e.gps, e.gps)));
    get('hanford-choice').hidden = false;
    load.hidden = true;
    await show();
  } catch (error) {
    status.textContent = `Archiv nicht verfügbar: ${error.message}`;
  } finally { load.disabled = false; }
});
select.addEventListener('change', show);
