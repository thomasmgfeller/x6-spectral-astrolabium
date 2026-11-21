"""Whole-cell rational enclosures and a coefficient-level Ward balance."""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
from math import isqrt
from pathlib import Path
import json

from basis_340.quellen import density_translation_375841 as src

P, I, F = src.PAST, src.INNER, src.FUTURE
ORDER, PATHS, B = src.local_geometry()
NODES = tuple(range(15))
M = Q(1, 4)
K = (5, 12, 13)
ROOT = Path(__file__).resolve().parent
box, add, sub, mul, scale, total = src.box, src.plus, src.minus, src.times, src.scale, src.add_all


def fields(radius):
    e = box(Q(-1, 4), radius)
    duration_units = sub(box(4), e)
    u = {v: box(src.CENTER[v], radius) for v in I}
    y = {v: box(v-5) for v in P+F}
    y[P[-1]] = add(y[P[-1]], e)
    z = Q(1, 2**20) if radius else Q(0)
    for v in F[1:]:
        y[v] = box(v-5, z)
    y.update({v: add(add(box(-2), e), mul(duration_units, u[v])) for v in I})
    coeff = {v: add(box(1), scale(Q(1, 19), total(
        scale(b, src.square(sub(y[i], y[v]))) for (i, j), b in B.items() if j == v)))
             for v in K}
    d = {v: scale(src.COFACTOR_SCALE, sub(coeff[a], coeff[b]))
         for v, a, b in ((5, 12, 13), (12, 13, 5), (13, 5, 12))}
    dwell = {v: box(0) for v in I}
    for path in PATHS:
        ends = [box(0)] + [scale(Q(1, 2), add(u[a], u[b]))
                for a, b in zip(path, path[1:])] + [box(1)]
        for v, a, b in zip(path, ends, ends[1:]):
            dwell[v] = add(dwell[v], scale(Q(1, len(PATHS)), sub(b, a)))
    precision = 10**18
    lo = isqrt(isqrt(3*precision**4//722))
    delta = (Q(lo, precision), Q(lo+1, precision))
    assert delta[0]**4 <= Q(3, 722) <= delta[1]**4
    inv_delta = (1/delta[1], 1/delta[0])
    weights = []
    for sign in (-1, 1):  # positive packet is f-d+xi
        w = {v: mul(box(Q(1, 8), z), inv_delta) for v in F}
        for v in I:
            x = add(add(dwell[v], scale(sign, d.get(v, box(0)))), box(0, radius))
            w[v] = mul(scale(M, duration_units), x)
        weights.append(w)
    delta_w = {v: mul(scale(-2*M, duration_units), d[v]) for v in K}
    return y, weights, delta_w


def ideals():
    # Enumerate subsets using the full order; check independently against
    # prefixes of the two maximal chains.
    result = []
    for size in range(len(I)+1):
        for subset in combinations(I, size):
            cut = set(P).union(subset)
            if all(j not in cut or i in cut for i, j in ORDER):
                result.append(cut)
    a, b = PATHS
    prefixes = {frozenset(P + a[:i] + b[:j])
                for i, j in product(range(len(a)+1), range(len(b)+1))}
    assert {frozenset(c) for c in result} == prefixes
    return result


def flux(cut, y, weights):
    # weights are w/Delta or the difference of those scaled densities.
    return scale(Q(1, 19), total(mul(weights[j], scale(b, sub(y[i], y[j])))
        for (i, j), b in B.items() if i in cut and j not in cut and j in weights))


def boundary_coefficient(edge, cut):
    i, j = edge
    return int(i in cut)-int(j in cut)


def verify_balance(cuts):
    # Oriented edge polynomial b_ij*w_j*(Y_i-Y_j)/(19*Delta).
    # For E_v=dS/dT_v its coefficient is +1 at j, -1 at i.
    count = 0
    for a, b in product(cuts, repeat=2):
        if not a < b:
            continue
        for i, j in ORDER:
            difference = boundary_coefficient((i, j), a)-boundary_coefficient((i, j), b)
            assert difference == sum((v == j)-(v == i) for v in b-a)
        count += 1
    return count


def frac_bounds(b):
    return list(map(str, b))


def calculate():
    contract = ROOT/'pruefvertrag.json'
    assert sha256(contract.read_bytes()).hexdigest() == (ROOT/'pruefvertrag.sha256').read_text().split()[0]
    cuts = ideals()
    yc, wc, dc = fields(Q(0))
    y, w, delta = fields(src.RADIUS)
    initial, middle, final = set(P), set(P) | {4, 5, 6, 11}, set(P+I)
    assert all(y[v][1] < 0 for v in middle) and all(y[v][0] > 0 for v in set(NODES)-middle)
    rows = []
    special = {}
    for cut in cuts:
        point = flux(cut, yc, dc)
        assert point[0] == point[1]
        band = flux(cut, y, delta)
        assert band[0] <= point[0] <= band[1]
        if band == (0, 0):
            classification = 'null'
        elif band[0] > 0:
            classification = 'positiv'
        elif band[1] < 0:
            classification = 'negativ'
        else:
            classification = 'offen'
        rows.append({'innere_ereignisse':sorted(cut-set(P)), 'differenz_zentrum':str(point[0]),
                     'differenz_intervall':frac_bounds(band), 'klasse':classification})
        for name, designated in [('anfang', initial), ('zwischen', middle), ('ausgang', final)]:
            if cut == designated:
                special[name] = {
                    'positivpaket':frac_bounds(flux(cut, y, w[0])),
                    'negativpaket':frac_bounds(flux(cut, y, w[1])),
                    'differenz_zentrum':str(point[0]), 'differenz_intervall':frac_bounds(band)}
    assert all(j in F for (i, j) in B if i in final and j not in final)
    assert flux(final, y, delta) == (0, 0)
    # Terms sensitive to the density displacement target K; their entire
    # predecessor clock support is disjoint from the future collar. This
    # certifies equality for arbitrary finite changes of the future fields.
    assert not (set(K) & set(F))
    assert {i for (i,j), b in B.items() if j in K and b}.isdisjoint(F)
    # Original global current and its cell certificates as an independent check.
    original = src.enclose(0)
    for idx, name in enumerate(['positive','negative']):
        assert flux(initial, yc, wc[idx]) == tuple(M*Q(t) for t in original[name])
    assert flux(initial, yc, dc) == box(Q(1217081,380000000))
    charge_gap = flux(initial, y, delta)
    assert charge_gap[0] > Q(1,320)
    # Sham impulse with zero receiver-density difference: every cut is null.
    assert all(flux(c, y, {}) == box(0) for c in cuts)
    residuals = {}
    for label, weights in zip(['positivpaket', 'negativpaket'], w):
        r = sub(flux(initial, y, weights), flux(final, y, weights))
        assert r[1] < 0
        residuals[label] = frac_bounds(r)
    return {'typ':src.ORDER, 'paare_verschachtelter_ideale_geprueft':verify_balance(cuts),
            'anzahl_ideale':len(cuts), 'klassen':{k:sum(row['klasse']==k for row in rows)
            for k in ('positiv','negativ','null','offen')}, 'drei_schnitte':special,
            'summe_innere_uhreulerableitungen':residuals,'alle_ideale':rows}


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Bitte ohne -O ausführen.')
    print(json.dumps(calculate(), indent=2, ensure_ascii=False))
