/* SPDX-License-Identifier: Apache-2.0 */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const O = OrderGeometry, P = ProperTime, bank = JSON.parse($('og-bank').textContent);
  const fmt = (x,n=3) => x.toLocaleString('de-CH',{maximumFractionDigits:n});
  const set = (id,s) => { $(id).textContent=s; };
  const show = (id,visible) => { $(id).hidden=!visible; };
  const colors = {text:'#ccd9ed', grid:'#32435c', edge:'#667993', cyan:'#68e6d2', purple:'#b8a3ff'};
  let order, graph, settings, current, trials, ticket=0, fileTicket=0, loaded=null, twin=null, started=false;

  function navigate() {
    const second = location.hash === '#experiment-02' || (!location.hash && document.documentElement.dataset.initialExperiment==='02');
    show('lab-one',!second); show('lab-two',second);
    $('lab-switch-one').setAttribute('aria-pressed',String(!second));
    $('lab-switch-two').setAttribute('aria-pressed',String(second));
    document.title=(second?'Ordnungsgeometrie':'Eigenzeit-Labor')+' · X6 Spectral Astrolabium';
    $('lab-notebook').onclick=second?e=>{e.preventDefault();notebook();}:null;
    $('lab-background').onclick=second?e=>{e.preventDefault();$('og-contract').scrollIntoView();}:null;
    if (second && !started) { started=true; sourceChange(); drawScaling(); drawLis(); }
    if (!second && started && $('og-repeat').disabled) cancelTrials();
  }
  $('lab-switch-one').onclick = () => { location.hash='experiment-01'; };
  $('lab-switch-two').onclick = () => { location.hash='experiment-02'; };
  window.addEventListener('hashchange',navigate);

  function table(head,rows) {
    const wrapper=document.createElement('div'), el=document.createElement('table');
    wrapper.className='og-scroll'; wrapper.append(el);
    const tr=el.createTHead().insertRow();
    for (const col of head) { const th=document.createElement('th'); th.scope='col'; th.textContent=col; tr.append(th); }
    const body=el.createTBody();
    for (const row of rows) { const tr=body.insertRow(); for (const col of row) tr.insertCell().textContent=col; }
    return wrapper;
  }
  function note(text) { const p=document.createElement('p'); p.className='explain'; p.textContent=text; return p; }
  function cancelTrials() {
    ticket++; trials=null; $('og-repeat').disabled=false;
    set('og-progress',''); $('og-repeat-out').replaceChildren();
  }
  function invalidate(message) {
    current=null; cancelTrials(); $('og-export').disabled=true; show('og-observation',false);
    show('og-repeat-panel',false); set('og-error',message); show('og-error',Boolean(message));
    set('og-diagnosis','Für die Auswertung eine gültige Ordnung wählen.'); set('og-time','');
  }
  function inputNumber(id) {
    const el=$(id);
    if (!el.value || !el.checkValidity()) throw Error('Bitte eine gültige Zahl für '+el.labels[0].textContent+' eingeben.');
    return Number(el.value);
  }
  function options(id,nodes) {
    $(id).replaceChildren(...nodes.map((v,i) => new Option(String(v),String(i))));
  }
  function restrictFuture(wanted) {
    const a=Number($('og-p').value), select=$('og-q');
    select.replaceChildren();
    order.nodes.forEach((v,i) => { if (order.rel[a]?.[i]) select.add(new Option(String(v),String(i))); });
    if (Array.from(select.options).some(o => o.value===String(wanted))) select.value=String(wanted);
  }
  function initialiseSelection(endpoints) {
    const nodes=order.nodes;
    options('og-p',nodes);
    const a=endpoints ? order.index.get(endpoints[0]) : nodes.indexOf(3);
    $('og-p').value=String(a >= 0 ? a : 0);
    restrictFuture(endpoints ? order.index.get(endpoints[1]) : nodes.indexOf(7));
    $('og-scope').value=endpoints?'interval':'whole';
  }
  function sourceChange() {
    const mode=$('og-source').value, flat=mode==='flat', twins=mode==='twins', file=mode==='import';
    fileTicket++; order=null; graph=null; settings=null; twin=null;
    show('og-flat',flat); show('og-upload',file); show('og-random',flat||twins);
    show('og-selection',!flat&&!twins); show('og-twin-controls',twins);
    set('og-context',flat?'Uniformer Diamant':twins?'32 identische Ereignisse':file?'JSON-Import':'CST-DUST');
    try {
      let ep=null;
      if (file) {
        if (!loaded) { show('og-selection',false); invalidate('Eine JSON-Datei zum Auswerten wählen.'); return; }
        graph=loaded.graph; ep=loaded.endpoints;
      } else if (flat || twins) {
        const seed=inputNumber('og-seed'), random=P.rng(seed);
        if (flat) {
          settings={seed, m:inputNumber('og-m'),d:inputNumber('og-d'),theta:inputNumber('og-theta'),T:inputNumber('og-scale')};
          graph=O.simulation(random,settings);
        } else { twin=O.twin(random); graph=twin.graph; }
      } else graph=O.dust(mode);
      order=O.graphOrder(graph);
      if (ep) O.analyse(order,ep);
      initialiseSelection(ep); render();
    } catch (e) { invalidate(e.message); }
  }

  function mmText(result) {
    return ({TOO_FEW:'zu wenige Paare', NO_FINITE_ROOT:'kein endlicher Wert', BELOW_RANGE:result.value===1?'1 (unter 2)':'unter 2',
      ABOVE_RANGE:'über 4', IN_RANGE:result.value===null?'':fmt(result.value,2)})[result.status];
  }
  function drawOrder(s) {
    const c=$('og-graph'), ctx=c.getContext('2d'), w=c.clientWidth, h=c.clientHeight;
    if (!w || !h) return;
    const ratio=Math.min(window.devicePixelRatio||1,2);
    c.width=Math.round(w*ratio); c.height=Math.round(h*ratio); ctx.setTransform(ratio,0,0,ratio,0,0);
    ctx.clearRect(0,0,w,h);
    const groups=Array.from({length:s.height},()=>[]);
    s.ranks.forEach((rank,i)=>groups[rank-1].push(i));
    const pos=[], active=new Set(s.path), segments=new Set(s.path.slice(1).map((v,i)=>s.path[i]+','+v));
    // Keep successor branches near their already placed parents to reduce crossings.
    const parents=s.ids.map(()=>[]);
    for (const [a,b] of s.covers) parents[b].push(a);
    groups.forEach((row,rank)=>{
      const centre=v=>parents[v].length?parents[v].reduce((sum,a)=>sum+pos[a][0],0)/parents[v].length:w/2;
      row.sort((a,b)=>centre(a)-centre(b)||a-b);
      row.forEach((v,i)=>{
        pos[v]=[20+(w-40)*(i+.5)/row.length,h-20-(h-40)*(s.height===1?.5:rank/(s.height-1))];
      });
    });
    function line(i,j) {
      ctx.beginPath(); ctx.moveTo(...pos[i]); ctx.lineTo(...pos[j]); ctx.stroke();
    }
    ctx.lineWidth=1.4; ctx.strokeStyle=colors.edge;
    for (const [i,j] of s.covers) if (!segments.has(i+','+j)) line(i,j);
    ctx.lineWidth=4; ctx.strokeStyle=colors.purple;
    s.path.slice(1).forEach((j,i)=>line(s.path[i],j));
    const radius=s.k<35?6:Math.max(2,Math.min(4,250/Math.max(...groups.map(g=>g.length))));
    ctx.textAlign='left'; ctx.font=(w<450?'12':'15')+'px system-ui';
    for (const [i,p] of pos.entries()) {
      ctx.fillStyle=active.has(i)?colors.purple:colors.cyan;
      ctx.beginPath(); ctx.arc(...p,radius,0,2*Math.PI); ctx.fill();
      if (s.k<=35) { ctx.fillStyle=colors.text; ctx.fillText(String(s.ids[i]).slice(0,12),p[0]+9,p[1]+4,69); }
    }
    if (!s.k) { ctx.fillStyle=colors.text;ctx.textAlign='center';ctx.fillText('Keine inneren Ereignisse',w/2,h/2); }
  }
  function render() {
    if (!order) return;
    cancelTrials();
    try {
      const mode=$('og-source').value;
      const scoped= !settings && !twin && $('og-scope').value==='interval';
      show('og-ends',scoped);
      if (scoped && (!$('og-q').value || !$('og-p').value)) throw Error('Dieser Randpunkt hat keinen strikten Nachfolger. Bitte p neu wählen.');
      const ep=scoped?[order.nodes[+$('og-p').value],order.nodes[+$('og-q').value]]:null;
      const s=O.analyse(order,ep);
      const inference=O.infer(s,settings ? {m:settings.m,T:settings.T} : null,bank);
      current={schema:'x6.order-geometry/1', source:mode, graph:{nodes:graph.nodes,edges:graph.edges}, endpoints:ep,
        convention:'Strict order. Open interval excludes endpoints. Height counts selected events. Matrix follows observables.ids.',
        reference:bank.version, observables:s, inference, simulation:settings, twin:null};
      if (twin) {
        const curved=$('og-metric').value==='curved';
        current.twin={seed:inputNumber('og-seed'), h:twin.h, metric:curved?'de_sitter':'flat_density_twin',
          referenceTime:curved?twin.properTime:1, referenceRicci:curved?twin.ricci:0};
        set('og-twin-note','Vorgegebene Referenz: τ = '+fmt(current.twin.referenceTime)+', Ricci-Skalar = '+fmt(current.twin.referenceRicci)+'. Beim Umschalten bleiben alle Relationen gleich.');
      }
      show('og-error',false); show('og-observation',true); $('og-export').disabled=false;
      set('og-k',s.k); set('og-pairs',s.pairs); set('og-r',s.fraction===null?'—':fmt(s.fraction));
      set('og-h',s.height); set('og-layers',s.layers.join(' · ')); set('og-action','4D-Wirkungskombination K − N₀ + 9N₁ − 16N₂ + 8N₃ = '+s.action4+' (ohne Vorfaktor).');
      set('og-path','Zukunft oben. '+(s.path.length?'Eine längste Kette: '+s.path.map(i=>s.ids[i]).join(' → '):'Die Auswahl ist leer.'));
      drawOrder(s);
      const diag=$('og-diagnosis'), value=document.createElement('strong');
      value.textContent='Myrheim–Meyer: '+mmText(inference.mm); diag.replaceChildren(value);
      let compatible='Ausserhalb der endlichen Vergleichstabelle (K > 128).';
      if (inference.compatible) compatible=s.k<2?'Bei K < 2 fehlt die Paarinformation. Alle drei Dimensionen bleiben offen.':
        inference.compatible.length?'Mit der endlichen flachen Paarreferenz vereinbar: '+inference.compatible.map(d=>d+'D').join(', ')+'.':
        'Die beobachtete Paarzahl liegt ausserhalb aller drei Referenzbereiche.';
      diag.append(note(compatible+' Die Inversion vergleicht mit flachen Diamanten. Eine einzelne Ordnung kann zu mehreren Referenzdimensionen passen.'));
      const time=$('og-time');time.replaceChildren();show('og-repeat-panel',Boolean(settings));
      if (settings) {
        time.append(table(['Dimension','Volumenzeit','Kettenzeit','Volumenintervall¹'],inference.byDimension.map(row=>[
          row.d+'D',fmt(row.volume),fmt(row.chain)+(row.upperLimit?' *':''),fmt(row.lower)+' – '+fmt(row.upper)])));
        time.append(note('¹ Je angenommener Dimension: 97,5%-Zählintervall. Äussere Hülle über vereinbare Dimensionen: '+
          (inference.interval?inference.interval.map(x=>fmt(x)).join(' – '):'keine Zeitfreigabe')+
          '. Generatorreferenz τ = '+fmt(settings.theta*settings.T)+'. * Obergrenze T der Kettenkalibrierung.'));
        time.append(note('Kettenzeit durch Inversion der vorab berechneten mittleren Höhe über alle möglichen K bei festem m und d. Die Dimension stammt aus der Paarstatistik. Die Hülle berücksichtigt beide Unsicherheiten; Details im Prüfnotebook.'));
      } else time.append(note('Der Ausschnitt liefert eine Höhe in Ereignissen. Eine unabhängige Zeitkalibrierung ist für diese Ordnung nicht hinterlegt.'));
    } catch (e) { invalidate(e.message); }
  }

  async function repeat() {
    if (!current || !settings) return;
    cancelTrials(); const id=ticket, p={...settings}, n=200, rows=[];
    const seed=(p.seed^0x9e3779b9)>>>0, random=P.rng(seed);
    $('og-repeat').disabled=true;
    try {
      for (let i=0;i<n;i++) {
        if (id!==ticket) return;
        const s=O.analyse(O.graphOrder(O.simulation(random,p)));
        const result=O.infer(s,{m:p.m,T:p.T},bank);
        const match=result.compatible.length===1?result.compatible[0]:null;
        rows.push({k:s.k,pairs:s.pairs,height:s.height,compatible:result.compatible,
          conditional:result.byDimension[p.d-2], blind:match===null?null:result.byDimension[match-2]});
        if (i%5===4) {set('og-progress',(i+1)+' / 200');await new Promise(resolve=>setTimeout(resolve,0));}
      }
      if (id!==ticket) return;
      const stats=[], truth=p.theta*p.T;
      for (const [key,name] of [['conditional','Bei bekanntem d'],['blind','Blind, eindeutige Fälle']]) {
        const subset=rows.map(row=>row[key]).filter(Boolean);
        for (const [field,title] of [['volume','Volumen'],['chain','Kette']]) {
          const err=subset.map(row=>row[field]-truth);
          stats.push({scope:name,estimator:title,n:err.length,bias:err.length?err.reduce((a,b)=>a+b,0)/err.length:null,
            rmse:err.length?Math.sqrt(err.reduce((a,b)=>a+b*b,0)/err.length):null});
        }
      }
      trials={seed,truth,rows,stats};
      const nBlind=rows.filter(r=>r.blind).length, nNone=rows.filter(r=>!r.compatible.length).length;
      set('og-progress','200 / 200 abgeschlossen. Blind eindeutig: '+nBlind+', mehrdeutig: '+(n-nBlind-nNone)+', ohne passende Dimension: '+nNone+'.');
      $('og-repeat-out').replaceChildren(table(['Vergleich','Schätzer','Fälle','Bias','RMSE'],stats.map(r=>[r.scope,r.estimator,r.n,r.bias===null?'—':fmt(r.bias),r.rmse===null?'—':fmt(r.rmse)])));
    } catch(e) { if(id===ticket)set('og-progress','Abgebrochen: '+e.message); }
    finally {if(id===ticket)$('og-repeat').disabled=false;}
  }

  function drawScaling() {
    const d=Number($('og-curve-d').value), rows=bank.scaling[d], c=$('og-curve'), ctx=c.getContext('2d');
    const w=c.width,h=c.height, x=k=>54+(w-100)*Math.log(k/15)/Math.log(16384/15);
    const norm=r=>r.heightMean/r.k**(1/d), y=v=>h-43-v*(h-76)/2.25;
    ctx.clearRect(0,0,w,h); ctx.font='16px system-ui';ctx.fillStyle=colors.text;ctx.textAlign='right';
    for(const val of [0,.5,1,1.5,2]) {
      ctx.fillText(fmt(val,1),44,y(val)+4); ctx.strokeStyle=colors.grid;
      ctx.beginPath();ctx.moveTo(54,y(val));ctx.lineTo(w-30,y(val));ctx.stroke();
    }
    ctx.textAlign='left';ctx.fillText('Mittlere Höhe / K¹ᐟᵈ',54,18);
    ctx.beginPath();rows.forEach((r,i)=>{if(i===0)ctx.moveTo(x(r.k),y(norm(r)));else ctx.lineTo(x(r.k),y(norm(r)));});
    ctx.strokeStyle=colors.cyan;ctx.lineWidth=2;ctx.stroke();ctx.textAlign='center';
    for(const r of rows) {
      ctx.fillStyle=colors.cyan;ctx.beginPath();ctx.arc(x(r.k),y(norm(r)),4,0,2*Math.PI);ctx.fill();
      if ([15,100,1024,16384].includes(r.k)) {ctx.fillStyle=colors.text;ctx.fillText(fmt(r.k,0),x(r.k),h-17);}
    }
    $('og-curve-values').replaceChildren(table(['K','Wolken','L̄ / K¹ᐟᵈ','Standardfehler','dMM aus mittl. r'],rows.map(r=>[
      fmt(r.k,0),r.trials,fmt(norm(r)),fmt(r.heightSE/r.k**(1/d),4),mmText(O.mm(2*r.pairMean/(r.k*(r.k-1)),bank))])));
  }
  function drawLis() {
    const c=$('og-lis'),ctx=c.getContext('2d'),counts=bank.lis15,total=counts.reduce((a,b)=>a+b,0);
    ctx.clearRect(0,0,c.width,c.height);ctx.font='14px system-ui';ctx.textAlign='center';
    counts.slice(1).forEach((n,i)=>{const x=22+43*i, height=350*n/total;
      ctx.fillStyle=colors.purple;ctx.fillRect(x,166-height,28,height);
      ctx.fillStyle=colors.text;ctx.fillText(i+1,x+14,188);});
    ctx.textAlign='left';ctx.fillText('Häufigkeit · Maximum '+fmt(100*Math.max(...counts)/total,1)+' %',20,18);
  }
  function download(data,name,type) {
    const a=document.createElement('a'),url=URL.createObjectURL(new Blob([data],{type}));
    a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),2000);
  }
  function notebook() {
    const markdown=text=>({cell_type:'markdown',metadata:{},source:text});
    const code=text=>({cell_type:'code',execution_count:null,metadata:{},outputs:[],source:text});
    const cells=[
      markdown('# Eigenzeit-Labor · Experiment 02\nDie exportierte Datei eigenzeit-ordnung.json neben dieses Notebook legen. Die Matrix ist strikt und folgt observables.ids. Endpunkte eines offenen Intervalls sind ausgeschlossen.'),
      code('import json\nfrom collections import Counter\nfrom pathlib import Path\nimport numpy as np\ndata = json.loads(Path("eigenzeit-ordnung.json").read_text())'),
      code(/* NOTEBOOK_ANALYSE */),
      code("g = data['graph']\naudit = analyse(g['nodes'],g['edges'],data['endpoints'])\nassert audit == {k:data['observables'][k] for k in audit}\n{k:v for k,v in audit.items() if k != 'matrix'}"),
      markdown('## Modell und Kalibrierung\nIm flachen Modell gilt K ~ Bin(m, (τ/T)^d). Für die endliche Dimensionsdiagnose werden je K und d die drittkleinste und drittgrösste Paarzahl aus 255 Referenzwolken verwendet. Dieser inklusive Rangbereich schliesst unter Austauschbarkeit die wahre Dimension mit Wahrscheinlichkeit höchstens 6/256 aus (über Kalibrierung und neue Beobachtung). Zusammen mit dem Fehlerbudget 0,025 für das Zählintervall beträgt die Fehlwahrscheinlichkeit höchstens 0,025 + 6/256. Das ist eine Modellrechnung über beide Stichproben; die realisierte, pseudozufällige Referenzbank hat keine separat bewiesene bedingte Überdeckung. Die Kettenpunktschätzung invertiert E[L|m,d,τ/T] mit einer unabhängig simulierten Höhenreferenz.\n\nKettenhöhen zählen Ereignisse. N₀ zählt direkte Nachfolger. Die 4D-Kombination ist K−N₀+9N₁−16N₂+8N₃. Eine Krümmungsauslese verlangt zusätzliche Modellannahmen.'),
      code("data['inference']")];
    const nb={nbformat:4,nbformat_minor:4,metadata:{kernelspec:{display_name:'Python 3',language:'python',name:'python3'}},cells};
    download(JSON.stringify(nb,null,2),'eigenzeit-ordnung.ipynb','application/x-ipynb+json');
  }
  $('og-source').onchange=sourceChange;
  for (const id of ['og-m','og-d','og-theta','og-seed','og-scale']) $(id).addEventListener('input',sourceChange);
  $('og-metric').onchange=render; $('og-scope').onchange=render; $('og-q').onchange=render;
  $('og-p').onchange=()=>{restrictFuture(Number($('og-q').value));render();};
  $('og-next').onclick=()=>{ $('og-seed').value=String((Number($('og-seed').value)+1)>>>0);sourceChange(); };
  $('og-file').onchange=async()=>{
    const file=$('og-file').files[0],version=++fileTicket;
    if (!file) return;
    loaded=null;order=null;show('og-selection',false);invalidate('Datei wird gelesen …');
    try {
      if (file.size>4*1024*1024) throw Error('Die Datei überschreitet 4 MiB.');
      const value=JSON.parse(await file.text());
      if (version!==fileTicket) return;
      const exported=value.schema==='x6.order-geometry/1';
      const g=exported?value.graph:value, endpoints=value.endpoints??null;
      const candidate=O.graphOrder(g);
      if (endpoints!==null) O.analyse(candidate,endpoints);
      loaded={graph:{nodes:candidate.nodes,edges:g.edges},endpoints};sourceChange();
    } catch(e) { if(version===fileTicket)invalidate(e.message); }
  };
  $('og-curve-d').onchange=drawScaling; $('og-repeat').onclick=repeat; $('og-notebook').onclick=notebook;
  $('og-html').onclick=()=>$('export-html').click();
  $('og-export').onclick=()=>{ if(current)download(JSON.stringify({...current,repetitions:trials}),'eigenzeit-ordnung.json','application/json'); };
  new ResizeObserver(()=>{
    if (current && !$('lab-two').hidden) drawOrder(current.observables);
  }).observe($('og-graph').parentElement);
  navigate();
})();
