/* RAX-CQG 0.2.0: finite order diagnostics, no physics-validation claim.
 * PCG-XSH-RR algorithm: M. E. O'Neill; see THIRD_PARTY_NOTICES.txt. */
(function(root){
'use strict';
const VERSION='0.2.0', MAX_SIZE=96;
const MODELS=['chain','antichain','percolation','three_layer','minkowski_2d','minkowski_4d'];
function integer(x,name,lo=0,hi=MAX_SIZE){
  if(!Number.isSafeInteger(x)||x<lo||x>hi)throw new Error(`${name}: ganze Zahl in [${lo}, ${hi}] erforderlich`);
  return x;
}
function real(x,name,lo=-Infinity,hi=Infinity){
  if(typeof x!=='number'||!Number.isFinite(x)||x<lo||x>hi)throw new Error(`${name}: ungültiger Wert`);
  return x;
}
class PCG32{
  constructor(seed=42,stream=54){
    integer(seed,'Seed',0,4294967295);integer(stream,'Stream',0,4294967295);
    this.state=0n;this.inc=(BigInt(stream)<<1n)|1n;this.next();
    this.state=BigInt.asUintN(64,this.state+BigInt(seed));this.next();
  }
  next(){
    const old=this.state;this.state=BigInt.asUintN(64,old*6364136223846793005n+this.inc);
    const word=Number(BigInt.asUintN(32,((old>>18n)^old)>>27n)),rot=Number(old>>59n);
    return ((word>>>rot)|(word<<((-rot)&31)))>>>0;
  }
  uniform(){return (this.next()+.5)/4294967296;}
}
function zeros(n){return Array.from({length:n},()=>Array(n).fill(0));}
function copy(r){return r.map(row=>row.slice());}
function closure(matrix){
  const r=copy(matrix),n=r.length;
  for(let k=0;k<n;k++)for(let i=0;i<n;i++)if(r[i][k])for(let j=0;j<n;j++)if(r[k][j])r[i][j]=1;
  return r;
}
function validate(r){
  if(!Array.isArray(r))throw new Error('Matrix fehlt');
  const n=integer(r.length,'N');
  if(r.some(row=>!Array.isArray(row)||row.length!==n||row.some(v=>v!==0&&v!==1)))throw new Error('Binäre quadratische Matrix erforderlich');
  const c=closure(r);
  for(let i=0;i<n;i++)for(let j=0;j<n;j++){
    if(i===j&&c[i][j])throw new Error('Zyklus oder reflexive Relation');
    if(c[i][j]!==r[i][j])throw new Error('Matrix ist nicht transitiv');
  }
  return r;
}
function addRelation(matrix,i,j){
  validate(matrix);const n=matrix.length;
  integer(i,'i',0,n-1);integer(j,'j',0,n-1);
  if(i===j||matrix[j][i])throw new Error('Einfügung würde einen Zyklus erzeugen');
  const r=copy(matrix);
  for(let a=0;a<n;a++)if(a===i||matrix[a][i])for(let b=0;b<n;b++)if(b===j||matrix[j][b])r[a][b]=1;
  return r;
}
function generate(model='percolation',n=30,seed=42,p=.25){
  integer(n,'N');integer(seed,'Seed',0,4294967295);real(p,'p',0,1);
  if(!MODELS.includes(model))throw new Error('Unbekanntes Ensemble');
  let r=zeros(n);const rng=new PCG32(seed);
  const generator={model,size:n,seed,rng:'PCG-XSH-RR-64-32',stream:54,version:VERSION,
    uniform:'(uint32+0.5)/2**32',p:['percolation','three_layer'].includes(model)?p:null};
  if(model==='chain'){
    for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)r[i][j]=1;
  }else if(model==='percolation'){
    for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)r[i][j]=rng.uniform()<p?1:0;
    r=closure(r);
  }else if(model==='three_layer'){
    if(n<4)throw new Error('Dreischicht-Ensemble benötigt N≥4');
    const a=Math.floor(n/4),b=Math.floor(n/2),bounds=[0,a,a+b,n];
    for(let layer=0;layer<2;layer++)for(let i=bounds[layer];i<bounds[layer+1];i++)
      for(let j=bounds[layer+1];j<bounds[layer+2];j++)r[i][j]=rng.uniform()<p?1:0;
    r=closure(r);generator.layer_sizes=[a,b,n-a-b];
    generator.ensemble_note='Independent adjacent-layer edges; fixed labels; not a uniform sample of all KR orders';
  }else if(model.startsWith('minkowski_')){
    const dim=model==='minkowski_2d'?2:4,pts=[];
    for(let i=0;i<n;i++){
      if(dim===2){const u=rng.uniform(),v=rng.uniform();pts.push([(u+v)/2-.5,(v-u)/2]);}
      else{
        const u=rng.uniform(),t=u<.5?-.5+.5*(2*u)**.25:.5-.5*(2*(1-u))**.25;
        const radius=(.5-Math.abs(t))*rng.uniform()**(1/3),z=2*rng.uniform()-1,angle=2*Math.PI*rng.uniform();
        const transverse=Math.sqrt(Math.max(0,1-z*z));
        pts.push([t,radius*transverse*Math.cos(angle),radius*transverse*Math.sin(angle),radius*z]);
      }
    }
    for(let i=0;i<n;i++)for(let j=0;j<n;j++){
      const dt=pts[j][0]-pts[i][0];let ds2=0;
      for(let k=1;k<dim;k++)ds2+=(pts[j][k]-pts[i][k])**2;
      r[i][j]=dt>0&&dt*dt>=ds2?1:0;
    }
    Object.assign(generator,{dimension:dim,coordinates:pts,diamond_endpoints:[[-.5,...Array(dim-1).fill(0)],[.5,...Array(dim-1).fill(0)]],
      volume:dim===2?.5:Math.PI/24,sampling:'Uniform spacetime volume conditioned on fixed N; N is not Poisson sampled',
      causal_comparison:'float64 dt>0 and dt^2>=sum(dx^2); no tolerance or closure repair'});
  }
  validate(r);return {R:r,generator};
}
function eigenvalues(matrix){
  const n=matrix.length;if(!n)return [];
  const a=copy(matrix);let norm=0;
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)norm+=a[i][j]**2;
  const threshold=1e-12*Math.max(1,Math.sqrt(norm));
  for(let sweep=0;sweep<60;sweep++){
    for(let p=0;p<n;p++)for(let q=p+1;q<n;q++){
      const apq=a[p][q];if(Math.abs(apq)<threshold/(Math.max(1,n)*10))continue;
      const tau=(a[q][q]-a[p][p])/(2*apq);
      const t=(tau>=0?1:-1)/(Math.abs(tau)+Math.hypot(1,tau));
      const c=1/Math.sqrt(1+t*t),s=t*c;
      a[p][p]-=t*apq;a[q][q]+=t*apq;a[p][q]=a[q][p]=0;
      for(let k=0;k<n;k++)if(k!==p&&k!==q){
        const kp=a[k][p],kq=a[k][q];
        a[k][p]=a[p][k]=c*kp-s*kq;a[k][q]=a[q][k]=s*kp+c*kq;
      }
    }
    let off=0;for(let p=0;p<n;p++)for(let q=p+1;q<n;q++)off+=2*a[p][q]**2;
    if(Math.sqrt(off)<=threshold)return a.map((row,i)=>row[i]).sort((x,y)=>x-y);
  }
  throw new Error('Jacobi-Eigensolver hat die Toleranz nicht erreicht');
}
function diagnose(r){
  validate(r);const n=r.length,h=zeros(n),hist=[],pred=Array(n).fill(0);let m=0,triangles=0;
  for(let i=0;i<n;i++)for(let j=0;j<n;j++){
    h[i][j]=r[i][j]+r[j][i];m+=r[i][j];pred[j]+=r[i][j];
    if(r[i][j]){let kcount=0;for(let k=0;k<n;k++)kcount+=r[i][k]*r[k][j];hist[kcount]=(hist[kcount]||0)+1;}
  }
  for(let k=0;k<hist.length;k++)hist[k]=hist[k]||0;
  const order=Array.from({length:n},(_,i)=>i).sort((a,b)=>pred[a]-pred[b]||a-b),depth=Array(n).fill(1);
  for(const j of order)for(let i=0;i<n;i++)if(r[i][j])depth[j]=Math.max(depth[j],depth[i]+1);
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)for(let k=j+1;k<n;k++)triangles+=h[i][j]*h[j][k]*h[k][i];
  const lap=h.map((row,i)=>row.map((v,j)=>i===j?row.reduce((a,b)=>a+b,0):-v));
  const eig=eigenvalues(h),leig=eigenvalues(lap);
  const entropy=m?eig.reduce((a,e)=>{const p=e*e/(2*m);return a-(p>0?p*Math.log(p):0);},0):null;
  return {size:n,relations:m,links:hist[0]||0,ordering_fraction:n>1?2*m/(n*(n-1)):0,
    height:n?Math.max(...depth):0,interval_counts:hist,
    bdg4_bracket:n+[-1,9,-16,8].reduce((s,c,k)=>s+c*(hist[k]||0),0),
    adjacency_spectrum:eig,laplacian_spectrum:leig,spectral_radius:n?Math.max(...eig.map(Math.abs)):0,
    adjacency_spectral_width:n?eig[n-1]-eig[0]:0,algebraic_connectivity:n>1?Math.max(0,leig[1]):null,
    h2_spectral_entropy:entropy,adjacency_spectral_std:n?Math.sqrt(2*m/n):0,
    triangles,triangles_per_vertex:n?triangles/n:0};
}
function rows(r){return r.map(row=>row.join(''));}
function experiment(model='percolation',n=30,seed=42,p=.25){
  const x=generate(model,n,seed,p);
  return {schema:'RAX-CQG-EXPERIMENT-0.2',software_version:VERSION,evidence_class:'FINITE_ORDER_BENCHMARK',
    generator:x.generator,relation_rows:rows(x.R),relation_sha256:null,metrics:diagnose(x.R)};
}
function loadExperiment(record){
  if(!record||record.schema!=='RAX-CQG-EXPERIMENT-0.2')throw new Error('Nicht unterstütztes Experimentformat');
  const rs=record.relation_rows;
  if(!Array.isArray(rs))throw new Error('Relationsmatrix fehlt');
  const n=integer(rs.length,'Importgröße');
  if(rs.some(row=>typeof row!=='string'||row.length!==n||/[^01]/.test(row)))throw new Error('Ungültige Matrixzeilen');
  const r=rs.map(row=>Array.from(row,Number));validate(r);return r;
}
function thinning(r,retention=.75,steps=4,seed=104729){
  validate(r);real(retention,'Retention',0,1);integer(steps,'Schritte',0,20);const rng=new PCG32(seed);
  let ids=r.map((_,i)=>i);const path=[];
  for(let step=0;step<=steps;step++){
    const sub=ids.map(i=>ids.map(j=>r[i][j]));
    path.push({step,original_indices:ids.slice(),relation_rows:rows(sub),metrics:diagnose(sub)});
    if(step<steps)ids=ids.filter(()=>rng.uniform()<retention);
  }
  return {method:'independent Bernoulli retention, induced suborders',retention,seed,steps,
    interpretation:'Thinning only; no fitted RG flow or continuum claim',path};
}
function clockReference(samples=33){
  integer(samples,'Uhrpunkte',3,1000);
  // Direct conditioning of (|01>+|10>)/sqrt(2) on e^(-i H_T tau)|+>.
  const data=[];
  for(let i=0;i<samples;i++){
    const tau=2*Math.PI*i/(samples-1),cos=Math.cos(tau/2),sin=Math.sin(tau/2);
    const raw=[[cos/2,sin/2],[cos/2,-sin/2]],weight=raw.reduce((s,z)=>s+z[0]**2+z[1]**2,0);
    const state=raw.map(z=>z.map(x=>x/Math.sqrt(weight)));
    const realSum=(state[0][0]+state[1][0])/Math.sqrt(2),imagSum=(state[0][1]+state[1][1])/Math.sqrt(2);
    data.push({tau,overlap_weight:weight,clock_probability_density:1/(2*Math.PI),p_plus_x:realSum**2+imagSum**2});
  }
  return {model:'assumed_two_qubit_periodic_clock',hbar:1,omega:1,period:2*Math.PI,samples:data};
}
function selfTest(){
  const checks=[];
  const add=(name,ok)=>checks.push({name,passed:Boolean(ok)}),near=(x,y)=>Math.abs(x-y)<1e-8;
  const rng=new PCG32(42),reference=[0xa15c02b7,0x7b47f409,0xba1d3330,0x83d2f293,0xbfa4784b,0xcbed606e];
  add('PCG32-Referenzvektor',reference.every(v=>rng.next()===v));
  add('Antikette B₄=4',diagnose(zeros(4)).bdg4_bracket===4);
  let star=zeros(4);for(let i=1;i<4;i++)star=addRelation(star,0,i);
  add('Stern B₄=1',diagnose(star).bdg4_bracket===1);
  let c=addRelation(addRelation(zeros(4),0,1),1,2),d=diagnose(c);
  add('Kette + isolierter Punkt',d.bdg4_bracket===11&&near(d.algebraic_connectivity,0));
  const chain=diagnose(generate('chain',8).R).adjacency_spectrum;
  add('Exaktes Kettenspektrum',chain.every((v,i)=>near(v,i===7?7:-1)));
  const start=addRelation(zeros(4),0,1),ab=addRelation(addRelation(start,1,2),2,3),ba=addRelation(addRelation(start,2,3),1,2);
  add('Einfügereihenfolge',JSON.stringify(ab)===JSON.stringify(ba));
  const clock=clockReference(5);add('Periodische Referenzuhr',near(clock.samples[0].p_plus_x,1)&&near(clock.samples[2].p_plus_x,0));
  return {checks,passed:checks.filter(x=>x.passed).length,total:checks.length,scope:'Finite mathematical reference cases only'};
}
const api={VERSION,MAX_SIZE,MODELS,PCG32,closure,validate,addRelation,generate,diagnose,experiment,loadExperiment,thinning,clockReference,selfTest};
if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.RAXCore=api;
})(typeof globalThis!=='undefined'?globalThis:this);
