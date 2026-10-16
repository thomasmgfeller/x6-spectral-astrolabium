"""Direct incidence/interval oracles and complete target accounting.

Numerical classification is replayed; it is not an external independent replication.
"""
from collections import Counter
from itertools import combinations, permutations
import gzip
import json
import math
from pathlib import Path
import numpy as np
from core import Stream, closure, require, verify_relation, validate_order
from produce import HERE, ROOT, matrix, readz, save
import geometry
import selftest


def coverage(records, expected):
    require(len(records) == len(expected) and
            {(r['family'], r['n'], r['split'], r['draw']) for r in records} == expected,
            'all geometry inputs once')


def scalar_predictions(records, families, model):
    """Separate scalar centroids, no NumPy reductions or production predictor."""
    def vector(r):
        f = r['features']
        return f['B']+f['P123'] if model == 'B+P123' else f[model]
    training = [r for r in records if r['split'] == 'train']
    columns = list(zip(*(vector(r) for r in training)))
    mean = [math.fsum(v)/len(v) for v in columns]
    scale = [math.sqrt(math.fsum((x-mu)**2 for x in v)/len(v)) for v, mu in zip(columns, mean)]
    scale = [s if s > 1e-12 else 1 for s in scale]
    centers = []
    for family in families:
        rows = [vector(r) for r in training if r['family'] == family]
        centers.append([(math.fsum(v)/len(v)-mu)/s for v, mu, s in zip(zip(*rows), mean, scale)])
    result = []
    for r in records:
        if r['split'] != 'test':
            continue
        z = [(x-mu)/s for x, mu, s in zip(vector(r), mean, scale)]
        distances = [math.fsum((x-y)**2 for x, y in zip(z, center)) for center in centers]
        result.append((r['id'], min(range(len(families)), key=lambda i: distances[i])))
    return result


def direct(c):
    n = len(c)
    a = np.asarray(c, dtype=np.int64)
    sizes = a@a  # transitive order: exact number of strict interior elements
    links = a*((sizes == 0).astype(np.int64))
    require(closure(links.tolist()) == c, 'Hasse closure must recover full relation')
    ih = [int(np.count_nonzero((a == 1) & (sizes == k))) for k in range(n)]
    degree = [[int(np.count_nonzero(links.sum(axis=axis) == k)) for k in range(n)] for axis in (0, 1)]
    intersections = []
    # Independent column-enumeration identity: for each target vertex, add one
    # to every root subset in its predecessor set (and conversely).
    for incidence in (a.T, a):
        result = []
        for k in (1, 2, 3):
            values = Counter()
            for row in incidence:
                neighbors = [i for i, x in enumerate(row) if x]
                for roots in combinations(neighbors, k):
                    values[roots] += 1
            hist = [0]*(n+1)
            hist[0] = math.comb(n, k)-len(values)
            for number in values.values():
                hist[number] += 1
            result.append(hist)
        intersections.append(result)
    lap = np.diag((links+links.T).sum(axis=1))-(links+links.T)
    ev = np.linalg.eigvalsh(lap.astype(float))
    return ih, degree, intersections, ev


