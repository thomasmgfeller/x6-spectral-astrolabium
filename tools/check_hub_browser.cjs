/* Browser acceptance for the static hub; no scientific or device qualification. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '..');
const prefix = '/x6-spectral-astrolabium/';
const mime = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'application/javascript; charset=utf-8','.json':'application/json','.xml':'application/xml','.md':'text/plain; charset=utf-8','.txt':'text/plain; charset=utf-8'};
async function main() {
  const output = process.argv[2];
  assert(output, 'Usage: node tools/check_hub_browser.cjs NEW_OUTPUT_DIRECTORY');
  fs.mkdirSync(output, {recursive: false});
  const server = http.createServer((req,res) => {
    const url = new URL(req.url, 'http://localhost');
    if (!url.pathname.startsWith(prefix)) { res.writeHead(404).end(); return; }
    let file = path.resolve(root, decodeURIComponent(url.pathname.slice(prefix.length)) || 'index.html');
    if (!file.startsWith(root + path.sep)) { res.writeHead(403).end(); return; }
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    if (!fs.existsSync(file)) { res.writeHead(404).end(); return; }
    res.setHeader('Content-Type', mime[path.extname(file)] || 'application/octet-stream');
    fs.createReadStream(file).pipe(res);
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = `http://127.0.0.1:${server.address().port}${prefix}`;
  let browser;
  const checks = [], errors = [], badResponses = [];
  try {
    browser = await chromium.launch({headless:true,args:['--no-sandbox'],...(process.env.X6_CHROMIUM_EXECUTABLE ? {executablePath:process.env.X6_CHROMIUM_EXECUTABLE} : {})});
    const page = await browser.newPage({viewport:{width:1440,height:1040}});
    page.on('pageerror', e=>errors.push(e.message));
    page.on('response', r=>{if(r.status()>=400)badResponses.push({url:r.url(),status:r.status()});});
    await page.goto(base);
    assert.equal(await page.locator('html').getAttribute('lang'),'en');
    assert.equal(await page.locator('.path-grid article').count(),3);
    await page.screenshot({path:path.join(output,'overview-desktop.png'),fullPage:true});
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(()=>document.activeElement.className),'skip');
    await page.keyboard.press('Enter');
    assert.equal(new URL(page.url()).hash,'#main');
    checks.push('English entry has three routes and a keyboard-accessible skip link');
    await page.getByRole('link',{name:'Deutsch',exact:true}).click();
    assert.equal(await page.locator('html').getAttribute('lang'),'de');
    await page.getByRole('link',{name:'Ein erstes Experiment starten →',exact:true}).click();
    assert.equal(new URL(page.url()).hash,'#try');
    assert.equal(await page.locator('#try h2').innerText(),'2. Ein Browserexperiment ausprobieren');
    checks.push('Language navigation and the German guided route reach the correct content');
    await page.goto(base+'modules/');
    const all=JSON.parse(fs.readFileSync(path.join(root,'MODULE_REGISTRY.json'))).modules;
    assert.equal(await page.locator('.module:visible').count(),all.length);
    await page.getByLabel('Module durchsuchen / Search modules').fill('lorentz');
    const expected=all.filter(m=>(m.name+' '+m.claim).toLocaleLowerCase().includes('lorentz')).length;
    assert.equal(await page.locator('.module:visible').count(),expected);
    await page.getByLabel('Quelle / Source').selectOption('BRANCH_ONLY');
    assert.equal(await page.locator('.module:visible').count(),all.filter(m=>m.source.availability==='BRANCH_ONLY'&&(m.name+' '+m.claim).toLocaleLowerCase().includes('lorentz')).length);
    await page.getByLabel('Module durchsuchen / Search modules').fill('no-such-module-987654');
    assert.equal(await page.locator('#empty').isVisible(),true);
    await page.getByRole('button',{name:'Zurücksetzen / Reset'}).click();
    assert.equal(await page.locator('.module:visible').count(),all.length);
    await page.getByLabel('Art / Kind').selectOption('DOSSIER');
    assert.equal(await page.locator('.module:visible').count(),all.filter(m=>m.kind==='DOSSIER').length);
    checks.push('Search, combined filters, kind filter, empty state and reset match the register');
    await page.getByRole('button',{name:'Zurücksetzen / Reset'}).click();
    await page.getByRole('link',{name:'NQK: Forschungsdossier',exact:true}).click();
    assert.equal(await page.locator('main').innerText().then(t=>t.includes('historische Tests 001–013 unbestätigt')),true);
    assert.equal(await page.locator('main pre').count(),0);
    checks.push('The NQK dossier retains missing-evidence limits and offers no invented execution command');
    for (const url of ['', 'de/', 'modules/', 'modules/lorentz-n6-residuals.html']) {
      await page.setViewportSize({width:360,height:800});
      await page.goto(base+url);
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true, 'mobile overflow: '+url);
    }
    await page.goto(base+'de/');
    await page.screenshot({path:path.join(output,'overview-mobile-de.png'),fullPage:true});
    checks.push('Four representative pages fit a 360px mobile viewport without horizontal page overflow');
    const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:1280,height:900}});
    const crawler=await nojs.newPage();
    await crawler.goto(base+'modules/');
    assert.equal(await crawler.locator('.module').count(),all.length);
    assert.equal(await crawler.locator('#filters').isVisible(),false);
    for(const m of all)assert.equal(await crawler.getByRole('link',{name:m.name,exact:true}).count(),1);
    await crawler.getByRole('link',{name:all[0].name,exact:true}).click();
    assert.equal(await crawler.locator('main h2').count(),4);
    assert.equal((await crawler.locator('main').innerText()).includes(all[0].claim),true);
    checks.push('All 37 module links and four-part detail pages remain usable with JavaScript disabled');
    assert.deepEqual(errors,[]);
    assert.deepEqual(badResponses,[]);
    const result={status:'PASS',checks,playwright:require('playwright/package.json').version,chromium:browser.version(),page_errors:errors,bad_responses:badResponses,scope:'Hub navigation and selected browser accessibility checks; not a complete WCAG audit, search-index confirmation or scientific validation.'};
    fs.writeFileSync(path.join(output,'browser-report.json'),JSON.stringify(result,null,2)+'\n');
    console.log(JSON.stringify(result,null,2));
  } finally {
    if(browser)await browser.close();
    await new Promise(resolve=>server.close(resolve));
  }
}
main().catch(e=>{console.error(e);process.exitCode=1;});
