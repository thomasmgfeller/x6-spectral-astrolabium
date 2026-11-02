const el = id => document.getElementById('nicer-' + id);
const remote = new URL('https://raw.githubusercontent.com/thomasmgfeller/x6-spectral-astrolabium/nicer-data/');
const seed = new URL('./nicer-data/', import.meta.url);
const format = (n, digits = 0) => n.toLocaleString('de-CH', {maximumFractionDigits: digits});
let archive, entries;

async function read(url) {
  const response = await fetch(url, {cache: 'no-cache', signal: AbortSignal.timeout(15000)});
  if (!response.ok) throw Error('HTTP ' + response.status);
  return response;
}

async function list(base) {
  const index = await (await read(new URL('index.json', base))).json();
  if (index.schema !== 'x6-nicer-index-v1' || !index.entries?.length || !index.entries.every(e =>
    /^\d{10}$/.test(e.obsid) && /^[0-9a-f]{64}$/.test(e.sha256) &&
    e.file === e.obsid + '-' + e.sha256.slice(0,16) + '.json')) throw Error('Ungültiges Archivverzeichnis');
  return index.entries;
}

function plot(r) {
  const svg = el('plot');
  svg.replaceChildren();
  function draw(name, attrs, label) {
    const n = document.createElementNS('http://www.w3.org/2000/svg', name);
    for (const [key, val] of Object.entries(attrs)) n.setAttribute(key, val);
    if (label !== undefined) n.textContent = label;
    svg.append(n);
  }
  const max = Math.max(1, ...r.bins.map(([, counts, exposure]) => counts / exposure));
  const left = 60, right = 700, top = 40, bottom = 155;
  const axisSpan = Math.ceil(r.span_s / r.bin_s) * r.bin_s;
  for (const f of [0, 0.5, 1]) {
    const y = bottom - f * (bottom-top);
    draw('line', {x1:left, x2:right, y1:y, y2:y, stroke:'#526578'});
    draw('text', {x:left-8, y:y+4, 'text-anchor':'end', fill:'#b9cad9'}, format(f*max, 2));
    const x = left + f * (right-left);
    draw('text', {x, y:179, 'text-anchor': f === 0 ? 'start' : f === 1 ? 'end' : 'middle', fill:'#b9cad9'},
      format(f * axisSpan / 3600, 2) + ' h');
  }
  draw('text', {x:left, y:20, fill:'#b9cad9'}, 'Ereignisse / s gültiger Messzeit');
  for (const [bin, counts, exposure] of r.bins) {
    draw('circle', {cx:left + (bin+0.5)*r.bin_s/axisSpan*(right-left),
      cy:bottom - (counts/exposure)/max*(bottom-top), r:2.6, fill:'#66e5da'});
  }
}

async function show() {
  const select = el('select');
  select.disabled = true;
  el('result').hidden = true;
  try {
    const entry = entries[Number(select.value)];
    const url = new URL(entry.file, archive);
    const bytes = await (await read(url)).arrayBuffer();
    const hash = new Uint8Array(await crypto.subtle.digest('SHA-256', bytes));
    if (Array.from(hash, b => b.toString(16).padStart(2,'0')).join('') !== entry.sha256)
      throw Error('Prüfsumme der Lichtkurve stimmt nicht');
    const r = JSON.parse(new TextDecoder().decode(bytes));
    if (r.schema !== 'x6-nicer-lightcurve-v1' || r.obsid !== entry.obsid || r.target !== 'PSR_J0030+0451' ||
        r.bin_s !== 64 || !r.bins?.length || !(r.gti_s > 0 && r.span_s >= r.gti_s) ||
        !r.bins.every(([i,c,e]) => Number.isInteger(i) && i >= 0 && Number.isInteger(c) && c >= 0 && e > 0 && e <= r.bin_s))
      throw Error('Ungültige NICER-Lichtkurve');
    const source = new URL(r.source.url);
    if (source.origin !== 'https://heasarc.gsfc.nasa.gov') throw Error('Unbekannte Quelle');
    plot(r);
    el('metrics').textContent = format(r.counts) + ' Ereignisse in ' + format(r.gti_s, 1) +
      ' s gültiger Messzeit. Über ' + format(r.gti_count) + ' Intervalle ergibt das ' +
      format(r.counts/r.gti_s, 3) + ' Ereignisse/s. Verteilt auf die gesamten ' + format(r.span_s, 1) +
      ' s wären es ' + format(r.counts/r.span_s, 3) + ' Ereignisse/s.';
    el('fits').href = source.href;
    el('download').href = url.href;
    el('status').textContent = (archive === seed ? 'Mitgelieferte Referenz · Online-Archiv nicht verfügbar.' :
      'Automatisches Messarchiv · ' + entries.length + ' Beobachtung(en).') + ' SHA-256 geprüft.';
    el('result').hidden = false;
    el('load').hidden = true;
  } finally { select.disabled = false; }
}

function failed(error) {
  el('status').textContent = 'Lichtkurve konnte nicht geladen werden. ' + error.message;
  el('load').hidden = false;
}

el('load').addEventListener('click', async () => {
  el('load').disabled = true;
  el('status').textContent = 'Messarchiv wird geladen …';
  try {
    try { entries = await list(remote); archive = remote; }
    catch { entries = await list(seed); archive = seed; }
    el('select').replaceChildren(...entries.map((e, i) => new Option(e.date + ' · ' + e.obsid, String(i))).reverse());
    await show();
  } catch (error) { failed(error); }
  finally { el('load').disabled = false; }
});
el('select').addEventListener('change', () => show().catch(failed));
