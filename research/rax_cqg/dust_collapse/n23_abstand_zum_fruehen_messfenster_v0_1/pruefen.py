"""Replay both interval coverings and compare their results and register byte for byte."""
import argparse
import csv
import json
from fractions import Fraction
from hashlib import sha256
from io import StringIO

from modellkontrolle import SIDES, check_model
from reduktion import ROOT, PIN, System, source
from zweige import prerequisites, search

MARGIN = Fraction(1, 1280)


def build():
    digest, filename = (ROOT / "Pruefplan.sha256").read_text().split()
    assert sha256((ROOT / filename).read_bytes()).hexdigest() == digest
    pair, parent = source()
    assert pair["normalized_window"] == parent["window"] == ["15/32", "17/32"]
    assert parent["P3_count"] == 60 and parent["physical_P3"] == "NOT_RUN"
    assert parent["physical_pilot_radii"] == [None] * 8
    check_model(pair, parent["cases"])
    runs = {}
    for family in (14, 18):
        for side in SIDES:
            results = {}
            for margin in (Fraction(0), MARGIN):
                system = System(pair, side, family, margin)
                bounds = prerequisites(system)
                coverage, remaining = search(system)
                if remaining:
                    raise RuntimeError(f"{family}/{side}/{margin}: {len(remaining)} offene Bereiche")
                results[str(margin)] = dict(bounds=bounds, coverage=coverage, unresolved=0)
            runs[f"{family}_{side}"] = results

    witness = parent["solutions"]["18_light"]
    upper = Fraction(witness["x"][19][1]) - Fraction(17, 32)
    assert MARGIN < upper < Fraction(786788, 10**9)
    register = StringIO()
    writer = csv.writer(register, delimiter="\t", lineterminator="\n")
    writer.writerow(["Nachfolger_22", "Vorgaenger_22", "Praeparation",
                     "Sonde_22_im_Fenster", "Positives_Ereignis_im_Fenster_mit_Sonde",
                     "Begruendung", "Abstand_unten_normiert_bei_Sonde_im_Fenster"])
    for case in parent["cases"]:
        for side in SIDES:
            exists = case["status"] == "EXISTS_IN_WINDOW"
            reason = case[side] if exists else "PR414_Sonde_ausgeschlossen"
            writer.writerow([",".join(map(str, case["future"])), ",".join(map(str, case["past"])) or "∅",
                             side, "JA" if exists else "NEIN", "AUSGESCHLOSSEN",
                             reason, str(MARGIN) if exists else ""])

    data = dict(input_sha256=PIN, commit="caf68f68454809c9b7e464eb681623f8afff530f",
                original_window=parent["window"], preparations=list(SIDES),
                orders=25, combinations=50, mixed_contacts_excluded=50, runs=runs,
                infimum_distance_lower=str(MARGIN), infimum_distance_upper=str(upper),
                upper_witness=dict(family=18, side="light", positive_event=19),
                physical_pilot_radii=[None] * 8, physical_P3="NOT_RUN", P3_count=60)
    return {"Ergebnisse.json": json.dumps(data, sort_keys=True, indent=2) + "\n",
            "Fallregister.tsv": register.getvalue()}


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Ohne -O ausführen")
    parser = argparse.ArgumentParser()
    parser.add_argument("--ausgabe", action="store_true")
    write = parser.parse_args().ausgabe
    for filename, content in build().items():
        path = ROOT / filename
        if write:
            path.write_bytes(content.encode("utf-8"))
        else:
            assert path.read_bytes() == content.encode("utf-8"), filename
    print("Alle vier Systeme für beide Fensterbreiten abgedeckt. 50 Kontaktentscheidungen bestätigt.")
