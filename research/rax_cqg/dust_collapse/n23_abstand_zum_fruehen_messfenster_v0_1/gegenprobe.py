"""Check arithmetic, positive controls and a different covering of the larger interval."""
from fractions import Fraction as Q
from pathlib import Path
from subprocess import run
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from intervall import I, S, box, point
from modellkontrolle import SIDES
from pruefen import MARGIN
from reduktion import ROOT, System, source
from zweige import ALLOWED_A, V, Empty, Singular, prerequisites, test


def check_endpoints():
    intervals = [box(*p) for p in [("-7.59", "-7.42"), ("-.5", "0"), ("-.8", ".25"),
                                      ("0", ".2"), ("2.35", "2.45"), ("19", "19")]]
    intervals += [point(Q(1, 7)), point(Q(-2, 11)), point(0)]
    for a in intervals:
        x = [Q(a.l, S), Q(a.h, S)]
        for b in intervals:
            y = [Q(b.l, S), Q(b.h, S)]
            ops = [(a + b, [v + w for v in x for w in y]),
                   (a - b, [v - w for v in x for w in y]),
                   (a * b, [v * w for v in x for w in y])]
            if b.h < 0 or b.l > 0:
                ops.append((a / b, [v / w for v in x for w in y]))
            for result, values in ops:
                assert Q(result.l, S) <= min(values) <= max(values) <= Q(result.h, S)
        squared = a.sq()
        extrema = [v*v for v in x] + ([Q(0)] if a.l <= 0 <= a.h else [])
        assert Q(squared.l, S) <= min(extrema) <= max(extrema) <= Q(squared.h, S)
        if a.h >= 0:
            root = a.sqrt()
            assert 0 <= Q(root.l, S)**2 <= max(0, x[0])
            assert Q(root.h, S)**2 >= x[1]


def partition(a, numerator, denominator):
    cut = a.l + (a.h - a.l) * numerator // denominator
    assert a.l < cut < a.h
    return I(a.l, cut), I(cut, a.h)


def alternate_cover(system):
    """Cover the same rectangle, change both split direction and partition ratio."""
    todo = [(ALLOWED_A, system.window, 0)]
    leaves = 0
    while todo:
        a, z, depth = todo.pop()
        try:
            test(system, a, z)
        except Empty:
            leaves += 1
            continue
        except Singular:
            pass
        if depth >= 65 or leaves >= 200000:
            raise RuntimeError("Zweite Abdeckung unvollständig")
        if 19 * (a.h - a.l) > z.h - z.l:
            todo.extend((half, z, depth + 1) for half in partition(a, 2, 5))
        else:
            todo.extend((a, half, depth + 1) for half in partition(z, 3, 5))
    return leaves


def replay_parent():
    with TemporaryDirectory() as work:
        with ZipFile(ROOT / "basis/Innenfelder.zip") as archive:
            archive.extractall(work)
        for name in ("pruefen.py", "gegenprobe.py"):
            run([sys.executable, "-B", str(Path(work) / name)], cwd=work, check=True)


def controls():
    pair, parent = source()
    check_endpoints()
    for family in (14, 18):
        for side in SIDES:
            system = System(pair, side, family, MARGIN)
            prerequisites(system)
            sol = parent["solutions"][f"{family}_{side}"]
            y = [box(*v) for v in sol["y"]]
            twin = (y[17] - y[20]) / 2
            assert V.l <= twin.l <= twin.h <= V.h
            assert system.window.l < y[22].l <= y[22].h < system.window.h
            assert y[18].h < point("1.18").l
            # Impose no condition on the positive-event time for this positive control.
            a, z, p, b, t, w21 = test(system, y[16], y[22], require_contact=False)
            for j, observed in [(16, a), (22, z), (19, p), (18, b), (21, t)]:
                assert max(observed.l, y[j].l) <= min(observed.h, y[j].h)
            weight = box(*sol["w"][21]) * (16 if side == "light" else 1)
            assert max(w21.l, weight.l) <= min(w21.h, weight.h)
            leaves = alternate_cover(system)
            print(f"{family}/{side}: Positivkontrolle bestanden, alternative Abdeckung mit {leaves} Endboxen.")
    replay_parent()


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Ohne -O ausführen")
    controls()
