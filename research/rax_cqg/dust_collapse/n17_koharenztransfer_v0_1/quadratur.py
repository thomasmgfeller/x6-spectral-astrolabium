"""Independent center quadrature of the recorded and erased N16 clock, type 375841.

Run python -B quadratur.py to print the deterministic JSON result. Only the
N15 packet and the Hasse-to-interval reconstruction are imported from PR 349.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json
import sys

import mpmath as mp

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "basis" / "n17"))
from gegenprobe import F, I, P, STEP, packet_family, rebuild

WIDTH = Fraction(1, 2**20)
MID = Fraction(1, 8)
TEST_WIDTHS = [Fraction(0), WIDTH / 2, WIDTH, 2 * WIDTH]
RESOLUTIONS = [(3, 65), (4, 85)]
ARMS = ("coherent", "dephased")


def number(value):
    value = Fraction(value)
    return mp.mpf(value.numerator) / value.denominator


def integrate(q, order, digits):
    with mp.workdps(digits):
        mid, density_width = number(MID), number(WIDTH)
        delta = (mp.mpf(3) / 722)**(mp.mpf(1) / 4)
        weights = rebuild("stromerhaltend")
        incoming = [[(i, w) for (i, j), w in weights.items() if j == k] for k in range(17)]
        def slope(y, k):
            return -mp.mpf("0.5") - mp.fsum(w * (y[i] - y[k])**2 for i, w in incoming[k]) / 38

        def box(s, center, radius):
            return mp.expj(center * s) * mp.sinc(radius * s)

        nodes, weights_1d = mp.gauss_quadrature(order, "legendre")
        grid = list(zip(nodes, [w / 2 for w in weights_1d]))
        # Each entry integrates one t-half with relative probability mass 1/2.
        end_nodes = [mid + (side + u)*density_width/2 for side in (-1, 1) for u, _ in grid]
        result = {w: {} for w in TEST_WIDTHS}
        _, family = packet_family(q)
        for sign, (yc, wc) in family.items():
            outer = []
            for triple in product(grid, repeat=3):
                y = [number(yc[k]) for k in range(15)] + [mp.mpf(6), mp.mpf(7)]
                for k, (u, _) in zip(F[1:], triple):
                    y[k] += u * density_width
                old_d = [slope(y, k) for k in range(15)]
                old = box(mp.fsum(old_d[k] for k in P), mid, number(Fraction(1, 32)))
                old *= mp.expj(delta * mp.fsum(number(wc[k]) * old_d[k] for k in I))
                old *= mp.fprod(box(old_d[k], mid, density_width) for k in F)
                old *= mp.fprod(w for _, w in triple)
                outer.append((y, old))
            for width in TEST_WIDTHS:
                clock_nodes = grid if width else [(mp.mpf(0), mp.mpf(1))]
                by_clock = []
                for u, w in clock_nodes:
                    # First sum amplitudes for all other histories compatible with this clock.
                    amplitudes = [mp.mpc(0) for _ in end_nodes]
                    for y, old in outer:
                        y[15] = 6 + number(width) * u
                        amp = old * box(slope(y, 15), mid, density_width)
                        final_slope = slope(y, 16)
                        for j, t in enumerate(end_nodes):
                            amplitudes[j] += amp * mp.expj(t * final_slope)
                    by_clock.append((w, amplitudes))
                # Distinct clock values interfere only in the coherent arm.
                intensities = {
                    "coherent": [abs(mp.fsum(w*a[j] for w, a in by_clock))**2
                                 for j in range(len(end_nodes))],
                    "dephased": [mp.fsum(w*abs(a[j])**2 for w, a in by_clock)
                                 for j in range(len(end_nodes))],
                }
                result[width][sign] = {}
                for arm, intensity in intensities.items():
                    halves = [mp.fsum(w*intensity[k*order+j]/2 for j, (_, w) in enumerate(grid))
                              for k in (0, 1)]
                    norm = mp.fsum(halves)
                    assert norm > number(Fraction(98, 100))
                    result[width][sign][arm] = (halves[1]/norm, norm)

        for by_sign in result.values():
            by_sign["gap"] = {arm: by_sign["positiv"][arm][0] - by_sign["negativ"][arm][0]
                              for arm in ARMS}
        return result


def main():
    if not __debug__:
        raise RuntimeError("Run without -O")
    document = {"type": 375841, "case": "stromerhaltend", "scope": "packet centers",
                "event": "t>1/8", "density_halfwidth": str(WIDTH),
                "q_sign": "positive-current probability minus negative-current probability",
                "arms": "At each t: coherent |sum w A|^2; dephased sum w |A|^2. Normalize once per arm and input.",
                "normalization": "Dust part only, with normalized integration windows and common scalar factor omitted.",
                "quadrature": [{"order": n, "decimal_digits": d} for n, d in RESOLUTIONS],
                "results": {}}
    for q in [STEP, STEP/2]:
        runs = [integrate(q, order, digits) for order, digits in RESOLUTIONS]
        with mp.workdps(85):
            rows = []
            for width in TEST_WIDTHS:
                low, high = (r[width] for r in runs)
                row = {"clock_halfwidth": str(width)}
                for arm in ARMS:
                    g_low, g_high = low["gap"][arm], high["gap"][arm]
                    assert abs(g_high - g_low) < mp.mpf("1e-48")
                    if arm == "coherent" and width:
                        assert g_high < -mp.mpf("1e-29")
                    else:
                        assert abs(g_high) < mp.mpf("1e-80")
                    stats = {}
                    for sign in ("positiv", "negativ"):
                        p, norm = high[sign][arm]
                        p_low, norm_low = low[sign][arm]
                        assert abs(p-p_low) < mp.mpf("1e-43")
                        assert abs(norm-norm_low) < mp.mpf("1e-30")
                        stats[sign] = {"p_upper": mp.nstr(p, 62), "integrated_norm": mp.nstr(norm, 45)}
                    stats["gap_order3_65"] = mp.nstr(g_low, 23)
                    stats["gap_order4_85"] = mp.nstr(g_high, 23)
                    row[arm] = stats
                if width:
                    row["coherent_gap_relative_to_h"] = mp.nstr(
                        high["gap"]["coherent"]/runs[-1][WIDTH]["gap"]["coherent"], 29)
                rows.append(row)
            document["results"][str(q)] = rows
    return document


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, indent=2))
