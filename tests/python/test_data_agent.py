"""Agent gates: stale/malformed data and forged certificates must not pass."""
import copy
import json
import unittest
from datetime import datetime, timedelta, timezone
from fractions import Fraction as F

from agent.run_agent import prepare_samples, verify_certificate, matrix_from_edges, lower_holds


class DataAgentTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 10, 22, 0, tzinfo=timezone.utc)
        self.rows = [{"time_tag": (self.now - timedelta(minutes=127-i)).isoformat(),
                      "satellite": 18, "energy": "0.1-0.8nm",
                      "electron_contaminaton": False, "flux": 1e-6 * (1 + i/128)}
                     for i in range(128)]

    def prepare(self, rows=None, **kwargs):
        return prepare_samples(json.dumps(self.rows if rows is None else rows).encode(),
                               now=kwargs.pop("now", self.now), **kwargs)

    def test_valid_data_has_reproducible_transform_and_provenance(self):
        prepared = self.prepare()
        self.assertEqual(prepared["sample_count"], 128)
        self.assertAlmostEqual(sum(prepared["values"]), 0, places=9)
        self.assertEqual(prepared["satellite"], 18)
        self.assertEqual(len(prepared["observations"]), 128)

    def test_stale_rejected_and_explicit_replay_distinguished(self):
        future = self.now + timedelta(days=1)
        with self.assertRaisesRegex(ValueError, "stale"):
            self.prepare(now=future)
        self.assertGreater(self.prepare(now=future, replay=True)["age_seconds_at_selection"], 7200)

    def test_gap_not_interpolated(self):
        with self.assertRaisesRegex(ValueError, "contiguous"):
            self.prepare(self.rows[:60] + self.rows[61:])

    def test_bad_measurements_and_satellite_switch_are_not_accepted(self):
        for field, value in [("flux", -1), ("flux", float("nan")),
                             ("electron_contaminaton", True),
                             ("electron_contaminaton", None), ("satellite", 19)]:
            rows = copy.deepcopy(self.rows)
            rows[64][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.prepare(rows)

    def test_future_dated_window_rejected(self):
        with self.assertRaisesRegex(ValueError, "future"):
            self.prepare(now=self.now - timedelta(hours=1))

    def test_exact_verifier_rejects_altered_bound_witness_and_source(self):
        source = "a b 1\nb c 1\nc d 1"
        certificate = {"source": source, "scope": "connected-undirected-positive-rational-weights",
                       "strictLower": "1/2", "upperBound": "1/1", "strictLowerCertified": True,
                       "upperWitnessPair": ["a", "d"],
                       "searchTrace": [{"bound": "1/2", "positiveDefinite": True},
                                       {"bound": "3/5", "positiveDefinite": False}]}
        self.assertEqual(verify_certificate(certificate, source)["status"], "PASS")
        for key, value in [("strictLower", "3/5"), ("upperBound", "1/4"),
                           ("upperWitnessPair", ["a", "b"]), ("source", "a b 1")]:
            tampered = copy.deepcopy(certificate)
            tampered[key] = value
            with self.subTest(field=key), self.assertRaises(ValueError):
                verify_certificate(tampered, source)
        tampered = copy.deepcopy(certificate)
        tampered["searchTrace"][1]["positiveDefinite"] = True
        with self.assertRaisesRegex(ValueError, "search trace"):
            verify_certificate(tampered, source)

    def test_equality_and_disconnected_graphs_rejected(self):
        _, L = matrix_from_edges("a b 0.125")
        self.assertTrue(lower_holds(L, F(1, 8)))
        self.assertFalse(lower_holds(L, F(1, 4)))
        with self.assertRaisesRegex(ValueError, "Disconnected"):
            matrix_from_edges("a b 1\nc d 1")


if __name__ == "__main__":
    unittest.main()
