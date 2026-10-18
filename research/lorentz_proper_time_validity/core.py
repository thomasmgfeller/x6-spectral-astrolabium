"""Finite-binomial validity map. Apache-2.0; no stochastic sampler."""
from functools import lru_cache
import math
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import betaincinv
from scipy.stats import binom


def inverse_odds(p, r):
    """Invert p=r*q/(1-q+r*q); also acts on arrays."""
    if not math.isfinite(r) or r <= 0:
        raise ValueError('positive finite relative intensity required')
    return p / (r + (1-r)*p)


@lru_cache(None)
def nodes(order):
    return leggauss(order)


def volume(a, h, order=64):
    """4D conformal diamond volume without the cancelling 4*pi/3 factor."""
    if not 0 < a <= 1 or not 0 <= h < 2:
        raise ValueError('0<a<=1 and 0<=h<2 required')
    x, w = nodes(order)
    t = (x+1)*a/4
    return float(a/4 * np.dot(w, (a/2-t)**3 * ((1-h*t)**-4+(1+h*t)**-4)))


def geometric_cells(contract):
    for theta in contract['theta_grid']:
        for d in contract['dimensions']:
            yield dict(model='uniform_flat', d=d, theta=theta, planning_theta=theta,
                       a=theta, parameter=0., p=theta**d, geometry='flat', relative_intensity=1.)
        for h in contract['models']['de_sitter_h']:
            a = 2*math.tanh(theta*math.atanh(h/2))/h
            pp = [volume(a,h,o)/volume(1.,h,o) for o in contract['numerics']['gauss_legendre_orders']]
            if max(pp)-min(pp) > contract['numerics']['geometry_absolute_tolerance']:
                raise ArithmeticError('quadrature gate failed')
            common = dict(d=4, planning_theta=theta, a=a, parameter=h, p=pp[-1],
                          quadrature_gap=max(pp)-min(pp))
            yield dict(common, model='de_sitter', theta=theta, geometry='curved', relative_intensity=None)
            q = a**4
            yield dict(common, model='density_twin', theta=a, geometry='flat',
                       relative_intensity=pp[-1]*(1-q)/(q*(1-pp[-1])))
        for b in contract['models']['density_beta']:
            p = theta**4*(1+b*theta**2/15)/(1+b/15)
            q = theta**4
            yield dict(model='density', d=4, theta=theta, planning_theta=theta,
                       a=theta, parameter=b, p=p, geometry='flat',
                       relative_intensity=p*(1-q)/(q*(1-p)))
        for z in contract['models']['thinning']:
            r = z['inside']/z['outside']
            q = theta**4
            yield dict(model='thinning', d=4, theta=theta, planning_theta=theta,
                       a=theta, parameter=r, p=r*q/(1-q+r*q), geometry='flat',
                       relative_intensity=r, retention_probability=z['inside']*q+z['outside']*(1-q))


def interval_arrays(k, m, d, bounds, alpha):
    k = np.asarray(k)
    if type(m) is not int or m < 1 or type(d) is not int or d < 2:
        raise ValueError('positive integer m and integer d>=2 required')
    if np.any(k < 0) or np.any(k > m) or np.any(k != np.floor(k)):
        raise ValueError('integer counts in [0,m] required')
    rl, ru = bounds
    if not 0 < rl <= ru or not 0 < alpha < 1:
        raise ValueError('ordered positive bounds and 0<alpha<1 required')
    lo = np.zeros(k.shape)
    hi = np.ones(k.shape)
    sel = k > 0
    lo[sel] = betaincinv(k[sel], m-k[sel]+1, alpha/2)
    sel = k < m
    hi[sel] = betaincinv(k[sel]+1, m-k[sel], 1-alpha/2)
    return inverse_odds(lo, ru)**(1/d), inverse_odds(hi, rl)**(1/d)


def summarize(cell, m, name, bounds, contract):
    p, theta, d = cell['p'], cell['theta'], cell['d']
    tail = contract['numerics']['binomial_tail_per_side']
    kmin, kmax = int(binom.ppf(tail,m,p)), int(binom.isf(tail,m,p))
    k = np.arange(kmin,kmax+1)
    mass = binom.pmf(k,m,p)
    omitted = float(binom.cdf(kmin-1,m,p)+binom.sf(kmax,m,p))
    if abs(float(mass.sum())+omitted-1) > contract['numerics']['mass_tolerance'] or omitted > 2.01*tail:
        raise ArithmeticError('binomial mass/tail gate failed')
    lo, hi = interval_arrays(k,m,d,bounds,contract['confidence_alpha'])
    center = 2*lo*hi/(lo+hi)
    radius = (hi-lo)/(hi+lo)
    raw_error = (k/m)**(1/d)/theta-1
    precision = radius <= contract['relative_precision']
    def probability(mask):
        return float(mass[mask].sum())
    coverage = probability((lo <= theta) & (theta <= hi))
    pprecision = probability(precision)
    r = cell['relative_intensity']
    in_class = cell['geometry']=='flat' and bounds[0]-1e-14 <= r <= bounds[1]+1e-14
    tol = contract['numerics']['probability_tolerance']
    numeric_pass = (coverage >= 1-contract['confidence_alpha']-tol and
                    pprecision >= contract['required_precision_probability']-tol)
    # Limiting interval uses the true observed p; it is not extra data to the estimator.
    limlo, limhi = inverse_odds(p,bounds[1])**(1/d), inverse_odds(p,bounds[0])**(1/d)
    max_abs_error = max(1.,1/theta-1.)
    return dict(cell, m=m, interval=name, intensity_bounds=bounds, in_assumed_class=in_class,
                status=('OUTSIDE_ASSUMED_CLASS' if not in_class else
                        'MEETS_DECLARED_GRID_CRITERIA' if numeric_pass else 'INSUFFICIENT_GRID_PRECISION'),
                meets_numeric_criteria=numeric_pass, expected_K=m*p,
                zero_count_probability=float(binom.pmf(0,m,p)), coverage=coverage,
                raw_relative_bias=float(np.dot(mass,raw_error)),
                raw_relative_rmse=float(np.sqrt(np.dot(mass,raw_error**2))),
                raw_within_10percent_probability=probability(np.abs(raw_error)<=contract['relative_precision']),
                precision_probability=pprecision,
                false_precision_probability=probability(precision & (np.abs(center/theta-1)>contract['relative_precision'])),
                asymptotic_raw_relative_bias=p**(1/d)/theta-1,
                asymptotic_interval_relative_radius=(limhi-limlo)/(limhi+limlo),
                support=[kmin,kmax], omitted_probability=omitted,
                raw_bias_tail_bound=omitted*max_abs_error,
                raw_mse_tail_bound=omitted*max_abs_error**2)


def evaluate(contract):
    rows=[]
    for cell in geometric_cells(contract):
        for m in contract['observed_counts']:
            for name,bounds in contract['intervals'].items():
                if name=='scope' or (name!='nominal' and (cell['d']!=4 or cell['geometry']!='flat')):
                    continue
                rows.append(summarize(cell,m,name,bounds,contract))
    return rows
