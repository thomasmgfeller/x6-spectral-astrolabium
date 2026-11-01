import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import h5py
import numpy as np

from agent import hanford as h


class HanfordTests(unittest.TestCase):
    def test_published_windows_and_summaries(self):
        self.assertGreaterEqual(h.sync(h.DEFAULT_ARCHIVE, None, 0, verify_only=True), 2)
        for entry in json.loads((h.DEFAULT_ARCHIVE / "index.json").read_bytes())["records"][:2]:
            rec = json.loads((h.DEFAULT_ARCHIVE / entry["file"]).read_bytes())
            self.assertEqual(rec["source"]["hdf5_sha256"], h.PILOT[rec["source"]["file_gps_start"]])
            self.assertEqual(rec["catalog"]["waveform"], h.FAMILY)

    def test_kernel_against_independent_direct_sums(self):
        n = np.arange(4 * h.RATE)
        x = 4e-22 * np.sin(n * (2*np.pi*235/h.RATE) + 0.6)
        response = h.summary(x, 2.0)["peak_amplitude_strain"]
        taper = np.hanning(256)
        phase = 2*np.pi*235*np.arange(256)/h.RATE
        peaks = []
        for i in range(7041, 9089):
            chunk = x[i:i+256] * taper
            peaks.append(2*np.hypot(chunk @ np.cos(phase), chunk @ np.sin(phase)) / sum(taper))
        self.assertAlmostEqual(response / max(peaks), 1.0, places=9)
        self.assertAlmostEqual(response / 4e-22, 1.0, places=3)

    def test_invalid_hdf5_cannot_become_a_measurement(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "record.h5"
            with h5py.File(path, "w") as f:
                f["meta/Detector"] = b"H1"
                f["meta/GPSstart"] = 930000000
                f["meta/Duration"] = 4
                d = f.create_dataset("strain/Strain", data=np.ones(4*h.RATE))
                d.attrs.update(Xstart=930000000, Xspacing=1/h.RATE)
                for group, prefix, flags in [("simple","DQ",[b"DATA",b"BURST_CAT1"]),
                                             ("injections","Inj",[b"HW_BURST"])]:
                    base = f.require_group("quality/" + group)
                    base[prefix+"Shortnames"] = flags
                    mask = base.create_dataset(prefix+"mask", data=np.full(4,2**len(flags)-1))
                    mask.attrs.update(Xstart=930000000, Xspacing=1, Bits=len(flags))
            row = {"gps":"930000002.50"}
            self.assertEqual(h.extract(path,row,930000000)["sample_count"], 16384)
            for key, index, bad in [("quality/injections/Injmask",2,0),
                                    ("quality/simple/DQmask",0,1),("strain/Strain",10,np.nan)]:
                with h5py.File(path,"r+") as f:
                    old = f[key][index]
                    f[key][index] = bad
                with self.assertRaises(ValueError):
                    h.extract(path,row,930000000)
                with h5py.File(path,"r+") as f:
                    f[key][index] = old

    def test_failure_restart_and_idempotence(self):
        rows = [json.loads(p.read_bytes()) for p in sorted(h.DEFAULT_ARCHIVE.glob("H1-*.json"))[:2]]
        cat = ("\n".join(r["catalog"]["source_row"] for r in rows)).encode()
        with tempfile.TemporaryDirectory() as td:
            out, cache = Path(td) / "out", Path(td) / "cache"
            def catalog(_url, path, _limit):
                path.write_bytes(cat)
                return {"sha256": hashlib.sha256(cat).hexdigest()}
            with patch.object(h,"download",side_effect=catalog), patch.object(
                    h,"import_row",side_effect=[rows[0],OSError("interrupted"),rows[1]]) as importer:
                with self.assertRaises(OSError):
                    h.sync(out,cache,2)
                self.assertEqual(h.sync(out,cache,0,True),1)
                self.assertEqual(h.sync(out,cache,2),2)
                original = (out/"index.json").read_bytes()
                h.sync(out,cache,2)
                self.assertEqual(importer.call_count,3)
                self.assertEqual(original,(out/"index.json").read_bytes())
            sample = next(out.glob("H1-*.json"))
            sample.write_bytes(sample.read_bytes()+b" ")
            with self.assertRaisesRegex(ValueError,"SHA-256"):
                h.sync(out,cache,0,True)
