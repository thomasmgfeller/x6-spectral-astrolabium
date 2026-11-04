"""Cross-domain input tests using the existing capture and a Stim development shot."""
import base64
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from research.x6_qed.c0_input import ShotInputError, decode_shot


class QedInputTests(unittest.TestCase):
    def setUp(self):
        fixture = json.loads(Path(__file__).with_name("fixtures").joinpath("qed_d5_single_fault.json").read_text())
        graph = fixture["graph"]
        serial = json.dumps(graph, sort_keys=True, separators=(",", ":")).encode()
        self.sha = hashlib.sha256(serial).hexdigest()
        self.count = graph["detector_count"]
        self.shot = fixture["shot"]
        self.infer = Mock(return_value=object())

    def dispatch(self, payload):
        return decode_shot(payload, graph_sha256=self.sha, detector_count=self.count, infer=self.infer)

    def assert_rejected(self, payload):
        with self.assertRaises(ShotInputError):
            self.dispatch(payload)
        self.infer.assert_not_called()

    def test_stim_shot_reaches_inference_with_detector_bits_only(self):
        self.assertEqual(self.count, 120)
        expected = tuple(int(i == 108) for i in range(self.count))
        self.assertIs(self.dispatch(self.shot), self.infer.return_value)
        self.infer.assert_called_once_with(expected)

    def test_rejects_foreign_graph_of_same_size(self):
        self.assert_rejected({**self.shot, "frozen_graph_sha256": "0" * 64})

    def test_rejects_sagnac_capture_and_decoded_evidence(self):
        capture = ROOT / "device/fixtures/synthetic_chsh_capture.bin"
        self.assert_rejected(capture.read_bytes())
        script = """const fs = require('node:fs');
const core = require('./app/sagnac-core.js');
const result = core.decode(fs.readFileSync(process.argv[1]), 'synthetic', '100');
process.stdout.write(JSON.stringify(result));"""
        evidence = json.loads(subprocess.check_output(["node", "-e", script, str(capture)], cwd=ROOT))
        self.assertEqual(evidence["schema"], "x6.sagnac.evidence/1")
        self.assertEqual(len(evidence["records"]), 4)
        self.assert_rejected(evidence)
        raw = capture.read_bytes()
        export = {**evidence, "input": {"mode": "file", "bytes": len(raw),
                  "expected_first_sequence": "100", "sha256": hashlib.sha256(raw).hexdigest(),
                  "raw_base64": base64.b64encode(raw).decode("ascii")}}
        self.assert_rejected(export)

    def test_rejects_missing_extra_and_evaluation_fields(self):
        self.assert_rejected({k: v for k, v in self.shot.items() if k != "detector_bits"})
        self.assert_rejected({**self.shot, "observable_flips": [1]})
        self.assert_rejected({**self.shot, "schema": "x6.qed.detector-shot/2"})

    def test_rejects_invalid_binary_vectors(self):
        invalid = [[], [0] * 119, [0] * 121, "0" * 120]
        invalid.extend([0] * 119 + [v] for v in (True, 0.0, -1, 2, "1", None))
        for bits in invalid:
            with self.subTest(bits=bits):
                self.assert_rejected({**self.shot, "detector_bits": bits})

    def test_all_zero_shot_reaches_inference(self):
        self.dispatch({**self.shot, "detector_bits": [0] * self.count})
        self.infer.assert_called_once_with((0,) * self.count)


if __name__ == "__main__":
    unittest.main()
