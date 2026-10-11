'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const { spawn } = require('node:child_process');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '../..');
const results = [], errors = [];
const raw = fs.readFileSync(path.join(root, 'device/fixtures/synthetic_chsh_capture.bin'));
async function test(name, fn) { await fn(); results.push({ name, passed: true }); }
async function main() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'x6-sagnac-ui-'));
  const server = spawn(process.env.PYTHON || 'python3', ['-u', 'device/sagnac_bridge.py', '--port', '0'], { cwd: root });
  let browser;
  try {
    const url = await new Promise((resolve, reject) => {
      let text = '';
      const timeout = setTimeout(() => reject(Error('Bridge startup timeout')), 10000);
      server.stdout.on('data', b => { text += b; const m = text.match(/http:\/\/127\.0\.0\.1:\d+\/app\//); if (m) { clearTimeout(timeout); resolve(m[0]); } });
      server.on('exit', code => { clearTimeout(timeout); reject(Error('Bridge exit ' + code)); });
    });
    browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
    const page = await browser.newPage({ acceptDownloads: true, viewport: { width: 1360, height: 960 } });
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(url);
    await page.locator('#tab-sagnac').click();
    async function valid() { await page.waitForFunction(() => document.querySelector('#sg-status').dataset.state === 'valid'); }
    async function invalid() { await page.waitForFunction(() => document.querySelector('#sg-status').dataset.state === 'invalid'); }
    await test('Synthetic example, raw counts, CHSH and permanently disabled control', async () => {
      await page.locator('#sg-demo').click(); await valid();
      assert.equal(await page.locator('#sg-counts tr').count(), 4);
      assert.ok((await page.locator('#sg-conditional').innerText()).includes('-2.825365'));
      assert.ok((await page.locator('#sg-all').innerText()).includes('-1.412500'));
      assert.equal(await page.locator('#sg-control').isDisabled(), true);
      assert.ok((await page.locator('#sg-origin-badge').innerText()).includes('SYNTHETISCH'));
    });
    await test('Evidence export preserves binary bytes, provenance and physical status', async () => {
      const wait = page.waitForEvent('download'); await page.locator('#sg-export').click();
      const download = await wait; const out = path.join(tmp, 'evidence.json'); await download.saveAs(out);
      const r = JSON.parse(fs.readFileSync(out, 'utf8'));
      assert.equal(r.origin, 'synthetic'); assert.equal(r.physical_quantum_claim, 'NOT_ASSESSED');
      assert.deepEqual(Buffer.from(r.input.raw_base64, 'base64'), raw);
      assert.equal(r.control.actuator_commands, false);
    });
    await test('Corruption blocks display and stale export', async () => {
      const damaged = Buffer.from(raw); damaged[55] ^= 1;
      await page.locator('#sg-origin').selectOption('synthetic');
      await page.locator('#sg-file').setInputFiles({ name: 'damaged.bin', mimeType: 'application/octet-stream', buffer: damaged });
      await page.locator('#sg-import').click(); await invalid();
      assert.equal(await page.locator('#sg-counts tr').count(), 0);
      assert.equal(await page.locator('#sg-export').isDisabled(), true);
    });
    await test('Hardware file declaration never produces physical verification', async () => {
      await page.locator('#sg-origin').selectOption('hardware');
      await page.locator('#sg-file').setInputFiles({ name: 'declared-hardware.bin', mimeType: 'application/octet-stream', buffer: raw });
      await page.locator('#sg-import').click(); await valid();
      assert.ok((await page.locator('#sg-origin-badge').innerText()).includes('unbestätigt'));
      const r = JSON.parse(await page.locator('#sg-details').textContent());
      assert.equal(r.physical_quantum_claim, 'NOT_ASSESSED');
    });
    await test('Real loopback bridge read and blocked command endpoint', async () => {
      await page.locator('#sg-connect').click(); await valid();
      assert.ok((await page.locator('#sg-summary').innerText()).includes('FILE_REPLAY'));
      const response = await page.request.post(new URL('/api/control', url).href, { data: { start: true } });
      assert.equal(response.status(), 405);
    });
    await test('Disconnected bridge removes prior successful results', async () => {
      await page.route('**/api/sagnac/capture', route => route.fulfill({ status: 503, body: '{}' }));
      await page.locator('#sg-connect').click(); await invalid();
      assert.equal(await page.locator('#sg-export').isDisabled(), true);
      assert.equal(await page.locator('#sg-counts tr').count(), 0);
      await page.unroute('**/api/sagnac/capture');
    });
    await test('DE EN FR labels', async () => {
      for (const [lang, text] of [['en', 'measurement data'], ['fr', 'mesures'], ['de', 'Messdaten']]) {
        await page.locator('#lang').selectOption(lang);
        assert.ok((await page.locator('[data-sg=title]').innerText()).includes(text));
      }
    });
    await test('Existing X6 graph qualification remains 10/10', async () => {
      await page.locator('#tab-audit').click(); await page.locator('#run39').click();
      await page.waitForFunction(() => { try { return JSON.parse(document.querySelector('#out39').textContent).total > 0; } catch { return false; } });
      const r = JSON.parse(await page.locator('#out39').textContent());
      assert.equal(r.allPassed, true); assert.equal(r.total, 10);
    });
    await test('Mobile layout has no viewport overflow', async () => {
      await page.locator('#tab-sagnac').click(); await page.locator('#sg-demo').click(); await valid();
      await page.setViewportSize({ width: 390, height: 844 });
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
      if (process.env.X6_SCREENSHOT_DIR) {
        fs.mkdirSync(process.env.X6_SCREENSHOT_DIR, { recursive: true });
        await page.screenshot({ path: path.join(process.env.X6_SCREENSHOT_DIR, 'sagnac-mobile.png'), fullPage: true });
        await page.setViewportSize({ width: 1360, height: 960 });
        await page.screenshot({ path: path.join(process.env.X6_SCREENSHOT_DIR, 'sagnac-desktop.png'), fullPage: true });
      }
    });
    await test('Offline file opening supports demo without a service', async () => {
      await page.goto(pathToFileURL(path.join(root, 'app/index.html')).href);
      await page.locator('#tab-sagnac').click(); await page.locator('#sg-demo').click(); await valid();
      assert.equal(await page.locator('#sg-counts tr').count(), 4);
    });
    assert.deepEqual(errors, []);
    console.log(JSON.stringify({ status: 'PASS', commit: process.env.GITHUB_SHA || null, tests: results.length, browser_errors: errors, results }, null, 2));
  } finally {
    if (browser) await browser.close();
    server.kill('SIGINT');
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}
main().catch(e => {
  console.log(JSON.stringify({ status: 'FAIL', commit: process.env.GITHUB_SHA || null,
    completed_tests: results.length, browser_errors: errors, results, error: String(e.stack || e) }, null, 2));
  console.error(e); process.exitCode = 1;
});
