/* SPDX-License-Identifier: Apache-2.0 */
(() => {
  'use strict';
  const P=ProperTime, $=id=>document.getElementById(id), budgets=[64,256,1024,4096,16384];
  const fmt=(n,d=3)=>n.toLocaleString('de-CH',{minimumFractionDigits:d,maximumFractionDigits:d});
  const int=n=>n.toLocaleString('de-CH'), cyan='#68e6d2', muted='#9bafcc', orange='#ffb077';
  let current=null, repetitions=null, generation=0, timer;
  const svg=(tag,attrs,text='')=>`<${tag} ${Object.entries(attrs).map(([k,v])=>`${k}="${v}"`).join(' ')}>${text}</${tag}>`;
  const line=(x1,y1,x2,y2,color,width=1,dash='')=>svg('line',{x1,y1,x2,y2,stroke:color,'stroke-width':width,'stroke-dasharray':dash});
  const label=(x,y,text,color=muted,size=12,anchor='middle')=>svg('text',{x,y,fill:color,'font-family':'system-ui,sans-serif','font-size':size,'text-anchor':anchor},text);
  function params() {
    const p={d:Number($('dimension').value),m:budgets[Number($('budget').value)],theta:Number($('theta').value)/100,seed:Number($('seed').value),T:Number($('scale').value)};
    if ($('seed').value.trim()==='') throw Error('Bitte einen Seed eingeben.');
    P.rng(p.seed); P.infer(0,p.m,p.d,.05,p.T);
    return p;
  }
  function cloudPlot(c,p,chain) {
    const X=x=>320+x*380,Y=t=>220-t*380;
    let s='<title id="cloud-svg-title">Raumzeitdiamant mit markierten Endpunkten</title><desc id="cloud-svg-desc">Alle Vergleiche verwenden die vollständigen Raumzeitkoordinaten. Die Grafik zeigt t und x₁.</desc>';
    for(let a=-.5;a<=.501;a+=.1) {s+=line(X(-.6),Y(a),X(.6),Y(a),'#1d2a40');s+=line(X(a),Y(-.5),X(a),Y(.5),'#1d2a40');}
    s+=line(X(-.62),Y(0),X(.62),Y(0),'#40516a');s+=line(X(0),Y(-.53),X(0),Y(.53),'#40516a');
    const diamond=r=>`${X(0)},${Y(r)} ${X(r)},${Y(0)} ${X(0)},${Y(-r)} ${X(-r)},${Y(0)}`;
    s+=svg('polygon',{points:diamond(.5),fill:'#16253a',stroke:'#63789a','stroke-width':1.4});
    s+=svg('polygon',{points:diamond(p.theta/2),fill:'#183b3d',stroke:cyan,'stroke-width':1.5,'stroke-dasharray':'5 5'});
    // A deterministic display subset; inference always uses every point.
    const n=Math.min(c.points.length,1400);
    for(let j=0;j<n;j++) {
      const i=Math.floor(j*c.points.length/n),pt=c.points[i];
      s+=svg('circle',{cx:X(pt[1]),cy:Y(pt[0]),r:c.inside[i]?2.7:1.8,fill:c.inside[i]?cyan:'#8194b5',opacity:c.inside[i]?.9:.5});
    }
    if(chain.path.length) {
      const seq=[[0,-p.theta/2],...chain.path.map(i=>[c.points[i][1],c.points[i][0]]),[0,p.theta/2]];
      s+=svg('polyline',{points:seq.map(([x,t])=>`${X(x)},${Y(t)}`).join(' '),fill:'none',stroke:'#b8a3ff','stroke-width':2.2,opacity:.95});
    }
    for(const [t,name] of [[-p.theta/2,'p'],[p.theta/2,'q']]) {
      s+=svg('circle',{cx:X(0),cy:Y(t),r:5,fill:'#fff',stroke:'#111b2b','stroke-width':2});
      s+=label(X(0)+14,Y(t)+4,name,'#fff',15,'start');
    }
    s+=label(330,18,'t / T',muted,12,'start');s+=label(600,211,'x₁ / T');
    s+=label(320,448,p.d>2?'Projektion: weitere Raumkoordinaten sind ausgeblendet.':'Vollständige 1+1-dimensionale Darstellung.',muted,11);
    $('cloud').innerHTML=s;
    $('point-note').textContent=`Gezeigt: ${int(n)} von ${int(p.m)} Punkten. Gezählt: alle ${int(p.m)}.`;
    $('chain-note').textContent=chain.height===null ? 'Kettenanzeige nur für K ≤ 256.' : `Längste innere Kette: ${chain.height} Knoten (ohne p, q).`;
  }
  function intervalPlot(c,p) {
    const x=v=>45+610*v/p.T, y=45;
    let s=line(45,y,655,y,'#3b4b65',2);
    for(let i=0;i<=4;i++) {const xx=45+i*610/4;s+=line(xx,y-5,xx,y+5,'#62758e');s+=label(xx,96,fmt(i*p.T/4,2));}
    s+=line(x(c.lower),y,x(c.upper),y,cyan,8);
    s+=line(x(p.theta*p.T),15,x(p.theta*p.T),72,'#fff',2,'3 3');
    s+=svg('circle',{cx:x(c.estimate),cy:y,r:6,fill:cyan,stroke:'#0b1423','stroke-width':2});
    $('interval').innerHTML=s;
  }
  function resolution(p) {
    const ms=[64,128,256,512,1024,2048,4096,8192,16384],values=ms.map(m=>P.exactMoments(m,p.d,p.theta));
    const max=Math.max(...values.map(v=>v.rmse))*1.12,X=i=>55+i*62,Y=v=>205-v/max*165;
    let s='';
    for(let i=0;i<4;i++){const v=max*i/3;s+=line(55,Y(v),551,Y(v),'#27354b');s+=label(46,Y(v)+4,fmt(v),muted,11,'end');}
    s+=svg('polyline',{points:values.map((v,i)=>`${X(i)},${Y(v.rmse)}`).join(' '),fill:'none',stroke:cyan,'stroke-width':2.5});
    values.forEach((v,i)=>{s+=svg('circle',{cx:X(i),cy:Y(v.rmse),r:ms[i]===p.m?5:3,fill:ms[i]===p.m?'#fff':cyan});if(i%2===0)s+=label(X(i),228,int(ms[i]),muted,11);});
    s+=label(55,20,'RMSE / T',muted,11,'start');s+=label(570,244,'m',muted,12);
    $('resolution').innerHTML=s;
    const v=P.exactMoments(p.m,p.d,p.theta);
    $('resolution-note').textContent=`Aktuell: E[K] = ${fmt(v.expectedK,2)} · P(K = 0) = ${fmt(v.zeroProbability*100,2)} % · theoretischer RMSE / T = ${fmt(v.rmse,4)}. Keine Mindestgenauigkeit für jeden einzelnen Versuch.`;
  }
  function run() {
    generation++;repetitions=null;$('repeat-results').hidden=true;$('repeat-status').textContent='Noch keine Wiederholungen berechnet.';$('repeat').disabled=false;
    try {
      const p=params(), c=P.cloud(p), chain=P.longestChain(c.points,c.inside);
      current={parameters:p,result:c,chain};$('error').hidden=true;$('export').disabled=false;
      $('budget-label').textContent=int(p.m);$('theta-label').textContent=fmt(p.theta,2);
      $('dimension-badge').textContent=p.d===2?'1 Raum + 1 Zeit':`${p.d}D → 2D-Projektion`;
      $('count').textContent=int(c.k);$('estimate').textContent=fmt(c.estimate);$('truth').textContent=fmt(p.theta*p.T);
      $('estimate-unit').textContent=p.T===1?'T = 1 · normierte Einheiten':`T = ${fmt(p.T)} · vorgegebene Zeiteinheiten`;
      $('interval-text').textContent=`[${fmt(c.lower)}; ${fmt(c.upper)}]`;
      const covered=c.lower<=p.theta*p.T && p.theta*p.T<=c.upper;
      $('interval-status').textContent=covered?'Die bekannte Referenz liegt in diesem Intervall.':'Dieser Versuch verfehlt die bekannte Referenz.';
      $('interval-status').style.color=covered?cyan:orange;
      $('zero-note').textContent=c.k===0?'K = 0: Keine inneren Ereignisse beobachtet. Die obere Zeitgrenze ist trotzdem positiv.':'Die Wurzelschätzung kann bei endlichen Stichproben nach unten verzerrt sein.';
      cloudPlot(c,p,chain);intervalPlot(c,p);resolution(p);
    } catch(e) {
      current=null;$('error').textContent=e.message+' Bitte Eingaben korrigieren; der zuletzt gezeigte Versuch wird nicht exportiert.';$('error').hidden=false;$('repeat').disabled=true;$('export').disabled=true;
    }
  }
  function repeatsPlot(rows,p) {
    const shown=rows.slice(0,40),x=i=>45+i*23.3,Y=v=>270-230*v;
    let s='';
    for(let j=0;j<=4;j++) {const v=j/4;s+=line(35,Y(v),975,Y(v),'#27354b');s+=label(28,Y(v)+4,fmt(v*p.T,2),muted,11,'end');}
    s+=line(35,Y(p.theta),975,Y(p.theta),'#fff',1.5,'4 4');
    shown.forEach((r,i)=>{const col=r.covered?cyan:orange;s+=line(x(i),Y(r.lower/p.T),x(i),Y(r.upper/p.T),col,2);s+=svg('circle',{cx:x(i),cy:Y(r.estimate/p.T),r:2.8,fill:col});if(i%5===0)s+=label(x(i),295,i+1,muted,11);});
    s+=label(975,20,'τ · erste 40 Wiederholungen',muted,12,'end');$('repeat-plot').innerHTML=s;
  }
  async function repeat() {
    if(!current)return;
    const ticket=generation,p={...current.parameters},random=P.rng((p.seed^0x9e3779b9)>>>0),rows=[],cache=new Map();
    $('repeat').disabled=true;$('repeat-results').hidden=true;
    try {
      for(let i=0;i<200;i++) {
        if(ticket!==generation)return;
        const k=P.binomial(p.m,p.theta**p.d,random);
        if(!cache.has(k))cache.set(k,P.infer(k,p.m,p.d,.05,p.T));
        const v=cache.get(k);rows.push({...v,covered:v.lower<=p.theta*p.T&&p.theta*p.T<=v.upper});
        if(i%10===9) {$('repeat-status').textContent=`${i+1} / 200 Versuche berechnet …`;await new Promise(resolve=>setTimeout(resolve,0));}
      }
      if(ticket!==generation)return;
      const hit=rows.filter(r=>r.covered).length,errors=rows.map(r=>r.thetaHat-p.theta);
      const band=P.infer(hit,200,2),rmse=Math.sqrt(errors.reduce((s,x)=>s+x*x,0)/200),bias=errors.reduce((s,x)=>s+x,0)/200;
      repetitions={seed:(p.seed^0x9e3779b9)>>>0,n:200,hits:hit,rmse,bias,coverageInterval:[band.aLow,band.aHigh],rows};
      $('coverage').textContent=`${hit} / 200 · ${fmt(hit/2,1)} %`;
      $('coverage-band').textContent=`95%-Intervall für die Überdeckungsrate: ${fmt(100*band.aLow,1)}–${fmt(100*band.aHigh,1)} %`;
      $('rmse').textContent=fmt(rmse,4);$('bias').textContent=fmt(bias,4);repeatsPlot(rows,p);
      $('repeat-results').hidden=false;$('repeat-status').textContent='200 / 200 abgeschlossen. Alle Ergebnisse sind im JSON-Export enthalten.';
    } catch(e) {$('repeat-status').textContent='Berechnung abgebrochen: '+e.message;}
    finally {if(ticket===generation)$('repeat').disabled=false;}
  }
  function download(text,name,type) {
    const url=URL.createObjectURL(new Blob([text],{type})),a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),2000);
  }
  function exportData() {
    if(!current)return;
    download(JSON.stringify({schema:P.VERSION,mode:'FIXED_BUDGET_BINOMIAL',inference:'Clopper-Pearson transformed by theta=a^(1/d)',alpha:.05,randomGenerator:'mulberry32; finite pseudo-random approximation',coordinateUnits:'T',assumptions:['known flat Minkowski geometry','known d and external T','iid uniform volume points','preselected contained central endpoints','fixed budget; no optional-stopping guarantee'],...current,repetitions},null,2),'eigenzeit-versuch.json','application/json');
  }
  ['dimension','budget','theta','seed','scale'].forEach(id=>$(id).addEventListener('input',()=>{clearTimeout(timer);generation++;$('repeat').disabled=true;$('export').disabled=true;timer=setTimeout(run,180);}));
  $('run').addEventListener('click',()=>{clearTimeout(timer);run();});
  $('new-seed').addEventListener('click',()=>{const n=Number($('seed').value);$('seed').value=String(((Number.isInteger(n)?n:20261017)+1)>>>0);clearTimeout(timer);run();});
  document.querySelectorAll('[data-preset]').forEach(b=>b.addEventListener('click',()=>{
    const settings={sparse:[4,1,10],dense:[4,4,50],two:[2,2,50]}[b.dataset.preset];
    $('dimension').value=settings[0];$('budget').value=settings[1];$('theta').value=settings[2];$('scale').value=1;$('seed').value=20261017;clearTimeout(timer);run();
  }));
  $('repeat').addEventListener('click',repeat);$('export').addEventListener('click',exportData);
  $('export-html').addEventListener('click',()=>{
    const doc=document.documentElement.cloneNode(true),base=document.createElement('base');
    base.href='https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/';doc.querySelector('head').prepend(base);
    download('<!doctype html>\n'+doc.outerHTML,'eigenzeit-demonstrator.html','text/html');
  });
  run();
})();
