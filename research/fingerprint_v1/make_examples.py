#!/usr/bin/env python3
"""Generate real exact-atlas examples and an explicitly unmeasured bench plan."""
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact(identifier, path, role):
    return {"id": identifier, "path": str(path.relative_to(ROOT)), "sha256": digest(path),
            "media_type": "text/x-python" if path.suffix == ".py" else "application/json", "role": role}


def write(name, value):
    path = HERE / "examples" / name
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    return path


def undefined(reason):
    return {"status": "UNDEFINED", "reason": reason}


def feature(identifier, kind, definition, value, dependencies=None):
    return {"id": identifier, "kind": kind, "definition": definition, "unit": "1",
            "evidence_kind": "EXACT_COMPUTATION", "source_ids": ["atlas", "protocol"],
            "depends_on": dependencies or [], "assumptions": ["Strict causal relation; time orientation retained."],
            "uncertainty": {"kind": "EXACT"}, "value": value}


def build():
    created = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    atlas_path = ROOT / "research/lorentz_n6/results/atlas_n6.json"
    verification = ROOT / "research/lorentz_n6/results/independent_verification.json"
    records = {r["id"]: r for r in json.loads(atlas_path.read_text())["records"]}
    files = []
    for identifier in ("n6-0073", "n6-0181"):
        record = records[identifier]
        spectra = [feature("spectrum." + operator, "operator_polynomial",
                           "Complete monic det(xI-" + operator + "), as defined in protocol.exact.operators.",
                           {"format": "INTEGER_POLYNOMIAL", "operator_id": operator, "dimension": 6,
                            "coefficient_order": "DESCENDING", "coefficients": list(map(str, coefficients))})
                   for operator, coefficients in zip(("S", "A", "K"), record["polynomials_S_A_K"])]
        matrix = record["causal_matrix"]
        degrees = sorted((sum(matrix[j][i] for j in range(6)), sum(matrix[i])) for i in range(6))
        layers = {
            "spectrum": {"status": "AVAILABLE", "features": spectra},
            "degeneracy": {"status": "AVAILABLE", "features": [feature(
                "degeneracy.encoded", "multiplicity_encoding",
                "Algebraic eigenvalue multiplicities are encoded by the full characteristic polynomials; no new independent evidence.",
                {"format": "CATEGORY", "value": "ENCODED_IN_COMPLETE_CHARACTERISTIC_POLYNOMIALS"},
                [f["id"] for f in spectra])]},
            "sector": {"status": "AVAILABLE", "features": [
                feature("sector.endpoints", "structural_signature", "Ordered minimal,maximal,isolated element counts.",
                        {"format": "INTEGER_VECTOR", "values": list(map(str, record["minimal_maximal_isolated"]))}),
                feature("sector.directed_degrees", "structural_signature", "Lexicographically sorted (past-size,future-size) pairs, flattened; full causal relation, not Hasse links.",
                        {"format": "INTEGER_VECTOR", "values": [str(v) for pair in degrees for v in pair]}),
            ]},
            "mode_structure": {"status": "NOT_MEASURED", "reason": "No projector or mode-shape comparison has been run for this record."},
            "correlation": {"status": "NOT_APPLICABLE", "reason": "No field observable and state/ensemble specified for this order-only experiment."},
            "dispersion": {"status": "NOT_APPLICABLE", "reason": "No momentum, spatial coordinate, embedding or time-translation model specified."},
            "dynamics": {"status": "NOT_APPLICABLE", "reason": "No evolution law or controlled dynamical probe in this fingerprint."},
        }
        value = {
            "schema_version": "x6.fingerprint/1.0.0", "fingerprint_id": "fp-" + identifier,
            "created_utc": created,
            "subject": {"id": identifier, "kind": "CAUSAL_ORDER", "description": "Exact six-element order from the independently algorithm-checked project atlas."},
            "context": {"protocol_artifact_id": "protocol", "comparison_domain": "lorentz-n6-order-oriented-v1",
                        "model": {"status": "DEFINED", "id": "finite-poset", "definition": "Strict finite partial order; no field dynamics or continuum identification."},
                        "state_or_ensemble": undefined("No physical state specified."),
                        "geometry": undefined("No embedding into a continuum assigned."), "scale": "n=6; dimensionless finite order",
                        "invariances": ["Simultaneous permutation of rows and columns of all operators."]},
            "acquisition": {"profile": "CAUSAL_ORDER_EXACT", "status": "COMPLETE", "evidence_kind": "EXACT_COMPUTATION",
                            "channels": [], "raw_artifact_ids": ["atlas"], "clock": undefined("Exact computation has no acquisition clock."),
                            "quality": {"status": "PASS", "report_artifact_ids": ["verification"]}},
            "layers": layers,
            "artifacts": [artifact("protocol", HERE / "protocol.json", "protocol"), artifact("atlas", atlas_path, "raw"),
                          artifact("verification", verification, "report"), artifact("generator", Path(__file__).resolve(), "code")],
            "provenance": {"code_artifact_ids": ["generator"], "method_version": "x6-fingerprint-reference-1.0.0",
                           "command": "python research/fingerprint_v1/make_examples.py", "runtime": "Python " + platform.python_version()},
            "claim": {"scope": "Finite n=6 atlas; exact registered invariants, with multiplicities derived from spectrum. No physical measurement.",
                      "physical_equivalence": "NOT_ASSESSED"},
        }
        files.append(write(identifier + ".json", value))
    steps = []
    groups = [["spectrum.S"], ["spectrum.A", "spectrum.K"], ["sector.endpoints"], ["sector.directed_degrees"]]
    cumulative = []
    for index, added in enumerate(groups):
        cumulative += added
        steps.append({"index": index, "feature_ids": list(cumulative),
                      "outcome": "SEPARATED" if index == 3 else "EXACT_COLLISION",
                      "witness_feature_ids": ["sector.directed_degrees"] if index == 3 else [],
                      "reason": "Different paired degree multisets." if index == 3 else "Identical exact values for all accumulated observables.",
                      "selection_basis": "Predeclared low-cost demonstration order; no learned information-gain claim."})
    event = {"schema_version": "x6.comparison-event/1.0.0", "event_id": "n6-0073-vs-0181",
             "fingerprints": [{"id": "fp-" + p.stem, "path": str(p.relative_to(ROOT)), "sha256": digest(p)} for p in files],
             "comparison_domain": "lorentz-n6-order-oriented-v1", "protocol_sha256": digest(HERE / "protocol.json"),
             "scope": "This pair of distinct atlas orders; no universal uniqueness claim.", "comparison_kind": "EXACT", "steps": steps,
             "stop_reason": "SEPARATED_WITHIN_SCOPE", "physical_equivalence": "NOT_ASSESSED"}
    files.append(write("separation-event.json", event))
    plan = json.loads(files[0].read_text())
    plan["fingerprint_id"] = "fp-modal-pilot-design"
    plan["subject"] = {"id": "bench-undesignated", "kind": "PHYSICAL_SYSTEM", "description": "Proposed two-position mechanical response experiment; no hardware or data acquired."}
    plan["context"] = {"protocol_artifact_id": "protocol", "comparison_domain": "mechanical-modal-pilot-design-v1",
                       "model": {"status": "DEFINED", "id": "small-signal-lti-hypothesis", "definition": "Linear time-invariant response is a hypothesis to test within registered amplitudes and mounting."},
                       "state_or_ensemble": undefined("Operating point and repeat ensemble must be registered before acquisition."),
                       "geometry": undefined("Actual fixture, coordinates and sensor axes must be surveyed."),
                       "scale": "Proposed analysis band 20–2000 Hz; 10 s records.", "invariances": ["Common acquisition time origin; no independent per-channel phase alignment."]}
    plan["acquisition"] = {"profile": "MODAL_2R1F", "status": "PLANNED", "evidence_kind": "PHYSICAL_MEASUREMENT",
                           "channels": [{"id": name, "quantity": quantity, "unit": unit, "sensor_id": "UNASSIGNED",
                                         "position_m": position, "axis": "Proposed +z; must be surveyed"}
                                        for name, quantity, unit, position in [("a1", "acceleration", "m/s^2", [0, 0, 0]),
                                                                              ("a2", "acceleration", "m/s^2", [0.1, 0, 0]),
                                                                              ("F", "force", "N", [0.05, 0, 0])]],
                           "raw_artifact_ids": [], "clock": undefined("DAQ hardware not assigned or calibrated; see protocol for design targets."),
                           "quality": {"status": "NOT_RUN", "report_artifact_ids": []}}
    plan["layers"] = {k: {"status": "NOT_MEASURED", "reason": "Design only; no physical acquisition."} for k in plan["layers"]}
    plan["artifacts"] = [a for a in plan["artifacts"] if a["id"] in {"protocol", "generator"}]
    plan["claim"] = {"scope": "Proposed acquisition design only. Coordinates are placeholders, not measured geometry.", "physical_equivalence": "NOT_ASSESSED"}
    files.append(write("physical-pilot-plan.json", plan))
    return files


if __name__ == "__main__":
    for path in build():
        print(path.relative_to(ROOT))
