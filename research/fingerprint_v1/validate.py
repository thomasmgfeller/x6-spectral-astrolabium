#!/usr/bin/env python3
"""Validate structure, references and local evidence hashes; not physical truth."""
import argparse
import hashlib
import json
import math
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def strict_load(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key: " + key)
            result[key] = value
        return result

    def reject(value):
        raise ValueError("non-finite JSON number: " + value)

    value = json.loads(Path(path).read_text(), object_pairs_hook=pairs, parse_constant=reject)
    def finite(node):
        if isinstance(node, float):
            require(math.isfinite(node), "non-finite or overflowed JSON number")
        elif isinstance(node, dict):
            for item in node.values():
                finite(item)
        elif isinstance(node, list):
            for item in node:
                finite(item)
    finite(value)
    return value


def checked_file(root, record):
    rel = Path(record["path"])
    require(not rel.is_absolute() and ".." not in rel.parts, "artifact path must be repository-relative")
    path = (root / rel).resolve()
    require(path.is_relative_to(root.resolve()), "artifact escaped repository root")
    require(path.is_file(), "missing artifact: " + str(rel))
    require(hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"], "artifact hash mismatch: " + str(rel))
    return path


def features(record):
    return {f["id"]: f for layer in record["layers"].values() for f in layer.get("features", [])}


def validate(record, root=ROOT):
    kind = record.get("schema_version")
    schema_name = {"x6.fingerprint/1.0.0": "x6-fingerprint.schema.json",
                   "x6.comparison-event/1.0.0": "comparison-event.schema.json"}.get(kind)
    require(schema_name is not None, "unknown schema version")
    schema = strict_load(HERE / schema_name)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(record)
    if kind == "x6.comparison-event/1.0.0":
        return validate_event(record, root)
    artifacts = {a["id"]: a for a in record["artifacts"]}
    require(len(artifacts) == len(record["artifacts"]), "duplicate artifact id")
    for artifact in artifacts.values():
        checked_file(root, artifact)
    def link(identifier, role=None):
        require(identifier in artifacts, "unknown artifact id: " + identifier)
        require(role is None or artifacts[identifier]["role"] == role, "incorrect artifact role: " + identifier)
    link(record["context"]["protocol_artifact_id"], "protocol")
    for identifier in record["provenance"]["code_artifact_ids"]:
        link(identifier, "code")
    acq = record["acquisition"]
    channels = {c["id"]: c for c in acq["channels"]}
    require(len(channels) == len(acq["channels"]), "duplicate channel id")
    for channel in channels.values():
        if "calibration_artifact_id" in channel:
            link(channel["calibration_artifact_id"], "calibration")
    for identifier in acq["raw_artifact_ids"]:
        link(identifier, "raw")
    for identifier in acq["quality"]["report_artifact_ids"]:
        link(identifier, "report")
    if acq["status"] == "COMPLETE":
        require(bool(acq["raw_artifact_ids"]), "completed acquisition needs raw input")
    if acq["profile"] == "MODAL_2R1F":
        response = [c for c in channels.values() if c["quantity"] == "acceleration" and c["unit"] == "m/s^2"]
        force = [c for c in channels.values() if c["quantity"] == "force" and c["unit"] == "N"]
        require(len(response) >= 2 and len(force) >= 1, "MODAL_2R1F requires two response channels and a force channel")
        require(len({tuple(c["position_m"]) for c in response}) >= 2, "response positions must differ")
    fs = features(record)
    count = sum(len(v.get("features", [])) for v in record["layers"].values())
    require(len(fs) == count, "duplicate feature id")
    require(not fs or (acq["status"] == "COMPLETE" and acq["quality"]["status"] == "PASS"), "available features require a completed acquisition and passed quality gate")
    for identifier, feature in fs.items():
        evidence = feature["evidence_kind"]
        permitted = {"EXACT_COMPUTATION": {"EXACT_COMPUTATION", "NUMERICAL_COMPUTATION"},
                     "NUMERICAL_COMPUTATION": {"NUMERICAL_COMPUTATION"},
                     "PHYSICAL_MEASUREMENT": {"PHYSICAL_MEASUREMENT"},
                     "SYNTHETIC_CONTROL": {"SYNTHETIC_CONTROL"}}[acq["evidence_kind"]]
        require(evidence in permitted, "feature evidence does not match acquisition origin")
        for source in feature["source_ids"]:
            link(source)
        for dependency in feature["depends_on"]:
            require(dependency in fs and dependency != identifier, "invalid feature dependency")
        uncertainty = feature["uncertainty"]
        if uncertainty["kind"] == "INTERVAL":
            require(uncertainty["lower"] <= uncertainty["upper"], "reversed uncertainty interval")
        if uncertainty["kind"] == "ARTIFACT":
            link(uncertainty["artifact_id"])
        value = feature["value"]
        form = value["format"]
        if form == "INTEGER_POLYNOMIAL":
            require(len(value["coefficients"]) == value["dimension"] + 1, "wrong polynomial degree")
            require(value["coefficients"][0] == "1", "characteristic polynomial must be monic")
        if form == "RATIONAL":
            require(math.gcd(int(value["numerator"]), int(value["denominator"])) == 1, "exact rational must be reduced to canonical form")
        if form in {"REAL_SERIES", "COMPLEX_SERIES"}:
            require(len(value["axis"]) == len(value["real"]), "series length mismatch")
            require(all(a < b for a, b in zip(value["axis"], value["axis"][1:])), "series axis must increase strictly")
            if "imaginary" in value:
                require(len(value["imaginary"]) == len(value["axis"]), "complex series length mismatch")
            require(set(value["channel_ids"]) <= set(channels), "unknown series channel")
            if feature["kind"] == "coherence":
                require(form == "REAL_SERIES" and all(0 <= x <= 1 for x in value["real"]), "invalid coherence")
        if feature["kind"] == "multiplicity_encoding":
            require(all(fs[d]["kind"] == "operator_polynomial" for d in feature["depends_on"]), "multiplicity must reference full operator spectra")
    def walk(identifier, stack):
        require(identifier not in stack, "cyclic feature dependencies")
        for dependency in fs[identifier]["depends_on"]:
            walk(dependency, stack | {identifier})
    for identifier in fs:
        walk(identifier, set())
    for layer in ("correlation", "dispersion", "dynamics"):
        if record["layers"][layer]["status"] == "AVAILABLE":
            require(record["context"]["model"]["status"] == "DEFINED", layer + " needs a model")
            if layer == "correlation":
                require(record["context"]["state_or_ensemble"]["status"] == "DEFINED", "correlation needs a state or ensemble")
            if layer == "dispersion":
                require(record["context"]["geometry"]["status"] == "DEFINED", "dispersion needs geometry and coordinate conventions")
    return "VALID_STRUCTURE_REFERENCES_AND_HASHES"


def validate_event(event, root):
    # Empirical decisions require a separately registered statistical assessor.
    # This reference release executes exact comparisons only.
    require(event["comparison_kind"] == "EXACT", "empirical event assessment is not implemented in v1")
    records = []
    for artifact in event["fingerprints"]:
        record = strict_load(checked_file(root, artifact))
        require(record.get("schema_version") == "x6.fingerprint/1.0.0", "event input must be a fingerprint")
        validate(record, root)
        require(record["fingerprint_id"] == artifact["id"], "fingerprint id mismatch")
        require(record["context"]["comparison_domain"] == event["comparison_domain"], "incompatible comparison domains")
        protocol = next(a for a in record["artifacts"] if a["id"] == record["context"]["protocol_artifact_id"])
        require(protocol["sha256"] == event["protocol_sha256"], "different protocols")
        records.append(record)
    require(records[0]["fingerprint_id"] != records[1]["fingerprint_id"], "self-comparison is not a collision event")
    # Model/state/geometry/scale and invariance declarations must match as well.
    require(records[0]["context"] == records[1]["context"], "comparison context mismatch")
    left, right = map(features, records)
    previous = set()
    for index, step in enumerate(event["steps"]):
        current = set(step["feature_ids"])
        require(step["index"] == index, "nonconsecutive comparison steps")
        require(previous < current, "steps must strictly accumulate observables")
        require(current <= left.keys() and current <= right.keys(), "missing compared feature")
        witnesses = set()
        for identifier in current:
            a, b = left[identifier], right[identifier]
            require(a["evidence_kind"] == b["evidence_kind"] == "EXACT_COMPUTATION", "exact comparison requires exact evidence")
            for key in ("kind", "definition", "unit", "assumptions", "depends_on"):
                require(a[key] == b[key], "feature definition mismatch")
            for key in ("format", "operator_id", "dimension"):
                require(a["value"].get(key) == b["value"].get(key), "value representation or operator mismatch")
            if a["value"] != b["value"]:
                witnesses.add(identifier)
        require(set(step["witness_feature_ids"]) == witnesses, "incorrect separation witnesses")
        require(step["outcome"] == ("SEPARATED" if witnesses else "EXACT_COLLISION"), "incorrect exact comparison outcome")
        previous = current
    if event["stop_reason"] == "SEPARATED_WITHIN_SCOPE":
        require(event["steps"][-1]["outcome"] == "SEPARATED", "unsupported separation stop")
    return "VALID_EXACT_COMPARISON_EVENT"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        for filename in args.files:
            result = validate(strict_load(filename), args.root)
            print(json.dumps({"file": filename, "status": result, "physical_equivalence": "NOT_ASSESSED"}))
    except Exception as exc:
        # ValidationError carries actionable schema-path detail.
        print(json.dumps({"status": "INVALID", "reason": str(exc)}))
        raise SystemExit(2)
