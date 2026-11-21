"""Rational certificates for the whole two-packet test; Python standard library."""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from math import isqrt
from pathlib import Path
import json

from quellen import density_translation_375841 as ref

ROOT = Path(__file__).resolve().parent
PAST, INNER, FUTURE = ref.PAST, ref.INNER, ref.FUTURE
MASS = Q(1, 4)
FUTURE_WIDTH = Q(1, 2**20)
NODES = set(range(15))
LAYERS = (1, -9, 16, -8)


def local_coefficients(nodes, order):
    coefficients = {}
    for i, j in order:
        count = sum((i, v) in order and (v, j) in order for v in nodes)
        coefficients[i, j] = LAYERS[count] if count < 4 else 0
    return coefficients


def cut_orders():
    order, paths, global_coef = ref.local_geometry()
    # Classified by Y=0 throughout the cells (the inequalities are checked below).
    earlier = set(PAST) | {v for v in INNER if ref.CENTER[v] <= Q(2, 5)}
    seam = {v for v in earlier if not any((v, w) in order for w in earlier)}
    assert seam == {5, 11}
    later = (NODES - earlier) | seam
    old, new = earlier - seam, later - seam
    def restrict(nodes):
        return {(i, j) for i, j in order if i in nodes and j in nodes}
    lo, ro = restrict(earlier), restrict(later)
    left = local_coefficients(earlier, lo)
    right = local_coefficients(later, ro)
    # Profiles computed from local inputs only. Count each stratum separately.
    exits = {i: {s for s in seam if (i, s) in lo} for i in old}
    entries = {j: {s for s in seam if (s, j) in ro} for j in new}
    crossing = {}
    for i, j in product(sorted(old), sorted(new)):
        through = exits[i] & entries[j]
        if through:
            count = (len(through)
                     + sum((i, v) in lo and bool(exits[v] & entries[j]) for v in old)
                     + sum((v, j) in ro and bool(exits[i] & entries[v]) for v in new))
            crossing[i, j] = LAYERS[count] if count < 4 else 0
    assert not (left.keys() & right.keys())  # antichain has no internal edges
    assert left | right | crossing == global_coef
    assert (left | right) != global_coef
    assert any(b and i in PAST and j in INNER for (i, j), b in crossing.items())
    return paths, global_coef, (earlier, later, seam), (left, right, crossing)


