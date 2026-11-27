"""Necessary equations of degree at most two after eliminating the helper clock."""
from fractions import Fraction as Q
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASE = next(p for p in (HERE / "basislauf", HERE.parent / "positive_probe_next")
            if (p / "pruefen.py").is_file())
sys.path.insert(0, str(BASE))
from pruefen import HelperModel, early_bounds, bounds, intersect, ordered, POS, EMPTY, S


class Polynomial(dict):
    """Sparse rational polynomial. Sorted tuples encode monomials."""

    def __add__(self, other):
        if not isinstance(other, Polynomial):
            other = Polynomial({(): Q(other)})
        result = self.copy()
        for key, value in other.items():
            result[key] = result.get(key, 0) + value
        return Polynomial({key: value for key, value in result.items() if value})

    __radd__ = __add__

    def __neg__(self):
        return Polynomial({key: -value for key, value in self.items()})

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return other + -self

    def __mul__(self, other):
        if not isinstance(other, Polynomial):
            return Polynomial({key: value * other for key, value in self.items()
                               if value * other})
        result = {}
        for a, x in self.items():
            for b, y in other.items():
                key = tuple(sorted(a + b))
                result[key] = result.get(key, 0) + x * y
        return Polynomial({key: value for key, value in result.items() if value})

    __rmul__ = __mul__


def variable(i):
    return Polynomial({(i,): Q(1)})


def square(x):
    return x * x


def form(side, start, past):
    pair = json.loads((BASE / "basis" / "Vergleichspaar.json").read_text())
    studies = json.loads((BASE / "basis" / "Sonden_auf_N23.json").read_text())
    order = next(x["order"] for x in studies[side] if x["start"] == start)
    rel = (set(map(tuple, pair["relation"])) | {(i, 22) for i in order["past"]}
           | {(22, j) for j in order["future"]})
    assert set(past) >= set(order["past"]) | {22}
    ext = rel | {(i, 23) for i in past}
    assert all((i, j) in ext for i, k in ext for m, j in ext if k == m)
    model = HelperModel(ext)
    clocks, weights = bounds(pair, side)
    clocks[22] = (clocks[3] + clocks[7]) / 2
    for i, interval in early_bounds(pair, side, model).items():
        intersect(clocks, i, interval)
    clocks[21] = model.bounded_root(21, clocks)
    assert clocks[21] is not None
    if not model.out[21]:
        model.terminal(21, clocks)
    for _ in range(8):
        ordered(rel, clocks)
        for j in POS:
            model.density(j, clocks)
    box = {i: (Q(v.l, S), Q(v.h, S)) for i, v in clocks.items()}
    box.update({i + 24: (Q(v.l, S), Q(v.h, S)) for i, v in weights.items()
                if i not in EMPTY})
    box[47] = (Q(0), Q(16 if side == "light" else 1))
    return rel, model, box


def constraints(rel, model, box):
    """Return necessary inequalities P <= 0 indexed by certificate row names."""
    x = {i: variable(i) for i in box}
    y = {i: x[i] for i in range(23)}
    w = {i: x.get(i + 24, Polynomial()) for i in range(24)}
    rows = {}

    def eq(name, expression):
        rows[name + "+"] = expression
        rows[name + "-"] = -expression

    for i, j in sorted(rel):
        rows[f"order{i}_{j}"] = y[i] - y[j]
    eq("mid", 2 * y[22] - y[3] - y[7])
    for j in POS:
        eq(f"D{j}", 19 + sum(k * square(y[j] - y[i]) for i, k, _ in model.inc[j]))

    # From G22, Z is the value of w23*(Y23-Y22) on every solution.
    force = sum(k * w[i] * (y[i] - y[22]) for i, k, _ in model.out[22] if i < 23)
    cap = [k for i, k, _ in model.out[22] if i == 23]
    assert len(cap) == 1 and not model.out[23]
    Z = force * (-Q(1) / cap[0])
    parents = {i: k for i, k, _ in model.inc[23]}
    A = sum(parents.values())
    U = sum(k * (y[i] - y[22]) for i, k in parents.items())
    V = 19 + sum(k * square(y[i] - y[22]) for i, k in parents.items())
    if A:
        eq("D23proj", A * V - square(U))
        for i in parents:
            rows[f"caus23_{i}"] = y[i] - y[22] - U * (Q(1) / A)
    else:
        eq("H23", U)
        eq("D23proj", V)
        for i in (15, 16, 17, 18, 19, 20, 21, 22):
            eq(f"lift23_{i}", U * y[i])
    eq("WH23", A * Z - w[23] * U)

    for j in (*POS, 15, 17, 20):
        expression = Polynomial()
        for i, k, _ in model.out[j]:
            if i == 23:
                expression += k * (Z + w[23] * (y[22] - y[j]))
            else:
                expression += k * w[i] * (y[i] - y[j])
        expression -= sum(k * w[j] * (y[j] - y[i]) for i, k, _ in model.inc[j])
        eq(f"G{j}", expression)
    for i in parents:
        rows[f"w23gap_{i}"] = -Z - w[23] * (y[22] - y[i])

    pairs = sorted({key for row in rows.values() for key in row if len(key) == 2})
    for i, j in pairs:
        l, h = box[i]
        a, b = box[j]
        v, u = x[i], x[j]
        product = v * u
        label = f"{i}_{j}"
        if i == j:
            for n, t in enumerate((l, (l + h) / 2, h)):
                rows[label + "T" + str(n)] = 2 * t * v - t * t - product
            rows[label + "S"] = product - (l + h) * v + l * h
        else:
            rows[label + "L1"] = l * u + a * v - l * a - product
            rows[label + "L2"] = h * u + b * v - h * b - product
            rows[label + "U1"] = product - h * u - a * v + h * a
            rows[label + "U2"] = product - l * u - b * v + l * b
    for i, (l, h) in box.items():
        rows[f"L{i}"] = l - x[i]
        rows[f"H{i}"] = x[i] - h
    return rows


def extrema(term, box):
    if len(term) == 1:
        return box[term[0]]
    i, j = term
    corners = [a * b for a in box[i] for b in box[j]]
    if i == j and box[i][0] <= 0 <= box[i][1]:
        corners.append(Q(0))
    return min(corners), max(corners)


def margin(rows, weights, box):
    combined = Polynomial()
    for key, weight in weights.items():
        weight = Q(weight)
        assert weight > 0
        combined += rows[key] * weight
    return (combined.get((), 0)
            + sum(min(k * v for v in extrema(term, box))
                  for term, k in combined.items() if term))
