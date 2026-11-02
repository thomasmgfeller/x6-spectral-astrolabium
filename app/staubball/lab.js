// The window and normalization follow the frozen smoothed-current design.
const cut = 0.47, start = 0.23, end = 0.58;
const radius = Math.cbrt(3 / (4 * Math.PI));
const dataRoot = '../../research/rax_cqg/dust_collapse/smoothed/';
const url = new URL(location.href);
const english = url.searchParams.get('lang') === 'en';
const lang = english ? 'en' : 'de';
const say = (de, en) => english ? en : de;
const id = name => document.getElementById(name);
const label = run => '#' + String(run).padStart(2, '0');
const format = (n, digits = 0) => n.toLocaleString(english ? 'en-US' : 'de-DE', {
  minimumFractionDigits: digits, maximumFractionDigits: digits
});
document.documentElement.lang = lang;
if (english) {
  document.querySelectorAll('[data-en]').forEach(el => { el.textContent = el.dataset.en; });
  document.title = 'Dust ball lab · X6 Spectral Astrolabium';
  id('home').href = '../../index.html';
}
const other = new URL(location.href);
other.searchParams.set('lang', english ? 'de' : 'en');
id('lang').href = other.href;
id('lang').lang = english ? 'de' : 'en';
id('lang').textContent = english ? 'Deutsch' : 'English';
id('rows').setAttribute('aria-label', say('Kausalordnung wählen', 'Select a causal order'));
document.querySelector('.ends span:first-child').textContent = 'T = ' + format(start, 2);
document.querySelector('.ends span:last-child').textContent = 'T = ' + format(end, 2);

// Horizontal distance is signed physical distance through the centre, not comoving radius.
const a = t => (1 - t) ** (2 / 3);
const eta = t => 3 * (1 - Math.cbrt(1 - t));
const surface = t => a(t) * radius;
const envelope = t => a(t) * (radius + eta(end) - eta(t));
const X = r => 246 + r * 187, Y = t => 251 - (t - start) / (end - start) * 212;
const svg = id('diagram');
function draw(tag, attrs, parent = svg, caption) {
  const shape = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [key, value] of Object.entries(attrs)) shape.setAttribute(key, value);
  if (caption !== undefined) shape.textContent = caption;
  parent.append(shape);
  return shape;
}
function line(x1, y1, x2, y2, stroke, parent = svg, extra = {}) {
  return draw('line', {x1, y1, x2, y2, stroke, ...extra}, parent);
}
function contour(fn, fill, stroke, dashed = false) {
  const times = Array.from({length: 81}, (_, i) => start + (end - start) * i / 80);
  const point = (t, sign) => X(sign * fn(t)).toFixed(2) + ',' + Y(t).toFixed(2);
  const points = [...times.map(t => point(t, -1)), ...times.reverse().map(t => point(t, 1))];
  draw('polygon', {points: points.join(' '), fill, stroke, 'stroke-width': 1.8,
    'stroke-dasharray': dashed ? '5 4' : 'none'});
}
draw('text', {x: 15, y: 21}, svg, say('Eigenzeit T ↑', 'Proper time T ↑'));
for (const t of [start, 0.35, cut, end]) {
  line(52, Y(t), 438, Y(t), '#36565a');
  draw('text', {x: 47, y: Y(t) + 4, 'text-anchor': 'end'}, svg, format(t, 2));
}
contour(envelope, '#234958', '#92b7d4', true);
contour(surface, '#195c56', '#71e7c8');
line(X(0), Y(end), X(0), Y(start), '#84a4a2', svg, {'stroke-dasharray': '2 4'});
line(52, Y(cut), 438, Y(cut), '#efb467', svg, {'stroke-dasharray': '6 4', 'stroke-width': 2});
for (const r of [-0.8, -0.4, 0, 0.4, 0.8]) {
  line(X(r), 254, X(r), 258, '#92aaa6');
  draw('text', {x: X(r), y: 273, 'text-anchor': 'middle'}, svg, r === 0 ? '0' : format(r, 1));
}
draw('text', {x: X(0), y: 294, 'text-anchor': 'middle'}, svg, say('Physischer Abstand vom Zentrum', 'Physical distance from centre'));
const slice = draw('g', {id:'slice'});
function showTime() {
  const t = Number(id('time').value) / 100;
  slice.replaceChildren();
  const width = surface(t), height = Y(t);
  line(X(-width), height, X(width), height, '#f4fff6', slice, {'stroke-width':3});
  for (const sign of [-1, 1]) draw('circle', {cx:X(sign * width), cy:height, r:4, fill:'#fffbea'}, slice);
  id('time-value').textContent = 'T = ' + format(t, 2);
  id('time').setAttribute('aria-valuetext', 'T = ' + format(t, 2));
  id('radii').textContent = say('Physischer Staubradius ', 'Physical dust radius ') + format(width,3) +
    say(' · Radius des Einzugsgebiets ', ' · Envelope radius ') + format(envelope(t),3);
}
let timer;
function stop() {
  clearInterval(timer); timer = undefined;
  id('play').textContent = say('Abspielen', 'Play');
}
id('time').addEventListener('input', () => { stop(); showTime(); });
id('reset').addEventListener('click', () => { stop(); id('time').value = 47; showTime(); });
id('play').addEventListener('click', () => {
  if (timer !== undefined) { stop(); return; }
  if (Number(id('time').value) >= 58) id('time').value = 23;
  showTime();
  id('play').textContent = 'Pause';
  timer = setInterval(() => {
    id('time').value = Number(id('time').value) + 1;
    showTime();
    if (Number(id('time').value) >= 58) stop();
  }, 150);
});
document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
showTime();

