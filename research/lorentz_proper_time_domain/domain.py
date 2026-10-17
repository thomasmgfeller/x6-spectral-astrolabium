"""Finite order validation and conditional Minkowski interval inference.

Coordinates belong only to the simulation oracle. The infer function accepts
K, m, d and alpha; the order_count adapter accepts a FULL strict relation.
None of these interfaces certifies the continuum assumptions.
"""
import math
import numpy as np
from scipy.special import betaincinv
from scipy.stats import binom


def validate_order(relation):
    c = np.asarray(relation)
    if c.ndim != 2 or c.shape[0] != c.shape[1] or c.shape[0] == 0:
        raise ValueError("nonempty square relation required")
    if not np.all((c == 0) | (c == 1)):
        raise ValueError("binary relation required")
    c = c.astype(bool)
    n = len(c)
    diag = np.flatnonzero(np.diag(c))
    if len(diag):
        return {"valid": False, "reason": "SELF_RELATION", "witness": [int(diag[0])]}
    reciprocal = np.argwhere(c & c.T)
    if len(reciprocal):
        return {"valid": False, "reason": "TWO_CYCLE", "witness": reciprocal[0].tolist()}
    # Topological removal detects longer cycles even in an unclosed input.
    indegree = c.sum(axis=0).astype(int)
    ready = list(np.flatnonzero(indegree == 0))
    visited = 0
    while ready:
        i = ready.pop()
        visited += 1
        for j in np.flatnonzero(c[i]):
            indegree[j] -= 1
            if indegree[j] == 0:
                ready.append(j)
    if visited != n:
        return {"valid": False, "reason": "DIRECTED_CYCLE", "witness_remaining_nodes": np.flatnonzero(indegree > 0).tolist()}
    masks = [sum(1 << int(j) for j in np.flatnonzero(row)) for row in c]
    for i, mask in enumerate(masks):
        todo = mask
        while todo:
            bit = todo & -todo
            j = bit.bit_length() - 1
            missing = masks[j] & ~mask
            if missing:
                k = (missing & -missing).bit_length() - 1
                return {"valid": False, "reason": "MISSING_TRANSITIVE_RELATION", "witness": [i, j, k]}
            todo -= bit
    return {"valid": True, "reason": "FINITE_STRICT_POSET_ONLY"}


def order_count(relation, marks):
    audit = validate_order(relation)
    if not audit["valid"]:
        raise ValueError(str(audit))
    c = np.asarray(relation, dtype=bool)
    if len(marks) != 2 or any(type(v) is not int or not 0 <= v < len(c) for v in marks):
        raise ValueError("two marked indices required")
    p, q = marks
    if not c[p, q]:
        raise ValueError("marks must be strictly chronologically ordered")
    return int(np.count_nonzero(c[p] & c[:, q])), len(c) - 2


def probability_limits(m, alpha=0.05):
    if type(m) is not int or m < 1 or not 0 < alpha < 1:
        raise ValueError("positive integer m and 0<alpha<1 required")
    k = np.arange(m + 1)
    lo = np.zeros(m + 1)
    hi = np.ones(m + 1)
    lo[1:] = betaincinv(k[1:], m-k[1:]+1, alpha/2)
    hi[:-1] = betaincinv(k[:-1]+1, m-k[:-1], 1-alpha/2)
    return lo, hi


def infer(k, m, d, alpha=0.05):
    if type(d) is not int or d < 2 or type(k) is not int or not 0 <= k <= m:
        raise ValueError("d>=2 integer and integer 0<=K<=m required")
    lo, hi = probability_limits(m, alpha)
    return {"theta_hat": (k/m)**(1/d), "interval": [float(lo[k]**(1/d)), float(hi[k]**(1/d))]}


def exact_summary(d, m, theta, alpha=0.05):
    k = np.arange(m + 1)
    a = theta**d
    mass = binom.pmf(k, m, a)
    lo, hi = probability_limits(m, alpha)
    # Evaluate inclusion in probability space (same monotone transformation).
    covered = (lo <= a) & (a <= hi)
    estimate = (k/m)**(1/d)
    return {"d": d, "m": m, "theta": theta, "probability": a,
            "expected_K": m*a, "zero_probability": float((1-a)**m),
            "coverage": float(mass[covered].sum()),
            "bias": float(np.dot(mass, estimate-theta)),
            "rmse": float(np.sqrt(np.dot(mass, (estimate-theta)**2))),
            "mean_interval_width": float(np.dot(mass, hi**(1/d)-lo**(1/d))),
            "theta_upper_if_zero": float(hi[0]**(1/d)),
            "mass_sum": float(mass.sum())}


def chronological(x, y):
    delta = np.asarray(y) - np.asarray(x)
    return delta[..., 0] > np.linalg.norm(delta[..., 1:], axis=-1)


def endpoints(d, theta, placement, eta=0.4, shift=0.04):
    p, q = np.zeros(d), np.zeros(d)
    p[0], q[0] = -theta/2, theta/2
    if placement == "boosted_shifted":
        p[0], q[0] = -theta*math.cosh(eta)/2, theta*math.cosh(eta)/2
        p[1], q[1] = shift-theta*math.sinh(eta)/2, shift+theta*math.sinh(eta)/2
    elif placement != "central":
        raise ValueError("unknown placement")
    if not chronological(p, q) or abs(p[0])+np.linalg.norm(p[1:]) >= 0.5 or abs(q[0])+np.linalg.norm(q[1:]) >= 0.5:
        raise ValueError("endpoints not strictly included in unit outer diamond")
    return p, q


def sample_diamond(rng, shape, d):
    """Uniform volume sampler: half-width A has density proportional to A^(d-1)."""
    A = 0.5*rng.random(shape)**(1/d)
    t = np.where(rng.integers(0, 2, shape) == 0, -1.0, 1.0)*(0.5-A)
    direction = rng.normal(size=(*shape, d-1))
    norm = np.linalg.norm(direction, axis=-1)
    if np.any(norm == 0):
        raise ArithmeticError("zero random direction; no silent reseeding")
    radius = A*rng.random(shape)**(1/(d-1))
    space = direction*(radius/norm)[..., None]
    return np.concatenate((t[..., None], space), axis=-1)


def full_relation_squared(points):
    """Independent predicate for finite crosschecks: positive dt and dt^2>r^2."""
    delta = points[None, :, :] - points[:, None, :]
    return (delta[..., 0] > 0) & (delta[..., 0]**2 > np.sum(delta[..., 1:]**2, axis=-1))


def embedding_audit(relation, points):
    c = np.asarray(relation, dtype=bool)
    expected = full_relation_squared(np.asarray(points))
    if c.shape != expected.shape:
        raise ValueError("relation/embedding shape mismatch")
    bad = np.argwhere(c != expected)
    return {"matches_known_embedding": len(bad) == 0, "mismatches": len(bad), "first_mismatch": bad[0].tolist() if len(bad) else None}
