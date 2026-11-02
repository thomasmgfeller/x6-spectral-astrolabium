"""Check the independently rebuilt product before it can replace the public data."""
import csv
import gzip
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path


def check(path):
    ref = json.loads(Path(__file__).with_name("reference.json").read_bytes())
    run = json.loads((path/"summary.json").read_bytes())
    for k in ("schema", "release_sha256", "engine_sha256", "protocol_sha256", "tempo_lock_sha256",
              "source", "checks", "decision", "calibration_rank", "numpy"):
        if run[k] != ref[k]:
            raise ValueError("Replay differs: " + k)
    def close(x, y):
        if not math.isclose(x, y, rel_tol=0.0001, abs_tol=0.00001):
            raise ValueError(f"Replay coordinate differs: {x} versus {y}")
    for arm, r in run["arms"].items():
        for key in ("false_alarm", "detection"):
            if r[key]["hits"] != ref["arms"][arm][key]["hits"] or r[key]["n"] != ref["arms"][arm][key]["n"]:
                raise ValueError("Decision counts differ")
        for key in ("threshold_us2", "power_fraction", "angular_cosine", "expected_hd_power_projection", "expected_angular_cosine"):
            close(r[key], ref["arms"][arm][key])
    for a,b in zip(run["pairs"], ref["pairs"], strict=True):
        if (a["p"],a["q"]) != (b["p"],b["q"]):
            raise ValueError("Sky pairs differ")
        for key in ("angle_deg","hd","identity","cspp","expected_identity","expected_cspp"):
            close(a[key], b[key])
    f = path/run["timing_csv"]["name"]
    if hashlib.sha256(f.read_bytes()).hexdigest() != run["timing_csv"]["sha256"]:
        raise ValueError("Damaged residual file")
    with gzip.open(f, "rt") as stream:
        counts = Counter(row["pulsar"] for row in csv.DictReader(stream))
    for a,b in zip(run["pulsars"], ref["pulsars"], strict=True):
        if a["name"] != b["name"] or counts[a["name"]] != a["toas"] or a["toas"] != b["toas"]:
            raise ValueError("Observation counts differ")
        close(a["wrms_us"], b["wrms_us"])
    print("Replay verified:", run["decision"], sum(counts.values()), "TOAs")


if __name__ == "__main__":
    check(Path(sys.argv[1]))
