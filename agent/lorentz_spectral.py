"""Small, auditable Lorentzian spectral-geometry replication benchmarks.

Integer characteristic polynomials classify finite orders exactly. Numerical
causal-diamond experiments are reported separately and never prove a limit.
Primary definitions and normalization: docs/LORENTZ_RESEARCH.md.
"""
from __future__ import annotations

import itertools
import math
from collections import defaultdict

import numpy as np

TABLE_TARGETS = {3: (5, 4), 4: (16, 14), 5: (63, 53)}
REFERENCE_SEED = 20260805
DIAMOND_SIZES = (64, 128)
REPLICATES = 3
COMPARE_RANKS = 8


def validate_order(c):
    a = np.asarray(c)
    if a.ndim != 2 or a.shape[0] != a.shape[1] or not 1 <= len(a) <= 256:
        raise ValueError("expected a bounded square causal matrix")
    if not np.all((a == 0) | (a == 1)) or np.any(np.diag(a)):
        raise ValueError("causal relation must be binary and irreflexive")
    a = a.astype(np.int64)
    if np.any(a & a.T) or np.any((a @ a > 0) & (a == 0)):
        raise ValueError("relation must be asymmetric and transitively closed")
    return a


def charpoly(a, budget):
    """Faddeev-LeVerrier over Python integers, coefficients descending incl. 1.

No floating-point equality or rounded eigenvalues define a spectral class.
The recurrence enforces exact division at every step.
"""
    a = np.array(a, dtype=object)
    n = len(a)
    identity = np.eye(n, dtype=object)
    b, coefficients = identity, [1]
    for k in range(1, n + 1):
        budget.check()
        ab = a @ b
        trace = int(np.trace(ab))
        if trace % k:
            raise ArithmeticError("nonintegral characteristic coefficient")
        coefficient = -trace // k
        coefficients.append(coefficient)
        b = ab + coefficient * identity
    if np.any(b):
        raise ArithmeticError("Cayley-Hamilton residual")
    return tuple(coefficients)


def spectral_key(c, budget):
    c = np.array(c, dtype=object)
    s, a = c + c.T, c - c.T
    # These are fixed nonzero scalar multiples of the paper's SA, ASA, Com.
    return tuple(charpoly(m, budget) for m in (s, a, s @ a - a @ s))


def endpoints(c):
    return (int(np.sum(np.sum(c, axis=0) == 0)),
            int(np.sum(np.sum(c, axis=1) == 0)))


def canonical_key(c, budget):
    """Exhaustive isomorphism key; intentionally limited to n <= 5."""
    if len(c) > 5:
        raise ValueError("exhaustive canonicalization capped at five elements")
    best = None
    for p in itertools.permutations(range(len(c))):
        budget.check()
        key = c[np.ix_(p, p)].tobytes()
        if best is None or key < best:
            best = key
    return best


def enumerate_orders(n, budget):
    """All upper-triangle binary relations, transitivity filter, quotient by Sn.

Every finite order admits a natural labeling, so this exhausts isomorphism
classes. Reverse orders are not identified unless actually isomorphic.
"""
    if not 1 <= n <= 5:
        raise ValueError("enumeration capped at five elements")
    edges = list(itertools.combinations(range(n), 2))
    seen, result = set(), []
    for mask in range(1 << len(edges)):
        budget.check()
        c = np.zeros((n, n), dtype=np.int64)
        for bit, (i, j) in enumerate(edges):
            c[i, j] = (mask >> bit) & 1
        if np.any((c @ c > 0) & (c == 0)):
            continue
        key = canonical_key(c, budget)
        if key not in seen:
            seen.add(key)
            result.append(c)
    return result


def finite_order_track(rng, budget):
    rows, records, collisions = [], [], []
    for n, (expected_orders, expected_classes) in TABLE_TARGETS.items():
        orders = enumerate_orders(n, budget)
        classes, augmented = defaultdict(list), set()
        for index, c in enumerate(orders):
            budget.check()
            key = spectral_key(c, budget)
            end = endpoints(c)
            p = list(range(n))
            rng.shuffle(p)
            if spectral_key(c[np.ix_(p, p)], budget) != key:
                raise AssertionError("spectral invariance under relabeling failed")
            classes[key].append(index)
            augmented.add((key, end))
            records.append({"n": n, "index": index, "causal_matrix": c.tolist(),
                            "characteristic_polynomials_S_A_Com": key,
                            "minimal_maximal": end, "checked_permutation": p})
        observed = (len(orders), len(classes), len(augmented))
        expected = (expected_orders, expected_classes, expected_orders)
        if observed != expected:
            raise AssertionError(f"literature replication n={n}: {observed} != {expected}")
        groups = [v for v in classes.values() if len(v) > 1]
        for group in groups:
            collisions.append({"n": n, "indices": group})
        rows.append({"n": n, "nonisomorphic_orders": len(orders),
                     "spectral_classes": len(classes), "unresolved_groups": len(groups),
                     "classes_with_minimal_maximal_counts": len(augmented),
                     "literature_expected": expected, "replication": "EXACT_MATCH"})
    return {"finding": "LITERATURE_REPLICATION_EXACT_SMALL_ORDERS",
            "source": "https://arxiv.org/abs/2008.02291v1",
            "source_locations": "Tables 1 and 2, causal matrix C columns, n=3..5 only",
            "rows": rows, "records": records, "collisions": collisions,
            "arithmetic": "Python arbitrary-precision integers; characteristic polynomials",
            "novelty": "NOT_CLAIMED_REPLICATION",
            "limits": "No n=6..9 replication, no quill perturbation implementation, no continuum claim"}


