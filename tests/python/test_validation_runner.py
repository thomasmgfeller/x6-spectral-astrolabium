"""Unit tests for X6 runner status semantics, independent of X6 app/runtime."""
import importlib.util
import sys
import unittest
from pathlib import Path

RUNNER = Path(__file__).with_name("run_validation.py")
spec = importlib.util.spec_from_file_location("x6_validation_runner", RUNNER)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

class RunnerStatusTests(unittest.TestCase):
    def test_success(self):
        r = runner.run_check("probe", [sys.executable, "-c", "print('ok')"], None, 5)
        self.assertEqual(r["status"], "PASS")
        self.assertEqual(r["exit_code"], 0)

    def test_failure(self):
        r = runner.run_check("probe", [sys.executable, "-c", "raise SystemExit(3)"], None, 5)
        self.assertEqual(r["status"], "FAIL")
        self.assertEqual(r["exit_code"], 3)

    def test_missing_runtime(self):
        r = runner.run_check("julia", ["missing-x6-runtime"], "missing-x6-runtime", 5)
        self.assertEqual(r["status"], "NOT_EXECUTED")

    def test_timeout(self):
        r = runner.run_check("probe", [sys.executable, "-c", "import time;time.sleep(3)"], None, 1)
        self.assertEqual(r["status"], "FAIL")

    def test_missing_command_without_runtime_hint(self):
        r = runner.run_check("probe", ["x6-nonexistent-executable-2026"], None, 5)
        self.assertEqual(r["status"], "NOT_EXECUTED")
        self.assertIn("reason", r)

if __name__ == "__main__":
    unittest.main()
