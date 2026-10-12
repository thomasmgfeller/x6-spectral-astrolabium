"""Additional negative controls and contract tests; no physical instruments."""
import hashlib
import json
import math
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from . import core, optical, recorded
from .boundary import evaluate_boundary
from .validation import read_snapshot, json_snapshot


class HardeningTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.a = Path(tmp.name) / "a.csv"
        self.b = Path(tmp.name) / "b.csv"
        self.a.write_bytes(b"10,0,0\n")
        self.b.write_bytes(b"0,10,0\n")
        self.meta = dict(instrument_id="fixture", pixel_pitch_um=2.0,
                        acquired_utc="2026-10-12T00:00:00Z", calibration_id="unverified",
                        evidence_class="SYNTHETIC", coordinate_plane="synthetic_grid",
                        scale_model="effective_isotropic_um_per_input_pixel")

    def test_all_invalid_gate_flag_types(self):
        params = dict(sample_count=10, minimum_samples=10, baseline=1, candidate=0,
                      tolerance=0, calibration_valid=True, data_integrity=True)
        for key in ("calibration_valid", "data_integrity"):
            for value in ("false", "true", 0, 1, [], [True], {}, None):
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    evaluate_boundary(**dict(params, **{key: value}))

    def test_gate_numeric_range_and_direction(self):
        params = dict(sample_count=10, minimum_samples=10, baseline=1, candidate=0,
                      tolerance=0, calibration_valid=True, data_integrity=True)
        for key in ("baseline", "candidate", "tolerance"):
            for value in (True, "1", math.nan, math.inf, -math.inf):
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    evaluate_boundary(**dict(params, **{key: value}))
        with self.assertRaises(ValueError):
            evaluate_boundary(**dict(params, baseline=-1e308, candidate=1e308))
        self.assertEqual(evaluate_boundary(**params)["metric_direction"], "lower_is_better")

    def test_threshold_invalid_values(self):
        for value in (True, "1", None, -1, math.nan, math.inf):
            with self.subTest(value=value), self.assertRaises(ValueError):
                optical.frame_metrics([[1]], value)

    def test_intensity_invalid_types(self):
        for value in (True, "1", None, -1, math.nan, math.inf, 10**400):
            with self.subTest(value=value), self.assertRaises(ValueError):
                optical.frame_metrics([[value]])

    def test_representable_large_centroid_and_total_overflow(self):
        result = optical.frame_metrics([[0, 0, 1e308]])
        self.assertEqual(result["centroid_x"], 2)
        self.assertEqual(result["sigma_x"], 0)
        with self.assertRaises(ValueError):
            optical.frame_metrics([[1e308, 1e308]])

    def test_no_signal_and_different_shapes(self):
        self.assertEqual(optical.frame_metrics([[0]])["status"], "NO_SIGNAL")
        with self.assertRaises(ValueError):
            optical.centroid_drift([[1]], [[1, 0]])

    def test_dates_types_and_explicit_utc(self):
        for value in ("nonsense", "2026-02-30T00:00:00Z", "2026-10-12",
                      "2026-10-12T00:00:00", "2026-10-12T02:00:00+02:00", True, []):
            with self.subTest(value=value), self.assertRaises(ValueError):
                recorded.compare_recorded_frames(self.a, self.b, dict(self.meta, acquired_utc=value))
        result = recorded.compare_recorded_frames(self.a, self.b,
            dict(self.meta, acquired_utc="2026-10-12T00:00:00.123+00:00"))
        self.assertEqual(result["status"], "SYNTHETIC_RESULT")

    def test_legacy_metadata_does_not_claim_measurement(self):
        for key in ("evidence_class", "coordinate_plane", "scale_model"):
            meta = dict(self.meta)
            del meta[key]
            self.assertEqual(recorded.compare_recorded_frames(self.a, self.b, meta)["status"],
                             "UNQUALIFIED_METADATA")

    def test_explicit_unverified_recorded_class(self):
        out = recorded.compare_recorded_frames(self.a, self.b,
                    dict(self.meta, evidence_class="RECORDED_UNVERIFIED", coordinate_plane="sensor"))
        self.assertEqual(out["status"], "UNVERIFIED_MEASUREMENT")
        self.assertEqual(out["calibration_status"], "UNVERIFIED")
        self.assertEqual(out["measurement_uncertainty"], "NOT_EVALUATED")

    def test_no_inferred_scale_or_class(self):
        for key, value in (("scale_model", "sensor_pitch_without_resizing"),
                           ("evidence_class", "VALIDATED"), ("pixel_pitch_um", True),
                           ("pixel_pitch_um", 0), ("coordinate_plane", " ")):
            with self.subTest(key=key), self.assertRaises(ValueError):
                recorded.compare_recorded_frames(self.a, self.b, dict(self.meta, **{key: value}))

    def test_scaled_displacement_overflow(self):
        self.b.write_bytes(b"0,0,10\n")
        with self.assertRaises(ValueError):
            recorded.compare_recorded_frames(self.a, self.b, dict(self.meta, pixel_pitch_um=1e308))

    def test_csv_invalid_bytes_and_fields(self):
        for value in (b"\xff", b'"1,2\n', b"1,\n", b"1,NaN\n", b"1,inf\n", b"-1\n", b"\n"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                recorded.parse_frame_bytes(value)

    def test_snapshot_read_bound(self):
        with patch("experimental.evidence_calibration.validation.MAX_BYTES", 2):
            with self.assertRaises(ValueError):
                read_snapshot(self.a)

    def test_background_not_automatically_physical_drift(self):
        self.assertEqual(optical.centroid_drift([[10,0,0]], [[20,10,10]])["drift_pixels"], .75)
        out = recorded.compare_recorded_frames(self.a, self.b, self.meta)
        self.assertIn("background", out["caveat"])

    def test_record_rejects_bad_schema_even_rehashed(self):
        rec = core.evidence_record(input_path=self.a, software_sha256="a"*64,
            parameters={}, results={}, uncertainty={}, source="fixture")
        for key, value in (("schema", "made-up"), ("software_sha256", "x"*64),
                           ("parameters", []), ("status", "VALIDATED"), ("source", "")):
            altered = dict(rec, **{key: value})
            altered.pop("record_sha256")
            altered["record_sha256"] = hashlib.sha256(core.canonical_json_bytes(altered)).hexdigest()
            self.assertFalse(core.verify_record(altered, self.a))

    def test_record_malformed_or_missing_input_returns_false(self):
        for value in (None, [], {}, {"record_sha256": math.nan}):
            self.assertFalse(core.verify_record(value, self.a))
        rec = core.evidence_record(input_path=self.a, software_sha256="a"*64,
            parameters={}, results={}, uncertainty={}, source="fixture")
        self.a.unlink()
        self.assertFalse(core.verify_record(rec, self.a))

    def test_no_claim_of_authenticity(self):
        rec = core.evidence_record(input_path=self.a, software_sha256="a"*64,
            parameters={}, results={"arbitrary": 1}, uncertainty={}, source="fixture")
        rec["results"]["arbitrary"] = 2
        rec.pop("record_sha256")
        rec["record_sha256"] = hashlib.sha256(core.canonical_json_bytes(rec)).hexdigest()
        # Expected: an untrusted caller can rehash. This is NOT authentication.
        self.assertTrue(core.verify_record(rec, self.a))

    def test_json_forbids_coercions_and_cycles(self):
        cycle = []; cycle.append(cycle)
        for value in ({1: "x"}, (1,2), {"x": math.nan}, {"x": float("inf")}, cycle):
            with self.subTest(kind=type(value).__name__), self.assertRaises(ValueError):
                json_snapshot(value)

    def test_sweep_callback_cannot_mutate_archived_parameters(self):
        grid = {"a": [{"x": 1}]}
        def callback(p):
            p["a"]["x"] = 9
            return {"done": True}
        rows = core.parameter_sweep(grid, callback)
        self.assertEqual(rows[0]["parameters"]["a"]["x"], 1)
        self.assertEqual(grid["a"][0]["x"], 1)

    def test_sweep_bound(self):
        with self.assertRaises(ValueError):
            core.parameter_sweep({"a": list(range(101)), "b": list(range(100))}, lambda p: {})

    def test_statistics_invalid_and_large(self):
        for value in (True, "1", math.nan, math.inf, 10**400):
            with self.subTest(value=value), self.assertRaises(ValueError):
                core.summarize_replicates([value])
        self.assertEqual(core.summarize_replicates([1e308,1e308])["mean"], 1e308)
        with self.assertRaises(ValueError):
            core.summarize_replicates([-1.7e308, 1.7e308])
