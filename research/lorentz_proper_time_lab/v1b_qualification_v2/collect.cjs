/* SPDX-License-Identifier: Apache-2.0
 * Fixed collection, unchanged native sampler, no interim statistical decisions.
 */
'use strict';
const fs=require('node:fs'), path=require('node:path'), crypto=require('node:crypto');
const zlib=require('node:zlib'), assert=require('node:assert/strict');
const P=require('../core.js'), {qualifiedInterval}=require('./qualified.cjs');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const fixture=process.argv[2]==='--fixture';
const output=path.resolve(fixture?process.argv[3]:(process.argv[2]||path.join(__dirname,'results/raw')));
assert.ok(!fs.existsSync(output),'Collection output must not exist; no replacement/rerun.');
const protocol=fixture?null:JSON.parse(fs.readFileSync(path.join(__dirname,'protocol.json')));
if(protocol) {
  assert.equal(Number(process.versions.node.split('.')[0]),protocol.runtime.node_major);
  assert.equal(sha(fs.readFileSync(path.join(__dirname,'../core.js'))),protocol.core_sha256);
  for(const [name,pin] of Object.entries(protocol.frozen_files))
    assert.equal(sha(fs.readFileSync(path.join(__dirname,name))),pin,name);
}
const schedule=fixture?{groups:[2,3,4].map(d=>({id:`fixture-d${d}`,arm:'native',d,seeds:[0,1]}))}:
  JSON.parse(fs.readFileSync(path.join(__dirname,'seeds.json')));
