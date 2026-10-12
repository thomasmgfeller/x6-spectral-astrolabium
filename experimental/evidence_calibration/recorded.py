"""Read-only optical CSV snapshots. v0.2 requires explicit measurement semantics."""
import csv
import io
import math
import re
from datetime import datetime
from hashlib import sha256
from .optical import frame_metrics, centroid_drift
from .validation import finite_number, nonempty_text, json_snapshot, read_snapshot, MAX_BYTES, MAX_PIXELS


def parse_frame_bytes(data):
    """Hash caller's same byte snapshot; never reopen the original path."""
    if type(data) is not bytes or len(data) > MAX_BYTES:
        raise ValueError("bounded bytes required")
    try:
        text = data.decode("utf-8-sig")
    except UnicodeError as exc:
        raise ValueError("CSV must be UTF-8") from exc
    rows = []
    cells = 0
    try:
        for row in csv.reader(io.StringIO(text, newline=""), strict=True):
            if not row:
                raise ValueError("empty CSV row")
            values = [finite_number(float(v), "intensity", minimum=0) for v in row]
            cells += len(values)
            if cells > MAX_PIXELS or (rows and len(values) != len(rows[0])):
                raise ValueError("oversized or nonrectangular frame")
            rows.append(values)
    except (csv.Error, OverflowError) as exc:
        raise ValueError("invalid CSV") from exc
    if not rows or not rows[0]:
        raise ValueError("empty frame")
    return rows


def load_frame_csv(path):
    return parse_frame_bytes(read_snapshot(path))


def _metadata(metadata):
    if type(metadata) is not dict:
        raise ValueError("metadata must be an object")
    meta = json_snapshot(metadata)
    required = ("instrument_id", "pixel_pitch_um", "acquired_utc", "calibration_id",
                "evidence_class", "coordinate_plane", "scale_model")
    missing = [k for k in required if k not in meta]
    if missing:
        return None, missing
    for key in ("instrument_id", "calibration_id", "coordinate_plane"):
        nonempty_text(meta[key], key)
    pitch = finite_number(meta["pixel_pitch_um"], "pixel pitch", positive=True)
    stamp = nonempty_text(meta["acquired_utc"], "acquired_utc")
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|\+00:00)", stamp):
        raise ValueError("acquired_utc requires explicit UTC timestamp")
    datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    if meta["evidence_class"] not in ("SYNTHETIC", "RECORDED_UNVERIFIED"):
        raise ValueError("evidence_class must be explicit; never infer measurement")
    if meta["scale_model"] != "effective_isotropic_um_per_input_pixel":
        raise ValueError("effective input-image scale must include binning/resizing/magnification")
    meta["pixel_pitch_um"] = pitch
    return meta, []


def compare_recorded_frames(reference_csv, sample_csv, metadata):
    meta, missing = _metadata(metadata)
    if missing:
        return {"status": "UNQUALIFIED_METADATA", "missing": missing}
    # One read per path; calculation and provenance share exactly the same bytes.
    reference_bytes = read_snapshot(reference_csv)
    sample_bytes = read_snapshot(sample_csv)
    a, b = parse_frame_bytes(reference_bytes), parse_frame_bytes(sample_bytes)
    drift = centroid_drift(a, b)
    micrometers = None if drift["drift_pixels"] is None else drift["drift_pixels"] * meta["pixel_pitch_um"]
    if micrometers is not None and not math.isfinite(micrometers):
        raise ValueError("scaled displacement overflows")
    status = ("SYNTHETIC_RESULT" if meta["evidence_class"] == "SYNTHETIC" else "UNVERIFIED_MEASUREMENT")
    return {"schema": "x6-recorded-optics-v0.2",
            "status": status if drift["status"] == "OK" else drift["status"],
            "evidence_class": meta["evidence_class"],
            "reference_sha256": sha256(reference_bytes).hexdigest(),
            "sample_sha256": sha256(sample_bytes).hexdigest(),
            "drift_pixels": drift["drift_pixels"], "drift_um": micrometers,
            "coordinate_plane": meta["coordinate_plane"],
            "calibration_status": "UNVERIFIED", "measurement_uncertainty": "NOT_EVALUATED",
            "reference_metrics": frame_metrics(a), "sample_metrics": frame_metrics(b),
            "metadata": meta,
            "caveat": "Intensity centroid displacement only; background, saturation and crop can mimic motion. Metadata declarations are not calibration evidence."}
