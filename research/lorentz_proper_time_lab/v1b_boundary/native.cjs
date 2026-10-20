/* Fixed, unblinded regression; does not decide the statistical qualification. */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),zlib=require('node:zlib');
const {root,protocol:q,sha,provenance,flagsHex}=require('./common.cjs');
const P=require('../core.js'),old=require('../v1b_port_correction/source/core.js');
const out=path.resolve(process.argv[2]||'/tmp/x6-v1b-boundary');fs.mkdirSync(out,{recursive:true});
const oldRaw=JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(__dirname,'../v1b_port_correction/results/native_reference.json.gz'))));
const checks=[],boundary=[],clouds=[],streams=[];
const support=p=>Math.abs(p[0])+Math.hypot(...p.slice(1));
const ensure=(name,f)=>{f();checks.push(name);};
ensure('PRNG streams unchanged: 40000 exact binary fractions',()=>{
  for(const seed of q.seeds){const r=P.rng(seed),values=Array.from({length:q.prng_values_per_seed},r);
    assert.deepEqual(values,oldRaw.streams.find(s=>s.seed===seed).uniforms);streams.push({seed,uint32:values.map(x=>x*2**32)});}
});
for(const d of q.dimensions){
  const args={m:64,d,theta:.5,seed:q.boundary_seed},previous=old.cloud(args),current=P.cloud(args);
  assert.equal(support(previous.points[0]),.5,'Historical negative control must fail strict support');
  assert.equal(current.sampling.rejected.zeroTemporalUniform,1);
  assert.ok(current.points.every(p=>support(p)<.5));
  assert.deepEqual(current,P.cloud(args));
  boundary.push({d,seed:q.boundary_seed,old_point:previous.points[0],old_support:support(previous.points[0]),
    result:current});
}
checks.push('Known zero-input seed repaired in d=2,3,4; old sampler rejected as negative control');
// An accepted fallback stream is deterministic and independent of tested output.
function injected(prefix,d){let i=0;const fallback=P.rng(1);return P.samplePoint(()=>i<prefix.length?prefix[i++]:fallback(),d);}
const injectedCases=[];
for(const d of q.dimensions){
  for(const [name,first] of [['zero',0],['smallest_PRNG',2**-32],['largest_PRNG',1-2**-32],['subnormal_time',Number.MIN_VALUE]]){
    const c=injected([first],d);assert.ok(support(c.point)<.5);
    if(name==='zero')assert.equal(c.rejected.zeroTemporalUniform,1);
    if(name==='subnormal_time')assert.ok(c.rejected.outsideSupport>=1);
    injectedCases.push({d,name,...c});
  }
  // Force a rounded outer boundary: A=1/8, near-unit radial draw and ordinary direction.
  const prefix=[(.25)**d,.75,...Array.from({length:d-1},()=>[.5,0]).flat(),1-Number.EPSILON/2];
  const c=injected(prefix,d);assert.ok(support(c.point)<.5);
  assert.ok(c.rejected.outsideSupport>=1,'Rounded boundary must be rejected');
  injectedCases.push({d,name:'rounded_outer_boundary',...c});
}
ensure('Bounded failure and invalid source values',()=>{
  let calls=0;assert.throws(()=>P.samplePoint(()=>{calls++;return 0;},4),/128/);assert.equal(calls,128);
  for(const u of [1,-Number.MIN_VALUE,NaN,Infinity])assert.throws(()=>P.samplePoint(()=>u,4),/außerhalb/);
});
// Exercise the exact membership predicate, including neighbouring representable points.
ensure('Inner predicate strictness at exactly representable boundaries',()=>{
  for(const theta of [.25,.5,.75]){
    const edge=theta/2;
    for(const d of q.dimensions){
      const point=x=>[0,x,...Array(d-2).fill(0)];
      assert.equal(P.insideDiamond(point(edge),theta),false);
      assert.equal(P.insideDiamond(point(edge-Number.EPSILON*edge),theta),true);
      assert.equal(P.insideDiamond(point(edge+Number.EPSILON*edge),theta),false);
    }
  }
});
for(const d of q.dimensions)for(const seed of q.seeds){
  const args={m:q.m,d,theta:.5,seed,T:q.T},c=P.cloud(args),legacy=oldRaw.clouds.find(r=>r.parameters.d===d&&r.parameters.seed===seed);
  assert.deepEqual(c.points,legacy.points,'Ordinary points must remain unchanged');
  assert.deepEqual(c.inside,legacy.inside);assert.equal(c.sampling.attempts,q.m);
  assert.ok(c.points.every(p=>support(p)<.5));assert.deepEqual(c,P.cloud(args));
  const thetaResults=[];
  for(const percent of q.theta_percent){
    const theta=percent/100,actual=P.cloud({...args,theta});
    assert.deepEqual(actual.points,c.points,'theta must not alter point generation');
    const flags=c.points.map(p=>support(p)<theta/2),k=flags.filter(Boolean).length;
    assert.deepEqual(actual.inside,flags);assert.equal(actual.k,k);
    thetaResults.push({theta,k,flags_hex:flagsHex(flags),estimate:actual.estimate,lower:actual.lower,upper:actual.upper});
  }
  clouds.push({parameters:args,...c,theta_results:thetaResults});
}
checks.push('196608 fixed-matrix points and flags unchanged; support and seed replay pass');
checks.push('192 dimension/seed/theta cases; exact flags/counts and theta-independent points');
const raw={schema:q.schema,provenance:provenance(),streams,clouds,boundary,injected_cases:injectedCases};
const bytes=zlib.gzipSync(Buffer.from(JSON.stringify(raw)),{level:9});
fs.writeFileSync(path.join(out,'native_raw.json.gz'),bytes);
const report={schema:q.schema,status:'PASS_NATIVE_ENGINEERING',provenance:raw.provenance,checks,
  unique_matrix_points:clouds.reduce((n,c)=>n+c.points.length,0),theta_cases:clouds.reduce((n,c)=>n+c.theta_results.length,0),
  boundary_dimensions:boundary.length,injected_cases:injectedCases.length,raw_sha256:sha(bytes),
  historical_points_unchanged:true,statistical_gate:'NOT_EVALUATED_HERE'};
fs.writeFileSync(path.join(out,'native_report.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
