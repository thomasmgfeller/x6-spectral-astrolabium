"""Recompute the exterior phase-access test. Python 3.10+, standard library."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha1, sha256
from itertools import combinations_with_replacement, product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "quellen"
sys.path.insert(0, str(SOURCE))

from intervalle import I, S, cis
from modell import H, INNER_MEANS, clocks, dwell
from ordnung import INNER, ORDER, PAST, pairs_from_intervals
from randquelle import fine_check, profile

SIGNS = tuple(product((-1, 1), repeat=2))
V = dict(zip(PAST, (F(29, 64), F(23, 64), F(16, 64), F(8, 64))))
U = dict.fromkeys(PAST, 1)
EDGES = pairs_from_intervals()
LEFT = ORDER[:ORDER.index(11) + 1]
E = F(1, 4)


def check(condition, message):
    if not condition:
        raise ValueError(message)


def provenance():
    entry = json.loads((SOURCE / "herkunft.json").read_text())
    for name, info in entry["files"].items():
        data = (SOURCE / name).read_bytes()
        git_id = sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        check(git_id == info["git_blob"], "Git blob: " + name)
        check(sha256(data).hexdigest() == info["sha256"], "SHA-256: " + name)
    for plan_name in ("pruefplan.json", "ergaenzungsplan.txt"):
        plan_file = ROOT / plan_name
        expected = plan_file.with_suffix(".sha256").read_text().split()[0]
        check(expected == sha256(plan_file.read_bytes()).hexdigest(), plan_name)
    return entry["commit"]


def response_column(target, y):
    """A,B divided by h sqrt(D), and chi divided by h², per unit of x_j."""
    a = b = mixed = F(0)
    for (i, j), weight in EDGES.items():
        if j != target:
            continue
        du = U.get(j, 0) - U.get(i, 0)
        dv = V.get(j, 0) - V.get(i, 0)
        c = -F(weight, 19)
        a += c * (y[j] - y[i]) * du
        b += c * (y[j] - y[i]) * dv
        mixed += c * du * dv
    return a, b, mixed


def direct(target, y, z, signs):
    """Independent single-density action, z=sqrt(D); count layers by chain rank."""
    sigma, tau = signs
    shifted = {j: z * y[j] + H * (sigma * U.get(j, 0) + tau * V.get(j, 0)) for j in ORDER}
    rank = ORDER.index(target)
    action = -z**2 / 2
    for lag, coefficient in enumerate((1, -9, 16, -8), start=1):
        if lag <= rank:
            gap = shifted[target] - shifted[ORDER[rank - lag]]
            action -= F(coefficient, 38) * gap**2
    return action


def check_phase_response():
    check(V == profile(11), "Selektives Profil")
    check(fine_check()["anzahl_endliche_vergleiche"] == 45, "Referenztest")
    y = clocks(E, INNER_MEANS)
    checks = 0
    for j in ORDER:
        a, b, mixed = response_column(j, y)
        check(mixed == F(j == 11, 19), "Gemischter Koeffizient")
        if j not in LEFT:
            check((a, b, mixed) == (0, 0, 0), "Späte Quellenabhängigkeit")
        # The phase is a polynomial of degree <= 2 in z. Three rational points suffice.
        for z in (F(3, 4), F(1), F(5, 4)):
            samples = {s: direct(j, y, z, s) for s in SIGNS}
            mean = sum(samples.values()) / 4
            for (s, t), value in samples.items():
                check(value == mean + H*z*(s*a + t*b) + H**2*s*t*mixed, "Direkte Wirkung")
                checks += 1
    a4, b4, _ = response_column(4, y)
    a5, b5, _ = response_column(5, y)
    determinant = a4*b5 - a5*b4
    check(determinant != 0 and b4 != 0, "Zwei unabhängige Störphasen")
    # Explicitly perturb the two cells inside their published independent jitter windows.
    centres = dwell(INNER_MEANS)
    for j in (4, 5):
        check(F(1, 10000) < centres[j]/100, "Dichtevariation muss zulässig sein")
    return {"direct_phase_comparisons": checks, "upstream_fine_checks": 45,
            "scaled_jacobian_rows_A_B_cols_x4_x5": [[a4, a5], [b4, b5]],
            "scaled_determinant": determinant, "chi_over_h_squared_x11": F(1, 19)}


def signature(seq):
    return tuple(sum(values) for values in zip(*[(a, b, a*b) for a, b in seq]))


def phase_codes():
    result = {}
    for n in (1, 2):
        groups = defaultdict(set)
        for seq in combinations_with_replacement(SIGNS, n):
            a, b, mixed = signature(seq)
            groups[a, b].add(mixed)
        distinct = {str(key): sorted(values) for key, values in groups.items() if len(values) > 1}
        result[str(n)] = {"distinct_nuisance_frequencies": len(groups),
                          "same_nuisance_different_mixed": distinct}
    check(not result["1"]["same_nuisance_different_mixed"], "Einmaliger Zugriff")
    check(result["2"]["same_nuisance_different_mixed"] == {"(0, 0)": [-2, 2]}, "Doppelzugriff")
    even = ((1, 1), (-1, -1))
    odd = ((1, -1), (-1, 1))
    y = clocks(E, INNER_MEANS)
    for z in (F(3, 4), F(1), F(5, 4)):
        for j in ORDER:
            phase = sum(direct(j, y, z, s) for s in even) - sum(direct(j, y, z, s) for s in odd)
            check(phase == 4*H**2*F(j == 11, 19), "Differenz des Zweifachzugriffs")
    # Histories with equal x11 and all clocks but a different admissible x4.
    eps = F(1, 10000)
    _, b4, _ = response_column(4, y)
    for z in (F(3, 4), F(1), F(5, 4)):
        offset = eps*(direct(4, y, z, even[0]) - direct(4, y, z, odd[0]))
        check(offset == 2*H*z*b4*eps and offset != 0, "Unabhängige Geschichten")
    result["contrast_phase_per_x11"] = 4*H**2/19
    result["independent_histories_residual_per_sqrt_D"] = 2*H*b4*eps
    return result


def witness():
    delta = I.of(F(3, 722)).sqrt().sqrt()
    duration = (4-E)*delta
    z = duration.sqrt()
    check((E*delta).lo > I.of(F(1, 32)).hi and (E*delta).hi < I.of(F(3, 32)).lo,
          "Originales äusseres Fenster")
    xs = []
    for sign in (-1, 1):
        u = list(INNER_MEANS)
        u[INNER.index(12)] += sign*F(1, 80)
        check(all(abs(v-c) < F(1, 64) for v, c in zip(u, INNER_MEANS)), "Innere Fenster")
        cells = dwell(u)
        check(all(f > 0 for f in cells.values()), "Positive Zellen")
        xs.append(cells)
    check([j for j in INNER if xs[0][j] != xs[1][j]] == [11, 13], "Zellunterschiede")
    check(set(i for i, j in EDGES if j == 11 and i in PAST) == {3}, "Selektives Paar")
    check(EDGES[3, 11] == -8, "Schicht 3 -> 11")
    low, high = [cells[11] for cells in xs]
    check((low, high) == (F(19, 160), F(21, 160)), "Zieldichten")
    y = clocks(E, INNER_MEANS)
    g = y[11]-y[3]
    v = H*(1+V[3])
    check((g*z).lo > I.of(v).hi, "Monotonie der relativen Phasen")
    # Any source dependence has ended by event 11. For both completions only x11 matters
    # in the relative channel. Check the closed formula independently by direct substitution.
    for scale in (F(3, 4), F(1), F(5, 4)):
        ref = direct(11, y, scale, SIGNS[0])
        t0 = -v
        for s, t in SIGNS:
            shift = H*(s+t*V[3])
            predicted = F(4, 19)*((g*scale-shift)**2-(g*scale-t0)**2)
            check(direct(11, y, scale, (s, t))-ref == predicted, "Relatives Spektrum")
    width = F(16, 19)*(high-low)*g*v*z
    sine = cis(width/2).im
    optimum = (1+sine)/2
    check(optimum.hi < I.of(F(5007, 10000)).lo, "Einmalige Treffergrenze")
    # Same-history double use: measuring a qubit in the sine quadrature gives this bit.
    angle = I.of(4*H**2/19)
    contrast = (cis(angle*high).im - cis(angle*low).im)/2
    check(contrast.lo > 0, "Nichtkonstantes bedingtes Bit")
    return {"low": low, "high": high, "difference": high-low, "threshold": F(1, 8),
            "g": g, "max_abs_source_shift": v, "phase_arc_rad": width.rounded(12),
            "optimal_single_use_equal_prior_probability": optimum.rounded(12),
            "conditional_two_use_sine_bit_probability_difference": contrast.rounded(12)}


def support_test():
    eta = F(1, 100)
    lower, upper = (1-eta)*F(7, 64), (1+eta)*F(9, 64)
    delta = I.of(F(3, 722)).sqrt().sqrt()
    duration = (4-E)*delta
    q = delta*H/(duration*duration.sqrt())
    margins = {}
    for sign, arm in ((1, "plus"), (-1, "minus")):
        original = F(1, 8)-sign*F(1, 160)
        check(lower < (1-eta)*original < (1+eta)*original < upper, "Offenes Jitterband")
        moved = original-sign*q/2
        margin = lower-(1+eta)*moved if sign == 1 else (1-eta)*moved-upper
        check(margin.lo > 0, "Ganzes verschobenes Jitterband ausserhalb")
        margins[arm] = margin.rounded(12)
    # Along the old global band the sine-quadrature effects are both strictly positive.
    whole = I(I.of(lower).lo, I.of(upper).hi)
    angle = whole/304
    effect_bounds = {}
    for sign in (-1, 1):
        effect = (1 + sign*cis(angle).im)/2
        check(0 < effect.lo <= effect.hi < S, "Zeigereffekt")
        effect_bounds[str(sign)] = effect.rounded(12)
    # Laurent coefficients of |(t +/- i/t)/2|², t=exp(2 i chi).
    summed = defaultdict(complex)
    for sign in (-1, 1):
        kraus = {1: 0.5, -1: sign*0.5j}
        effect = defaultdict(complex)
        for j, amplitude in kraus.items():
            for k, other in kraus.items():
                effect[j-k] += amplitude * other.conjugate()
        check(dict(effect) == {0: 0.5, 2: -sign*0.25j, -2: sign*0.25j}, "Effektpolynom")
        for index, value in effect.items():
            summed[index] += value
    check(dict(summed) == {0: 1, 2: 0, -2: 0}, "Vollständigkeit")
    return {"original_global_band": [lower, upper], "moved_jitter_band_clearance": margins,
            "two_use_pointer_effects_on_original_band": effect_bounds}


def compute():
    commit = provenance()
    p3 = json.loads((SOURCE/"p3.json").read_text())
    status = Counter(row["execution"] for row in p3 if row["checkpoint_id"] == "P3")
    check(len(p3) == 60 and status == {"NOT_RUN": 60}, "P3-Originalregister")
    return {"basis": commit, "phase": check_phase_response(), "codes": phase_codes(),
            "witness": witness(), "support": support_test(), "P3_source": dict(status)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ausgeben", action="store_true", help="Berechnetes JSON ausgeben")
    args = parser.parse_args()
    result = json.dumps(compute(), default=str, indent=2, ensure_ascii=False) + "\n"
    if args.ausgeben:
        print(result, end="")
    else:
        check(result == (ROOT/"ergebnisse.json").read_text(), "Archiviertes Ergebnis")
        print("PASS · Quellen, Phasen, Rang, Frequenzen, Gegenpaar und P3-Status")
