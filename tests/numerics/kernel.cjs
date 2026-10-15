'use strict';
// Extract real application code. No replacement numerical implementation is used.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),crypto=require('node:crypto'),cp=require('node:child_process');
const ROOT=path.resolve(__dirname,'../..');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
function load(sourcePath=path.join(ROOT,'app/index.html')){
 const app=fs.readFileSync(sourcePath),tag=app.toString('utf8').match(/<iframe\b[^>]*\bid="spectrumFrame"[^>]*>/);
 if(!tag)throw Error('Missing spectrumFrame');
 const attr=tag[0].match(/\bsrcdoc="([^"]*)"/),named={amp:'&',lt:'<',gt:'>',quot:'"',apos:"'"};
 const src=attr[1].replace(/&(#x[\da-f]+|#\d+|amp|lt|gt|quot|apos);/gi,(_,k)=>k[0]==='#'?String.fromCodePoint(k[1].toLowerCase()==='x'?parseInt(k.slice(2),16):parseInt(k.slice(1),10)):named[k.toLowerCase()]);
 const start=src.indexOf('function parse(s)'),end=src.indexOf('function show(o)',start);
 if(start<0||end<=start)throw Error('Extraction boundaries changed');
 const original=src.slice(start,end),needle='return {value:lambda,residual:res}';
 if(original.split(needle).length!==2)throw Error('Ambiguous vector observation point');
 const observed=original.replace(needle,'return {value:lambda,residual:res,vector:v}');
 function context(code){const c=vm.createContext({});vm.runInContext(code+'\nglobalThis.api={parse,analyze,jacobi};',c,{timeout:1000});return c;}
 const a=context(original),b=context(observed);
 function execute(c,input){c.input=input;return JSON.parse(JSON.stringify(vm.runInContext('({graph:api.parse(input),analysis:api.analyze(input)})',c,{timeout:60000})));}
 function run(test){
  const x=execute(a,test.input),y=execute(b,test.input),clean=JSON.parse(JSON.stringify(y)),ref=JSON.parse(JSON.stringify(x));
  clean.analysis.numerical.eig.forEach(e=>delete e.vector);delete clean.analysis.timestamp;delete ref.analysis.timestamp;
  if(JSON.stringify(clean)!==JSON.stringify(ref))throw Error(test.id+': observation changed public output');
  return {id:test.id,input:test.input,nodes:x.graph.nodes,A:x.graph.A,L:x.graph.L,analysis:x.analysis,eigenpairs:y.analysis.numerical.eig,observation_parity:true};
 }
 const commit=cp.execFileSync('git',['rev-parse','HEAD'],{cwd:ROOT,encoding:'utf8'}).trim();
 const committed=cp.execFileSync('git',['show',commit+':app/index.html'],{cwd:ROOT});
 return {run,original,observed,source:{commit,app_sha256:hash(app),kernel_sha256:hash(original),observed_kernel_sha256:hash(observed),source_dirty:!app.equals(committed),source_path:'app/index.html',node:process.version,execution:'Node.js VM; original public output plus observation-only vector return; no DOM'}};
}
module.exports={load,hash,ROOT};
