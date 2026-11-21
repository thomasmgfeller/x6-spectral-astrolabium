"""Rational enclosures on the entire supplementary pair of PR 342."""
from fractions import Fraction as Q
from math import isqrt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'vorarbeit'))
import schnittimpulse as cell
from randquelle import PAST, PROFILE


def certificate():
    radius = cell.ref.RADIUS
    dur, y, f, c, _ = cell.coordinates(radius, cell.SHIFT)
    difference = cell.mul(cell.sc(Q(2)*cell.M/64, dur), cell.sub(c[6], c[4]))
    assert difference[0] > 0
    # Each chain's dwell fractions telescope to one before averaging.
    # The two recentering shifts sum to zero; the seven jitters are independent.
    base = cell.mul(cell.sc(cell.M, dur), cell.box(1, 7*radius))
    amounts = (cell.add(base, cell.sc(Q(1,2),difference)),
               cell.sub(base, cell.sc(Q(1,2),difference)))
    threshold = cell.M * (4 + Q(1,4))
    assert amounts[1][1] < threshold < amounts[0][0]
    scale = 10**18
    lo = isqrt(isqrt(3 * scale**4 // 722))
    delta = (Q(lo, scale), Q(lo + 1, scale))
    assert delta[0]**4 <= Q(3, 722) < delta[1]**4
    sab_diff = cell.sc(Q(64, 19), cell.mul(delta, difference))
    signs, _, _ = cell.ranges('ohne_gesamtinformation', radius)
    assert signs[0][0] > 0 > signs[1][1]

    # S_b for the full dust action, dimensionless displacements of Y.
    # The common initial density r multiplies the entire P->P contribution.
    v = dict(zip(PAST, PROFILE))
    def coefficient(j):
        return cell.sc(-Q(1,19), cell.total(
            cell.sc(b*(v.get(i,0)-v.get(j,0)), cell.sub(y[i],y[j]))
            for (i,k), b in cell.B.items() if k == j and i in PAST))
    exterior = cell.mul((Q(3,32), Q(5,32)), cell.total(coefficient(j) for j in PAST))
    assert all(coefficient(j) == cell.ZERO for j in cell.F)
    densities = {j:cell.mul(cell.mul(delta, cell.sc(cell.M, dur)),
                             cell.mul((Q(99,100), Q(101,100)), f[j])) for j in cell.I}
    sb = cell.add(exterior, cell.total(cell.mul(densities[j], coefficient(j)) for j in cell.I))
    # |delta(S_a S_b)| <= Delta*(max|p+| + max|p-|)*max|S_b|.
    product_error = delta[1] * sum(max(map(abs, interval)) for interval in signs) * max(map(abs, sb))
    phase = cell.dust_phase()
    assert -Q(5,8) < phase[0] <= phase[1] < 0
    cosine_lower = 1 - max(map(abs, phase))**2 / 2
    sine_upper = max(map(abs, phase))
    response_lower = cosine_lower * sab_diff[0] - sine_upper * product_error
    assert response_lower > 0
    return {
        'delta_W': difference, 'W_intervalle_je_paket':amounts,
        'schwelle_fuer_dieses_paar':threshold, 'delta_S_ab': sab_diff, 'p_intervalle': signs,
        'S_b_einschluss': sb, 'betrag_differenz_SaSb_obere_schranke': product_error,
        'S_d': phase, 're_minus_i_gemischte_amplitudenantwort_untere_schranke':response_lower
    }
