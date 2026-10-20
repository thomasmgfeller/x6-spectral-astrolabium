/* Real Chromium controls, downloads and same-runtime byte replay, fixed matrix. */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http'),zlib=require('node:zlib');
const {chromium}=require('playwright');
const {root,protocol:q,sha,provenance,flagsHex}=require('./common.cjs');
const P=require('../core.js');
const out=path.resolve(process.argv[2]||'/tmp/x6-v1b-boundary');fs.mkdirSync(out,{recursive:true});
const nativeBytes=fs.readFileSync(path.join(out,'native_raw.json.gz'));
const native=JSON.parse(zlib.gunzipSync(nativeBytes));
const source=provenance();assert.deepEqual(source.source_sha256,native.provenance.source_sha256);
const failures=[],records=[],frozen=[];let maximumCoordinateError=0,maximumInferenceError=0,activeCase=null;
function close(a,b){return Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<=q.float_tolerance.absolute+q.float_tolerance.relative*Math.abs(b);}
async function setCase(page,p){
  await page.evaluate(p=>{
    for(const [id,value] of Object.entries({dimension:p.d,budget:p.m===64?0:4,theta:Math.round(100*p.theta),seed:p.seed,scale:p.T}))document.getElementById(id).value=String(value);
    document.getElementById('run').click();
  },p);
  assert.equal(await page.locator('#error').isVisible(),false);
}
async function download(page,id){const promise=page.waitForEvent('download');await page.locator('#'+id).click();const d=await promise;
  const bytes=fs.readFileSync(await d.path());await d.delete();return bytes;}
function compare(data,ref,p){
  assert.equal(data.schema,P.VERSION);assert.deepEqual(data.parameters,p);
  const r=data.result;assert.equal(r.sampling.policy,P.SAMPLER_POLICY);
  assert.deepEqual(r.sampling,ref.sampling);assert.equal(r.points.length,p.m);
  for(let i=0;i<p.m;i++){
    for(let j=0;j<p.d;j++){const e=Math.abs(r.points[i][j]-ref.points[i][j]);maximumCoordinateError=Math.max(maximumCoordinateError,e);assert.ok(close(r.points[i][j],ref.points[i][j]));}
    assert.ok(Math.abs(r.points[i][0])+Math.hypot(...r.points[i].slice(1))<.5);
  }
  assert.deepEqual(r.inside,ref.inside);assert.equal(r.k,ref.k);
  for(const key of ['estimate','lower','upper']){maximumInferenceError=Math.max(maximumInferenceError,Math.abs(r[key]-ref[key]));assert.ok(close(r[key],ref[key]));}
}
async function main(){
  const server=http.createServer((req,res)=>{const file=path.resolve(root,'.'+new URL(req.url,'http://localhost').pathname);
    if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404).end();return;}
    res.setHeader('Content-Type',file.endsWith('.html')?'text/html; charset=utf-8':'text/plain; charset=utf-8');fs.createReadStream(file).pipe(res);});
  await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;
  try{
    browser=await chromium.launch({headless:true,args:['--no-sandbox']});
    const url=`http://127.0.0.1:${server.address().port}/app/proper-time.html`;
    let page=await browser.newPage({acceptDownloads:true});page.on('pageerror',e=>failures.push(e.message));
    await page.goto(url);
    const cdp=await page.context().newCDPSession(page),engine=await cdp.send('Browser.getVersion');
    // Verify PRNG directly in the shipped inline browser core.
    const streams=await page.evaluate(q=>q.seeds.map(seed=>{const r=ProperTime.rng(seed);return {seed,uint32:Array.from({length:q.prng_values_per_seed},()=>r()*2**32)};}),q);
    assert.deepEqual(streams,native.streams);
    for(const c of native.clouds){
      for(const t of c.theta_results){
        const p={d:c.d,m:c.m,theta:t.theta,seed:c.parameters.seed,T:q.T};
        // Isolate cases: hundreds of downloads from one page can be throttled.
        // Each pair still regenerates and downloads twice in the same page.
        activeCase=p;await page.close();page=await browser.newPage({acceptDownloads:true});
        page.on('pageerror',e=>failures.push(e.message));await page.goto(url);
        await setCase(page,p);const a=await download(page,'export');
        await setCase(page,p);const b=await download(page,'export');assert.ok(a.equals(b),'Same-runtime downloaded JSON must replay byte for byte');
        const data=JSON.parse(a),ref=P.cloud(p);compare(data,ref,p);
        assert.equal(flagsHex(data.result.inside),t.flags_hex);assert.equal(data.result.k,t.k);
        records.push({parameters:p,bytes:a.length,export_sha256:sha(a),replay_sha256:sha(b),flags_hex:t.flags_hex,k:t.k});
        if(t.theta===.5){const name=`browser-d${p.d}-s${p.seed}.json.gz`,bytes=zlib.gzipSync(a,{level:9});fs.writeFileSync(path.join(out,name),bytes);frozen.push({file:name,sha256:sha(bytes)});}
      }
      console.log(`Browser matrix completed d=${c.d} seed=${c.parameters.seed}`);
    }
    const boundary=[];
    for(const d of q.dimensions){const p={d,m:64,theta:.5,seed:q.boundary_seed,T:1};
      await setCase(page,p);const a=await download(page,'export');await setCase(page,p);const b=await download(page,'export');assert.ok(a.equals(b));
      const data=JSON.parse(a);compare(data,P.cloud(p),p);boundary.push({parameters:p,export_sha256:sha(a),data});}
    // Test invalid input after a valid export: stale data must not remain exportable.
    await page.locator('#seed').fill('-1');await page.locator('#run').click();
    assert.equal(await page.locator('#error').isVisible(),true);assert.equal(await page.locator('#export').isDisabled(),true);
    const p={d:4,m:64,theta:.5,seed:q.boundary_seed,T:1};await setCase(page,p);
    const html=await download(page,'export-html'),htmlPath=path.join(out,'standalone.html');fs.writeFileSync(htmlPath,html);
    const standalone=await browser.newPage({acceptDownloads:true});standalone.on('pageerror',e=>failures.push(e.message));
    await standalone.goto('file://'+htmlPath);await setCase(standalone,p);
    const a=await download(standalone,'export');await setCase(standalone,p);const b=await download(standalone,'export');assert.ok(a.equals(b));
    compare(JSON.parse(a),P.cloud(p),p);assert.deepEqual(failures,[]);
    const report={schema:q.schema,status:'PASS_BROWSER_EXPORT_FREEZE',provenance:source,
      browser:{version:browser.version(),...engine,playwright:require('playwright/package.json').version},
      native_raw_sha256:sha(nativeBytes),matrix_cases:records.length,download_replays:records.length+boundary.length+1,
      maximum_coordinate_error:maximumCoordinateError,maximum_inference_error:maximumInferenceError,
      records,frozen_exports:frozen,boundary,standalone:{html_sha256:sha(html),export_sha256:sha(a),replay_sha256:sha(b)},
      invalid_input_export_blocked:true,page_errors:failures};
    fs.writeFileSync(path.join(out,'browser_report.json'),JSON.stringify(report,null,2)+'\n');
    console.log(JSON.stringify({status:report.status,cases:records.length,browser:report.browser,max_coordinate_error:maximumCoordinateError}));
  }finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
}
main().catch(e=>{
  fs.writeFileSync(path.join(out,'browser_failure.json'),JSON.stringify({error:e.message,activeCase,completed_cases:records.length,records,page_errors:failures},null,2)+'\n');
  console.error(e);process.exitCode=1;
});
