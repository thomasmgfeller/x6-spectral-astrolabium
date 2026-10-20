'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),vm=require('node:vm'),zlib=require('node:zlib');
const assert=require('node:assert/strict');
const root=__dirname,out=path.resolve(process.argv[2]||path.join(root,'results/native_reference.json.gz'));
const protocol=JSON.parse(fs.readFileSync(path.join(root,'protocol.json')));
const manifest=JSON.parse(fs.readFileSync(path.join(root,'source_manifest.json')));
const source=fs.readFileSync(path.join(root,'source/core.js'));
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const blob=crypto.createHash('sha1').update(Buffer.from('blob '+source.length+'\0')).update(source).digest('hex');
assert.equal(blob,manifest.files.find(x=>x.path.endsWith('/core.js')).git_blob_sha1);
const P=require('./source/core.js');
// Extract unchanged normal() only because it is not exported by the source API.
const normalSource=source.toString().match(/  function normal\(random\) \{[\s\S]*?\n  \}/)[0];
const normal=vm.runInNewContext('('+normalSource.trim()+')');
const streams=protocol.seeds.map(seed=>{
  const random=P.rng(seed),normalRandom=P.rng(seed);
  return {seed,uniforms:Array.from({length:protocol.prng_values_per_seed},random),
    normals:Array.from({length:protocol.normal_values_per_seed},()=>normal(normalRandom))};
});
const clouds=[];
for(const d of protocol.dimensions)for(const seed of protocol.seeds){
  const args={m:protocol.m,d,theta:protocol.theta,seed};
  const c=P.cloud(args);
  clouds.push({parameters:args,points:c.points,inside:c.inside,k:c.k});
}
const tiny=P.cloud({m:64,d:4,theta:.5,seed:20261017});
const fixture=JSON.stringify({points:tiny.points,inside:tiny.inside});
const boundary=protocol.dimensions.map(d=>{
  const c=P.cloud({m:1,d,theta:.5,seed:protocol.boundary_seed});
  return {d,point:c.points[0],support:Math.abs(c.points[0][0])+Math.hypot(...c.points[0].slice(1))};
});
const result={git_commit:manifest.git_commit,source_sha256:hash(source),test_sha256:hash(fs.readFileSync(__filename)),
  protocol_sha256:hash(fs.readFileSync(path.join(root,'protocol.json'))),
  runtime:{node:process.version,v8:process.versions.v8,platform:process.platform,arch:process.arch},
  timestamp_utc:new Date().toISOString(),streams,clouds,boundary,
  fixture:{schema:'points and inside only',serialization:'UTF-8 JSON.stringify, no final newline',sha256:hash(fixture),points:tiny.points,inside:tiny.inside}};
fs.mkdirSync(path.dirname(out),{recursive:true});
fs.writeFileSync(out,zlib.gzipSync(JSON.stringify(result),{level:9}));
fs.writeFileSync(path.join(path.dirname(out),'native_fixture.json'),fixture);
console.log(JSON.stringify({output:out,clouds:clouds.length,unique_points:clouds.length*protocol.m,source_sha256:result.source_sha256,runtime:result.runtime}));
