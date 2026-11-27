"""Triangular consequences of the original density and clock equations."""
from fractions import Fraction as F
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from zipfile import ZipFile

from intervall import I, box, point, positive, zero

ROOT = Path(__file__).resolve().parent
PIN = "d9fbaa44c5db7dc31c06c4521a3059c6ca8c762f3a300cd3da1db12e89189f18"
EPS = point(F(1, 10**11))
ONE = point(1)


def source():
    archive = ROOT / "basis/Innenfelder.zip"
    assert sha256(archive.read_bytes()).hexdigest() == PIN
    with ZipFile(archive) as parent:
        data = json.loads(parent.read("Ergebnisse.json"))
        with ZipFile(BytesIO(parent.read("basis/Randgeometrie.zip"))) as prev:
            pair = json.loads(prev.read("basis/Vergleichspaar.json"))
    return pair, data


def edges(pair, case):
    rel = set(map(tuple, pair["relation"]))
    rel.update((i, 22) for i in case["past"])
    rel.update((22, j) for j in case["future"])
    device = {(15, 16), (16, 18), (17, 18), (18, 7)}
    coeff = {}
    for i, j in rel:
        n = sum((i, k) in rel and (k, j) in rel for k in range(23))
        value = F((1, -9, 16, -8, 0)[min(n, 4)]) - F((i, j) in device, 10**11)
        if value:
            coeff[i, j] = value
    return rel, coeff


def sqsum(terms, q):
    return sum((k * (q-y).sq() for k, y in terms), point(0))


def lin(terms, q):
    return sum((k * (q-y) for k, y in terms), point(0))


def quadratic(terms, anchor):
    return sum(k for k, _ in terms), 2*lin(terms, anchor), 19+sqsum(terms, anchor)


class System:
    def __init__(self, pair, side, family, margin=F(0)):
        self.family = family
        old = pair[side]
        self.y = y = {i: box(*old["clock_box"][i]) for i in (0, 1, 2, 3, 7, 8, 9, 10)}
        scale = 16 if side == "light" else 1
        w = {i: box(*old["weight_box"][i])*scale for i in range(7, 11)}
        self.window = y[3] + box(F(15, 32), F(17, 32))*(y[7]-y[3])
        self.positive_window = y[3] + box(F(15, 32)-margin, F(17, 32)+margin)*(y[7]-y[3])
        assert all(y[i].h < self.positive_window.l for i in (0, 1, 2, 3))
        assert all(y[i].l > self.positive_window.h for i in (7, 8, 9, 10))
        self.early = tuple(zip((-8, 16, -9), (y[0], y[1], y[2])))
        self.ucoef = quadratic(self.early, point(-1))
        self.late = {}
        rows = {"full": (1, -9, 16, -8), "18": (ONE-EPS, -9, 16, -8),
                "twin": (-9, 16, -8, 0), "15": (-8, 0, 0, 0), "16": (16, -8, 0, 0)}
        for label, row in rows.items():
            weighted = [k*w[j] for j, k in enumerate(row, start=7)]
            self.late[label] = (sum((k*y[j] for j, k in enumerate(weighted, start=7)), point(0)),
                                sum(weighted, point(0)))

        A, B, C = quadratic((*self.early, (1, y[3])), point(0))
        assert A == 0 and B.h < 0
        y[4] = y[5] = y[6] = -C/B
        early_rows = [(11, {2: -8, 3: 16, 4: 1, 5: 1}, 4),
                      (12, {4: -9, 5: -9, 6: 1, 11: 1}, 11),
                      (13, {3: -8, 4: 1, 5: 1, 6: 1}, 4)]
        for j, row, last in early_rows:
            terms = tuple((k, y[i]) for i, k in row.items())
            A, B, C = quadratic(terms, y[last])
            # The two increments have opposite signs; causality selects the positive one.
            assert (A > 0 and C.h < 0) or (A < 0 and C.l > 0)
            disc = (B.sq()-4*A*C).sqrt()
            y[j] = y[last] + (-B+(disc if A > 0 else -disc))/(2*A)
        assert all(y[i].h < self.positive_window.l for i in (4, 5, 6, 11, 12, 13))
        assert (19-9*(self.positive_window-y[11]).sq()).l > 0

    def late_at(self, kind, clock):
        offset, slope = self.late[kind]
        return offset - slope*clock

    def first(self, a):
        A, B, C = self.ucoef
        x = a + 1
        u = a - (-(C+x*(B+A*x))/(ONE-EPS)).sqrt()
        positive(u-self.y[2], "15 nach 2")
        terms = ((-8, self.y[1]), (16, self.y[2]), (-9, u), (1, a))
        h = -lin(terms, point(-1))
        D = 19 + sqsum(terms, point(-1))
        # This test precedes division, so a box containing h=0 cannot lose a root.
        admissible = I(a.l, self.y[7].h)
        zero(D-2*h*(admissible+1), "D19 ausserhalb")
        p = (-1+D/(2*h)).cut(admissible)
        return u, h, p

    def front14(self, z):
        y = self.y
        # The -8,-8,+16 terms cancel because Y4=Y5=Y6.
        terms = ((-9, y[11]), (1, y[12]), (1, y[13]))
        if self.family == 14:
            terms += ((1, z),)
        A, B, C = quadratic(terms, point(0))
        # G14 and w14>0 require the negative derivative.
        assert self.late_at("full", I(y[11].l, y[7].h)).h < 0
        disc = (B.sq()-4*A*C).sqrt()
        clock = (-B-disc)/(2*A)
        return clock, -2*self.late_at("full", clock)/disc
