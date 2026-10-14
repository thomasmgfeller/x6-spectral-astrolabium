const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '../../..');
async function main() {
  const errors = [], remote = [], workers = [];
  const server = http.createServer((request, response) => {
    try {
      const url = new URL(request.url, 'http://localhost');
      const filename = path.resolve(root, '.' + decodeURIComponent(url.pathname));
      if (!filename.startsWith(root + path.sep) || !fs.statSync(filename).isFile()) throw Error('not found');
      response.writeHead(200, {'Content-Type':{'.html':'text/html','.mjs':'text/javascript','.json':'application/json','.md':'text/plain'}[path.extname(filename)] || 'application/octet-stream'});
      fs.createReadStream(filename).pipe(response);
    } catch {response.writeHead(404);response.end('not found');}
  });
  await new Promise(resolve => server.listen(0,'127.0.0.1',resolve));
  const base = 'http://127.0.0.1:' + server.address().port;
  let browser;
  try {
    browser = await chromium.launch({headless:true,args:['--no-sandbox'],...(process.env.X6_CHROMIUM_EXECUTABLE ? {executablePath:process.env.X6_CHROMIUM_EXECUTABLE}: {})});
    const page = await browser.newPage({viewport:{width:1280,height:1000}});
    page.on('pageerror', error=>errors.push(String(error)));
    page.on('request', request=>{if(!request.url().startsWith(base))remote.push(request.url());});
    page.on('worker', worker=>workers.push(worker.url()));
    await page.goto(base+'/experimental/experiment_fabric/browser.html');
    await page.waitForFunction(()=>!document.getElementById('run').disabled);
    await page.locator('#run').click();
    await page.waitForFunction(()=>!document.getElementById('export').disabled,{},{timeout:30000});
    const record=await page.evaluate(()=>window.X6FabricDemo.snapshot());
    const {verify}=await import(pathToFileURL(path.join(root,'experimental/experiment_fabric/run.mjs')).href);
    assert.equal((await verify(record)).status,'REPLAY_PASS');
    assert.equal(record.events.length,4);assert.equal(workers.length,8);
    assert.equal(await page.locator('#events tr').count(),4);
    assert.ok(record.final_model_probabilities.M_K144_C3>.99);
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth),false);
    if(process.env.X6_FABRIC_SCREENSHOT)await page.screenshot({path:process.env.X6_FABRIC_SCREENSHOT,fullPage:true});
    await page.setViewportSize({width:390,height:844});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth),false);
    await page.locator('#reset').click();
    await page.waitForFunction(()=>!document.getElementById('run').disabled);
    assert.equal(await page.locator('#events tr').count(),0);
    assert.equal(await page.locator('#export').isDisabled(),true);
    assert.deepEqual(errors,[]);assert.deepEqual(remote,[]);
    console.log(JSON.stringify({status:'BROWSER_WORKER_PASS',browser:browser.version(),worker_instances:workers.length,batches:record.events.length,desktop_and_mobile:true,external_requests:0,page_errors:0,physical_evidence:false},null,2));
  } finally {if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
}
main().catch(error=>{console.error(error.stack);process.exitCode=1;});