def check(directory):
    cfg = json.loads((HERE/'contract.json').read_text())
    toys = selftest.run()
    source = ROOT/'research/lorentz_relational_boundary/results'
    old = {r['id']: r for r in json.loads((source/'inputs.json').read_text())}
    refs = readz(source/'reference.json.gz')
    data = readz(directory/'matching.json.gz')
    require(len(data['pairs']) == len(refs), 'pair count')
    for actual, expected in zip(data['pairs'], refs):
        require(actual['ids'] == expected['ids'] and actual['status'] ==
                ('ISOMORPHIC' if expected['isomorphic'] else 'NONISOMORPHIC'), 'complete ordered reference accounting')
    require(len(data['renamed_copies']) == 3*len(old), 'all renamed copies')
    expected_keys = {(name, repeat) for name in old for repeat in range(3)}
    require({(r['id'], r['repeat']) for r in data['renamed_copies']} == expected_keys, 'unique copy coverage')
    for row in data['renamed_copies']:
        c = matrix(old[row['id']])
        p = Stream('relabel', cfg['matching']['seed'], row['id'], row['repeat']).shuffle(range(len(c)))
        require(p == row['output_to_original'], 'relabel replay')
        d = [[c[i][j] for j in p] for i in p]
        verify_relation(c, d, row['source_to_target'])
    control = json.loads((directory/'three_layer.json').read_text())
    require(control == selftest.counterexample(), 'three-layer counterexample')
    require(control['total_relations'] == [10, 9], 'six-node nonisomorphism certificate')
    # Check every bijection directly for the six-node counterexample, without layer assumptions.
    a, b = control['relation_a'], control['relation_b']
    require(not any(all(a[i][j] == b[p[i]][p[j]] for i in range(6) for j in range(6))
                    for p in permutations(range(6))), 'all 720 node bijections reject')
    records = readz(directory/'geometry_records.json.gz')
    expected = {(f, n, s, d) for n in cfg['geometry']['sizes'] for f in cfg['geometry']['families']
                for s in ['train', 'test'] for d in range(cfg['geometry'][s+'_per_cell'])}
    coverage(records, expected)
    max_eigen_difference = 0.0
    for r in records:
        base = {k: v for k, v in r.items() if k != 'features'}
        require(base == geometry.sample(r['family'], r['n'], r['split'], r['draw']), 'input replay')
        c, f = matrix(r), r['features']
        validate_order(c)
        if r['coordinates'] is not None:
            # Independent Minkowski metric test of the recorded null coordinates.
            for i, (u, v) in enumerate(r['coordinates']):
                for j, (a, b) in enumerate(r['coordinates']):
                    dt, dx = (a-u+b-v)/2, (a-u-b+v)/2
                    require(c[i][j] == int(i != j and dt > 0 and dt >= abs(dx)), 'null vs Minkowski order')
        ih, degree, intersections, ev = direct(c)
        require(ih == f['interval_histogram'] and degree == f['link_histograms']
                and intersections == f['intersections'], 'independent integer feature check')
        difference = float(np.max(np.abs(ev-f['eigenvalues'])))
        max_eigen_difference = max(max_eigen_difference, difference)
        require(np.allclose(ev, f['eigenvalues'], atol=1e-10, rtol=1e-10), 'eigensolver agreement')
        expected_b = [x/r['n'] for h in degree for x in h]+[x/math.comb(r['n'], 2) for x in ih]+[float(x)/r['n'] for x in ev]
        expected_p = [x/math.comb(r['n'], k) for direction in intersections for k, h in enumerate(direction, 1) for x in h]
        require(np.allclose(f['B'], expected_b, atol=1e-10, rtol=1e-10) and f['P123'] == expected_p, 'normalized features')
        permutation = Stream('geometry-relabel', r['id']).shuffle(range(r['n']))
        renamed = geometry.features([[c[i][j] for j in permutation] for i in permutation])
        require(renamed['P123'] == f['P123'] and np.allclose(renamed['B'], f['B'], atol=1e-10, rtol=1e-10),
                'geometry relabel invariance')
    actual = readz(directory/'geometry_evaluation.json.gz')
    require(actual == geometry.evaluate(records, cfg['geometry']), 'classifier and bootstrap replay')
    for n in cfg['geometry']['sizes']:
        for model in cfg['geometry']['models']:
            expected_predictions = scalar_predictions([r for r in records if r['n'] == n], cfg['geometry']['families'], model)
            require(expected_predictions == [(r['id'], r['predicted']) for r in actual['cells'][str(n)][model]['predictions']],
                    'independent scalar classifier')
    # Missing observations must not be accepted as a smaller successful run.
    try:
        coverage(records[:-1], expected)
    except ValueError:
        pass
    else:
        raise ValueError('missing-input negative control failed')
    save(directory/'verification.json', dict(status='PASS', matching_pairs=len(refs),
         full_relation_witnesses=len(data['renamed_copies']), geometry_orders=len(records),
         independent_integer_features=len(records), relabeling_checks=len(records),
         counterexample_full_permutations=720, toys=toys,
         independence='Distinct exact feature formulas and scalar classifier in one authoring process; bootstrap replay shares source; external replication not performed.'))
    save(directory/'numerical_check.json', dict(maximum_eigenvalue_difference=max_eigen_difference))


if __name__ == '__main__':
    import sys
    check(Path(sys.argv[1]))
