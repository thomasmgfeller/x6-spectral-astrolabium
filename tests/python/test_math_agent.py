"""Scientific witnesses and fail-closed operating limits, not UI snapshots."""
import copy
import datetime as dt
import json
import os
import random
import re
import tempfile
import textwrap
import unittest
from datetime import timedelta
from fractions import Fraction as F
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

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

    def test_authorised_sunday_and_finite_eight_day_ceiling(self):
        stop = m.parse_time(self.c["stop_utc"])
        self.assertEqual(stop, m.datetime(2026, 10, 19, tzinfo=ZoneInfo("Europe/Zurich")))
        self.assertTrue(m.admitted(self.c, m.parse_time("2026-10-18T18:23:00Z"), 360))
        self.assertFalse(m.admitted(self.c, stop - timedelta(seconds=360), 360))
        self.assertFalse(m.admitted(self.c, stop + timedelta(days=365), 360))
        start = m.parse_time(self.c["start_utc"])
        with tempfile.TemporaryDirectory() as t:
            path = Path(t) / "window.json"
            path.write_text(json.dumps({**self.c, "stop_utc": (start + timedelta(days=8)).isoformat()}))
            m.load_config(path)
            for duration in [timedelta(0), timedelta(seconds=-1), timedelta(days=8, seconds=1)]:
                path.write_text(json.dumps({**self.c, "stop_utc": (start + duration).isoformat()}))
                with self.assertRaises(ValueError):
                    m.load_config(path)

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


class WorkflowWindowTests(unittest.TestCase):
    """Execute the real pre-checkout guards at authorised and forbidden times."""

    def guard(self, filename, now):
        workflow = (m.ROOT / ".github/workflows" / filename).read_text()
        source = textwrap.dedent(workflow.split("          python3 - <<'PY'\n", 1)[1]
                                .split("          PY\n", 1)[0])

        class Clock(dt.datetime):
            @classmethod
            def now(cls, tz=None):
                return now.astimezone(tz)

        with tempfile.TemporaryDirectory() as t:
            output, summary = Path(t) / "output", Path(t) / "summary"
            with patch.object(dt, "datetime", Clock), patch.dict(os.environ, {
                "GITHUB_OUTPUT": str(output), "GITHUB_STEP_SUMMARY": str(summary)
            }):
                exec(compile(source, filename, "exec"), {})
            active = output.read_text() == "active=true\n"
            if not active:
                self.assertIn("STOPPED", summary.read_text())
            return active

    def test_actual_daily_guards_reserve_full_timeout_and_reject_next_year(self):
        start = m.parse_time("2026-10-10T22:26:52Z")
        stop = m.parse_time("2026-10-18T22:00:00Z")
        sunday = m.parse_time("2026-10-18T06:37:00Z")
        for name, reserve in [("x6-data-agent.yml", 15), ("x6-source-agents.yml", 25)]:
            for now, expected in [(start-timedelta(seconds=1), False), (start, True), (sunday, True),
                                  (stop-timedelta(minutes=reserve), True),
                                  (stop-timedelta(minutes=reserve)+timedelta(seconds=1), False),
                                  (stop, False), (sunday.replace(year=2027), False)]:
                with self.subTest(workflow=name, time=now):
                    self.assertEqual(self.guard(name, now), expected)

    def test_cron_includes_sunday_with_existing_cadence(self):
        for name, expected in [("x6-data-agent.yml", "17 6 11-18 10 *"),
                               ("x6-source-agents.yml", "37 6 11-18 10 *"),
                               ("x6-math-agent.yml", "23 */6 11-18 10 *")]:
            source = (m.ROOT / ".github/workflows" / name).read_text()
            self.assertEqual(re.findall(r"cron: '([^']+)'", source), [expected])


if __name__ == "__main__":
    unittest.main()
