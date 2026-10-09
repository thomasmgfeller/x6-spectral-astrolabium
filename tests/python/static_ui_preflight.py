"""Static structural preflight for the X6 v4.2 RC qualification UI.

Not a substitute for executing JavaScript or testing iframe messaging.
"""
from pathlib import Path
import json
import re

APP = Path(__file__).resolve().parents[2] / "app" / "index.html"
REQUIRED_IDS = [
    "signalFrame", "spectrumFrame", "ack34", "samples34", "sigma34",
    "digits34", "modelRun34", "modelOut34", "tab-audit", "run39", "out39",
]

def run():
    html = APP.read_text(encoding="utf-8")
    checks = {}
    for element_id in REQUIRED_IDS:
        checks["id:" + element_id] = len(re.findall(
            r'\bid\s*=\s*["\']' + re.escape(element_id) + r'["\']', html)) == 1
    checks["bridge-schema-present"] = "x6-cert-bridge-1" in html
    checks["certify-message-present"] = bool(re.search(r"action\s*:\s*['\"]CERTIFY['\"]", html))
    checks["qualification-report-schema-present"] = "x6-qualification-1" in html
    checks["two-iframe-tags"] = len(re.findall(r"<iframe\b", html, re.I)) == 2
    report = {
        "schema": "x6-m1-9-static-preflight-1",
        "scope": "static HTML structure only; not a browser execution",
        "passed": sum(checks.values()),
        "total": len(checks),
        "checks": checks,
        "status": "PASS" if all(checks.values()) else "FAIL",
    }
    print(json.dumps(report, indent=2))
    if report["status"] != "PASS":
        raise SystemExit(1)

if __name__ == "__main__":
    run()
