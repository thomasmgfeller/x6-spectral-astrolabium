"""HTTP-origin Chromium smoke test for the X6 qualification gate.

Run from repository root:
    python -m pip install -r requirements-test.txt
    python -m playwright install chromium
    python tests/browser/browser_http_test.py
"""
import json
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

APP_DIR = Path(__file__).resolve().parents[2] / "app"
APP = APP_DIR / "index.html"


def main():
    if not APP.is_file():
        raise SystemExit("NOT_EXECUTED: app/index.html missing")
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0),
        partial(SimpleHTTPRequestHandler, directory=str(APP_DIR)),
    )
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        with sync_playwright() as pw:
            system_chromium = Path('/usr/bin/chromium')
            launch = {'headless': True}
            if system_chromium.exists():
                launch['executable_path'] = str(system_chromium)
                launch['args'] = ['--no-sandbox']
            browser = pw.chromium.launch(**launch)
            try:
                page = browser.new_page(accept_downloads=True)
                errors = []
                page.on("pageerror", lambda exc: errors.append(str(exc)))
                url = f"http://127.0.0.1:{server.server_port}/index.html"
                response = page.goto(url, wait_until="load", timeout=30000)
                assert response is not None and response.status == 200, "HTTP load failed"
                for selector in ("#tab-signal", "#tab-spectrum", "#tab-audit"):
                    assert page.locator(selector).count() == 1, selector
                # The iframe is sandboxed without allow-same-origin.
                # Parent-page contentDocument is therefore inaccessible.
                # Playwright can still wait inside the child frame.
                page.frame_locator("#spectrumFrame").locator("body").wait_for(
                    state="attached", timeout=20000
                )
                page.locator("#tab-audit").click()
                page.locator("#run39").click()
                page.wait_for_function(
                    """() => {
                      const e = document.querySelector('#out39');
                      if (!e) return false;
                      try { return JSON.parse(e.textContent).total > 0; }
                      catch (_) { return false; }
                    }""",
                    timeout=20000,
                )
                report = json.loads(page.locator("#out39").inner_text())
                summary = {
                    "status": "PASS" if report.get("allPassed") and not errors else "FAIL",
                    "passed": report.get("passed"),
                    "total": report.get("total"),
                    "page_errors": errors,
                    "origin": "http://127.0.0.1:<ephemeral>/index.html",
                }
                print(json.dumps(summary, indent=2))
                evidence_dir = os.environ.get("X6_EVIDENCE_DIR")
                if evidence_dir:
                    output = Path(evidence_dir)
                    output.mkdir(parents=True, exist_ok=True)
                    (output / "browser_http_summary.json").write_text(
                        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
                    )
                    (output / "qualification39.json").write_text(
                        json.dumps(report, indent=2) + "\n", encoding="utf-8"
                    )
                assert summary["status"] == "PASS", "Qualification gate failed"
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)


if __name__ == "__main__":
    main()
