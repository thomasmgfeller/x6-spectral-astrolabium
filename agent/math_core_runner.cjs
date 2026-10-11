'use strict';
// Only the pinned application's numerical functions are injected by the Python
// extractor. No browser/DOM execution or external service is claimed here.
const fs = require('node:fs');
const vm = require('node:vm');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
if (!Array.isArray(input.cases) || input.cases.length > 600) throw Error('case budget');
const box = {cases: input.cases};
vm.createContext(box, {codeGeneration: {strings: false, wasm: false}});
const code = `const T=2*Math.PI; ${input.functions}\n` +
  (input.action === 'filter'
    ? `result=cases.map(c=>filter(c.values,c.angle,c.width,c.mode));`
    : input.action === 'mapping'
      ? `result=cases.map(c=>makeGraph(c.values,c.sigma,c.digits));`
      : (()=>{throw Error('unsupported action')})());
new vm.Script(code).runInContext(box, {timeout: 10000});
process.stdout.write(JSON.stringify(box.result));
