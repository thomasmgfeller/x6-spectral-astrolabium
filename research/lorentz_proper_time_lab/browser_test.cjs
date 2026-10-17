/* UI acceptance, not scientific qualification. Screenshots are CI artifacts. */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'../..'),out=path.resolve(process.argv[2]||'/tmp/x6-proper-time-browser');
fs.mkdirSync(out,{recursive:true});
async function main(){
  const server=http.createServer((req,res)=>{
    const pathname=new URL(req.url,'http://localhost').pathname;
    const file=path.resolve(root,'.'+decodeURIComponent(pathname));
    if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404).end();return;}
    res.setHeader('Content-Type',file.endsWith('.html')?'text/html; charset=utf-8':file.endsWith('.ipynb')?'application/x-ipynb+json':'text/plain; charset=utf-8');
    fs.createReadStream(file).pipe(res);
  });
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  let browser;const checks=[],errors=[];
  try{
    browser=await chromium.launch({headless:true,args:['--no-sandbox']});
    const page=await browser.newPage({viewport:{width:1440,height:1000},acceptDownloads:true});
    page.on('pageerror',e=>errors.push(e.message));
    const base=`http://127.0.0.1:${server.address().port}`;
    await page.goto(base+'/app/proper-time.html');
    await page.waitForFunction(()=>document.querySelector('#count').textContent!=='—');
    assert.equal(await page.locator('#error').isVisible(),false);
    await page.screenshot({path:path.join(out,'desktop.png'),fullPage:true});
    const initial=await page.locator('#count').innerText();
    await page.locator('#run').click();assert.equal(await page.locator('#count').innerText(),initial);
    checks.push('Default cloud and deterministic replay');
    await page.getByRole('button',{name:'Kaum Ereignisse',exact:true}).click();
    assert.equal(await page.locator('#count').innerText(),'0');
    assert.match(await page.locator('#zero-note').innerText(),/obere Zeitgrenze.*positiv/);
    checks.push('K=0 keeps a positive upper confidence limit');
    await page.getByRole('button',{name:'Mehr Information',exact:true}).click();
    assert.match(await page.locator('#point-note').innerText(),/16.?384/);
    assert.equal(await page.locator('#cloud circle').count(),1402);
    assert.match(await page.locator('#chain-note').innerText(),/256/);
    checks.push('Display cap does not truncate inference; chain budget is explicit');
    await page.getByRole('button',{name:'1 + 1 Dimensionen',exact:true}).click();
    assert.equal(await page.locator('#dimension').inputValue(),'2');
    const estimate=Number((await page.locator('#estimate').innerText()).replaceAll('’','').replace(',','.'));
    await page.locator('.scale summary').click();await page.locator('#scale').fill('10');
    await page.waitForFunction(()=>document.querySelector('#estimate-unit').textContent.includes('10.000'));
    const scaled=Number((await page.locator('#estimate').innerText()).replaceAll('’','').replace(',','.'));
    assert.ok(Math.abs(scaled-10*estimate)<.01);checks.push('External scale changes time, not the point count');
    await page.locator('#scale').fill('0');await page.waitForFunction(()=>!document.querySelector('#error').hidden);
    assert.equal(await page.locator('#export').isDisabled(),true);
    await page.locator('#scale').fill('1');await page.waitForFunction(()=>document.querySelector('#error').hidden);
    await page.locator('#repeat').click();
    await page.waitForFunction(()=>!document.querySelector('#repeat-results').hidden,{},{timeout:30000});
    assert.match(await page.locator('#coverage').innerText(),/200/);
    const downloadPromise=page.waitForEvent('download');await page.locator('#export').click();
    const download=await downloadPromise;await download.saveAs(path.join(out,'experiment.json'));
    const exported=JSON.parse(fs.readFileSync(path.join(out,'experiment.json')));
    assert.equal(exported.repetitions.rows.length,200);assert.equal(exported.result.points.length,exported.parameters.m);
    assert.equal(exported.result.k,exported.result.inside.filter(Boolean).length);
    checks.push('200 trials and complete JSON export');
    const nb=await page.request.get(base+'/research/lorentz_proper_time_lab/eigenzeit.ipynb');
    assert.equal(nb.ok(),true);assert.equal((await nb.json()).nbformat,4);
    checks.push('Notebook download exists and is valid notebook JSON');
    await page.screenshot({path:path.join(out,'repetitions.png'),fullPage:true});
    for(const width of [360,390,768]){
      await page.setViewportSize({width,height:900});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,`overflow at ${width}`);
    }
    await page.setViewportSize({width:390,height:844});
    await page.screenshot({path:path.join(out,'mobile.png'),fullPage:true});
    checks.push('No horizontal overflow at 360, 390 and 768 pixels');
    const offlinePromise=page.waitForEvent('download');await page.locator('#export-html').click();
    const offline=await offlinePromise,offlinePath=path.join(out,'offline.html');await offline.saveAs(offlinePath);
    const offlinePage=await browser.newPage();offlinePage.on('pageerror',e=>errors.push(e.message));
    await offlinePage.goto('file://'+offlinePath);
    assert.equal(await offlinePage.locator('#error').isVisible(),false);
    assert.notEqual(await offlinePage.locator('#count').innerText(),'—');
    assert.equal(await offlinePage.locator('base').getAttribute('href'),'https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/');
    checks.push('Exported single HTML runs directly from disk');
    assert.deepEqual(errors,[]);
    fs.writeFileSync(path.join(out,'result.json'),JSON.stringify({status:'PASS_PROPER_TIME_LAB_BROWSER',checks,errors},null,2));
    console.log(JSON.stringify({status:'PASS_PROPER_TIME_LAB_BROWSER',checks},null,2));
  }finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
}
main().catch(e=>{console.error(e);process.exitCode=1;});
