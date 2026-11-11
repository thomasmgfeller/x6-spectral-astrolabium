#!/usr/bin/env python3
"""Regression and independent finite algebra checks for the declared auxiliary test."""
from pathlib import Path
from fractions import Fraction as F
import argparse
import copy
import io
import json
import tempfile
import unittest
import numpy as np
import normalize_cst_dust_8x8 as n


class NormalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads((n.ROOT/'inputs/label_quotient.json').read_text())
        cls.meta = json.loads((n.ROOT/'inputs/geometry_z1.json').read_text())
        with np.load(n.ROOT/'inputs/geometry_z1.npz', allow_pickle=False) as d:
            cls.arr = {k: d[k] for k in d.files}
        cls.a0 = n.read_input(n.ROOT/'inputs/geometry_z1.npz', n.ROOT/'inputs/geometry_z1.json')

    def test_01_seven_orbits_four_selected(self):
        g, parent, e, j, r = n.selection(self.source)
        self.assertEqual(r['selected_source_orbit_indices'], [0, 3, 2, 6])
        self.assertEqual(r['excluded_source_orbit_indices'], [1, 4, 5])
        np.testing.assert_array_equal(np.diag(g), [1/8, 1/8, 1/4, 1/4]*2)
        self.assertEqual(r['parent_gram7_diagonal_exact'][1], '1/4')

    def test_02_embedding_pullback_and_isometry(self):
        g, parent, e, j, _ = n.selection(self.source)
        self.assertEqual(e.shape, (14, 8))
        np.testing.assert_array_equal(e.T @ parent @ e, g)
        np.testing.assert_allclose(j.T @ parent @ j, np.eye(8), atol=1e-14)
        self.assertGreater(np.linalg.norm(g-np.eye(8)), 1)

    def test_03_orbit_weight_tampering_rejected(self):
        bad = copy.deepcopy(self.source)
        bad['cases'][2]['orbits'][0]['indicator_norm_squared'] = '1/4'
        with self.assertRaises(ValueError): n.selection(bad)

    def test_04_transport_preserves_source_map(self):
        d, _ = n.calculate(self.source, self.a0, 'transport')
        np.testing.assert_allclose(d['normalized_from_coefficients'], self.a0, atol=2e-14)
        self.assertGreater(np.linalg.norm(d['A_indicator']-self.a0), 10)

    def test_05_coefficient_assignment_known_block(self):
        d, _ = n.calculate(self.source, self.a0, 'assign_coefficients')
        block = d['normalized_from_coefficients'][np.ix_([0, 2], [0, 2])]
        np.testing.assert_allclose(block, [[35, 13*np.sqrt(2)], [26*np.sqrt(2), 20]], atol=1e-13)

    def test_06_covariant_assignment_legacy_block(self):
        d, _ = n.calculate(self.source, self.a0, 'assign_covariant')
        block = d['normalized_from_coefficients'][np.ix_([0, 2], [0, 2])]
        np.testing.assert_allclose(block, [[280, 104*np.sqrt(2)], [104*np.sqrt(2), 80]], atol=1e-12)

    def test_07_two_conventions_agree_for_noncommuting_metrics(self):
        gin = np.array([[2, .25j], [-.25j, 1]])
        gout = np.array([[3, .5], [.5, 2]])
        a = np.array([[1, 2j], [.3, 4]])
        np.testing.assert_allclose(n.normalize_coefficients(a, gin, gout),
                                   n.normalize_covariant(gout@a, gin, gout), atol=1e-13)

    def test_08_unequal_products_algebra_positive_control(self):
        gin, gout = np.diag([2, 3]), np.diag([5, 7])
        u = np.array([[1, 1j], [1j, 1]])/np.sqrt(2)
        a = n.roots(gout)[1] @ u @ n.roots(gin)[0]
        np.testing.assert_allclose(a.conj().T @ gout @ a, gin, atol=1e-14)
        np.testing.assert_allclose(n.normalize_coefficients(a, gin, gout), u, atol=1e-14)

    def test_09_nonhermitian_gram_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Hermitian'):
            n.roots([[1, 1], [0, 1]])

    def test_10_nonpositive_or_unsafe_gram_rejected(self):
        for x in (0, -1, 1e-15):
            with self.subTest(eigenvalue=x), self.assertRaises(ValueError):
                n.roots(np.diag([1, x]))

    def test_11_nonfinite_gram_rejected(self):
        for x in (np.nan, np.inf):
            with self.assertRaises(ValueError): n.roots(np.diag([1, x]))

    def test_12_basis_permutation_covariance(self):
        p = [4, 2, 7, 1, 6, 0, 5, 3]
        d, m = copy.deepcopy(self.arr), copy.deepcopy(self.meta)
        for k in ('K', 'G_in_diagnostic', 'G_out_diagnostic'):
            d[k] = d[k][np.ix_(p, p)]
        for k in ('basis', 'stratum_index', 'geometry_index', 'matter_index'):
            d[k] = d[k][p]
        m['basis'] = d['basis'].tolist()
        m['basis_layout'] = 'explicit_permutation'
        d['basis_layout'] = np.array('explicit_permutation')
        np.testing.assert_array_equal(n.canonical_input(d, m), self.a0)
        g = n.selection(self.source)[0]
        a = n.calculate(self.source, self.a0, 'transport')[0]['A_indicator']
        got = n.normalize_coefficients(a[np.ix_(p, p)], g[np.ix_(p, p)], g[np.ix_(p, p)])
        np.testing.assert_allclose(got, self.a0[np.ix_(p, p)], atol=2e-14)

    def test_13_duplicate_basis_and_wrong_indices_rejected(self):
        d, m = copy.deepcopy(self.arr), copy.deepcopy(self.meta)
        d['basis'][0] = d['basis'][1]; m['basis'] = d['basis'].tolist()
        with self.assertRaises(ValueError): n.canonical_input(d, m)
        d = copy.deepcopy(self.arr); d['stratum_index'][0] = 1
        with self.assertRaises(ValueError): n.canonical_input(d, self.meta)

    def test_14_wrong_role_convention_clock_rejected(self):
        for key, value in [('dataset_role', 'PHYSICAL'), ('diagnostic_operator_convention', 'covariant'),
                           ('delta_chi', 1.0), ('physical_clock', 'assumed')]:
            m = copy.deepcopy(self.meta); m[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError): n.canonical_input(self.arr, m)

    def test_15_bad_kernel_shape_values_rejected(self):
        for bad in (np.eye(7), np.full((8, 8), np.nan), self.a0 + np.eye(8)):
            d = copy.deepcopy(self.arr); d['K'] = bad
            with self.assertRaises(ValueError): n.canonical_input(d, self.meta)

    def test_16_hash_rejection_leaves_no_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); meta = copy.deepcopy(self.meta); meta['npz_sha256'] = '0'*64
            (root/'bad.json').write_bytes(n.json_bytes(meta))
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                n.generate(outdir=root/'output', json_path=root/'bad.json')
            self.assertFalse((root/'output').exists())

    def test_17_true_mixing_masks_not_tensor_residual(self):
        for mode in n.MODES:
            d, r = n.calculate(self.source, self.a0, mode)
            self.assertEqual(r['diagnostics']['stratum_mixing_fro'], 0)
        a = self.a0.copy(); a[0, 4] = 3; a[4, 0] = 4; a[0, 1] = 12
        m = n.mixing(a)
        self.assertEqual(m['stratum_mixing_fro'], 5)
        self.assertEqual(m['test_label_mixing_fro'], 12)
        self.assertEqual(m['either_label_mixing_fro'], 13)

    def test_18_legacy_wrong_order_false_mixing_reproduced(self):
        inv = np.diag(1/np.sqrt([1/8]*4+[1/4]*4))
        old = inv @ self.a0 @ inv
        false_residual = np.linalg.norm(old - np.kron(old[np.ix_([0, 4], [0, 4])], np.eye(4)))
        self.assertAlmostEqual(false_residual, 502.31464243041927, places=10)
        self.assertEqual(n.mixing(old)['stratum_mixing_fro'], 0)

    def test_19_independent_singular_polynomial_controls(self):
        # Exact trace/determinant of each 2x2 U*U; roots independently fix singular values.
        for mode, trace, det in [('transport', 2977, 576), ('assign_coefficients', 3315, 576),
                                  ('assign_covariant', 128064, 589824)]:
            d, r = n.calculate(self.source, self.a0, mode)
            eig = np.array([(trace+np.sqrt(trace*trace-4*det))/2,
                            2*det/(trace+np.sqrt(trace*trace-4*det))])
            expected = np.repeat(np.sqrt(eig), 4)
            np.testing.assert_allclose(r['diagnostics']['singular_values'], expected, rtol=2e-13)
            self.assertAlmostEqual(r['diagnostics']['unitarity_defect_2']/(eig[0]-1), 1, places=13)
            self.assertGreater(eig[0]/eig[1], 1e3)  # no single scalar makes both singular values one

    def test_20_diagonal_product_obstruction_exact(self):
        a, b, c, d = map(F, (35, 26, 26, 20))
        self.assertEqual((a*b, c*d), (F(910), F(520)))
        self.assertTrue(a*b > 0 and c*d > 0)
        self.assertEqual(a*d-b*c, 24)

    def test_21_deterministic_exports_no_physical_upgrade(self):
        with tempfile.TemporaryDirectory() as tmp:
            for mode in n.MODES:
                first, second = Path(tmp)/'first', Path(tmp)/'second'
                r = n.generate(mode, first); n.generate(mode, second)
                stem = f'cst_dust_auxnorm_{mode}_z1'
                for suffix in ('.npz', '.json'):
                    self.assertEqual((first/(stem+suffix)).read_bytes(), (second/(stem+suffix)).read_bytes())
                self.assertEqual(r['physical_gates'], n.GATES)
                self.assertIsNone(r['delta_chi'])
                self.assertEqual(r['physical_K_0plus'], 'NOT_COMPUTED')
                with np.load(first/(stem+'.npz'), allow_pickle=False) as data:
                    self.assertNotIn('delta_chi', data.files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    names = unittest.defaultTestLoader.getTestCaseNames(NormalizationTests)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(NormalizationTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {'tests_run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
              'status': 'PASS' if result.wasSuccessful() else 'FAIL', 'test_names': names,
              'scope': 'finite auxiliary algebra, input rejection and reproducibility; not physical validation',
              'producer_sha256': n.sha(__file__)}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_bytes(n.json_bytes(report))
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__': main()
