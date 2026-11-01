"""Lossless negative-only screening of a prefix of the same fixed audit."""
import argparse
import json
from pathlib import Path
from audit import DESIGN_ID, MAX_DISCORDANT, NODES, OUTCOMES, PAIRS, read_json


def screen(prefix):
    invalid = {"status": "HOLD_INPUT", "geometry_release": False}
    if not isinstance(prefix, dict) or set(prefix) != {"design","mode","scope_id","node","counts"}:
        return invalid
    if prefix["design"] != DESIGN_ID or prefix["mode"] not in ("synthetic","field") or prefix["node"] not in NODES:
        return invalid
    if not isinstance(prefix["scope_id"], str) or not prefix["scope_id"].strip():
        return invalid
    c = prefix["counts"]
    if not isinstance(c, dict) or set(c) != set(OUTCOMES) or any(type(v) is not int or v < 0 for v in c.values()):
        return invalid
    if not 0 < sum(c.values()) <= PAIRS:
        return invalid
    mismatch = c["01"]+c["10"]
    return {"status": "STOP_DISCORDANCE" if mismatch > MAX_DISCORDANT else "NO_EARLY_STOP",
            "scope_id": prefix["scope_id"], "mode": prefix["mode"], "node": prefix["node"],
            "opportunities": sum(c.values()), "discordant": mismatch, "geometry_release": False}


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("prefix",type=Path)
    path=cli.parse_args().prefix
    try:
        out=screen(read_json(path))
    except (OSError, ValueError):
        out={"status":"HOLD_INPUT","geometry_release":False}
    print(json.dumps(out,sort_keys=True,indent=2))
