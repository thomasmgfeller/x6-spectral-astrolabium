"""SPDX-License-Identifier: Apache-2.0
Seed-level bounds: no independence assumption for points within a cloud.
"""
import math
import numpy as np
from scipy.stats import beta


def cp(k, n, alpha):
    return [0.0 if k == 0 else float(beta.ppf(alpha / 2, k, n-k+1)),
            1.0 if k == n else float(beta.ppf(1-alpha / 2, k+1, n-k))]


def tail_upper(k, n, delta):
    return 1.0 if k == n else float(beta.ppf(1-delta, k+1, n-k))


def bounded_mean(values, ideal, m, alpha):
    """Clip to a fixed range; explicitly bound both omitted tails.

    Four events at alpha/4: two empirical Bernstein bounds (Maurer &
    Pontil 2009, Theorem 4), and two one-sided Clopper-Pearson tail bounds.
    Clipping width uses an ideal variance only as a prechosen constant.
    Its validity does NOT require the actual cloud counts to be binomial.
    """
    x = np.asarray(values, dtype=float)
    assert x.ndim == 1 and len(x) >= 2 and np.all((0 <= x) & (x <= 1))
    n = len(x)
    a = max(0.0, ideal - 8*math.sqrt(ideal*(1-ideal)/m))
    b = min(1.0, ideal + 8*math.sqrt(ideal*(1-ideal)/m))
    y = np.clip(x, a, b)
    log = math.log(8/alpha)
    radius = math.sqrt(2*float(np.var(y, ddof=1))*log/n) + 7*(b-a)*log/(3*(n-1))
    low_tail, high_tail = int(np.count_nonzero(x < a)), int(np.count_nonzero(x > b))
    low_up, high_up = tail_upper(low_tail, n, alpha/4), tail_upper(high_tail, n, alpha/4)
    lo = max(0.0, float(y.mean()) - radius - a*low_up)
    hi = min(1.0, float(y.mean()) + radius + (1-b)*high_up)
    return dict(mean=float(x.mean()), interval=[lo, hi], clipping=[a, b],
                clipped_mean=float(y.mean()), bernstein_radius=radius,
                tail_counts=[low_tail, high_tail], tail_upper=[low_up, high_up])


def equivalence(interval, acceptable):
    lo, hi = interval
    a, b = acceptable
    if a <= lo and hi <= b:
        return 'PASS'
    if hi < a or lo > b:
        return 'FAIL'
    return 'UNENTSCHIEDEN'


def minimum(interval, threshold):
    if interval[0] >= threshold:
        return 'PASS'
    if interval[1] < threshold:
        return 'FAIL'
    return 'UNENTSCHIEDEN'


def interval_table(m, d, eps):
    k = np.arange(m+1)
    low_p = np.zeros(m+1)
    high_p = np.ones(m+1)
    low_p[1:] = beta.ppf(.025, k[1:], m-k[1:]+1)
    high_p[:-1] = beta.ppf(.975, k[:-1]+1, m-k[:-1])
    native_low, native_high = low_p**(1/d), high_p**(1/d)
    low, high = native_low/(1+eps), native_high/(1-eps)
    center = 2*low*high/(low+high)
    radius = (high-low)/(high+low)
    return dict(low=low, high=high, center=center, radius=radius,
                native_low=native_low, native_high=native_high)


def marginal_specs(d):
    specs = [(f'{kind}_{j}', q) for kind in ['time', 'radial']
             for j, q in enumerate([.25, .5, .75])]
    qs = [.5] if d == 2 else [.25, .5, .75]
    specs += [(f'angle_{axis}_{j}', q) for axis in range(d-1) for j, q in enumerate(qs)]
    return specs
