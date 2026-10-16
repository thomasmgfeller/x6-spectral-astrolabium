"""Fixed finite-generator pilot. Imports no historical target feature values."""
from collections import Counter
from itertools import combinations
import math
import numpy as np
from core import Stream, closure, require, validate_order


def sample(family, n, split, draw):
    rng = Stream('geometry', family, n, split, draw)
    coordinates = None
    if family == 'layered':
        sizes = [n//4, n-2*(n//4), n//4]
        l, m, u = sizes
        c = [[0]*n for _ in range(n)]
        for first, last, stop in [(0, l, l+m), (l, l+m, n)]:
            for i in range(first, last):
                for j in range(last, stop):
                    c[i][j] = rng.below(2)
        c = closure(c)
    else:
        if family == 'minkowski':
            coordinates, seen_u, seen_v = [], set(), set()
            while len(coordinates) < n:
                u, v = rng.unit(), rng.unit()
                if u in seen_u or v in seen_v:
                    continue
                coordinates.append([u, v])
                seen_u.add(u)
                seen_v.add(v)
        else:
            side = 2*math.isqrt(n)
            require(side*side == 4*n, 'square N for lattice designs')
            sites = rng.shuffle(range(side*side))[:n]
            coordinates = [[k//side, k % side] for k in sites]
            require(family in ['lattice', 'jittered_lattice'], 'known family')
            if family == 'jittered_lattice':
                coordinates = [[u+0.4*(rng.unit()-0.5), v+0.4*(rng.unit()-0.5)]
                               for u, v in coordinates]
        # t=(u+v)/2, x=(u-v)/2. <= includes null causal pairs in the lattice.
        c = [[int(i != j and u <= a and v <= b) for j, (a, b) in enumerate(coordinates)]
             for i, (u, v) in enumerate(coordinates)]
    validate_order(c)
    return dict(id=f'{family}-n{n}-{split}-{draw:03d}', family=family, n=n,
                split=split, draw=draw, coordinates=coordinates,
                relation_rows=[''.join(map(str, row)) for row in c])


def intervals_links(c):
    n = len(c)
    future = [sum(x << j for j, x in enumerate(row)) for row in c]
    past = [sum(c[i][j] << i for i in range(n)) for j in range(n)]
    intervals, links = [0]*n, [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if c[i][j]:
                k = (future[i] & past[j]).bit_count()
                intervals[k] += 1
                links[i][j] = int(k == 0)
    return intervals, links, future, past


def intersection_histograms(masks):
    n = len(masks)
    result = []
    for k in (1, 2, 3):
        histogram = [0]*(n+1)
        for group in combinations(masks, k):
            common = (1 << n)-1
            for mask in group:
                common &= mask
            histogram[common.bit_count()] += 1
        result.append(histogram)
    return result


def features(c):
    n = len(c)
    intervals, links, future, past = intervals_links(c)
    out = [sum(r) for r in links]
    incoming = [sum(links[i][j] for i in range(n)) for j in range(n)]
    link_hist = [[values.count(k) for k in range(n)] for values in (incoming, out)]
    a = np.asarray(links, dtype=float)
    a = a+a.T
    laplacian = np.diag(a.sum(axis=1))-a
    eigenvalues, vectors = np.linalg.eigh(laplacian)
    residual = float(np.max(np.abs(laplacian@vectors-vectors*eigenvalues)))
    require(residual <= 1e-10*n, 'Laplacian eigensolver residual')
    require(abs(float(eigenvalues.sum())-float(np.trace(laplacian))) <= 1e-9*n,
            'Laplacian trace check')
    require(float(eigenvalues[0]) >= -1e-10*n, 'positive semidefinite Laplacian')
    intersections = [intersection_histograms(future), intersection_histograms(past)]
    baseline = [x/n for hist in link_hist for x in hist]
    baseline += [x/math.comb(n, 2) for x in intervals]
    baseline += [float(x)/n for x in eigenvalues]
    candidate = [x/math.comb(n, k) for direction in intersections
                 for k, hist in enumerate(direction, 1) for x in hist]
    # A strict order can be processed by increasing predecessor count.
    lengths = [1]*n
    for j in sorted(range(n), key=lambda j: past[j].bit_count()):
        lengths[j] = 1+max([lengths[i] for i in range(n) if c[i][j]], default=0)
    return dict(link_histograms=link_hist, interval_histogram=intervals,
                intersections=intersections, eigenvalues=[float(x) for x in eigenvalues],
                B=baseline, P123=candidate, relation_fraction=sum(intervals)/math.comb(n, 2),
                height=max(lengths), eigen_residual=residual)


def feature_vector(record, model):
    f = record['features']
    return f['B']+f['P123'] if model == 'B+P123' else f[model]


def predict(records, families, model):
    train = [r for r in records if r['split'] == 'train']
    test = [r for r in records if r['split'] == 'test']
    x = np.asarray([feature_vector(r, model) for r in train])
    mean, scale = x.mean(axis=0), x.std(axis=0)
    scale[scale <= 1e-12] = 1
    z = (x-mean)/scale
    centers = np.array([z[[r['family'] == f for r in train]].mean(axis=0) for f in families])
    predictions, confusion = [], [[0]*len(families) for _ in families]
    for r in test:
        point = (np.asarray(feature_vector(r, model))-mean)/scale
        distance = ((centers-point)**2).sum(axis=1)
        chosen = int(np.argmin(distance))
        truth = families.index(r['family'])
        confusion[truth][chosen] += 1
        predictions.append(dict(id=r['id'], truth=truth, predicted=chosen,
                                squared_distances=[float(x) for x in distance]))
    recalls = [confusion[i][i]/sum(confusion[i]) for i in range(len(families))]
    return dict(confusion=confusion, balanced_accuracy=sum(recalls)/len(recalls),
                predictions=predictions, training_mean=mean.tolist(), training_scale=scale.tolist(),
                standardized_centroids=centers.tolist())


def evaluate(records, cfg):
    results = {}
    families = cfg['families']
    for n in cfg['sizes']:
        rr = [r for r in records if r['n'] == n]
        results[str(n)] = {model: predict(rr, families, model) for model in cfg['models']}
    primary = results['64']
    differences = [[] for _ in families]
    for a, b in zip(primary['B']['predictions'], primary['B+P123']['predictions']):
        require(a['id'] == b['id'] and a['truth'] == b['truth'], 'paired predictions')
        differences[a['truth']].append(int(b['truth'] == b['predicted'])-int(a['truth'] == a['predicted']))
    rng = Stream('paired-bootstrap', 64)
    bootstrap = []
    for _ in range(2000):
        bootstrap.append(sum(sum(v[rng.below(len(v))] for _ in v)/len(v)
                             for v in differences)/len(families))
    low, high = [float(x) for x in np.quantile(bootstrap, [0.025, 0.975], method='linear')]
    gain = sum(sum(v)/len(v) for v in differences)/len(families)
    return dict(cells=results, primary=dict(n=64, gain=gain, paired_bootstrap_95=[low, high],
                replicates=2000, passes_fixed_incremental_criterion=bool(gain >= 0.05 and low > 0),
                interpretation='Finite generator discrimination; no geometry or continuum certificate.'))
