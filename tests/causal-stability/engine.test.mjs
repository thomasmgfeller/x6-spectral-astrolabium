import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {makeModel,analyze,assemble,normInf,exportRecord,horizon} from '../../app/causal-stability/engine.mjs';
const near=(a,b,tol=2e-12)=>assert.ok(Math.abs(a-b)<=tol*Math.max(1,Math.abs(a),Math.abs(b)),`${a} != ${b}`);
// Independent general Gauss-Jordan inverse; no triangular recursion reused.
function inverse(a) {
  const n=a.length,m=a.map((r,i)=>[...r,...Array.from({length:n},(_,j)=>+(i===j))]);
  for(let j=0;j<n;j++) {
    let k=j;for(let i=j+1;i<n;i++)if(Math.abs(m[i][j])>Math.abs(m[k][j]))k=i;
    assert.ok(Math.abs(m[k][j])>1e-14);[m[k],m[j]]=[m[j],m[k]];
    const z=m[j][j];m[j]=m[j].map(v=>v/z);
    for(let i=0;i<n;i++)if(i!==j){const t=m[i][j];m[i]=m[i].map((v,k)=>v-t*m[j][k]);}
  }
  return m.map(r=>r.slice(n));
}
test('original Git blob and published 192-bit CSPP finite control',()=>{
  const raw=readFileSync(new URL('../../research/cspp/scalar_candidate_v0_25/cspp_v025/results/CERTIFICATE_192.json',import.meta.url));
  assert.equal(createHash('sha1').update(`blob ${raw.length}\0`).update(raw).digest('hex'),'7ca4c23463d59e38d690690c4856c9746b672474');
  const ref=JSON.parse(raw).finite_stability,r=analyze(makeModel({preset:'cspp'}));
  near(r.historyGain,ref.actual_history_operator_norm.display_mid,2e-14);
  near(r.pathBound,ref.history_gain_enclosure.display_mid,2e-14);
  near(makeModel().parameters.D,ref.D.display_mid,2e-14);
});
test('finite solves agree with independent pivoted dense inversion',()=>{
  for(const preset of ['cspp','contract','amplify','cancel'])for(const n of [3,5,9]) {
    const model=makeModel({preset,n}),r=analyze(model),dense=inverse(r.K.map((row,i)=>row.map((k,j)=>+(i===j)-k)));
    near(normInf(dense),r.resolventGain);
    dense.forEach((row,i)=>row.forEach((v,j)=>near(v,r.R[i][j])));
    for(let h=0;h<r.history.length;h++) {
      const out=r.qH[h]+r.qA.reduce((s,q,i)=>s+q*dense[i].reduce((t,x,j)=>t+x*r.H[j][h],0),0);
      near(out,r.transfer[h]);
    }
  }
});
test('chain exact formulas, unbounded family and zero spectra coexist',()=>{
  for(const gain of [0,0.3,0.8,1,1.18,1.6])for(const n of [2,5,12,24]) {
    const r=analyze(makeModel({preset:'amplify',gain,n}));
    near(r.historyGain,gain**(n+1));
    near(r.resolventGain,Array.from({length:n},(_,k)=>gain**k).reduce((s,x)=>s+x,0));
    assert.ok(r.K.every((row,i)=>row.slice(i).every(x=>x===0)));
    if(gain<1)assert.ok(r.resolventGain<=1/(1-gain)+1e-12);
  }
});
test('all-path enumeration matches sign and absolute majorant',()=>{
  for(const preset of ['cspp','cancel','amplify']) {
    const model=makeModel({preset,n:5}),r=analyze(model,{eta:0.1,pattern:'alternating'});
    let signed=0,absolute=0;const byLength=new Map();
    function walk(id,value,depth) {
      if(id==='d'){signed+=value;absolute+=Math.abs(value);byLength.set(depth,(byLength.get(depth)||0)+value);return;}
      for(const e of model.edges.filter(e=>e.from===id))walk(e.to,value*e.weight,depth+1);
    }
    r.history.forEach((h,i)=>walk(h.id,r.input[i],0));
    near(signed,r.detectorResponse);near(absolute,0.1*r.pathBound);
    for(const p of r.paths)near(p.signed,byLength.get(p.length)||0);
  }
});
test('exact output cancellation does not remove internal error amplification',()=>{
  const r=analyze(makeModel({preset:'cancel',n:12,gain:1.4,mismatch:0}));
  near(r.historyGain,0);assert.ok(r.pathBound>20);assert.ok(r.resolventGain>20);
  assert.equal(r.cancellation,1);
});
test('worst-case input attains norm; response scales linearly',()=>{
  for(const theta of [-8,0,12,21,30]) {
    const model=makeModel({preset:'cspp',theta,n:10}),r=analyze(model,{eta:0.02}),r2=analyze(model,{eta:0.04});
    near(r.detectorResponse,0.02*r.historyGain);near(r2.detectorResponse,2*r.detectorResponse);
    assert.ok(r.historyGain<=r.pathBound+1e-11);near(analyze(model,{eta:0}).detectorResponse,0);
  }
});
test('permutation of storage and node identifiers does not alter observables',()=>{
  const model=makeModel({preset:'cspp',n:8}),original=analyze(model);
  const names=Object.fromEntries(model.nodes.map((x,i)=>[x.id,`renamed-${i*7}`]));
  const changed={...model,nodes:model.nodes.slice().reverse().map(x=>({...x,id:names[x.id]})),edges:model.edges.slice().reverse().map(e=>({...e,from:names[e.from],to:names[e.to]}))};
  const r=analyze(changed);near(r.historyGain,original.historyGain);near(r.pathBound,original.pathBound);near(r.resolventGain,original.resolventGain);near(r.detectorResponse,original.detectorResponse);
});
test('cycles, invalid edges and nonfinite parameters fail closed',()=>{
  const m=makeModel({preset:'amplify',n:4});
  assert.throws(()=>assemble({...m,edges:[...m.edges,{from:'a3',to:'a0',weight:1}]}),/Zyklischer/);
  assert.throws(()=>assemble({...m,edges:[...m.edges,{from:'d',to:'h0',weight:1}]}));
  assert.throws(()=>makeModel({gain:NaN}));assert.throws(()=>analyze(m,{eta:NaN}));
});
test('export and horizon preserve explicit scientific scope',()=>{
  const m=makeModel(),r=analyze(m),e=exportRecord(m,r,{eta:0.01});
  assert.equal(e.METHOD,'HOLD');assert.equal(e.G1,'HOLD');assert.equal(e.new_random_clouds,0);
  assert.equal(e.density_uniform_stability,'NOT_CERTIFIED');assert.equal(horizon(m.parameters,12).length,12);
  assert.ok(!JSON.stringify(e).includes('NaN'));
});
