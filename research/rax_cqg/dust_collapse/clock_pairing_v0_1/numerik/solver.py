"""Endrandfreier Referenztransport bis N=2. Ausgabe als exaktes JSON."""
import argparse
import json
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from pathlib import Path

STATES = ("leer", "ein", "zweierkette", "zweierantikette")
GRID = tuple(F(i, 8) for i in range(9))
IDENTITY = tuple(tuple(F(i == j) for j in range(4)) for i in range(4))


def check(condition, message):
    if not condition:
        raise ValueError(message)


def multiply(left, right):
    return tuple(tuple(sum(x*y for x, y in zip(row, col) if x and y)
                       for col in zip(*right)) for row in left)


@lru_cache(maxsize=None)
def birth(delta, alpha):
    w = F(1, 2**alpha)
    pair = w * delta**2 / 2
    return ((1, delta, pair, pair), (0, 1, w*delta, w*delta),
            (0, 0, 1, 0), (0, 0, 0, 1))


def h(s, c, alpha):
    return tuple(sum(x*y for x, y in zip(row, c)) for row in birth(-s, alpha))


@lru_cache(maxsize=None)
def transport(a, b, c, alpha):
    check(0 <= a <= b <= 1, "Zeiten ausserhalb des Fensters")
    before, after = h(a, c, alpha), h(b, c, alpha)
    check(min(before + after) > 0, "Metrik singulaer oder indefinit")
    matrix = tuple(tuple(bij * after[j] / before[i] for j, bij in enumerate(row))
                   for i, row in enumerate(birth(b-a, alpha)))
    check(all(min(row) >= 0 and sum(row) == 1 for row in matrix), "Zeilennorm")
    return matrix


def partitions(first, last):
    for count in range(last-first):
        for middle in combinations(range(first+1, last), count):
            yield (first, *middle, last)


def horizon_laws(end_index, c, alpha):
    total = full = 0
    for first, last in combinations(range(end_index+1), 2):
        direct = transport(GRID[first], GRID[last], c, alpha)
        for route in partitions(first, last):
            product = IDENTITY
            for i, j in zip(route, route[1:]):
                product = multiply(product, transport(GRID[i], GRID[j], c, alpha))
            check(product == direct, "Schnittabweichung")
            total += 1
            full += (first, last) == (0, end_index)
    return {"alle_endpunktpaare_und_unterteilungen": total, "wege_der_gesamtstrecke": full}


def early_marginal(a, mid, end, c, alpha):
    # Marginalize the complete *joint* distribution on (intermediate, final) records.
    first = transport(a, mid, c, alpha)
    last = transport(mid, end, c, alpha)
    return tuple(tuple(sum(row[y]*last[y][z] for z in range(4)) for y in range(4))
                 for row in first)


def coherent_record(c, alpha):
    # Abstract record-space isometry |i> -> sum_y sqrt(P_iy) |i,y>.
    # At u=1/4 select the same, phase-sensitive plus effect for both preparations.
    # Prepared vectors are (|empty> +/- |one>)/sqrt(2); their norms are one.
    start, split, read = F(1, 8), F(3, 16), F(1, 4)
    direct = transport(start, read, c, alpha)
    p, q = direct[0][1], direct[1][1]
    check(p > 0 and q > 0, "beide kohaerenten Pfade erforderlich")
    # Refine the coarse basis record |i,y> via its normalized positive bridge.
    # Since the basis vectors are orthogonal, the map is isometric once each
    # bridge has unit norm. Checking squares suffices for these positive roots.
    first, second = transport(start, split, c, alpha), transport(split, read, c, alpha)
    bridge_norms = 0
    for i in range(4):
        for y, prob in enumerate(direct[i]):
            weights = [first[i][j]*second[j][y] for j in range(4)]
            if prob:
                check(sum(w / prob for w in weights) == 1, "Brueckennorm")
                bridge_norms += 1
            else:
                check(sum(weights) == 0, "unerlaubte Bruecke")
    # After the fixed early readout the same record y has the same continuations.
    for endpoint in (F(1, 2), F(1)):
        invisible_extension = sum(transport(read, endpoint, c, alpha)[1])
        check(invisible_extension == 1, "spaeteres Ende aendert fruehe Kohaerenz")
    # p_+/- = center +/- sqrt(radicand)/2, where the suffix denotes the input sign.
    center = (p+q)/4
    radicand = p*q
    check(center**2 >= radicand/4 and (1-center)**2 >= radicand/4, "Effekt ausserhalb [0,1]")
    return {"start": start, "rechenzwischenschnitt": split, "auslese": read,
            "zustandsraum": "Abstrakter Registerraum der Ordnungstypen; Halbgruppenzeile für den bevölkerten Einsektor bei positivem Startuhrwert. Keine aus der CST-Wirkung abgeleitete kohärente Präparation.",
            "wirkung": "F=|f><f|, f=(|leer,ein>+|ein,ein>)/sqrt(2)",
            "praeparationen": "(|leer> +/- |ein>)/sqrt(2)",
            "p_leer_nach_ein": p, "p_ein_nach_ein": q, "wahrscheinlichkeit_mitte": center,
            "wahrscheinlichkeit_formel": "mitte +/- sqrt(kontrast_quadrat)/2",
            "kontrast_quadrat": radicand, "anzahl_gepruefter_nichtleerer_bruecken": bridge_norms,
            "status": "kohärenter Hilfsrecord mit positiven Wurzeln, offen für das physikalische CST-Modell"}


