#!/usr/bin/env python3
"""X6 local validation orchestrator: explicit PASS/FAIL/NOT_EXECUTED."""
import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKS = [
    ("manifest", [sys.executable, "tests/python/verify_manifest.py"], None),
    ("static_ui", [sys.executable, "tests/python/static_ui_preflight.py"], None),
    ("rational_python", [sys.executable, "tests/python/independent_audit.py"], None),
    ("julia", ["julia", "tests/julia/reference.jl"], "julia"),
    ("chromium_http", [sys.executable, "tests/browser/browser_http_test.py"], None),
]

def run_check(name, command, executable, timeout):
    if executable and not shutil.which(executable):
        return {"name": name, "status": "NOT_EXECUTED",
                "reason": f"Required executable unavailable: {executable}"}
    if name == "chromium_http":
        try:
            import playwright.sync_api
        except ImportError:
            return {"name": name, "status": "NOT_EXECUTED",
                    "reason": "Python Playwright package unavailable"}
    try:
        p = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                           timeout=timeout, check=False)
        return {"name": name, "status": "PASS" if p.returncode == 0 else "FAIL",
                "exit_code": p.returncode,
                "stdout": p.stdout[-30000:], "stderr": p.stderr[-30000:]}
    except subprocess.TimeoutExpired as e:
        return {"name": name, "status": "FAIL", "reason": f"Timed out after {timeout}s"}
    except OSError as e:
        return {"name": name, "status": "NOT_EXECUTED", "reason": str(e)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="x6-evidence/local_validation.json")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    if args.timeout < 1:
        parser.error("--timeout must be positive")
    output = ROOT / args.output
    if not output.resolve().is_relative_to(ROOT.resolve()):
        parser.error("output must be inside repository")
    results = [run_check(name, cmd, executable, args.timeout)
               for name, cmd, executable in CHECKS]
    statuses = [r["status"] for r in results]
    overall = ("FAIL" if "FAIL" in statuses else
               "INCOMPLETE" if "NOT_EXECUTED" in statuses else "PASS")
    report = {"schema": "x6-local-validation-1",
              "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "python": sys.version.split()[0],
              "overall": overall, "results": results}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"overall": overall,
                      "checks": {r["name"]: r["status"] for r in results},
                      "report": str(output.relative_to(ROOT))}, indent=2))
    return 0 if overall == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
