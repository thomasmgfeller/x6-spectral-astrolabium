"""Fail-closed scientific acceptance checks; never hardware safety authorization."""
import math

def evaluate_boundary(*,sample_count,minimum_samples,baseline,candidate,tolerance,calibration_valid,data_integrity):
    if any(type(v) is not int or v<0 for v in (sample_count,minimum_samples)) or minimum_samples<1:
        raise ValueError("invalid sample count")
    if any(not isinstance(v,(int,float)) or not math.isfinite(v) for v in (baseline,candidate,tolerance)) or tolerance<0:
        raise ValueError("invalid metric")
    reasons=[]
    if sample_count<minimum_samples: reasons.append("INSUFFICIENT_SAMPLES")
    if not calibration_valid: reasons.append("CALIBRATION_UNVERIFIED")
    if not data_integrity: reasons.append("DATA_INTEGRITY_FAILED")
    if candidate>baseline+tolerance: reasons.append("BASELINE_NOT_MET")
    return {"status":"REJECT" if reasons else "PASS","reasons":reasons,"metric_delta":candidate-baseline,
            "interpretation":"Software-only scientific gate; not physical safety approval"}
