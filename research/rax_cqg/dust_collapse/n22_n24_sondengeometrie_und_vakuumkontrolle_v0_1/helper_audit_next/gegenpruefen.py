"""Kontrolle aus Eingaben und Fallregister der positiven N24-Hilfssonde."""
import argparse
import csv
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

KRAGEN = {0, 1, 2, 3, 7, 8, 9, 10}
KORREKTUR = {(15, 16), (16, 18), (17, 18), (18, 7)}


def mengen(eintrag):
    return frozenset(map(int, eintrag.split(","))) if eintrag else frozenset()


def raender(relation):
    """Rekursive Enumeration sämtlicher Antiketten, unabhängig von Idealerweiterungen."""
    def antiketten(wahl, kandidaten):
        yield wahl
        for index, v in enumerate(kandidaten):
            rest = tuple(k for k in kandidaten[index + 1:]
                         if (k, v) not in relation and (v, k) not in relation)
            yield from antiketten(wahl | {v}, rest)

    vergangenheiten, zukuenfte = set(), set()
    for rand in antiketten(frozenset(), tuple(range(23))):
        vergangenheiten.add(rand | {a for a, b in relation if b in rand})
        zukuenfte.add(rand | {b for a, b in relation if a in rand})
    return vergangenheiten, zukuenfte


def zeile(relation, ziel):
    eltern = {i for i, j in relation if j == ziel}
    result = {}
    for i in eltern:
        n = len({m for m in eltern if (i, m) in relation})
        wert = (1, -9, 16, -8, 0)[min(n, 4)]
        if (i, ziel) in KORREKTUR:
            wert -= Fraction(1, 10**11)
        if wert:
            result[i] = wert
    return result


def kraft_vorzeichen(spaete_zeile, uhr, gewicht):
    """Hülle von Summe k*w*(Y_j-(Y_3+Y_7)/2) in Originalgewichtseinheiten."""
    unten = oben = 0
    for j, k in spaete_zeile.items():
        grenzen = [k * w * (yj - (y3 + y7)/2)
                   for w in gewicht[j] for yj in uhr[j] for y3 in uhr[3] for y7 in uhr[7]]
        unten += min(grenzen)
        oben += max(grenzen)
    return (unten > 0) - (oben < 0)


def skaliert(k, box):
    return tuple(sorted(k*x for x in box))


def summiert(boxen, konst=0):
    boxen = list(boxen)
    return (konst + sum(l for l, h in boxen), konst + sum(h for l, h in boxen))


def quadrat(l, h):
    return (0 if l <= 0 <= h else min(l*l, h*h), max(l*l, h*h))


def dichte(zeile_j, z, uhr):
    return summiert((skaliert(k, quadrat(z[0]-uhr[i][1], z[1]-uhr[i][0]))
                     for i, k in zeile_j.items()), 19)


