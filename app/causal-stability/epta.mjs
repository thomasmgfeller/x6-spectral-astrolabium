const el = name => document.getElementById('epta-' + name);
const archive = new URL('https://raw.githubusercontent.com/thomasmgfeller/x6-spectral-astrolabium/epta-data/');
const pinned = new URL('../../research/epta_filter_v1/reference.json', import.meta.url);
const fmt = (v, d=2) => v.toLocaleString('de-CH', {maximumFractionDigits:d});
const pct = n => fmt(100*n, 2) + ' %';

async function read(url) {
  const response = await fetch(url, {cache:'no-cache', signal:AbortSignal.timeout(15000)});
  if (!response.ok) throw Error('HTTP ' + response.status);
  const r = await response.json();
  if (r.schema !== 'x6.epta-filter/1' || r.protocol_sha256 !== '9124e60fdd8bdb674f3a2e5522a9af9ace1458b5ba766b6540e9321fc8d0b17a' ||
      r.source.doi !== 'https://doi.org/10.5281/zenodo.8300645' || r.pulsars?.length !== 8 || r.pairs?.length !== 28 ||
      !/^[a-f0-9]{64}$/.test(r.timing_csv.sha256) || r.timing_csv.name !== 'timing-'+r.timing_csv.sha256.slice(0,16)+'.csv.gz')
    throw Error('Unerwarteter Datensatz');
  return r;
}

function row(parent, cells) {
  const tr = document.createElement('tr');
  for (const s of cells) {
    const td = document.createElement('td');
    td.textContent = s;
    tr.append(td);
  }
  parent.append(tr);
}

function draw(points) {
  const svg = el('plot');
  svg.replaceChildren();
  function put(tag, attrs, label) {
    const n = document.createElementNS('http://www.w3.org/2000/svg',tag);
    for (const [k,v] of Object.entries(attrs)) n.setAttribute(k,v);
    if (label !== undefined) n.textContent=label;
    svg.append(n);
  }
  const left=66, right=650, extent=Math.max(1,...points.map(p=>Math.abs(p[1])));
  const min=points[0][0], max=points.at(-1)[0];
  for (const f of [-1,0,1]) {
    const py=84-50*f;
    put('line',{x1:left,x2:right,y1:py,y2:py,stroke:'#566b80'});
    put('text',{x:left-8,y:py+4,'text-anchor':'end',fill:'#b9cad9'},fmt(f*extent));
  }
  put('text',{x:left,y:19,fill:'#b9cad9'},'Residuum (µs)');
  put('text',{x:left,y:163,fill:'#b9cad9'},'MJD '+fmt(min,0));
  put('text',{x:right,y:163,fill:'#b9cad9','text-anchor':'end'},'MJD '+fmt(max,0));
  for (const [mjd,y] of points) put('circle',{cx:left+(mjd-min)/(max-min)*(right-left),cy:84-50*y/extent,r:2.5,fill:'#66e5da'});
}

el('load').addEventListener('click',async () => {
  el('load').disabled=true;
  el('status').textContent='EPTA-Auswertung wird geladen …';
  try {
    let url=new URL('summary.json',archive), r;
    try { r=await read(url); }
    catch { url=pinned; r=await read(pinned); }
    const ref=r.pulsars[0];
    el('reference').textContent=fmt(ref.toas)+' Radio-Ankunftszeiten von 1999 bis 2021. Gewichteter RMS mit dem veröffentlichten Timing-Modell: '+
      fmt(ref.wrms_us,6)+' µs. EPTA gibt 2,45583 µs an.';
    draw(r.reference_90d);
    el('rates').replaceChildren();
    for (const [key,name] of [['identity','Ohne Filter'],['cspp','CSPP-Filter']]) {
      const a=r.arms[key], cell=x=>fmt(x.hits)+' / '+fmt(x.n)+' ('+pct(x.fraction)+')';
      row(el('rates'),[name,cell(a.false_alarm),cell(a.detection)]);
    }
    const [lo,hi]=r.paired_difference_mc95;
    el('verdict').textContent=(r.decision==='DOES_NOT_QUALIFY'?'Freigabekriterien verfehlt. ':'Freigabekriterien erfüllt. ')+
      'Differenz der Trefferquoten (Filter minus Referenz): '+fmt(100*r.paired_detection_difference)+
      ' Prozentpunkte, gepaartes 95-%-Intervall von '+fmt(100*lo)+' bis '+fmt(100*hi)+'.';
    el('precision').textContent='Bei einigen Pulsaren lassen sich langsame Schwingungen und der quadratische Zeittrend nur schlecht trennen. Die Amplitudenschätzung streut entsprechend stark. Die Simulation bewertet dieses Filter- und Auswerteverfahren unter dem festgelegten Rauschmodell.';
    el('pairs').replaceChildren();
    for (const p of [...r.pairs].sort((a,b)=>a.angle_deg-b.angle_deg))
      row(el('pairs'),[p.p+' / '+p.q,fmt(p.angle_deg,1)+'°',fmt(p.hd,3),fmt(p.expected_cspp,3)]);
    el('json').href=url.href;
    el('csv').href=new URL(r.timing_csv.name,archive).href;
    el('result').hidden=false;
    el('load').hidden=true;
    el('status').textContent=url===pinned?'Mitgelieferte Referenz. Das Online-Verzeichnis war nicht erreichbar.':'Veröffentlichter automatischer Rechenlauf · EPTA DR2full';
  } catch(error) { el('status').textContent='EPTA-Auswertung konnte nicht geladen werden. '+error.message; }
  finally { el('load').disabled=false; }
});
