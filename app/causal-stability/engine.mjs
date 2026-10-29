// Finite, real, retarded history problems. No random sampling, display filtering,
// spectral-stability claim or continuum-limit inference is performed here.
export const VERSION = '0.1.0';
export const BASE_COMMIT = '13d12544fba9ac8fd54549eacc4a1ec19a2d6b51';
export const SOURCE_URL = `https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/${BASE_COMMIT}/research/cspp/scalar_candidate_v0_25/cspp_v025/PROOF.md`;
const ensure = (v, msg) => { if (!v) throw new Error(msg); };
const zeros = (n, m) => Array.from({length:n}, () => Array(m).fill(0));
const sum = xs => xs.reduce((a,b) => a+b,0);
export const norm1 = xs => sum(xs.map(Math.abs));
export const normInf = rows => Math.max(0,...rows.map(norm1));
const choose = (n,k) => { if(k>n) return 0; let z=1; for(let j=1;j<=k;j++) z=z*(n-j+1)/j; return z; };
export function csppWeight(n,theta) {
  const base=[1,-9,16,-8,0], direction=[9/8,-141/8,111/2,-63,24], e=1/16;
  return sum(base.map((b,k)=>(b+theta*direction[k])*choose(n,k)*e**k*(1-e)**(n-k)));
}
export const PRESETS = {
  cspp:{name:'CSPP v0.25',tag:'Publizierter Kontrollgraph',n:5,theta:21,gain:0.55,mismatch:0.04},
  contract:{name:'Kontraktive Kette',tag:'Analytische Referenz',n:10,theta:21,gain:0.55,mismatch:0.04},
  amplify:{name:'Verstärkende Kette',tag:'Gegenbeispiel zu Eigenwerten',n:10,theta:21,gain:1.18,mismatch:0.04},
  cancel:{name:'Zwei gegenläufige Pfade',tag:'Kontrollierte Aufhebung',n:7,theta:21,gain:1.1,mismatch:0.04}
};
export function makeModel(input={}) {
  const preset=input.preset??'cspp'; ensure(PRESETS[preset], 'Unbekanntes Modell.');
  const p={...PRESETS[preset],...input,preset};
  ensure(Number.isInteger(p.n)&&p.n>=1&&p.n<=60,'1 bis 60 aktive Knoten erforderlich.');
  ensure(Number.isFinite(p.gain)&&p.gain>=0&&p.gain<=2,'Ungültige Kopplung.');
  ensure(Number.isFinite(p.theta)&&p.theta>=-8&&p.theta<=40,'Theta liegt außerhalb des Diagnosebereichs.');
  ensure(Number.isFinite(p.mismatch)&&p.mismatch>=0&&p.mismatch<=1,'Ungültige Pfad-Asymmetrie.');
  if(preset==='cancel') ensure(p.n>=3,'Aufhebungsmodell benötigt mindestens drei aktive Knoten.');
  const nh=preset==='cspp'?3:1;
  const nodes=[...Array.from({length:nh},(_,j)=>({id:`h${j}`,label:`H${j+1}`,role:'history'})),
    ...Array.from({length:p.n},(_,j)=>({id:`a${j}`,label:`A${j+1}`,role:'active'})),
    {id:'d',label:'D',role:'detector'}];
  const edges=[]; const add=(from,to,weight)=>{ if(weight!==0) edges.push({from,to,weight}); };
  let parameters={...p,nh},description,scope;
  if(preset==='cspp') {
    const a=1/Math.sqrt(2*Math.PI),diagonal=-1-3*p.theta/8,D=1-a*diagonal;
    ensure(D>0,'Lokaler KG-Nenner ist nicht positiv.');
    const beta=a/(16*D);
    for(let target=nh;target<nodes.length;target++)
      for(let source=0;source<target;source++) add(nodes[source].id,nodes[target].id,beta*csppWeight(target-source-1,p.theta));
    parameters={...parameters,a,diagonal,D,beta,rho:'3/pi',epsilon:'1/16',q:'3/(16*pi)',mass:1};
    description='Zeitartig totalgeordneter Kontrollgraph; exakte Intervallzahlen. Drei vorgeschriebene History-Werte und eine passive Probe.';
    scope='Synthetischer finiter History-Kontrollgraph; kein Poisson-Ensemble, keine kompakte KG-Detektorproduktion. Nur n=5 und theta=21 entsprechen dem publizierten v0.25-Kontrollfall.';
  } else if(preset==='cancel') {
    add('h0','a0',1);add('h0','a1',1);
    add('a0','a2',p.gain);add('a1','a2',-p.gain*(1-p.mismatch));
    for(let j=3;j<p.n;j++) add(`a${j-1}`,`a${j}`,p.gain);
    add(`a${p.n-1}`,'d',1);
    description='Ein History-Wert speist zwei Pfade. Am Zusammenfluss treffen positive und negative Beiträge aufeinander.';
    scope='Algebraisches Kontrollmodell. Asymmetrie verändert einen Operator-Koeffizienten; keine Rauschfilterung und keine behauptete Raumzeitgeometrie.';
  } else {
    add('h0','a0',p.gain);
    for(let j=1;j<p.n;j++) add(`a${j-1}`,`a${j}`,p.gain);
    add(`a${p.n-1}`,'d',p.gain);
    description='Jeder aktive Knoten übernimmt die Störung seines Vorgängers mit derselben Kopplung γ.';
    scope='Algebraische Kettenfamilie. Aussagen über beliebige Kettenlängen gelten nur für diese fest definierte Familie, nicht für CSPP oder Poisson-Kausalsets.';
  }
  return {preset,nodes,edges,parameters,description,scope};
}
export function assemble(model) {
  const {nodes,edges}=model;
  ensure(nodes.length>0&&nodes.length<=100,'Ungültige Knotenzahl.');
  const byId=new Map(nodes.map(n=>[n.id,n])); ensure(byId.size===nodes.length,'Doppelte Knotenkennung.');
  ensure(nodes.every(n=>['history','active','detector'].includes(n.role)),'Ungültige Rolle.');
  const degree=new Map(nodes.map(n=>[n.id,0])),out=new Map(nodes.map(n=>[n.id,[]]));
  const pairs=new Set();
  for(const e of edges) {
    ensure(byId.has(e.from)&&byId.has(e.to)&&e.from!==e.to&&Number.isFinite(e.weight),'Ungültige Kante.');
    ensure(byId.get(e.to).role!=='history'&&byId.get(e.from).role!=='detector','History ist vorgeschrieben; Detektor ist passiv.');
    const key=JSON.stringify([e.from,e.to]);ensure(!pairs.has(key),'Doppelte Kante.');pairs.add(key);
    degree.set(e.to,degree.get(e.to)+1);out.get(e.from).push(e.to);
  }
  const queue=nodes.filter(n=>degree.get(n.id)===0).map(n=>n.id),order=[];
  while(queue.length) {const id=queue.shift();order.push(byId.get(id));for(const target of out.get(id)){degree.set(target,degree.get(target)-1);if(degree.get(target)===0)queue.push(target);}}
  ensure(order.length===nodes.length,'Zyklischer Graph: keine retardierte Vorwärtslösung.');
  const history=order.filter(x=>x.role==='history'),active=order.filter(x=>x.role==='active'),detectors=order.filter(x=>x.role==='detector');
  ensure(history.length>0&&active.length>0&&detectors.length===1,'History, aktive Knoten und genau eine Probe erforderlich.');
  const hi=new Map(history.map((x,i)=>[x.id,i])),ai=new Map(active.map((x,i)=>[x.id,i]));
  const K=zeros(active.length,active.length),H=zeros(active.length,history.length),qA=Array(active.length).fill(0),qH=Array(history.length).fill(0);
  for(const e of edges) {
    if(ai.has(e.to)) {const i=ai.get(e.to);if(hi.has(e.from))H[i][hi.get(e.from)]=e.weight;else {const j=ai.get(e.from);ensure(j<i,'Nicht-retardierte aktive Kante.');K[i][j]=e.weight;}}
    else if(e.to===detectors[0].id) {if(hi.has(e.from))qH[hi.get(e.from)]=e.weight;else qA[ai.get(e.from)]=e.weight;}
  }
  return {history,active,detector:detectors[0],order,K,H,qA,qH};
}
export function analyze(model,{eta=0.01,pattern='worst'}={}) {
  ensure(Number.isFinite(eta)&&eta>=0&&eta<=1,'Störungsamplitude muss zwischen 0 und 1 liegen.');
  ensure(['worst','common','alternating'].includes(pattern),'Unbekanntes Störungsmuster.');
  const system=assemble(model),{K,H,qA,qH,active,history}=system,n=active.length,nh=history.length;
  const R=zeros(n,n),T=zeros(n,nh),absoluteT=zeros(n,nh);
  for(let i=0;i<n;i++) {
    R[i][i]=1;
    for(let j=0;j<i;j++) for(let k=0;k<n;k++)R[i][k]+=K[i][j]*R[j][k];
    for(let h=0;h<nh;h++) {
      T[i][h]=H[i][h];absoluteT[i][h]=Math.abs(H[i][h]);
      for(let j=0;j<i;j++){T[i][h]+=K[i][j]*T[j][h];absoluteT[i][h]+=Math.abs(K[i][j])*absoluteT[j][h];}
    }
  }
  const transfer=qH.map((v,h)=>v+sum(qA.map((q,i)=>q*T[i][h])));
  const absoluteTransfer=qH.map((v,h)=>Math.abs(v)+sum(qA.map((q,i)=>Math.abs(q)*absoluteT[i][h])));
  const historyGain=norm1(transfer),pathBound=sum(absoluteTransfer),resolventGain=normInf(R),rowNorm=normInf(K);
  const input=history.map((_,h)=>eta*(pattern==='worst'?(Math.sign(transfer[h])||1):pattern==='alternating'?(h%2?-1:1):1));
  const response=T.map(row=>sum(row.map((v,h)=>v*input[h]))),detectorResponse=sum(transfer.map((v,h)=>v*input[h]));
  const values=Object.fromEntries([...history.map((x,h)=>[x.id,input[h]]),...active.map((x,i)=>[x.id,response[i]]),[system.detector.id,detectorResponse]]);
  // Aggregate paths by their number of transfer edges. These are finite sums,
  // not time steps, probabilities or independent variance contributions.
  let term=H.map(row=>row.slice()),absTerm=H.map(row=>row.map(Math.abs));
  const paths=[{length:1,signed:sum(qH.map((v,h)=>v*input[h])),absolute:sum(qH.map((v,h)=>Math.abs(v*input[h])))}];
  for(let k=0;k<n;k++) {
    const coefficients=Array.from({length:nh},(_,h)=>sum(qA.map((q,i)=>q*term[i][h])));
    const absCoefficients=Array.from({length:nh},(_,h)=>sum(qA.map((q,i)=>Math.abs(q)*absTerm[i][h])));
    paths.push({length:k+2,signed:sum(coefficients.map((v,h)=>v*input[h])),absolute:sum(absCoefficients.map((v,h)=>v*Math.abs(input[h])))});
    const next=zeros(n,nh),absNext=zeros(n,nh);
    for(let i=0;i<n;i++)for(let j=0;j<i;j++)for(let h=0;h<nh;h++){next[i][h]+=K[i][j]*term[j][h];absNext[i][h]+=Math.abs(K[i][j])*absTerm[j][h];}
    term=next;absTerm=absNext;
  }
  const incoming=Object.fromEntries(system.order.map(node=>[node.id,model.edges.filter(e=>e.to===node.id).map(e=>({...e,input:values[e.from],contribution:e.weight*values[e.from]}))]));
  const result={...system,R,T,transfer,absoluteTransfer,historyGain,pathBound,resolventGain,rowNorm,input,response,detectorResponse,values,paths,incoming,
    cancellation:pathBound>0?Math.max(0,Math.min(1,1-historyGain/pathBound)):0,
    contractionBound:rowNorm<1-1e-12?1/(1-rowNorm):null,
    numericResidual:Math.max(...R.map((row,i)=>Math.max(...row.map((v,j)=>Math.abs(v-sum(K[i].map((k,l)=>k*R[l][j]))-(i===j?1:0))))))};
  for(const value of [historyGain,pathBound,resolventGain,rowNorm,detectorResponse,result.numericResidual])ensure(Number.isFinite(value),'Nicht-endliches Rechenergebnis.');
  return result;
}
export function horizon(params,maxN=24) {
  const start=params.preset==='cancel'?3:1;
  return Array.from({length:maxN-start+1},(_,i)=>{const n=start+i,r=analyze(makeModel({...params,n}));return {n,historyGain:r.historyGain,pathBound:r.pathBound,resolventGain:r.resolventGain,rowNorm:r.rowNorm};});
}
export function exportRecord(model,result,settings) {
  return {schema:'cspp.finite-causal-stability-lab/0.1',version:VERSION,created_at:new Date().toISOString(),
    provenance:{base_commit:BASE_COMMIT,proof:SOURCE_URL,certificate_git_blob:'7ca4c23463d59e38d690690c4856c9746b672474'},
    scope:model.scope,parameters:model.parameters,settings,model:{nodes:model.nodes,edges:model.edges},
    finite_diagnostics:{history_gain:result.historyGain,absolute_path_bound:result.pathBound,resolvent_infinity_norm:result.resolventGain,
      active_row_norm:result.rowNorm,history_input:result.input,active_response:result.response,detector_response:result.detectorResponse,
      transfer:result.transfer,path_lengths:result.paths,numeric_residual:result.numericResidual},
    arithmetic:'IEEE-754 float64; diagnostic only, no interval certificate',new_random_clouds:0,
    METHOD:'HOLD',G1:'HOLD',density_uniform_stability:'NOT_CERTIFIED',infinite_past_spectral_stability:'NOT_CERTIFIED',
    interpretation:'The exact conditional contraction theorem is documented separately. A finite sample does not establish its uniform hypotheses.'};
}
