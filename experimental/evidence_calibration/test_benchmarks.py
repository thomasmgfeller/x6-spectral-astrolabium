"""Reproducible synthetic fixtures and explicit uncertainty/negative gates."""
import math
import unittest
from experimental.evidence_calibration.core import parameter_sweep, summarize_replicates
from experimental.evidence_calibration.optical import frame_metrics, centroid_drift
from experimental.evidence_calibration.boundary import evaluate_boundary
from experimental.evidence_calibration.ecc import encode_hamming74, decode_hamming74

class BenchmarkFixtures(unittest.TestCase):
    def test_optical_translation_baseline(self):
        reference=[[0,0,0,0],[0,10,0,0],[0,0,0,0]]
        shifted=[[0,0,0,0],[0,0,10,0],[0,0,0,0]]
        self.assertEqual(centroid_drift(reference, shifted)["drift_pixels"],1)
        self.assertEqual(frame_metrics(reference)["sigma_y"],0)

    def test_no_signal_is_not_zero_drift(self):
        result=centroid_drift([[0]],[[10]])
        self.assertEqual(result["status"],"INSUFFICIENT_SIGNAL")
        self.assertIsNone(result["drift_pixels"])

    def test_repeatability_and_uncertainty(self):
        rows=parameter_sweep({"threshold":[0,5,10]},lambda p:{"observed":max(0,10-p["threshold"])})
        self.assertEqual([r["result"]["observed"] for r in rows],[10,5,0])
        summary=summarize_replicates([1.0,2.0,3.0])
        self.assertAlmostEqual(summary["sample_sd"],1)
        self.assertAlmostEqual(summary["standard_error"],1/math.sqrt(3))
        self.assertIsNone(summarize_replicates([1.0])["sample_sd"])

    def test_negative_boundary_gates(self):
        p=dict(sample_count=10,minimum_samples=10,baseline=1,candidate=1,tolerance=0,
               calibration_valid=True,data_integrity=True)
        self.assertEqual(evaluate_boundary(**p)["status"],"PASS")
        for key,value in [("sample_count",9),("calibration_valid",False),
                          ("data_integrity",False),("candidate",2)]:
            q=dict(p);q[key]=value
            self.assertEqual(evaluate_boundary(**q)["status"],"REJECT")

    def test_ecc_no_double_error_guarantee(self):
        # A nonzero syndrome alone does not prove one-bit corruption.
        word=encode_hamming74([1,0,1,0])
        word[0]^=1;word[1]^=1
        outcome=decode_hamming74(word)
        self.assertEqual(outcome["status"],"CORRECTED_OR_UNDETECTED_MULTI_ERROR")
        self.assertNotEqual(outcome["data"],[1,0,1,0])

if __name__=="__main__": unittest.main()
