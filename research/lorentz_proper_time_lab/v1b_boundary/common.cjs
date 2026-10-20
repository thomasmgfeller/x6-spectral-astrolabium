'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process'),os=require('node:os');
const root=path.resolve(__dirname,'../../..');
const protocol=JSON.parse(fs.readFileSync(path.join(__dirname,'protocol.json')));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const sourcePaths=['app/proper-time.html',...['core.js','ui.js','web.html','build.py','v1b_boundary/protocol.json','v1b_boundary/common.cjs','v1b_boundary/native.cjs','v1b_boundary/browser.cjs','v1b_boundary/analyze.py','v1b_boundary/requirements.txt'].map(p=>'research/lorentz_proper_time_lab/'+p)];
function provenance(){return {
  git_commit:cp.execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim(),
  source_sha256:Object.fromEntries(sourcePaths.map(p=>[p,sha(fs.readFileSync(path.join(root,p)))])),
  dirty_source_paths:cp.execFileSync('git',['diff','HEAD','--name-only','--',...sourcePaths],{cwd:root,encoding:'utf8'}).trim().split('\n').filter(Boolean),
  runtime:{node:process.version,v8:process.versions.v8,platform:process.platform,architecture:process.arch,os_release:os.release()},
  timestamp_utc:new Date().toISOString()
};}
function flagsHex(flags){const b=Buffer.alloc(Math.ceil(flags.length/8));flags.forEach((v,i)=>{if(v)b[i>>3]|=1<<(i&7);});return b.toString('hex');}
module.exports={root,protocol,sha,provenance,flagsHex};
