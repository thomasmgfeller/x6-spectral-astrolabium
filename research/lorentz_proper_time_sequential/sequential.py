"""Howard stitched empirical-Bernstein CS with immutable sampling context.

The mathematical guarantee is conditional on the declared sampling assumptions;
metadata checks cannot establish that physical observations satisfy them.
"""
from dataclasses import dataclass
import math
import numpy as np
from scipy.special import zeta


def require(condition, message):
    if not condition:
        raise ValueError(message)


def stitched_bound(v, alpha_one, eta=2.0, s=1.4, v_min=1.0, c=1.0):
    """Equation (8), l0=1, h(k)=zeta(s)*(1+k)^s; NOT rounded equation (24)."""
    require(0 < alpha_one < 1 and eta > 1 and s > 1 and v_min > 0 and c >= 0, "invalid bound parameters")
    v = np.asarray(v, dtype=float)
    require(bool(np.all(np.isfinite(v) & (v >= 0))), "finite nonnegative intrinsic variance required")
    w = np.maximum(v, v_min)
    ell = math.log(float(zeta(s, 1.0))/alpha_one) + s*np.log1p(np.log(w/v_min)/math.log(eta))
    k1 = (eta**0.25 + eta**-0.25)/math.sqrt(2)
    k2 = (math.sqrt(eta)+1)/2
    bound = np.sqrt(k1*k1*w*ell + k2*k2*c*c*ell*ell) + k2*c*ell
    # Small outward guard; this is ordinary float64, not certified interval arithmetic.
    return np.nextafter(bound*(1+1e-12)+1e-12, np.inf)


def probability_interval(k, n, variance, alpha=0.025):
    require(type(n) is int and n > 0, "positive integer n required")
    k = np.asarray(k)
    require(bool(np.all((k >= 0) & (k <= n))), "count outside [0,n]")
    radius = stitched_bound(variance, alpha/2)/n
    return np.maximum(0.0, k/n-radius), np.minimum(1.0, k/n+radius)


def estimate_interval(lower, upper, d, scale):
    low = np.asarray(lower)**(1/d)*scale
    high = np.asarray(upper)**(1/d)*scale
    total = low+high
    estimate = np.divide(2*low*high, total, out=np.zeros_like(total), where=total > 0)
    relative = np.divide(high-low, total, out=np.ones_like(total), where=total > 0)
    return low, high, estimate, relative


@dataclass(frozen=True)
class Context:
    domain_id: str
    marked_pair_id: str
    dimension: int
    reference_time: float
    batch_size: int
    max_n: int
    alpha: float = 0.025
    relative_tolerance: float = 0.1
    sampling_law: str = "iid_uniform_fixed_diamond"

    def __post_init__(self):
        require(bool(self.domain_id) and bool(self.marked_pair_id), "named fixed domain and marks required")
        require(type(self.dimension) is int and self.dimension >= 2, "known d>=2 required")
        require(math.isfinite(self.reference_time) and self.reference_time > 0, "known positive reference time required")
        require(type(self.batch_size) is int and type(self.max_n) is int and 0 < self.batch_size <= self.max_n and self.max_n % self.batch_size == 0, "fixed positive batch and divisible budget required")
        require(0 < self.alpha < 1 and 0 < self.relative_tolerance < 1, "invalid error budget")
        require(self.sampling_law == "iid_uniform_fixed_diamond", "unsupported sampling law")


class SequentialTime:
    def __init__(self, context):
        self.context = context
        self.n = self.k = 0
        self.variance = 0.0
        self.lower, self.upper = 0.0, 1.0
        self.status = "SAMPLING"
        self.diagnostic_used = False

    def append_counts(self, successes, *, start_index, context):
        require(context == self.context, "changed domain, marks, scale or sampling contract; start a separately budgeted experiment")
        require(self.status == "SAMPLING", "stream is already stopped")
        require(type(start_index) is int and start_index == self.n, "duplicate or out-of-order batch")
        b = self.context.batch_size
        require(type(successes) is int and 0 <= successes <= b, "integer batch success count required")
        pred = self.k/self.n if self.n else 0.0
        self.variance += successes*(1-pred)**2+(b-successes)*pred**2
        self.k += successes
        self.n += b
        lo, hi = probability_interval(self.k, self.n, self.variance, self.context.alpha)
        self.lower, self.upper = max(self.lower, float(lo)), min(self.upper, float(hi))
        if self.lower > self.upper:
            self.status = "EMPTY_CONFIDENCE_SEQUENCE"
        else:
            low, high, estimate, relative = estimate_interval(self.lower, self.upper, self.context.dimension, self.context.reference_time)
            if low > 0 and relative < self.context.relative_tolerance:
                self.status = "PRECISION_REACHED"
            elif self.n == self.context.max_n:
                self.status = "BUDGET_EXHAUSTED"
        return self.snapshot()

    def snapshot(self):
        result = {"n": self.n, "K": self.k, "prediction_error_sum": self.variance,
                  "probability_interval": [self.lower, self.upper], "status": self.status,
                  "alpha_time": self.context.alpha}
        if self.lower <= self.upper:
            lo, hi, est, rel = estimate_interval(self.lower, self.upper, self.context.dimension, self.context.reference_time)
            result.update(time_interval=[float(lo), float(hi)], certified_point_estimate=float(est),
                          relative_radius=float(rel), raw_volume_estimate=self.context.reference_time*(self.k/self.n)**(1/self.context.dimension) if self.n else None)
        return result
