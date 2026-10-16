"""Independent matching reconstruction, integer observables and scalar classifier."""
from collections import Counter
from itertools import combinations
import hashlib
import json
import math
import numpy as np
from common import (HERE, NAMESPACE, matrix, prior_core, prior_geometry, readz, require,
                    sample, save, selected_ids, token, validate_ledger, validate_pairs)
import analysis


def independent_profile(c):
    a = np.asarray(c, dtype=np.int64)
    require(not np.any(np.diag(a)) and not np.any((a@a > 0) & (a == 0)), 'strict transitive relation')
    remaining = np.ones(len(a), dtype=bool)
    height = 0
    while remaining.any():
        minima = remaining & ~np.any(a[remaining, :], axis=0)
        require(minima.any(), 'acyclic relation')
        remaining[minima] = False
        height += 1
    return int(a.sum()), height


def independent_selection(ledger, cfg):
    answer = {}
    for n in cfg['generators']['sizes']:
        for control in cfg['matching']['controls']:
            cell = dict(n=n, control=control)
            for split in ['train', 'test']:
                subset = [r for r in ledger if r['n'] == n and r['split'] == split and r['family'] in ['minkowski', control]]
                keys = sorted({(r['R'], r['H']) for r in subset})
                bins = {k: {'minkowski': [], control: []} for k in keys}
                for r in sorted(subset, key=lambda r: r['draw']):
                    bins[(r['R'], r['H'])][r['family']].append(r['id'])
                pairs, strata = [], []
                for R, H in keys:
                    first, second = bins[(R, H)]['minkowski'], bins[(R, H)][control]
                    count = min(len(first), len(second))
                    strata.append(dict(R=R, H=H, minkowski=len(first), control=len(second), eligible=count))
                    for k in range(count):
                        payload = json.dumps([NAMESPACE, 'pair-priority', control, n, split, first[k], second[k]], separators=(',', ':'))
                        pairs.append(dict(ids=[first[k], second[k]], R=R, H=H,
                                          priority=hashlib.sha256(payload.encode()).hexdigest()))
                pairs = sorted(pairs, key=lambda p: (p['priority'], p['ids']))
                cap = cfg['matching'][split+'_pairs']
                cell[split] = dict(eligible=len(pairs), required=cap, pairs=pairs[:cap], all_eligible_pairs=pairs,
                                   strata=strata, unused_per_family=cfg['generators']['pool_per_family_size_split']-min(cap, len(pairs)))
            cell['status'] = ('EVALUABLE' if cell['train']['eligible'] >= cell['train']['required']
                              and cell['test']['eligible'] >= cell['test']['required'] else 'INSUFFICIENT_COMMON_SUPPORT')
            answer[f'{control}/n{n}'] = cell
    return answer


def verify_features(record):
    c, f, n = matrix(record), record['features'], record['n']
    a = np.asarray(c, dtype=np.int64)
    inside = a@a
    links = a*(inside == 0)
    require(prior_core.closure(links.tolist()) == c, 'Hasse closure')
    ih = [int(np.count_nonzero((a == 1) & (inside == k))) for k in range(n)]
    degrees = [[int(np.count_nonzero(links.sum(axis=axis) == k)) for k in range(n)] for axis in (0, 1)]
    pooled = []
    for incidence in (a.T, a):
        direction = []
        for k in [1, 2, 3]:
            values = Counter()
            for row in incidence:
                for roots in combinations([i for i, x in enumerate(row) if x], k):
                    values[roots] += 1
            histogram = [0]*(n+1)
            histogram[0] = math.comb(n, k)-len(values)
            for value in values.values():
                histogram[value] += 1
            direction.append(histogram)
        pooled.append(direction)
    require(ih == f['interval_histogram'] and degrees == f['link_histograms'] and pooled == f['intersections'], 'exact feature oracle')
    lap = np.diag((links+links.T).sum(axis=1))-(links+links.T)
    ev = np.linalg.eigvalsh(lap.astype(float))
    require(np.allclose(ev, f['eigenvalues'], atol=1e-10, rtol=1e-10), 'numerical spectral oracle')
    b = [x/n for h in degrees for x in h]+[x/math.comb(n, 2) for x in ih]+[float(x)/n for x in ev]
    p = [x/math.comb(n, k) for direction in pooled for k, hist in enumerate(direction, 1) for x in hist]
    R, H = independent_profile(c)
    require(np.allclose(b, f['B'], atol=1e-10, rtol=1e-10) and p == f['P123'] and f['D'] == [R/math.comb(n, 2), H/n], 'normalized features')
    if record['coordinates'] is not None:
        for i, (u, v) in enumerate(record['coordinates']):
            for j, (x, y) in enumerate(record['coordinates']):
                dt, dx = (x-u+y-v)/2, (x-u-y+v)/2
                require(c[i][j] == int(i != j and dt > 0 and dt >= abs(dx)), 'Minkowski metric oracle')


