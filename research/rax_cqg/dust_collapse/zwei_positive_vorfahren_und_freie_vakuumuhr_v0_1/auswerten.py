"""Enumerate and check the two-ancestor cones; report counts and nearest bounds."""
import json
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256

from kegel import ROOT, IDEALS, SOURCE, direct, links, members, predecessors, successive
from uhr import SCALE, SLAB, enclose


def integers(nodes):
    return sum(1 << i for i in nodes)


def text_intervals(intervals):
    return [[str(F(lo, SCALE)), str(F(hi, SCALE))] for lo, hi in intervals]


def baseline():
    archive = json.loads((ROOT / 'quelle/Vergangenheiten.json').read_bytes())
    expected = {(integers(c['old_past']), () if not c['ancestor'] else
                 ((integers(c['past_u']), integers(c['future_u_in_past'])),)):
                {tuple(row) for row in c['x_outer_enclosures']} for c in archive['cases']}
    result = Counter()
    distances = {0: [], 1: []}
    for ideal in IDEALS:
        for pos in [()] + [(pair,) for pair in links(ideal)]:
            parts, singular = enclose(predecessors(ideal, pos))
            if singular or {tuple(row) for row in text_intervals(parts)} != expected.get((ideal, pos), set()):
                raise ArithmeticError(('Baseline mismatch', ideal, pos))
            result['one_ancestor' if pos else 'zero_ancestors'] += 1
            for lo, hi in parts:
                distances[len(pos)].append(max(SLAB[0] - F(hi, SCALE), F(lo, SCALE) - SLAB[1], 0))
            if parts and (ideal, pos) in expected:
                del expected[ideal, pos]
    if expected or (result['zero_ancestors'], result['one_ancestor']) != (23, 1656):
        raise ArithmeticError('Incomplete baseline replay')
    return {'cones': dict(result), 'min_distance_to_enlarged_band': {
        str(k): str(min(gaps)) for k, gaps in distances.items()}}


def time_window():
    old = json.loads((ROOT / 'quelle/vorversuch.json').read_bytes())['CST']['x_fenster']
    assert all(SLAB[0] <= F(lo) <= F(hi) <= SLAB[1] for lo, hi in old)
    # T_end = 5 sqrt(5)/3 > 7/2. Use two full eightfold stamp errors
    # in addition to the widest duration for a conservative check at either end.
    assert F(125, 9) > F(7, 2)**2
    shift = (F(1500, 10**6) + 2 * 8 * F(2, 10**6)) / F(7, 2)
    assert SLAB[0] <= F(1, 2) - shift < F(1, 2) + shift <= SLAB[1]


def scan():
    time_window()
    replay = baseline()
    totals = [Counter(), Counter()]
    nearest = [{}, {}]
    overlaps = []
    unresolved = []
    by_ideal = []
    digest = sha256()
    for ideal in IDEALS:
        keys = sorted(direct(ideal))
        if len(keys) != len(set(keys)) or set(keys) != successive(ideal):
            raise ArithmeticError(('Two enumerations differ', ideal))
        by_ideal.append({'old_past': list(members(ideal)), 'incomparable': sum(k[0] == 0 for k in keys),
                         'chain': sum(k[0] == 1 for k in keys)})
        for key in keys:
            kind, p, f, q, g = key
            stats = totals[kind]
            stats['cones'] += 1
            digest.update((','.join(map(str, (ideal, *key))) + '\n').encode())
            # All future collars have Y >= 2, hence x >= 1; causal ordering is strict.
            if any(ideal & (1 << j) for j in SOURCE['future']):
                stats['excluded_by_future_collar'] += 1
                continue
            pred = predecessors(ideal, [(p, f), (q, g)], bool(kind))
            parts, singular = enclose(pred)
            if singular:
                stats['cones_with_singular_form'] += 1
            if parts is None:
                unresolved.append([ideal, *key])
                continue
            if not parts:
                stats['no_surviving_enclosure'] += 1
                continue
            stats['with_enclosures'] += 1
            row = {'old_past': list(members(ideal)), 'u_past': list(members(p)), 'u_future': list(members(f)),
                   'v_past': list(members(q)), 'v_future': list(members(g)), 'kind': ('incomparable', 'chain')[kind]}
            hits = []
            for lo, hi in parts:
                if F(hi, SCALE) < SLAB[0]:
                    side, edge = 'below', hi
                elif F(lo, SCALE) > SLAB[1]:
                    side, edge = 'above', lo
                else:
                    hits.append((lo, hi))
                    continue
                record = nearest[kind].get(side)
                if record is None or (edge > record[0] if side == 'below' else edge < record[0]):
                    nearest[kind][side] = (edge, row, [lo, hi])
            if hits:
                stats['intersecting_slab'] += 1
                overlaps.append({**row, 'enclosures': text_intervals(hits)})
    output = {}
    for kind, name in enumerate(('incomparable', 'chain')):
        stats = totals[kind]
        assert stats['cones'] == sum(stats[k] for k in ('excluded_by_future_collar','no_surviving_enclosure','with_enclosures')) + sum(k[1] == kind for k in unresolved)
        limits = {}
        for side, (edge, row, interval) in nearest[kind].items():
            value = F(edge, SCALE)
            gap = SLAB[0] - value if side == 'below' else value - SLAB[1]
            limits[side] = {'edge': str(value), 'distance': str(gap), 'witness': row,
                            'interval': text_intervals([interval])[0]}
        output[name] = {'counts': dict(stats), 'neighbours_outside_slab': limits}
    return {'baseline': replay, 'type': SOURCE['type'], 'e': '1/6 +/- 2^-22',
            'x_slab': list(map(str, SLAB)), 'enumeration_sha256': digest.hexdigest(),
            'orders_per_old_ideal': by_ideal, 'two_ancestor_results': output,
            'intersections': overlaps, 'unresolved': unresolved, 'physical_P3': {'run': 0, 'not_run': 60}}


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O')
    print(json.dumps(scan(), indent=2, sort_keys=True))
