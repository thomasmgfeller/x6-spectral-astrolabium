"""Exact incidence and interval bounds for a two-sided marked causal diamond."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent / 'basis'
sys.path.insert(0, str(BASE))
from quellenpaket import model
from einfuegung import diamond_extension, density_gradient, predecessor_families, receiver_bound

WINDOWS = tuple(F(1, n) for n in (256, 64, 16, 8, 4, 2))


def candidates(order, material, zero):
    mixed = {(a, b) for a in material for b in zero
             if (a, b) not in order and (b, a) not in order}
    # Each tuple contains the past and future anchors, a material candidate and a zero.
    quartets = {(p, q, a, b) for a, b in mixed for p in material for q in material
                if (p, a) in order and (p, b) in order and (a, q) in order and (b, q) in order}
    return mixed, quartets


def intervals(order, material, zero):
    nodes = material | zero
    result = set()
    for p, q in order:
        if p not in material or q not in material:
            continue
        interior = {i for i in nodes if (p, i) in order and (i, q) in order}
        for i, j in combinations(interior, 2):
            if (i, j) in order or (j, i) in order or (i in zero) == (j in zero):
                continue
            a, b = (i, j) if i in material else (j, i)
            result.add((p, q, a, b))
    return result


def thresholds(candidates, distances):
    if not candidates:
        return None
    return tuple(min(max(distances[n][k] for n in group) for group in candidates)
                 for k in (0, 1))


def audit(certificate):
    with model() as (_, __, prev, early):
        from gemischt import ORDER
        from modell import setup
        from empfangsbit import STEP, K0, V
        from quelle import hull, box
        from staubgeraet import solve, verify
        from referenzwechsel import displaced
        from driftfamilie import LABELS, LIMIT
        order = set(ORDER)
        y, w = setup(prev, early)
        nodes = set(y)
        material = {n for n in nodes if w[n].lo > 0}
        zero = nodes - material
        assert len(nodes) == 19 and zero == {15, 17}
        assert all(w[i].lo == w[i].hi == 0 for i in zero)
        pairs, quads = candidates(order, material, zero)
        assert quads == intervals(order, material, zero)
        assert not candidates(order, set(), nodes)[0]
        assert not candidates(order, nodes, set())[0]
        total_order = {(i, j) for i, j in combinations(sorted(nodes), 2)}
        assert candidates(total_order, material, zero) == (set(), set())
        diamond = {(0, 1), (0, 2), (1, 3), (2, 3), (0, 3)}
        assert candidates(diamond, {0, 1, 3}, {2}) == ({(1, 2)}, {(0, 3, 1, 2)})
        for i, j in combinations(nodes, 2):
            perm = {k: (j if k == i else i if k == j else k) for k in nodes}
            permuted = lambda seq: tuple(perm[k] for k in seq)
            actual = candidates({permuted(edge) for edge in order}, {perm[k] for k in material}, {perm[k] for k in zero})
            assert actual == ({permuted(p) for p in pairs}, {permuted(q) for q in quads})
        leaves = [tuple(map(F, row['delta'])) for row in certificate['leaves']]
        assert len(leaves) == 7 and leaves[0][0] == -LIMIT and leaves[-1][1] == LIMIT
        assert all(a < b for a, b in leaves) and all(b == c for (_, b), (c, _) in zip(leaves, leaves[1:]))
        velocities = (hull(-112*V, 112*V),)*3
        positions = (hull(-1, 1),)*3
        extended, coefficients = diamond_extension(order, nodes)
        alternatives = predecessor_families(order, nodes)
        ext_quads = candidates(extended, material | {19}, zero | {20})[1]
        assert (16, 18, 19, 20) in ext_quads
        rows = []
        for lo, hi in leaves:
            yy, ww = displaced(y, w, hull(6*STEP+lo, 6*STEP+hi))
            for source in LABELS:
                st = solve(yy, ww, source, velocities, K0, box(-K0), 'positive_bridge')
                verify(st, source, velocities, K0, box(-K0), 'positive_bridge', positions)
                assert all(st['w'][n].lo > 0 for n in material)
                assert all(st['w'][n].lo == st['w'][n].hi == 0 for n in zero)
                Y = st['y']
                den = Y[7] - Y[3]
                assert den.lo > 0
                dist = {}
                for n in nodes:
                    # The two normalizing events have exact normalized coordinates.
                    if n in (3, 7):
                        L = H = F(int(n == 7))
                    else:
                        L, H = map(F, ((Y[n]-Y[3])/den).data())
                    dist[n] = (max(F(0), F(1,2)-H, L-F(1,2)), max(abs(L-F(1,2)), abs(H-F(1,2))))
                row = {'delta': list(map(str, (lo, hi))), 'source': str(source), 'windows': {}}
                for kind, groups in [('mixed', pairs), ('diamond', quads)]:
                    limits = thresholds(groups, dist)
                    row[kind] = list(map(str, limits)) if limits else None
                row['extension_gradient'] = density_gradient(Y, coefficients)
                row['receiver_identity'] = receiver_bound(st, alternatives[-1][1], velocities, K0)
                row['alternative_gradients'] = [density_gradient(Y,c) for s,c in alternatives]
                row['exhaustive_quartet_minimizers_not_excluded'] = sorted(
                    g for g in quads if max(dist[i][0] for i in g) <= F(row['diamond'][1]))
                row['exhaustive_pair_minimizers_not_excluded'] = sorted(
                    g for g in pairs if max(dist[i][0] for i in g) <= F(row['mixed'][1]))
                for h in WINDOWS:
                    entry = {}
                    for name, index in [('guaranteed', 1), ('not_excluded', 0)]:
                        active = {n for n in nodes if dist[n][index] <= h}
                        ps = sorted(g for g in pairs if set(g) <= active)
                        ds = sorted(g for g in quads if set(g) <= active)
                        entry[name] = {'events':sorted(active),'mixed':ps,'diamonds':ds}
                    row['windows'][str(h)] = entry
                rows.append(row)
        out = {'positive':sorted(material),'zero':sorted(zero),'number_of_relations':len(order),
               'mixed_pairs':sorted(pairs),'anchored_quartets':sorted(quads),'cell_results':rows,
               'pair_by_zero':dict(sorted(Counter(b for a,b in pairs).items())),
               'permutations_tested':171}
        for kind in ('mixed', 'diamond'):
            out[kind+'_minimum_halfwidth'] = None if rows[0][kind] is None else [
                str(min(F(r[kind][0]) for r in rows)),str(max(F(r[kind][1]) for r in rows))]
        out['least_extension'] = {'positive':19, 'zero':20, 'anchors':[16,18],
                                  'incoming_dust_coefficients':dict(sorted(coefficients.items())),
                                  'gradient_range':[str(min(F(r['extension_gradient'][0]) for r in rows)),
                                                    str(max(F(r['extension_gradient'][1]) for r in rows))]}
        out['all_predecessor_ideals'] = [{'old_past':s, 'coefficients':c, 'range':[str(min(F(r['alternative_gradients'][i][0]) for r in rows)), str(max(F(r['alternative_gradients'][i][1]) for r in rows))]} for i,(s,c) in enumerate(alternatives)]
        return out
