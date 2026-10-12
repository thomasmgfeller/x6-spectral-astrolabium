import unittest
from experimental.evidence_calibration.optical import frame_metrics,centroid_drift
from experimental.evidence_calibration.ecc import encode_hamming74,decode_hamming74,exhaustive_single_error_check
from experimental.evidence_calibration.boundary import evaluate_boundary

class TestOptics(unittest.TestCase):
    def test_centroid(self):
        m=frame_metrics([[0,0,0],[0,2,0],[0,0,0]])
        self.assertEqual((m["centroid_x"],m["centroid_y"],m["sigma_x"]),(1,1,0))
        self.assertEqual(centroid_drift([[1,0]],[[0,1]])["drift_pixels"],1)
    def test_invalid(self):
        with self.assertRaises(ValueError): frame_metrics([[1],[1,2]])
        with self.assertRaises(ValueError): frame_metrics([[float("nan")]])
        self.assertEqual(frame_metrics([[0]])["status"],"NO_SIGNAL")

class TestECC(unittest.TestCase):
    def test_exhaustive(self):
        self.assertEqual(exhaustive_single_error_check()["cases"],128)
        self.assertTrue(exhaustive_single_error_check()["passed"])
    def test_invalid(self):
        with self.assertRaises(ValueError): encode_hamming74([0,1,2,1])
        with self.assertRaises(ValueError): decode_hamming74([0]*6)

class TestBoundary(unittest.TestCase):
    def test_fail_closed(self):
        p=dict(sample_count=20,minimum_samples=10,baseline=0.2,candidate=0.1,tolerance=0,calibration_valid=True,data_integrity=True)
        self.assertEqual(evaluate_boundary(**p)["status"],"PASS")
        p["data_integrity"]=False
        self.assertEqual(evaluate_boundary(**p)["status"],"REJECT")
        p["data_integrity"]=True;p["candidate"]=0.3
        self.assertIn("BASELINE_NOT_MET",evaluate_boundary(**p)["reasons"])

if __name__=="__main__": unittest.main()
