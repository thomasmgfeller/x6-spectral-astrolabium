import unittest
import math
import tempfile
from pathlib import Path
import numpy as np
from scipy.stats import binom
from chsh_check import evaluate, lower_cp, read_csv, SETTINGS

class Tests(unittest.TestCase):
    def fixture(self, good=8536, n=10000):
        d={}
        for s in SETTINGS:
            a=good//2; b=good-a; c=(n-good)//2; e=n-good-c
            d[s]=[a,c,e,b] if s=='11' else [c,a,b,e]
        return d

    def test_singlet_synthetic(self):
        r=evaluate(self.fixture(),'synthetic')
        self.assertAlmostEqual(r['T_signed'],2.8288,12)
        self.assertGreater(r['T_lower_99_percent'],2)
        self.assertEqual(r['overall_CHSH_acceptance'],'NOT_ASSESSED')

    def test_fixed_sign_reversed_state(self):
        r=evaluate(self.fixture(good=1464),'synthetic')
        self.assertGreater(r['abs_T_descriptive'],2)
        self.assertFalse(r['statistical_criterion_met'])

    def test_local_bound_not_accepted(self):
        self.assertFalse(evaluate(self.fixture(good=7500),'synthetic')['statistical_criterion_met'])

    def test_random_parity_not_accepted(self):
        self.assertFalse(evaluate(self.fixture(good=5000),'synthetic')['statistical_criterion_met'])

    def test_zero_and_small_n(self):
        for n in (0,1,1999):
            r=evaluate(self.fixture(good=n,n=n),'synthetic')
            self.assertEqual(r['statistical_status'],'HOLD_INSUFFICIENT_DATA')
            self.assertFalse(r['statistical_criterion_met'])

    def test_cp_endpoints(self):
        self.assertEqual(lower_cp(0,10),0)
        self.assertAlmostEqual(lower_cp(10,10),(.0025)**.1,13)
        self.assertAlmostEqual(lower_cp(1,1),.0025,14)

    def test_cp_monotonicity(self):
        values=[lower_cp(k,80) for k in range(81)]
        self.assertTrue(all(a<=b for a,b in zip(values,values[1:])))

    def test_exact_coverage_finite_grid(self):
        # Exhaust all k for n=1..50 and a grid of 103 true probabilities.
        # This verifies the implementation numerically; not a proof for all p,n.
        ps=np.concatenate(([0.,1.],np.linspace(.001,.999,101)))
        for n in range(1,51):
            lower=np.array([lower_cp(k,n) for k in range(n+1)])
            for p in ps:
                fail=float(binom.pmf(np.arange(n+1),n,p)[lower>p+1e-14].sum())
                self.assertLessEqual(fail,.0025+1e-12)

    def test_angle_sign_convention(self):
        angles=[(0,22.5),(0,-22.5),(45,22.5),(45,-22.5)]
        e=[-math.cos(math.radians(2*(a-b))) for a,b in angles]
        self.assertAlmostEqual(-e[0]-e[1]-e[2]+e[3],2*math.sqrt(2),13)

    def test_malformed_counts_rejected(self):
        for bad in (-1,1.0,True,float('nan')):
            d=self.fixture();d['00'][0]=bad
            with self.assertRaises(ValueError):evaluate(d,'synthetic')
        d=self.fixture();del d['11']
        with self.assertRaises(ValueError):evaluate(d,'synthetic')

    def test_csv_duplicate_and_float_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'counts.csv'
            for txt in ('setting,pp,pm,mp,mm\n00,1,2,3,4\n00,1,2,3,4\n',
                        'setting,pp,pm,mp,mm\n00,1.0,2,3,4\n'):
                p.write_text(txt)
                with self.assertRaises(ValueError):read_csv(p)

if __name__=='__main__':unittest.main()
