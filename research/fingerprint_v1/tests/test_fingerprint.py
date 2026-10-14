import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
from build_schema import build
from validate import strict_load, validate
from research.lorentz_n6.verify import polynomial, operators


class FingerprintContract(unittest.TestCase):
    def setUp(self):
        self.fp = strict_load(HERE / "examples/n6-0073.json")
        self.event = strict_load(HERE / "examples/separation-event.json")

    def reject(self, record):
        with self.assertRaises((ValueError, ValidationError)):
            validate(record)

    def test_schema_metaschema_and_generated_contract(self):
        for name, generated in zip(("x6-fingerprint.schema.json", "comparison-event.schema.json"), build()):
            Draft202012Validator.check_schema(generated)
            self.assertEqual(generated, strict_load(HERE / name))

    def test_all_delivered_examples_and_actual_separation(self):
        for path in (HERE / "examples").glob("*.json"):
            validate(strict_load(path))
        self.assertEqual(self.event["steps"][-1]["witness_feature_ids"], ["sector.directed_degrees"])

    def test_pair_polynomials_independently_recomputed(self):
        atlas = strict_load(ROOT / "research/lorentz_n6/results/atlas_n6.json")
        for identifier in ("n6-0073", "n6-0181"):
            row = next(r for r in atlas["records"] if r["id"] == identifier)
            fp = strict_load(HERE / ("examples/" + identifier + ".json"))
            for operator, feature in zip(operators(row["causal_matrix"])[:3], fp["layers"]["spectrum"]["features"]):
                self.assertEqual([str(v) for v in polynomial(operator)], feature["value"]["coefficients"])

    def test_degree_witness_invariant_under_relabelling(self):
        atlas = strict_load(ROOT / "research/lorentz_n6/results/atlas_n6.json")
        c = next(r["causal_matrix"] for r in atlas["records"] if r["id"] == "n6-0073")
        def degrees(matrix):
            return sorted((sum(row[i] for row in matrix), sum(matrix[i])) for i in range(len(matrix)))
        for permutation in ([5, 4, 3, 2, 1, 0], [2, 0, 4, 1, 5, 3]):
            self.assertEqual(degrees(c), degrees([[c[i][j] for j in permutation] for i in permutation]))

    def test_exact_float_payload_rejected(self):
        self.fp["layers"]["spectrum"]["features"][0]["value"]["coefficients"][2] = -5.0
        self.reject(self.fp)

    def test_no_unavailable_layer_can_hide_a_value(self):
        self.fp["layers"]["mode_structure"]["features"] = []
        self.reject(self.fp)

    def test_no_physical_equivalence_promotion(self):
        self.fp["claim"]["physical_equivalence"] = "CONFIRMED"
        self.reject(self.fp)

    def test_no_completed_physical_data_without_calibration_and_raw_samples(self):
        plan = strict_load(HERE / "examples/physical-pilot-plan.json")
        plan["acquisition"]["status"] = "COMPLETE"
        self.reject(plan)

    def test_no_synthetic_to_physical_promotion(self):
        self.fp["acquisition"]["evidence_kind"] = "SYNTHETIC_CONTROL"
        self.reject(self.fp)

    def test_false_exact_collision_rejected(self):
        self.event["steps"][-1]["outcome"] = "EXACT_COLLISION"
        self.event["steps"][-1]["witness_feature_ids"] = []
        self.reject(self.event)

    def test_non_cumulative_ladder_rejected(self):
        self.event["steps"][2]["feature_ids"] = ["sector.endpoints"]
        self.reject(self.event)

    def test_empirical_decision_requires_future_assessor(self):
        self.event["comparison_kind"] = "EMPIRICAL"
        self.reject(self.event)

    def test_hash_tampering_and_path_escape_rejected(self):
        for mutation in ({"sha256": "0" * 64}, {"path": "../outside.json"}):
            fp = copy.deepcopy(self.fp)
            fp["artifacts"][0].update(mutation)
            self.reject(fp)

    def test_dependent_evidence_cannot_be_cyclic(self):
        self.fp["layers"]["spectrum"]["features"][0]["depends_on"] = ["degeneracy.encoded"]
        self.reject(self.fp)

    def test_wrong_polynomial_degree_rejected(self):
        self.fp["layers"]["spectrum"]["features"][0]["value"]["coefficients"].pop()
        self.reject(self.fp)

    def test_rational_representation_cannot_create_false_separator(self):
        feature = copy.deepcopy(self.fp["layers"]["spectrum"]["features"][0])
        feature.update(id="test.projector", kind="projector_overlap", value={"format": "RATIONAL", "numerator": "2", "denominator": "4"})
        self.fp["layers"]["mode_structure"] = {"status": "AVAILABLE", "features": [feature]}
        self.reject(self.fp)

    def test_duplicate_keys_nan_and_numeric_overflow_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            for text in ('{"a":1,"a":2}', '{"a":NaN}', '{"a":1e999}'):
                path.write_text(text)
                with self.assertRaises(ValueError):
                    strict_load(path)


if __name__ == "__main__":
    unittest.main()
