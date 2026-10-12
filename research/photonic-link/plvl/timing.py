"""Relative epochs only. Clock calibration does not measure optical phase."""
from dataclasses import dataclass
import numpy as np


def stamp(physical_s, clock, rng, jitter_sigma_s):
    physical_s = np.asarray(physical_s, float)
    if not np.isfinite(physical_s).all() or np.max(np.abs(physical_s), initial=0) > 20:
        raise ValueError("Only short relative epochs (<=20 s) supported")
    noisy = physical_s+rng.normal(0, jitter_sigma_s, physical_s.shape)
    local = clock.offset_s+(1+clock.skew_ppm*1e-6)*noisy + .5*clock.drift_ppm_per_s*1e-6*noisy**2
    # Round-to-nearest/ties-to-even. tick is an assumed quantizer step, not TDC accuracy.
    return np.rint(local/(clock.tick_ps*1e-12))*(clock.tick_ps*1e-12)


@dataclass(frozen=True)
class AffineCalibration:
    reference_center_s: float
    local_center_s: float
    scale: float
    training_min_s: float
    training_max_s: float

    def correct(self, local_s):
        a = np.asarray(local_s, float)
        if not np.isfinite(a).all():
            raise ValueError("Finite local timestamps required")
        return self.reference_center_s+(a-self.local_center_s)/self.scale


def fit_affine(reference_s, local_s):
    """OLS of local versus a known accurate reference; no event-pair truth input."""
    x, y = np.asarray(reference_s, float), np.asarray(local_s, float)
    if x.ndim != 1 or y.shape != x.shape or len(x) < 3:
        raise ValueError("At least three paired calibration anchors required")
    if not np.isfinite(x).all() or not np.isfinite(y).all() or np.any(np.diff(x) <= 0):
        raise ValueError("Finite, strictly ordered calibration references required")
    x0, y0 = float(x.mean()), float(y.mean())
    xx, yy = x-x0, y-y0
    scale = float(xx@yy/(xx@xx))
    if not .99 < scale < 1.01:
        raise ValueError("Calibration slope outside declared short-link clock model")
    return AffineCalibration(x0, y0, scale, float(x[0]), float(x[-1]))


def residual_summary(calibration, reference_s, local_s):
    x = np.asarray(reference_s, float)
    y = np.asarray(local_s, float)
    if x.ndim != 1 or y.shape != x.shape or not len(x) or not np.isfinite(x).all():
        raise ValueError("Finite, nonempty holdout required")
    if x.min() < calibration.training_min_s or x.max() > calibration.training_max_s:
        raise ValueError("Holdout extrapolates outside calibration interval")
    r = calibration.correct(y)-x
    return {"n": len(r), "mean_s": float(r.mean()),
            "rms_s": float(np.sqrt(np.mean(r*r))),
            "max_abs_s": float(np.max(np.abs(r)))}