def positive_22(rel, kragen):
    # Zuerst die linearen D4=D5=D6 lösen, nur acht Kragenintervalle sind Daten.
    uhr = {i:kragen[i] for i in KRAGEN}
    for j in (4, 5, 6):
        zeile_j = zeile(rel, j)
        assert sum(zeile_j.values()) == 0
        nenner = summiert(skaliert(2*k, uhr[i]) for i, k in zeile_j.items())
        zaehler = summiert((skaliert(k, quadrat(*uhr[i])) for i, k in zeile_j.items()), 19)
        assert nenner[0] * nenner[1] > 0
        quotienten = [z/n for z in zaehler for n in nenner]
        uhr[j] = min(quotienten), max(quotienten)
    # Vollständige rationale Teilung für D11 ohne Entscheidung für eine Wurzel.
    zeile11 = zeile(rel, 11)
    lo, hi = max(uhr[i][0] for i in zeile11), uhr[7][1]
    assert (11, 7) in rel and lo < hi
    teile = 256
    step = (hi-lo)/teile
    verbleibend = []
    for i in range(teile):
        box = lo + i*step, lo + (i+1)*step
        a, b = dichte(zeile11, box, uhr)
        if a <= 0 <= b:
            verbleibend.append(box)
    assert verbleibend
    uhr[11] = verbleibend[0][0], verbleibend[-1][1]
    mitte = tuple((v+w)/2 for v, w in zip(uhr[3], uhr[7]))
    a, b = dichte(zeile(rel, 22), mitte, uhr)
    assert b < 0
    # Nach aussen gerundete Einheit 1/100 für die lesbare Ausgabe.
    return [a*100//1, -((-b*100)//1)]


def pruefen(studie):
    paar = json.loads((studie / "basis" / "Vergleichspaar.json").read_bytes())
    bahnen = json.loads((studie / "basis" / "Sonden_auf_N23.json").read_bytes())
    zusammenfassung = json.loads((studie / "Ergebnisse.json").read_bytes())
    alt = set(map(tuple, paar["relation"]))
    register = {}
    with (studie / "Fallregister.tsv").open(newline="", encoding="utf-8") as datei:
        for row in csv.DictReader(datei, delimiter="\t"):
            key = (row["praeparation"], mengen(row["bahnen_von"]),
                   mengen(row["alte_vergangenheit_23_mit_22"]), mengen(row["alte_zukunft_23"]))
            assert key not in register, "Doppelter Registereintrag"
            register[key] = row["status"], row["grund"]
    result = {}
    for seite, daten in sorted(bahnen.items()):
        uhr = [tuple(map(Fraction, box)) for box in paar[seite]["clock_box"]]
        gewicht = [tuple(map(Fraction, box)) for box in paar[seite]["weight_box"]]
        assert all(gewicht[j][0] > 0 for j in KRAGEN)
        familien = defaultdict(set)
        for d in daten:
            ordnung = d["order"]
            familien[(frozenset(ordnung["past"]), frozenset(ordnung["future"]))].add(d["start"])
        for (p22, f22), starts in sorted(familien.items(), key=lambda item:min(item[1])):
            rel = alt | {(p, 22) for p in p22} | {(22, f) for f in f22}
            assert f22 == {7, 8, 9, 10}
            past, future = raender(rel)
            frei_alt = set(range(23)) - KRAGEN - {21, 22}
            assert all((0, j) in rel and (j, 7) in rel for j in frei_alt)
            row21 = zeile(rel, 21)
            assert set(row21) <= frei_alt | KRAGEN | {22}
            a21 = sum(row21.values())
            assert a21 != 0
            stat, regeln, kontrollen = Counter(), Counter(), Counter()
            for f in future:
                if not f <= f22:
                    continue
                for p in past:
                    if 22 not in p or any((i, j) not in rel for i in p for j in f):
                        continue
                    key = seite, frozenset(starts), p, f
                    status, grund = register.pop(key)
                    stat[status] += 1
                    regeln[grund] += 1
                    ext = rel | {(i, 23) for i in p} | {(23, j) for j in f}
                    # Nur Ziele in f können 23 als neues Zwischenereignis aufnehmen.
                    assert not f & (frei_alt | {21, 22})
                    assert zeile(ext, 21) == row21
                    sonde = zeile(ext, 23)
                    a23 = sum(sonde.values())
                    if not f:
                        kontrollen["terminal"] += 1
                        if a23 == 0:
                            kontrollen["terminal_A23_null"] += 1
                    if status == "OFFEN":
                        kontrollen["offen_mit_zukunft" if f else "offen_terminal"] += 1
                        if not f and a23 == 0:
                            kontrollen["offen_terminal_A23_null"] += 1
                    if grund == "G22 Vorzeichen":
                        kraefte = {j:zeile(ext, j).get(22, 0) for j in f22}
                        signum = kraft_vorzeichen(kraefte, uhr, gewicht)
                        assert signum and signum * sonde.get(22, 0) >= 0
                        assert status == "AUSGESCHLOSSEN"
                        kontrollen["G22_rational_bestaetigt"] += 1
            name = seite + "_" + ",".join(map(str, sorted(starts)))
            assert stat == zusammenfassung[name]["cases"] and regeln == zusammenfassung[name]["rules"]
            result[name] = dict(anzahl=sum(stat.values()), A21=str(a21),
                                D22_in_Hundertsteln=positive_22(rel, uhr), **kontrollen)
    assert not register and set(result) == set(zusammenfassung)
    return result


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Ohne -O ausführen")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("studie", type=Path, help="Verzeichnis mit Fallregister.tsv, Ergebnisse.json und basis/")
    args = parser.parse_args()
    print(json.dumps(pruefen(args.studie), indent=2, ensure_ascii=False, sort_keys=True))
