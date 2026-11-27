"""Match each reduced equation to the layer coefficients of each original order."""
from fractions import Fraction
from reduktion import edges

POSITIVE = (4, 5, 6, 11, 12, 13, 14, 16, 18, 19, 21)
EMPTY = (15, 17, 20, 22)
SIDES = ("heavy", "light")
DEVICE_FACTOR = 1 - Fraction(1, 10**11)


def check_model(pair, cases):
    factor = DEVICE_FACTOR
    early = {0: -8, 1: 16, 2: -9, 3: 1}
    late = {7: 1, 8: -9, 9: 16, 10: -8}
    twins = {7: -9, 8: 16, 9: -8, 18: 1, 21: 1}
    known = {14: set(), 18: set()}

    for case in cases:
        if case["status"] == "EXCLUDED":
            continue
        assert case["status"] == "EXISTS_IN_WINDOW"
        family = 14 if 14 in case["future"] else 18
        assert set(case["future"]) == {7, 8, 9, 10, family, 21}
        known[family].add(tuple(case["past"]))
        rel, coeff = edges(pair, case)
        assert len(rel) == case["relations"]
        assert all((a, c) in rel and a != c for a, b in rel for j, c in rel if b == j)
        assert all((i, j) in rel for i, j in (
            (4, 11), (11, 12), (4, 13), (11, 14), (14, 7),
            (2, 15), (15, 16), (16, 18), (16, 19), (19, 7), (18, 7),
            (19, 21), (0, 16), (0, 17), (0, 20), (17, 18), (20, 18),
            (17, 21), (20, 21), (22, 21), (22, family)))
        incoming = {
            4: early, 5: early, 6: early,
            11: {2: -8, 3: 16, 4: 1, 5: 1}, 12: {4: -9, 5: -9, 6: 1, 11: 1},
            13: {3: -8, 4: 1, 5: 1, 6: 1},
            14: {4: -8, 5: -8, 6: 16, 11: -9, 12: 1, 13: 1},
            16: {0: -8, 1: 16, 2: -9, 15: factor},
            18: {1: -8, 2: 16, 15: -9, 16: factor, 17: factor, 20: 1},
            19: {1: -8, 2: 16, 15: -9, 16: 1},
            21: {2: -8, 15: 16, 16: -9, 17: 1, 19: 1, 20: 1, 22: 1}}
        incoming[family][22] = 1
        outgoing = {
            14: late, 15: {7: -8, 16: factor, 18: -9, 19: -9, 21: 16},
            16: {7: 16, 8: -8, 18: factor, 19: 1, 21: -9},
            17: {**twins, 18: factor}, 18: {**late, 7: factor},
            19: {**late, 21: 1}, 20: twins, 21: {},
            22: {7: -9, 8: 16, 9: -8, family: 1, 21: 1}}
        for j, row in incoming.items():
            assert row == {i: k for (i, dst), k in coeff.items() if dst == j}
        for i, row in outgoing.items():
            assert row == {j: k for (src, j), k in coeff.items() if src == i and j not in EMPTY}

    assert known == {14: {(), (0,), (0, 1)}, 18: {(), (0,)}}
    assert len(cases) == 25 and sum(c["status"] == "EXCLUDED" for c in cases) == 20
