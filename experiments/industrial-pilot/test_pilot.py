"""Fail-closed data/result controls plus an independent small-n power enumeration."""
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import tempfile
import unittest

import numpy as np
from scipy.stats import beta, multinomial

import pilot
import power
import replay

ROOT = Path(__file__).resolve().parent


class PilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = pilot.read(ROOT/'contract.json')
        cls.manifest = pilot.read(ROOT/'data/manifest.json')
        cls.report = pilot.read(ROOT/'evidence/pilot-report.json')

    def test_all_real_data_and_saved_report_replay(self):
        expected = replay.verify(ROOT/'data', ROOT/'evidence/fit.json',ROOT/'evidence/pilot-report.json')
        self.assertEqual(expected['units'],20)
        self.assertIs(expected['industrial_claim_supported'],False)

    def test_non_evaluation_roundoff_is_reconciled_without_changing_scores(self):
        row=dict(bearing_id='K004',record_id='test',split='validation',label='healthy',
                 scores={'x':1.0},decisions={'x':False})
        actual=copy.deepcopy(row);actual['scores']['x']=math.nextafter(1.0,math.inf);actual['decisions']['x']=True
        original_score=actual['scores']['x']
        result=replay.reconcile_decisions([row],[actual],{'x':math.nextafter(1.0,math.inf)})
        self.assertEqual(result,['K004:x']);self.assertEqual(actual['scores']['x'],original_score)

    def test_evaluation_roundoff_must_fail(self):
        row=dict(bearing_id='K005',record_id='test',split='evaluation',label='healthy',
                 scores={'x':1.0},decisions={'x':False})
        actual=copy.deepcopy(row)
        with self.assertRaisesRegex(ValueError,'UNSTABLE_EVALUATION_DECISION'):
            replay.reconcile_decisions([row],[actual],{'x':math.nextafter(1.0,math.inf)})

    def test_manifest_negative_controls(self):
        def missing(d):d['records'].pop()
        def duplicate(d):d['records'][1]['bearing_id']=d['records'][0]['bearing_id']
        def leakage(d):d['records'][0]['split']='evaluation'
        def label(d):d['records'][0]['label']='damaged'
        def identical(d):d['records'][1]['signal_sha256']=d['records'][0]['signal_sha256']
        def substitution(d):d['records'][0]['record_id']='N15_M07_F10_K001_20'
        def path(d):d['records'][0]['path']='../K001.npz'
        def rights(d):d['license']='Apache-2.0'
        def missing_attempt(d):d['records'][0]['selection_audit']=[]
        for mutation in [missing,duplicate,leakage,label,identical,substitution,path,rights,missing_attempt]:
            with self.subTest(mutation=mutation.__name__):
                d=copy.deepcopy(self.manifest);mutation(d)
                with self.assertRaises((ValueError,IndexError)):
                    pilot.validate_manifest(self.contract,d)

    def test_report_negative_controls(self):
        def incomplete(d):d['records'].pop()
        def false_claim(d):d['industrial_claim_supported']=True
        def fake_count(d):d['evaluation']['raw_rms']['false_positive']=999
        def fake_score(d):d['records'][0]['scores']['raw_rms']+=1
        def added(d):d['unregistered_success']=True
        def nan(d):d['records'][0]['scores']['raw_rms']=float('nan')
        def false_decision(d):d['records'][0]['decisions']['raw_rms']=not d['records'][0]['decisions']['raw_rms']
        for mutation in [incomplete,false_claim,fake_count,fake_score,added,nan,false_decision]:
            with self.subTest(mutation=mutation.__name__):
                d=copy.deepcopy(self.report);mutation(d)
                with tempfile.TemporaryDirectory() as tmp:
                    path=Path(tmp)/'report.json';path.write_text(json.dumps(d))
                    with self.assertRaises(ValueError):
                        replay.verify(ROOT/'data',ROOT/'evidence/fit.json',path)

    def test_raw_corruption_and_symlink(self):
        record=copy.deepcopy(self.manifest['records'][0])
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path=root/record['path']
            path.write_bytes((ROOT/'data'/record['path']).read_bytes()[:-1])
            with self.assertRaises(ValueError):pilot.load_signal(root,record)
            path.unlink();path.symlink_to(ROOT/'data'/record['path'])
            with self.assertRaises(ValueError):pilot.load_signal(root,record)

    def test_rehashed_nonfinite_and_wrong_shape_still_rejected(self):
        for x in [np.full(256000,np.nan,dtype='<f8'),np.zeros(255999,dtype='<f8')]:
            with self.subTest(shape=x.shape), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);record=copy.deepcopy(self.manifest['records'][0]);p=root/record['path']
                np.savez_compressed(p,vibration=x)
                record['bytes']=p.stat().st_size;record['sha256']=pilot.sha(p)
                record['signal_sha256']=hashlib.sha256(x.tobytes()).hexdigest()
                with self.assertRaises(ValueError):pilot.load_signal(root,record)

    def test_modified_threshold_cannot_be_evaluated(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=pilot.read(ROOT/'evidence/fit.json');d['thresholds']['raw_rms']+=1
            p=Path(tmp)/'fit.json';p.write_text(json.dumps(d))
            with self.assertRaisesRegex(ValueError,'OUTPUT_NUMBER'):
                pilot.run(ROOT/'data',p)

    def test_strict_json_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'a.json'
            for text in ['{"a":1,"a":2}','{"a":NaN}']:
                p.write_text(text)
                with self.assertRaises(ValueError):pilot.read(p)
            p.write_text('preserve')
            with self.assertRaises(FileExistsError):pilot.write_new(p,{'a':1})
            self.assertEqual(p.read_text(),'preserve')


class PlanningTests(unittest.TestCase):
    def test_saved_plan_replay(self):
        pilot.same(pilot.read(ROOT/'evidence/power-plan.json'),power.plan(),'power-plan')

    def test_367_fails_368_passes_and_no_pseudoreplication(self):
        self.assertGreater(1-0.025**(1/367),0.01)
        self.assertLessEqual(1-0.025**(1/368),0.01)
        self.assertGreater(1-0.025**(1/2),0.84)
        self.assertLess(power.negative_power(368,0.002)['power'],0.5)

    def test_paired_power_against_independent_four_cell_enumeration(self):
        n=12;probs=[0.1,0.8,0.05,0.05];alpha=0.2;smin=0.2;gmin=0.01;terms=[]
        def lo(k,a):return 0 if k==0 else beta.ppf(a,k,n-k+1)
        def hi(k,a):return 1 if k==n else beta.ppf(1-a,k+1,n-k)
        for both in range(n+1):
            for win in range(n-both+1):
                for loss in range(n-both-win+1):
                    neither=n-both-win-loss
                    if lo(both+win,alpha)>=smin and lo(win,alpha/2)-hi(loss,alpha/2)>gmin:
                        terms.append(multinomial.pmf([both,win,loss,neither],n,probs))
        expected=math.fsum(terms)
        self.assertGreater(expected,0);self.assertLess(expected,1)
        self.assertAlmostEqual(power.positive_power(n,probs,alpha,smin,gmin),expected,places=12)

    def test_planner_uses_original_v1_gates(self):
        path=ROOT.parent/'industrial-v1/evaluate.py'
        spec=importlib.util.spec_from_file_location('original_v1',path)
        v1=importlib.util.module_from_spec(spec);spec.loader.exec_module(v1)
        for n in [367,368,1163,1164]:
            k=power.negative_power(n,0.002)['largest_accepted_false_alarm_count']
            if k>=0:self.assertLessEqual(v1.cp_bounds(k,n,0.025)[1],0.01+1e-14)
            self.assertGreater(v1.cp_bounds(k+1,n,0.025)[1],0.01)
        for wins,losses,n in [(150,40,800),(200,30,800),(10,5,100)]:
            a=float(power.lower(wins,n,0.0125)-power.upper(losses,n,0.0125))
            self.assertAlmostEqual(a,v1.paired_bounds(wins,losses,n,0.025)[0],places=14)


if __name__=='__main__':unittest.main(verbosity=2)
