"""Unabhängige endliche Kontrollen am publizierten Stand von PR 418. Python >= 3.10."""
import json
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'input'


def read(name):
    return json.loads((DATA / name).read_text(encoding='utf-8'))


def boxes(values):
    parsed = [tuple(map(F, endpoints)) for endpoints in values]
    assert all(lo <= hi for lo, hi in parsed)
    return parsed


def boundary_count(clocks, cut, links, order):
    early = {i for i, (_, hi) in enumerate(clocks) if hi <= cut}
    assert all(i in early or lo > cut for i, (lo, _) in enumerate(clocks))
    assert all(j not in early or i in early for i, j in order)
    crossing = sorted((i, j) for i, j in links if i in early and j not in early)
    return {'early_events': sorted(early), 'crossing': crossing, 'count': len(crossing)}


def chains(order, n, start, end):
    # One iteration appends exactly one strict comparison, including non-cover pairs.
    counts = [int(i == start) for i in range(n)]
    profile = []
    for _ in range(1, n):
        nxt = [0] * n
        for i, j in order:
            nxt[j] += counts[i]
        profile.append(nxt[end])
        counts = nxt
    while profile and profile[-1] == 0:
        profile.pop()
    return profile


def squared_distance(p, q):
    return sum((a-b)**2 for a, b in zip(p, q, strict=True))


def verify_embedding(coords, clocks, weights, order):
    for i, j in combinations(range(len(coords)), 2):
        lo = clocks[j][0] - clocks[i][1]
        hi = clocks[j][1] - clocks[i][0]
        distance = squared_distance(coords[i], coords[j])
        if (i, j) in order:
            assert lo > 0 and lo**2 > distance
        elif (j, i) in order:
            assert hi < 0 and hi**2 > distance
        else:
            assert max(lo**2, hi**2) < distance

    for z_center, radius_at_half in [(F(-1), F(1)), (F(-5, 2), F(2))]:
        for point, (tmin, tmax), (wmin, wmax) in zip(coords, clocks, weights, strict=True):
            radius_min = radius_at_half - (tmax - F(1, 2)) / 8
            radius_max = radius_at_half - (tmin - F(1, 2)) / 8
            distance = squared_distance(point, (0, 0, z_center))
            assert radius_min > 0
            if wmin > 0:
                assert distance < radius_min**2
            else:
                assert wmin == wmax == 0 and distance > radius_max**2


def main():
    pair = read('Vergleichspaar.json')
    coords = [tuple(map(F, point)) for point in read('Ortskoordinaten.json')]
    n = len(coords)
    order = {tuple(edge) for edge in pair['relation']}
    two_steps = {(i, k) for i, j in order for mid, k in order if j == mid}
    assert two_steps <= order and not any(i == j for i, j in order)
    links = order - two_steps
    maxima = sorted(set(range(n)) - {i for i, _ in order})
    assert (n, len(order), len(links), maxima) == (22, 152, 32, [10, 21])
    assert pair['external_mass_standard'] is None
    cuts = ['15/32', '1/2', '17/32', '129/256']
    rows = {}
    for name in ('heavy', 'light'):
        clocks = boxes(pair[name]['normalized_clocks'])
        weights = boxes(pair[name]['weight_box'])
        assert len(clocks) == len(weights) == n
        verify_embedding(coords, clocks, weights, order)
        rows[name] = {c: boundary_count(clocks, F(c), links, order) for c in cuts}
    assert all(rows['heavy'][c] == rows['light'][c] for c in cuts[:3])
    assert [rows['heavy'][c]['count'] for c in cuts] == [6, 6, 7, 6]
    assert [rows['light'][c]['count'] for c in cuts] == [6, 6, 7, 8]
    profiles = {(i, j): chains(order, n, i, j) for i, j in
                [(18, 10), (19, 10), (18, 21), (19, 21), (0, 18), (0, 19)]}
    assert profiles == {(18,10):[1,3,3,1], (19,10):[1,3,3,1], (18,21):[],
                        (19,21):[1], (0,18):[1,6,6,4,1], (0,19):[1,4,6,4,1]}
    area_values = [4*r**2 for r in (1, 2)]
    lower_bound = F(area_values[1]-area_values[0], sum(area_values))
    assert lower_bound == F(3,5)
    plan, eligibility, pilot = read('plan.json'), read('eligibility.json'), read('pilot.json')
    ref = plan['reference']
    densities = plan['physical_refinement']['density_ratios']
    points = len(ref['masses'])*len(ref['time_fractions'])*len(densities)
    pilot_checks = pilot['p3_reference_check']
    assert points == 60 and pilot_checks['physical_checkpoint_records_checked'] == 8
    assert eligibility['execution'] == pilot['physical']['execution'] == 'NOT_RUN'
    assert pilot['physical']['radius_M_1_4'] is None and pilot['physical']['radius_M_4'] is None
    result = dict(order_id=pair['order_id'], events=n, strict_relations=len(order),
                  hasse_links=len(links), maximal_events=maxima, exact_cuts=rows,
                  strict_chain_profiles={f'{i}->{j}': vals for (i,j),vals in profiles.items()},
                  compatible_spherical_area_in_pi=area_values, area_minimax=str(lower_bound),
                  status_from_contract=eligibility['decision'], physical_execution=eligibility['execution'],
                  pilot_slots=8, p3_slots=points, planned_comparisons=plan['family']['total'])
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Bitte Python ohne -O aufrufen.')
    main()
