"""Prespecified fixed-budget evaluation; overlapping budgets are descriptive."""
from fractions import Fraction as Q
from functools import lru_cache
from math import comb
import numpy as np
from exact import (certificate, coefficients, probability, q_bounds, epsilon,
                   invert, confidence, relative_radius)
from support import contract, fraction_record, interval_record, quadrature


def mathematics():
    cert = certificate()
    rows = []
    for value in contract()['probability_grid']:
        h = Q(value)
        lo, hi = probability(h)
        quad = quadrature.pair_probability(float(h), 32)
        rows.append(dict(h=value, enclosure=[fraction_record(lo), fraction_record(hi)],
                         quadrature=quad, quadrature_absolute_discrepancy=float(abs(Q(quad)-(lo+hi)/2))))
    n, v = coefficients()
    return dict(status='PASS_RATIONAL_MONOTONICITY_AND_TAIL_CERTIFICATE',
        domain_h=['0', '1/2'], degree_z=16,
        certificate={k: fraction_record(x) for k, x in cert.items()},
        numerator_coefficients=[str(x) for x in n], volume_coefficients=[str(x) for x in v],
        probability_grid=rows)


def planning():
    rows = []
    for value in contract()['fresh_h']:
        h = Q(value)
        pl, pu = probability(h)
        first = None
        for m in contract()['planning_cloud_counts']:
            e = epsilon(128, m)
            outer = invert(pl-2*e, pu+2*e)
            radius = relative_radius(outer)
            passed = radius is not None and radius <= Q(1, 5)
            rows.append(dict(h=value, clouds=m, epsilon=fraction_record(e),
                sufficient_95pct_joint_coverage_and_precision=passed,
                worst_case_on_coverage_event=interval_record(outer)))
            if first is None and passed:
                first = m
        for row in rows:
            if row['h'] == value:
                row['first_passing_grid_budget'] = first
    return dict(scope='Sufficient fixed-budget design, no large-budget simulation; 2epsilon rule', rows=rows)


def analyze_cell(counts, h):
    n = 128
    pl, pu = probability(h)
    rows, records = [], []
    @lru_cache(None)
    def bounds(total, m):
        return confidence(total, n, m)
    for m in contract()['observed_group_sizes']:
        totals = counts.reshape(-1, m).sum(axis=1)
        covered = qualified = incompatible = wrong_precision = 0
        max_radius, min_radius = Q(0), Q(1)
        for index, total in enumerate(totals):
            total = int(total)
            interval = bounds(total, m)
            inside = interval is not None and interval[0] <= h <= interval[1]
            rad = relative_radius(interval)
            precision = rad is not None and rad <= Q(1, 5)
            covered += inside
            qualified += precision
            incompatible += interval is None
            if rad is not None:
                max_radius, min_radius = max(max_radius, rad), min(min_radius, rad)
            # Wrong precision means q falls outside the reported interval; its
            # 20% center guarantee is a consequence only on the coverage event.
            wrong_precision += precision and not inside
            records.append(dict(group_size=m, group_index=index, total_c2=total,
                h_interval=None if interval is None else [str(x) for x in interval],
                contains_true_h=bool(inside), qualifies_20pct=bool(precision)))
        rows.append(dict(h=str(h), group_size=m, groups=len(totals), covered=int(covered),
            coverage_observed=covered/len(totals), qualified_20pct=int(qualified),
            incompatible=int(incompatible), qualified_but_noncovering=int(wrong_precision),
            min_radius=fraction_record(min_radius), max_radius=fraction_record(max_radius)))
    # Counterfactual same relations with flat metric and nonuniform intensity.
    full_interval = bounds(int(counts.sum()), len(counts))
    twin = dict(geometry='flat conformal-density twin', metric_q=0,
        same_relations=True, classification='OUTSIDE_UNIFORM_DENSITY_ASSUMPTION',
        restricted_uniform_model_output=interval_record(full_interval),
        contains_metric_q_zero=bool(full_interval is not None and full_interval[0] == 0))
    return dict(h=str(h), rows=rows, groups=records, density_twin=twin,
                true_probability=[fraction_record(pl), fraction_record(pu)])
