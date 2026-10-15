'use strict';
const fs=require('node:fs');
const {load,hash}=require('./kernel.cjs');
if(process.argv.length!==4)throw Error('Usage: node export.cjs CASES_JSON OUTPUT_JSON');
const bytes=fs.readFileSync(process.argv[2]),contract=JSON.parse(bytes),kernel=load();
const runs=contract.cases.map(c=>kernel.run(c));
const output={schema:'x6.numerics.current-export/1',source:{...kernel.source,contract_sha256:hash(bytes),exporter_sha256:hash(fs.readFileSync(__filename)),loader_sha256:hash(fs.readFileSync(require.resolve('./kernel.cjs')))},runs};
fs.writeFileSync(process.argv[3],JSON.stringify(output,(_,v)=>{if(typeof v==='number'&&!Number.isFinite(v))throw Error('Nonfinite export');return v;},2)+'\n');
console.log(JSON.stringify({cases:runs.length,source:output.source}));