def check_case(name, c, alpha):
    c = tuple(F(x) for x in c)
    w = F(1, 2**alpha)
    rate = w * (c[2]+c[3])
    # On [0,1], h1(s)=c1-rate*s, h0'(s)=-h1(s). Both attain their minima at s=1.
    minima = h(F(1), c, alpha)
    check(c[2] > 0 and c[3] > 0 and c[1] > rate and min(minima) > 0, "Positivitaetszertifikat")
    check(minima == (c[0]-c[1]+rate/2, c[1]-rate, c[2], c[3]), "analytische Minima")
    horizons = {str(GRID[end]): horizon_laws(end, c, alpha) for end in (4, 8)}
    check(horizons["1/2"] == {"alle_endpunktpaare_und_unterteilungen":26, "wege_der_gesamtstrecke":8},
          "Abdeckung kurzer Endwert")
    check(horizons["1"] == {"alle_endpunktpaare_und_unterteilungen":502, "wege_der_gesamtstrecke":128},
          "Abdeckung langer Endwert")
    tested_prefixes = 0
    for ai, ui in combinations(range(5), 2):
        a, u = GRID[ai], GRID[ui]
        direct = transport(a, u, c, alpha)
        short = early_marginal(a, u, F(1, 2), c, alpha)
        long = early_marginal(a, u, F(1), c, alpha)
        check(direct == short == long, "Endwert-Marginale")
        tested_prefixes += 1
    empty = {str(t): transport(F(0), t, c, alpha)[0][0] for t in (F(1, 4),F(1, 2))}
    return {"fall": name, "alpha": alpha, "anfangsmetrik_diagonal": c, "minima_ueber_ganzes_intervall": minima,
            "p_leer_beim_start_leer": empty, "endwerte": horizons,
            "fruehe_endpunktpaare_marginalisiert_auf_beiden_endwerten": tested_prefixes,
            "kohaerenter_record": coherent_record(c, alpha)}


def legacy_empty(u, end):
    # The archived short-horizon normalization chooses terminal h(end)=1 each time.
    return sum(birth(end-u,1)[0]) / sum(birth(end,1)[0])


def run():
    inputs = [("primaer_beta_5_4", (1,F(5,4),1,1), 1), ("primaer_beta_4_3", (1,F(4,3),1,1), 1)]
    inputs.extend((f"zusatz_c0_{c0}_alpha_{alpha}", (c0, 2, 1, 1), alpha)
                  for c0 in (3, 4) for alpha in (1, 2))
    cases = [check_case(*entry) for entry in inputs]
    empty = [v["p_leer_beim_start_leer"] for v in cases]
    check(empty[0] == {"1/4":F(23,32), "1/2":F(1,2)}, "primaer beta 5/4")
    check(empty[1] == {"1/4":F(67,96), "1/2":F(11,24)}, "primaer beta 4/3")
    check(empty[2]["1/4"] == F(27,32) and empty[4]["1/4"] == F(113,128), "Zusatzzeuge")
    old = {str(end): legacy_empty(F(1, 4), end) for end in (F(1,4), F(1,2), F(1))}
    check(old == {"1/4":F(32,41), "1/2":F(41,52), "1":F(13,16)}, "Endwert-Gegenprobe")
    return {"bereich": "Diagonale N<=2-Uhrreferenz, vier Ordnungsklassen, s in [0,1]",
            "zustandsfolge": STATES, "faelle": cases, "feste_endnorm_gegenprobe_p_leer_bis_s_1_4": old,
            "befund": "Endwertunabhaengige normtreue Referenzen existieren auf N<=2; das Anfangsprodukt ist im Sektor nicht eindeutig gewaehlt.",
            "physikalische_P3_Vergleiche_ausgefuehrt": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="JSON-Datei; standardmaessig stdout")
    args = parser.parse_args()
    result = json.dumps(run(), indent=2, ensure_ascii=False, default=str) + "\n"
    if args.out is None:
        print(result, end="")
    else:
        args.out.write_text(result, encoding="utf-8")
