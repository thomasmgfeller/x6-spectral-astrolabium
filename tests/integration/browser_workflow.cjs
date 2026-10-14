/* Focused UI/CLI interoperability test. Apache-2.0. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('playwright');
const evidence = require('../../app/signal-lab-evidence.js');

async function main() {
  const [base, nativeFile, output] = process.argv.slice(2);
  if (!base || !nativeFile || !output) throw new Error('Usage: browser_workflow.cjs BASE_URL NATIVE_EVIDENCE NEW_OUTPUT');
  fs.mkdirSync(output, {recursive: false});
  const browser = await chromium.launch({headless: true, args: ['--no-sandbox'], ...(process.env.X6_CHROMIUM_EXECUTABLE ? {executablePath: process.env.X6_CHROMIUM_EXECUTABLE} : {})});
  const errors = [];
  const checks = [];
  try {
    const page = await browser.newPage({acceptDownloads: true, viewport: {width: 1440, height: 1000}});
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(base);
    assert.equal(await page.title(), 'X6 · Lokaler Einstieg');
    assert.equal(await page.locator('nav article a').count(), 2);
    await page.screenshot({path: path.join(output, 'start-desktop.png'), fullPage: true});
    await page.setViewportSize({width: 390, height: 844});
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
    await page.screenshot({path: path.join(output, 'start-mobile.png'), fullPage: true});
    checks.push('Local entry renders both applications at desktop and mobile widths');
    await page.setViewportSize({width: 1440, height: 1000});
    await page.locator('a[href="/app/signal-lab.html"]').click();
    await page.waitForFunction(() => !!window.X6SignalLabUI);
    await page.locator('#sl-import-file').setInputFiles(nativeFile);
    await page.locator('#sl-import').click();
    await page.waitForFunction(() => ['ready', 'error'].includes(document.querySelector('#sl-status').dataset.state));
    const state = await page.evaluate(() => window.X6SignalLabUI.getState());
    assert.equal(state.phase, 'ready');
    const original = await evidence.verifyAndReplay(fs.readFileSync(nativeFile, 'utf8'));
    assert.deepEqual(state.result.parameters, original.result.parameters);
    assert.deepEqual(Object.fromEntries(Object.entries(state.result.analysis).map(([k,v]) => [k,v.status])), Object.fromEntries(Object.entries(original.result.analysis).map(([k,v]) => [k,v.status])));
    checks.push('CLI-native signal JSON imports and replays in the existing browser UI');
    for (const [selector, name] of [['#sl-export-json', 'browser-evidence.json'], ['#sl-export-csv', 'browser-samples.csv']]) {
      const pending = page.waitForEvent('download');
      await page.locator(selector).click();
      const download = await pending;
      await download.saveAs(path.join(output, name));
    }
    const downloaded = JSON.parse(fs.readFileSync(path.join(output, 'browser-evidence.json'), 'utf8'));
    assert.deepEqual(downloaded.payload.result, state.result);
    assert.equal((await evidence.verifyAndReplay(downloaded)).verification.passed, true);
    assert.equal(fs.readFileSync(path.join(output, 'browser-samples.csv'), 'utf8'), evidence.toCSV(state.result));
    await page.screenshot({path: path.join(output, 'signal-imported.png'), fullPage: true});
    checks.push('Actual browser JSON and CSV downloads preserve displayed data and pass native replay');
    await page.goto(base + 'app/index.html');
    for (const id of ['tab-signal', 'tab-spectrum', 'tab-audit']) assert.equal(await page.locator('#' + id).count(), 1);
    await page.frameLocator('#spectrumFrame').locator('body').waitFor({state: 'attached'});
    await page.locator('#tab-audit').click();
    await page.locator('#run39').click();
    await page.waitForFunction(() => {
      try { return JSON.parse(document.querySelector('#out39').textContent).total > 0; } catch (_) { return false; }
    });
    const qualification = JSON.parse(await page.locator('#out39').innerText());
    assert.equal(qualification.allPassed, true);
    checks.push('Existing Astrolabium browser qualification gate passes through the common server');
    assert.deepEqual(errors, []);
    const report = {status: 'PASS', playwright: require('playwright/package.json').version, chromium: browser.version(), checks, page_errors: errors, existing_app_qualification: qualification, scope: 'Browser entry, selected existing gate and signal import/export roundtrip; not all UI functions or hardware.'};
    fs.writeFileSync(path.join(output, 'browser-report.json'), JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify({status: report.status, checks: checks.length, chromium: report.chromium}));
  } finally { await browser.close(); }
}
main().catch(error => {console.error(error.stack); process.exitCode = 1;});