def phase_enclosure(paths, coef):
    box, add, sub, mul = ref.box, ref.plus, ref.minus, ref.times
    scale, total, square = ref.scale, ref.add_all, ref.square
    rad = ref.RADIUS
    e = box(Q(-1, 4), rad)
    u = {v: box(ref.CENTER[v], rad) for v in INNER}
    duration = sub(box(4), e)
    unit = 10**18
    lo = isqrt(isqrt(3*unit**4//722))
    delta = (Q(lo, unit), Q(lo+1, unit))
    assert delta[0]**4 <= Q(3, 722) <= delta[1]**4
    y = {v: box(v-5) for v in PAST}
    y[3] = add(y[3], e)
    y.update({v: add(add(box(-2), e), mul(duration, u[v])) for v in INNER})
    for v in INNER:
        if ref.CENTER[v] <= Q(2, 5):
            assert y[v][1] < 0
        else:
            assert y[v][0] > 0
    y.update({v: box(v-5, FUTURE_WIDTH if v != 7 else 0) for v in FUTURE})
    c = {v: add(box(1), scale(Q(1, 19), total(
        scale(b, square(sub(y[i], y[v]))) for (i, j), b in coef.items() if j == v)))
         for v in NODES}
    dwell = {v: box(0) for v in INNER}
    for path in paths:
        ends = [box(0)] + [scale(Q(1, 2), add(u[i], u[j]))
                            for i, j in zip(path, path[1:])] + [box(1)]
        for v, a, b in zip(path, ends, ends[1:]):
            dwell[v] = add(dwell[v], scale(Q(1, len(paths)), sub(b, a)))
    # The frozen packet certificate puts BOTH translated cells inside these bands.
    weights = {v: mul(mul(scale(MASS, delta), duration),
                      mul(dwell[v], (Q(99, 100), Q(101, 100)))) for v in INNER}
    weights.update({v: box(Q(1, 8), FUTURE_WIDTH) for v in FUTURE})
    past = mul((Q(3, 32), Q(5, 32)), total(c[v] for v in PAST))
    return scale(Q(-1, 2), add(past, total(mul(weights[v], c[v]) for v in weights)))


def certificate():
    config_sum = (ROOT/'pruefvertrag.sha256').read_text().split()[0]
    assert config_sum == sha256((ROOT/'pruefvertrag.json').read_bytes()).hexdigest()
    paths, coef, sides, pieces = cut_orders()
    # p=-(d/dtau)S with physical T=Delta*Y. For each edge, only the
    # past-to-complement terms survive a common past translation. Verify that
    # the independently reconstructed polynomial has the same sparse support.
    def current_rows(table):
        return {edge: b for edge, b in table.items()
                if edge[0] in PAST and edge[1] not in PAST and b}
    assert current_rows(coef) == {k:v for part in pieces for k,v in current_rows(part).items()}
    assert all(j in INNER for i, j in current_rows(coef))
    # The C-independent gravitational and scalar factors must also agree
    # before using their cancellation in normalized pointer probabilities.
    def laplacian(entries):
        h = [[0 for _ in NODES] for _ in NODES]
        for (i, j), weight in entries.items():
            h[i][i] -= weight
            h[j][j] -= weight
            h[i][j] += weight
            h[j][i] += weight
        return h
    sewn_h = [laplacian(part) for part in pieces]
    assert laplacian(coef) == [[sum(h[i][j] for h in sewn_h) for j in range(15)]
                               for i in range(15)]
    gravity = len(NODES)-sum(coef.values())
    assert gravity == (len(sides[0])+len(sides[1])-len(sides[2])
                       -sum(sum(part.values()) for part in pieces)) == 7
    boxes = ref.enclose(ref.RADIUS)
    p_pos, p_neg = ([MASS*Q(v) for v in boxes[s]] for s in ('positive', 'negative'))
    phase = phase_enclosure(paths, coef)
    width = phase[1] - phase[0]
    p_max = max(map(abs, p_pos+p_neg))
    assert width < Q(43, 100) and p_max < Q(1, 500)
    # cos(x) >= 1-x^2/2 on the entire doubled history integral.
    cos_lower = Q(9, 10)
    assert 1-(width+p_max)**2/2 > cos_lower
    # Also the real part of both full off-diagonal Gram terms stays positive.
    assert 1-(width+2*p_max)**2/2 > cos_lower
    pl, nl = Q(74, 40000), Q(51, 40000)
    assert p_pos[0] > pl and p_neg[1] < -nl
    half = Q(1, 2)
    pp, pn = half+cos_lower*pl/2, half-cos_lower*nl/2
    assert pp-pn == Q(9, 6400)
    return {
        'typ': ref.ORDER, 'schnitt': sorted(sides[2]), 'pfade': paths,
        'schnittpaare':len(pieces[2]), 'nichtverschwindende_kreuzkoeffizienten':
        sum(bool(b) for b in pieces[2].values()), 'quelle_mit_kreuzterm': len(current_rows(pieces[2])),
        'exakte_polynomgleichheit':True, 'zweifache_skalare_hesse_gleich':True,
        'F4_beide_wege':gravity, 'kopplung_aus':{'P_Yplus_beide':'1/2','matrix':'gamma [[1,1],[1,1]]'},
        'staubphase_gesamt_rad':list(map(str,phase)), 'staubphase_breite_oben':'43/100',
        'p_bereiche':{k:list(map(str,r)) for k,r in [('plus',p_pos),('minus',p_neg)]},
        'P_Yplus_positives_paket_strikt_ueber':str(pp),
        'P_Yplus_negatives_paket_strikt_unter':str(pn),
        'abstand_strikt_ueber':str(pp-pn),'vollstaendige_matrix_identitaet':'PASS_HILFSPAARUNG',
        'physikalischer_schnitttransport':'HOLD', 'physikalischer_vorzeichenrecord':'HOLD'}


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Die exakten Prüfungen benötigen Python ohne -O.')
    print(json.dumps(certificate(), indent=2, ensure_ascii=False))
