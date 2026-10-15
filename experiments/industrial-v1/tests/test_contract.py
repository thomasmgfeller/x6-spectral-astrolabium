import copy
import importlib.util
import json
import math
from pathlib import Path
import struct
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import evaluate as e
from make_control import make
from build_schemas import schemas


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.fixture = make(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def setUp(self):
        self.p, self.i, self.r, self.ph, self.ih = copy.deepcopy(self.fixture)

    def run_evaluation(self):
        return e.evaluate(self.p, self.i, self.r, self.root, self.ph, self.ih)

    def test_end_to_end_small_control_is_inconclusive(self):
        out = self.run_evaluation()
        self.assertEqual(out["status"], "INCONCLUSIVE")
        self.assertFalse(out["claim_supported"])
        self.assertEqual(out["claim_scope"], "SOFTWARE_CONTROL_ONLY")
        self.assertEqual(out["gates"]["amplitude:impulse"], "PASS")
        self.assertGreater(out["one_sided_bounds"]["false_positive_rate"][1], 0)
        out["evaluator_sha256"] = "0"*64
        e.validate(out, "assessment")

    def test_real_draft_is_not_ready(self):
        profile = json.loads((ROOT/"V1_PROFILE_DRAFT.json").read_text())
        missing = e.readiness(profile, ROOT)
        self.assertIn("references.data_rights", missing)
        self.assertTrue(any("not_materialized" in s for s in missing))

    def test_exact_zero_failure_bound(self):
        self.assertAlmostEqual(e.cp_bounds(0, 400, .025)[1], 1-.025**(1/400), places=12)
        self.assertGreater(e.cp_bounds(0, 367, .025)[1], .01)
        self.assertLessEqual(e.cp_bounds(0, 368, .025)[1], .01)
        self.assertAlmostEqual(e.cp_bounds(400, 400, .025)[0], .025**(1/400), places=12)

    def test_schema_snapshots_match_generator(self):
        for name, schema in schemas().items():
            schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
            self.assertEqual(schema, json.loads((ROOT/"schema"/(name+".schema.json")).read_text()))

    def test_assessment_cannot_promote_synthetic_control(self):
        out = self.run_evaluation()
        out.update(status="PASS", claim_supported=True, evaluator_sha256="0"*64)
        with self.assertRaises(Exception):
            e.validate(out, "assessment")

    def test_paired_bounds_against_multinomial_enumeration(self):
        n = 6
        for pw, pl in ((.1, .1), (.5, .1), (.7, .2), (.0, .2)):
            below = above = 0
            for w in range(n+1):
                for loss in range(n-w+1):
                    ties = n-w-loss
                    mass = math.factorial(n)/math.factorial(w)/math.factorial(loss)/math.factorial(ties)
                    mass *= pw**w * pl**loss * (1-pw-pl)**ties
                    lo, hi = e.paired_bounds(w, loss, n, .05)
                    below += mass*(pw-pl < lo)
                    above += mass*(pw-pl > hi)
            self.assertLessEqual(max(below, above), .05+1e-12)

    def test_all_binomial_outcomes_have_one_sided_coverage(self):
        # Independent finite probability enumeration, including boundary p=0,1.
        for n in (1, 5, 20):
            for p in (0, .01, .2, .5, .8, .99, 1):
                below = above = 0
                for k in range(n+1):
                    probability = math.comb(n, k)*p**k*(1-p)**(n-k)
                    lo, hi = e.cp_bounds(k, n, .05)
                    below += probability*(p < lo)
                    above += probability*(p > hi)
                self.assertLessEqual(max(below, above), .05+1e-12)

    def test_statistical_pass_fail_and_inconclusive_controls(self):
        stats = self.p["statistics"]
        self.assertEqual(set(e.diagnostic_gates(stats, 1000, 1000, 1000, 0, 500, 0)[-1].values()), {"PASS"})
        self.assertIn("FAIL", e.diagnostic_gates(stats, 1000, 1000, 0, 500, 0, 500)[-1].values())
        self.assertIn("INCONCLUSIVE", e.diagnostic_gates(stats, 1, 1, 1, 0, 1, 0)[-1].values())
        self.assertEqual(e.bound_gate((.05, .08), .05, "lower", True), "INCONCLUSIVE")
        self.assertEqual(e.bound_gate((.01, .05), .05, "lower", True), "FAIL")

    def test_duplicate_bearing_rejected(self):
        self.i["units"][1]["bearing_id"] = self.i["units"][0]["bearing_id"]
        with self.assertRaisesRegex(ValueError, "REPEATED_BEARING"):
            self.run_evaluation()

    def test_same_data_under_different_id_rejected(self):
        self.i["units"][1]["samples"] = self.i["units"][0]["samples"]
        with self.assertRaisesRegex(ValueError, "DUPLICATE_SAMPLE"):
            self.run_evaluation()

    def test_missing_holdout_rejected(self):
        self.r["decisions"].pop()
        with self.assertRaisesRegex(ValueError, "HOLDOUT_DECISION"):
            self.run_evaluation()

    def test_evidence_class_cannot_be_promoted_by_result(self):
        self.r["evidence_class"] = "REAL_MEASURED"
        with self.assertRaisesRegex(ValueError, "EVIDENCE_CLASS"):
            self.run_evaluation()

    def test_hash_binding_rejected(self):
        self.r["profile_sha256"] = "f"*64
        with self.assertRaisesRegex(ValueError, "HASH_BINDING"):
            self.run_evaluation()

    def test_algorithm_source_mismatch(self):
        self.r["candidate_source_sha256"] = "f"*64
        with self.assertRaisesRegex(ValueError, "SOURCE_MISMATCH"):
            self.run_evaluation()

    def test_run_before_freeze_rejected(self):
        self.r["started_utc"] = self.p["frozen_utc"]
        with self.assertRaisesRegex(ValueError, "PROTOCOL_FREEZE"):
            self.run_evaluation()

    def test_unknown_metric_and_supplied_pass_rejected(self):
        self.r["status"] = "PASS"
        with self.assertRaises(Exception):
            self.run_evaluation()

    def test_json_nan_infinity_and_duplicate_keys_rejected(self):
        for raw in (b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":1e999}', b'{"x":Infinity}'):
            with self.assertRaises(ValueError):
                e.strict_json(raw)

    def test_unsafe_missing_and_corrupted_reference(self):
        for ref in ({"path": "../escape", "sha256": "0"*64},
                    {"path": "missing", "sha256": "0"*64},
                    {"path": "pulse.f32", "sha256": "0"*64}):
            with self.assertRaises(ValueError):
                e.local_file(self.root, ref)

    def test_nonfinite_waveform_rejected(self):
        path = self.root/"bad.f32"
        path.write_bytes(struct.pack("<f", float("nan")))
        with self.assertRaisesRegex(ValueError, "NON_FINITE_SAMPLE"):
            e.samples(path, 1)

    def test_missing_resource_block_rejected(self):
        self.r["resources"]["service_ms"].pop()
        with self.assertRaisesRegex(ValueError, "RESOURCE_BLOCK"):
            self.run_evaluation()

    def test_latency_and_throughput_are_separate_gates(self):
        self.r["resources"]["service_ms"] = [10.0]*6000
        out = self.run_evaluation()
        self.assertEqual(out["status"], "FAIL")
        self.assertEqual(out["gates"]["mean_service"], "FAIL")
        self.assertEqual(out["gates"]["latency"], "PASS")

    def test_missing_preservation_case_rejected(self):
        self.r["preservation"][0]["id"] = "unknown"
        with self.assertRaisesRegex(ValueError, "PRESERVATION_OBSERVATION"):
            self.run_evaluation()

    def test_polarity_loss_is_not_gain_corrected(self):
        values = [0.0]*1024
        values[256] = -.5
        values[257] = .1
        raw = struct.pack("<1024f", *values)
        (self.root/"damaged-pulse.f32").write_bytes(raw)
        self.r["preservation"][0]["output"] = {"path": "damaged-pulse.f32", "sha256": e.digest(raw)}
        out = self.run_evaluation()
        self.assertEqual(out["status"], "FAIL")
        self.assertEqual(out["gates"]["amplitude:impulse"], "FAIL")

    def test_tied_peak_is_ambiguous(self):
        with self.assertRaisesRegex(ValueError, "AMBIGUOUS"):
            e.peak([0, 1, 1, 0], [0, 4])

    def test_not_enough_independent_units_is_not_ready(self):
        self.p["statistics"]["min_positive_units"] = 2
        self.assertEqual(self.run_evaluation()["status"], "NOT_READY")


if __name__ == "__main__":
    unittest.main()
