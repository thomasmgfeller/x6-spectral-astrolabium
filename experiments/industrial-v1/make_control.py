"""Materialize a tiny software-control bundle, never a physical experiment.

Two independent synthetic labels cannot establish a 1% false-alarm bound.
Expected end-to-end result: INCONCLUSIVE, claim_supported=false.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parent


def write_json(path, value):
    raw = (json.dumps(value, indent=2, allow_nan=False)+"\n").encode()
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def make(root):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    def write(name, raw):
        (root/name).write_bytes(raw)
        return {"path": name, "sha256": hashlib.sha256(raw).hexdigest()}
    note = write("CONTROL_ONLY.txt", b"Synthetic software fixture. No sensor, real machine, independent sample population or measured performance.\n")
    profile = json.loads((ROOT/"V1_PROFILE_DRAFT.json").read_text())
    profile.update(profile_id="V1-SOFTWARE-CONTROL-ONLY", status="FROZEN", frozen_utc="2026-10-14T00:00:00Z", evidence_class="SYNTHETIC_CONTROL")
    profile["processing"].update(candidate_id="CONTROL_SCORES", baseline_id="CONTROL_BASELINE", candidate_threshold=0.5, baseline_threshold=0.5)
    profile["statistics"].update(min_positive_units=1, min_negative_units=1)
    profile["references"] = {role: copy.deepcopy(note) for role in profile["references"]}
    pulse = [0.0]*1024
    pulse[256] = 1.0
    pulse_ref = write("pulse.f32", struct.pack("<1024f", *pulse))
    profile["preservation_cases"] = [{"id": "impulse", "reference_amplitude": 1,
        "reference_sample": 256, "reference_kind": "SYNTHETIC_FLOAT32", "sample_count": 1024,
        "peak_window": [128, 384], "reference": pulse_ref}]
    ph = write_json(root/"profile.json", profile)
    units = []
    for i, label in enumerate(("healthy", "damaged")):
        # Distinct deterministic finite Float32 arrays; no claim these model bearings.
        raw = struct.pack("<f", float(i+1)) + bytes((256000*4-1)*4)
        ref = write(f"control_{i}.f32", raw)
        units.append({"record_id": str(i), "bearing_id": f"synthetic-{i}", "split": "holdout", "label": label, "samples": ref})
    inputs = {"schema": "x6.industrial.v1.inputs/1", "profile_sha256": ph,
              "evidence_class": "SYNTHETIC_CONTROL", "units": units}
    ih = write_json(root/"inputs.json", inputs)
    result = {"schema": "x6.industrial.v1.result/1", "run_id": "SOFTWARE-CONTROL-ONLY",
              "started_utc": "2026-10-14T00:00:01Z", "evidence_class": "SYNTHETIC_CONTROL",
              "profile_sha256": ph, "input_manifest_sha256": ih,
              "candidate_source_sha256": note["sha256"], "baseline_source_sha256": note["sha256"],
              "environment": {"hardware": "SIMULATED_FIXTURE", "os": "NOT_MEASURED", "runtime": "NOT_MEASURED", "precision": "float32", "measurement_report": note},
              "decisions": [{"record_id": "0", "candidate_score": 0, "baseline_score": 0}, {"record_id": "1", "candidate_score": 1, "baseline_score": 0}],
              "preservation": [{"id": "impulse", "output": pulse_ref}],
              "resources": {"service_ms": [1.0]*6000, "latency_ms": [11.0]*6000,
                            "additional_state_peak_bytes": 4096, "dropped_blocks": 0, "peak_backlog_blocks": 0, "final_backlog_blocks": 0}}
    write_json(root/"result.json", result)
    return profile, inputs, result, ph, ih


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    make(args.output)
    print("Created SYNTHETIC_CONTROL bundle; expected INCONCLUSIVE, no physical claim.")
