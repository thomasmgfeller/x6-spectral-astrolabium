"""Exakter Kontrollfall im bedingten N15-Skalarrandraum aus PR 336.

Aufruf: python3 -B pruefe_typ_375841.py /pfad/zu/joint_charge_distribution_v0_1
Benötigt nur Python 3 und die drei mit SHA-256 geprüften Quelldateien der Studie.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import sys

SOURCE_HASHES = {
    "coherence.py": "66c7e632c09559b87a4791ada16f601826ef431404e5237a5375c67012e46c8d",
    "tube.py": "b062243d601780511e87504ac980961d9c8016348aafe82ea90764550f564701",
    "support.py": "19a1ef8caef8f371f53984604b00d32e1af8f95b4d9c9756713cfbab2b36bc61",
}


def audit(study):
    sync = study.resolve() / "inputs" / "sync"
    for name, expected in SOURCE_HASHES.items():
        actual = sha256((sync / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Unerwartete Quelldatei: {name}")
    sys.path.insert(0, str(sync))
    from coherence import add, bounds as point, mul, phase_box, sub
    from support import DELTA, I, PAST, WINDOWS, fractions_on_paths, geometry
    from tube import template

    code = 375841
    mass, rho = Q(1, 4), Q(1, 8)
    paths, u, du, eps, f_min, f_max = template(code)
    _, relation = geometry(code)
    assert WINDOWS == ((Q(-3, 32), Q(-1, 32)), (Q(1, 32), Q(3, 32)))
    assert du == Q(1, 64) and eps == Q(1, 100)
    assert all(0 < v - du < v < v + du < 1 for v in u.values())
    assert all(u[i] + du < u[j] - du for i, j in relation if i in u and j in u)
    assert 0 < rho - Q(1, 32) < rho < rho + Q(1, 32) < 1
    assert 0 < DELTA[0] ** 4 <= Q(3, 722) <= DELTA[1] ** 4

    # Vollständige Uhren- und Dichtebox bei der leichten Masse, auf beiden Lappen.
    span = sub(mul(point(4), DELTA), (WINDOWS[0][0], WINDOWS[1][1]))
    assert span[0] > 0 and mass * span[1] * max(f_max) * (1 + eps) < 1
    assert mass * span[0] * min(f_min) * (1 - eps) > 0
    profile = {
        "clock_center": {str(k): str(v) for k, v in u.items()},
        "clock_halfwidth": str(du),
        "dwell_affine_ranges_per_vertex": {
            str(k): list(map(str, pair)) for k, pair in zip(I, zip(f_min, f_max))
        },
    }
    phase = []
    for left, right in WINDOWS:
        h = (right - left) / 8
        phase.extend(phase_box(relation, (left + j*h, left + (j+1)*h),
                               rho, mass, profile) for j in range(8))
    lower = min(a for a, b in phase)
    upper = max(b for a, b in phase)
    assert Q(-765, 1000) < lower <= upper < Q(-356, 1000)
    width = upper - lower
    assert width < Q(409, 1000)
    # Re(exp(i(S-Mitte))) >= 1-width^2/8 auf der gesamten Box.
    assert 1 - width**2 / 8 > Q(979, 1000)

    # Innenpunkte: u sind die Boxzentren; w_v = M D f_v(u).
    f_center = fractions_on_paths(paths, u)
    assert sum(f_center) == 1 and len(f_center) == 7 and min(f_center) > 0
    inv_delta = (1/DELTA[1], 1/DELTA[0])
    for window, shift, enclosure in (
        (WINDOWS[0], Q(-5, 64), (Q(-6717, 10**6), Q(-6716, 10**6))),
        (WINDOWS[1], Q(1, 16), (Q(52692, 10**6), Q(52693, 10**6))),
    ):
        assert window[0] < shift < window[1]
        e = mul(point(shift), inv_delta)
        D = sub(mul(point(4), DELTA), point(shift))
        Y = {i: point(Q(i - 5)) for i in PAST}
        Y[3] = add(Y[3], e)
        for k in I:
            Y[k] = add(point(-2 + 4*u[k]), mul(point(1-u[k]), e))

        p = point(0)
        for k, weight in zip(I, f_center):
            w = mul(point(mass * weight), D)
            assert 0 < (1-eps)*w[0] and (1+eps)*w[1] < 1
            assert (1-eps)*w[1] < w[0] <= w[1] < (1+eps)*w[0]
            total = point(0)
            for i in PAST:
                assert (i,k) in relation
                n = sum((i,v) in relation and (v,k) in relation for v in range(15))
                b = (1, -9, 16, -8)[n] if n < 4 else 0
                total = add(total, mul(point(b), sub(Y[i], Y[k])))
            p = add(p, mul(w, total))
        p = mul(p, mul(point(Q(1, 19)), inv_delta))
        assert enclosure[0] < p[0] <= p[1] < enclosure[1]
        print(f"delta={shift}, {enclosure[0]} < p < {enclosure[1]}")
    print("Gemeinsame Staubphasenspanne < 409/1000 rad; gedrehter Realteil > 979/1000.")


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Diese Prüfung benötigt aktive Assertions.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("study", type=Path)
    audit(parser.parse_args().study)
