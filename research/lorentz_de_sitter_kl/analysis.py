"""Frozen sufficient-budget comparison and paired fresh-cloud checks."""
from fractions import Fraction as Q
from core import reference, first_sufficient, design_interval, confidence
from support import contract, interval_record, fraction_record


def planning():
    rows = []
    for value in contract()['planning_h']:
        h = Q(value)
        found = {}
        for method in ('Hoeffding', 'KL'):
            budget = first_sufficient(h, 128, method, contract()['maximum_planning_clouds'])
            found[method] = budget
            rows.append(dict(h=value, method=method, sufficient_clouds=budget,
                sufficient_interval=None if budget is None else interval_record(design_interval(h, 128, budget, method)),
                adjacent_interval=None if budget is None or budget == 1 else interval_record(design_interval(h, 128, budget-1, method))))
        ratio = Q(found['Hoeffding'], found['KL']) if all(found.values()) else None
        for row in rows:
            if row['h'] == value:
                row['budget_reduction_factor'] = None if ratio is None else fraction_record(ratio)
    factors = [Q(r['budget_reduction_factor']['exact']) for r in rows
               if r['method'] == 'KL' and r['budget_reduction_factor'] is not None]
    passed = len(factors) == len(contract()['planning_h']) and min(factors) >= 2
    return dict(primary_status='TWO_FOLD_BUDGET_GAIN_CERTIFIED' if passed else 'TWO_FOLD_BUDGET_GAIN_NOT_ESTABLISHED',
        fresh_run_gate=passed, rows=rows,
        claim='Sufficient fixed-budget certificate boundaries, not optimal sample sizes or executed cloud counts')


def analyze(counts, cell):
    h = Q(cell['h'])
    rows, groups = [], []
    for m in cell['group_sizes']:
        totals = counts.reshape(-1, m).sum(axis=1)
        summary = {name:dict(covered=0,qualified=0,incompatible=0,qualified_noncovering=0)
                   for name in ('Hoeffding', 'KL')}
        for i, total in enumerate(totals):
            total = int(total)
            intervals = dict(Hoeffding=reference.confidence(total, 128, m), KL=confidence(total, 128, m))
            old, new = intervals['Hoeffding'], intervals['KL']
            assert new is None or (old is not None and old[0] <= new[0] <= new[1] <= old[1])
            record = dict(group_size=m, group_index=i, total_c2=total, intervals={})
            for method, interval in intervals.items():
                inside = interval is not None and interval[0] <= h <= interval[1]
                radius = reference.relative_radius(interval)
                qualified = radius is not None and radius <= Q(1, 5)
                summary[method]['covered'] += int(inside)
                summary[method]['qualified'] += int(qualified)
                summary[method]['incompatible'] += int(interval is None)
                summary[method]['qualified_noncovering'] += int(qualified and not inside)
                record['intervals'][method] = dict(**interval_record(interval), contains_true_h=bool(inside))
            groups.append(record)
        for method in ('Hoeffding', 'KL'):
            rows.append(dict(h=cell['h'], clouds_per_group=m, groups=len(totals), method=method,
                             **summary[method]))
    full = confidence(int(counts.sum()), 128, len(counts))
    twin = dict(status='OUTSIDE_UNIFORM_DENSITY_ASSUMPTION', same_relations=True,
                flat_metric_q=0, restricted_interval_contains_zero=bool(full is not None and full[0] == 0))
    return dict(h=cell['h'], rows=rows, groups=groups, density_twin=twin,
        observation='Nested group sizes reuse clouds; no pooled independent success rate')
