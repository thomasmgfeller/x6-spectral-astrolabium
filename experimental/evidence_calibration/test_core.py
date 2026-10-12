import tempfile
import unittest
from pathlib import Path

from experimental.evidence_calibration.core import (
    evidence_record, parameter_sweep, sha256_file, summarize_replicates, verify_record
)


class EvidenceCalibrationTests(unittest.TestCase):
    def test_integrity_and_replay(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "sample.bin"
            p.write_bytes(b"reproducible")
            kwargs = dict(input_path=p, software_sha256="a"*64,
                          parameters={"threshold": 3}, results={"count": 7},
                          uncertainty={"count": "not estimated"}, source="fixture")
            record = evidence_record(**kwargs)
            self.assertEqual(record, evidence_record(**kwargs))
            self.assertTrue(verify_record(record, p))
            record["results"]["count"] = 8
            self.assertFalse(verify_record(record, p))
            record = evidence_record(**kwargs)
            p.write_bytes(b"changed")
            self.assertFalse(verify_record(record, p))

    def test_sweep(self):
        fn = lambda p: {"value": p["a"] + p["b"]}
        rows = parameter_sweep({"b": [2, 3], "a": [1]}, fn)
        self.assertEqual([r["result"]["value"] for r in rows], [3, 4])

    def test_replicates(self):
        self.assertEqual(summarize_replicates([1, 2, 3])["mean"], 2)
        self.assertIsNone(summarize_replicates([3])["standard_error"])
        with self.assertRaises(ValueError):
            summarize_replicates([float("nan")])


if __name__ == "__main__":
    unittest.main()
