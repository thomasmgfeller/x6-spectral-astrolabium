'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const os = require('node:os');
const crypto = require('node:crypto');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');
const evidence = require('../../app/signal-lab-evidence.js');
const root = path.resolve(__dirname, '../..');
const output = process.env.X6_EVIDENCE_DIR ? path.resolve(process.env.X6_EVIDENCE_DIR) : null;
const results = [], pageErrors = [], remoteRequests = [];
const methods = ['identity', 'moving_average', 'fft_lowpass', 'x6_phase'];
const clone = value => JSON.parse(JSON.stringify(value));
let browserVersion = null;

async function test(name, fn) {
  try { await fn(); results.push({ name, passed: true }); }
  catch (error) { results.push({ name, passed: false, error: String(error.stack || error) }); }
}

function staticServer() {
  const types = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json', '.md': 'text/plain; charset=utf-8' };
  return http.createServer((request, response) => {
    try {
      const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
      const filename = path.resolve(root, '.' + pathname + (pathname.endsWith('/') ? 'index.html' : ''));
      if (!filename.startsWith(root + path.sep) || !fs.statSync(filename).isFile()) throw new Error('not found');
      response.writeHead(200, { 'Content-Type': types[path.extname(filename)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
      fs.createReadStream(filename).pipe(response);
    } catch (_) { response.writeHead(404); response.end('Not found'); }
  });
}

async function state(page) { return page.evaluate(() => window.X6SignalLabUI.getState()); }
async function run(page) {
  await page.locator('#sl-run').click();
  await page.waitForFunction(() => ['ready', 'error'].includes(document.querySelector('#sl-status').dataset.state));
  assert.equal((await state(page)).phase, 'ready', await page.locator('#sl-status').innerText());
}
async function errorState(page) {
  await page.waitForFunction(() => document.querySelector('#sl-status').dataset.state === 'error');
  assert.equal((await state(page)).result, null);
  assert.equal(await page.locator('#sl-export-json').isDisabled(), true);
  assert.equal(await page.locator('#sl-export-csv').isDisabled(), true);
}
async function importJSON(page, object) {
  await page.locator('#sl-import-file').setInputFiles({ name: 'evidence.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(object)) });
  await page.locator('#sl-import').click();
}
async function downloaded(page, selector, target) {
  const pending = page.waitForEvent('download');
  await page.locator(selector).click();
  const download = await pending;
  await download.saveAs(target);
  return fs.readFileSync(target, 'utf8');
}

async function main() {
  if (output) fs.mkdirSync(output, { recursive: true });
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'x6-signal-ui-'));
  const server = staticServer();
  await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
  const base = 'http://127.0.0.1:' + server.address().port;
  let browser;
  try {
    const options = { headless: true, args: ['--no-sandbox'] };
    if (process.env.X6_CHROMIUM_EXECUTABLE) options.executablePath = process.env.X6_CHROMIUM_EXECUTABLE;
    browser = await chromium.launch(options);
    browserVersion = browser.version();
    const context = await browser.newContext({ acceptDownloads: true, viewport: { width: 1440, height: 1000 }, locale: 'de-CH' });
    const page = await context.newPage();
    page.setDefaultTimeout(10000);
    page.on('pageerror', error => pageErrors.push(error.message));
    page.on('request', request => { if (/^https?:/.test(request.url()) && !request.url().startsWith(base + '/')) remoteRequests.push(request.url()); });
    await page.goto(base + '/app/signal-lab.html');
    await page.waitForFunction(() => !!window.X6SignalLabUI);
    let exported = null, captured = null;

    await test('Initial page requires a run and disables stale exports', async () => {
      assert.equal((await state(page)).result, null);
      assert.equal(await page.locator('#sl-export-json').isDisabled(), true);
      assert.equal(await page.locator('#sl-export-csv').isDisabled(), true);
      assert.equal(await page.locator('[data-param]').count(), 25);
    });
    await test('Default run displays actual four-method metrics and finite sample arrays', async () => {
      await run(page);
      const s = await state(page);
      assert.equal(s.result.parameters.samples, 1024);
      assert.equal(await page.locator('#sl-comparison tbody tr[data-method]').count(), 4);
      for (const method of methods) {
        assert.equal(s.result.arrays.outputs[method].length, 1024);
        assert.ok(s.result.arrays.outputs[method].every(Number.isFinite));
        const cell = await page.locator('tr[data-method="' + method + '"] td[data-metric="nrmse"]').innerText();
        assert.ok(Math.abs(Number(cell.replace(',', '.')) - s.result.analysis[method].metrics.nrmse.value) <= 0.00051, cell);
      }
      assert.equal(s.result.analysis.x6_phase.status, 'FAIL');
      assert.equal(s.result.analysis.fft_lowpass.status, 'PASS');
    });
    await test('Method selection redraws actual charts without regenerating the experiment', async () => {
      const before = await state(page);
      const imageBefore = await page.locator('#sl-time-chart').evaluate(canvas => canvas.toDataURL());
      await page.locator('#sl-method').selectOption('fft_lowpass');
      const after = await state(page);
      assert.equal(after.selectedMethod, 'fft_lowpass');
      assert.deepEqual(after.result, before.result);
      assert.notEqual(await page.locator('#sl-time-chart').evaluate(canvas => canvas.toDataURL()), imageBefore);
      for (const id of ['sl-time-chart', 'sl-psd-chart', 'sl-coherence-chart']) {
        assert.ok((await page.locator('#' + id).getAttribute('aria-label')).length > 30);
      }
    });
    await test('Changing a parameter immediately invalidates completed output', async () => {
      await page.locator('#sl-noise').fill('0.05');
      const s = await state(page);
      assert.equal(s.phase, 'pending'); assert.equal(s.result, null); assert.equal(s.suite, null);
      assert.equal(await page.locator('#sl-export-json').isDisabled(), true);
      const values = await page.locator('#sl-comparison tbody td[data-metric]').allTextContents();
      assert.ok(values.every(value => value.trim() === '—'));
    });
    await test('Invalid and blank numerical fields cannot yield a result or stale download', async () => {
      await page.locator('#sl-seed').fill('-1');
      await page.locator('#sl-run').click(); await errorState(page);
      assert.equal(await page.locator('#sl-seed').getAttribute('aria-invalid'), 'true');
      await page.locator('#sl-seed').fill('0');
      await page.locator('#sl-amplitude').fill('');
      await page.locator('#sl-run').click(); await errorState(page);
      assert.equal(await page.locator('#sl-amplitude').getAttribute('aria-invalid'), 'true');
      await page.locator('#sl-amplitude').fill('1');
    });
    await test('A new chirp experiment uses exactly the selected seed, sampling and controls', async () => {
      await page.locator('#sl-signal').selectOption('chirp');
      await page.locator('#sl-samples').selectOption('512');
      await page.locator('#sl-frequency').fill('37');
      await run(page);
      const s = await state(page);
      assert.equal(s.result.parameters.seed, 0);
      assert.equal(s.result.parameters.frequency, 37);
      assert.equal(s.result.parameters.noiseStd, 0.05);
      assert.equal(s.result.arrays.reference.length, 512);
      assert.equal(s.result.arrays.time[511], 511 / 1024);
    });
    await test('Counterexamples show eight actual constructions and 27 passing checks', async () => {
      await page.locator('#sl-counterexamples').click();
      await page.waitForFunction(() => !!window.X6SignalLabUI.getState().suite);
      const s = await state(page);
      assert.equal(s.suite.totalCases, 8); assert.equal(s.suite.totalChecks, 27); assert.equal(s.suite.passedChecks, 27);
      assert.equal(s.suite.passed, true);
      assert.equal(await page.locator('#sl-suite-results [data-case][data-passed="true"]').count(), 8);
      const inverse = s.suite.cases.find(c => c.id === 'polarity_inversion');
      assert.equal(inverse.result.analysis.identity.metrics.nrmse.value, 2);
      assert.equal(inverse.result.analysis.identity.status, 'FAIL');
    });
    await test('JSON download preserves every displayed array, metric and counterexample', async () => {
      captured = await state(page);
      exported = JSON.parse(await downloaded(page, '#sl-export-json', path.join(temp, 'evidence.json')));
      assert.deepEqual(exported.payload.result, captured.result);
      assert.deepEqual(exported.payload.counterexamples, captured.suite);
      const hash = crypto.createHash('sha256').update(evidence.canonical(exported.payload)).digest('hex');
      assert.equal(exported.integrity.sha256, hash);
      if (output) fs.copyFileSync(path.join(temp, 'evidence.json'), path.join(output, 'actual-browser-evidence.json'));
      assert.equal((await evidence.verifyAndReplay(exported)).verification.passed, true);
    });
    await test('CSV download contains every actual sample from all four methods', async () => {
      const text = await downloaded(page, '#sl-export-csv', path.join(temp, 'samples.csv'));
      const rows = text.trim().split('\n');
      assert.equal(rows.length, 513);
      assert.equal(rows[0], 'index,time_s,reference,observed,identity,moving_average,fft_lowpass,x6_phase');
      for (let i = 0; i < captured.result.parameters.samples; i++) {
        assert.deepEqual(rows[i + 1].split(',').map(Number), [i, captured.result.arrays.time[i], captured.result.arrays.reference[i],
          captured.result.arrays.observed[i], ...methods.map(m => captured.result.arrays.outputs[m][i])]);
      }
      if (output) fs.copyFileSync(path.join(temp, 'samples.csv'), path.join(output, 'actual-browser-samples.csv'));
    });
    await test('Import clears old state, verifies digest and actually restores the experiment', async () => {
      await page.locator('#sl-noise').fill('0.9');
      await importJSON(page, exported);
      await page.waitForFunction(() => window.X6SignalLabUI.getState().phase === 'ready');
      const restored = await state(page);
      assert.equal(restored.verification.passed, true);
      assert.equal(restored.verification.authenticity, 'NOT_ASSESSED');
      assert.deepEqual(restored.result, captured.result);
      assert.deepEqual(restored.suite, captured.suite);
      assert.equal(await page.locator('#sl-noise').inputValue(), '0.05');
    });
    await test('Changing file selection invalidates output before reading any file', async () => {
      await page.locator('#sl-import-file').setInputFiles({ name: 'invalid.json', mimeType: 'application/json', buffer: Buffer.from('{broken') });
      assert.equal((await state(page)).result, null);
      assert.equal(await page.locator('#sl-export-json').isDisabled(), true);
      await page.locator('#sl-import').click(); await errorState(page);
    });
    await test('Tampered evidence is rejected without displaying old or submitted data', async () => {
      const edited = clone(exported); edited.payload.result.arrays.observed[1] += 1;
      await importJSON(page, edited); await errorState(page);
      assert.ok((await page.locator('#sl-status-detail').innerText()).includes('SHA-256 mismatch'));
    });
    await test('Rehashed forged results are rejected by computational replay in browser', async () => {
      const edited = clone(exported); edited.payload.result.arrays.outputs.x6_phase[2] += 1;
      edited.integrity.sha256 = crypto.createHash('sha256').update(evidence.canonical(edited.payload)).digest('hex');
      await importJSON(page, edited); await errorState(page);
      assert.ok((await page.locator('#sl-status-detail').innerText()).includes('Replay numerical mismatch'));
    });
    await test('An edit during asynchronous hashing cancels an outdated export', async () => {
      await run(page);
      let downloads = 0; const listen = () => downloads++; page.on('download', listen);
      await page.evaluate(() => {
        const saved = crypto.subtle.digest.bind(crypto.subtle);
        window.__digestSaved = saved; window.__digestDone = false;
        crypto.subtle.digest = async function (...args) {
          await new Promise(resolve => { window.__releaseDigest = resolve; });
          const result = await saved(...args); window.__digestDone = true; return result;
        };
      });
      try {
        await page.locator('#sl-export-json').click();
        await page.waitForFunction(() => typeof window.__releaseDigest === 'function');
        await page.locator('#sl-noise').fill('0.06');
        await page.evaluate(() => window.__releaseDigest());
        await page.waitForFunction(() => window.__digestDone);
        await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
        assert.equal(downloads, 0);
        assert.equal((await state(page)).phase, 'pending');
        assert.equal(await page.locator('#sl-export-json').isDisabled(), true);
      } finally {
        await page.evaluate(() => { crypto.subtle.digest = window.__digestSaved; });
        page.off('download', listen);
      }
    });
    await test('DE EN FR labels update while the completed calculation stays identical', async () => {
      await run(page);
      const fixed = (await state(page)).result;
      const labels = [];
      for (const lang of ['de', 'en', 'fr']) {
        await page.locator('#sl-language').selectOption(lang);
        assert.equal(await page.locator('html').getAttribute('lang'), lang);
        labels.push(await page.locator('#sl-run').innerText());
        assert.deepEqual((await state(page)).result, fixed);
      }
      assert.equal(new Set(labels).size, 3);
      await page.locator('#sl-language').selectOption('de');
    });
    await test('Desktop and 390px mobile layouts remain usable without page overflow', async () => {
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
      if (output) await page.screenshot({ path: path.join(output, 'signal-lab-desktop.png'), fullPage: true });
      await page.setViewportSize({ width: 390, height: 844 });
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
      assert.ok(await page.locator('#sl-run').isVisible());
      if (output) await page.screenshot({ path: path.join(output, 'signal-lab-mobile.png'), fullPage: true });
      await page.setViewportSize({ width: 1440, height: 1000 });
    });
    await test('Local file opening supports computation and verified export without a server', async () => {
      const local = await context.newPage();
      local.on('pageerror', error => pageErrors.push(error.message));
      local.setDefaultTimeout(10000);
      await local.goto(pathToFileURL(path.join(root, 'app/signal-lab.html')).href);
      await local.waitForFunction(() => !!window.X6SignalLabUI);
      await run(local);
      const doc = JSON.parse(await downloaded(local, '#sl-export-json', path.join(temp, 'offline.json')));
      assert.equal(doc.payload.evidence_class, 'SYNTHETIC_RESULT');
      assert.equal((await evidence.verifyAndReplay(doc)).verification.passed, true);
      await local.close();
    });
    await test('Portal integration points to the new lab and keeps the research app accessible', async () => {
      const portal = await context.newPage();
      await portal.goto(base + '/index.html');
      // The portal may expose one primary entry or repeat it in several sections.
      // Verify the actual route and reachable lab instead of the old link count.
      const labLinks = portal.locator('a[href="app/signal-lab.html"], a[href="./app/signal-lab.html"]');
      assert.ok(await labLinks.count() > 0, 'portal exposes a direct Signal Lab entry');
      assert.ok(await labLinks.first().isVisible(), 'primary lab entry is visible');
      await labLinks.first().click();
      await portal.waitForFunction(() => !!window.X6SignalLabUI);
      assert.ok(await portal.locator('a[href="./index.html"]').count() > 0);
      await portal.close();
    });
    await test('No browser JavaScript errors or external requests from the lab', async () => {
      assert.deepEqual(pageErrors, []);
      assert.deepEqual(remoteRequests, []);
    });
    await context.close();
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
    fs.rmSync(temp, { recursive: true, force: true });
  }
}

main().catch(error => { results.push({ name: 'browser setup or teardown', passed: false, error: String(error.stack || error) }); }).finally(() => {
  const report = { schema: 'x6.signal-lab.browser-tests/1', status: results.length > 0 && results.every(x => x.passed) ? 'PASS' : 'FAIL',
    browser_version: browserVersion, total: results.length, passed: results.filter(x => x.passed).length,
    page_errors: pageErrors, external_requests: remoteRequests, cases: results };
  if (output) fs.writeFileSync(path.join(output, 'browser-report.json'), JSON.stringify(report, null, 2) + '\n');
  process.stdout.write(JSON.stringify(report, null, 2) + '\n');
  if (report.status !== 'PASS') process.exitCode = 1;
});
