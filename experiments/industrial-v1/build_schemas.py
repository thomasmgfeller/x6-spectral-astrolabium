"""Generate closed Draft 2020-12 schemas; all references are local."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def obj(properties):
    return {"type": "object", "properties": properties,
            "required": list(properties), "additionalProperties": False}


def array(items, low=0, high=100000):
    return {"type": "array", "items": items, "minItems": low, "maxItems": high}


def nullable(item):
    return {"anyOf": [item, {"type": "null"}]}


def number(low=0, high=None):
    out = {"type": "number", "minimum": low}
    if high is not None:
        out["maximum"] = high
    return out


TEXT = {"type": "string", "minLength": 1, "maxLength": 1000}
SHA = {"type": "string", "pattern": "^[a-f0-9]{64}$"}
BOOL = {"type": "boolean"}
COUNT = {"type": "integer", "minimum": 1, "maximum": 100000}
STAMP = {"type": "string", "format": "date-time", "pattern": "Z$"}
REF = obj({"path": TEXT, "sha256": SHA})
EVIDENCE = {"enum": ["REAL_MEASURED", "SYNTHETIC_CONTROL"]}
ROLES = ["machine_and_sensor", "acquisition_and_calibration", "data_rights",
         "ground_truth_definition", "split_and_access_registry", "power_plan",
         "protocol_review", "candidate_source", "baseline_source", "resource_protocol"]


def schemas():
    profile = obj({
        "schema": {"const": "x6.industrial.v1.profile/1"}, "profile_id": TEXT,
        "status": {"enum": ["DRAFT", "FROZEN"]}, "frozen_utc": nullable(STAMP),
        "evidence_class": EVIDENCE, "primary_route": {"const": "D"},
        "sampling": obj({"channels": {"const": 4}, "sample_rate_hz": {"const": 25600},
                         "block_samples": {"const": 256}, "dtype": {"const": "float32-le"},
                         "unit": {"const": "m/s^2"}, "record_samples_per_channel": {"const": 256000}}),
        "processing": obj({"causal": {"const": True}, "lookahead_samples": {"const": 0},
                           "diagnostic_unit": {"const": "one_preselected_record_per_independent_bearing"},
                           "decision_rule": {"const": "score_gte_frozen_threshold"},
                           "candidate_id": nullable(TEXT), "baseline_id": nullable(TEXT),
                           "candidate_threshold": nullable(number(-1e100, 1e100)),
                           "baseline_threshold": nullable(number(-1e100, 1e100))}),
        "statistics": obj({"family_alpha": {"const": 0.05},
                           "registered_claim_count": {"type": "integer", "minimum": 1, "maximum": 2},
                           "sensitivity_min": number(0, 1), "sensitivity_gain_min": number(0, 1),
                           "false_positive_rate_max": number(0, 0.01),
                           "min_positive_units": nullable(COUNT), "min_negative_units": nullable(COUNT),
                           "target_power": number(0.8, 1)}),
        "limits": obj({"latency_max_ms": number(0.001, 50), "mean_service_exclusive_ms": {"const": 10},
                       "p99_service_max_ms": number(0.001, 10),
                       "additional_state_max_bytes": {"type": "integer", "minimum": 1, "maximum": 8388608},
                       "max_backlog_blocks": {"type": "integer", "minimum": 0, "maximum": 4},
                       "resource_blocks": {"type": "integer", "minimum": 6000, "maximum": 100000},
                       "amplitude_relative_error_max": number(0, 1),
                       "timing_error_max_samples": number(0, 256)}),
        "references": obj({role: nullable(REF) for role in ROLES}),
        "preservation_cases": array(obj({"id": TEXT, "reference_amplitude": {"type": "number", "exclusiveMinimum": 0},
                                          "reference_sample": {"type": "integer", "minimum": 0},
                                          "reference_kind": {"enum": ["DESIGN_ONLY", "SYNTHETIC_FLOAT32"]},
                                          "sample_count": COUNT,
                                          "peak_window": {"type": "array", "items": {"type": "integer", "minimum": 0}, "minItems": 2, "maxItems": 2},
                                          "reference": REF}), 1, 10000),
    })
    manifest = obj({
        "schema": {"const": "x6.industrial.v1.inputs/1"}, "evidence_class": EVIDENCE,
        "profile_sha256": SHA, "units": array(obj({
            "record_id": TEXT, "bearing_id": TEXT,
            "split": {"enum": ["development", "validation", "holdout", "external"]},
            "label": {"enum": ["healthy", "damaged"]}, "samples": REF,
        }), 1, 10000),
    })
    result = obj({
        "schema": {"const": "x6.industrial.v1.result/1"}, "run_id": TEXT,
        "started_utc": STAMP, "evidence_class": EVIDENCE,
        "profile_sha256": SHA, "input_manifest_sha256": SHA,
        "candidate_source_sha256": SHA, "baseline_source_sha256": SHA,
        "environment": obj({"hardware": TEXT, "os": TEXT, "runtime": TEXT,
                            "precision": {"const": "float32"}, "measurement_report": REF}),
        "decisions": array(obj({"record_id": TEXT, "candidate_score": {"type": "number"},
                                 "baseline_score": {"type": "number"}}), 1, 10000),
        "preservation": array(obj({"id": TEXT, "output": REF}), 1, 10000),
        "resources": obj({"service_ms": array(number(), 1), "latency_ms": array(number(), 1),
                          "additional_state_peak_bytes": {"type": "integer", "minimum": 0},
                          "dropped_blocks": {"type": "integer", "minimum": 0},
                          "peak_backlog_blocks": {"type": "integer", "minimum": 0},
                          "final_backlog_blocks": {"type": "integer", "minimum": 0}}),
    })
    bounds = {"type": "array", "items": {"type": "number"}, "minItems": 2, "maxItems": 2}
    assessment = {
        "type": "object", "additionalProperties": False,
        "required": ["schema", "status", "claim_supported", "evaluator_sha256"],
        "properties": {
            "schema": {"const": "x6.industrial.v1.assessment/1"},
            "status": {"enum": ["PASS", "FAIL", "INCONCLUSIVE", "NOT_READY", "INVALID", "READY_FOR_RESULT_REVIEW"]},
            "claim_supported": BOOL, "evaluator_sha256": SHA, "profile_sha256": SHA,
            "inputs_sha256": SHA, "result_sha256": SHA, "blocking_items": array(TEXT), "reason": TEXT,
            "evidence_class": EVIDENCE, "claim_scope": {"enum": ["REGISTERED_V1_DATASET_ONLY", "SOFTWARE_CONTROL_ONLY"]},
            "alpha_per_claim": number(0, 1),
            "gates": {"type": "object", "additionalProperties": {"enum": ["PASS", "FAIL", "INCONCLUSIVE"]}},
            "counts": obj({k: {"type": "integer", "minimum": 0} for k in
                           ("positive_bearings", "negative_bearings", "true_positive", "false_positive", "paired_wins", "paired_losses")}),
            "one_sided_bounds": obj({k: bounds for k in ("sensitivity", "false_positive_rate", "paired_sensitivity_gain")}),
            "resources": obj({k: number() for k in ("mean_service_ms", "p99_service_ms", "max_observed_latency_ms")}),
            "unavailable_metrics": obj({"reconstruction_MSE": TEXT, "energy_savings": TEXT}),
        },
        "allOf": [
            {"if": {"properties": {"status": {"enum": ["PASS", "FAIL", "INCONCLUSIVE"]}}},
             "then": {"required": ["gates", "counts", "one_sided_bounds", "evidence_class", "claim_scope"]}},
            {"if": {"properties": {"status": {"const": "INVALID"}}}, "then": {"required": ["reason"]}},
            {"if": {"properties": {"status": {"const": "NOT_READY"}}}, "then": {"required": ["blocking_items"]}},
            {"if": {"properties": {"claim_supported": {"const": True}}},
             "then": {"required": ["evidence_class", "claim_scope"], "properties": {
                 "status": {"const": "PASS"}, "evidence_class": {"const": "REAL_MEASURED"},
                 "claim_scope": {"const": "REGISTERED_V1_DATASET_ONLY"}}}},
        ],
    }
    return {"profile": profile, "inputs": manifest, "result": result, "assessment": assessment}


if __name__ == "__main__":
    for name, schema in schemas().items():
        schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
        (ROOT/"schema"/(name+".schema.json")).write_text(json.dumps(schema, indent=2)+"\n")
