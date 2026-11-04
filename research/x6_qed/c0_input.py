"""C0 development input boundary. The caller binds inference to a validated graph."""

import re
from collections.abc import Callable
from typing import TypeVar

Result = TypeVar("Result")
SHOT_SCHEMA = "x6.qed.detector-shot/1"


class ShotInputError(ValueError):
    """Invalid input envelope, excluded from all decoder shot statistics."""


def decode_shot(
    shot: object,
    *,
    graph_sha256: str,
    detector_count: int,
    infer: Callable[[tuple[int, ...]], Result],
) -> Result:
    """Forward only validated detector bits, in graph order, to the bound inference."""
    if not isinstance(graph_sha256, str) or not re.fullmatch("[0-9a-f]{64}", graph_sha256):
        raise ValueError("Invalid trusted graph SHA-256")
    if type(detector_count) is not int or detector_count <= 0:
        raise ValueError("Invalid trusted detector count")

    if not isinstance(shot, dict) or shot.get("schema") != SHOT_SCHEMA:
        raise ShotInputError("Unsupported shot schema")
    if set(shot) != {"schema", "frozen_graph_sha256", "detector_bits"}:
        raise ShotInputError("Unexpected or missing shot fields")
    if shot["frozen_graph_sha256"] != graph_sha256:
        raise ShotInputError("FrozenGraph identity mismatch")
    bits = shot["detector_bits"]
    if not isinstance(bits, list) or len(bits) != detector_count:
        raise ShotInputError("Incorrect detector vector length or type")
    if any(type(bit) is not int or bit not in (0, 1) for bit in bits):
        raise ShotInputError("Detector bits must be binary JSON integers")
    return infer(tuple(bits))
