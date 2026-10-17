"""Analytic and structural oracles; never generates the registered target cohort."""
import math
from decimal import Decimal, localcontext
import unittest
import numpy as np
from scipy.linalg import block_diag, eigh
from threadpoolctl import threadpool_limits
from core import (entropy, sj_state, commutator, diamond_order, validate_order,
                  regional_diagnostics, numerical_zero)


def oscillator(g):
    k = np.array([[1+g, -g], [-g, 1+g]])
    d, u = eigh(k)
    q = (u*(.5/np.sqrt(d)))@u.T
    p = (u*(.5*np.sqrt(d)))@u.T
    omega = np.block([[np.zeros((2, 2)), np.eye(2)], [-np.eye(2), np.zeros((2, 2))]])
    h = 1j*omega
    return block_diag(q, p) + h/2, h


def decimal_oracle():
    with localcontext() as ctx:
        ctx.prec = 70
        r = Decimal(3).sqrt()
        nu = (2+r+1/r).sqrt()/4
        plus, minus = nu+Decimal('.5'), nu-Decimal('.5')
        return str(plus*plus.ln()-minus*minus.ln())


class GaussianTests(unittest.TestCase):
    def test_analysis_slope_and_incomplete_gate(self):
        from analyze import slope, summarize
        import json
        from pathlib import Path
        x=np.array([1.,2.,4.,8.])
        self.assertAlmostEqual(slope(x, 2+x/3),1/3)
        cfg=json.loads((Path(__file__).parent/'contract.json').read_text())
        self.assertEqual(summarize([],cfg)['status'],'INCOMPLETE')

    def test_ledger_rejects_missing_or_duplicate_cases(self):
        from check import check_records
        import json
        from pathlib import Path
        cfg=json.loads((Path(__file__).parent/'contract.json').read_text())
        with self.assertRaisesRegex(ValueError,'exact complete cohort'):
            check_records([],cfg)
        with self.assertRaisesRegex(ValueError,'exact complete cohort'):
            check_records([{'n':256,'replicate':0}]*64,cfg)

    def test_two_oscillator_closed_form(self):
        w, h = oscillator(1)
        a = [0, 2]
        result = entropy(w[np.ix_(a, a)], h[np.ix_(a, a)])
        self.assertEqual(result.status, 'OK')
        self.assertAlmostEqual(result.entropy_nats, float(decimal_oracle()), delta=2e-12)
        self.assertAlmostEqual(entropy(w, h).entropy_nats, 0, delta=2e-12)
        self.assertNotAlmostEqual(float(np.trace(w).real), 1)

    def test_product_state(self):
        w, h = oscillator(0)
        self.assertEqual(entropy(w, h).status, 'OK')
        self.assertAlmostEqual(entropy(w[np.ix_([0, 2], [0, 2])], h[np.ix_([0, 2], [0, 2])]).entropy_nats, 0)

    def test_thermal_one_oscillator(self):
        h = np.array([[0, 1j], [-1j, 0]])
        for occupation in [.01, .5, 5]:
            w = (occupation+.5)*np.eye(2)+h/2
            expected = (occupation+1)*math.log(occupation+1)-occupation*math.log(occupation)
            self.assertAlmostEqual(entropy(w, h).entropy_nats, expected, delta=1e-11)

    def test_central_mode_refused(self):
        result = entropy([[1]], [[0]])
        self.assertEqual(result.status, 'KERNEL_MISMATCH')
        self.assertIsNone(result.entropy_nats)

    def test_common_kernel_quotient(self):
        w, h = oscillator(1)
        extended = entropy(block_diag(w, 0), block_diag(h, 0))
        self.assertEqual(extended.status, 'OK')
        self.assertEqual(extended.numerical_nullity, 1)
        self.assertAlmostEqual(extended.entropy_nats, 0, delta=1e-12)

    def test_invalid_covariance_refused(self):
        h = np.array([[0, 1j], [-1j, 0]])
        with self.assertRaisesRegex(ValueError, 'positive W'):
            entropy(h/2, h)
        with self.assertRaisesRegex(ValueError, 'CCR'):
            entropy(np.eye(2), h)
        with self.assertRaisesRegex(ValueError, 'finite'):
            entropy([[np.nan]], [[0]])

    def test_order_rejection(self):
        for c in [[[0, 1], [1, 0]], [[1]], [[0, 1, 0], [0, 0, 1], [0, 0, 0]], [[0, .5], [0, 0]]]:
            with self.assertRaises(ValueError):
                validate_order(c)

    def test_sj_and_retarded_support(self):
        points = np.array([[-.9,-.9],[-.7,.6],[.1,-.2],[.6,.7],[.9,.9]])
        c = diamond_order(points)
        w, h = sj_state(c)
        np.testing.assert_allclose(w-w.T, h, atol=1e-12)
        np.testing.assert_allclose(w, w.conj().T, atol=1e-12)
        self.assertGreaterEqual(np.linalg.eigvalsh(w).min(), -1e-12)
        np.testing.assert_array_equal(h == 0, ~(c|c.T))
        np.testing.assert_array_equal(np.triu(c.T/2, 1), 0)
        self.assertAlmostEqual(entropy(w, h).entropy_nats, 0, delta=1e-12)

    def test_permutation_and_time_reversal(self):
        c = diamond_order(np.random.default_rng(571).uniform(-1, 1, (24, 2)))
        w, h = sj_state(c)
        p = np.random.default_rng(572).permutation(len(c))
        wp, hp = sj_state(c[np.ix_(p, p)])
        np.testing.assert_allclose(wp, w[np.ix_(p, p)], atol=1e-11)
        wr, hr = sj_state(c.T)
        np.testing.assert_allclose(wr, w.conj(), atol=1e-11)
        np.testing.assert_allclose(hr, -h, atol=1e-11)
        a = np.arange(12)
        f = entropy(w[np.ix_(a,a)], h[np.ix_(a,a)], .4)
        b = entropy(wr[np.ix_(a,a)], hr[np.ix_(a,a)], .4)
        self.assertEqual(f.status, 'OK')
        self.assertAlmostEqual(f.entropy_nats, b.entropy_nats, delta=1e-10)

    def test_scale_and_cutoff_conventions(self):
        c = diamond_order(np.random.default_rng(575).uniform(-1, 1, (32, 2)))
        w, h = sj_state(c)
        a = np.arange(16)
        w, h = w[np.ix_(a,a)], h[np.ix_(a,a)]
        first, second = entropy(w, h, .3), entropy(w*.125, h*.125, .3*.125)
        self.assertEqual(first.status, 'OK')
        self.assertEqual(first.retained_rank, second.retained_rank)
        self.assertAlmostEqual(first.entropy_nats, second.entropy_nats, delta=1e-10)
        self.assertEqual(entropy(w, h, 1e6).status, 'EMPTY_PHYSICAL_ALGEBRA')
        with self.assertRaisesRegex(ValueError, 'physical cutoff'):
            entropy(w, h, 0)

    def test_regional_formula_and_independent_hermitian_oracle(self):
        c = diamond_order(np.random.default_rng(576).uniform(-1, 1, (32, 2)))
        a = np.arange(16)
        output = regional_diagnostics(c, a, (1.,))
        w, h = sj_state(c)
        # Reconstruct the global projection explicitly, unlike production's regional construction.
        d, u = eigh(h)
        keep = np.abs(d) > math.sqrt(32)/(4*math.pi)
        proj = u[:,keep]@u[:,keep].conj().T
        wc, hc = (proj@w@proj)[np.ix_(a,a)], (proj@h@proj)[np.ix_(a,a)]
        d, u = eigh(hc)
        keep = np.abs(d) > math.sqrt(16)/(4*math.pi)
        wr = u[:,keep].conj().T@wc@u[:,keep]
        hr = np.diag(d[keep])
        # Hermitian covariance construction gives +/- symplectic values, not eig(W,H).
        rr = (wr-hr/2 + (wr-hr/2).conj().T)/2
        rd, ru = eigh(rr)
        self.assertGreater(rd.min(), 0)
        root = (ru*np.sqrt(rd))@ru.conj().T
        nu = eigh(root@np.linalg.solve(hr, root), eigvals_only=True)
        nu = nu[nu > 0]
        expected = np.sum((nu+.5)*np.log(nu+.5)-(nu-.5)*np.log(nu-.5))
        actual = output['cutoffs']['1.0']['double']
        self.assertEqual(actual['status'], 'OK')
        self.assertAlmostEqual(actual['entropy_nats'], float(expected), delta=1e-10)


if __name__ == '__main__':
    with threadpool_limits(1):
        unittest.main()
