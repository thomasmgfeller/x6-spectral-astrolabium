"""One-shot conditional-K chain-height diagnostic, not a curvature detector."""
import sys
from pathlib import Path
import numpy as np
from sequential import require

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/"lorentz_proper_time_domain"))
from domain import sample_diamond, validate_order


def height(relation):
    c = np.asarray(relation)
    if c.shape == (0, 0):
        return 0
    audit = validate_order(c)
    require(audit["valid"], str(audit))
    c = c.astype(bool)
    h = np.ones(len(c), dtype=int)
    for j in np.argsort(c.sum(axis=0), kind="stable"):
        h[j] = 1+int(h[c[:, j]].max(initial=0))
    return int(h.max())


def heights_from_points(points):
    """Vectorized oracle for independent reference samples, sorted by time."""
    points = np.take_along_axis(points, np.argsort(points[..., 0], axis=1)[..., None], axis=1)
    batch, k, d = points.shape
    h = np.ones((batch, k), dtype=int)
    for j in range(1, k):
        delta = points[:, j:j+1, :]-points[:, :j, :]
        predecessors = delta[..., 0] > np.linalg.norm(delta[..., 1:], axis=-1)
        h[:, j] = 1+np.where(predecessors, h[:, :j], 0).max(axis=1)
    return h.max(axis=1) if k else np.zeros(batch, dtype=int)


def sample_heights(rng, d, k, count, compression=1.0):
    require(type(d) is int and d >= 2 and type(k) is int and k >= 0 and type(count) is int and count > 0, "invalid reference size")
    result = []
    for first in range(0, count, 64):
        points = sample_diamond(rng, (min(64, count-first), k), d)
        points[..., 1:] *= compression
        result.extend(heights_from_points(points).tolist())
    return np.asarray(result, dtype=int)


def rank_pvalue(observed_height, reference_heights):
    ref = np.asarray(reference_heights)
    require(ref.ndim == 1 and len(ref) > 0, "nonempty independent reference bank required")
    lower = (1+np.count_nonzero(ref <= observed_height))/(len(ref)+1)
    upper = (1+np.count_nonzero(ref >= observed_height))/(len(ref)+1)
    return min(1.0, 2*min(lower, upper))


def diagnose_at_stop(stream, inner_relation, *, rng, alpha=0.025, reference_count=255):
    require(stream.status in {"PRECISION_REACHED", "BUDGET_EXHAUSTED"}, "one diagnostic only after count-based stopping")
    require(not stream.diagnostic_used, "diagnostic already consumed; repeated looks require another error allocation")
    require(0 < alpha < 1 and type(reference_count) is int and reference_count > 0, "invalid diagnostic parameters")
    c = np.asarray(inner_relation)
    require(c.shape == (stream.k, stream.k), "inner-order cardinality differs from counted K")
    observed = height(c)
    stream.diagnostic_used = True
    if stream.k < 8 or stream.k > 512:
        return {"status": "DIAGNOSTIC_OUTSIDE_DECLARED_K_BUDGET", "K": stream.k, "height": observed,
                "curvature_identified": False, "scientific_time_qualification": "MODEL_ASSUMPTIONS_REQUIRED"}
    ref = sample_heights(rng, stream.context.dimension, stream.k, reference_count)
    p = rank_pvalue(observed, ref)
    warning = p <= alpha
    return {"status": "FLAT_MODEL_DEVIATION" if warning else "NO_DEVIATION_DETECTED",
            "K": stream.k, "height": observed, "reference_heights": ref.tolist(), "p_value": p,
            "alpha_chain": alpha, "curvature_identified": False,
            "scientific_time_qualification": "WITHHELD_MODEL_WARNING" if warning else "CONDITIONAL_ON_DECLARED_MODEL"}