async function csv(filename) {
  const response = await fetch(dataRoot + filename);
  if (!response.ok) throw new Error(filename);
  const lines = (await response.text()).trim().split(/\r?\n/);
  const keys = lines.shift().split(',');
  return lines.map(line => {
    const values = line.split(',');
    if (values.length !== keys.length || values.some(v => !v.trim() || !Number.isFinite(Number(v)))) throw new Error(filename);
    return Object.fromEntries(keys.map((key, i) => [key, Number(values[i])]));
  });
}
const hit = row => Math.abs(row.smoothed - 1) + row.tail_bound <= 0.1;
let sample = [], current = 0;
const span = (cls, text) => {
  const el = document.createElement('span'); el.className = cls;
  if (text !== undefined) el.textContent = text;
  return el;
};
function choose(run, updateUrl = true) {
  current = run;
  const row = sample.find(entry => entry.run === run);
  for (const btn of id('rows').children) btn.setAttribute('aria-pressed', String(Number(btn.dataset.run) === run));
  id('selected').textContent = say('Ordnung ', 'Order ') + label(run);
  id('context-id').textContent = label(run);
  id('context').textContent = format(row.n) + say(' Ereignisse im Würfel · ', ' events in the cube · ') + format(row.marked) + say(' markierte Zukunftspunkte.', ' marked future endpoints.');
  id('local-value').textContent = format(row.unsmoothed, 3);
  id('smooth-value').textContent = format(row.smoothed, 3);
  id('verdict').textContent = hit(row) ? say('Geglättet im Zielband', 'Smoothed inside band') : say('Geglättet ausserhalb', 'Smoothed outside band');
  id('verdict').classList.toggle('hit', hit(row));
  other.searchParams.set('order', run); id('lang').href = other.href;
  if (updateUrl) {
    url.searchParams.set('order', run); history.replaceState(null, '', url);
  }
}
function showPlot() {
  const focus = id('scale').value === 'focus';
  const transform = x => focus ? Math.sign(x - 1) * Math.log1p(Math.abs(x - 1)) : x;
  const min = transform(-110), max = transform(75);
  const percent = x => 100 * (transform(x) - min) / (max - min);
  const width = (el, l, r) => { el.style.left = percent(l) + '%'; el.style.width = (percent(r) - percent(l)) + '%'; };
  const ticks = span('ticks');
  for (const n of (focus ? [-100,-10,1,10,60] : [-100,-50,1,50])) {
    const mark = span('', String(n)); mark.style.left = percent(n) + '%'; ticks.append(mark);
  }
  id('axis').replaceChildren(span(''), ticks);
  const buttons = sample.map(row => {
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'mass-row'; button.dataset.run = row.run;
    button.setAttribute('aria-label', say('Ordnung ', 'Order ') + label(row.run) + say(', lokal ', ', local ') + format(row.unsmoothed,3) + say(', geglättet ', ', smoothed ') + format(row.smoothed,3));
    const track = span('track'); track.setAttribute('aria-hidden','true');
    const band = span('band'); width(band, .9, 1.1);
    const ref = span('ref'); ref.style.left = percent(1) + '%';
    const range = span('range'); width(range, Math.min(row.unsmoothed,row.smoothed), Math.max(row.unsmoothed,row.smoothed));
    const local = span('dot local'); local.style.left = percent(row.unsmoothed) + '%';
    const smooth = span('dot smooth'); smooth.style.left = percent(row.smoothed) + '%';
    track.append(band,ref,range,local,smooth);
    button.append(span('name',label(row.run)), track);
    button.addEventListener('click', () => choose(row.run));
    return button;
  });
  id('rows').replaceChildren(...buttons);
  id('scale-note').textContent = focus ? say('Um M = 1 logarithmisch gespreizt. Die Zahlen geben die ursprünglichen Massenwerte an.', 'Logarithmically expanded around M = 1. Labels give the original mass values.') :
    say('Beide Schätzer auf derselben linearen Achse. Die senkrechte Linie markiert M = 1.', 'Both estimators share one linear axis. The vertical line marks M = 1.');
  choose(current, false);
}
async function loadSample() {
  const [scores, full] = await Promise.all([csv('full_scores.csv'),csv('full.csv')]);
  const counts = new Map(full.map(row => [row.run,row]));
  if (scores.length !== 12 || counts.size !== 12 || new Set(scores.map(row => row.run)).size !== 12) throw new Error('Incomplete sample');
  sample = scores.map(row => {
    const count = counts.get(row.run);
    if (!count || ![row.smoothed,row.unsmoothed,row.tail_bound,count.n,count.marked].every(Number.isFinite)) throw new Error('Missing columns');
    return {...row, n:count.n, marked:count.marked};
  }).sort((a,b) => a.run-b.run);
  const requested = Number(url.searchParams.get('order'));
  current = sample.some(row => row.run === requested) ? requested : sample[0].run;
  id('scale').addEventListener('change', showPlot);
  showPlot();
  const localHits = sample.filter(r => Math.abs(r.unsmoothed - 1) <= .1).length;
  const smoothHits = sample.filter(hit).length;
  id('cohort').textContent = say('Treffer unter zwölf Ordnungen · lokal ', 'Hits among twelve orders · local ') + localHits + '/12 · ' + say('geglättet ', 'smoothed ') + smoothHits + '/12.';
}
loadSample().catch(() => {
  id('cohort').textContent = say('Messdaten konnten nicht geladen werden. Bitte neu laden oder die CSV-Dateien unten öffnen.', 'Could not load the measurements. Reload the page or open the CSV files below.');
});
