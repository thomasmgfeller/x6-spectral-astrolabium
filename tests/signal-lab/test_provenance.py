"""Regression tests for the fixed baseline and fail-before-read archive guards.

Manipulations are in memory: these tests never edit protected research files,
replace repository manifests, create symlinks, or run the research agents.
"""
from __future__ import annotations

from contextlib import ExitStack, redirect_stdout
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
REVIEWED_MAP_SHA256 = "6d38206180efb5acb6c7e377878c67e9e5df8f079b2a77b20891b2f6711a1f61"


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BUILD = load_module("x6_signal_build_provenance_test", "tools/build_signal_lab.py")
QUALIFY = load_module("x6_signal_qualify_provenance_test", "tests/signal-lab/qualify.py")
VERIFY = load_module("x6_manifest_provenance_test", "tests/python/verify_manifest.py")


class SourceProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "SIGNAL_LAB_SOURCE_MANIFEST.json").read_text())

    def baseline(self):
        return json.loads(json.dumps(self.manifest))

    def reject_baseline_without_reads(self, candidate):
        # A forged inventory must fail against the fixed inventory digest before
        # it can turn an attacker-chosen path into a protected-file read.
        with patch.object(Path, "read_bytes", side_effect=AssertionError("Unreviewed baseline reached file reads")):
            with self.assertRaises(ValueError):
                BUILD.protected_baseline(candidate, True)

    def test_complete_reviewed_baseline_and_current_bytes_pass(self):
        protected = BUILD.protected_baseline(self.baseline(), True)
        canonical = json.dumps(protected, sort_keys=True, ensure_ascii=False,
                               separators=(",", ":"), allow_nan=False).encode()
        self.assertEqual(hashlib.sha256(canonical).hexdigest(), REVIEWED_MAP_SHA256)
        self.assertEqual(len(protected), 17)
        self.assertIn("agent/run_math_agent.py", protected)
        self.assertIn(".github/workflows/x6-source-agents.yml", protected)

    def test_old_app_plus_eleven_documents_bypass_is_rejected(self):
        candidate = self.baseline()
        paths = [ROOT / "app/index.html"] + sorted((ROOT / "docs").glob("*.md"))[:11]
        candidate["protected_research"] = {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths
        }
        self.assertEqual(len(candidate["protected_research"]), 12)
        self.reject_baseline_without_reads(candidate)

    def test_dropping_a_protected_agent_is_rejected(self):
        candidate = self.baseline()
        del candidate["protected_research"]["agent/run_math_agent.py"]
        self.reject_baseline_without_reads(candidate)

    def test_original_baseline_cannot_be_rewritten_by_amendment(self):
        candidate = self.baseline()
        candidate["protected_research_baseline"]["agent/run_math_agent.py"] = "0" * 64
        self.reject_baseline_without_reads(candidate)

    def test_old_pre_repair_inventory_is_not_current_evidence(self):
        candidate = self.baseline()
        candidate["protected_research"] = candidate["protected_research_baseline"].copy()
        self.reject_baseline_without_reads(candidate)

    def test_superseded_licensing_documents_still_reject_changed_bytes(self):
        original = Path.read_bytes
        for name in ["CITATION.cff", "CONTRIBUTING.md", "docs/LICENSE_OPTIONS.md", "LICENSE"]:
            target = ROOT / name
            def changed(path):
                data = original(path)
                return data + b"tamper" if path == target else data
            stream = io.StringIO()
            with self.subTest(path=name), patch.object(Path, "read_bytes", changed), redirect_stdout(stream):
                with self.assertRaises(SystemExit) as result:
                    VERIFY.main()
                self.assertEqual(result.exception.code, 1)
            report = json.loads(stream.getvalue())
            self.assertIn({"path": name, "reason": "extension SHA-256 mismatch"}, report["failed"])

    def test_rehashing_a_changed_agent_cannot_refresh_the_baseline(self):
        candidate = self.baseline()
        candidate["protected_research"]["agent/run_math_agent.py"] = "0" * 64
        self.reject_baseline_without_reads(candidate)

    def test_same_cardinality_replacement_is_rejected(self):
        candidate = self.baseline()
        del candidate["protected_research"]["agent/run_math_agent.py"]
        candidate["protected_research"]["README.md"] = hashlib.sha256((ROOT / "README.md").read_bytes()).hexdigest()
        self.assertEqual(len(candidate["protected_research"]), 17)
        self.reject_baseline_without_reads(candidate)

    def test_changed_base_commit_is_rejected(self):
        candidate = self.baseline()
        candidate["base_commit"] = "0" * 40
        self.reject_baseline_without_reads(candidate)

    def test_unmodified_manifest_detects_changed_protected_bytes(self):
        original = Path.read_bytes
        target = ROOT / "agent/run_math_agent.py"

        def changed_bytes(path):
            data = original(path)
            return data + b"\n# virtual mutation\n" if path == target else data

        with patch.object(Path, "read_bytes", changed_bytes):
            with self.assertRaisesRegex(ValueError, "protected research source changed"):
                BUILD.protected_baseline(self.baseline(), True)

    def test_protected_file_symlink_is_rejected(self):
        original = Path.is_symlink
        target = ROOT / "app/index.html"
        with patch.object(Path, "is_symlink", lambda p: p == target or original(p)):
            with self.assertRaisesRegex(ValueError, "protected research source changed"):
                BUILD.protected_baseline(self.baseline(), True)

    def test_expected_runtime_and_executed_verifier_paths_are_allowed(self):
        names = ["app/signal-lab-core.js", "app/signal-lab-evidence.js", "tools/build_signal_lab.py",
                 "SIGNAL_LAB_SOURCE_MANIFEST.json", "tests/python/verify_manifest.py", "SHA256_REPOSITORY.json",
                 "agent/math-agent-config.json", "docs/SIGNAL_LAB_METHODS.md"]
        for name in names:
            with self.subTest(name=name):
                self.assertEqual(QUALIFY.source_path(name), ROOT / name)

    def test_traversal_absolute_alias_and_unexpected_paths_are_rejected(self):
        names = ["../outside.txt", "../../app/index.html", "/etc/passwd", "app/../index.html",
                 "./app/signal-lab-core.js", "app//signal-lab-core.js", "app\\signal-lab-core.js",
                 "agent/run_math_agent.py", "tests/python/unknown.py", "docs/README.md", "", None, 3]
        for name in names:
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    QUALIFY.source_path(name)

    def test_source_symlink_and_parent_escape_are_rejected(self):
        target = ROOT / "app/signal-lab-core.js"
        original_link, original_resolve = Path.is_symlink, Path.resolve
        with patch.object(Path, "is_symlink", lambda p: p == target or original_link(p)):
            with self.assertRaises(ValueError):
                QUALIFY.source_path("app/signal-lab-core.js")
        # Simulate a symlinked ancestor escaping the root without creating one.
        with patch.object(Path, "resolve", lambda p, *a, **kw:
                          Path("/outside/signal-lab-core.js") if p == target else original_resolve(p, *a, **kw)):
            with self.assertRaises(ValueError):
                QUALIFY.source_path("app/signal-lab-core.js")

    def virtual_main(self, extra_patches):
        """Run only the qualification guard path, without creating an archive."""
        with ExitStack() as stack:
            stack.enter_context(patch.object(sys, "argv", ["qualify.py", "--output", "/tmp/x6-provenance-virtual-probe"]))
            stack.enter_context(patch.object(Path, "mkdir", return_value=None))
            stack.enter_context(patch.object(Path, "write_text", return_value=0))
            writes = stack.enter_context(patch.object(Path, "write_bytes", return_value=0))
            stack.enter_context(patch.object(Path, "rglob", return_value=[]))
            stack.enter_context(patch.object(QUALIFY, "git", return_value=None))
            stack.enter_context(patch.object(QUALIFY.platform, "platform", return_value="virtual-test-platform"))
            command = stack.enter_context(patch.object(QUALIFY.subprocess, "run",
                                                       side_effect=AssertionError("Commands ran before inventory validation")))
            for manager in extra_patches:
                stack.enter_context(manager)
            with redirect_stdout(io.StringIO()):
                status = QUALIFY.main()
            self.assertEqual(status, 1)
            command.assert_not_called()
            writes.assert_not_called()

    def test_initial_manifest_is_guarded_before_its_first_read(self):
        attempted = []

        def abort_first_path(name):
            attempted.append(name)
            raise ValueError("virtual source guard stop")

        with patch.object(Path, "read_text", side_effect=AssertionError("Manifest read before source guard")) as reads:
            self.virtual_main([patch.object(QUALIFY, "source_path", side_effect=abort_first_path)])
            reads.assert_not_called()
        self.assertEqual(attempted, ["SIGNAL_LAB_SOURCE_MANIFEST.json"])

    def test_invalid_inventory_cannot_read_or_archive_source_bytes(self):
        candidate = self.baseline()
        candidate["files"]["../../outside.txt"] = "0" * 64
        original_read = Path.read_text

        def manifest_text(path, *args, **kwargs):
            if path == ROOT / "SIGNAL_LAB_SOURCE_MANIFEST.json":
                return json.dumps(candidate)
            return original_read(path, *args, **kwargs)

        with patch.object(Path, "read_bytes", side_effect=AssertionError("Inventory bytes read before all paths were validated")) as reads:
            self.virtual_main([patch.object(Path, "read_text", manifest_text)])
            reads.assert_not_called()


if __name__ == "__main__":
    unittest.main()