const m=4096, thetas=[.1,.2,.4,.7], started=Date.now(), tables={}, summaries=[];
fs.mkdirSync(output,{recursive:true});
for(const group of schedule.groups) {
  const {d,arm}=group, rowPath=path.join(output,group.id+'.jsonl');
  const thresholds=d===2?[0]:(d===3?[-Math.SQRT1_2,0,Math.SQRT1_2]:[-.5,0,.5]);
  const coordinateBuffer=Buffer.alloc(m*d*8), seenK=new Set();
  for(let si=0;si<group.seeds.length;si++) {
    assert.ok(Date.now()-started<1200000,'Fixed 1200-second collection budget exhausted.');
    const seed=group.seeds[si], base=P.rng(seed);
    let recent=[], draws=0;
    const random=()=>{const u=base();recent.push(u);draws++;return u;};
    const counts=[0,0,0,0], marginals={};
    for(const kind of ['time','radial']) for(let j=0;j<3;j++) marginals[`${kind}_${j}`]=0;
    for(let axis=0;axis<d-1;axis++) for(let j=0;j<thresholds.length;j++) marginals[`angle_${axis}_${j}`]=0;
    const rejected={zeroTemporalUniform:0,invalidDirection:0,outsideSupport:0};
    let maxRadialError=0,maxTimeError=0,maxSupport=0,zeros=0;
    let first=null;
    for(let i=0;i<m;i++) {
      let c;
      if(arm==='repeated-point' && i>0) c=first;
      else {recent=[];c=P.samplePoint(random,d);first=c;
        for(const key of Object.keys(rejected)) rejected[key]+=c.rejected[key];}
      const p=c.point.slice(), n=d-1, accepted=recent.slice(-(2*d+1));
      assert.equal(accepted.length,2*d+1);
      const A=.5-Math.abs(p[0]), nativeR=Math.hypot(...p.slice(1));
      maxRadialError=Math.max(maxRadialError,Math.abs((nativeR/A)**n-accepted.at(-1)));
      maxTimeError=Math.max(maxTimeError,Math.abs((2*A)**d-accepted[0]));
      if(arm==='wrong-radius' && nativeR>0) {
        const scale=A*accepted.at(-1)/nativeR;
        for(let axis=1;axis<d;axis++)p[axis]*=scale;
      }
      const r=Math.hypot(...p.slice(1)), support=Math.abs(p[0])+r;
      assert.ok(p.every(Number.isFinite)&&support<.5,'Strict support violated');
      maxSupport=Math.max(maxSupport,support);
      const z=(2*A)**d,w=(r/A)**n;
      for(let j=0;j<3;j++) {
        if(z<=[.25,.5,.75][j])marginals[`time_${j}`]++;
        if(w<=[.25,.5,.75][j])marginals[`radial_${j}`]++;
      }
      let direction;
      if(r===0) {
        zeros++;
        const v=Array.from({length:n},(_,j)=>Math.sqrt(-2*Math.log(Math.max(.5/2**32,accepted[2+2*j])))*Math.cos(2*Math.PI*accepted[3+2*j]));
        const norm=Math.hypot(...v); direction=v.map(x=>x/norm);
      } else direction=p.slice(1).map(x=>x/r);
      for(let axis=0;axis<n;axis++)for(let j=0;j<thresholds.length;j++)
        if(direction[axis]<=thresholds[j])marginals[`angle_${axis}_${j}`]++;
      for(let j=0;j<thetas.length;j++) if(support<thetas[j]/2)counts[j]++;
      p.forEach((v,j)=>coordinateBuffer.writeDoubleLE(v,(i*d+j)*8));
    }
    assert.ok(maxRadialError<=1e-12 && maxTimeError<=1e-12,'Transform identity failed');
    if(fixture) for(let j=0;j<thetas.length;j++) {
      const reference=P.cloud({m,d,theta:thetas[j],seed});
      assert.equal(reference.k,counts[j]);
      const bytes=Buffer.alloc(m*d*8);
      reference.points.forEach((p,i)=>p.forEach((v,k)=>bytes.writeDoubleLE(v,(i*d+k)*8)));
      assert.equal(sha(bytes),sha(coordinateBuffer));
    }
    counts.forEach(k=>seenK.add(k));
    const record={index:si,seed,d,arm,counts,marginals,draws,rejected,zero_radius:zeros,
      max_radial_error:maxRadialError,max_time_error:maxTimeError,max_support:maxSupport,
      coordinates_sha256:sha(coordinateBuffer)};
    fs.appendFileSync(rowPath,JSON.stringify(record)+'\n');
    if((si+1)%1024===0)console.log(JSON.stringify({group:group.id,completed:si+1,total:group.seeds.length,elapsed_seconds:(Date.now()-started)/1000}));
  }
  tables[d]??={};
  for(const k of [...seenK].sort((a,b)=>a-b))tables[d][k]=qualifiedInterval(k,m,d);
  const raw=fs.readFileSync(rowPath),packed=zlib.gzipSync(raw,{level:9});
  const file=group.id+'.jsonl.gz';fs.writeFileSync(path.join(output,file),packed);fs.unlinkSync(rowPath);
  summaries.push({id:group.id,d,arm,clouds:group.seeds.length,file,sha256:sha(packed),raw_sha256:sha(raw)});
  fs.writeFileSync(path.join(output,'progress.json'),JSON.stringify({groups:summaries},null,2)+'\n');
  console.log(JSON.stringify({group:group.id,complete:true,elapsed_seconds:(Date.now()-started)/1000}));
}
const intervalBytes=zlib.gzipSync(Buffer.from(JSON.stringify(tables)+'\n'),{level:9});
fs.writeFileSync(path.join(output,'native-intervals.json.gz'),intervalBytes);
const manifest={schema:'x6.v1b-qualification-raw/2',fixture,started_utc:new Date(started).toISOString(),
  elapsed_seconds:(Date.now()-started)/1000,runtime:{node:process.version,v8:process.versions.v8,platform:process.platform,arch:process.arch},
  protocol_sha256:protocol?sha(fs.readFileSync(path.join(__dirname,'protocol.json'))):null,
  groups:summaries,intervals_sha256:sha(intervalBytes),
  raw_contract:'Per-cloud sufficient statistics plus ordered-coordinate SHA-256; coordinates are replayable from seeds but not stored.'};
fs.writeFileSync(path.join(output,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
console.log(JSON.stringify({complete:true,output,elapsed_seconds:manifest.elapsed_seconds}));
