#!/usr/bin/env python3
"""Run bounded software checks and archive the actual source snapshot and logs.

No hardware, user data, source-agent fetching or scheduled research execution.
Install the declared NumPy/SciPy and Playwright test dependencies first.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]


def source_path(name):
    """Reject unexpected inventory paths before reading/archiving any bytes."""
    exact = {"SIGNAL_LAB_SOURCE_MANIFEST.json", "SAGNAC_SOURCE_MANIFEST.json",
             "EVIDENCE_CALIBRATION_SOURCE_MANIFEST.json", "app/index.html",
             "tests/python/verify_manifest.py", "SHA256_REPOSITORY.json", "index.html", "README.md",
             "agent/math-agent-config.json", "tools/build_signal_lab.py",
             ".github/workflows/x6-signal-lab.yml", "docs/SIGNAL_VALIDATION_LAB.md"}
    if not isinstance(name, str):
        raise ValueError("source path must be a string")
    rel = Path(name)
    allowed = (name in exact or bool(re.fullmatch(r"app/signal-lab(?:-[a-z]+)?\.(?:html|css|js)", name))
               or bool(re.fullmatch(r"tests/signal-lab/[A-Za-z_][A-Za-z0-9_-]*\.(?:py|cjs|txt)", name))
               or bool(re.fullmatch(r"docs/SIGNAL_LAB[A-Z_]*\.md", name)))
    candidate = ROOT / rel
    if (not allowed or rel.is_absolute() or ".." in rel.parts or rel.as_posix() != name
            or candidate.is_symlink() or not candidate.is_file()
            or ROOT not in candidate.resolve().parents):
        raise ValueError("unexpected or unsafe source inventory path: " + name)
    return candidate


def digest(value):
    return hashlib.sha256(value).hexdigest()


def git(*args):
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL, timeout=10).strip()
    except (OSError, subprocess.SubprocessError):
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="new directory; existing evidence is never overwritten")
    args = parser.parse_args()
    output = args.output.resolve()
    if output == ROOT or output in ROOT.parents or any(output == ROOT / p or ROOT / p in output.parents for p in ["app", "agent", "tests", "tools", "docs", "experimental"]):
        raise ValueError("choose an evidence output directory outside source directories")
    output.mkdir(parents=True, exist_ok=False)
    (output / "logs").mkdir()
    report = {"schema": "x6.signal-lab.qualification/1", "status": "ERROR",
              "created_utc": datetime.now(timezone.utc).isoformat(),
              "git_commit": git("rev-parse", "HEAD"), "git_tree": git("rev-parse", "HEAD^{tree}"),
              "git_worktree_status_at_start": git("status", "--short"),
              "environment": {"python": sys.version, "platform": platform.platform()},
              "github_run_id": os.environ.get("GITHUB_RUN_ID"), "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
              "physical_validation": "NOT_PERFORMED", "research_agents_executed": False,
              "steps": [], "sources": {}, "protected_research": {},
              "limitations": ["Fixed synthetic software fixtures, not a general performance guarantee.",
                              "SHA-256 records content only; source snapshots and timestamps are not authenticated.",
                              "CI artifacts have finite retention and are not immutable long-term archives."]}
    snapshots = {}
    try:
        manifest = json.loads(source_path("SIGNAL_LAB_SOURCE_MANIFEST.json").read_text())
        paths = sorted(set(manifest["files"]) | {"SIGNAL_LAB_SOURCE_MANIFEST.json", "SAGNAC_SOURCE_MANIFEST.json",
                       "EVIDENCE_CALIBRATION_SOURCE_MANIFEST.json", "app/index.html", "agent/math-agent-config.json",
                       "tests/python/verify_manifest.py", "SHA256_REPOSITORY.json", "index.html", "README.md"})
        checked_paths = {name: source_path(name) for name in paths}
        snapshots = {name: path.read_bytes() for name, path in checked_paths.items()}
        report["sources"] = {name: digest(value) for name, value in snapshots.items()}
        report["protected_research"] = manifest["protected_research"]
        commands = [
            ("build", [sys.executable, "tools/build_signal_lab.py", "--check"], 30),
            ("repository_integrity", [sys.executable, "tests/python/verify_manifest.py"], 30),
            ("core", ["node", "tests/signal-lab/test_core.cjs"], 90),
            ("evidence", ["node", "tests/signal-lab/test_evidence.cjs"], 90),
            ("provenance", [sys.executable, "-m", "unittest", "discover", "-s", "tests/signal-lab", "-p", "test_provenance.py", "-v"], 30),
            ("independent_reference", [sys.executable, "tests/signal-lab/reference_validation.py", "--report", str(output / "reference.json")], 120),
            ("browser", ["node", "tests/signal-lab/browser_test.cjs"], 180),
        ]
        environment = dict(os.environ, X6_EVIDENCE_DIR=str(output / "browser"))
        for name, command, timeout in commands:
            stdout, stderr = output / "logs" / (name + ".stdout.log"), output / "logs" / (name + ".stderr.log")
            with stdout.open("wb") as out, stderr.open("wb") as err:
                try:
                    result = subprocess.run(command, cwd=ROOT, env=environment, stdout=out, stderr=err, timeout=timeout, check=False)
                    code, error = result.returncode, None
                except (OSError, subprocess.TimeoutExpired) as exc:
                    code, error = -1, str(exc)
            step = {"name": name, "command": command, "exit_code": code, "status": "PASS" if code == 0 else "FAIL"}
            if error:
                step["error"] = error
            try:
                detail = json.loads(stdout.read_text())
                step["details"] = {key: detail[key] for key in ["status", "passed", "total", "browser_version", "versions", "protected_research_files"] if key in detail}
            except (ValueError, OSError):
                count = re.search(r"^# tests (\d+)$", stdout.read_text(), re.MULTILINE)
                passed = re.search(r"^# pass (\d+)$", stdout.read_text(), re.MULTILINE)
                if count and passed:
                    step["details"] = {"total": int(count[1]), "passed": int(passed[1])}
            report["steps"].append(step)
            print(name + ": " + step["status"], flush=True)
            # Integrity failures block execution; numerical failures are collected
            # alongside the other independent test classes for diagnosis.
            if code != 0 and name in ["build", "repository_integrity"]:
                raise ValueError(name + " failed; refusing qualification with inconsistent sources")
        if any((ROOT / name).read_bytes() != data for name, data in snapshots.items()):
            raise ValueError("source changed during qualification")
        for name, expected in manifest["protected_research"].items():
            if digest((ROOT / name).read_bytes()) != expected:
                raise ValueError("protected research source changed: " + name)
        report["status"] = "SOFTWARE_TESTS_PASS" if all(step["exit_code"] == 0 for step in report["steps"]) else "SOFTWARE_TESTS_FAIL"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    finally:
        for name, data in snapshots.items():
            destination = output / "source_snapshot" / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        (output / "report.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
        inventory = {str(path.relative_to(output)): digest(path.read_bytes()) for path in sorted(output.rglob("*")) if path.is_file()}
        (output / "SHA256.json").write_text(json.dumps(inventory, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "output": str(output), "steps": report["steps"], "error": report.get("error")}, indent=2))
    return 0 if report["status"] == "SOFTWARE_TESTS_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
