'use strict';
(() => {
const $=id=>document.getElementById(id), core=RAXCore;
let current=null,currentR=null,importedRuns=[],selftestOK=false,requestSerial=0;
const names={chain:'Vollständige Kette',antichain:'Antikette',percolation:'Transitive Perkolation',three_layer:'Dreischicht-Poset',minkowski_2d:'2D-Minkowski-Diamant',minkowski_4d:'4D-Minkowski-Diamant'};
const notes={percolation:'p gilt für Kanten vor dem transitiven Abschluss; der resultierende Ordnungsanteil ist eine andere Größe.',three_layer:'Feste Schichten ungefähr N/4, N/2, N/4; unabhängige Kanten zwischen Nachbarschichten. Kein gleichverteiltes KR-Gesamtensemble.',minkowski_2d:'Gleichverteilung im Raumzeitvolumen bei festem N. Die Gesamtzahl wird nicht poissonverteilt gezogen.',minkowski_4d:'Gleichverteilung im 4D-Raumzeitvolumen bei festem N. Die Zeitkoordinate wird mit dem korrekten Querschnittsgewicht gezogen.',chain:'Exakter Referenzfall: Jedes Ereignispaar ist vergleichbar.',antichain:'Exakter Referenzfall: Keine zwei Ereignisse sind vergleichbar.'};
const fmt=(x,d=4)=>x===null||x===undefined?'undefiniert':Number.isInteger(x)?String(x):Math.abs(x)<1e-10?'0':Number(x).toLocaleString('de-CH',{maximumFractionDigits:d});
function error(message){$('error').textContent=message;$('error').hidden=false;$('run-status').textContent='Berechnung nicht abgeschlossen.';}
function clearError(){$('error').hidden=true;$('error').textContent='';}
function clearResult(){current=null;currentR=null;$('results').hidden=true;$('export-button').disabled=true;}
function note(){$('probability').disabled=!['percolation','three_layer'].includes($('model').value);$('ensemble-note').textContent=notes[$('model').value];}
function svgStart(label){return `<svg viewBox="0 0 540 250" role="img" aria-label="${label}">`;}
function bars(container,values,color='#6ee7ce',xCaption='Index'){
  if(!values.length){$(container).innerHTML='<p class="empty">Keine Werte für dieses leere Objekt.</p>';return;}
  const lo=Math.min(0,...values),hi=Math.max(1,...values),span=hi-lo,w=470/values.length;
  const y=v=>206-(v-lo)/span*176,zero=y(0);let svg=svgStart('Balkendiagramm der berechneten Werte');
  for(let k=0;k<=4;k++){const v=lo+span*k/4;svg+=`<line class="gridline" x1="50" x2="520" y1="${y(v)}" y2="${y(v)}"/><text x="43" y="${y(v)+4}" text-anchor="end">${fmt(v,1)}</text>`;}
  values.forEach((v,i)=>{const top=Math.min(zero,y(v)),height=Math.abs(y(v)-zero);svg+=`<rect x="${51+i*w}" y="${top}" width="${Math.max(.4,w-1.5)}" height="${Math.max(.2,height)}" fill="${v<0?'#c3afff':color}"><title>${i}: ${v}</title></rect>`;});
  svg+=`<line class="axis" x1="50" x2="520" y1="${zero}" y2="${zero}"/><text x="50" y="230">0</text><text x="520" y="230" text-anchor="end">${values.length-1}</text><text x="285" y="246" text-anchor="middle">${xCaption}</text></svg>`;
  $(container).innerHTML=svg;
}
function line(container,points,label,color='#6ee7ce',maxY=null){
  if(!points.length)return;
  const minX=points[0][0],maxX=points[points.length-1][0],top=maxY??Math.max(1,...points.map(p=>p[1]));
  const x=v=>50+(v-minX)/Math.max(1e-12,maxX-minX)*470,y=v=>206-v/top*176;
  let svg=svgStart(label);
  for(let k=0;k<=4;k++){let v=top*k/4;svg+=`<line class="gridline" x1="50" x2="520" y1="${y(v)}" y2="${y(v)}"/><text x="43" y="${y(v)+4}" text-anchor="end">${fmt(v,2)}</text>`;}
  svg+=`<polyline points="${points.map(p=>x(p[0])+','+y(p[1])).join(' ')}" fill="none" stroke="${color}" stroke-width="2"/>`;
  if(points.length<=12)for(const p of points)svg+=`<circle cx="${x(p[0])}" cy="${y(p[1])}" r="3" fill="${color}"/>`;
  svg+=`<text x="50" y="230">${fmt(minX,2)}</text><text x="520" y="230" text-anchor="end">${fmt(maxX,2)}</text><text x="285" y="246" text-anchor="middle">${label}</text></svg>`;
  $(container).innerHTML=svg;
}
function matrix(r){
  const n=r.length;if(!n){$('matrix-chart').innerHTML='<p class="empty">Leere Ordnung.</p>';return;}
  const unit=190/n;let svg=svgStart('Relationsmatrix: Zeilen sind Quellen, Spalten sind Ziele');
  svg+='<rect x="165" y="20" width="190" height="190" fill="#0b1423"/>';
  r.forEach((row,i)=>row.forEach((v,j)=>{if(v)svg+=`<rect x="${165+j*unit}" y="${20+i*unit}" width="${unit}" height="${unit}" fill="#6ee7ce"><title>${i} ≺ ${j}</title></rect>`;}));
  svg+=`<text x="260" y="236" text-anchor="middle">Ziel j · 0 … ${n-1}</text><text x="135" y="115" text-anchor="middle" transform="rotate(-90 135 115)">Quelle i · 0 … ${n-1}</text></svg>`;
  $('matrix-chart').innerHTML=svg;
}
function tableRow(body,values){const tr=document.createElement('tr');for(let i=0;i<values.length;i++){const td=document.createElement('td');td.textContent=String(values[i]);if(i>0)td.className='num';tr.appendChild(td);}body.appendChild(tr);}
async function digest(r){
  if(!globalThis.crypto?.subtle)return null;
  const bytes=new TextEncoder().encode(r.length+'\n'+r.map(row=>row.join('')+'\n').join(''));
  const hash=await crypto.subtle.digest('SHA-256',bytes);
  return Array.from(new Uint8Array(hash),x=>x.toString(16).padStart(2,'0')).join('');
}
function renderSpectrum(){if(!current)return;const key=$('spectrum-kind').value;bars('spectrum-chart',current.metrics[key]);$('spectrum-note').textContent=`${current.metrics.size} Eigenwerte · zyklisches Jacobi-Verfahren · relative Offdiagonal-Toleranz 10⁻¹²`;;}
function render(){
  const m=current.metrics;$('results').hidden=false;$('export-button').disabled=false;
  $('result-heading').textContent=names[current.generator?.model]||'Importierte endliche Ordnung';
  $('result-meta').replaceChildren();for(const value of [`N = ${m.size}`,`Seed ${current.generator?.seed??'unbekannt'}`,`Ordnungsanteil ${fmt(m.ordering_fraction)}`]){const span=document.createElement('span');span.textContent=value;$('result-meta').appendChild(span);}
  $('m-relations').textContent=`${m.relations} / ${m.links}`;$('m-bdg').textContent=m.bdg4_bracket;$('m-fiedler').textContent=fmt(m.algebraic_connectivity);$('m-height').textContent=m.height;
  renderSpectrum();bars('interval-chart',m.interval_counts,'#c3afff','Innere Ereignisse k');matrix(currentR);
  const tbody=$('diagnostics-table');tbody.replaceChildren();
  for(const [label,v] of [['Spektralradius H',m.spectral_radius],['Spektralbreite H',m.adjacency_spectral_width],['H²-Spektralentropie · nats',m.h2_spectral_entropy],['Spektralstandardabweichung',m.adjacency_spectral_std],['Dreiecke im Vergleichbarkeitsgraphen',m.triangles],['Ordnungsanteil 2M / N(N−1)',m.ordering_fraction]])tableRow(tbody,[label,fmt(v)]);
  $('matrix-hash').textContent=current.relation_sha256?`Matrix SHA-256: ${current.relation_sha256}`:'SHA-256 hier nicht verfügbar; die vollständige Matrix ist im Export enthalten.';
  runThinning();
}
function runThinning(){
  if(!currentR)return;
  try{const q=Number($('retention').value),steps=Number($('steps').value);if(!Number.isInteger(steps)||steps<0||steps>8)throw new Error('Schritte müssen zwischen 0 und 8 liegen');
    const data=core.thinning(currentR,q,steps,104729);current.thinning=data;
    line('thinning-chart',data.path.map(x=>[x.step,x.metrics.size]),'Schritt · Anzahl erhaltener Ereignisse');
    const body=$('thinning-table');body.replaceChildren();for(const row of data.path)tableRow(body,[row.step,row.metrics.size,row.metrics.relations,fmt(row.metrics.ordering_fraction),row.metrics.bdg4_bracket]);
  }catch(e){delete current.thinning;$('thinning-chart').innerHTML='';$('thinning-table').replaceChildren();error(e.message);}
}
async function run(event){
  const serial=++requestSerial;
  event?.preventDefault();clearError();clearResult();if(!selftestOK){error('Referenzprüfungen müssen zuerst bestehen.');return;}
  $('run-button').disabled=true;$('run-status').textContent='Relationsmatrix und Spektren werden berechnet …';
  await new Promise(resolve=>setTimeout(resolve,0));
  try{const n=Number($('size').value),seed=Number($('seed').value),p=$('probability').disabled ? 0.25 : Number($('probability').value);
    if(!Number.isInteger(n)||n<4||n>96)throw new Error('N muss eine ganze Zahl von 4 bis 96 sein');
    const next=core.experiment($('model').value,n,seed,p),r=core.loadExperiment(next);
    next.relation_sha256=await digest(r);if(serial!==requestSerial)return;
    next.origin={kind:'browser_generation',solver:'cyclic_jacobi',core_version:core.VERSION};current=next;currentR=r;
    render();if($('error').hidden)$('run-status').textContent='Endliche Berechnung abgeschlossen. Kein physikalischer Validierungsstatus.';
  }catch(e){if(serial===requestSerial){clearResult();error(e.message);}}finally{if(serial===requestSerial)$('run-button').disabled=false;}
}
async function useImported(index){
  const serial=++requestSerial;
  clearError();clearResult();
  try{const record=importedRuns[index],r=core.loadExperiment(record),hash=await digest(r);if(serial!==requestSerial)return;
    if(record.relation_sha256&&hash&&record.relation_sha256!==hash)throw new Error('SHA-256 stimmt nicht mit der importierten Matrix überein');
    if(record.relation_sha256&&!hash)throw new Error('Dieser Browser kann die importierte Prüfsumme nicht verifizieren');
    current={schema:'RAX-CQG-EXPERIMENT-0.2',software_version:core.VERSION,evidence_class:'FINITE_ORDER_BENCHMARK',generator:record.generator||{model:'imported'},relation_rows:core.loadExperiment(record).map(row=>row.join('')),relation_sha256:hash,metrics:core.diagnose(r),origin:{kind:'matrix_import',stored_metrics_used:false,generator_replay_checked:false}};
    currentR=r;render();if($('error').hidden)$('run-status').textContent='Matrix geprüft; Kennzahlen neu berechnet. Generatorangaben stammen aus der importierten Datei.';
  }catch(e){if(serial===requestSerial){clearResult();error(e.message);}}finally{if(serial===requestSerial)$('run-button').disabled=false;}
}
async function importFile(event){
  const file=event.target.files[0];if(!file)return;
  try{if(file.size>20*1024*1024)throw new Error('Import auf 20 MB begrenzt');const data=JSON.parse(await file.text());
    importedRuns=data.schema==='RAX-CQG-SWEEP-0.2'?data.runs:[data];
    if(!Array.isArray(importedRuns)||!importedRuns.length||importedRuns.length>1000)throw new Error('Ungültige Anzahl Experimente');
    const select=$('dataset-run');select.replaceChildren();importedRuns.forEach((record,i)=>{const option=document.createElement('option');option.value=i;option.textContent=`${i+1} · ${names[record.generator?.model]||'Import'} · N=${record.relation_rows?.length??'?'} · Seed ${record.generator?.seed??'?'}`;select.appendChild(option);});
    $('dataset-picker').hidden=importedRuns.length===1;$('dataset-note').textContent=`${importedRuns.length} Experimente. Gespeicherte Kennzahlen werden beim Auswählen durch Neuberechnung ersetzt.`;await useImported(0);
  }catch(e){clearResult();error(e.message);}finally{event.target.value='';}
}
function exportFile(){if(!current)return;const blob=new Blob([JSON.stringify(current,null,2)+'\n'],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='rax_cqg_experiment.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
$('model').addEventListener('change',note);$('experiment-form').addEventListener('submit',run);$('thin-button').addEventListener('click',()=>{clearError();runThinning();});$('spectrum-kind').addEventListener('change',renderSpectrum);$('export-button').addEventListener('click',exportFile);$('import-file').addEventListener('change',importFile);$('dataset-run').addEventListener('change',event=>useImported(Number(event.target.value)));
note();
try{const tests=core.selfTest();selftestOK=tests.passed===tests.total;$('selftest-status').textContent=`Selbstprüfung: ${tests.passed}/${tests.total} endliche Referenzfälle bestanden.`;$('selftest-status').className='status '+(selftestOK?'success':'warning');if(!selftestOK)throw new Error('Mindestens eine Referenzprüfung ist fehlgeschlagen');const clock=core.clockReference(65);line('clock-chart',clock.samples.map(x=>[x.tau,x.p_plus_x]),'Uhrparameter τ · P(+x | τ)','#c3afff',1);run();}catch(e){error(e.message);$('run-button').disabled=true;}
})();
