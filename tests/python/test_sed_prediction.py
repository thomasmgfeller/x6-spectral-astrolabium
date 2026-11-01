import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import numpy as np

from agent import sed_prediction as study
from agent import sed_three_station as pilot


def decisions(event,x6,snr):
    names=[a+"-"+b for a,b in study.PAIRS]
    return {"id":event,"pairs":[{"pair":n} for n in names],"x6":x6,"snr":snr}


class PredictionTests(unittest.TestCase):
    def test_reference_score_uses_one_band_and_native_sample_rate(self):
        rng=np.random.default_rng(1831)
        rate=200
        t0=-60.0
        t=t0+np.arange(95*rate)/rate
        x=rng.normal(0,0.01,len(t))+(t>=4)*np.sin(2*np.pi*4*t)
        with patch.object(pilot,"filtered_band",wraps=pilot.filtered_band) as filtering, \
             patch.object(study,"controls",side_effect=AssertionError("Evaluation during prediction")):
            features,pick=study.reference_station(x,t0,4,rate)
        self.assertEqual(filtering.call_count,1)
        self.assertEqual(filtering.call_args.args[2:],((2,8),200))
        self.assertEqual(features["status"],"OK")
        self.assertIsNotNone(pick)
        self.assertGreater(features["snr"],5)

    def test_identical_coverage_risk_and_ties(self):
        station={s:{"status":"OK","snr":v,"width_s":w} for s,v,w in
                 [("LLS",2,.01),("MUO",3,.02),("BNALP",5,None)]}
        actual=study.select("a",station)
        self.assertEqual((actual["x6"],actual["snr"]),("LLS-MUO","MUO-BNALP"))
        self.assertEqual(actual["pairs"][0]["risk_us"],30000)
        station["LLS"]={"status":"LOW_CONTRAST"}
        self.assertEqual(study.select("a",station)["x6"],"MUO-BNALP")
        station["MUO"]={"status":"NOISE_HOLD"}
        self.assertEqual(study.select("a",station),{"pairs":[],"x6":None,"snr":None})
        station={s:{"status":"OK","snr":1,"width_s":0} for s in study.sed.STATIONS}
        tied=study.select("some-id",station)
        expected=min((r["pair"] for r in tied["pairs"]),key=lambda p:study.digest(("some-id|"+p).encode()))
        self.assertEqual((tied["x6"],tied["snr"]),(expected,expected))

    def test_budget_missing_labels_and_paired_test(self):
        self.assertEqual(study.label([2.,2.10,2.05])["label"],"WITHIN")
        self.assertEqual(study.label([2.,2.100001,2.05])["label"],"EXCEEDED")
        self.assertEqual(study.label([2.,None,2.05])["label"],"INDETERMINATE")
        rows=[decisions(str(i),"LLS-MUO","MUO-BNALP") for i in range(12)]
        labels={r["id"]:{p["pair"]:study.label([0,.1,None] if p["pair"]=="MUO-BNALP" else [0,.1,.05])
                          for p in r["pairs"]} for r in rows}
        result=study.trial_result(rows,labels)
        self.assertEqual(result["snr_only_success"],0)
        self.assertEqual(result["x6_only_success"],12)
        self.assertAlmostEqual(result["p_one_sided"],1/4096)
        self.assertEqual(result["decision"],"ADVANTAGE_SUPPORTED")
        for r in rows:r["x6"]=r["snr"]
        tied=study.trial_result(rows,labels)
        self.assertEqual(tied["p_one_sided"],1)
        self.assertEqual(tied["decision"],"ADVANTAGE_NOT_DEMONSTRATED")

    def test_invalid_freeze_stops_before_control_access(self):
        with TemporaryDirectory() as tmp:
            path=Path(tmp)/"predictions.json"
            path.write_text("{}")
            with patch.object(study,"controls",side_effect=AssertionError("Controls were opened")):
                with self.assertRaisesRegex(ValueError,"Frozen predictions"):
                    study.evaluate(None,path,"a"*64)

    def test_input_schema_does_not_accept_extra_provider_fields(self):
        data={"contract_sha256":study.CONTRACT,"catalogue_sha256":"a"*64,"blocks":[
            {"half":h,"eligible_catalogue_count":0,"reviewed":[],"selected":None} for h in study.HALVES]}
        study.check_selection(data)
        data["blocks"][0]["waveform"]=[1]
        with self.assertRaises(ValueError):study.check_selection(data)
        with self.assertRaises(ValueError):
            study.trial_result([decisions("x","LLS-MUO","MUO-BNALP")],{"x":{
                p:{"spread_us":100001,"label":"WITHIN"} for p in ("LLS-MUO","LLS-BNALP","MUO-BNALP")}})
