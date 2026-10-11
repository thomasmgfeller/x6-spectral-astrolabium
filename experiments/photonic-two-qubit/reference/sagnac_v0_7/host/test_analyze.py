import copy
import json
from pathlib import Path
import unittest
from analyze import InvalidRecord,analyze,summarize,correlation

ROOT=Path(__file__).resolve().parents[1]
class HostTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records=json.loads((ROOT/"examples/synthetic_chsh_snapshots.json").read_text())["records"]
    def test_conditional_is_not_all_trials(self):
        r=analyze(self.records)
        self.assertTrue(r["conditional_coincidences"]["model_conditional_gate"])
        self.assertFalse(r["all_trials_fixed_assignment"]["model_conditional_gate"])
        self.assertEqual(r["physical_quantum_claim"],"NOT_ASSESSED")
    def test_every_integrity_bit_blocks(self):
        for bit in range(8):
            with self.subTest(bit=bit):
                r=copy.deepcopy(self.records);r[0]["flags"]=1<<bit
                with self.assertRaises(InvalidRecord):analyze(r)
    def test_counter_and_configuration_tampering(self):
        changes=[("complete",False),("setting_index",1),("calibration_id","8"),
                 ("origin","unknown"),("flags",False)]
        for key,val in changes:
            with self.subTest(key=key):
                r=copy.deepcopy(self.records);r[0][key]=val
                with self.assertRaises(InvalidRecord):analyze(r)
        for index in (0,16,17,18,22,23):
            with self.subTest(counter=index):
                r=copy.deepcopy(self.records);r[0]["counters"][index]=str(int(r[0]["counters"][index])+1)
                with self.assertRaises(InvalidRecord):analyze(r)
    def test_missing_coincidences(self):
        r=copy.deepcopy(self.records)
        for rec in r:
            n=int(rec["counters"][16]);rec["counters"]=["0"]*24
            rec["counters"][0]=str(n);rec["counters"][16]=str(n)
        report=analyze(r)
        self.assertEqual(report["conditional_coincidences"]["status"],"INSUFFICIENT_DATA")
        self.assertAlmostEqual(report["all_trials_fixed_assignment"]["S"],2)
        self.assertFalse(report["all_trials_fixed_assignment"]["model_conditional_gate"])
    def test_boundaries_no_zero_sigma(self):
        self.assertIsNone(correlation(100,0)["sigma_normal_approx"])
        self.assertIsNone(correlation(0,0)["E"])
    def test_no_automatic_five_percent_rule(self):
        rec=json.loads((ROOT/"validation/same_channel_repeat_61.json").read_text())
        r=summarize(rec)
        self.assertEqual(r["repeat_fraction_observed"],1)
        self.assertEqual(r["multiport_trials"],0)
        self.assertEqual(r["nine_categories"]["+0"],61)
    def test_alpha_validation(self):
        for alpha in (0,1,-1,float("nan"),True):
            with self.subTest(alpha=alpha):
                with self.assertRaises(InvalidRecord):analyze(self.records,alpha)
    def test_classical_always_minus(self):
        r=copy.deepcopy(self.records)
        for rec in r:
            n=int(rec["counters"][16]);c=[0]*24
            c[10]=c[16]=c[19]=c[21]=n
            rec["counters"]=[str(x) for x in c]
        result=analyze(r)
        self.assertEqual(result["conditional_coincidences"]["S"],2)
        self.assertFalse(result["conditional_coincidences"]["model_conditional_gate"])

if __name__=="__main__":unittest.main(verbosity=2)
