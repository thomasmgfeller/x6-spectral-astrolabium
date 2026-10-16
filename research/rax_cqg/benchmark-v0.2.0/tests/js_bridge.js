// Batched Node interface to the exact browser numerical kernel.
'use strict';
const fs=require('node:fs'),core=require('../web/rax_core.js');
const request=JSON.parse(fs.readFileSync(0,'utf8'));
const results=request.cases.map(x=>{
  if(x.rows){const r=core.loadExperiment({schema:'RAX-CQG-EXPERIMENT-0.2',relation_rows:x.rows});return {relation_rows:x.rows,metrics:core.diagnose(r),thinning:core.thinning(r,.75,3,104729)};}
  const out=core.experiment(x.model,x.size,x.seed,x.p??.25);
  out.thinning=core.thinning(core.loadExperiment(out),.75,3,104729);return out;
});
console.log(JSON.stringify({results,selftest:core.selfTest(),clock:core.clockReference(33)}));
