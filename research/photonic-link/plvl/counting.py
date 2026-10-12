"""Sparse 16-mask fixed bins; no nearest-neighbour pairing or hidden IDs."""
import numpy as np
from .config import integer


def count_events(time_ps, channel, *, start_ps, stop_ps, window_ps):
    for name, val in (("start", start_ps), ("stop", stop_ps), ("width", window_ps)):
        integer(val, name, 0 if name == "start" else 1, 2**64-1)
    if stop_ps <= start_ps or (stop_ps-start_ps) % window_ps:
        raise ValueError("Invalid fixed-bin interval")
    ts, ch = np.asarray(time_ps), np.asarray(channel)
    if ts.ndim != 1 or ch.shape != ts.shape or ts.dtype.kind not in "ui" or ch.dtype.kind not in "ui":
        raise ValueError("One-dimensional integer timestamp/channel arrays required")
    if np.any(ts < start_ps) or np.any(ts >= stop_ps) or np.any(ch > 3) or np.any(ch < 0):
        raise ValueError("Out-of-range event; filtering must be explicit upstream")
    if len(ts) > 1 and np.any(ts[1:] < ts[:-1]):
        raise ValueError("Events must be ordered; silent repair prohibited")
    # Integer subtraction avoids any conversion of epochs to floating point.
    bins = (ts.astype(np.uint64)-np.uint64(start_ps))//np.uint64(window_ps)
    unique, first, multiplicity = np.unique(bins, return_index=True, return_counts=True)
    masks = np.bitwise_or.reduceat(np.left_shift(np.uint64(1), ch.astype(np.uint64)), first) if len(ts) else np.array([],np.uint64)
    totals = np.bincount(masks.astype(np.int64), minlength=16).astype(object)
    n = (stop_ps-start_ps)//window_ps
    totals[0] += n-len(unique)
    presence = np.array([sum(int(totals[m]) for m in range(16) if m & (1<<k)) for k in range(4)])
    clicks = np.bincount(ch.astype(np.int64), minlength=4)
    popcount = np.array([int(m).bit_count() for m in masks])
    repeats = int(np.sum(multiplicity > popcount))
    extra = int(clicks.sum()-presence.sum())
    multi = sum(int(totals[m]) for m in range(16) if (m&3)==3 or ((m>>2)&3)==3)
    counters = [int(v) for v in totals]+[n, repeats]+[int(v) for v in clicks]+[extra,multi]
    if any(c >= 2**64 for c in counters):
        raise ValueError("Counter overflow")
    return counters


def diagnostics(c):
    same, opposite = c[5]+c[10], c[6]+c[9]
    n = same+opposite
    return {"conditional_port_bins": n,
            "conditional_same_port_fraction": same/n if n else None,
            "conditional_correlation": (same-opposite)/n if n else None,
            "repeat_bins": c[17], "multiport_bins": c[23],
            "uncertainty": "NOT_ESTIMATED_NONIID_POSSIBLE",
            "interpretation": "Port occupancy diagnostic; not unique photon pairs, not a secret-key estimate"}