def continuum_eigenvalues(count=COMPARE_RANKS):
    """Largest positive eigenvalues of the L=1 massless 1+1 causal diamond.

Union of 1/(n*pi) and 1/z for the positive nonzero roots tan(z)=2z.
The zero root is excluded. Bisection stays below each tangent pole.
"""
    values = [1 / (n * math.pi) for n in range(1, count + 1)]
    for n in range(count):
        lo = n * math.pi + (1e-7 if n == 0 else 0)
        hi = (n + 0.5) * math.pi - 1e-10
        for _ in range(70):
            mid = (lo + hi) / 2
            if math.tan(mid) - 2 * mid > 0:
                hi = mid
            else:
                lo = mid
        values.append(1 / ((lo + hi) / 2))
    return np.array(sorted(values, reverse=True)[:count])


def causal_diamond(points):
    p = np.asarray(points, dtype=float)
    if p.ndim != 2 or p.shape[1] != 2 or not np.all(np.isfinite(p)):
        raise ValueError("finite pairs of null coordinates required")
    return np.all(p[:, None, :] < p[None, :, :], axis=2).astype(np.int64)


def diamond_observation(seed, n, truth, budget):
    budget.check()
    rng = np.random.default_rng(seed)
    # Uniform conditional on N. No claim to sample an unconditioned Poisson N.
    points = rng.uniform(-1, 1, size=(n, 2))
    c = validate_order(causal_diamond(points))
    # Jones/Yazdi v3 Eq.14 convention; Monte Carlo integral measure V/N=4/N.
    h = 0.5j * (c.T - c) * (4.0 / n)
    if not np.array_equal(h, h.conj().T):
        raise AssertionError("causal propagator is not Hermitian")
    eig = np.linalg.eigvalsh(h)
    budget.check()
    permutation = rng.permutation(n)
    relabeled = np.linalg.eigvalsh(h[np.ix_(permutation, permutation)])
    relabel_error = float(np.max(np.abs(eig - relabeled)))
    pair_error = float(np.max(np.abs(eig + eig[::-1])))
    if max(relabel_error, pair_error) > 1e-10:
        raise AssertionError("propagator relabeling/pair symmetry cross-check failed")
    positive = eig[eig > 1e-12][::-1]
    if len(positive) < len(truth):
        raise AssertionError("insufficient nonzero modes for registered rank range")
    first = positive[:len(truth)]
    return {"seed": seed, "n": n, "null_coordinates": points.tolist(),
            "volume": 4.0, "integral_weight": 4.0/n,
            "positive_eigenvalues": positive.tolist(),
            "top_rank_relative_l2_error": float(np.linalg.norm(first-truth)/np.linalg.norm(truth)),
            "relabeling_max_abs_error": relabel_error, "pairing_max_abs_error": pair_error}


def propagator_track(seed_slot, budget):
    truth = continuum_eigenvalues()
    records, comparisons = [], []
    for n in DIAMOND_SIZES:
        sequences = {}
        for sequence, base in [("reference", REFERENCE_SEED),
                               ("comparison", 900_000_000 + seed_slot * 1_000_003)]:
            observations = []
            for replicate in range(REPLICATES):
                seed = base + n * 1009 + replicate * 97
                observation = diamond_observation(seed, n, truth, budget)
                observation.update({"sequence": sequence, "replicate": replicate})
                observations.append(observation)
                records.append(observation)
            sequences[sequence] = observations
        means = {k: np.mean([r["positive_eigenvalues"][:COMPARE_RANKS] for r in v], axis=0)
                 for k, v in sequences.items()}
        comparisons.append({"n": n, "replicates_per_sequence": REPLICATES,
                            "mean_top_eigenvalues": {k: v.tolist() for k, v in means.items()},
                            "mean_relative_l2_error": {
                                k: float(np.mean([r["top_rank_relative_l2_error"] for r in v]))
                                for k, v in sequences.items()},
                            "relative_distance_of_mean_spectra": float(
                                np.linalg.norm(means["comparison"]-means["reference"])/np.linalg.norm(truth))})
    return {"finding": "FINITE_SIZE_NUMERICAL_COMPARISON",
            "source": "https://arxiv.org/html/2606.00311v3",
            "source_locations": "Equations 11,12,14; volume normalization in Figure 3 caption",
            "analytic_top_eigenvalues_L1": truth.tolist(), "compared_positive_ranks": COMPARE_RANKS,
            "reference_seed": REFERENCE_SEED, "comparison_slot": seed_slot,
            "comparisons": comparisons, "records": records,
            "sampling": "uniform fixed-N samples in null square [-1,1]^2, massless 1+1 Minkowski",
            "novelty": "NOT_CLAIMED_KNOWN_ANALYTIC_CALIBRATION",
            "limits": "n=64,128 and three replicates; no asymptotic-law test, no fitted exponent or physical validation"}
