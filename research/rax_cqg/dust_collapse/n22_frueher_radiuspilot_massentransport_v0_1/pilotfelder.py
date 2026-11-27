"""Read pinned input field boxes and enumerate the transport paths."""
from contextlib import contextmanager
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import json
import sys

ROOT = Path(__file__).resolve().parent
PARENT_SHA = "876e51f089dfc555363ab427fa11a9219fc594f8db881e4c7a2595b0458ef29b"
PAST = (0, 1, 2, 3)
FUTURE = (7, 8, 9, 10)
HALF = F(1, 2)
H = F(1, 32)


@contextmanager
def archive():
    path = ROOT / "basis/Randimpulse.zip"
    assert sha256(path.read_bytes()).hexdigest() == PARENT_SHA
    with TemporaryDirectory() as work, ZipFile(path) as z:
        z.extractall(work)
        sys.path.insert(0, work)
        from versuch import inputs
        sequel = json.loads((Path(work)/"Ergebnisse.json").read_text())
        with inputs() as (previous, (_, _, coeff, free, rel, goals, _)):
            rows = [("Feld", row["fixed"], row) for row in previous["witnesses"]]
            rows.extend(("Impuls", row["pair"], row) for row in sequel["cases"])
            assert len(rows) == 81
            yield rows, set(rel), coeff, free, goals


def read_box(row):
    y, w = ([tuple(map(F, b)) for b in row[key]] for key in ("y", "w"))
    width = (y[7][0]-y[3][1], y[7][1]-y[3][0])
    assert width[0] > 0
    x = []
    for lo, hi in y:
        bounds = [v/d for v in (lo-y[3][1], hi-y[3][0]) for d in width]
        x.append((min(bounds), max(bounds)))
    x[3], x[7] = (F(0), F(0)), (F(1), F(1))
    positive = {j for j, (lo, _) in enumerate(w) if lo > 0}
    assert all(w[j] == (0, 0) for j in set(range(22))-positive)
    for j in positive - set(PAST+FUTURE):
        assert 0 < x[j][0] <= x[j][1] < 1 and not (x[j][0] <= HALF <= x[j][1])
    nodes = sorted(positive - set(PAST+FUTURE))
    return x, w, positive, nodes


def paths(nodes, order):
    def extend(chain):
        yield chain
        for j in nodes:
            if (chain[-1], j) in order:
                yield from extend(chain+(j,))
    chains = sorted(p for j in nodes for p in extend((j,)))
    # A comparable subset admits exactly one path in its order direction.
    expected = {frozenset(group) for n in range(1, len(nodes)+1)
                for group in combinations(nodes, n)
                if all((a,b) in order or (b,a) in order for a,b in combinations(group,2))}
    assert len(chains) == len(expected) and {frozenset(p) for p in chains} == expected
    return chains


def shares(chain, x):
    cuts = [(F(0), F(0))]
    for a,b in zip(chain, chain[1:]):
        cuts.append(((x[a][0]+x[b][0])/2, (x[a][1]+x[b][1])/2))
    cuts.append((F(1), F(1)))
    durations = [(r[0]-l[1], r[1]-l[0]) for l, r in zip(cuts, cuts[1:])]
    assert all(l > 0 for l, _ in durations)
    assert sum(v[0] for v in durations) <= 1 <= sum(v[1] for v in durations)
    return dict(zip(chain, durations, strict=True))
