import tempfile
import unittest
from pathlib import Path
from experimental.evidence_calibration.recorded import load_frame_csv,compare_recorded_frames

class RecordedTests(unittest.TestCase):
    def test_known_translation(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/"a.csv";b=Path(d)/"b.csv"
            a.write_text("0,0,0\n0,10,0\n0,0,0\n")
            b.write_text("0,0,0\n0,0,10\n0,0,0\n")
            m=dict(instrument_id="fixture",pixel_pitch_um=2,acquired_utc="2026-10-12T00:00:00Z",calibration_id="not-verified",evidence_class="SYNTHETIC",coordinate_plane="synthetic_grid",scale_model="effective_isotropic_um_per_input_pixel")
            result=compare_recorded_frames(a,b,m)
            self.assertEqual(result["status"],"SYNTHETIC_RESULT")
            self.assertEqual(result["drift_um"],2)
            self.assertEqual(compare_recorded_frames(a,b,{})["status"],"UNQUALIFIED_METADATA")
            b.write_text("0,0\n0,0\n")
            with self.assertRaises(ValueError):compare_recorded_frames(a,b,m)
    def test_reject_corrupt(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"bad.csv"
            for s in ("1,NaN\n","1,2\n3\n","1,\n",""):
                p.write_text(s)
                with self.assertRaises(ValueError):load_frame_csv(p)

if __name__=="__main__":unittest.main()
