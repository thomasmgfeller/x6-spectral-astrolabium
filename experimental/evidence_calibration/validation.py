"""Strict JSON/numeric contracts for the isolated research prototype."""
import json
import math
from pathlib import Path

MAX_BYTES = 16 * 1024 * 1024
MAX_PIXELS = 1_000_000


def finite_number(value, name, *, minimum=None, positive=False):
    if type(value) not in (int, float):
        raise ValueError(name + " must be a real number, not bool or text")
    try:
        number = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(name + " is outside finite float range") from exc
    if not math.isfinite(number) or (minimum is not None and number < minimum) or (positive and number <= 0):
        raise ValueError(name + " is outside its finite range")
    return number


def nonempty_text(value, name):
    if type(value) is not str or not value.strip():
        raise ValueError(name + " must be nonempty text")
    return value


def json_snapshot(value):
    """Independent JSON snapshot; no custom coercions, non-string keys or NaN."""
    def check(x, depth=0):
        if depth > 32:
            raise ValueError("JSON nesting exceeds 32")
        if x is None or type(x) in (str, bool, int):
            return
        if type(x) is float and math.isfinite(x):
            return
        if type(x) is list:
            for item in x:
                check(item, depth + 1)
            return
        if type(x) is dict and all(type(k) is str for k in x):
            for item in x.values():
                check(item, depth + 1)
            return
        raise ValueError("Only finite JSON values with string keys are allowed")
    check(value)
    try:
        text = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
        if len(text.encode("utf-8")) > MAX_BYTES:
            raise ValueError("JSON snapshot exceeds size limit")
        return json.loads(text)
    except (TypeError, OverflowError, UnicodeError) as exc:
        raise ValueError("Invalid JSON snapshot") from exc


def read_snapshot(path):
    """Read once, bounded. Hash AND parser must consume these exact bytes.

    This binds provenance but cannot make a concurrently written file atomic.
    Producers must publish complete files using atomic replacement.
    """
    with Path(path).open("rb") as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("Input exceeds 16 MiB snapshot limit")
    return data
