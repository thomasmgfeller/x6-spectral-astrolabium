"""Scientific witnesses and fail-closed operating limits, not UI snapshots."""
import copy
import json
import random
import tempfile
import unittest
from datetime import timedelta
from fractions import Fraction as F
from pathlib import Path

from agent import run_math_agent as m
from agent.run_agent import lower_holds


class MathAgentTests(unittest.TestCase):
    def setUp(self):
        self.c = m.load_config(m.DEFAULT_CONFIG)

    def budget(self):
        c = copy.deepcopy(self.c)
        c["stop_utc"] = (m.datetime.now(m.timezone.utc)+timedelta(minutes=5)).isoformat()
        return m.Budget(c)

    def test_admission_boundaries_and_kill_switch(self):
        start, stop = m.parse_time(self.c["start_utc"]), m.parse_time(self.c["stop_utc"])
        self.assertFalse(m.admitted(self.c, start-timedelta(seconds=1)))
        self.assertTrue(m.admitted(self.c, start))
        self.assertFalse(m.admitted(self.c, stop))
        self.assertFalse(m.admitted(self.c, stop-timedelta(seconds=90)))
        self.assertFalse(m.admitted({**self.c, "enabled": False}, start))

    def test_invalid_extended_window_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t)/"bad.json"
            for patch in [{"stop_utc": "2030-01-01T00:00:00Z"}, {"max_seconds": 10000},
                          {"cases_per_track": 100000}, {"enabled": "true"},
                          {"seed": True}, {"start_utc": "2026-10-11T08:13:02"}]:
                p.write_text(json.dumps({**self.c, **patch}))
                with self.assertRaises(ValueError):
                    m.load_config(p)

    def test_expired_run_never_claims_pass(self):
        c = {**self.c, "start_utc": "2020-01-01T00:00:00Z", "stop_utc": "2020-01-02T00:00:00Z"}
        with tempfile.TemporaryDirectory() as t:
            out = Path(t)/"run"
            self.assertEqual(m.run(c, out), 0)
            report = json.loads((out/"report.json").read_text())
            self.assertEqual(report["status"], "STOPPED")
            self.assertEqual(report["tracks"], {})

    def test_mapping_collision_is_not_global_sign(self):
        x, y = [0, 1, 2], [0, 1, 0]
        self.assertEqual(m.squared_increments(x), m.squared_increments(y))
        self.assertNotEqual(x, y)
        self.assertNotEqual(x, [-v for v in y])
        # Three nonzero edges give 8 sign patterns, 4 modulo a global sign.
        walks = {tuple(m.walk(list(s))) for s in m.itertools.product([-1, 1], repeat=3)}
        self.assertEqual(len(walks), 8)

    def test_exact_schur_rejects_equality_and_too_high(self):
        L = m.laplacian(2, [(0, 1, F(1, 8))])
        for b, expected in [(F(1, 5), True), (F(1, 4), False), (F(1), False)]:
            self.assertEqual(m.strict_lower(L, b), expected)
            self.assertEqual(m.strict_lower(L, b), lower_holds(L, b))
        self.assertFalse(m.strict_lower(m.laplacian(3, [(0, 1, F(1))]), F(0)))

    def test_perturbation_factor_two_is_necessary(self):
        a = m.laplacian(2, [(0, 1, F(1))])
        b = m.laplacian(2, [(0, 1, F(11, 10))])
        # For two vertices the nonzero eigenvalue equals trace(L), exactly.
        change = sum(b[i][i]-a[i][i] for i in range(2))
        self.assertEqual(change, F(1, 5))
        self.assertGreater(change, F(1, 10))
        self.assertEqual(change, 2*F(1, 10))

    def test_actual_core_witnesses(self):
        functions, mapping = m.core_functions((m.ROOT/"app/index.html").read_text())
        r = m.mapping_track(random.Random(7), 8, mapping, self.budget())
        self.assertEqual(r["finding"], "FALSIFIED_EXACT_WITNESS")
        p = m.phase_track(random.Random(9), 8, functions, self.budget())
        self.assertAlmostEqual(p["analytically_explained_control"]["relative_equivariance_defect"], 1, places=10)
        q = m.perturbation_track(random.Random(3), 8, self.budget())
        self.assertEqual(q["finding"], "FALSIFIED_EXACT_WITNESS")
        self.assertTrue(all(x["factor_two_exact_transfer"] for x in q["records"]))

    def test_budget_failure(self):
        budget = self.budget()
        budget.end = m.time.monotonic()-1
        with self.assertRaises(TimeoutError):
            budget.check()

    def test_extractor_fails_on_changed_structure(self):
        with self.assertRaises((ValueError, KeyError)):
            m.core_functions("<html>not the audited application</html>")


if __name__ == "__main__":
    unittest.main()
