"""Frozen estimators; no data-dependent fit ranges or cutoff selection."""
from collections import Counter
import numpy as np


def slope(x, y):
    x, y = np.asarray(x), np.asarray(y)
    dx = x-x.mean()
    return float(np.dot(dx, y-y.mean())/np.dot(dx, dx))


def summarize(records, contract):
    sizes = contract['sampling']['sizes']
    reps = contract['sampling']['replicates_per_size']
    primary = contract['analysis']['primary_sizes']
    summary = {'cohort_expected': len(sizes)*reps, 'cohort_observed': len(records), 'cells': [], 'fits': {}}
    complete = len(records) == len(sizes)*reps and len({(r['n'],r['replicate']) for r in records}) == len(records)
    for n in sizes:
        cell = [r for r in records if r['n'] == n]
        complete &= len(cell) == reps
        row = {'n': n, 'observed': len(cell), 'raw_statuses': dict(Counter(r['diagnostics']['raw']['status'] for r in cell)), 'cutoffs': {}}
        for coefficient in contract['regularization']['sensitivity_coefficients']:
            key = str(float(coefficient))
            outputs = [r['diagnostics']['cutoffs'][key] for r in cell]
            valid = [o['double']['entropy_nats'] for o in outputs if o['double']['status'] == 'OK']
            row['cutoffs'][key] = {'double_statuses': dict(Counter(o['double']['status'] for o in outputs)),
                'global_only_statuses': dict(Counter(o['global_only']['status'] for o in outputs)),
                'mean_entropy_nats': float(np.mean(valid)) if valid else None,
                'sample_sd': float(np.std(valid, ddof=1)) if len(valid)>1 else None}
        row['mean_region_count'] = float(np.mean([r['n_a'] for r in cell])) if cell else None
        summary['cells'].append(row)
    for coefficient in contract['regularization']['sensitivity_coefficients']:
        key = str(float(coefficient))
        good = [r for r in records if r['diagnostics']['cutoffs'][key]['double']['status'] == 'OK']
        if len(good) != len(sizes)*reps or not complete:
            summary['fits'][key] = {'status':'INCOMPLETE'}
            continue
        x = lambda subset: np.array([.5*np.log(r['n_a']) for r in subset])
        y = lambda subset: np.array([r['diagnostics']['cutoffs'][key]['double']['entropy_nats'] for r in subset])
        selected = [r for r in good if r['n'] in primary]
        groups = [np.array([i for i,r in enumerate(selected) if r['n']==n]) for n in primary]
        xx, yy = x(selected), y(selected)
        rng = np.random.default_rng(contract['analysis']['bootstrap_seed'])
        boot = []
        for _ in range(contract['analysis']['bootstrap_replicates']):
            ids = np.concatenate([rng.choice(g, len(g), replace=True) for g in groups])
            boot.append(slope(xx[ids], yy[ids]))
        fit = {'status':'OK', 'primary_slope':slope(xx, yy), 'primary_intercept':float(yy.mean()-slope(xx,yy)*xx.mean()),
               'ci95':np.quantile(boot,[.025,.975]).tolist(), 'all_sizes_slope':slope(x(good), y(good)), 'adjacent_mean_slopes':[]}
        for left,right in zip(sizes[:-1], sizes[1:]):
            a, b = [r for r in good if r['n']==left], [r for r in good if r['n']==right]
            fit['adjacent_mean_slopes'].append({'sizes':[left,right], 'slope':float((y(b).mean()-y(a).mean())/(x(b).mean()-x(a).mean()))})
        summary['fits'][key] = fit
    primary_key = str(float(contract['regularization']['primary_coefficient']))
    f = summary['fits'][primary_key]
    target = contract['analysis']['reference_slope']
    margin = contract['analysis']['engineering_equivalence_margin']
    low, high = target-margin, target+margin
    valid = complete and all(v['status']=='OK' for v in summary['fits'].values())
    equivalence = valid and low <= f['ci95'][0] <= f['ci95'][1] <= high
    sensitivity = valid and all(low <= v['primary_slope'] <= high for v in summary['fits'].values())
    summary.update(reference_band=[low,high], complete=bool(valid), primary_equivalence=bool(equivalence),
                   cutoff_sensitivity_acceptable=bool(sensitivity),
                   status='REFERENCE_AGREEMENT' if equivalence and sensitivity else ('REFERENCE_NOT_ESTABLISHED' if valid else 'INCOMPLETE'))
    return summary
