/* Actual generated HTML scripts executed with a minimal test DOM.
 * Covers UI calculations/events/import/export. Does NOT test browser rendering. */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const {webcrypto}=require('node:crypto');
const html=fs.readFileSync(path.join(__dirname,'../rax_cqg_lab.html'),'utf8');
class Element{
  constructor(tag,id='',attrs=''){
    this.tagName=tag;this.id=id;this.value=(attrs.match(/\bvalue="([^"]*)"/)||[])[1]||'';
    this.hidden=/\bhidden\b/.test(attrs);this.disabled=/\bdisabled\b/.test(attrs);
    this.textContent='';this.innerHTML='';this.className='';this.children=[];this.listeners={};this.files=[];
  }
  addEventListener(name,fn){(this.listeners[name]??=[]).push(fn);}
  appendChild(child){this.children.push(child);if(this.tagName==='select'&&this.children.length===1)this.value=String(child.value);return child;}
  replaceChildren(...children){this.children=children;if(this.tagName==='select')this.value=children[0]?.value??'';}
  async dispatch(name){for(const fn of this.listeners[name]||[])await fn({target:this,preventDefault(){}});}
  click(){this.clicked=true;}
}
const nodes={};
for(const m of html.matchAll(/<([a-z][a-z0-9-]*)\b([^>]*\bid="([^"]+)"[^>]*)>/gi))nodes[m[3]]=new Element(m[1],m[3],m[2]);
for(const m of html.matchAll(/<select\b[^>]*id="([^"]+)"[^>]*>([\s\S]*?)<\/select>/gi)){
  const v=m[2].match(/<option\s+value="([^"]+)"/);if(v)nodes[m[1]].value=v[1];
}
const blobs=[];
const context=vm.createContext({document:{getElementById:id=>nodes[id]||null,createElement:tag=>new Element(tag)},
  crypto:webcrypto,TextEncoder,Blob,URL:{createObjectURL:b=>{blobs.push(b);return 'blob:test';},revokeObjectURL(){}},
  setTimeout,clearTimeout,console});
const scripts=[...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)];
assert(scripts.every(s=>!/\bsrc=/.test(s[1])),'No external scripts are allowed');
scripts.forEach(s=>vm.runInContext(s[2],context,{timeout:10000}));
const checks=[];
async function eventually(fn){for(let i=0;i<200;i++){if(fn())return;await new Promise(r=>setTimeout(r,5));}throw new Error('UI did not settle');}
function check(name,condition){assert(condition,name);checks.push({name,passed:true});}
async function upload(data){nodes['import-file'].files=[{size:JSON.stringify(data).length,text:async()=>JSON.stringify(data)}];await nodes['import-file'].dispatch('change');}
async function main(){
  await eventually(()=>!nodes['export-button'].disabled);
  check('default calculation completes',!nodes.results.hidden&&nodes.error.hidden);
  check('runtime selftests displayed',nodes['selftest-status'].textContent.includes('7/7'));
  check('actual spectrum plotted',nodes['spectrum-chart'].innerHTML.includes('<rect'));
  check('matrix hash available',/SHA-256: [0-9a-f]{64}/.test(nodes['matrix-hash'].textContent));
  nodes.model.value='chain';await nodes.model.dispatch('change');nodes.size.value='8';await nodes['experiment-form'].dispatch('submit');
  check('controls recompute actual values',nodes['m-relations'].textContent==='28 / 7'&&String(nodes['m-bdg'].textContent)==='7');
  nodes.size.value='4oops';await nodes['experiment-form'].dispatch('submit');
  check('invalid size clears stale results',!nodes.error.hidden&&nodes.results.hidden&&nodes['export-button'].disabled);
  nodes.size.value='8';await nodes['experiment-form'].dispatch('submit');
  const record=JSON.parse(vm.runInContext("JSON.stringify(RAXCore.experiment('percolation',16,123,.3))",context));
  record.metrics.bdg4_bracket=99999;await upload(record);
  check('import recomputes and ignores stored metrics',nodes.error.hidden&&String(nodes['m-bdg'].textContent)!=='99999');
  await nodes['export-button'].dispatch('click');const exported=JSON.parse(await blobs.at(-1).text());
  check('export contains recomputed matrix and diagnostics',exported.relation_rows.length===16&&exported.relation_sha256.length===64&&exported.metrics.bdg4_bracket!==99999);
  const tampered=structuredClone(exported);tampered.relation_sha256='0'.repeat(64);await upload(tampered);
  check('bad hash rejected',!nodes.error.hidden&&nodes.results.hidden);
  await upload([{size:10,bdg_action:7.6}]);check('legacy unverified schema rejected',!nodes.error.hidden);
  const chain=JSON.parse(vm.runInContext("JSON.stringify(RAXCore.experiment('chain',8,42,.25))",context));
  await upload({schema:'RAX-CQG-SWEEP-0.2',runs:[record,chain]});
  check('sweep import populates selector',!nodes['dataset-picker'].hidden&&nodes['dataset-run'].children.length===2);
  nodes['dataset-run'].value='1';await nodes['dataset-run'].dispatch('change');
  check('sweep selection recomputes chosen graph',nodes['m-relations'].textContent==='28 / 7');
  nodes.retention.value='0';await nodes['thin-button'].dispatch('click');
  check('zero retention produces empty suborders',nodes['thinning-table'].children[1].children[1].textContent==='0');
  nodes.retention.value='1.2';await nodes['thin-button'].dispatch('click');
  check('invalid thinning clears stale diagram',!nodes.error.hidden&&nodes['thinning-chart'].innerHTML==='');
  nodes.retention.value='.75';await nodes['thin-button'].dispatch('click');
  check('thinning recovers after correction',nodes.error.hidden&&nodes['thinning-chart'].innerHTML.includes('<polyline'));
  check('independent clock chart rendered in DOM',nodes['clock-chart'].innerHTML.includes('<polyline'));
  console.log(JSON.stringify({method:'Node VM with minimal test DOM; actual generated HTML scripts',visual_browser_qa:'NOT_RUN',checks,
    count:checks.length,export_fixture:exported},null,2));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
