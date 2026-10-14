import copy
import itertools
import json
from pathlib import Path
import random
import unittest

import numpy as np

from research.lorentz_n6 import atlas, verify


class AtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads((Path(__file__).resolve().parents[2]/
                             "research/lorentz_n6/results/atlas_n6.json").read_text())

    def test_independent_complete_corpus(self):
        result = verify.verify(self.doc)
        self.assertEqual(result["natural_orders_checked"], 4824)
        self.assertEqual(result["exact_polynomials_checked"], 4208)

    def test_deterministic_regeneration(self):
        self.assertEqual(json.loads(json.dumps(atlas.build())), self.doc)

    def test_relabeling_and_time_orientation(self):
        c = [[0, 1, 1], [0, 0, 0], [0, 0, 0]]
        key = atlas.canonical(c)
        for p in itertools.permutations(range(3)):
            self.assertEqual(atlas.canonical([[c[i][j] for j in p] for i in p]), key)
        reverse = np.array(c).T.tolist()
        self.assertNotEqual(atlas.canonical(reverse), key)
        self.assertFalse(verify.isomorphic(c, reverse))

    def test_quill_is_single_hasse_link_and_closure(self):
        c = np.array([[0, 1, 1], [0, 0, 1], [0, 0, 0]])
        for i in range(3):
            for direction in ("past", "future"):
                q = atlas.quill(c, i, direction)
                self.assertEqual(q.tolist(), verify.closure_quill(c.tolist(), i, direction))
                np.testing.assert_array_equal(q[:3, :3], c)
                links = q & ~(q @ q > 0)
                self.assertEqual(int(links[3].sum()+links[:, 3].sum()), 1)

    def test_independent_polynomials_adversarial_integers(self):
        rng = random.Random(777)
        for n in range(1, 8):
            matrix = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
            self.assertEqual(list(atlas.charpoly(matrix, atlas.Budget())), verify.polynomial(matrix))
        huge = 2**60+1
        self.assertEqual(verify.polynomial([[huge, 0], [0, -huge]]), [1, 0, -huge**2])

    def test_duplicate_graph_is_not_hidden_by_different_id(self):
        bad = copy.deepcopy(self.doc)
        bad["records"][1]["causal_matrix"] = bad["records"][0]["causal_matrix"]
        with self.assertRaisesRegex(ValueError, "duplicate isomorphism"):
            verify.verify(bad)

    def test_polynomial_tampering_rejected(self):
        bad = copy.deepcopy(self.doc)
        bad["records"][0]["polynomials_S_A_K"][0][-1] += 1
        with self.assertRaisesRegex(ValueError, "polynomial mismatch"):
            verify.verify(bad)

    def test_missing_quill_rejected(self):
        bad = copy.deepcopy(self.doc)
        bad["records"][0]["quills"].pop()
        with self.assertRaisesRegex(ValueError, "missing or duplicate quill"):
            verify.verify(bad)

    def test_incomplete_enumeration_rejected(self):
        bad = copy.deepcopy(self.doc)
        bad["records"].pop()
        with self.assertRaises(ValueError):
            verify.verify(bad)

    def test_bounded_scope(self):
        with self.assertRaises(ValueError):
            atlas.enumerate_orders(7, atlas.Budget())
        with self.assertRaises(TimeoutError):
            atlas.enumerate_orders(6, atlas.Budget(-1))


if __name__ == "__main__":
    unittest.main()
