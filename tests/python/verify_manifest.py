#!/usr/bin/env python3
"""Verify tracked research-source hashes against the original archive manifest.

Only manifest entries present in the checkout are checked. Known intentionally
excluded files are reported, never silently treated as PASS.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "SHA256_REPOSITORY.json"
EXCLUDED = {
    ".github/workflows/validation.yml": "historical archived workflow omitted; separately installed CI differs",
    "docs/RELEASE_CHECKLIST.md": "updated release checklist; historical digest retained only as provenance",
    "README.md": "updated public preview and license disclosure; historical digest retained as provenance",
    "tests/python/python_results.local.json": "generated local test output; not part of published source checkout",
}

def main():
    doc = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if doc.get("algorithm") != "sha256" or not isinstance(doc.get("files"), dict):
        raise SystemExit("FAIL: malformed SHA-256 manifest")
    expected = doc["files"]
    integration_path = ROOT / "SAGNAC_SOURCE_MANIFEST.json"
    integration = json.loads(integration_path.read_text(encoding="utf-8")) if integration_path.exists() else None
    if integration is not None:
        if (integration.get("schema") != "x6.sagnac.source-manifest/1"
                or integration.get("base_app_sha256") != expected.get("app/index.html")
                or not isinstance(integration.get("files"), dict)
                or not {"app/index.html", "app/sagnac-core.js", "app/sagnac-ui.js",
                        "device/sagnac_bridge.py", "tests/python/verify_manifest.py"}
                       .issubset(integration.get("files", {}))):
            raise SystemExit("FAIL: malformed Sagnac integration manifest or incorrect baseline")
    # Isolated extensions have explicit inventories; do not weaken the unknown-file
    # check or change the app pin used by the bounded research agents.
    extension_specs = {
        "ACVM_OPTICAL_SOURCE_MANIFEST.json": (
            "x6.acvm-optical.source-manifest/1",
            {"experimental/acvm/engine.py", "experimental/acvm/archive.py",
             "experimental/acvm/devices.py", "experimental/acvm/feedback.py",
             "tests/acvm/test_acvm.py", "tests/acvm/qualify_checkout.py",
             "docs/acvm/optical-v0.2/README.md", ".github/workflows/x6-acvm-optical.yml"}),
        "CONTROL_CHANNEL_SOURCE_MANIFEST.json": (
            "x6.control-channel.source-manifest/1",
            {"experimental/control_channel/channel.py", "experimental/control_channel/reference.py",
             "experimental/control_channel/firmware/core.hpp", "experimental/control_channel/firmware/pico.cpp",
             "experimental/control_channel/qualification.py", "tests/control-channel/test_channel.py",
             "docs/acvm/control-channel-v0.1/README.md", ".github/workflows/x6-control-channel.yml"}),
        "INTEGRATION_SOURCE_MANIFEST.json": (
            "x6.integration.source-manifest/1",
            {"x6.py", "tools/workflow/cli.py", "tools/workflow/backends.py",
             "tools/workflow/signal_adapter.cjs", "tools/workflow/start.html",
             "tools/workflow/requirements-research.txt", "docs/INTEGRATION.md",
             "tests/integration/test_workflow.py", "tests/integration/qualify_checkout.py",
             "tests/integration/browser_workflow.cjs", ".gitignore"}),
        "EDGE_REFERENCE_SOURCE_MANIFEST.json": (
            "x6.edge-reference.source-manifest/1",
            {"experimental/edge_reference/runner.cjs", "experimental/edge_reference/test_runner.cjs",
             "docs/perspectives/edge-platform/README.md", ".github/workflows/x6-edge-reference.yml"}),
        "LICENSE_SOURCE_MANIFEST.json": (
            "x6.license.source-manifest/1",
            {"CITATION.cff", "CONTRIBUTING.md", "docs/LICENSE_OPTIONS.md", "LICENSE",
             "LICENSE_SCOPE.md", "NOTICE", "LICENSE_ACTIVATION_MANIFEST.json",
             "docs/LICENSE_ACTIVATION_2026-10-13.md"}),
        "EVIDENCE_CALIBRATION_SOURCE_MANIFEST.json": (
            "x6.evidence-calibration.source-manifest/1",
            {"experimental/evidence_calibration/core.py", "experimental/evidence_calibration/run_qualification.py",
             ".github/workflows/x6-experimental-evidence.yml"}),
        "SIGNAL_LAB_SOURCE_MANIFEST.json": (
            "x6.signal-lab.source-manifest/1",
            {"app/signal-lab.html", "app/signal-lab-core.js", "app/signal-lab-ui.js",
             "app/signal-lab-evidence.js", "app/signal-lab-build.js", "app/signal-lab.css",
             "tests/signal-lab/test_core.cjs", "tests/signal-lab/reference_validation.py",
             "tests/signal-lab/browser_test.cjs"}),
    }
    extensions = {}
    for name, (schema, required) in extension_specs.items():
        path = ROOT / name
        if not path.is_file():
            raise SystemExit("FAIL: missing extension manifest: " + name)
        ext = json.loads(path.read_text(encoding="utf-8"))
        if (ext.get("schema") != schema or ext.get("algorithm") != "sha256"
                or not isinstance(ext.get("files"), dict)
                or not required.issubset(ext["files"])
                or any(not isinstance(h, str) or not re.fullmatch(r"[0-9a-f]{64}", h)
                       for h in ext["files"].values())):
            raise SystemExit("FAIL: malformed extension manifest: " + name)
        extensions[name] = ext
    tracked = set(subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8").strip("\0").split("\0"))
    failed = []
    verified = 0
    excluded = []
    superseded = []
    for rel, digest in sorted(expected.items()):
        if rel == ".gitignore":
            superseded.append({"path": rel, "historical_sha256": digest,
                               "reason": "integration output directories; current bytes checked by INTEGRATION_SOURCE_MANIFEST.json"})
            continue
        if rel in EXCLUDED:
            excluded.append({"path": rel, "reason": EXCLUDED[rel]})
            continue
        if rel not in tracked:
            failed.append({"path": rel, "reason": "manifest file missing from checkout"})
            continue
        if rel in {"CITATION.cff", "CONTRIBUTING.md", "docs/LICENSE_OPTIONS.md"}:
            superseded.append({"path": rel, "historical_sha256": digest,
                               "reason": "authorised Apache-2.0 activation; current bytes checked by LICENSE_SOURCE_MANIFEST.json"})
            continue
        if rel == "app/index.html" and integration is not None:
            superseded.append({"path": rel, "historical_sha256": digest,
                               "reason": "Sagnac integration; current content checked by separate versioned manifest"})
            continue
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        if actual != digest:
            failed.append({"path": rel, "reason": "SHA-256 mismatch"})
        else:
            verified += 1
    # The manifest itself is deliberately not self-hashed.
    expected_tracked = set(expected) | {"agent/__init__.py", "agent/run_agent.py", "agent/requirements.txt", "tests/python/test_data_agent.py", "docs/DATA_AGENT.md", ".github/workflows/x6-data-agent.yml", "SHA256_REPOSITORY.json", ".github/workflows/unpack-x6.yml", "tests/python/verify_manifest.py", "docs/CI_VALIDATION_PLAN.md", "docs/M1_6_EXECUTION_REPORT.md", "tests/browser/browser_http_test.py", "docs/M1_7_VALIDATION_REPORT.md", "tests/python/static_ui_preflight.py", "docs/M1_9_BROWSER_AUDIT.md", "docs/M1_11_BROWSER_EXECUTION.md", "tests/python/run_validation.py", "docs/M1_12_VALIDATION_RUNNER.md", "tests/python/test_validation_runner.py", "docs/M1_13_RUNNER_AUDIT.md", "docs/M1_14_CI_SETUP.md", ".github/workflows/x6-validation.yml", "docs/M1_16_RELEASE_READINESS.md", "docs/APACHE_2_0_RIGHTS_CLEARANCE.md", "docs/M1_18_PROVENANCE_AUDIT.md", "docs/M1_19_COMPONENT_PROVENANCE.md", "docs/M1_20_DEPENDENCY_LICENSE_AUDIT.md", "docs/X6_OPEN_RESEARCH_AGENDA_DRAFT.md"}
    # The public portal predates the data agent and is not in the historical archive.
    expected_tracked |= {".nojekyll", "index.html"}
    # New automation sources have their own per-run hashes, not historical archive digests.
    expected_tracked |= {
        "agent/source_transport.py", "agent/measurement_sources.py", "agent/atlas_checks.py",
        "agent/run_sources.py", "agent/source-requirements.txt", "docs/SOURCE_AGENTS.md",
        "tests/python/test_source_agents.py", ".github/workflows/x6-source-agents.yml",
    }
    # Bounded mathematical-search sources carry their own per-run SHA-256 record.
    expected_tracked |= {
        "agent/run_math_agent.py", "agent/math_core_runner.cjs",
        "agent/math-agent-config.json", "agent/math-requirements.txt",
        "tests/python/test_math_agent.py", ".github/workflows/x6-math-agent.yml",
        "docs/MATH_AGENT.md", "docs/MATH_FORECAST_2026_10.md",
        "agent/lorentz_spectral.py", "tests/python/test_lorentz_spectral.py",
        "docs/LORENTZ_RESEARCH.md",
        "docs/AGENT_WINDOW_REPAIR_2026_10_13.md",
    }
    if integration is not None:
        expected_tracked |= set(integration['files']) | {'SAGNAC_SOURCE_MANIFEST.json'}
        for rel, digest in sorted(integration['files'].items()):
            candidate = ROOT / rel
            if Path(rel).is_absolute() or '..' in Path(rel).parts or rel not in tracked or not candidate.is_file():
                failed.append({'path': rel, 'reason': 'integration manifest path missing or invalid'})
            elif hashlib.sha256(candidate.read_bytes()).hexdigest() != digest:
                failed.append({'path': rel, 'reason': 'integration SHA-256 mismatch'})
            else:
                verified += 1
    for name, ext in extensions.items():
        expected_tracked |= set(ext["files"]) | {name}
        for rel, digest in sorted(ext["files"].items()):
            candidate = ROOT / rel
            if (Path(rel).is_absolute() or ".." in Path(rel).parts
                    or rel not in tracked or not candidate.is_file() or candidate.is_symlink()):
                failed.append({"path": rel, "reason": "extension manifest path missing or invalid"})
            elif hashlib.sha256(candidate.read_bytes()).hexdigest() != digest:
                failed.append({"path": rel, "reason": "extension SHA-256 mismatch"})
            else:
                verified += 1
    unlisted = sorted(tracked - expected_tracked)
    result = {
        "status": "FAIL" if failed or unlisted else "PASS_WITH_EXCLUSIONS",
        "verified": verified,
        "excluded": excluded,
        "superseded": superseded,
        "failed": failed,
        "unlisted_tracked": unlisted,
    }
    print(json.dumps(result, indent=2))
    if failed or unlisted:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
