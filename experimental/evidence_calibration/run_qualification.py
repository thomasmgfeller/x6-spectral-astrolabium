"""Bounded, reproducible software qualification with archived sources and logs.

No hardware, no data-source fetching, no research-agent execution.
"""
import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import unittest
from pathlib import Path
from .test_independent_oracles import check_oracles

ROOT = Path(__file__).resolve().parents[2]
MODULE = Path(__file__).resolve().parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git_value(*args):
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True,
                                       stderr=subprocess.DEVNULL, timeout=10).strip()
    except (OSError, subprocess.SubprocessError):
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--protect-research", action="store_true")
    args = parser.parse_args()
    output = args.output.resolve()
    if output == ROOT or output == MODULE or MODULE in output.parents:
        raise ValueError("evidence output must be outside the source module")
    output.mkdir(parents=True, exist_ok=False)
    files = sorted(p for p in MODULE.iterdir() if p.suffix in (".py", ".md"))
    snapshots = {str(p.relative_to(ROOT)): p.read_bytes() for p in files}
    report = {"schema": "x6-software-qualification-v1", "status": "ERROR",
              "physical_validation": "NOT_PERFORMED", "research_agents_executed": False,
              "measurement_release": "BLOCKED_PENDING_PHYSICAL_VALIDATION",
              "git_commit": git_value("rev-parse", "HEAD"),
              "git_tree": git_value("rev-parse", "HEAD^{tree}"),
              "github_run_id": os.environ.get("GITHUB_RUN_ID"),
              "environment": {"python": sys.version, "platform": platform.platform()},
              "protected_app_check": "NOT_REQUESTED",
              "sources": {name: digest(data) for name, data in snapshots.items()}}
    ok = False
    try:
        suite = unittest.defaultTestLoader.discover(str(MODULE), top_level_dir=str(ROOT))
        with (output / "tests.log").open("w", encoding="utf-8") as stream:
            result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
        report["tests"] = {"run": result.testsRun, "failures": len(result.failures),
                           "errors": len(result.errors), "skipped": len(result.skipped)}
        if result.testsRun < 47 or not result.wasSuccessful() or result.skipped:
            raise ValueError("test acceptance failed or tests unexpectedly missing/skipped")
        report["independent_oracles"] = check_oracles()
        if args.protect_research:
            config_bytes = (ROOT / "agent/math-agent-config.json").read_bytes()
            config = json.loads(config_bytes)
            app_hash = digest((ROOT / "app/index.html").read_bytes())
            if app_hash != config["app_sha256"]:
                raise ValueError("pinned app mismatch; never rewrite reference automatically")
            report["protected_app_check"] = "PASS"
            report["app_sha256"] = app_hash
            report["agent_config_sha256"] = digest(config_bytes)
            report["agent_stop_utc"] = config["stop_utc"]
        if any((ROOT / name).read_bytes() != data for name, data in snapshots.items()):
            raise ValueError("source changed during qualification")
        report["status"] = "SOFTWARE_TESTS_PASS"
        ok = True
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    finally:
        for name, data in snapshots.items():
            p = output / "source_snapshot" / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        workflow = ROOT / ".github/workflows/x6-experimental-evidence.yml"
        if workflow.is_file():
            (output / "workflow.yml").write_bytes(workflow.read_bytes())
        (output / "report.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        manifest = {str(p.relative_to(output)): digest(p.read_bytes())
                    for p in sorted(output.rglob("*")) if p.is_file()}
        (output / "SHA256.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, allow_nan=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
