"""Typed scientific screening, NOT statistical or hardware safety approval."""
import math
from .validation import finite_number


def evaluate_boundary(*, sample_count, minimum_samples, baseline, candidate,
                      tolerance, calibration_valid, data_integrity):
    if any(type(v) is not int or v < 0 for v in (sample_count, minimum_samples)) or minimum_samples < 1:
        raise ValueError("invalid sample count")
    if type(calibration_valid) is not bool or type(data_integrity) is not bool:
        raise ValueError("calibration_valid and data_integrity must be bool")
    baseline = finite_number(baseline, "baseline")
    candidate = finite_number(candidate, "candidate")
    tolerance = finite_number(tolerance, "tolerance", minimum=0)
    delta = candidate - baseline
    if not math.isfinite(delta):
        raise ValueError("metric difference overflows")
    reasons = []
    if sample_count < minimum_samples:
        reasons.append("INSUFFICIENT_SAMPLES")
    if not calibration_valid:
        reasons.append("CALIBRATION_UNVERIFIED")
    if not data_integrity:
        reasons.append("DATA_INTEGRITY_FAILED")
    if delta > tolerance:
        reasons.append("BASELINE_NOT_MET")
    return {"status": "REJECT" if reasons else "PASS", "reasons": reasons,
            "metric_delta": delta, "metric_direction": "lower_is_better",
            "interpretation": "Typed software screening only. Caller flags are not authenticated; no statistical significance or physical safety approval."}
