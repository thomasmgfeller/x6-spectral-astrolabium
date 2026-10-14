"""Bounded, reproducible software qualification; no scheduled research run."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    records = []
    def run(name, command, expected=0):
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=120)
        log = result.stdout+result.stderr
        (args.output/(name+".txt")).write_text(log)
        record = {"name": name, "expected_exit_code": expected, "observed_exit_code": result.returncode,
                  "status": "PASS" if result.returncode == expected else "FAIL",
                  "log_sha256": hashlib.sha256(log.encode()).hexdigest()}
        records.append(record)
        print(name+": "+record["status"], flush=True)
        return result
    run("lorentz_and_agent_regression", [sys.executable, "-m", "unittest",
        "tests/python/test_lorentz_n6.py", "tests/python/test_lorentz_spectral.py",
        "tests/python/test_math_agent.py", "-v"])
    run("v1_contract", [sys.executable, "-m", "unittest", "discover", "-s", "experiments/industrial-v1/tests", "-v"])
    run("signal_lab_provenance", [sys.executable, "tests/signal-lab/test_provenance.py", "-v"])
    run("signal_lab_inventory", [sys.executable, "tools/build_signal_lab.py", "--check"])
    run("edge_reference", ["node", "--test", "experimental/edge_reference/test_runner.cjs"])
    run("v1_real_readiness", [sys.executable, "experiments/industrial-v1/evaluate.py",
        "experiments/industrial-v1/V1_PROFILE_DRAFT.json", "--root", "experiments/industrial-v1",
        "--output", str((args.output/"v1_real_readiness.json").resolve())], 3)
    with tempfile.TemporaryDirectory(prefix="x6-v1-control-") as temp:
        run("control_generation", [sys.executable, "experiments/industrial-v1/make_control.py", temp])
        run("v1_control_assessment", [sys.executable, "experiments/industrial-v1/evaluate.py",
            temp+"/profile.json", "--root", temp, "--inputs", temp+"/inputs.json",
            "--result", temp+"/result.json", "--output", str((args.output/"v1_control_assessment.json").resolve())], 4)
    report = {"schema": "x6.workpackages.qualification/1",
              "status": "SOFTWARE_QUALIFICATION_PASS" if all(r["status"] == "PASS" for r in records) else "FAIL",
              "physical_validation": "NOT_PERFORMED", "v1_real_profile": "NOT_READY",
              "python": platform.python_version(),
              "dependencies": {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "jsonschema")},
              "qualifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "checks": records}
    (args.output/"qualification.json").write_text(json.dumps(report, indent=2)+"\n")
    return 0 if report["status"] == "SOFTWARE_QUALIFICATION_PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
