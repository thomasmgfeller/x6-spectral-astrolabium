"""Exact certificate and an independent sliding-window quadrature, Python 3.10+."""
import argparse
from collections import Counter
import cmath
from fractions import Fraction as F
from hashlib import sha1, sha256
import json
from math import exp, log, pi, sin
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "quellen"
sys.path.insert(0, str(SOURCE))
from intervalle import I, cis
from modell import INNER_MEANS, clocks
from ordnung import ORDER, PAST, INNER, pairs_from_intervals

EDGES = pairs_from_intervals()
ETA = F(1, 100)
T = F(1, 608)
DELTA = I.of(F(3, 722)).sqrt().sqrt()
CUTOFF = ORDER.index(11)


def require(test, message):
    if not test:
        raise ValueError(message)


def source_check():
    info = json.loads((SOURCE / "herkunft.json").read_text())
    for name, rec in info["files"].items():
        data = (SOURCE / name).read_bytes()
        git_id = sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(git_id == rec["git_blob"] and sha256(data).hexdigest() == rec["sha256"], name)
    for plan in ("pruefplan", "quadraturplan", "paarungsplan"):
        expected = (ROOT / (plan+".sha256")).read_text().split()[0]
        require(sha256((ROOT / (plan+".txt")).read_bytes()).hexdigest() == expected, plan)
    source = json.loads((SOURCE / "p3.json").read_text())
    status = Counter(row["execution"] for row in source if row["checkpoint_id"] == "P3")
    require(len(source) == 60 and status == {"NOT_RUN": 60}, "P3")
    return info["commit"], dict(status)


def ownership():
    rank = {j: k for k, j in enumerate(ORDER)}
    by_rank = {(i, j): (1, -9, 16, -8)[rank[j]-rank[i]-1]
               for i in ORDER for j in ORDER if 1 <= rank[j]-rank[i] <= 4}
    require(by_rank == EDGES, "Lokale direkte Layerzählung")
    incoming = {i: b for (i, j), b in EDGES.items() if j == 11}
    require(incoming == {3: -8, 4: 16, 5: -9, 6: 1}, "Vier gespeicherte Uhren")
    require([i for i in PAST if i in incoming] == [3], "Genau ein äusseres Eingangspaar")
    # Enumerate decompositions into three nonempty consecutive pieces.
    splits = 0
    for c in range(1, len(ORDER)-1):
        for d in range(c+1, len(ORDER)):
            pieces = (ORDER[:c], ORDER[c:d], ORDER[d:])
            counts = Counter(edge for piece in pieces for edge in EDGES if edge[1] in piece)
            require(counts == Counter({edge: 1 for edge in EDGES}), "Doppelte oder fehlende Phase")
            splits += 1
    after = sorted([list(edge) for edge in EDGES if edge[0] in (3, 4) and rank[edge[1]] > CUTOFF])
    require(after == [[4, 12]], "Spätfolge der Steuerung")
    contract = json.loads((SOURCE / "verklebung.json").read_text())
    require(contract["parameters"]["scalar_mass"] == 0, "Skalarvertrag")
    return {"active_pairs": len(EDGES), "three_piece_partitions": splits,
            "incoming_at_11": dict(sorted(incoming.items())), "continuing_affected_edges": after}


def local_action():
    # Store direction coefficients for the incoming clocks until site 11 only.
    direction = {3: 2, 4: 1}
    edges = [(i, b) for (i, j), b in EDGES.items() if j == 11]
    linear_target = sum(b * direction.get(i, 0) for i, b in edges)
    raw_square = sum(b * direction.get(i, 0)**2 for i, b in edges)
    require((linear_target, raw_square) == (0, -16), "Lokale Richtungskoeffizienten")
    comparisons = 0
    for e in (F(-1, 4), F(1, 4)):
        for shift in (F(-1, 128), F(0), F(1, 128)):
            u = [m + (-1)**i*shift for i, m in enumerate(INNER_MEANS)]
            y = clocks(e, u)
            g = y[4]-y[3]
            for target in ORDER:
                rank = ORDER.index(target)
                for d in (F(-1, 16), F(0), F(1, 11)):
                    # Direct, finite difference of the two whole single-density actions.
                    a0 = a1 = -F(1, 2)
                    for lag, coef in enumerate((1, -9, 16, -8), 1):
                        if lag <= rank:
                            i = ORDER[rank-lag]
                            gap = y[target]-y[i]
                            moved = d*direction.get(i, 0) if target == 11 else 0
                            a0 -= F(coef, 38)*gap**2
                            a1 -= F(coef, 38)*(gap-moved)**2
                    expected = F(8, 19)*(d*d-2*g*d) if target == 11 else 0
                    require(a1-a0 == expected, "Direkte Vergleichswirkung")
                    comparisons += 1
    for sign in (-1, 1):
        # d² = 2 g d + sign/(256D) in the quotient polynomial ring.
        require(F(8, 19)*sign/256 == sign*T, "Armphase nach Eliminieren der Wurzel")
    duration = I( (4*DELTA-F(3, 32)).lo, (4*DELTA+F(3, 32)).hi)
    gap = duration/DELTA * I(I.of(F(7, 64)).lo, I.of(F(9, 64)).hi)
    radicand = gap**2 - 1/(256*duration)
    require(radicand.lo > 0, "Steuerung auf ganzer Präparation")
    max_shift = 2/(256*duration*(gap + radicand.sqrt()))
    require(max_shift.hi < I.of(F(1, 80)).lo, "Beide Verschiebungen beschränkt")
    # The target-only clock source is blind when the four incoming weighted clocks sum to zero.
    u = list(INNER_MEANS)
    u[0] -= F(1, 128)
    y = clocks(F(1, 4), u)
    require(sum(b for _, b in edges) == 0 and sum(b*y[i] for i, b in edges) == 0,
            "Zieluhr allein am zulässigen Blindpunkt")
    # A phase with persistent shifts on memory 4 also changes the next target.
    duration0 = F(15, 4)*DELTA
    y = clocks(F(1, 4), INNER_MEANS)
    g0, gap12 = y[4]-y[3], y[12]-y[4]
    displacements = {s: -s/(256*duration0*(g0+(I.of(g0**2)+s/(256*duration0)).sqrt()))
                     for s in (-1, 1)}
    dplus, dminus = displacements[1], displacements[-1]
    extra_per_x12 = F(-8, 38)*duration0*(dplus-dminus)*(2*gap12-dplus-dminus)
    require(extra_per_x12.lo > 0, "Auslaufen auf 12")
    return {"direct_basis_comparisons": comparisons, "linear_target": linear_target,
            "weighted_square": raw_square, "arm_frequencies": [-T, T],
            "lower_radicand_bound": F(radicand.rounded(10)[0]),
            "upper_abs_shift_of_clock3": F(max_shift.rounded(10)[1]),
            "leak_phase_per_x12_at_centre": extra_per_x12.rounded(12),
            "target_only_blind_u4": u[0]}


