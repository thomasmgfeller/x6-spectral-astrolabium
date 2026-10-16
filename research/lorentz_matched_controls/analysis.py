"""Fixed training-only classifiers and pair-preserving conditional evaluation."""
import math
import numpy as np
from common import prior_core, prior_geometry, require


def pair_scores(predictions):
    require(len(predictions) % 2 == 0, 'paired observation count')
    scores, discordant, correct_orientation = [], 0, 0
    for first, second in zip(predictions[::2], predictions[1::2]):
        require(first['truth'] == 0 and second['truth'] == 1, 'pair orientation')
        scores.append((int(first['predicted'] == 0)+int(second['predicted'] == 1))/2)
        if first['predicted'] != second['predicted']:
            discordant += 1
            correct_orientation += int(first['predicted'] == 0)
    tail = sum(math.comb(discordant, k) for k in range(correct_orientation, discordant+1))/(2**discordant)
    return np.asarray(scores), dict(discordant_predicted_pairs=discordant,
                                   correctly_oriented_pairs=correct_orientation,
                                   one_sided_label_swap_p=tail)


def evaluate(selection, records, cfg):
    lookup = {r['id']: r for r in records}
    cells = {}
    for key, cell in selection.items():
        if cell['status'] != 'EVALUABLE':
            cells[key] = dict(status=cell['status'], train_eligible=cell['train']['eligible'],
                              test_eligible=cell['test']['eligible'])
            continue
        rr = [lookup[name] for split in ['train', 'test'] for pair in cell[split]['pairs'] for name in pair['ids']]
        n_pairs = len(cell['test']['pairs'])
        rng = prior_core.Stream('matched-bootstrap', cell['control'], cell['n'])
        indices = np.array([[rng.below(n_pairs) for _ in range(n_pairs)] for _ in range(2000)])
        methods, scores = {}, {}
        for model in cfg['features']['models']:
            report = prior_geometry.predict(rr, ['minkowski', cell['control']], model)
            scores[model], permutation = pair_scores(report['predictions'])
            require(abs(float(scores[model].mean())-report['balanced_accuracy']) < 1e-14, 'pair accuracy equals balanced accuracy')
            report['test_pair_accuracy'] = scores[model].tolist()
            report['conditional_pair_bootstrap_95'] = np.quantile(scores[model][indices].mean(axis=1), [0.025, 0.975], method='linear').tolist()
            report['label_swap'] = permutation
            methods[model] = report
        require(methods['D']['balanced_accuracy'] == 0.5, 'confound-only classifier must be at chance')
        difference = scores['B+P123']-scores['B']
        gain = float(difference.mean())
        interval = np.quantile(difference[indices].mean(axis=1), [0.025, 0.975], method='linear').tolist()
        cells[key] = dict(status='EVALUABLE', methods=methods, incremental=dict(gain=gain,
                         paired_bootstrap_95=interval, meets_numerical_threshold=bool(gain >= 0.05 and interval[0] > 0)))
    primary_key = f"{cfg['analysis']['primary_cell']['control']}/n{cfg['analysis']['primary_cell']['n']}"
    primary_cell = cells[primary_key]
    if primary_cell['status'] != 'EVALUABLE':
        primary = dict(cell=primary_key, status='INSUFFICIENT_COMMON_SUPPORT')
    else:
        primary = dict(cell=primary_key, **primary_cell['incremental'],
                       status='POSITIVE_CONDITIONAL_INCREMENT' if primary_cell['incremental']['meets_numerical_threshold'] else 'NO_DEMONSTRATED_INCREMENT')
    return dict(cells=cells, primary=primary, bootstrap_replicates=2000,
                scope='Conditional on selected common support and fixed training; secondary results descriptive.')


def summarize(report):
    cells = {}
    for key, cell in report['cells'].items():
        if cell['status'] != 'EVALUABLE':
            cells[key] = cell
        else:
            cells[key] = dict(status=cell['status'], incremental=cell['incremental'],
                methods={name: {k: v for k, v in row.items() if k in
                         ['confusion', 'balanced_accuracy', 'conditional_pair_bootstrap_95', 'label_swap']}
                         for name, row in cell['methods'].items()})
    return {**report, 'cells': cells}
