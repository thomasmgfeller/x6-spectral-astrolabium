"""Rational whole-packet error bounds for one-birth extensions of type 375841."""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "basis" / "port"))
import zertifikat as old
from optimal import packet_approximation

P, I, F = old.P, old.I, old.F
H, R = old.H, old.RADIUS
MID = Q(1, 8)
OUT = 15
YN = Q(6)
LAYERS = (1, -9, 16, -8)
CASES = {
    "minimal": frozenset(P + (6,)),
    "abgeschirmt": frozenset(range(15)),
    "stromerhaltend": frozenset(P + (6, 11, 12, 13)),
}


def new_edges(past):
    """A past element's old successors in the ideal form its open interval to n."""
    assert all(i in past for i, j in old.ORDER if j in past)
    result = {}
    for i in sorted(past):
        between = sum((i, k) in old.ORDER for k in past)
        if between < len(LAYERS):
            result[i] = LAYERS[between]
    return result


def slope(weights, y):
    return -Q(1, 2) - sum(b * (y[i] - YN)**2 for i, b in weights.items()) / 38


def old_coefficient(y):
    return {j: v[0] for j, v in old.coefs({i: old.box(t) for i, t in y.items()}).items()}


def packet_family(q_abs):
    frozen, _ = old.centers()
    # Undo the known positive-q deformation to retrieve the neutral preparation.
    yy, ww = frozen["negativ"]
    neutral_y = yy.copy()
    neutral_y[6] = (yy[6] + frozen["positiv"][0][6]) / 2
    neutral_w = ww.copy()
    earlier = json.loads((HERE / "basis/port/basis/pr344_ergebnis.json").read_text())
    transfer = Q(earlier["ergaenzung_gegenpaar_gleicher_wirkung"]["transfer_6_nach_4"][0])
    neutral_w[4] += 10 * old.STEP - transfer
    neutral_w[6] += transfer
    neutral_w[12] -= 9 * old.STEP
    neutral_w[13] -= old.STEP
    neutral_c = old_coefficient(neutral_y)
    total = sum(neutral_w[i] * c for i, c in neutral_c.items())
    family = {}
    for label, q in (("positiv", -q_abs), ("negativ", q_abs)):
        y, w = neutral_y.copy(), neutral_w.copy()
        y[6] += 9 * q * (y[13] - y[12]) / w[11]
        w[4] -= 10 * q
        w[12] += 9 * q
        w[13] += q
        c = old_coefficient(y)
        shift = (total - sum(w[i] * c[i] for i in c)) / (c[4] - c[6])
        w[4] += shift
        w[6] -= shift
        assert sum(w[i] * c[i] for i in c) == total
        family[label] = y, w
    if q_abs == old.STEP:
        assert family == frozen
    return neutral_y, family


def budget(weights, center, region):
    # For each fixed set of outer dust values (including v, w7, common entrance
    # density), bound the phase perturbation over the old 15 independent axes.
    yy, _ = center
    legacy = packet_approximation(center, region["staubphase"])
    uniform = legacy["phasenabweichung_sup"]
    mean = legacy["phasenmittel_betrag_max"]
    for i, b in weights.items():
        if i not in I + (3,):
            continue
        coef = (MID + H) * abs(b) / 38
        uniform += coef * (2 * abs(yy[i] - YN) * R + R**2)
        mean += coef * R**2 / 3
    err = mean + uniform**2 / 2
    width = region["staubphase"][1] - region["staubphase"][0]
    cone = 1 - width**2 / 8
    assert cone > Q(99, 100)
    # At each fixed new v and retained old z the ideal added phase is a single
    # unit factor at the old center. Average w7 and entrance density first.
    return {"max_phasenfehler": uniform, "max_mittlere_phasenabweichung": mean,
            "amplitudenfehler_je_paketmass": err, "norm_unten_zentrum": cone,
            "spurabstand_zum_zentrum_max": 2 * err / cone}


def input_correction(weights, yy):
    # p=-dS/d(physical clock displacement of ALL old input clocks).
    linear = old.total(old.sc(weights[i], old.sub(old.box(yy[i], R if i == 3 else 0),
                                                   old.box(YN))) for i in P if i in weights)
    return old.sc(Q(1, 19), old.mul(old.divide(old.box(MID, H), old.DELTA), linear))


