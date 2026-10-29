import {makeModel,analyze,horizon,PRESETS,BASE_COMMIT,SOURCE_URL,exportRecord} from './engine.mjs';
const $=id=>document.getElementById(id),NS='http://www.w3.org/2000/svg';
const colors={cyan:'#66e5da',rose:'#f08ba5',amber:'#efbd71',lavender:'#aba7fa',muted:'#61778f'};
let state={preset:'cspp',...PRESETS.cspp,eta:0.01,pattern:'worst'},model,result,curve=[],curveKey='',timer=null,progress=6,selected='d';
const number=(x,d=3)=>{
 if(x===0)return '0';if(!Number.isFinite(x))return 'nicht bestimmbar';
 if(Math.abs(x)<10**(-d)||Math.abs(x)>=10000)return x.toExponential(2).replace('.',',').replace('e-','e−');
 return new Intl.NumberFormat('de-CH',{maximumFractionDigits:d,minimumFractionDigits:Math.abs(x)>=0.01&&Math.abs(x)<10?Math.min(d,3):0}).format(x).replace('.',',');
};
const precise=x=>number(x,7);
function el(tag,attributes={},text){const x=document.createElementNS(NS,tag);for(const[k,v]of Object.entries(attributes))x.setAttribute(k,String(v));if(text!==undefined)x.textContent=text;return x;}
function svgText(svg,x,y,text,extra={}){const t=el('text',{x,y,...extra},text);svg.append(t);return t;}
function stop(){if(timer)clearInterval(timer);timer=null;$('play').innerHTML='<span aria-hidden="true">▶</span> Berechnung abspielen';}
function syncControls(){
 for(const b of document.querySelectorAll('[data-preset]')){const chosen=b.dataset.preset===state.preset;b.classList.toggle('selected',chosen);b.setAttribute('aria-pressed',String(chosen));}
 $('node-count').value=state.n;$('node-count-out').value=state.n;
 $('theta').value=state.theta;$('theta-out').value=number(state.theta,2);
 $('coupling').value=state.gain;$('coupling-out').value=number(state.gain,2);
 $('mismatch').value=state.mismatch;$('mismatch-out').value=`${Math.round(state.mismatch*100)} %`;
 $('eta').value=Math.log10(state.eta);$('eta-out').value=number(state.eta,4);$('pattern').value=state.pattern;
 $('theta-control').hidden=state.preset!=='cspp';$('coupling-control').hidden=state.preset==='cspp';$('mismatch-control').hidden=state.preset!=='cancel';
}
function update(){
 try{
  stop();model=makeModel(state);result=analyze(model,{eta:state.eta,pattern:state.pattern});progress=state.n+1;
  const key=JSON.stringify([state.preset,state.theta,state.gain,state.mismatch]);
  if(key!==curveKey){curve=horizon(state,24).filter(x=>x.n>=3);curveKey=key;}
  $('error').hidden=true;syncControls();
  $('gain-value').textContent=number(result.historyGain);$('bound-value').textContent=number(result.pathBound);$('resolvent-value').textContent=number(result.resolventGain);$('cancellation-value').textContent=number(result.cancellation*100,1);
  $('probe-value').textContent=precise(result.detectorResponse);
  $('probe-note').textContent=state.pattern==='worst'?'Vorzeichen erreichen die endliche History-Norm.':`Betragsschranke: η · ΓH = ${precise(state.eta*result.historyGain)}`;
  $('model-description').textContent=model.description;
  $('graph-count').textContent=`${result.history.length} History · ${state.n} aktiv · 1 Probe`;
  if(!model.nodes.some(n=>n.id===selected))selected='d';
  $('node-select').replaceChildren(...result.order.map(n=>{const o=document.createElement('option');o.value=n.id;o.textContent=`${n.label} · ${n.role==='history'?'History':n.role==='active'?'aktiv':'Probe'}`;return o;}));
  $('node-select').value=selected;$('progress').max=state.n+1;
  renderGraph();renderNode();renderHorizon();renderPaths();renderInterpretation();
 }catch(e){stop();$('error').hidden=false;$('error').textContent=`Berechnung angehalten: ${e.message}`;}
}
function positions(){
 const width=Math.max(1000,state.n*65+340),height=350,pos={};
 result.history.forEach((n,i)=>{pos[n.id]={x:78,y:result.history.length===1?178:87+i*90};});
 result.active.forEach((n,i)=>{pos[n.id]={x:220+i*(width-430)/Math.max(1,state.n-1),y:state.preset==='cancel'&&i<2?(i===0?98:258):178+(i%2?28:-28)};});
 pos[result.detector.id]={x:width-75,y:178};return {pos,width,height};
}
function renderGraph(){
 const svg=$('network'),{pos,width,height}=positions();svg.replaceChildren(el('title',{id:'network-svg-title'},'Schematischer Transfergraph. Knoten sind per Tastatur auswählbar; Abstände sind keine physikalischen Entfernungen.'));svg.setAttribute('viewBox',`0 0 ${width} ${height}`);svg.style.minWidth=`${Math.max(650,state.n*53+300)}px`;
 const defs=el('defs');for(const [key,color]of Object.entries(colors)){
  const marker=el('marker',{id:`arrow-${key}`,viewBox:'0 0 10 10',refX:8,refY:5,markerWidth:4,markerHeight:4,orient:'auto-start-reverse'});marker.append(el('path',{d:'M 0 0 L 10 5 L 0 10 z',fill:color}));defs.append(marker);
 }svg.append(defs);
 svgText(svg,78,29,'HISTORY',{'text-anchor':'middle',class:'graph-group-label'});svgText(svg,(width-150)/2+70,29,'AKTIVE ÜBERTRAGUNG',{'text-anchor':'middle',class:'graph-group-label'});svgText(svg,width-75,29,'PROBE',{'text-anchor':'middle',class:'graph-group-label'});
 const completed=new Set([...result.history.map(n=>n.id),...result.active.slice(0,progress).map(n=>n.id),...(progress>state.n?['d']:[])]);
 const all=model.edges.map(e=>({...e,contribution:e.weight*result.values[e.from]}));let edges=all;
 const view=$('edge-view').value;if(view==='strong')edges=all.slice().sort((a,b)=>Math.abs(b.contribution)-Math.abs(a.contribution)).slice(0,12);if(view==='selected')edges=all.filter(e=>e.to===selected);
 const maximum=Math.max(1e-300,...all.map(e=>Math.abs(e.contribution)));
 for(const e of edges){
  const a=pos[e.from],b=pos[e.to],sgn=e.contribution>0?'cyan':e.contribution<0?'rose':'muted';
  const dx=b.x-a.x,curveOffset=dx>170?Math.min(110,dx*.13)*(e.weight>=0?-1:1):0;
  const path=el('path',{d:`M ${a.x+14} ${a.y} C ${a.x+dx*.38} ${a.y+curveOffset} ${b.x-dx*.35} ${b.y+curveOffset} ${b.x-20} ${b.y}`,fill:'none',stroke:colors[sgn],'stroke-width':.65+2.3*Math.sqrt(Math.abs(e.contribution)/maximum),'marker-end':`url(#arrow-${sgn})`,opacity:completed.has(e.to)?(e.to===selected?.9:.43):.09,class:'edge'});
  path.append(el('title',{},`${e.from} → ${e.to}: Gewicht ${precise(e.weight)}, Beitrag ${precise(e.contribution)}`));svg.append(path);
 }
 const maxValue=Math.max(state.eta,1e-300,...Object.values(result.values).map(Math.abs));
 for(const n of result.order){
  const p=pos[n.id],value=result.values[n.id],done=completed.has(n.id),color=value>=0?colors.cyan:colors.rose;
  const g=el('g',{class:`node ${n.id===selected?'selected':''}`,tabindex:0,role:'button','aria-label':`${n.label}, ${n.role==='history'?'History':n.role==='active'?'aktiv':'Probe'}, Antwort ${precise(value)}`,transform:`translate(${p.x},${p.y})`});
  if(done&&n.role!=='history')g.append(el('circle',{r:23+7*Math.sqrt(Math.abs(value)/maxValue),fill:color,opacity:.05+Math.min(.08,Math.abs(value)/maxValue*.08)}));
  g.append(el('circle',{r:n.role==='detector'?18:14,fill:done?(n.role==='history'?'#1c2a3b':'#123031'):'#131d2a',stroke:done?(n.role==='history'?'#819bb7':color):'#3b4a60','stroke-width':1.6,opacity:done?1:.5}));
  if(n.role==='detector')g.append(el('circle',{r:12,fill:'none',stroke:done?color:'#3b4a60','stroke-width':.6}));
  g.append(el('text',{y:4,class:'node-label','font-size':n.role==='detector'?12:9},n.label));
  g.append(el('text',{y:38,class:'node-number'},done?number(value,4):'…'));
  g.addEventListener('click',()=>selectNode(n.id));g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();selectNode(n.id);}});svg.append(g);
 }
 $('edge-count').textContent=`${edges.length} von ${all.length} Transferkanten sichtbar · alle werden gerechnet`;
 $('progress').value=progress;$('step-label').textContent=`${progress}/${state.n+1}`;
}
function selectNode(id){selected=id;$('node-select').value=id;renderGraph();renderNode();}
function renderNode(){
 const incoming=result.incoming[selected]||[],node=model.nodes.find(x=>x.id===selected);
 $('node-value').textContent=precise(result.values[selected]);
 $('node-absolute').textContent=node.role==='history'?'vorgegeben':precise(incoming.reduce((s,e)=>s+Math.abs(e.contribution),0));
 $('node-edges').textContent=node.role==='history'?'Eingabewert':String(incoming.length);
}
function renderInterpretation(){
 $('row-norm').textContent=number(result.rowNorm,4);
 const chain=['contract','amplify'].includes(state.preset),contract=state.gain<1;
 if(chain){
  $('criterion-title').textContent=contract?'Beschränkte Kettenfamilie':'Unbeschränktes Wachstum mit N';
  $('criterion-body').textContent=contract?`Für jede Länge dieser Kette gilt analytisch ‖R‖∞ ≤ 1/(1−γ) = ${number(1/(1-state.gain),4)}. Die aktuelle endliche Norm beträgt ${number(result.resolventGain,4)}. Das ist eine Aussage über diese algebraische Familie.`:`Für diese Kettenfamilie wächst ‖R‖∞ ${state.gain===1?'linear':'exponentiell'} mit der Knotenzahl. Jede einzelne Matrix bleibt invertierbar. Diese Aussage betrifft keine physikalische Zeitrate und keine CSPP-Dichtefolge.`;
  $('criterion-badge').textContent=contract?'Analytische Schranke für diese Kettenfamilie':'Analytisches Gegenbeispiel zur Eigenwertdiagnose';$('criterion-badge').classList.toggle('good',contract);
 }else{
  const good=result.contractionBound!==null;
  $('criterion-title').textContent=good?'Kontraktion im endlichen System':'Dieses Kriterium bleibt ohne Freigabe';
  $('criterion-body').textContent=good?`Die berechnete Zeilennorm liegt unter 1. Die geometrische Schranke für diese Matrix beträgt ${number(result.contractionBound,4)}. Eine uniforme Aussage für wachsende Dichte oder Gebiete folgt daraus nicht.`:`Für diese Matrix ist kein ausreichender Abstand r < 1 gegeben. Der Kontraktionstest liefert deshalb keine Stabilitätsfreigabe. Sein Scheitern beweist keine Instabilität; die endliche Fehlernorm ist separat ausgewiesen.`;
  $('criterion-badge').textContent=good?'Ausreichendes Kriterium numerisch erfüllt':'Keine Entscheidung über allgemeine Stabilität';$('criterion-badge').classList.toggle('good',good);
 }
 $('scope-title').textContent=state.preset==='cspp'?(state.theta===21&&state.n===5?'Abgleich mit dem v0.25-Kontrollfall':'Variierter CSPP-Kontrollgraph'):'Ein klar begrenztes Kontrollmodell';$('scope-body').textContent=model.scope;
 if(state.preset==='cancel'){
  $('insight-title').textContent=state.mismatch===0?'Die Probe sieht null. Interne Fehler können trotzdem wachsen.':'Aufhebung ist sichtbar — ihre Empfindlichkeit auch.';
  $('insight-body').textContent=`Die gegenläufigen Beiträge reduzieren die Probe-Verstärkung um ${number(result.cancellation*100,1)} % gegenüber der Betragsmajorante. Die aktive Fehlernorm beträgt gleichzeitig ${number(result.resolventGain)}. Die Asymmetrie verändert einen Pfad, ohne Werte zu filtern.`;
 }else{
  $('insight-title').textContent='Alle Eigenwerte von K sind exakt null. Die Verstärkung kann trotzdem groß sein.';
  $('insight-body').textContent=chain?`Vergleiche γ < 1 mit γ ≥ 1. Das Spektrum bleibt unverändert; die endliche Antwortnorm und ihr Wachstum mit der Kettenlänge ändern sich grundlegend.`:'Der aktive Block ist strikt dreieckig. Entscheidend sind die aufsummierten Übertragungspfade und die Norm der Antwort — nicht allein die Eigenwerte.';
 }
}
function renderHorizon(){
 const svg=$('horizon-chart');svg.replaceChildren(el('title',{},'Knotenvergleich innerhalb derselben Kontrollfamilie'));
 const left=61,right=580,top=24,bottom=220,log=$('log-scale').checked;
 const entries=[['historyGain',colors.cyan],['pathBound',colors.amber],['resolventGain',colors.lavender]];
 const values=curve.flatMap(r=>entries.map(([k])=>r[k])).filter(v=>v>0),actualMin=Math.min(...values),actualMax=Math.max(...values);
 let lo=log?Math.floor(Math.log10(actualMin)):0,hi=log?Math.ceil(Math.log10(actualMax)):actualMax*1.08;
 if(log&&hi===lo){hi++;lo--;}if(!log&&hi===0)hi=1;
 const x=n=>left+(n-3)/21*(right-left),y=v=>bottom-((log?Math.log10(v):v)-lo)/(hi-lo)*(bottom-top);
 const count=5;for(let i=0;i<=count;i++){
  const v=lo+(hi-lo)*i/count,yy=bottom-(bottom-top)*i/count;
  svg.append(el('line',{x1:left,y1:yy,x2:right,y2:yy,stroke:'#27374b','stroke-width':.7}));
  svgText(svg,left-10,yy+3,log?`10^${number(v,1)}`:number(v,2),{'text-anchor':'end','font-size':9});
 }
 for(const n of [3,6,9,12,15,18,21,24])svgText(svg,x(n),240,String(n),{'text-anchor':'middle'});
 svgText(svg,320,263,'aktive Knoten N',{'text-anchor':'middle','font-size':9});
 svg.append(el('line',{x1:x(state.n),y1:top,x2:x(state.n),y2:bottom,stroke:'#51667e','stroke-dasharray':'3 4'}));
 for(const [key,color]of entries){let d='',continuing=false;
  for(const r of curve){if(log&&r[key]<=0){continuing=false;continue;}d+=`${continuing?'L':'M'}${x(r.n).toFixed(2)},${y(r[key]).toFixed(2)} `;continuing=true;}
  svg.append(el('path',{d,fill:'none',stroke:color,'stroke-width':1.8,...(key==='pathBound'?{'stroke-dasharray':'5 4'}:{})}));
  const current=curve.find(r=>r.n===state.n);if(current&&(!log||current[key]>0)){
   const point=el('circle',{cx:x(state.n),cy:y(current[key]),r:3.7,fill:color,stroke:'#101927','stroke-width':1.5});point.append(el('title',{},`${key}: ${precise(current[key])}`));svg.append(point);
  }
 }
}
function renderPaths(){
 const svg=$('paths-chart');svg.replaceChildren(el('title',{},'Pfadbeiträge nach Anzahl der Transferkanten'));
 const rows=result.paths,left=61,right=580,top=24,bottom=220,mid=(top+bottom)/2,max=Math.max(1e-300,...rows.map(x=>x.absolute));
 const y=v=>mid-v/max*(bottom-top)*.43,w=(right-left)/rows.length;
 for(const f of [-1,0,1]){const yy=y(f*max);svg.append(el('line',{x1:left,y1:yy,x2:right,y2:yy,stroke:f===0?'#50627b':'#27374b','stroke-width':.7}));svgText(svg,left-10,yy+3,number(f*max,3),{'text-anchor':'end','font-size':9});}
 rows.forEach((r,i)=>{
  const cx=left+(i+.5)*w,barWidth=Math.max(3,w*.53),outline=el('rect',{x:cx-barWidth/2-2,y:y(r.absolute),width:barWidth+4,height:Math.max(0,mid-y(r.absolute)),fill:'none',stroke:colors.amber,'stroke-width':.7,opacity:.75});svg.append(outline);
  const bar=el('rect',{x:cx-barWidth/2,y:Math.min(mid,y(r.signed)),width:barWidth,height:Math.abs(mid-y(r.signed)),rx:1.5,fill:r.signed>=0?colors.cyan:colors.rose,opacity:.85});bar.append(el('title',{},`${r.length} Kanten: signiert ${precise(r.signed)}, Betragssumme ${precise(r.absolute)}`));svg.append(bar);
  if(rows.length<=13||i%2===0)svgText(svg,cx,240,String(r.length),{'text-anchor':'middle','font-size':9});
 });svgText(svg,320,263,'Pfadlänge · Anzahl Transferkanten',{'text-anchor':'middle','font-size':9});
}
function advance(){if(progress>=state.n+1){stop();return;}progress++;selected=progress<=state.n?result.active[progress-1].id:'d';$('node-select').value=selected;renderGraph();renderNode();if(progress===state.n+1)stop();}
$('play').addEventListener('click',()=>{if(timer){stop();return;}if(progress>=state.n+1)progress=0;renderGraph();$('play').innerHTML='<span aria-hidden="true">Ⅱ</span> Anhalten';timer=setInterval(advance,750);});
$('step').addEventListener('click',()=>{stop();if(progress>=state.n+1)progress=0;advance();});
$('progress').addEventListener('input',e=>{stop();progress=+e.target.value;renderGraph();});
$('node-select').addEventListener('change',e=>selectNode(e.target.value));$('edge-view').addEventListener('change',renderGraph);$('log-scale').addEventListener('change',renderHorizon);
for(const b of document.querySelectorAll('[data-preset]'))b.addEventListener('click',()=>{state={preset:b.dataset.preset,...PRESETS[b.dataset.preset],eta:state.eta,pattern:state.pattern};selected='d';update();});
$('reset').addEventListener('click',()=>{state={preset:state.preset,...PRESETS[state.preset],eta:0.01,pattern:'worst'};$('edge-view').value='all';$('log-scale').checked=true;selected='d';update();});
for(const [id,key,transform]of [['node-count','n',Number],['theta','theta',Number],['coupling','gain',Number],['mismatch','mismatch',Number],['eta','eta',x=>10**Number(x)]])$(id).addEventListener('input',e=>{state[key]=transform(e.target.value);update();});
$('pattern').addEventListener('change',e=>{state.pattern=e.target.value;update();});
function download(content,type,filename){const a=document.createElement('a'),url=URL.createObjectURL(new Blob([content],{type}));a.href=url;a.download=filename;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);$('toast').textContent=`Export erstellt: ${filename}`;$('toast').classList.add('visible');setTimeout(()=>$('toast').classList.remove('visible'),3500);}
$('export-json').addEventListener('click',()=>download(JSON.stringify(exportRecord(model,result,{eta:state.eta,pattern:state.pattern}),null,2)+'\n','application/json',`cspp-stability-${state.preset}.json`));
$('export-csv').addEventListener('click',()=>{const fields=['n','historyGain','pathBound','resolventGain','rowNorm'],lines=[fields.join(','),...curve.map(r=>fields.map(k=>r[k]).join(','))];download(lines.join('\n')+'\n','text/csv','cspp-stability-knotenvergleich.csv');});
$('proof-link').href=SOURCE_URL;$('certificate-link').href=SOURCE_URL.replace('/PROOF.md','/results/CERTIFICATE_192.json');$('source-stamp').textContent=`Basis: ${BASE_COMMIT.slice(0,12)} · Float64-Diagnose · v0.1.0`;
document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
update();
