"""Run: python -m pip install playwright; python -m playwright install chromium; python browser_test.py"""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from functools import partial
from playwright.sync_api import sync_playwright
p=(Path(__file__).resolve().parents[2] / 'app' / 'index.html').resolve()
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(p.parent)))
Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None,args=['--no-sandbox'])
    page=browser.new_page(accept_downloads=True)
    errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.set_content(p.read_text(encoding='utf-8'),wait_until='domcontentloaded',timeout=30000)
    assert page.locator('#tab-signal').count()==1
    assert page.locator('#tab-spectrum').count()==1
    assert page.locator('#tab-audit').count()==1
    page.locator('#tab-audit').click()
    page.locator('#run39').click()
    page.wait_for_function("JSON.parse(document.querySelector('#out39').textContent).total > 0",timeout=20000)
    import json
    report=json.loads(page.locator('#out39').inner_text())
    print(json.dumps({'passed':report['passed'],'total':report['total'],'errors':errors},indent=2))
    assert report['allPassed'] and not errors
    browser.close()

server.shutdown()
