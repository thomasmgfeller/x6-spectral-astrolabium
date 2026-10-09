#!/usr/bin/env python3
"""Verify tracked research-source hashes against the original archive manifest.

Only manifest entries present in the checkout are checked. Known intentionally
excluded files are reported, never silently treated as PASS.
"""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "SHA256_REPOSITORY.json"
EXCLUDED = {
    ".github/workflows/validation.yml": "requires separately authorized workflow review",
    "tests/python/python_results.local.json": "generated local test output",
}

def main():
    doc = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if doc.get("algorithm") != "sha256" or not isinstance(doc.get("files"), dict):
        raise SystemExit("FAIL: malformed SHA-256 manifest")
    expected = doc["files"]
    tracked = set(subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8").strip("\0").split("\0"))
    failed = []
    verified = 0
    excluded = []
    for rel, digest in sorted(expected.items()):
        if rel in EXCLUDED and rel not in tracked:
            excluded.append({"path": rel, "reason": EXCLUDED[rel]})
            continue
        if rel not in tracked:
            failed.append({"path": rel, "reason": "manifest file missing from checkout"})
            continue
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        if actual != digest:
            failed.append({"path": rel, "reason": "SHA-256 mismatch"})
        else:
            verified += 1
    # The manifest itself is deliberately not self-hashed.
    expected_tracked = set(expected) | {"SHA256_REPOSITORY.json", ".github/workflows/unpack-x6.yml", "tests/python/verify_manifest.py", "docs/CI_VALIDATION_PLAN.md", "docs/M1_6_EXECUTION_REPORT.md", "tests/browser/browser_http_test.py", "docs/M1_7_VALIDATION_REPORT.md", "tests/python/static_ui_preflight.py", "docs/M1_9_BROWSER_AUDIT.md"}
    unlisted = sorted(tracked - expected_tracked)
    result = {
        "status": "FAIL" if failed or unlisted else "PASS_WITH_EXCLUSIONS",
        "verified": verified,
        "excluded": excluded,
        "failed": failed,
        "unlisted_tracked": unlisted,
    }
    print(json.dumps(result, indent=2))
    if failed or unlisted:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
