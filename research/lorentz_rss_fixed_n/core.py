"""Conditional RSS coefficients and order-only chain statistics. Apache-2.0."""
from fractions import Fraction as Q
from math import comb, factorial, gamma
import numpy as np


def coefficients(d, k):
    if type(d) is not int or type(k) is not int or d < 2 or k < 1:
        raise ValueError('integer dimension >= 2 and chain size >= 1 required')
    alpha = -Q(d*k, 12*(k*d+2)*((k+1)*d+2))
    beta = Q(d*k, 12*((k+1)*d+2))
    a1, b1 = -Q(d, 24*(d+1)*(d+2)), Q(d, 24*(d+1))
    return alpha, beta, alpha-k*a1, beta-k*b1


def flat_probability(d, k):
    coefficients(d, k)
    return (factorial(k)/k * (gamma(d+1)/2)**(k-1)*gamma(d/2)*gamma(d)
            / (gamma(k*d/2)*gamma((k+1)*d/2)))


def de_sitter_slope(k):
    _, _, a, b = coefficients(4, k)
    return a-b/4


def overlap_weights(n, k, ell):
    """Probability that a fixed k-subset and random ell-subset overlap in s."""
    if not (1 <= k <= n and 1 <= ell <= n):
        raise ValueError('subset sizes must be in 1..n')
    return [Q(comb(k, s)*comb(n-k, ell-s), comb(n, ell))
            if 0 <= ell-s <= n-k else Q(0) for s in range(min(k, ell)+1)]


def chain_sums(c, weights=None):
    """Counts all 2/3/4-element chains, including non-link relations.

    c must be the complete strict order of the sampled points; callers validate
    geometry independently. Rows of weights are separate importance functions.
    This is not a sampler or a curvature estimator.
    """
    c = np.asarray(c)
    if c.ndim != 2 or c.shape[0] != c.shape[1] or len(c) < 4:
        raise ValueError('square order of size >= 4 required')
    if np.any(np.diag(c)) or np.any((c != 0) & (c != 1)):
        raise ValueError('binary, irreflexive order required')
    if weights is None:
        paths = np.ones(len(c), dtype=np.int64)
        a = c.astype(np.int64)
        result = []
        for _ in range(3):
            paths = paths @ a
            result.append(int(paths.sum()))
        return np.array(result, dtype=np.int64)
    w = np.atleast_2d(np.asarray(weights, dtype=float))
    if w.shape[1] != len(c) or not np.all(np.isfinite(w)) or np.any(w < 0):
        raise ValueError('finite nonnegative weights of matching length required')
    paths = w.copy()
    a = c.astype(float)
    result = []
    for _ in range(3):
        paths = (paths @ a)*w
        result.append(paths.sum(axis=1))
    return np.stack(result, axis=1)


def taylor_sums(c, times):
    """h^2 coefficient of chain products of normalized (1-h*t)^-4.

    For one point w=1+4ht+h²(10t²-1/6)+O(h³). The 1/6 comes from
    E_flat[t²]=1/60 in this 4D coordinate diamond. Polynomial convolution
    through the order computes the full coefficient, without finite differences.
    """
    t = np.asarray(times)
    w = np.array([np.ones(len(t)), 4*t, 10*t*t-1/6])
    paths = w.copy()
    a = np.asarray(c, dtype=float)
    out = []
    for _ in range(3):
        prev = paths @ a
        paths = np.array([prev[0], prev[1]+prev[0]*w[1],
                          prev[2]+prev[1]*w[1]+prev[0]*w[2]])
        out.append(paths[2].sum())
    return np.array(out)