def sliding_null():
    # x0=1/8. Analytic lower bounds use log((1+eta)/(1-eta))>2eta and pi<22/7.
    fmin, fmax = F(7, 64), F(9, 64)
    bmax = (1+ETA)*fmax
    omega_upper = F(44, 7)/(2*ETA)
    require(1+omega_upper**2 < 315**2, "Frequenzschranke")
    arm_min = T/315 - T**2*(2*fmax)/4
    sine_min = T/315 - T**3*bmax**2/6
    require(arm_min > F(5, 1000000) and sine_min > F(52, 10000000), "Nullzeuge")
    # Independent evaluation on log(x), Simpson (with endpoints); only the
    # inequality above is used as a certificate. Ratios are divided by band width.
    L = log(float((1+ETA)/(1-ETA)))
    omega = 2*pi/L
    rows = []
    for f in (fmin, F(1, 8), fmax):
        a, b = float((1-ETA)*f), float((1+ETA)*f)
        base = cmath.exp(1j*omega*log(a*8))
        values = []
        for n in (256, 512):
            unshifted = sine_mode = 0j
            for k in range(n+1):
                s = k/n
                w = (1 if k in (0, n) else 4 if k%2 else 2)/(3*n)
                value = base*cmath.exp(2j*pi*s)
                unshifted += w * value
                sine_mode += w * value * sin(float(T)*a*exp(L*s))
            null = abs(unshifted)*L/(b-a)
            sine_abs = abs(sine_mode)*L/(b-a)
            require(null < 1e-13 and sine_abs > float(sine_min), "Quadratur des Nullzeugen")
            values.append(sine_abs)
        require(abs(values[0]-values[1]) < 5e-13, "Gittervergleich")
        rows.append({"f": f, "normalized_sine_abs": round(values[-1], 12)})
    return {"f_range": [fmin, fmax], "omega_upper": omega_upper,
            "normalized_each_arm_lower": arm_min, "normalized_sine_mode_lower": sine_min,
            "quadrature": rows}


def run():
    commit, statuses = source_check()
    return {"commit": commit, "ownership": ownership(), "insert": local_action(),
            "reduction": sliding_null(), "pairing": pairing(), "P3": statuses}


def pairing():
    f = F(1, 8)
    x0, x1 = f-F(1, 1600), f+F(1, 1600)
    require((1-ETA)*f < x0 < x1 < (1+ETA)*f, "Gleiche bedingte Dichtezelle")
    angle = T*(x1-x0)
    defect = 1-cis(I.of(angle)).re
    # Independent real Taylor bounds on 1-cos(angle).
    lower, upper = angle**2/2-angle**4/24, angle**2/2
    require(defect.hi >= I.of(lower).lo and defect.lo <= I.of(upper).hi, "Kosinus")
    diagonal = cis(I.of(0)).re
    require(defect.lo > 0 and diagonal.lo <= I.of(1).lo <= diagonal.hi, "Kreuzpaarung")
    return {"densities": [x0, x1], "relative_loss_of_cross_term": defect.rounded(16)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = json.dumps(run(), default=str, indent=2, ensure_ascii=False) + "\n"
    if args.json:
        print(result, end="")
    else:
        require(result == (ROOT/"exakt.json").read_text(), "Archivierte Ergebnisse")
        print("PASS · Quellen, Schnittzerlegungen, Uhreinfügung, Gültigkeitsbereich und Nullzeuge")
