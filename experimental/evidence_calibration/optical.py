"""Intensity centroids and RMS widths, in input pixels; NOT physical drift proof."""
import math
from .validation import finite_number, MAX_PIXELS


def frame_metrics(frame, threshold=0):
    threshold = finite_number(threshold, "threshold", minimum=0)
    if type(frame) not in (list, tuple) or not frame or type(frame[0]) not in (list, tuple) or not frame[0]:
        raise ValueError("nonempty 2D list/tuple required")
    width = len(frame[0])
    if width * len(frame) > MAX_PIXELS:
        raise ValueError("frame exceeds pixel limit")
    if any(type(row) not in (list, tuple) or len(row) != width for row in frame):
        raise ValueError("ragged frame")
    points = []
    for y, row in enumerate(frame):
        for x, value in enumerate(row):
            value = finite_number(value, "intensity", minimum=0)
            if value > threshold:
                points.append((x, y, value))
    if not points:
        return {"status": "NO_SIGNAL", "total": 0, "centroid_x": None,
                "centroid_y": None, "sigma_x": None, "sigma_y": None}
    # Scale BEFORE weighted multiplication to prevent x*intensity overflow.
    scale = max(v for _, _, v in points)
    weights = [(x, y, v / scale) for x, y, v in points]
    norm = math.fsum(v for _, _, v in weights)
    total = scale * norm
    if not math.isfinite(total):
        raise ValueError("total intensity exceeds finite result range")
    cx = math.fsum(x * (v / norm) for x, _, v in weights)
    cy = math.fsum(y * (v / norm) for _, y, v in weights)
    sx = math.sqrt(math.fsum((x - cx)**2 * (v / norm) for x, _, v in weights))
    sy = math.sqrt(math.fsum((y - cy)**2 * (v / norm) for _, y, v in weights))
    if not all(math.isfinite(v) for v in (cx, cy, sx, sy)):
        raise ValueError("nonfinite optical result")
    return {"status": "OK", "total": total, "centroid_x": cx,
            "centroid_y": cy, "sigma_x": sx, "sigma_y": sy}


def centroid_drift(reference, current):
    a, b = frame_metrics(reference), frame_metrics(current)
    if len(reference) != len(current) or len(reference[0]) != len(current[0]):
        raise ValueError("frame dimensions differ")
    if a["status"] != "OK" or b["status"] != "OK":
        return {"status": "INSUFFICIENT_SIGNAL", "drift_pixels": None}
    return {"status": "OK", "drift_pixels": math.hypot(
        b["centroid_x"] - a["centroid_x"], b["centroid_y"] - a["centroid_y"])}
