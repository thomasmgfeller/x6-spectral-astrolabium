import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
from obspy import UTCDateTime

from agent import sed_three_station as sed


class SedTests(unittest.TestCase):
    def test_change_point_and_no_signal(self):
        times = np.arange(-4*sed.RATE, 4*sed.RATE)/sed.RATE
        rng = np.random.default_rng(12017)
        x = rng.normal(0,1,len(times))
        self.assertIsNone(sed.variance_onset(x,times,0,1)[0])
        x[times>=0] *= 24
        onset, status = sed.variance_onset(x,times,0,1)
        self.assertEqual(status,"OK")
        self.assertLessEqual(abs(onset),3/sed.RATE)
        self.assertEqual(sed.variance_onset(np.zeros_like(x),times,0,1)[1],"BOUNDARY_OR_FLAT")

    def test_rms_boundary_hold_and_sustained_crossing(self):
        t = np.arange(4*sed.RATE)/sed.RATE
        x = np.zeros_like(t)
        x[t>=1] = 2
        self.assertEqual(sed.first_crossing(x,t,1,0.5,2),1)
        self.assertEqual(sed.first_crossing(x,t,1,1.5,2),"LEFT_EDGE")
        self.assertIsNone(sed.first_crossing(x,t,1,.1,.5))
        x[:]=0; x[120]=3
        self.assertIsNone(sed.first_crossing(x,t,1,.5,2))

    def test_pair_order_units_and_hold(self):
        picks = dict(LLS=[3.,3.,None], MUO=[4.,4.1,4.], BNALP=[8.,8.1,8.2])
        r = sed.compare(picks)
        self.assertEqual(r[0]["delay_s"],[1.,1.1,None])
        self.assertIsNone(r[0]["spread_ms"])
        self.assertEqual(r[2]["delay_s"],[4.,4.,4.2])
        self.assertEqual(r[2]["spread_ms"],200.)

    def test_unverified_access_stops_before_waveform(self):
        # Simulate an archive whose public metadata no longer confirms an open network.
        class Network(list):
            code="CH"
            restricted_status="partial"
            start_date=end_date=None
            @property
            def stations(self): return self
        class Inventory(list):
            @property
            def networks(self): return self
        sta = type("Station",(list,),{"code":"LLS","channels":property(lambda obj:obj)})([SimpleNamespace()])
        with patch.object(sed,"fetch") as fetch, patch.object(sed,"read_inventory",return_value=Inventory([Network([sta])])):
            with self.assertRaisesRegex(ValueError,"open status"):
                sed.calibrated_station("LLS",UTCDateTime("2017-03-06T20:12:07Z"))
        self.assertEqual(fetch.call_count,1)
        self.assertEqual(fetch.call_args.args,("station",))

    def test_publication_allowlist_and_preservation(self):
        folder = sed.ROOT/"app/causal-stability/sed-data"
        self.assertEqual({p.name for p in folder.iterdir()},{".gitignore","summary.json"})
        sample = json.loads((folder/"summary.json").read_bytes())
        sed.verify_public_result(sample)
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"result.json"
            sed.save(sample,out)
            before=out.read_bytes()
            for mapping, key in [(sample,"waveform"),(sample["pairs"][0],"source_pick"),
                                 (sample["checks"]["LLS"][0],"response_xml")]:
                mapping[key]="foreign bytes"
                with self.assertRaises(ValueError): sed.save(sample,out)
                del mapping[key]
                self.assertEqual(out.read_bytes(),before)
