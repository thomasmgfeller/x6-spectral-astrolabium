"""Stricter audit criteria, intentionally not the repository's original contract.
A failure is a demonstrated gap against the stated criterion, not an invented
failure of the upstream CI. Regression of the 2026-10-12 audit. A07 injects at the new byte-snapshot seam; the scientific criterion is unchanged.
"""
import copy, hashlib, json, math, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from experimental.evidence_calibration import core, optical, recorded
from experimental.evidence_calibration.boundary import evaluate_boundary

class ScientificAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.a=Path(self.tmp.name)/'reference.csv'
        self.b=Path(self.tmp.name)/'sample.csv'
        self.a.write_text('10,0,0\n',encoding='utf-8')
        self.b.write_text('0,10,0\n',encoding='utf-8')
        self.meta=dict(instrument_id='FIXTURE-NOT-PHYSICAL',pixel_pitch_um=2.0,
            acquired_utc='2026-10-12T00:00:00Z',calibration_id='UNVERIFIED-FIXTURE',evidence_class='SYNTHETIC',
            coordinate_plane='synthetic_grid',scale_model='effective_isotropic_um_per_input_pixel')
        self.gate=dict(sample_count=10,minimum_samples=10,baseline=1.0,
            candidate=0.5,tolerance=0.0,calibration_valid=True,data_integrity=True)

    def require_invalid_or_rejected(self,fn):
        try: result=fn()
        except (ValueError,TypeError): return
        self.assertIn(result.get('status'),('REJECT','INVALID_INPUT','UNQUALIFIED_METADATA'),str(result))

    def test_A01_text_false_must_not_authorize(self):
        args=dict(self.gate,calibration_valid='false',data_integrity='false')
        self.require_invalid_or_rejected(lambda:evaluate_boundary(**args))

    def test_A02_nonboolean_truthy_values_must_not_authorize(self):
        args=dict(self.gate,calibration_valid=1,data_integrity=['false'])
        self.require_invalid_or_rejected(lambda:evaluate_boundary(**args))

    def test_A03_nan_threshold_must_not_be_no_signal(self):
        self.require_invalid_or_rejected(lambda:optical.frame_metrics([[10]],threshold=math.nan))

    def test_A04_ok_optical_metrics_must_be_finite(self):
        # Finite input and representable centroid x=2; intermediate overflow must
        # be prevented or rejected, not converted into an OK result with infinity.
        try: result=optical.frame_metrics([[0,0,1e308]])
        except (ValueError,OverflowError): return
        self.assertFalse(result.get('status')=='OK' and
            any(isinstance(v,float) and not math.isfinite(v) for v in result.values()),str(result))

    def test_A05_timestamp_must_be_valid_utc_not_just_present(self):
        meta=dict(self.meta,acquired_utc='not-a-timestamp')
        self.require_invalid_or_rejected(lambda:recorded.compare_recorded_frames(self.a,self.b,meta))

    def test_A06_boolean_pixel_pitch_must_not_be_length(self):
        meta=dict(self.meta,pixel_pitch_um=True)
        self.require_invalid_or_rejected(lambda:recorded.compare_recorded_frames(self.a,self.b,meta))

    def test_A07_provenance_hash_must_bind_bytes_actually_analyzed(self):
        original_loader=recorded.read_snapshot
        original_hash=core.sha256_file(self.b)
        def changing_loader(path):
            frame=original_loader(path)
            if Path(path)==self.b:
                self.b.write_text('0,0,10\n',encoding='utf-8')
            return frame
        with patch.object(recorded,'read_snapshot',side_effect=changing_loader) as loader:
            result=recorded.compare_recorded_frames(self.a,self.b,self.meta)
        self.assertEqual(loader.call_count,2)
        self.assertEqual(self.b.read_text(), '0,0,10\n')
        self.assertEqual(result['drift_pixels'],1.0) # original bytes were used
        self.assertEqual(result['sample_sha256'],original_hash,
            'Reported drift was computed from old bytes, but hash identifies new bytes')

    def test_A08_evidence_record_must_snapshot_nested_input(self):
        params={'nested':{'threshold':1}}
        rec=core.evidence_record(input_path=self.a,software_sha256='a'*64,
            parameters=params,results={'x':0},uncertainty={},source='SIMULATION fixture')
        params['nested']['threshold']=2
        self.assertEqual(rec['parameters']['nested']['threshold'],1,
            'Caller mutation silently changes already-created evidence record')

    def test_A09_wrong_container_types_must_not_be_valid_metadata(self):
        meta=dict(self.meta,instrument_id=[],calibration_id={})
        self.require_invalid_or_rejected(lambda:recorded.compare_recorded_frames(self.a,self.b,meta))

    def test_A10_record_verification_must_also_enforce_schema(self):
        # Critically: a raw content checksum alone does not validate the schema.
        record={'input_sha256':core.sha256_file(self.a)}
        record['record_sha256']=hashlib.sha256(core.canonical_json_bytes(record)).hexdigest()
        self.assertFalse(core.verify_record(record,self.a),
            'Checksum verifies despite absent schema, software provenance and results')

if __name__=='__main__':
    unittest.main(verbosity=2)
