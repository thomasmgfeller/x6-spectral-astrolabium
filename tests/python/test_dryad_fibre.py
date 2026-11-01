import hashlib
import math
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.request import Request

import h5py
import numpy as np

from agent import dryad_fibre as fibre


class FibreTests(unittest.TestCase):
    def test_axes_and_independent_complex_sum(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)/"tiny.h5"
            with h5py.File(p,"w") as f:
                f["T1"] = np.array([[1j,2],[100,500]],complex)
                f["T2"] = np.array([[2,1j],[43,23j]],complex)
            m = fibre.extract(p)
            self.assertEqual(m["channels"]["T1"]["coefficients"], [[0,1],[2,0]])
            for angle in (-180,-10,0,10,180):
                r = fibre.response(m,angle)
                # For these coefficients the T1 and T2 interference terms have opposite signs.
                self.assertAlmostEqual(r["T1_intensity"],2.5-2*math.cos(math.radians(angle)))
                self.assertAlmostEqual(r["T2_intensity"],2.5+2*math.cos(math.radians(angle)))
                self.assertAlmostEqual(r["total_intensity"],5)

    def test_redirect_does_not_forward_bearer(self):
        request = Request(fibre.api(fibre.FILE+"/download"),headers={"Authorization":"Bearer example"})
        redir = fibre.SafeRedirect().redirect_request(request,None,302,"",{}, "https://example.org/blob")
        self.assertFalse(redir.has_header("Authorization"))
        with self.assertRaises(ValueError):
            fibre.SafeRedirect().redirect_request(request,None,302,"",{}, "http://example.org/blob")

    def test_archiving_is_idempotent_and_preserves_verified_state(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td); path=base/"source.h5"; out=base/"archive"; cache=base/"cache"
            with h5py.File(path,"w") as f:
                f["T1"]=np.ones((2,2),complex); f["T2"]=np.array([[1j,2],[2,3]],complex)
            sha=hashlib.sha256(path.read_bytes()).hexdigest()
            with patch.object(fibre,"SIZE",path.stat().st_size), patch.object(fibre,"DIGEST",sha), \
                 patch.object(fibre,"source",return_value={"sha256":sha,"download_url":fibre.api(fibre.FILE+"/download")}):
                self.assertEqual(fibre.sync(out,cache,metadata_only=True),"METADATA_ONLY")
                self.assertEqual(fibre.sync(out,cache,local=path),"VERIFIED_MATRIX_SLICE")
                original=(out/"record.json").read_bytes()
                self.assertEqual(fibre.sync(out,cache,metadata_only=True),"VERIFIED_MATRIX_SLICE")
                bad=base/"bad.h5";bad.write_bytes(b"X"*path.stat().st_size)
                with self.assertRaisesRegex(ValueError,"SHA-256"):
                    fibre.sync(out,cache,local=bad)
                self.assertEqual(original,(out/"record.json").read_bytes())

    def test_bad_matrix_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"bad.h5"
            with h5py.File(p,"w") as f:
                f["T1"]=np.zeros((1,2),complex); f["T2"]=np.zeros((1,2),complex)
            with self.assertRaisesRegex(ValueError,"phase reference"):
                fibre.response(fibre.extract(p),0)
            with h5py.File(p,"r+") as f: f["T2"][0,1]=complex(float("nan"))
            with self.assertRaisesRegex(ValueError,"nonfinite"): fibre.extract(p)

    def test_published_result_replays(self):
        import json
        record = json.loads((fibre.DEFAULT_ARCHIVE/"record.json").read_bytes())
        self.assertEqual(record["status"],"VERIFIED_MATRIX_SLICE")
        self.assertEqual(record["source"]["sha256"],fibre.DIGEST)
        self.assertEqual(record["source"]["size_bytes"],fibre.SIZE)
        sample = record["measurement"]
        self.assertEqual(sample["input_columns"],[0,1])
        self.assertEqual(sample["output_row"],0)
        self.assertTrue(all(v["shape"] == [12449,1941] for v in sample["channels"].values()))
        for expected in record["predictions"]:
            actual = fibre.response(sample,expected["phase_error_deg"])
            for k in expected:
                self.assertTrue(math.isclose(expected[k],actual[k],rel_tol=1e-12))
