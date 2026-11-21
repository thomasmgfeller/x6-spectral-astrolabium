"""Run the complete offline core, optionally adding the high-precision quadrature."""
import argparse
import json
from hashlib import sha256
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def run_json(script, *args):
    return json.loads(subprocess.check_output(
        [sys.executable, "-B", str(script), *args], cwd=script.parent))


def check_result(script, result_file, args=(), key=None):
    expected = json.loads(result_file.read_text(encoding="utf-8"))
    if key is not None:
        expected = expected[key]
    if run_json(script, *args) != expected:
        raise ValueError(f"Abweichung von {result_file.name} bei {script.name}.")
    print(f"PASS  {script.relative_to(ROOT)} {' '.join(args)}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quadratur", action="store_true",
                        help="zusätzlich die 60/85-stellige Gegenquadratur ausführen (mpmath 1.3.0)")
    args = parser.parse_args()
    for line in (ROOT / "SHA256SUMS").read_text().splitlines():
        expected, filename = line.split("  ", 1)
        if sha256((ROOT / filename).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Prüfsumme abweichend: {filename}")
    print("PASS  SHA-256 der Paketdateien", flush=True)
    check_result(ROOT / "pakettest.py", ROOT / "ergebnis.json")
    check_result(ROOT / "schnitt.py", ROOT / "schnitt.json")
    check_result(ROOT / "skalar.py", ROOT / "skalar.json")
    check_result(ROOT / "gegenprobe.py", ROOT / "gegenprobe.json", ("--struktur",), "struktur")
    old = ROOT / "altstudien"
    # The archive runner verifies the original JSONs and has its own tolerances
    # for the independent floating-point checks. Verify its scope here.
    actual = run_json(old / "pruefen.py")
    expected = json.loads((old / "referenzlauf.json").read_text(encoding="utf-8"))
    keys = ("status", "commit", "originalrechnungen", "sobol", "physikalische_P3_Laeufe")
    if any(actual[k] != expected[k] for k in keys):
        raise ValueError("Umfang oder Status der N15-Reproduktion weicht ab.")
    if set(actual["unabhaengige_kontrollen"]) != set(expected["unabhaengige_kontrollen"]):
        raise ValueError("Unvollständige unabhängige Gegenkontrollen.")
    print("PASS  altstudien/pruefen.py (14 Originalrechnungen und vier Gegenkontrollen)", flush=True)
    if args.quadratur:
        check_result(ROOT / "gegenprobe.py", ROOT / "gegenprobe.json")
    print("Physikalische Randpaarung: HOLD. P3: NOT_RUN.")


if __name__ == "__main__":
    main()
