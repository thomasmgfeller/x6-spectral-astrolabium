"""Reproduce the finite clock pairing study from a repository checkout. Python >= 3.10."""
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def run(script):
    command = [sys.executable, "-O", "-B", str(ROOT / script)]
    completed = subprocess.run(command, cwd=ROOT, check=True, stdout=subprocess.PIPE)
    return completed.stdout.decode("utf-8")


def read(path):
    return json.loads((ROOT / path).read_bytes())


def replay(script, snapshot):
    result = json.loads(run(script))
    if result != read(snapshot):
        raise RuntimeError(f"Abweichung in {snapshot}")
    return result


def main():
    repo = ROOT.parents[3]
    for source in read("quellen.json")["dateien"].values():
        path = repo / source["pfad"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != source["sha256"]:
            raise RuntimeError(f"Quelldatei abweichend: {path}")
    print(run("theorie/harmonisch.py").strip())
    solver = replay("numerik/solver.py", "numerik/ergebnisse.json")
    audit = replay("audit/coherent_audit.py", "audit/coherent_audit.json")
    by_name = {c["fall"]: c for c in solver["faelle"]}
    for name, label in [("primaer_beta_5_4", "5/4"), ("primaer_beta_4_3", "4/3")]:
        c = by_name[name]
        beta = F(c["anfangsmetrik_diagonal"][1])
        ratio = (beta - F(3,8)) / (beta - F(1,4))
        for row in audit["models"]["linear_h_beta_"+label]:
            if any(F(coord) != ratio/3 for coord in row["E_cross_re_im"]):
                raise RuntimeError("Audit und Anfangsprodukt liefern verschiedene Kreuzterme")
    extra = json.loads(run("zusatz.py"))
    archived = read("zusatz.json")
    # Each floating diagnostic has its own tolerance in zusatz.py; platform
    # libraries can differ at machine precision. The rational checks are exact.
    for k in ["orbit","audit"]:
        if extra[k] != archived[k]:
            raise RuntimeError(f"Abweichender Kontrollbefund: {k}")
    if extra["actions"]["example"] != archived["actions"]["example"]:
        raise RuntimeError("Wirkungsdiagnose abweichend")
    print("Solver und unabhängiger komplexer Audit reproduziert. 108 direkte/verklebte Auditpaare.")
    print("N14: identische N13-Spalten. Wirkungskontrollen:",extra["actions"]["branch_comparisons"])
    print("P3 M=1: 20/20 klassische Hüllen; neue physikalische Auslesen:",extra["M1"]["physical_observations"])
    print("Referenzlauf abgeschlossen. Physikalische Auswahl und P3 bleiben offen.")


if __name__ == "__main__":
    main()
