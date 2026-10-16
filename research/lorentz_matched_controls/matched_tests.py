"""Small matching and analysis oracles; never draw target N or namespaces."""
import copy
from itertools import product
import math
import numpy as np
from common import (ledger_entry, prior_geometry, require, select, validate_pairs,
                    validate_ledger)
import analysis
from check import independent_profile, independent_selection, scalar_predictions, verify_features


def run():
    cfg = {'generators': {'sizes': [4], 'families': ['minkowski', 'lattice', 'layered'],
                         'splits': ['train', 'test'], 'pool_per_family_size_split': 4},
           'matching': {'controls': ['lattice', 'layered'], 'train_pairs': 2, 'test_pairs': 4},
           'features': {'models': ['D', 'B', 'P123', 'B+P123']},
           'analysis': {'primary_cell': {'control': 'lattice', 'n': 4}}}
    ledger = []
    for family in cfg['generators']['families']:
        for split in ['train', 'test']:
            for draw in range(4):
                ledger.append(dict(id=f'{family}-{split}-{draw}', family=family, n=4, split=split,
                                   draw=draw, R=2+draw % 2, H=2 if family != 'layered' else 3,
                                   relation_sha256='toy', rng_split='toy'))
    validate_ledger(ledger, cfg)
    chosen = select(ledger, cfg)
    require(chosen == independent_selection(ledger, cfg), 'toy matching oracle')
    require(chosen['lattice/n4']['status'] == 'EVALUABLE' and chosen['layered/n4']['status'] == 'INSUFFICIENT_COMMON_SUPPORT', 'support gates')
    validate_pairs(chosen, ledger)
    require(select(list(reversed(ledger)), cfg) == chosen, 'ledger order does not change selection')
    replaced = [{**r, 'relation_sha256': 'changed'} for r in ledger]
    require(select(replaced, cfg) == chosen, 'relation hashes not used for selection')
    records = []
    for r in ledger:
        if r['family'] == 'layered':
            continue
        x = int(r['family'] == 'lattice')
        records.append({**r, 'features': dict(D=[r['R']/6, r['H']/4], B=[x, 1-x], P123=[1-x, x])})
    result = analysis.evaluate(chosen, records, cfg)
    report = result['cells']['lattice/n4']['methods']
    require(report['D']['balanced_accuracy'] == 0.5 and report['B']['balanced_accuracy'] == 1,
            'known confound-only chance and feature separation')
    require(report['B']['label_swap']['one_sided_label_swap_p'] == 1/16, 'known exact label-swap p')
    lookup = {r['id']: r for r in records}
    ordered = [lookup[name] for split in ['train', 'test'] for p in chosen['lattice/n4'][split]['pairs'] for name in p['ids']]
    for model in cfg['features']['models']:
        require(scalar_predictions(ordered, ['minkowski', 'lattice'], model) ==
                [(p['id'], p['predicted']) for p in report[model]['predictions']], 'toy scalar prediction oracle')
    poisoned = copy.deepcopy(ordered)
    for r in poisoned:
        if r['split'] == 'test':
            r['features']['B'] = [1000, -1000]
    altered = prior_geometry.predict(poisoned, ['minkowski', 'lattice'], 'B')
    require(all(altered[k] == report['B'][k] for k in ['training_mean', 'training_scale', 'standardized_centroids']),
            'test values cannot affect model fit')
    # Exhaustive label-swap oracle including pairs with identical predictions.
    patterns = [[0, 1], [1, 0], [0, 0], [1, 1]]
    cases = 0
    for a, b in product(patterns, repeat=2):
        labels = a+b
        predictions = [dict(truth=i % 2, predicted=v) for i, v in enumerate(labels)]
        scores, pval = analysis.pair_scores(predictions)
        observed = sum(v == i % 2 for i, v in enumerate(labels))
        counts = []
        for flips in product([0, 1], repeat=2):
            counts.append(sum(int(labels[2*j] == flip)+int(labels[2*j+1] == 1-flip) for j, flip in enumerate(flips)))
        require(pval['one_sided_label_swap_p'] == sum(x >= observed for x in counts)/4, 'brute label-swap distribution')
        cases += 1
    rejected = []
    def rejects(name, function):
        try:
            function()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('negative control failed '+name)
    rejects('missing candidate', lambda: validate_ledger(ledger[:-1], cfg))
    wrong = copy.deepcopy(chosen)
    wrong['lattice/n4']['test']['pairs'][0]['R'] += 1
    rejects('inexact matched relation count', lambda: validate_pairs(wrong, ledger))
    wrong2 = copy.deepcopy(chosen)
    wrong2['lattice/n4']['test']['pairs'][1] = wrong2['lattice/n4']['test']['pairs'][0]
    rejects('reused paired observation', lambda: validate_pairs(wrong2, ledger))
    for family in ['minkowski', 'layered', 'lattice', 'jittered_lattice']:
        record = prior_geometry.sample(family, 4, 'matched-toy-only', 0)
        record['rng_split'] = 'matched-toy-only'
        c = [[int(x) for x in row] for row in record['relation_rows']]
        entry = ledger_entry(record)
        require(independent_profile(c) == (entry['R'], entry['H']), 'tiny height oracle')
        record['features'] = prior_geometry.features(c)
        record['features']['D'] = [entry['R']/6, entry['H']/4]
        verify_features(record)
    bad = copy.deepcopy(record)
    bad['features']['intersections'][0][0][0] += 1
    rejects('corrupt intersection histogram', lambda: verify_features(bad))
    # Height checked for every naturally labelled four-node DAG closure.
    edges = [(i, j) for i in range(4) for j in range(i+1, 4)]
    from common import prior_core
    for bits in range(64):
        c = [[0]*4 for _ in range(4)]
        for k, (i, j) in enumerate(edges):
            c[i][j] = (bits >> k) & 1
        c = prior_core.closure(c)
        r = dict(id='toy', family='toy', n=4, split='toy', draw=0, rng_split='toy',
                 relation_rows=[''.join(map(str, row)) for row in c])
        e = ledger_entry(r)
        require(independent_profile(c) == (e['R'], e['H']), 'all tiny DAG heights')
    return dict(status='PASS_TOY_ONLY', exhaustive_label_swap_cases=cases,
                upper_DAG_closures=64, rejected_controls=rejected, target_generation=False)


if __name__ == '__main__':
    import json
    print(json.dumps(run(), indent=2))
