"""Deterministic evidence and calibration utilities; standard library only.

This experimental module does not actuate hardware and does not alter X6 app.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import math


def sha256_file(path: str | Path) -> str:
    """Actual content hash, not a random registry identifier."""
    h = sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json_bytes(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def evidence_record(*, input_path: str | Path, software_sha256: str,
                    parameters: dict, results: dict, uncertainty: dict,
                    source: str, simulation: bool = True) -> dict:
    """Produce a content-bound, deterministic record; no invented confidence."""
    if not source or len(software_sha256) != 64 or any(c not in "0123456789abcdef" for c in software_sha256):
        raise ValueError("Source and valid lowercase software SHA-256 required")
    record = {
        "schema": "x6-evidence-v0.1",
        "source": source,
        "input_sha256": sha256_file(input_path),
        "software_sha256": software_sha256,
        "parameters": parameters,
        "results": results,
        "uncertainty": uncertainty,
        "evidence_class": "SIMULATION" if simulation else "UNVERIFIED_MEASUREMENT",
        "status": "UNREVIEWED",
    }
    record["record_sha256"] = sha256(canonical_json_bytes(record)).hexdigest()
    return record


def verify_record(record: dict, input_path: str | Path) -> bool:
    original = dict(record)
    digest = original.pop("record_sha256", None)
    return (digest == sha256(canonical_json_bytes(original)).hexdigest()
            and original.get("input_sha256") == sha256_file(input_path))


def parameter_sweep(grid: dict[str, list], measure):
    """Lexicographically ordered Cartesian sweep; callback must be pure."""
    keys = sorted(grid)
    if not keys or any(not grid[k] for k in keys):
        raise ValueError("Nonempty parameter grid required")
    rows = []
    for values in product(*(grid[k] for k in keys)):
        params = dict(zip(keys, values))
        output = measure(dict(params))
        if not isinstance(output, dict):
            raise TypeError("Measurement must return a dict")
        rows.append({"parameters": params, "result": output})
    return rows


def summarize_replicates(values: list[float]) -> dict:
    """Sample SD and SE, no claim of independence or Gaussian coverage."""
    if not values or any(not math.isfinite(float(v)) for v in values):
        raise ValueError("Finite nonempty values required")
    n = len(values)
    mean = math.fsum(values) / n
    sd = math.sqrt(math.fsum((v - mean)**2 for v in values) / (n - 1)) if n > 1 else None
    return {"n": n, "mean": mean, "sample_sd": sd,
            "standard_error": sd / math.sqrt(n) if sd is not None else None,
            "note": "SE assumes independent replicates; n=1 has no SD"}
