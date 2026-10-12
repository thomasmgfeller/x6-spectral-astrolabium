"""Strict read-only ingestion of externally recorded optical frames.

The format does not claim instrument calibration or quantum-state tomography.
"""
import csv
import json
import math
from pathlib import Path
from .optical import frame_metrics, centroid_drift
from .core import sha256_file


def load_frame_csv(path):
    """Rectangular nonnegative finite intensity matrix; no silent missing values."""
    rows=[]
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.reader(handle):
            if not row:
                raise ValueError("empty CSV row")
            try:
                vals=[float(v) for v in row]
            except ValueError as exc:
                raise ValueError("non-numeric intensity") from exc
            if any(not math.isfinite(v) or v<0 for v in vals):
                raise ValueError("invalid intensity")
            rows.append(vals)
    if not rows or not rows[0] or any(len(row)!=len(rows[0]) for row in rows):
        raise ValueError("non-rectangular or empty frame")
    return rows


def compare_recorded_frames(reference_csv, sample_csv, metadata):
    """Measured pixels only; missing instrument metadata prevents qualification."""
    required=("instrument_id","pixel_pitch_um","acquired_utc","calibration_id")
    missing=[k for k in required if k not in metadata or metadata[k] in (None,"")]
    if missing:
        return {"status":"UNQUALIFIED_METADATA","missing":missing}
    pitch=metadata["pixel_pitch_um"]
    if not isinstance(pitch,(int,float)) or not math.isfinite(pitch) or pitch<=0:
        raise ValueError("invalid pixel pitch")
    a=load_frame_csv(reference_csv);b=load_frame_csv(sample_csv)
    if len(a)!=len(b) or len(a[0])!=len(b[0]):
        raise ValueError("frame dimensions differ")
    drift=centroid_drift(a,b)
    return {"schema":"x6-recorded-optics-v0.1",
            "status":"UNVERIFIED_MEASUREMENT" if drift["status"]=="OK" else drift["status"],
            "reference_sha256":sha256_file(reference_csv),
            "sample_sha256":sha256_file(sample_csv),
            "drift_pixels":drift["drift_pixels"],
            "drift_um":None if drift["drift_pixels"] is None else drift["drift_pixels"]*pitch,
            "reference_metrics":frame_metrics(a),
            "sample_metrics":frame_metrics(b),
            "metadata":dict(metadata),
            "caveat":"No calibration certificate, uncertainty budget, or physical validation supplied"}
