"""Replay rational certificates and optional independent checks from this archive."""
import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def replay(stem):
    result = subprocess.check_output([sys.executable, "-B", str(ROOT / (stem + ".py"))], cwd=ROOT)
    data = json.loads(result)
    if data != json.loads((ROOT / (stem + ".json")).read_text()):
        raise ValueError("Ergebnisabweichung: " + stem)
    print("PASS", stem, flush=True)
    return data


def check_matrices():
    import zulassung
    sys.path.insert(0, str(ROOT / "basis/n17"))
    from gegenprobe import complex_schur
    import sympy as sp
    data = zulassung.run()["geometries"]
    for name, (_, weights) in zulassung.develop()[2].items():
        det, eff = complex_schur(weights)
        scalar = data[name]["scalar"]
        assert Fraction(det) == scalar["hidden_det"]
        for i in range(2):
            for j in range(2):
                assert Fraction(str(sp.re(eff[i, j]))) == scalar["real_over_beta"][i][j]
                assert Fraction(str(-sp.im(eff[i, j]))) == scalar["phase_over_beta"][i][j]
    print("PASS unabhängige Skalarreduktion, beide Geometrien", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gegenprobe", action="store_true")
    args = parser.parse_args()
    for line in (ROOT / "SHA256SUMS").read_text().splitlines():
        expected, name = line.split("  ", 1)
        if sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise ValueError("Abweichende Prüfsumme: " + name)
    print("PASS SHA-256", flush=True)
    for name in ("zulassung", "kontrolle", "massentest"):
        replay(name)
    cert = replay("transfer")
    assert cert["decision"] == "PASS_NONZERO"
    if args.gegenprobe:
        check_matrices()
        replay("quadratur")
        independent = replay("transfer_quadratur")["resolutions"]
        lo, hi = map(Fraction, cert["center_contrast"])
        for data in independent.values():
            assert lo <= Fraction(data["positive_minus_negative"]["primary"]) <= hi
        print("PASS unabhängige Zentren im rationalen Intervall", flush=True)


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Die Prüfung benötigt aktive Assertions.")
    main()
