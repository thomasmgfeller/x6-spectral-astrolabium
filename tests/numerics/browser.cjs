'use strict';
// Real HTTP/browser UI test: input -> parser -> solver -> displayed JSON -> download.
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
const {chromium}=require('playwright');
const {ROOT,hash}=require('./kernel.cjs');
const output=path.resolve(process.argv[2]||'numerics-evidence');fs.mkdirSync(output,{recursive:true});
const contract=JSON.parse(fs.readFileSync(path.join(ROOT,'docs/numerics-v1/historical/check3-contract.json')));
const reference=JSON.parse(fs.readFileSync(path.join(output,'frozen-results.json')));
assert.equal(reference.status,'PASS');
assert.equal(reference.source.app_sha256,hash(fs.readFileSync(path.join(ROOT,'app/index.html'))));
const server=http.createServer((req,res)=>{
 const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
 const file=path.resolve(ROOT,'.'+pathname);
 if(!file.startsWith(ROOT+path.sep)){res.writeHead(403).end();return;}
 try{const data=fs.readFileSync(file);res.setHeader('Content-Type',file.endsWith('.html')?'text/html; charset=utf-8':file.endsWith('.js')?'text/javascript':'application/octet-stream');res.end(data);}catch(e){res.writeHead(404).end();}
});
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const browser=await chromium.launch({headless:true});
 const context=await browser.newContext({acceptDownloads:true,viewport:{width:1280,height:900}}),page=await context.newPage(),pageErrors=[];
 page.on('pageerror',e=>pageErrors.push(String(e)));
 const checks=[],runs=[];
 try{
  await page.goto('http://127.0.0.1:'+server.address().port+'/app/index.html',{waitUntil:'load'});
  await page.locator('#tab-spectrum').click();
  const f=page.frameLocator('#spectrumFrame');
  for(let i=0;i<contract.cases.length;i++){
   const c=contract.cases[i],ref=reference.results[i];
   await f.locator('#edges').fill(c.input);await f.locator('#run').click();
   const data=JSON.parse(await f.locator('#out').innerText());
   assert.equal(data.input,c.input);assert.equal(data.numerical.converged,true);
   const vals=data.numerical.eig.map(e=>e.value);assert.equal(vals.length,ref.n);
   const denominator=ref.scale_inf||1;
   const maxError=Math.max(...vals.map((v,j)=>Math.abs(v-ref.eigenvalues_reference[j])/denominator));
   assert.ok(maxError<=contract.eigenvalue_scaled_limit,c.id+': eigenvalues');
   assert.ok(data.numerical.scaledMaxResidual<=contract.residual_scaled_limit,c.id+': residual');
   checks.push({id:c.id,status:'PASS',scaledEigenvalueError:maxError});runs.push({id:c.id,analysis:data});
   if(['scaled_pair_-50','path4','isolated4'].includes(c.id)){
    const downloading=page.waitForEvent('download');await f.locator('#export').click();const download=await downloading;
    const name=path.join(output,'browser-export-'+c.id+'.json');await download.saveAs(name);
    assert.deepEqual(JSON.parse(fs.readFileSync(name)),data);
    checks.push({id:'export_'+c.id,status:'PASS'});
   }
  }
  for(const [id,input] of [['negative','a b -1'],['zero','a b 0'],['self_loop','a a 1'],['nan','a b NaN'],['overflow','a b 1e308'],['limit',Array.from({length:121},(_,i)=>'v'+i).join('\n')]]){
   await f.locator('#edges').fill(input);await f.locator('#run').click();assert.match(await f.locator('#out').innerText(),/^ERROR:/);
   checks.push({id:'reject_'+id,status:'PASS'});
  }
  const alert=page.waitForEvent('dialog').then(async dialog=>{const message=dialog.message();await dialog.dismiss();return message;});
  await f.locator('#export').click();assert.match(await alert,/Analyze first/);
  checks.push({id:'no_stale_export_after_invalid_input',status:'PASS'});
  const tiny=contract.cases.find(c=>c.id==='scaled_pair_-50');await f.locator('#edges').fill(tiny.input);await f.locator('#run').click();
  await page.screenshot({path:path.join(output,'browser-tiny-fixed.png'),fullPage:false});
  assert.deepEqual(pageErrors,[]);
  fs.writeFileSync(path.join(output,'browser-results.json'),JSON.stringify({schema:'x6.numerics.browser/1',status:'PASS',browser:browser.version(),source:reference.source,checks,runs,pageErrors,scope:'Real Chromium UI and JSON downloads for the 27 frozen inputs; eigenvectors remain internal.'},null,2)+'\n');
  console.log(JSON.stringify({status:'PASS',checks:checks.length,frozenCases:runs.length,pageErrors}));
 }finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
