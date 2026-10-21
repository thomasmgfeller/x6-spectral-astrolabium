/* SPDX-License-Identifier: Apache-2.0
 * Observe the unchanged native sampler; never substitute its transform.
 * Each binary row is uint32 radial input, then float64 recovered radial CDF,
 * little endian, with no padding (12 bytes). Input buffers are replayable.
 */
'use strict';
const fs=require('node:fs'), path=require('node:path'), zlib=require('node:zlib');
const crypto=require('node:crypto'), assert=require('node:assert/strict');
const P=require('../core.js');
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const config=JSON.parse(fs.readFileSync(process.argv[2]));
const out=path.resolve(config.output);fs.mkdirSync(out,{recursive:true});
const old=config.historical ? JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(__dirname,'../v1b_boundary/results/native_raw.json.gz')))) : null;
const summaries=[];
for(const group of config.groups){
  const raw=Buffer.alloc(group.streams.length*config.m*12); let row=0;
  const records=[];
  for(const spec of group.streams){
    let read=0;const bytes=spec.input_file?fs.readFileSync(spec.input_file):null;
    const base=bytes?()=>{assert.ok(read*4<bytes.length,'Exhausted fixed uniform budget');return bytes.readUInt32LE(4*read++)/2**32;}:P.rng(spec.seed);
    let drawCount=0, recent=[], maxError=0, maxSupport=0;
    const random=()=>{const u=base();drawCount++;recent.push(u);return u;};
    const rejected={zeroTemporalUniform:0,invalidDirection:0,outsideSupport:0};
    const counts=Array(16).fill(0);
    const legacy=old?.clouds.find(c=>c.d===4&&c.parameters.seed===spec.seed);
    const coordinateHash=crypto.createHash('sha256');
    const coordinateBuffer=Buffer.alloc(32);
    for(let i=0;i<config.m;i++){
      recent=[];
      const c=P.samplePoint(random,4),p=c.point;
      assert.ok(recent.length>=9);
      const u=recent.at(-1),a=.5-Math.abs(p[0]);
      const radius=Math.hypot(...p.slice(1)),w=(radius/a)**3;
      if(legacy)assert.deepEqual(p,legacy.points[i],'Historical coordinates changed');
      maxError=Math.max(maxError,Math.abs(w-u));maxSupport=Math.max(maxSupport,Math.abs(p[0])+radius);
      raw.writeUInt32LE(u*2**32,12*row);raw.writeDoubleLE(w,12*row+4);row++;
      p.forEach((v,j)=>coordinateBuffer.writeDoubleLE(v,j*8));coordinateHash.update(coordinateBuffer);
      for(const key of Object.keys(rejected))rejected[key]+=c.rejected[key];
      for(let j=0;j<16;j++)if(P.insideDiamond(p,(10+5*j)/100))counts[j]++;
    }
    assert.ok(maxSupport<.5);assert.ok(maxError<1e-12);
    records.push({id:spec.id,seed:spec.seed??null,key:spec.key??null,n:config.m,draws:drawCount,rejected,
      max_transform_error:maxError,max_support:maxSupport,counts,
      coordinates_sha256:coordinateHash.digest('hex'),input_file_sha256:bytes?sha(bytes):null,
      historical_coordinate_replay:legacy?'EXACT':null});
  }
  const file=group.id+'.bin.gz',z=zlib.gzipSync(raw,{level:9});fs.writeFileSync(path.join(out,file),z);
  summaries.push({id:group.id,file,n:row,raw_sha256:sha(raw),file_sha256:sha(z),streams:records});
}
const result={schema:'x6.v1b-radial-trace/1',runtime:{node:process.version,v8:process.versions.v8,arch:process.arch,platform:process.platform},
  core_sha256:sha(fs.readFileSync(path.join(__dirname,'../core.js'))),trace_sha256:sha(fs.readFileSync(__filename)),groups:summaries};
fs.writeFileSync(path.join(out,config.summary_file),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({groups:summaries.length,points:summaries.reduce((s,g)=>s+g.n,0),output:out}));
