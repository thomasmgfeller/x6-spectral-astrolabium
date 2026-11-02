import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from agent import nicer


class NicerTests(unittest.TestCase):
    def test_gaps_energy_edges_and_partial_exposure(self):
        # Four GTIs include a partial bin, two within one bin, an empty bin and a measured zero.
        curve = nicer.lightcurve(np.array([9, 10, 12, 20, 24, 25, 26, 30, 138, 145]),
                                 np.array([30, 30, 299, 30, 30, 29, 300, 30, 31, 30]),
                                 np.array([10, 24, 138, 202]), np.array([20, 30, 145, 210]))
        self.assertEqual(curve["bins"], [[0, 3, 16], [2, 1, 7], [3, 0, 8]])
        self.assertEqual(curve["band_events_outside_gti"], 4)
        self.assertEqual(curve["counts"], 4)
        self.assertEqual(curve["gti_s"], 31)

    def test_overlapping_gtis_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid GTIs"):
            nicer.lightcurve(np.array([]), np.array([]), np.array([0, 2]), np.array([3, 4]))

    def test_no_reimport_or_partial_publication(self):
        row = {"obsid": "1060020101", "revision": ["1", "test"]}
        rec = {"date_obs": "2017-07-24", "counts": 0, "gti_s": 1}
        with tempfile.TemporaryDirectory() as tmp, patch.object(nicer, "catalog", return_value=[row]):
            path = Path(tmp)
            with patch.object(nicer, "acquire", return_value=rec) as acquire:
                nicer.archive_next(path)
                first = (path / "index.json").read_bytes()
                nicer.archive_next(path)
                self.assertEqual(acquire.call_count, 1)
                self.assertEqual(first, (path / "index.json").read_bytes())
            row["revision"] = ["2", "new"]
            with patch.object(nicer, "acquire", side_effect=RuntimeError("interrupted")):
                with self.assertRaises(RuntimeError):
                    nicer.archive_next(path)
            self.assertEqual(first, (path / "index.json").read_bytes())

    def test_real_reference(self):
        seed = Path(__file__).resolve().parents[2] / "app/causal-stability/nicer-data"
        entry = json.loads((seed / "index.json").read_text())["entries"][0]
        raw = (seed / entry["file"]).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"])
        r = json.loads(raw)
        self.assertEqual(r["source"]["sha256_gzip"],
                         "9719a4e59a3c7f1875db65ef150ac4ef4fe10132441b0869fb7770c811cc2ecf")
        self.assertEqual((r["counts"], r["gti_count"], r["gti_s"], r["span_s"]), (1003, 15, 1162, 12037))
        self.assertEqual(sum(b[1] for b in r["bins"]), r["counts"])
        self.assertEqual(sum(b[2] for b in r["bins"]), r["gti_s"])


if __name__ == "__main__":
    unittest.main()
