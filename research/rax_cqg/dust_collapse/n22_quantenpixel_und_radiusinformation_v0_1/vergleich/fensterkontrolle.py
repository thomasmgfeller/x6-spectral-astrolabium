"""Bedingte Einteilchenkontrolle im publizierten Modelluhrfenster, Python >= 3.10."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
HASH = "c75c0c97c1b536d0140d77b4f01d8bfa0a2aab487a1b05a2b58f2ebf23159c2f"


def binary_impurity(p):
    return 2 * p * (1-p)


def evaluate(record):
    positive = record["positive_in_window"]
    zeros = record["zero_in_window"]
    assert positive == [18, 19] and zeros == [17, 20]
    weights = [tuple(map(Fraction, box)) for box in record["weight_box"]]
    assert all(weights[i] == (0, 0) for i in zeros)
    (a, b), (c, d) = (weights[i] for i in positive)
    assert 0 < a <= b and 0 < c <= d
    # p = w18/(w18+w19) steigt in w18 und fällt in w19.
    low, high = a/(a+d), b/(b+c)
    assert Fraction(1,2) < low <= high < 1
    # Auf [1/2,1] fällt 2p(1-p).
    interval = binary_impurity(high), binary_impurity(low)
    return {
        "normierter_Anteil_18": list(map(str,(low,high))),
        "klassische_Unreinheit_im_Zweiknotenregister": list(map(str,interval)),
        "einteilchenmodell_entropie_material_leer": "0",
        "einteilchenmodell_entropie_18_gegen_19": list(map(str,interval)),
    }


def run():
    raw = (HERE/"Vergleichspaar.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == HASH
    data = json.loads(raw)
    assert data["normalized_window"] == ["15/32", "17/32"]
    out = {case:evaluate(data[case]) for case in ("heavy", "light")}
    assert Fraction(out["heavy"]["klassische_Unreinheit_im_Zweiknotenregister"][0]) > Fraction(
        out["light"]["klassische_Unreinheit_im_Zweiknotenregister"][1])
    return {
        "input_sha256":HASH,
        "umfang":"Nur die vier Ereignisse im normierten Fenster. Bedingte Beispielmodelle.",
        "praeparationen":out,
        "leeres_fenster_mit_vier_nullgewichten":"Anteile und Einteilchenzustand undefiniert",
        "physische_entropie_schwer_leicht_vakuum":None,
        "unabhaengige_radiusablesung":None,
    }


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Python ohne -O starten.")
    print(json.dumps(run(),indent=2,ensure_ascii=False))
