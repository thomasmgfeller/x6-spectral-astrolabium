#!/usr/bin/env python3
"""Build closed, self-contained JSON Schema 2020-12 contracts (no network refs)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAYERS = {
    "spectrum": ["operator_polynomial", "psd", "resonance_frequencies"],
    "degeneracy": ["multiplicity_encoding", "resolved_multiplicities"],
    "sector": ["structural_signature", "symmetry_sector"],
    "mode_structure": ["projector_overlap", "sampled_mode_shape", "subspace_signature"],
    "correlation": ["cross_correlation", "cross_spectrum", "coherence", "state_two_point_function"],
    "dispersion": ["dispersion_relation"],
    "dynamics": ["transfer_function", "impulse_response", "decay_rates", "quill_response"],
}


def obj(properties, required=None, **extra):
    return dict(type="object", properties=properties,
                required=list(properties) if required is None else required,
                additionalProperties=False, **extra)


def arr(items, minimum=0, **extra):
    return dict(type="array", items=items, minItems=minimum, **extra)


def ref(name):
    return {"$ref": "#/$defs/" + name}


def enum(*values):
    return {"enum": list(values)}


TEXT = {"type": "string", "minLength": 1}
IDENT = {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:-]*$"}
NUM = {"type": "number"}
POS = {"type": "number", "exclusiveMinimum": 0}
INTSTR = {"type": "string", "pattern": "^(0|-[1-9][0-9]*|[1-9][0-9]*)$"}
SHA = {"type": "string", "pattern": "^[a-f0-9]{64}$"}
EVIDENCE = enum("EXACT_COMPUTATION", "NUMERICAL_COMPUTATION", "PHYSICAL_MEASUREMENT", "SYNTHETIC_CONTROL")
UNDEFINED = obj({"status": {"const": "UNDEFINED"}, "reason": TEXT})
DEFINED = obj({"status": {"const": "DEFINED"}, "id": IDENT, "definition": TEXT})


def build():
    defs = {}
    defs["artifact"] = obj({
        "id": IDENT, "path": TEXT, "sha256": SHA, "media_type": TEXT,
        "role": enum("protocol", "raw", "code", "derived", "calibration", "report"),
    })
    defs["definition"] = {"oneOf": [UNDEFINED, DEFINED]}
    defs["uncertainty"] = {"oneOf": [
        obj({"kind": {"const": "EXACT"}}),
        obj({"kind": {"const": "BOUNDED"}, "absolute_bound": {"type": "number", "minimum": 0}, "method": TEXT}),
        obj({"kind": {"const": "INTERVAL"}, "lower": NUM, "upper": NUM,
             "coverage": {"type": "number", "exclusiveMinimum": 0, "exclusiveMaximum": 1}, "method": TEXT}),
        obj({"kind": {"const": "ARTIFACT"}, "artifact_id": IDENT, "method": TEXT}),
        obj({"kind": {"const": "UNKNOWN"}, "reason": TEXT}),
    ]}
    defs["polynomial"] = obj({
        "format": {"const": "INTEGER_POLYNOMIAL"}, "operator_id": IDENT,
        "dimension": {"type": "integer", "minimum": 1},
        "coefficient_order": {"const": "DESCENDING"}, "coefficients": arr(INTSTR, 2),
    })
    defs["integer_vector"] = obj({"format": {"const": "INTEGER_VECTOR"}, "values": arr(INTSTR, 1)})
    defs["scalar"] = obj({"format": {"const": "SCALAR"}, "value": NUM})
    defs["rational"] = obj({"format": {"const": "RATIONAL"}, "numerator": INTSTR,
                            "denominator": {"type": "string", "pattern": "^[1-9][0-9]*$"}})
    defs["category"] = obj({"format": {"const": "CATEGORY"}, "value": TEXT})
    defs["series"] = obj({
        "format": enum("REAL_SERIES", "COMPLEX_SERIES"), "axis_name": TEXT, "axis_unit": TEXT,
        "axis": arr(NUM, 1), "real": arr(NUM, 1), "imaginary": arr(NUM, 1),
        "channel_ids": arr(IDENT, uniqueItems=True),
    }, required=["format", "axis_name", "axis_unit", "axis", "real", "channel_ids"],
        allOf=[{"if": {"properties": {"format": {"const": "COMPLEX_SERIES"}}},
                "then": {"required": ["imaginary"]}, "else": {"not": {"required": ["imaginary"]}}}])
    defs["feature"] = obj({
        "id": IDENT, "kind": enum(*(k for kinds in LAYERS.values() for k in kinds)),
        "definition": TEXT, "unit": TEXT, "evidence_kind": EVIDENCE,
        "source_ids": arr(IDENT, 1, uniqueItems=True), "depends_on": arr(IDENT, uniqueItems=True),
        "assumptions": arr(TEXT, uniqueItems=True), "uncertainty": ref("uncertainty"),
        "value": {"oneOf": [ref(k) for k in ["polynomial", "integer_vector", "scalar", "rational", "category", "series"]]},
    }, allOf=[
        {"if": {"properties": {"kind": {"const": "operator_polynomial"}}},
         "then": {"properties": {"value": ref("polynomial"), "unit": {"const": "1"}}}},
        {"if": {"properties": {"kind": {"const": "multiplicity_encoding"}}},
         "then": {"properties": {"value": ref("category"), "depends_on": {"minItems": 1}}}},
        {"if": {"properties": {"kind": {"enum": ["psd", "sampled_mode_shape", "cross_correlation", "cross_spectrum", "coherence", "state_two_point_function", "dispersion_relation", "transfer_function", "impulse_response"]}}},
         "then": {"properties": {"value": ref("series")}}},
        {"if": {"properties": {"evidence_kind": {"const": "EXACT_COMPUTATION"}}},
         "then": {"properties": {"uncertainty": {"properties": {"kind": {"const": "EXACT"}}},
                                  "value": {"oneOf": [ref(k) for k in ["polynomial", "integer_vector", "rational", "category"]]}}},
         "else": {"properties": {"uncertainty": {"not": {"properties": {"kind": {"const": "EXACT"}}}}}}},
    ])
    for layer, kinds in LAYERS.items():
        defs[layer] = {"oneOf": [
            obj({"status": {"const": "AVAILABLE"},
                 "features": arr({"allOf": [ref("feature"), {"properties": {"kind": {"enum": kinds}}}]}, 1)}),
            obj({"status": enum("NOT_MEASURED", "NOT_APPLICABLE", "INVALID"), "reason": TEXT}),
        ]}
    defs["channel"] = obj({
        "id": IDENT, "quantity": TEXT, "unit": TEXT, "sensor_id": TEXT,
        "position_m": arr(NUM, 3, maxItems=3), "axis": TEXT,
        "calibration_artifact_id": IDENT,
    }, required=["id", "quantity", "unit", "sensor_id", "position_m", "axis"])
    defs["acquisition"] = obj({
        "profile": enum("CAUSAL_ORDER_EXACT", "SIGNAL_SINGLE_POINT", "MODAL_2R1F", "DISPERSION_SPATIAL", "MODEL_SIMULATION"),
        "status": enum("PLANNED", "COMPLETE"), "evidence_kind": EVIDENCE,
        "channels": arr(ref("channel")), "raw_artifact_ids": arr(IDENT, uniqueItems=True),
        "clock": {"oneOf": [UNDEFINED, obj({
            "status": {"const": "DEFINED"}, "sample_rate_hz": POS,
            "samples_per_channel": {"type": "integer", "minimum": 1},
            "synchronization": TEXT, "max_skew_s": {"type": "number", "minimum": 0},
            "anti_alias_filter": TEXT,
        })]},
        "quality": obj({"status": enum("NOT_RUN", "PASS", "FAIL"), "report_artifact_ids": arr(IDENT, uniqueItems=True)}),
    }, allOf=[
        {"if": {"properties": {"profile": {"const": "CAUSAL_ORDER_EXACT"}}},
         "then": {"properties": {"evidence_kind": {"const": "EXACT_COMPUTATION"}, "channels": {"maxItems": 0}}}},
        {"if": {"properties": {"status": {"const": "COMPLETE"}, "evidence_kind": {"const": "PHYSICAL_MEASUREMENT"}}},
         "then": {"properties": {
             "channels": {"minItems": 1, "items": {"required": ["calibration_artifact_id"]}},
             "raw_artifact_ids": {"minItems": 1}, "clock": {"properties": {"status": {"const": "DEFINED"}}},
             "quality": {"properties": {"status": enum("PASS", "FAIL"), "report_artifact_ids": {"minItems": 1}}},
         }}},
        {"if": {"properties": {"status": {"const": "COMPLETE"}, "profile": {"const": "MODAL_2R1F"}}},
         "then": {"properties": {"channels": {"minItems": 3}}}},
    ])
    schema = obj({
        "schema_version": {"const": "x6.fingerprint/1.0.0"},
        "fingerprint_id": IDENT, "created_utc": {"type": "string", "format": "date-time", "pattern": "Z$"},
        "subject": obj({"id": IDENT, "kind": enum("CAUSAL_ORDER", "PHYSICAL_SYSTEM", "SIMULATION"), "description": TEXT}),
        "context": obj({"protocol_artifact_id": IDENT, "comparison_domain": IDENT,
                         "model": ref("definition"), "state_or_ensemble": ref("definition"),
                         "geometry": ref("definition"), "scale": TEXT, "invariances": arr(TEXT, 1, uniqueItems=True)}),
        "acquisition": ref("acquisition"), "layers": obj({k: ref(k) for k in LAYERS}),
        "artifacts": arr(ref("artifact"), 1),
        "provenance": obj({"code_artifact_ids": arr(IDENT, 1, uniqueItems=True), "method_version": TEXT,
                           "command": TEXT, "runtime": TEXT}),
        "claim": obj({"scope": TEXT, "physical_equivalence": {"const": "NOT_ASSESSED"}}),
    }, allOf=[
        {"if": {"properties": {"acquisition": {"properties": {"status": {"const": "PLANNED"}}}}},
         "then": {"properties": {"layers": {"properties": {k: {"properties": {"status": enum("NOT_MEASURED", "NOT_APPLICABLE")}} for k in LAYERS}}}}},
    ])
    schema.update({"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "urn:x6:fingerprint:1.0.0", "$defs": defs,
                   "title": "X6 multilayer fingerprint v1.0.0", "$comment": "Run validate.py as well: cross-references, array dimensions, evidence constraints and local hashes are semantic checks. Schema validity does not certify a physical claim."})
    event = obj({
        "schema_version": {"const": "x6.comparison-event/1.0.0"}, "event_id": IDENT,
        "fingerprints": arr(obj({"id": IDENT, "path": TEXT, "sha256": SHA}), 2, maxItems=2),
        "comparison_domain": IDENT, "protocol_sha256": SHA,
        "scope": TEXT, "comparison_kind": enum("EXACT", "EMPIRICAL"),
        "steps": arr(obj({
            "index": {"type": "integer", "minimum": 0}, "feature_ids": arr(IDENT, 1, uniqueItems=True),
            "outcome": enum("EXACT_COLLISION", "OBSERVATIONALLY_UNRESOLVED", "SEPARATED", "INCONCLUSIVE"),
            "witness_feature_ids": arr(IDENT, uniqueItems=True), "reason": TEXT,
            "selection_basis": TEXT,
        }), 1),
        "stop_reason": enum("SEPARATED_WITHIN_SCOPE", "BUDGET_EXHAUSTED", "NO_ADMISSIBLE_OBSERVABLE", "NEEDS_CONFIRMATION"),
        "physical_equivalence": {"const": "NOT_ASSESSED"},
    })
    event.update({"$schema": schema["$schema"], "$id": "urn:x6:comparison-event:1.0.0", "title": "X6 comparison event"})
    return schema, event


if __name__ == "__main__":
    for name, schema in zip(["x6-fingerprint.schema.json", "comparison-event.schema.json"], build()):
        (HERE / name).write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n")
