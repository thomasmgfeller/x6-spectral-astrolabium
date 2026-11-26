"""Read the fixed N19 background and select positive material records by windows."""
from dataclasses import dataclass
from fractions import Fraction as F
import json
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
E = (F(1, 6) - F(1, 2**22), F(1, 6) + F(1, 2**22))
LAYERS = (1, -9, 16, -8)


@dataclass
class Background:
    relation: set
    past: set
    future: set
    clocks: dict
    weights: dict
    windows: list

    @property
    def nodes(self):
        return sorted(self.clocks)

    @property
    def inner(self):
        return sorted(set(self.nodes) - self.past - self.future)

    def renamed(self, perm):
        return Background({(perm[i], perm[j]) for i, j in self.relation},
                          {perm[i] for i in self.past}, {perm[i] for i in self.future},
                          {perm[i]: x for i, x in self.clocks.items()},
                          {perm[i]: w for i, w in self.weights.items()}, self.windows)


def load_background():
    with ZipFile(ROOT / 'basis/N19.zip') as archive:
        witness = json.loads(archive.read('Paar.json'))
        old = json.loads(archive.read('basis/zweig.json'))
        windows = json.loads(archive.read('basis/vorversuch.json'))['CST']['x_fenster']
    case, fixed = witness['case'], witness['fixed_rounded']
    assert list(map(F, fixed['normalized_future_64w'])) == [
        F('1.006543'), F('0.96181039'), F('0.95090962'), F(1)]
    relation = set(map(tuple, old['order']))
    relation.update((i, j) for i in (0, 1, 2) for j in (15, 16))
    relation.add((15, 16))
    relation.update((i, j) for i in (15, 16) for j in old['future'])
    relation.update((i, 17) for i in case['old_past_of_h'])
    relation.update((i, 18) for i in case['old_past_of_r'])
    assert case['h_before_r']
    relation.add((17, 18))
    relation.update((i, j) for i in (17, 18) for j in case['old_future_of_h_and_r'])
    assert all(i != j for i, j in relation)
    assert all((i, k) in relation for i, j in relation for l, k in relation if j == l)
    clocks = {}
    for node, ends in fixed['Y'].items():
        xs = [(F(t) + 2 - e) / (4 - e) for t in ends for e in E]
        clocks[int(node)] = (min(xs), max(xs))
    return Background(relation, set(old['past']), set(old['future']), clocks,
                      {int(k): tuple(map(F, w)) for k, w in fixed['w'].items()},
                      [tuple(map(F, w)) for w in windows])


def select(bg):
    selected = []
    for low, high in bg.windows:
        possible, definite = [], []
        for n in bg.nodes:
            w0, w1 = bg.weights[n]
            x0, x1 = bg.clocks[n]
            if w1 > 0 and x0 <= high and x1 >= low:
                possible.append(n)
                if w0 > 0 and low <= x0 <= x1 <= high:
                    definite.append(n)
        if len(possible) != 1 or possible != definite:
            raise ValueError('unresolved material window')
        selected.append(definite[0])
    if tuple(selected) not in bg.relation:
        raise ValueError('disconnected material windows')
    return tuple(selected)


def operators(bg):
    n = len(bg.nodes)
    assert bg.nodes == list(range(n))
    b = [[0] * n for _ in range(n)]
    h = [[F(0)] * n for _ in range(n)]
    for k in range(n):
        b[k][k] = -1
    for i, j in bg.relation:
        size = sum((i, k) in bg.relation and (k, j) in bg.relation for k in bg.nodes)
        value = LAYERS[size] if size < len(LAYERS) else 0
        b[j][i] = value
        half = F(value, 2)
        h[j][j] -= half
        h[i][i] -= half
        h[j][i] += half
        h[i][j] += half
    return b, h
