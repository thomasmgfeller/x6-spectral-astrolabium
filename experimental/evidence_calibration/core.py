"""Deterministic evidence and calibration utilities; standard library only.

This experimental module does not actuate hardware and does not alter X6 app.
"""
from __future__ import annotations

from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import math
from .validation import finite_number, nonempty_text, json_snapshot, read_snapshot


def sha256_file(path: str | Path) -> str:
    """Actual content hash, not a random registry identifier."""
    h = sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json_bytes(obj: object) -> bytes:
    return json.dumps(json_snapshot(obj), sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def evidence_record(*, input_path: str | Path, software_sha256: str,
                    parameters: dict, results: dict, uncertainty: dict,
                    source: str, simulation: bool = True) -> dict:
    """Produce a content-bound, deterministic record; no invented confidence."""
    nonempty_text(source, "source")
    if type(simulation) is not bool:
        raise ValueError("simulation must be bool")
    if not valid_digest(software_sha256):
        raise ValueError("valid lowercase software SHA-256 required")
    for value in (parameters, results, uncertainty):
        if type(value) is not dict:
            raise ValueError("parameters, results and uncertainty must be objects")
    parameters, results, uncertainty = json_snapshot([parameters, results, uncertainty])
    record = {
        "schema": "x6-evidence-v0.1",
        "source": source,
        "input_sha256": sha256(read_snapshot(input_path)).hexdigest(),
        "software_sha256": software_sha256,
        "parameters": parameters,
        "results": results,
        "uncertainty": uncertainty,
        "evidence_class": "SIMULATION" if simulation else "UNVERIFIED_MEASUREMENT",
        "status": "UNREVIEWED",
    }
    record["record_sha256"] = sha256(canonical_json_bytes(record)).hexdigest()
    return record


def valid_digest(value):
    return type(value) is str and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def verify_record(record: dict, input_path: str | Path) -> bool:
    """Schema + content consistency only; NOT authenticity or computational replay."""
    fields = {"schema", "source", "input_sha256", "software_sha256", "parameters",
              "results", "uncertainty", "evidence_class", "status", "record_sha256"}
    try:
        if type(record) is not dict or set(record) != fields:
            return False
        original = json_snapshot(record)
        if original["schema"] != "x6-evidence-v0.1" or original["status"] != "UNREVIEWED":
            return False
        nonempty_text(original["source"], "source")
        if original["evidence_class"] not in ("SIMULATION", "UNVERIFIED_MEASUREMENT"):
            return False
        if any(type(original[k]) is not dict for k in ("parameters", "results", "uncertainty")):
            return False
        if not all(valid_digest(original[k]) for k in ("record_sha256", "software_sha256", "input_sha256")):
            return False
        digest = original.pop("record_sha256")
        return (digest == sha256(canonical_json_bytes(original)).hexdigest()
                and original["input_sha256"] == sha256(read_snapshot(input_path)).hexdigest())
    except (OSError, ValueError, TypeError, OverflowError, RecursionError):
        return False


def parameter_sweep(grid: dict[str, list], measure):
    """Lexicographically ordered Cartesian sweep; callback must be pure."""
    if type(grid) is not dict or any(type(k) is not str or type(v) is not list for k, v in grid.items()):
        raise ValueError("grid must map string keys to lists")
    grid = json_snapshot(grid)
    keys = sorted(grid)
    if not keys or any(not grid[k] for k in keys):
        raise ValueError("Nonempty parameter grid required")
    if math.prod(len(grid[k]) for k in keys) > 10000:
        raise ValueError("sweep exceeds 10000 cases")
    rows = []
    for values in product(*(grid[k] for k in keys)):
        params = dict(zip(keys, values))
        output = measure(json_snapshot(params))
        if not isinstance(output, dict):
            raise TypeError("Measurement must return a dict")
        rows.append({"parameters": params, "result": json_snapshot(output)})
    return rows


def summarize_replicates(values: list[float]) -> dict:
    """Sample SD and SE, no claim of independence or Gaussian coverage."""
    if type(values) not in (list, tuple) or not values:
        raise ValueError("finite nonempty list/tuple required")
    values = [finite_number(v, "replicate") for v in values]
    n = len(values)
    scale = max(abs(v) for v in values)
    normalized = [v / scale for v in values] if scale else [0.0] * n
    center = math.fsum(normalized) / n
    mean = scale * center
    sd = (scale * math.sqrt(math.fsum((v - center)**2 for v in normalized) / (n - 1))
          if n > 1 else None)
    if not math.isfinite(mean) or (sd is not None and not math.isfinite(sd)):
        raise ValueError("statistic exceeds finite result range")
    return {"n": n, "mean": mean, "sample_sd": sd,
            "standard_error": sd / math.sqrt(n) if sd is not None else None,
            "note": "SE assumes independent replicates; n=1 has no SD; not a complete measurement uncertainty budget"}
