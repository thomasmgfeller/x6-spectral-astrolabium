'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path'),cp=require('node:child_process');
const {load,hash,ROOT}=require('./kernel.cjs');
const current=load(),checks=[];
function check(id,fn){fn();checks.push({id,status:'PASS'});}
function pair(w){return current.run({id:'pair',input:'a b '+w}).analysis.numerical;}
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'x6-numerics-regression-'));
try{
 const historical=cp.execFileSync('python3',['-c',"import sys,zipfile;sys.stdout.buffer.write(zipfile.ZipFile(sys.argv[1]).read('X6_Pruefung_3_v1/source/app/index.html'))",path.join(ROOT,'docs/numerics-v1/historical/check3-original.zip')]);
 assert.equal(hash(historical),'ff60231155f0fc869564ec0eb24c87568943cdd96e154094ae9abd9877bd7ff8');
 const oldPath=path.join(dir,'old.html');fs.writeFileSync(oldPath,historical);const old=load(oldPath);
 check('historical_failure_is_reproduced',()=>{const w=2**-50,r=old.run({id:'old',input:'a b '+w}).analysis.numerical;assert.equal(r.converged,true);assert.equal(r.sweeps,0);assert.deepEqual(r.eig.map(e=>e.value),[w,w]);});
 for(const exponent of [-996,-500,-50,-40,0,40,500,996]){
  check('scaled_pair_exponent_'+exponent,()=>{const w=2**exponent,r=pair(w);assert.equal(r.converged,true);assert.ok(r.sweeps>0);assert.ok(Math.abs(r.eig[0].value/w)<=2e-12);assert.ok(Math.abs(r.eig[1].value/w-2)<=2e-12);assert.ok(r.scaledMaxResidual<=1e-12);assert.equal(r.positiveGap.status,'RESOLVED_AT_TOLERANCE');});
 }
 // Adjacent binary64 values around the old threshold, not a rounded decimal grid.
 function adjacent(x,step){const b=new ArrayBuffer(8),v=new DataView(b);v.setFloat64(0,x);v.setBigUint64(0,v.getBigUint64(0)+BigInt(step));return v.getFloat64(0);}
 for(const offset of [-1,0,1])check('old_threshold_adjacent_'+offset,()=>{const w=adjacent(2e-14,offset),r=pair(w);assert.equal(r.converged,true);assert.ok(Math.abs(r.eig[1].value/w-2)<2e-12);assert.ok(r.sweeps>0);});
 check('zero_matrix',()=>{const r=current.run({id:'zero',input:'a\nb\nc'}).analysis.numerical;assert.equal(r.matrixScale,0);assert.equal(r.converged,true);assert.deepEqual(r.eig.map(e=>e.value),[0,0,0]);assert.equal(r.positiveGap.status,'NO_POSITIVE_MODE');});
 check('unresolved_positive_gap_is_labelled',()=>{const input='a b 1\nc d 1\nb c '+2**-50,r=current.run({id:'weak',input}).analysis;assert.equal(r.exactNullity,1);assert.equal(r.numerical.positiveGap.status,'UNRESOLVED_AT_TOLERANCE');});
 check('normalization_underflow_is_reported',()=>{const r=current.run({id:'range',input:'a b '+2**996+'\nb c '+2**-996}).analysis.numerical;assert.ok(r.normalizationUnderflowCount>0);assert.equal(r.positiveGap.status,'UNRESOLVED_AT_TOLERANCE');});
 const invalid=[['negative','a b -1'],['zero','a b 0'],['self_loop','a a 1'],['nan','a b NaN'],['infinity','a b Infinity'],['degree_overflow','a b 1e308\na c 1e308'],['eigenvalue_overflow','a b 1e308'],['too_many_vertices',Array.from({length:121},(_,i)=>'v'+i).join('\n')]];
 for(const [id,input] of invalid)check('reject_'+id,()=>assert.throws(()=>current.run({id,input})));
 console.log(JSON.stringify({schema:'x6.numerics.regression/1',status:'PASS',checks,source:current.source,scope:'Targeted numerical regression and explicit input/range rejection; not universal robustness.'},null,2));
}finally{fs.rmSync(dir,{recursive:true,force:true});}