def scalar_predictions(records, families, model):
    def vector(r):
        f = r['features']
        return f['B']+f['P123'] if model == 'B+P123' else f[model]
    train = [r for r in records if r['split'] == 'train']
    columns = list(zip(*(vector(r) for r in train)))
    mean = [math.fsum(c)/len(c) for c in columns]
    scales = [math.sqrt(math.fsum((x-mu)**2 for x in c)/len(c)) for c, mu in zip(columns, mean)]
    scales = [s if s > 1e-12 else 1 for s in scales]
    centers = []
    for family in families:
        data = [vector(r) for r in train if r['family'] == family]
        centers.append([(math.fsum(c)/len(c)-mu)/s for c, mu, s in zip(zip(*data), mean, scales)])
    output = []
    for r in records:
        if r['split'] != 'test':
            continue
        z = [(x-mu)/s for x, mu, s in zip(vector(r), mean, scales)]
        distance = [math.fsum((x-y)**2 for x, y in zip(z, center)) for center in centers]
        output.append((r['id'], min(range(2), key=lambda k: distance[k])))
    return output


def run(directory):
    cfg = json.loads((HERE/'contract.json').read_text())
    ledger, selection = readz(directory/'candidate_ledger.json.gz'), readz(directory/'selection.json.gz')
    validate_ledger(ledger, cfg)
    for entry in ledger:
        record = sample(entry['family'], entry['n'], entry['split'], entry['draw'])
        R, H = independent_profile(matrix(record))
        digest = hashlib.sha256(json.dumps(record['relation_rows'], separators=(',', ':')).encode()).hexdigest()
        require(R == entry['R'] and H == entry['H'] and digest == entry['relation_sha256']
                and all(record[k] == entry[k] for k in ['id', 'family', 'n', 'split', 'draw', 'rng_split']), 'complete candidate replay')
    require(selection == independent_selection(ledger, cfg), 'independent exact matching selection')
    validate_pairs(selection, ledger)
    records = readz(directory/'selected_records.json.gz')
    require([r['id'] for r in records] == selected_ids(selection), 'selected full raw coverage')
    for r in records:
        require({k: v for k, v in r.items() if k != 'features'} == sample(r['family'], r['n'], r['split'], r['draw']), 'selected raw replay')
        verify_features(r)
        c = matrix(r)
        p = prior_core.Stream('matched-relabel', r['id']).shuffle(range(r['n']))
        f = prior_geometry.features([[c[i][j] for j in p] for i in p])
        require(f['P123'] == r['features']['P123'] and np.allclose(f['B'], r['features']['B'], atol=1e-10, rtol=1e-10), 'selected relabel invariance')
    report = readz(directory/'evaluation.json.gz')
    require(report == analysis.evaluate(selection, records, cfg), 'paired evaluation replay')
    require(json.loads((directory/'summary.json').read_text()) == analysis.summarize(report), 'summary derivation')
    lookup = {r['id']: r for r in records}
    predictions = 0
    for key, cell in selection.items():
        if cell['status'] != 'EVALUABLE':
            continue
        rr = [lookup[name] for split in ['train', 'test'] for pair in cell[split]['pairs'] for name in pair['ids']]
        # Identical nuisance distributions within both splits, not just equal means.
        for split in ['train', 'test']:
            groups = [[tuple(r['features']['D']) for r in rr if r['split'] == split and r['family'] == family]
                      for family in ['minkowski', cell['control']]]
            require(groups[0] == groups[1], 'identical confound distributions')
        for model in cfg['features']['models']:
            pred = report['cells'][key]['methods'][model]['predictions']
            require(scalar_predictions(rr, ['minkowski', cell['control']], model) == [(r['id'], r['predicted']) for r in pred], 'scalar classifier oracle')
            predictions += len(pred)
    import matched_tests
    toys = matched_tests.run()
    save(directory/'verification.json', dict(status='PASS', candidates_replayed=len(ledger),
         unique_selected_verified=len(records), exact_matching_cells=len(selection),
         evaluable_cells=sum(c['status'] == 'EVALUABLE' for c in selection.values()),
         scalar_predictions_verified=predictions, toys=toys,
         independence='Distinct matching, height, integer feature and classifier formulas in one authoring process; generator/paired bootstrap replay shares source. External replication not performed.'))


if __name__ == '__main__':
    from pathlib import Path
    import sys
    run(Path(sys.argv[1]))
