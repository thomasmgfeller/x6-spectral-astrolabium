"""Fixed-sample paired-reference test for the 20 ppm input of Eigenzeit v0.10."""
import argparse
import hashlib
import json
from pathlib import Path


DESIGN_ID = "X6/v0.11/paired-reference/20ppm"
PAIRS = 3_300_000
MAX_DISCORDANT = 25
NODES = tuple(f"C{cell:02d}@{anchor}" for cell in range(1, 17) for anchor in ("1/4", "3/4"))
OUTCOMES = ("00", "01", "10", "11")
EVIDENCE = (
    "target_comparator_2ppm",
    "live_history_1ppm",
    "cell_response_lipschitz_8ppm",
    "common_gain_lipschitz_4ppm_range_0.99_1.01",
    "state_coverage_monitor_and_interlock",
    "tag_matching_all_trials_and_iid_pairs_at_each_node",
    "frozen_single_audit_and_fresh_v10_data",
)


def read_json(path):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError(f"duplicate JSON key {key}")
            obj[key] = value
        return obj
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)


def checked_path(root, ref):
    if not isinstance(ref, dict) or set(ref) != {"file", "sha256"}:
        return None
    if not isinstance(ref["file"], str) or not isinstance(ref["sha256"], str):
        return None
    relative = Path(ref["file"])
    path = (root / relative).resolve()
    if relative.is_absolute() or not path.is_relative_to(root) or not path.is_file():
        return None
    with path.open("rb") as stream:
        return path if hashlib.file_digest(stream, "sha256").hexdigest() == ref["sha256"] else None



def valid_evidence(root, ref, name, mode, scope):
    receipt = checked_path(root, ref)
    if receipt is None:
        return False
    try:
        data = read_json(receipt)
    except (OSError, ValueError):
        return False
    if not isinstance(data, dict) or data.get("mode") != mode or data.get("scope_id") != scope:
        return False
    claims = data.get("claims")
    return isinstance(claims, dict) and checked_path(root, claims.get(name)) is not None


def assess(record, root):
    result = {"status": "HOLD_INPUT", "geometry_release": False}
    if not isinstance(record, dict) or set(record) != {"design", "mode", "scope_id", "evidence", "nodes"}:
        return result
    mode = record["mode"]
    if record["design"] != DESIGN_ID or mode not in ("synthetic", "field"):
        return result
    if not isinstance(record["scope_id"], str) or not record["scope_id"].strip():
        return result
    result.update(mode=mode, scope_id=record["scope_id"])
    refs = record["evidence"]
    if not isinstance(refs, dict) or set(refs) != set(EVIDENCE):
        return result
    missing = [name for name in EVIDENCE if not valid_evidence(root.resolve(), refs[name], name, mode, record["scope_id"])]
    if missing:
        return {**result, "status": "HOLD_EVIDENCE", "unverified_attachments": missing}
    rows = record["nodes"]
    if not isinstance(rows, dict) or set(rows) != set(NODES):
        return result
    counts = {}
    for node in NODES:
        values = rows[node]
        if not isinstance(values, dict) or set(values) != set(OUTCOMES):
            return result
        if any(type(v) is not int or v < 0 for v in values.values()) or sum(values.values()) != PAIRS:
            return result
        counts[node] = values["01"] + values["10"]
    failures = [node for node in NODES if counts[node] > MAX_DISCORDANT]
    status = "HOLD_DISCORDANCE" if failures else ("SYNTHETIC_PASS" if mode == "synthetic" else "PASS_COUNTS_REVIEW_REQUIRED")
    return {**result, "status": status, "pairs": PAIRS * len(NODES),
            "maximum_discordant": max(counts.values()), "above_threshold": failures}


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("record", type=Path)
    args = cli.parse_args()
    try:
        decision = assess(read_json(args.record), args.record.resolve().parent)
    except (ValueError, OSError, RuntimeError):
        decision = {"status": "HOLD_INPUT", "geometry_release": False}
    print(json.dumps(decision, sort_keys=True, indent=2))