def evaluate(q_abs):
    neutral, packets = packet_family(q_abs)
    reference_old = -old_coefficient(neutral)[7] / 2
    regions = {s: old.whole_cell(p, reference_old) for s, p in packets.items()}
    assert regions["positiv"]["p"][0] > 0 > regions["negativ"]["p"][1]
    yp, wp = packets["positiv"]
    yn, wn = packets["negativ"]
    assert [j for j in sorted(yp) if yp[j] != yn[j]] == [6]
    assert all(old.B.get((6, j), 0) == 0 for j in F[1:])
    assert all(wp[j] == wn[j] for j in P + F)
    results = {}
    for name, past in CASES.items():
        weights = new_edges(past)
        reference = slope(weights, neutral)
        data = {}
        for sign, center in packets.items():
            y, _ = center
            extra = input_correction(weights, y)
            data[sign] = {"p15": regions[sign]["p"], "p16_minus_p15": extra,
                          "p16": old.add(regions[sign]["p"], extra),
                          "D_im_randzentrum": slope(weights, y),
                          "fehler": budget(weights, center, regions[sign])}
        a, b = data["positiv"], data["negativ"]
        total_error = sum(item["fehler"]["spurabstand_zum_zentrum_max"] for item in data.values())
        d = a["D_im_randzentrum"] - b["D_im_randzentrum"]
        if name == "abgeschirmt":
            assert set(weights) == set(F) and d == 0
            # The entire centered, w7-closed states are proportional as functions
            # of the remaining data, also after the common isometric v extension.
            contrast = old.box(0, total_error)
            # Fixed new port then reads multiplication by
            # [1+sin(h*(D(z)-Dref))]/2 on retained old z. Remove its constant.
            delta = sum(abs(k) * (2 * abs(neutral[i] - YN) * H + H**2) / 38
                        for i, k in weights.items() if i in F[1:])
            # osc(P(z)) <= H*delta, valid for any fixed reference Dref.
            fixed_port = old.box(0, total_error * H * delta)
            fixed_zero_reference = fixed_port
            assert a["p16"] == a["p15"] and b["p16"] == b["p15"]
        else:
            assert not (set(weights) & set(F))  # no moving retained clocks in centered slope
            angles = [H * (branch["D_im_randzentrum"] - reference) for branch in (a, b)]
            cubic = sum(abs(angle)**3 for angle in angles) / 12
            fixed_port = old.box(H * d / 2, total_error + cubic)
            # Additional check with the same literal hardware phase in all three cases.
            cubic_zero = sum(abs(H * branch["D_im_randzentrum"])**3 for branch in (a, b)) / 12
            fixed_zero_reference = old.box(H * d / 2, total_error + cubic_zero)
            assert fixed_zero_reference[0] * fixed_zero_reference[1] > 0
            contrast = None
            assert fixed_port[0] > 0 or fixed_port[1] < 0
            if name == "minimal":
                assert min(a["p16"][0], b["p16"][0]) > Q(1, 4)
            else:
                assert a["p16"] == a["p15"] and b["p16"] == b["p15"]
        results[name] = {"vorgaenger": sorted(past), "gewichte_zum_neuen_ziel": weights,
                         "D_referenz": reference, "D_plus_minus_D_minus_im_zentrum": d,
                         "pakete": data, "kontrast_des_gemeinsamen_Y_ports": fixed_port,
                         "kontrast_mit_identischem_D_stern_null": fixed_zero_reference,
                         "schranke_aller_binaeren_effekte_abgeschirmt": contrast}
    return results


def run():
    for stem in ("pruefvertrag", "ergaenzung"):
        assert sha256((HERE / (stem + ".json")).read_bytes()).hexdigest() == (
            HERE / (stem + ".sha256")).read_text().split()[0]
    return {"typ_vor_der_geburt": 375841, "schritt_physische_dichte": H,
            "urspruengliches_paar_q_2_hoch_minus_24": evaluate(old.STEP),
            "lokaler_transfer_q_2_hoch_minus_25": evaluate(old.STEP / 2),
            "P_dephasiert_beide_pakete": Q(1, 2),
            "physikalische_paarung": "HOLD", "N16_wachstumsgewichte": "nicht bestimmt"}


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Ohne -O ausführen.")
    print(json.dumps(run(), ensure_ascii=False, indent=2, default=str))
