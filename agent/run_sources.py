#!/usr/bin/env python3
"""Run one bounded source-specific historical benchmark against the actual X6 app."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.run_agent import ROOT, browser_run, require, stamp, write_json
from agent.source_transport import sha256


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=["atlas", "qutech", "nasa"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path, default=ROOT/".agent-cache")
    args = parser.parse_args(argv)
    out = args.output.resolve()
    require(not out.exists() or not any(out.iterdir()), "Output must be empty")
    out.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    report = {"schema": "x6-source-agent-1", "source": args.source, "status": "NOT_EXECUTED",
              "started_at": stamp(), "mode": "FIXED_BENCHMARK", "physical_validation": "NOT_CLAIMED",
              "denoising_improvement": "NOT_EVALUATED_WITH_CLEAN_REFERENCE",
              "runtime": {"python": platform.python_version()},
              "provenance": {"app_sha256": sha256(ROOT/"app/index.html"),
                             "agent_files_sha256": {p.name: sha256(p) for p in sorted((ROOT/"agent").glob("*.py"))}},
              "windows": [], "limits": ["Historical data, not new live measurements",
                 "Imported SNR uses a moving-average proxy; it is not a clean-reference accuracy metric",
                 "Signal-to-graph mapping is a model; certificate covers only its rounded rational graph",
                 "No health classification, qubit-state classification, coherence improvement or external peer review claimed"]}
    try:
        report["provenance"]["git_commit"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        report["provenance"]["tracked_working_tree_dirty"] = bool(subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT, text=True).strip())
        for package in ["numpy", "networkx", "h5py", "playwright", "py7zr", "libarchive-c"]:
            report["runtime"][package] = importlib.metadata.version(package)
        if args.source == "atlas":
            from agent.atlas_checks import run_atlas
            report["atlas"] = run_atlas(out)
            require(report["atlas"]["status"] == "PASS", "Graph Atlas checks failed")
        else:
            from agent.measurement_sources import fetch_nasa, fetch_qutech
            fetcher = fetch_nasa if args.source == "nasa" else fetch_qutech
            meta, windows = fetcher(out, args.cache_dir.resolve())
            report["source_metadata"] = meta
            report["expected_windows"] = len(windows)
            require(len(windows) == 3, "Expected three fixed windows")
            for prepared in windows:
                folder = out/prepared["name"]
                folder.mkdir()
                write_json(folder/"selected_samples.json", prepared)
                (folder/"signal.csv").write_text("value\n" + "\n".join(repr(v) for v in prepared["values"]) + "\n")
                result = browser_run(folder, prepared)
                report["windows"].append({"name": prepared["name"], "status": result["status"],
                                           "sample_count": len(prepared["values"]), "error": result.get("error")})
                print(f"{args.source}/{prepared['name']}: {result['status']}", flush=True)
            require(all(w["status"] == "PASS" for w in report["windows"]), "One or more browser windows failed")
        report["status"] = "PASS"
    except Exception as exc:
        report["status"] = "FAIL"
        report["error"] = f"{type(exc).__name__}: {exc}"
    report["finished_at"] = stamp()
    report["elapsed_seconds"] = round(time.monotonic()-started, 3)
    write_json(out/"report.json", report)
    summary = (f"# X6 {args.source} agent: {report['status']}\n\n"
               f"Historical benchmark. Started {report['started_at']}. Duration {report['elapsed_seconds']} s.\n\n")
    if "atlas" in report:
        summary += "Graph counts: `" + json.dumps(report["atlas"]["counts"]) + "`\n\n"
    for window in report["windows"]:
        summary += f"- {window['name']}: **{window['status']}** ({window['sample_count']} samples)\n"
    summary += "\nPASS means source, application and mathematical checks passed; it does not demonstrate improved denoising or physical performance.\n"
    if report.get("error"):
        summary += "\nFailure: " + report["error"] + "\n"
    (out/"summary.md").write_text(summary)
    files = {str(p.relative_to(out)): sha256(p) for p in sorted(out.rglob("*"))
             if p.is_file() and p.name != "SHA256.json"}
    write_json(out/"SHA256.json", {"algorithm": "sha256", "files": files})
    print(summary)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
