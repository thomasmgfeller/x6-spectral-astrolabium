"""Check the twelve independent terminal certificates without a numerical solver."""
import csv
from fractions import Fraction
import json
import re
from elimination import HERE, BASE, form, constraints, margin


def main():
    proofs = json.loads((HERE / "Zweitnachweise.json").read_text())
    with (BASE / "Fallregister.tsv").open() as table:
        terminal = [r for r in csv.DictReader(table, delimiter="\t")
                    if r["grund"] == "rationales Terminalzertifikat"]
    registered = set()
    for row in terminal:
        assert row["status"] == "AUSGESCHLOSSEN" and not row["alte_zukunft_23"]
        start = row["bahnen_von"].split(",")[0]
        mask = sum(1 << int(i) for i in row["alte_vergangenheit_23_mit_22"].split(","))
        registered.add(f"{row['praeparation']}{start}_{mask}")
    assert set(proofs) == registered and len(registered) == 12
    groups = json.loads((BASE / "basis" / "Sonden_auf_N23.json").read_text())
    results = []
    for tag, weights in proofs.items():
        side, start, mask = re.fullmatch(r"(light|heavy)(\d)_(\d+)", tag).groups()
        start = int(start)
        past = [i for i in range(23) if (int(mask) >> i) & 1]
        rel, model, box = form(side, start, past)
        assert model.out[23] == [] and 23 not in box and len(box) <= 48
        rows = constraints(rel, model, box)
        assert all(isinstance(c,(int,Fraction)) for r in rows.values() for c in r.values())
        delta = margin(rows, weights, box)
        assert delta > Fraction(1, 100000), tag
        order = next(r["order"] for r in groups[side] if r["start"] == start)
        starts = [r["start"] for r in groups[side] if r["order"] == order]
        results.append({"id": tag, "strahlen": starts, "A23": str(sum(
            k for _, k, _ in model.inc[23])), "marge": str(delta)})
    expected = HERE / "Ergebnisse.json"
    assert json.loads(expected.read_text()) == results
    print(f"{len(results)} rationale Zweitnachweise bestätigt.")


if __name__ == "__main__":
    main()
