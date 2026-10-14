"""Closed JSON Schema for the prototype's simulation job/result messages."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
def obj(properties):
    return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)
ID = {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:-]{0,95}$"}
SHA = {"type": "string", "pattern": "^[a-f0-9]{64}$"}
UINT = {"type": "integer", "minimum": 0, "maximum": 4294967295}
BINDING = {"campaign_sha256": SHA, "job_id": ID, "batch_revision": UINT,
           "attempt": {"type": "integer", "minimum": 1}, "node_id": ID,
           "specimen_id": ID, "experiment_id": ID, "replicate_id": ID}
def build():
    job = obj({"schema": {"const": "x6.fabric.job/0.1.0"}, **BINDING,
               "deadline_epoch_ms": {"type": "integer", "minimum": 0},
               "execution_mode": {"const": "SIMULATION_ONLY"}, "seed": UINT})
    raw = obj({"replicate_id": ID, "experiment_id": ID, "seed": UINT,
               "measured_accelerance": {"type": "number"}, "unit": {"const": "(m/s^2)/N"},
               "threshold": {"type": "number"}, "outcome": {"enum": [0, 1]}})
    result = obj({"schema": {"const": "x6.fabric.result/0.1.0"}, **BINDING,
                  "observation_id": ID, "evidence_kind": {"const": "SYNTHETIC_CONTROL"},
                  "quality": {"const": "PASS"}, "outcome": {"enum": [0, 1]},
                  "raw": raw, "raw_sha256": SHA})
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "urn:x6:fabric:messages:0.1.0",
            "title": "X6 experimental fabric simulation messages", "$defs": {"job": job, "result": result},
            "oneOf": [{"$ref": "#/$defs/job"}, {"$ref": "#/$defs/result"}]}
if __name__ == "__main__":
    (HERE / "protocol.schema.json").write_text(json.dumps(build(), indent=2) + "\n")
