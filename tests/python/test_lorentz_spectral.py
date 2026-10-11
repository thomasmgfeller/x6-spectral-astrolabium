"""Literature targets and independent analytic checks for Lorentzian tracks."""
import random
import time
import unittest

import numpy as np

from agent import lorentz_spectral as l


class TestBudget:
    def __init__(self, seconds=20):
        self.end = time.monotonic() + seconds

    def check(self):
        if time.monotonic() >= self.end:
            raise TimeoutError("test budget")


class LorentzTests(unittest.TestCase):
    def test_exact_polynomials_known_operators(self):
        b = TestBudget()
        self.assertEqual(l.charpoly([[0, 1], [1, 0]], b), (1, 0, -1))
        self.assertEqual(l.charpoly([[0, 1], [-1, 0]], b), (1, 0, 1))
        self.assertEqual(l.charpoly([[0, 1, 1], [0, 0, 1], [0, 0, 0]], b), (1, 0, 0, 0))
        large = 2**60 + 1
        self.assertEqual(l.charpoly([[large, 0], [0, -large]], b), (1, 0, -large**2))

    def test_order_validation(self):
        for bad in [[[0, 1], [1, 0]], [[1, 0], [0, 0]],
                    [[0, 1, 0], [0, 0, 1], [0, 0, 0]]]:
            with self.assertRaises(ValueError):
                l.validate_order(bad)
        np.testing.assert_array_equal(l.validate_order([[0, 1], [0, 0]]), [[0, 1], [0, 0]])

    def test_complete_small_order_literature_replication(self):
        result = l.finite_order_track(random.Random(19), TestBudget())
        self.assertEqual([r["nonisomorphic_orders"] for r in result["rows"]], [5, 16, 63])
        self.assertEqual([r["spectral_classes"] for r in result["rows"]], [4, 14, 53])
        self.assertEqual(len(result["records"]), 84)
        # Opposite 3-element forks are nonisomorphic although all 3 spectra coincide.
        fork = np.array([[0, 1, 1], [0, 0, 0], [0, 0, 0]])
        b = TestBudget()
        self.assertNotEqual(l.canonical_key(fork, b), l.canonical_key(fork.T, b))
        self.assertEqual(l.spectral_key(fork, b), l.spectral_key(fork.T, b))
        self.assertEqual(l.endpoints(fork), (1, 2))
        self.assertEqual(l.endpoints(fork.T), (2, 1))

    def test_analytic_diamond_modes_and_measure(self):
        truth = l.continuum_eigenvalues()
        self.assertAlmostEqual(truth[0], 1 / 1.165561185207211, places=12)
        self.assertAlmostEqual(truth[1], 1 / np.pi, places=12)
        points = [[-0.5, -0.5], [0.5, 0.5]]
        c = l.causal_diamond(points)
        np.testing.assert_array_equal(c, [[0, 1], [0, 0]])
        # V/N = 2 and Delta=(C.T-C)/2 -> eigenvalues exactly +/-1.
        np.testing.assert_allclose(np.linalg.eigvalsh(1j*(c.T-c)), [-1, 1], atol=1e-14)
        # A spacelike pair is unrelated; use both null coordinates.
        self.assertFalse(l.causal_diamond([[-0.5, 0.5], [0.5, -0.5]]).any())

    def test_frozen_reference_and_independent_comparison(self):
        a = l.propagator_track(0, TestBudget())
        b = l.propagator_track(1, TestBudget())
        ref_a = [r for r in a["records"] if r["sequence"] == "reference"]
        ref_b = [r for r in b["records"] if r["sequence"] == "reference"]
        self.assertEqual(ref_a, ref_b)
        other = [r for r in a["records"] if r["sequence"] == "comparison"]
        self.assertFalse({r["seed"] for r in ref_a} & {r["seed"] for r in other})
        self.assertNotEqual(a["records"], b["records"])
        self.assertEqual(len(a["records"]), 12)

    def test_enumeration_and_deadline_limits(self):
        with self.assertRaises(ValueError):
            l.enumerate_orders(6, TestBudget())
        with self.assertRaises(TimeoutError):
            l.enumerate_orders(5, TestBudget(-1))


if __name__ == "__main__":
    unittest.main()
