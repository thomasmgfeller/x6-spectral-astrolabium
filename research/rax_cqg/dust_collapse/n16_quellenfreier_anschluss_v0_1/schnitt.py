"""Local orders at Y=0, the bypass link, and reconstruction of the whole action."""
from itertools import product
import json
import pakettest as test

NODES = set(range(16))
SEAM = {5, 11}
LEFT = set(test.P) | {4, 5, 6, 11}
RIGHT = (NODES - LEFT) | SEAM


def closure(rel):
    while True:
        expanded = rel | {(i, j) for i, a in rel for b, j in rel if a == b}
        if expanded == rel:
            return rel
        rel = expanded


def interval_table(rel, groups):
    weights = {}
    for i, j in rel:
        count = sum(sum((i, k) in rel and (k, j) in rel for k in group) for group in groups)
        if count < len(test.LAYERS):
            weights[i, j] = test.LAYERS[count]
    return weights


def run():
    neutral, _ = test.packet_family(test.old.STEP)
    y = {**neutral, 15: test.YN}
    assert {i for i in NODES if y[i] < 0} == LEFT
    assert min(abs(y[i]) for i in NODES) > test.H
    assert LEFT & RIGHT == SEAM
    result = {}
    for name, past in test.CASES.items():
        direct = test.old.ORDER | {(i, 15) for i in past}
        suborders = {(i, j) for i, j in direct if {i, j} <= LEFT or {i, j} <= RIGHT}
        from_seam = closure(suborders)
        # In the minimal case a link skips the cut antichain on another branch.
        bypass = {(6, 15)} if name == "minimal" else set()
        sewn = closure(suborders | bypass)
        assert sewn == direct
        wd = interval_table(direct, (NODES,))
        ws = interval_table(sewn, (LEFT - SEAM, SEAM, RIGHT - SEAM))
        assert ws == wd
        assert {i: b for (i, j), b in ws.items() if j == 15} == test.new_edges(past)
        assert (from_seam == direct) == (not bypass)
        counts = [sum((i, j) in direct for i, j in product(LEFT - SEAM, RIGHT - SEAM)),
                  sum((i, j) in ws for i, j in product(LEFT - SEAM, RIGHT - SEAM))]
        # Translation family from PR 339: all old clocks fixed between branches;
        # direction in the three old recipient densities preserves their sum and action.
        c = test.old_coefficient(neutral)
        direction = {5: c[12] - c[13], 12: c[13] - c[5], 13: c[5] - c[12]}
        assert sum(direction.values()) == sum(c[i] * t for i, t in direction.items()) == 0
        result[name] = {"antikette": sorted(SEAM), "zusaetzlich_noetige_hasserelationen": sorted(bypass),
                        "ohne_zusatz_fehlen": sorted(direct - from_seam),
                        "anzahl_kreuzbeziehungen_und_davon_aktiv": counts,
                        "alle_koeffizienten_gleich": True,
                        "staub_gravitation_skalar_quellen_und_kreuzterme": "identische Ordnung und identische Intervallzahlen"}
    return result


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Ohne -O ausführen.")
    print(json.dumps(run(), indent=2, ensure_ascii=False))
