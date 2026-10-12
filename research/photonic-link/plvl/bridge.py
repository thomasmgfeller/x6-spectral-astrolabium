"""Synthetic SGNCv007 export, compatible with inherited snapshot validation."""
import struct
import zlib
from .config import integer


def encode_snapshot(report, *, setting_index=0, calibration_id=1, sequence=0):
    """Setting index is an external label; it does not certify CHSH angles."""
    if report.get("origin") != "synthetic":
        raise ValueError("Only synthetic reports may be exported by this adapter")
    integer(setting_index,"setting_index",0,3)
    integer(calibration_id,"calibration_id",0,2**32-1)
    integer(sequence,"sequence",0,2**64-1)
    cfg = report["config"]
    counters = report["calibrated"]["counters"]
    if len(counters) != 24:
        raise ValueError("Exactly 24 counters required")
    for c in counters:
        integer(c,"counter",0,2**64-1)
    n = cfg["duration_ps"]//cfg["window_ps"]
    if counters[16] != n or sum(counters[:16]) != n:
        raise ValueError("Broken trial accounting")
    header = struct.pack("<8sBBBBIQQQQ", b"SGNCv007",7,setting_index,0,0,
                         calibration_id,0,cfg["duration_ps"],cfg["window_ps"],sequence)
    payload = header+struct.pack("<24Q",*counters)
    return payload+struct.pack("<I",zlib.crc32(payload))
