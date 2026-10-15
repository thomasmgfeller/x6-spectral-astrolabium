"""Exact finite-design calculations for the unchanged V1 diagnostic gates.

Planning alternatives are assumptions, never estimates from the small pilot.
No Monte Carlo. Conditional multinomial summation retains paired dependence.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.stats import beta, binom


def lower(k, n, alpha):
    k = np.asarray(k)
    return np.where(k == 0, 0.0, beta.ppf(alpha, np.maximum(k, 1), n-k+1))


def upper(k, n, alpha):
    k = np.asarray(k)
    return np.where(k == n, 1.0, beta.ppf(1-alpha, k+1, np.maximum(n-k, 1)))


def negative_power(n, true_fpr, alpha=0.025, maximum=0.01):
    # Accept exactly those k whose upper CP limit is <= maximum.
    k = int(binom.ppf(alpha, n, maximum))
    if binom.cdf(k, n, maximum) > alpha:
        k -= 1
    return {'n':n, 'largest_accepted_false_alarm_count':k,
            'power':float(binom.cdf(k, n, true_fpr)) if k >= 0 else 0.0}


def positive_power(n, probabilities, alpha=0.025, sensitivity_min=0.8, gain_min=0.05):
    both, win, loss, neither = probabilities
    if (min(probabilities) < 0 or not math.isclose(sum(probabilities), 1, abs_tol=1e-12)
            or win >= 1 or both+neither <= 0):
        raise ValueError('INVALID_PLANNING_PROBABILITIES')
    k = np.arange(n+1)
    needed = np.flatnonzero(lower(k, n, alpha) >= sensitivity_min)
    if not len(needed):
        return 0.0
    minimum_tp = int(needed[0])
    win_lower, loss_upper = lower(k, n, alpha/2), upper(k, n, alpha/2)
    p_w = binom.pmf(k, n, win)
    terms = []
    for w in range(n+1):
        max_l = min(n-w, int(np.searchsorted(loss_upper, win_lower[w]-gain_min, side='left'))-1)
        if max_l < 0 or p_w[w] == 0:
            continue
        losses = np.arange(max_l+1)
        p_l_given_w = binom.pmf(losses, n-w, loss/(1-win))
        p_enough_both = binom.sf(minimum_tp-w-1, n-w-losses, both/(both+neither))
        terms.append(float(p_w[w]*np.sum(p_l_given_w*p_enough_both)))
    return math.fsum(terms)


def plan():
    alpha = 0.05/2
    minimum_zero = math.ceil(math.log(alpha)/math.log1p(-0.01))
    alternatives = {'main':[0.70,0.20,0.05,0.05], 'smaller_gain':[0.75,0.15,0.05,0.05]}
    grid = [100,200,400,800,1200,1600,2400]
    positive = {name:[{'n':n, 'joint_sensitivity_and_gain_power':positive_power(n, probs)} for n in grid]
                for name, probs in alternatives.items()}
    negative = {}
    for rate in [0.001,0.002,0.005]:
        # First n satisfying the specified component power, scanning every n.
        chosen = next((negative_power(n, rate) for n in range(1,20001)
                       if negative_power(n, rate)['power'] >= 0.95), None)
        negative[str(rate)] = chosen
    chosen_positive = next(row for row in positive['main'] if row['joint_sensitivity_and_gain_power'] >= 0.95)
    chosen_negative = negative['0.002']
    # Two claims, each with a positive joint gate and a healthy gate: union bound.
    joint_lower = max(0.0, 1-2*((1-chosen_positive['joint_sensitivity_and_gain_power'])+(1-chosen_negative['power'])))
    return {'schema':'x6.industrial.v1-planning/1','status':'CONDITIONAL_PLANNING_ONLY',
        'unchanged_gates':{'family_alpha':0.05,'registered_claim_count':2,'alpha_per_claim':alpha,
                           'sensitivity_min':0.8,'strict_sensitivity_gain_min':0.05,'false_positive_rate_max':0.01},
        'zero_false_alarms':{'minimum_independent_healthy_units':minimum_zero,
            'upper_at_367':-math.expm1(math.log(alpha)/367),
            'upper_at_368':-math.expm1(math.log(alpha)/368),
            'upper_at_two_if_iid':-math.expm1(math.log(alpha)/2),
            'probability_of_zero_at_368_if_true_fpr_0_002':float(binom.pmf(0,368,0.002))},
        'positive_category_order':['both_correct','candidate_only_correct','baseline_only_correct','both_wrong'],
        'assumed_alternatives':alternatives,'positive_power_grid':positive,
        'healthy_component_target_power':0.95,'healthy_designs_by_assumed_true_fpr':negative,
        'illustrative_design_for_two_claims':{'positive_n_per_claim':chosen_positive['n'],
            'healthy_n_per_claim':chosen_negative['n'],
            'positive_joint_gate_power_per_claim':chosen_positive['joint_sensitivity_and_gain_power'],
            'healthy_gate_power_per_claim':chosen_negative['power'],
            'simultaneous_quality_gate_power_union_lower_bound':joint_lower,
            'scope':'Conditional on identical registered alternatives for both claims, iid comparable bearings within each class, and all deterministic resource/preservation gates passing. No cross-claim independence is assumed. Positive n is first passing grid value, not a global minimum.'},
        'not_estimated_from_pilot':True,'confirmation_authorized':False,
        'required_before_confirmation':['Justify alternatives and population with domain review.',
            'Obtain independent machine/site-aware development, validation, holdout and external data with rights and labels.',
            'Freeze candidate, baseline, thresholds, sample sizes and unchanged gates before access.',
            'If clustering invalidates iid: preregister a new cluster-aware design; do not multiply windows.']}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    value = plan()
    with a.output.open('x') as f:
        f.write(json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+'\n')
    print(json.dumps(value['illustrative_design_for_two_claims'], indent=2))
